"""
Session 3.6 — Week 3 Lab: Campus Student Services Q&A Bot (YOUR TURN)

You've built every piece of a RAG system across this week:
  3.2 — turning text into vectors and comparing them
  3.3 — chunking a document and storing/searching chunks
  3.4 — grounding answers in retrieved context with citations
  3.5 — diagnosing and fixing retrieval failures

This lab puts all of it together over FOUR separate campus documents
instead of one handbook: a Registration Guide, a Financial Aid Handbook,
an Academic Standing Policy, and a Housing Handbook. These documents
genuinely cross-reference each other -- dropping below full-time status
shows up in both the Registration Guide AND the Housing Handbook, for
different reasons -- which is exactly the kind of overlap that trips up
naive multi-document retrieval in the real world.

Fill in every function marked TODO. Run offline_test() first -- it
needs no API key and will tell you immediately if your retrieval and
prompt-building logic is correct. There's a real, genuinely-discovered
chunking bug waiting for you in Part 4.

Files you need (already provided, don't edit):
  campus_docs/registration_guide.pdf
  campus_docs/financial_aid_handbook.pdf
  campus_docs/academic_standing_policy.pdf
  campus_docs/housing_handbook.pdf
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
# Part 1: Load and chunk the corpus (builds on 3.3)
# ---------------------------------------------------------------------------

def load_documents(doc_dir: str = DOC_DIR) -> dict:
    """
    TODO: Load every .pdf file in doc_dir using PdfReader, extract its
    text (joining all pages with "\n"), and return {filename: full_text}.
    """
    raise NotImplementedError("Fill in load_documents()")


def chunk_text(text: str, target_words: int = 80, overlap_words: int = 20) -> list:
    """
    TODO: Paragraph-aware chunking with overlap (same approach as 3.3).

    Steps:
      1. Split text into paragraphs on blank lines: re.split(r"\\n\\s*\\n", text)
      2. Strip and drop any empty paragraphs.
      3. Accumulate paragraphs into a buffer until target_words is reached,
         then close that chunk.
      4. Carry the last overlap_words words of the closed chunk forward
         into the next chunk's buffer.
      5. Flush whatever's left in the buffer at the end (if non-trivial).

    Return a list of chunk strings.

    NOTE: this function has a real limitation on this specific corpus.
    Keep that in mind for Part 4.
    """
    raise NotImplementedError("Fill in chunk_text()")


def build_corpus_chunks(docs: dict, target_words: int = 80) -> list:
    """
    TODO: For every (filename, text) pair in docs, chunk the text with
    chunk_text(), and return a flat list of dicts:
        {"doc": filename, "text": chunk_text}
    across ALL documents.
    """
    raise NotImplementedError("Fill in build_corpus_chunks()")


# ---------------------------------------------------------------------------
# Part 2: Embedding + retrieval (builds on 3.2/3.3)
# ---------------------------------------------------------------------------

def tokenize(text: str) -> list:
    """Already implemented for you -- same tokenizer as earlier sessions."""
    words = re.findall(r"[a-z']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


def vectorize(text: str) -> Counter:
    """Already implemented for you."""
    return Counter(tokenize(text))


def cosine_sim(c1: Counter, c2: Counter) -> float:
    """Already implemented for you -- same formula as 3.2."""
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
        """
        TODO: For each item in corpus_chunks (each a {"doc", "text"} dict),
        build self.entries as a list of dicts:
            {"doc": ..., "text": ..., "vector": vectorize(text)}
        """
        raise NotImplementedError("Fill in CampusVectorStore.__init__()")

    def search(self, query: str, k: int = 3) -> list:
        """
        TODO:
          1. Vectorize the query.
          2. Score every entry by cosine_sim(query_vector, entry_vector).
          3. Sort descending by score.
          4. Return the top k as {"doc", "text", "score"} dicts.
        """
        raise NotImplementedError("Fill in CampusVectorStore.search()")


# ---------------------------------------------------------------------------
# Part 3: Citation-grounded answer generation (builds directly on 3.4)
# ---------------------------------------------------------------------------

def format_context(results: list) -> str:
    """
    TODO: Number each retrieved result [1], [2], [3]... starting at 1.
    Tag each with a human-readable source label (filename with
    underscores replaced by spaces, ".pdf" removed, title-cased --
    e.g. "housing_handbook.pdf" -> "Housing Handbook").

    Format each line: "[1] (Source: Housing Handbook) <chunk text>"
    Join all lines with a blank line between them.

    IMPORTANT: do NOT include the similarity score in the output.
    """
    raise NotImplementedError("Fill in format_context()")


def build_rag_prompt(question: str, context: str) -> str:
    """
    TODO: Build a prompt that:
      - Instructs the model to act as a campus student services assistant
      - Says to use ONLY the provided context to answer
      - Requires every sentence in the answer to end with a citation
        marker like [1] or [2]
      - Instructs the model to say plainly if it can't answer from the
        context, rather than guessing
      - Includes the context and the question

    Return the full prompt string.
    """
    raise NotImplementedError("Fill in build_rag_prompt()")


def extract_citations(answer_text: str) -> list:
    """
    TODO: Use a regex to find every [N] citation marker in answer_text,
    and return the SORTED, UNIQUE list of integers found.

    Example: "Answer [1]. More [2][2]." -> [1, 2]
    Edge case: no citations at all -> []
    """
    raise NotImplementedError("Fill in extract_citations()")


def call_llm(prompt: str) -> str:
    """Already implemented for you. Requires ANTHROPIC_API_KEY to be set."""
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def answer_question(store: "CampusVectorStore", question: str, k: int = 3) -> dict:
    """
    TODO: Wire the full pipeline together:
      1. retrieved = store.search(question, k=k)
      2. context = format_context(retrieved)
      3. prompt = build_rag_prompt(question, context)
      4. answer = call_llm(prompt)
      5. cited = extract_citations(answer)
      6. source_docs = the sorted set of unique "doc" values from
         retrieved[i-1] for every cited chunk number i (1-indexed!)

    Return a dict with keys:
      "answer", "cited_chunk_numbers", "retrieved_chunks", "source_documents"
    """
    raise NotImplementedError("Fill in answer_question()")


# ---------------------------------------------------------------------------
# Part 4: Find AND fix a real retrieval bug
# ---------------------------------------------------------------------------
#
# Once Parts 1-3 pass offline_test(), run this:
#
#   docs = load_documents()
#   corpus = build_corpus_chunks(docs)
#   store = CampusVectorStore(corpus)
#   results = store.search("What is the maximum course load for a "
#                           "student on probation?", k=1)
#   print(results[0]["doc"])
#
# It should print "academic_standing_policy.pdf" -- but with your Part 1
# chunker, it almost certainly won't.
#
# YOUR TASK:
#   1. Print out every chunk for registration_guide.pdf and look at how
#      big they are. (Hint: try chunk_text() at a few different
#      target_words values -- does the chunk boundary ever move? If not,
#      the bug isn't actually about target_words.)
#   2. Figure out why re.split(r"\n\s*\n", text) might not be doing what
#      you'd expect on text that came out of a PDF. (Hint: print
#      repr(text[:300]) for one of the loaded documents and look closely
#      at where the newlines actually are.)
#   3. Look at how THIS corpus's section headers are actually written --
#      they're different from a numbered-list style. What pattern would
#      reliably mark the start of a new section here?
#   4. Write a NEW chunking function, chunk_text_by_caps_header(), that
#      splits on that pattern instead of blank lines.
#   5. Write build_corpus_chunks_fixed() using your new chunker, and
#      confirm the probation/course-load question (and the full-time/
#      housing question) now retrieve the right documents.


def chunk_text_by_caps_header(text: str) -> list:
    """
    TODO: Split text on this corpus's actual section header style
    instead of blank lines.

    Hint: look at how a section header appears in the extracted text --
    is it numbered? Is it capitalized in some distinctive way? A regex
    like r"(?=\\n[A-Z][A-Z /]+\\n)" splits right before a line that's
    entirely uppercase (allowing spaces and slashes) without consuming
    it. Strip whitespace and drop empty chunks from the result.
    """
    raise NotImplementedError("Fill in chunk_text_by_caps_header() -- this is the fix!")


def build_corpus_chunks_fixed(docs: dict) -> list:
    """
    TODO: Same shape as build_corpus_chunks(), but using
    chunk_text_by_caps_header() instead of chunk_text().
    """
    raise NotImplementedError("Fill in build_corpus_chunks_fixed()")


# ---------------------------------------------------------------------------
# Offline tests (no API key required) -- get these passing first
# ---------------------------------------------------------------------------

def offline_test():
    print("=== Part 1: load_documents + chunk_text ===")
    docs = load_documents()
    assert len(docs) == 4, f"Expected 4 campus PDFs, found {len(docs)}"
    print(f"Loaded {len(docs)} documents: {list(docs.keys())}")

    corpus = build_corpus_chunks(docs)
    assert len(corpus) > 0
    print(f"Chunked into {len(corpus)} chunks\n")

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

    print("=== Part 4: find and fix the chunking bug ===")
    fixed_corpus = build_corpus_chunks_fixed(docs)
    fixed_store = CampusVectorStore(fixed_corpus)
    query = "What is the maximum course load for a student on probation?"
    fixed_top = fixed_store.search(query, k=1)[0]
    print(f"Fixed chunking top doc: {fixed_top['doc']} (score={fixed_top['score']:.3f})")
    assert fixed_top["doc"] == "academic_standing_policy.pdf", (
        "Your caps-header chunking should fix this retrieval -- check "
        "that chunk_text_by_caps_header() is actually isolating each "
        "section on its own."
    )
    print("Bug fixed -- the right document now wins.\n")

    print("All offline tests passed!")


if __name__ == "__main__":
    offline_test()
