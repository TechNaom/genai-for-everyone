"""
Session 3.6 — Week 3 Lab: Company Policy Q&A Bot (REFERENCE SOLUTION)

This is the answer key. Look at exercise.py first and try it yourself
before reading this file.

WHAT THIS BUILD INTEGRATES FROM THE WEEK:
  - 3.2: bag-of-words vectors + cosine similarity for semantic-ish search
  - 3.3: PDF text extraction, paragraph-aware chunking, a VectorStore class
  - 3.4: format_context(), build_rag_prompt(), extract_citations(), citation
         grounding so every answer says exactly which document backs it up
  - 3.5: a re-ranking / chunk-size fix for a retrieval failure you will
         find yourself in Part 2 (no spoilers in this docstring -- go run
         validate_retrieval_baseline() first)

WHAT'S NEW IN THIS LAB:
  - Multiple separate source documents instead of one handbook. The bot
    must pick the RIGHT document, not just the right sentence -- this is
    the realistic failure surface real policy bots hit, because real
    company docs are written by different teams, at different times, and
    sometimes repeat or cross-reference each other.
  - A "which policy?" tag on every answer, so a user (or your QA process)
    can immediately tell if the bot pulled from the wrong document.
"""

import os
import re
import math
from collections import Counter
from pypdf import PdfReader

DOC_DIR = os.path.join(os.path.dirname(__file__), "policy_docs")

STOPWORDS = set("""
a an the is are was were be been being of to in on for and or with as at by
from this that these those it its if then than so such not no may might
will would should could can does do did has have had your you employees
employee company policy
""".split())


# ---------------------------------------------------------------------------
# Part 1: Load and chunk the corpus (builds on 3.3)
# ---------------------------------------------------------------------------

def load_documents(doc_dir: str = DOC_DIR) -> dict:
    """Load every PDF in doc_dir. Returns {filename: full_text}."""
    docs = {}
    for fname in sorted(os.listdir(doc_dir)):
        if fname.endswith(".pdf"):
            reader = PdfReader(os.path.join(doc_dir, fname))
            docs[fname] = "\n".join(page.extract_text() or "" for page in reader.pages)
    return docs


def chunk_text(text: str, target_words: int = 80, overlap_words: int = 20) -> list:
    """
    Paragraph-aware chunking with overlap (same approach as 3.3).

    NOTE: this default target_words=80 is what we'll deliberately break
    in Part 2 -- watch what happens when a section like "Home Office
    Equipment Stipend" gets buried inside a much bigger chunk.
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
    """
    Returns a flat list of dicts: {"doc": filename, "text": chunk_text}
    across ALL documents. Keeping the source doc name attached to every
    chunk is what lets us answer "which policy does this come from?"
    """
    corpus = []
    for fname, text in docs.items():
        for chunk in chunk_text(text, target_words=target_words):
            corpus.append({"doc": fname, "text": chunk})
    return corpus


# ---------------------------------------------------------------------------
# Part 2: Embedding + retrieval (builds on 3.2/3.3)
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


class PolicyVectorStore:
    """A tiny in-memory vector store across multiple source documents."""

    def __init__(self, corpus_chunks: list):
        self.entries = []
        for item in corpus_chunks:
            self.entries.append({
                "doc": item["doc"],
                "text": item["text"],
                "vector": vectorize(item["text"]),
            })

    def search(self, query: str, k: int = 3) -> list:
        """
        Returns top-k entries as dicts with "doc", "text", "score",
        sorted by descending cosine similarity to the query.
        """
        qvec = vectorize(query)
        scored = [
            {"doc": e["doc"], "text": e["text"], "score": cosine_sim(qvec, e["vector"])}
            for e in self.entries
        ]
        scored.sort(key=lambda x: -x["score"])
        return scored[:k]


# ---------------------------------------------------------------------------
# Part 3: Citation-grounded answer generation (builds directly on 3.4)
# ---------------------------------------------------------------------------

def format_context(results: list) -> str:
    """
    Numbers each retrieved chunk [1], [2], [3]... and tags it with its
    source document, WITHOUT leaking similarity scores into the prompt
    (same rule as 3.4 -- the model should never see "0.42", because it
    has no idea what that number means and may parrot it back).
    """
    lines = []
    for i, r in enumerate(results, start=1):
        doc_label = r["doc"].replace("_", " ").replace(".pdf", "").title()
        lines.append(f"[{i}] (Source: {doc_label}) {r['text']}")
    return "\n\n".join(lines)


def build_rag_prompt(question: str, context: str) -> str:
    return f"""You are a company policy assistant. Answer the employee's
