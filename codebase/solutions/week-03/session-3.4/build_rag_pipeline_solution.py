"""
Session 3.4 — Reference Solution
Building a RAG Pipeline (Retrieve -> Augment -> Generate)
===========================================================================

Try the exercise yourself first -- the value is in implementing the
augment/generate/citation-extraction logic, not in reading someone
else's implementation.

IMPORTANT NOTE ON VERIFICATION: format_context(), build_rag_prompt(),
and extract_citations() below are pure logic with no API dependency,
and are fully tested in offline_test() with no external calls required.
The retrieval behavior described in the Pro Path Notes (which chunks
get surfaced for each test question) was also verified directly by
running build_store() and store.search() with no API needed. Only the
model's exact generated wording requires a live ANTHROPIC_API_KEY and
was not run in the environment that wrote this solution -- run it
yourself with your own key to see your own live output.
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Reproduced from Session 3.3
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)


def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list:
    words = text.split()
    chunks = []
    step = max(chunk_size - overlap, 1)
    i = 0
    while i < len(words):
        piece = words[i:i + chunk_size]
        if len(piece) >= 15:
            chunks.append(" ".join(piece))
        if i + chunk_size >= len(words):
            break
        i += step
    return chunks


def tokenize(s: str) -> list:
    return re.findall(r"[a-z']+", s.lower())


def build_vocabulary(chunks: list) -> list:
    vocab = set()
    for chunk in chunks:
        vocab.update(tokenize(chunk))
    return sorted(vocab)


def embed_chunks(chunks: list, vocab: list) -> np.ndarray:
    word_to_idx = {word: i for i, word in enumerate(vocab)}
    vectors = np.zeros((len(chunks), len(vocab)))
    for row, chunk in enumerate(chunks):
        for word in tokenize(chunk):
            if word in word_to_idx:
                vectors[row, word_to_idx[word]] += 1
    return vectors


def embed_query(query: str, vocab: list) -> np.ndarray:
    word_to_idx = {word: i for i, word in enumerate(vocab)}
    vec = np.zeros(len(vocab))
    for word in tokenize(query):
        if word in word_to_idx:
            vec[word_to_idx[word]] += 1
    return vec


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return np.dot(vec_a, vec_b) / (norm_a * norm_b)


class VectorStore:
    def __init__(self):
        self.chunks = []
        self.vectors = []

    def add(self, chunk_text: str, vector: np.ndarray):
        self.chunks.append(chunk_text)
        self.vectors.append(vector)

    def search(self, query_vector: np.ndarray, k: int = 3) -> list:
        similarities = [cosine_similarity(query_vector, v) for v in self.vectors]
        top_k_idx = np.argsort(similarities)[::-1][:k]
        return [(self.chunks[i], similarities[i]) for i in top_k_idx]


def build_store(pdf_path: str, chunk_size: int = 100, overlap: int = 20):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)

    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)

    return store, vocab


# ---------------------------------------------------------------------------
# Session 3.4 additions
# ---------------------------------------------------------------------------

def format_context(search_results: list) -> str:
    """Turn (chunk_text, score) tuples into clean numbered context."""
    parts = []
    for i, (chunk, _score) in enumerate(search_results, start=1):
        parts.append(f"[{i}] {chunk}")
    return "\n\n".join(parts)


RAG_PROMPT_TEMPLATE = """You are answering a question using ONLY the information in the provided context below. If the context does not contain enough information to answer the question, say so explicitly rather than guessing or using outside knowledge.

CONTEXT:
{context}

QUESTION: {question}

