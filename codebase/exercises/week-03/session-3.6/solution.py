"""
Session 3.6 — Week 3 Lab: Campus Student Services Q&A Bot (REFERENCE SOLUTION)

This is the answer key. Look at exercise.py first and try it yourself
before reading this file.

WHAT THIS BUILD INTEGRATES FROM THE WEEK:
  - 3.2: bag-of-words vectors + cosine similarity
  - 3.3: PDF text extraction, chunking, a searchable vector store
  - 3.4: citation-grounded generation (format_context, build_rag_prompt,
         extract_citations)
  - 3.5: diagnosing and fixing a genuine retrieval failure

WHAT'S NEW IN THIS LAB:
  - Four separate campus documents (Registration, Financial Aid, Academic
    Standing, Housing) that genuinely cross-reference each other -- a
    student dropping below full-time status appears in BOTH the
    Registration Guide and the Housing Handbook, for different reasons.
  - A real retrieval bug discovered by actually running this code against
    actual generated PDFs: blank-line chunking merges each document's five
    sections into one diluted blob, which causes the registration guide's
    one giant chunk to falsely win on questions that are really about
    academic probation or housing eligibility, because it touches on
    "course load" and "full-time status" in passing.
"""

import os
import re
import math
from collections import Counter
from pypdf import PdfReader

DOC_DIR = os.path.join(os.path.dirname(__file__), "campus_docs")

STOPWORDS = set("""
a an the is are was were be been being of to in on for and or with as at by
from this that these those it its if then than so such not no may might
will would should could can does do did has have had your you students
student university policy
""".split())


# ---------------------------------------------------------------------------
# Part 1: Load and chunk the corpus
# ---------------------------------------------------------------------------

def load_documents(doc_dir: str = DOC_DIR) -> dict:
    docs = {}
    for fname in sorted(os.listdir(doc_dir)):
        if fname.endswith(".pdf"):
            reader = PdfReader(os.path.join(doc_dir, fname))
            docs[fname] = "\n".join(page.extract_text() or "" for page in reader.pages)
    return docs


def chunk_text(text: str, target_words: int = 80, overlap_words: int = 20) -> list:
    """
    Blank-line, paragraph-aware chunking with overlap -- the baseline
    approach from Session 3.3.

    NOTE: this has a real limitation on this corpus. See Part 4.
    """
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    buf, buf_words = [], 0
    for para in paragraphs:
        buf.append(para)
        buf_words += len(para.split())
        if buf_words >= target_words:
            chunks.append(" ".join(buf))
            tail = " ".join(buf).split()[-overlap_words:]
            buf, buf_words = [" ".join(tail)], len(tail)
    if buf and buf_words > 5:
        chunks.append(" ".join(buf))
    return chunks


def build_corpus_chunks(docs: dict, target_words: int = 80) -> list:
    corpus = []
    for fname, text in docs.items():
        for chunk in chunk_text(text, target_words=target_words):
            corpus.append({"doc": fname, "text": chunk})
    return corpus


# ---------------------------------------------------------------------------
# Part 2: Embedding + retrieval
# ---------------------------------------------------------------------------