question using ONLY the information in the numbered context below. Every
sentence in your answer must end with a citation marker like [1] or [2]
pointing to the context entry it came from. If the context does not
contain enough information to answer, say so plainly instead of guessing.

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


def answer_question(store: PolicyVectorStore, question: str, k: int = 3) -> dict:
    """
    The full pipeline: retrieve -> format -> prompt -> generate -> verify
    citations against real retrieved chunks.
    """
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
# Part 4: The 3.5 fix -- re-chunking to repair a retrieval miss
# ---------------------------------------------------------------------------
#
# If you ran validate_retrieval_baseline() (see exercise.py Part 0), you
# found that "What is the home office equipment stipend amount?" retrieves
# the WRONG document. Here's why, and the fix -- and the real cause is
# more interesting than "the chunks were too big."
#
# WHY IT FAILS: chunk_text() splits on blank lines (\n\s*\n) because that's
# how paragraphs look in clean markdown or plain text. But PDF text
# extraction does NOT reliably preserve blank lines between sections --
# pypdf's extract_text() returns the whole document as single newlines
# between visual lines, with no blank line marking where one numbered
# section ends and the next begins. So re.split(r"\n\s*\n", text) finds
# exactly ONE "paragraph": the entire five-section document. target_words
# never gets a chance to act, because there's no second paragraph to even
# consider starting a new chunk with -- the whole 222-word document becomes
# one chunk no matter what target_words is set to. (Try changing
# target_words to 80, 50, 25, even 10 -- the chunk boundaries don't move,
# because the bug is upstream of target_words entirely.)
#
# Inside that one giant chunk, "stipend" is one topic out of five, so its
# contribution to the bag-of-words vector is diluted. Meanwhile,
# expense_policy.pdf's short "Equipment Purchases" section is its own
# tight chunk that also mentions "stipend" once (as a cross-reference) --
# and a short, hyper-focused chunk scores higher on cosine similarity for
# a query about "stipend" and "equipment" than a diluted 222-word chunk
# does, even though it doesn't contain the actual dollar figure.
#
# THE FIX: don't assume blank-line paragraphs. Split on the document's
# actual structure -- here, numbered section headers ("1. Eligibility",
# "2. Remote Work Days", ...) -- so each policy topic becomes its own
# chunk before target_words is even applied. This is the "chunking
# errors" failure mode from 3.5: the fix isn't a magic number, it's
# matching your splitting strategy to how the source document is
# actually structured, which for PDFs is rarely "blank line = new
# paragraph."


def chunk_text_by_section(text: str) -> list:
    """
    Splits on numbered section headers (e.g. "1. Eligibility") instead of
    blank lines. This is the fix: PDF extraction rarely preserves blank
    lines between sections, so blank-line splitting silently collapses
    an entire multi-section document into one chunk.
    """
    # Split right before every "\nN. " pattern, keeping the header attached
    # to its section content.
    parts = re.split(r"(?=\n\d+\.\s)", text)
    chunks = [p.strip() for p in parts if p.strip()]
    return chunks


def build_corpus_chunks_fixed(docs: dict) -> list:
    """Same shape as build_corpus_chunks(), but using the section-aware
    chunker so each numbered policy section becomes its own chunk."""
    corpus = []
    for fname, text in docs.items():
        for chunk in chunk_text_by_section(text):
            corpus.append({"doc": fname, "text": chunk})
    return corpus


# ---------------------------------------------------------------------------
# Offline tests (no API key required)
# ---------------------------------------------------------------------------