Answer the question, and cite which numbered context chunk(s) support each part of your answer using the format [1], [2], etc.
"""


def build_rag_prompt(question: str, context: str) -> str:
    return RAG_PROMPT_TEMPLATE.format(context=context, question=question)


def call_llm(prompt: str) -> str:
    """Calls the Anthropic API. Requires ANTHROPIC_API_KEY to be set."""
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def extract_citations(answer_text: str) -> list:
    """Find every [N] citation marker and return sorted unique chunk numbers."""
    matches = re.findall(r"\[(\d+)\]", answer_text)
    unique_numbers = {int(m) for m in matches}
    return sorted(unique_numbers)


def answer_question(store: "VectorStore", vocab: list, question: str, k: int = 3) -> dict:
    query_vector = embed_query(question, vocab)
    retrieved_chunks = store.search(query_vector, k=k)
    context = format_context(retrieved_chunks)
    prompt = build_rag_prompt(question, context)
    answer = call_llm(prompt)
    cited_chunk_numbers = extract_citations(answer)

    return {
        "answer": answer,
        "cited_chunk_numbers": cited_chunk_numbers,
        "retrieved_chunks": retrieved_chunks,
    }


# ---------------------------------------------------------------------------
# Offline test (no API key required) -- fully verified, no live call
# ---------------------------------------------------------------------------

def offline_test():
    print("--- Testing format_context() ---")
    fake_results = [
        ("Full-time employees accrue 18 days of PTO per year.", 0.42),
        ("Sick days do not carry over to the following year.", 0.31),
    ]
    formatted = format_context(fake_results)
    print(formatted)
    assert "0.42" not in formatted, "Similarity scores should not appear in the formatted context!"
    assert "[1]" in formatted and "[2]" in formatted, "Context should be numbered starting at 1"
    print("format_context() looks correct.\n")

    print("--- Testing build_rag_prompt() ---")
    prompt = build_rag_prompt("How many PTO days?", formatted)
    assert "How many PTO days?" in prompt
    assert "[1] Full-time employees" in prompt
    assert "ONLY the information" in prompt
    print("build_rag_prompt() looks correct.\n")

    print("--- Testing extract_citations() ---")
    fake_answer = "Employees get 18 days of PTO [1]. Sick days do not roll over [2][2]."
    citations = extract_citations(fake_answer)
    print(f"Extracted citations: {citations}")
    assert citations == [1, 2], f"Expected [1, 2], got {citations}"

    # Edge case: no citations at all
    no_citation_answer = "I don't have enough information to answer this question."
    assert extract_citations(no_citation_answer) == []
    print("extract_citations() looks correct (including the no-citation edge case).\n")

    print("All offline tests passed.")


# ---------------------------------------------------------------------------
# Full pipeline (requires ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

TEST_QUESTIONS = [
    "How many PTO days do employees get per year?",
    "What is the company's policy on remote work?",
    "Does the company offer dental insurance?",  # deliberately not in the handbook
]


def run_full_pipeline():
    store, vocab = build_store("sample_handbook.pdf", chunk_size=100, overlap=20)

    for question in TEST_QUESTIONS:
        print(f"\n{'=' * 70}")
        print(f"Q: {question}")
        result = answer_question(store, vocab, question, k=3)
        print(f"\nA: {result['answer']}")
        print(f"\nCited chunks: {result['cited_chunk_numbers']}")


# ---------------------------------------------------------------------------
# Pro path notes
# ---------------------------------------------------------------------------

PRO_PATH_NOTES = """
Pro path observations:

Note on verification: the retrieval step below (which chunks get
surfaced for each question) was verified directly by running this
code -- those results are real and reproducible by you. The model's
exact generated wording was NOT run live in the environment that wrote
this solution (no API key was available there); run it yourself with
your own key to see your own live output, which may vary somewhat
between runs even for the same prompt.

1. Verifying a citation by hand: for "How many PTO days do employees
   get per year?", retrieval (at chunk_size=100) genuinely surfaces a
   chunk containing "Full-time employees accrue 18 days of paid time
   off per calendar year..." among its top-3 results -- confirmed by
   running build_store() and store.search() directly, no API needed for
   this part. If the model cites that chunk for the "18 days" figure,
   reading the actual chunk text confirms the number really is there,
   not invented. This is what a working, checkable citation looks like.
   Run the full pipeline yourself and check: does the chunk your model
   actually cites contain the claim it's attached to?

2. Removing the "ONLY the information in the provided context"
   instruction: the dental insurance question is a clean test case for
   this, confirmed directly -- the word "dental" does not appear
   anywhere in the source handbook, and the chunks retrieved for this
   question (verified above) discuss health insurance premiums and
   401(k) matching, but never dental coverage specifically. With the
   grounding instruction in place, a well-behaved model should
   recognize the retrieved context doesn't address dental coverage and
   say so. With the instruction removed, there's a real risk the model
   instead reaches for general knowledge about typical benefits
   packages. Try both versions yourself and compare -- this is exactly
   the kind of before/after comparison that makes an instruction's
   effect visible rather than assumed.

3. Chunk-size mismatch: Session 3.3 already demonstrated, with verified
   real output, that a deliberately poor chunk size measurably degrades
   retrieval (the PTO-vs-sick-leave confusion at chunk_size=100, and the
   intro-paragraph false positive at chunk_size=250). The risk this
   exercise asks you to check directly: does a weaker retrieval result
   produce a visibly weaker-SOUNDING answer, or does the model's fluent
   phrasing paper over the gap regardless? Generating fluent text is
   what models are good at even when given mediocre source material --
   which is exactly why checking citations against actual chunk text,
   rather than judging an answer by how confident it sounds, is the
   real safeguard here.
"""


if __name__ == "__main__":
    offline_test()
    print("\n" + "=" * 70)
    print("Now attempting the full pipeline (requires ANTHROPIC_API_KEY)...")
    print("=" * 70)
    run_full_pipeline()
    print(PRO_PATH_NOTES)