def tokenize(text: str) -> list:
    words = re.findall(r"[a-z']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def vectorize(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_sim(c1: Counter, c2: Counter) -> float:
    common = set(c1) & set(c2)
    dot = sum(c1[w] * c2[w] for w in common)
    mag1 = math.sqrt(sum(v * v for v in c1.values()))
    mag2 = math.sqrt(sum(v * v for v in c2.values()))
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


class CampusVectorStore:
    """A tiny in-memory vector store across multiple campus documents."""

    def __init__(self, corpus_chunks: list):
        self.entries = []
        for item in corpus_chunks:
            self.entries.append({
                "doc": item["doc"],
                "text": item["text"],
                "vector": vectorize(item["text"]),
            })

    def search(self, query: str, k: int = 3) -> list:
        qvec = vectorize(query)
        scored = [
            {"doc": e["doc"], "text": e["text"], "score": cosine_sim(qvec, e["vector"])}
            for e in self.entries
        ]
        scored.sort(key=lambda x: -x["score"])
        return scored[:k]


# ---------------------------------------------------------------------------
# Part 3: Citation-grounded answer generation
# ---------------------------------------------------------------------------

def format_context(results: list) -> str:
    lines = []
    for i, r in enumerate(results, start=1):
        doc_label = r["doc"].replace("_", " ").replace(".pdf", "").title()
        lines.append(f"[{i}] (Source: {doc_label}) {r['text']}")
    return "\n\n".join(lines)


def build_rag_prompt(question: str, context: str) -> str:
    return f"""You are a campus student services assistant. Answer the
student's question using ONLY the information in the numbered context
below. Every sentence in your answer must end with a citation marker
like [1] or [2] pointing to the context entry it came from. If the
context does not contain enough information to answer, say so plainly
instead of guessing.

Context:
{context}

Question: {question}

Answer (with citations):"""


def extract_citations(answer_text: str) -> list:
    matches = re.findall(r"\[(\d+)\]", answer_text)
    return sorted({int(m) for m in matches})


def call_llm(prompt: str) -> str:
    """Requires ANTHROPIC_API_KEY to be set in the environment."""
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def answer_question(store: CampusVectorStore, question: str, k: int = 3) -> dict:
    retrieved = store.search(question, k=k)
    context = format_context(retrieved)
    prompt = build_rag_prompt(question, context)
    answer = call_llm(prompt)
    cited = extract_citations(answer)
    source_docs = sorted({retrieved[i - 1]["doc"] for i in cited if 1 <= i <= len(retrieved)})
    return {
        "answer": answer,
        "cited_chunk_numbers": cited,
        "retrieved_chunks": retrieved,
        "source_documents": source_docs,
    }


# ---------------------------------------------------------------------------
# Part 4: The retrieval bug -- found by actually running this corpus
# ---------------------------------------------------------------------------
#
# Two test questions retrieve the WRONG document with blank-line chunking:
#
#   "What happens if I drop below full-time enrollment while living in a
#    dorm?"  -- should come from housing_handbook.pdf, but registration_
#    guide.pdf wins instead.
#
#   "What is the maximum course load for a student on probation?" --
#    should come from academic_standing_policy.pdf, but registration_
#    guide.pdf wins instead, AGAIN.
#
# WHY IT FAILS: just like the blank-line problem you may have already
# diagnosed in earlier work, pypdf's extract_text() does not reliably
# preserve blank lines between sections. registration_guide.pdf has FIVE
# sections (Add/Drop Deadlines, Course Load Requirements, Waitlists,
# Registration Holds, Transfer Credit) that all get merged into one
# 240-word chunk, because there's no blank line for the chunker's
# paragraph splitter to find. That one merged chunk happens to mention
# "course load," "full-time," and cross-references both the Academic
# Standing Policy and the Financial Aid Handbook by name -- so it scores
# deceptively well against questions that are really about OTHER
# documents, because it touches every related topic in passing without
# being the actual best answer to any of them.
#
# THIS TIME THE EARLIER FIX DOESN'T WORK AS-IS: this corpus uses
# ALL-CAPS section headers on their own line ("COURSE LOAD REQUIREMENTS"),
# not numbered headers ("1. Eligibility"). A numbered-section splitter
# would find nothing to split on here. The fix has to match THIS
# corpus's actual structure.
#
# THE FIX: split on lines that are entirely uppercase (allowing spaces
# and slashes), since that pattern survives PDF extraction and matches
# how these specific documents are actually structured.


def chunk_text_by_caps_header(text: str) -> list:
    """
    Splits on ALL-CAPS section headers on their own line (e.g.
    "COURSE LOAD REQUIREMENTS") instead of blank lines. This is the fix
    for THIS corpus -- a different splitting rule than would be needed
    for a numbered-section document, because the right chunking strategy
    always depends on how the specific source document is structured.
    """
    parts = re.split(r"(?=\n[A-Z][A-Z /]+\n)", text)
    return [p.strip() for p in parts if p.strip()]


def build_corpus_chunks_fixed(docs: dict) -> list:
    corpus = []
    for fname, text in docs.items():
        for chunk in chunk_text_by_caps_header(text):
            corpus.append({"doc": fname, "text": chunk})
    return corpus


# ---------------------------------------------------------------------------
# Offline tests (no API key required)
# ---------------------------------------------------------------------------

def offline_test():
    print("=== Part 1: load_documents + chunk_text ===")
    docs = load_documents()
    assert len(docs) == 4, f"Expected 4 campus PDFs, found {len(docs)}"
    print(f"Loaded {len(docs)} documents: {list(docs.keys())}")

    corpus = build_corpus_chunks(docs)
    assert len(corpus) > 0
    print(f"Chunked into {len(corpus)} chunks (baseline blank-line chunking)\n")

    print("=== Part 2: CampusVectorStore ===")
    store = CampusVectorStore(corpus)
    results = store.search("How many nights can an overnight guest stay?", k=2)
    assert len(results) == 2
    assert results[0]["doc"] == "housing_handbook.pdf"
    print(f"Top result for guest-policy query: {results[0]['doc']} (score={results[0]['score']:.3f})")
    print("Correctly retrieved housing_handbook.pdf.\n")

    print("=== Part 3: format_context / build_rag_prompt / extract_citations ===")
    fake_results = [
        {"doc": "financial_aid_handbook.pdf", "text": "Aid is disbursed within 10 business days.", "score": 0.5},
        {"doc": "housing_handbook.pdf", "text": "The housing deposit is $200.", "score": 0.3},
    ]
    context = format_context(fake_results)
    assert "0.5" not in context, "Similarity score leaked into context!"
    assert "[1]" in context and "[2]" in context
    assert "Financial Aid Handbook" in context
    print("format_context() OK.\n")

    prompt = build_rag_prompt("When is aid disbursed?", context)
    assert "When is aid disbursed?" in prompt
    print("build_rag_prompt() OK.\n")

    fake_answer = "Aid is disbursed within 10 days [1]. The deposit is $200 [2][2]."
    citations = extract_citations(fake_answer)
    assert citations == [1, 2], f"Expected [1, 2], got {citations}"
    assert extract_citations("I don't have enough information.") == []
    print("extract_citations() OK, including the no-citation edge case.\n")

    print("=== Part 4: the retrieval bug, and the fix ===")
    baseline_store = CampusVectorStore(build_corpus_chunks(docs, target_words=80))
    fixed_store = CampusVectorStore(build_corpus_chunks_fixed(docs))

    bug_queries = [
        ("What happens if I drop below full-time enrollment while living in a dorm?", "housing_handbook.pdf"),
        ("What is the maximum course load for a student on probation?", "academic_standing_policy.pdf"),
    ]
    for query, expected_doc in bug_queries:
        baseline_top = baseline_store.search(query, k=1)[0]
        fixed_top = fixed_store.search(query, k=1)[0]
        print(f"Q: {query}")
        print(f"  Baseline top doc: {baseline_top['doc']} (score={baseline_top['score']:.3f})")
        print(f"  Fixed    top doc: {fixed_top['doc']} (score={fixed_top['score']:.3f})")
        assert baseline_top["doc"] == "registration_guide.pdf", (
            "Expected the baseline chunker to retrieve the WRONG document "
            "here (that's the bug) -- if this fails, the corpus or chunker "
            "has changed and the lesson text needs updating."
        )
        assert fixed_top["doc"] == expected_doc, (
            f"Expected the caps-header chunker to fix this and retrieve "
            f"{expected_doc} -- if this fails, the fix no longer works."
        )
        print("  Confirmed: caps-header chunking fixes this retrieval.\n")

    print("All offline tests passed.")


# ---------------------------------------------------------------------------
# Full pipeline demo (requires ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

DEMO_QUESTIONS = [
    "What GPA puts a student on academic probation?",
    "What happens if I drop below full-time enrollment while living in a dorm?",
    "How much is the housing deposit and when is it refunded?",
    "Does the university offer free laundry service in every dorm?",  # unanswerable
]


def run_demo():
    docs = load_documents()
    corpus = build_corpus_chunks_fixed(docs)
    store = CampusVectorStore(corpus)

    for q in DEMO_QUESTIONS:
        print(f"\nQ: {q}")
        result = answer_question(store, q, k=3)
        print(f"A: {result['answer']}")
        print(f"   Cited chunks: {result['cited_chunk_numbers']}")
        print(f"   Source document(s): {result['source_documents']}")


if __name__ == "__main__":
    offline_test()
    print("\n" + "=" * 70)
    print("Offline tests above need no API key. To see live model answers,")
    print("set ANTHROPIC_API_KEY and uncomment run_demo() below.")
    print("=" * 70)
    # run_demo()