def offline_test():
    print("=== Part 1: load_documents + chunk_text ===")
    docs = load_documents()
    assert len(docs) == 4, f"Expected 4 policy PDFs, found {len(docs)}"
    print(f"Loaded {len(docs)} documents: {list(docs.keys())}")

    corpus = build_corpus_chunks(docs)
    assert len(corpus) > 0
    print(f"Chunked into {len(corpus)} chunks at target_words=80\n")

    print("=== Part 2: PolicyVectorStore ===")
    store = PolicyVectorStore(corpus)
    results = store.search("How many sick days do I get?", k=2)
    assert len(results) == 2
    assert all("score" in r and "doc" in r and "text" in r for r in results)
    print(f"Top result for sick-day query: {results[0]['doc']} (score={results[0]['score']:.3f})")
    assert results[0]["doc"] == "leave_policy.pdf", "Sick day question should retrieve leave_policy.pdf"
    print("Correctly retrieved leave_policy.pdf.\n")

    print("=== Part 3: format_context / build_rag_prompt / extract_citations ===")
    fake_results = [
        {"doc": "leave_policy.pdf", "text": "Employees accrue 18 PTO days per year.", "score": 0.5},
        {"doc": "expense_policy.pdf", "text": "Expense reports are due within 30 days.", "score": 0.3},
    ]
    context = format_context(fake_results)
    print(context)
    assert "0.5" not in context, "Similarity score leaked into context!"
    assert "[1]" in context and "[2]" in context
    assert "Leave Policy" in context, "Doc label should be human-readable"
    print("format_context() OK.\n")

    prompt = build_rag_prompt("How many PTO days?", context)
    assert "How many PTO days?" in prompt
    assert "ONLY the information" in prompt
    print("build_rag_prompt() OK.\n")

    fake_answer = "You get 18 PTO days per year [1]. Expense reports are due in 30 days [2][2]."
    citations = extract_citations(fake_answer)
    assert citations == [1, 2], f"Expected [1, 2], got {citations}"
    no_citation = "I don't have enough information to answer that."
    assert extract_citations(no_citation) == []
    print("extract_citations() OK, including the no-citation edge case.\n")

    print("=== Part 4: the chunking fix ===")
    baseline_corpus = build_corpus_chunks(docs, target_words=80)
    fixed_corpus = build_corpus_chunks_fixed(docs)
    baseline_store = PolicyVectorStore(baseline_corpus)
    fixed_store = PolicyVectorStore(fixed_corpus)

    query = "What is the home office equipment stipend amount?"
    baseline_top = baseline_store.search(query, k=1)[0]
    fixed_top = fixed_store.search(query, k=1)[0]

    print(f"Baseline (blank-line chunking) top doc: {baseline_top['doc']} (score={baseline_top['score']:.3f})")
    print(f"Fixed    (section-aware chunking) top doc: {fixed_top['doc']} (score={fixed_top['score']:.3f})")

    assert baseline_top["doc"] == "expense_policy.pdf", (
        "Expected the baseline chunking to retrieve the WRONG document here "
        "(that's the bug we're demonstrating) -- if this fails, the corpus "
        "or chunker has changed and the lesson text needs updating."
    )
    assert fixed_top["doc"] == "remote_work_policy.pdf", (
        "Expected section-aware chunking to fix this retrieval -- if this "
        "fails, the fix no longer works and needs revisiting."
    )
    print("Confirmed: section-aware chunking fixes the retrieval miss.\n")

    print("All offline tests passed.")


# ---------------------------------------------------------------------------
# Full pipeline demo (requires ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

DEMO_QUESTIONS = [
    "How many PTO days do I get per year, and do they roll over?",
    "What is the home office equipment stipend amount?",
    "Do I need to use a VPN when working from home?",
    "Does the company offer unlimited free snacks in the office?",  # unanswerable
]


def run_demo():
    docs = load_documents()
    corpus = build_corpus_chunks_fixed(docs)  # use the fixed chunking
    store = PolicyVectorStore(corpus)

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
