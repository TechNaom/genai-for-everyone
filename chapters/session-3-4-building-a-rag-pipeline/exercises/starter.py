"""
Session 3.4 Exercise — Building a RAG Pipeline (Retrieve -> Augment -> Generate)
===========================================================================

Goal: take the working vector store from Session 3.3 and complete the
pipeline -- augment a prompt with retrieved chunks, generate a grounded
answer with citations, and return both the answer and a way to verify
which chunks actually supported it.

This builds directly on Session 3.3's chunking, embedding, and
VectorStore code (reproduced below so this file is self-contained).

WHAT YOU NEED TO BUILD
-----------------------
1. format_context()     -- TODO: turn retrieval results into numbered,
                            citeable context (the "augment" step)
2. build_rag_prompt()    -- TODO: assemble the full grounded prompt
3. call_llm()            -- provided: a real call to the Anthropic API
                            (requires YOUR OWN API key -- see below)
4. extract_citations()   -- TODO: pull out which chunk numbers the
                            model's answer actually cited
5. answer_question()     -- TODO: tie it all together: retrieve -> format
                            -> prompt -> generate -> return answer + cited
                            chunks

REQUIRES AN API KEY TO RUN END TO END
---------------------------------------
Unlike Sessions 3.1-3.3, this exercise needs a real LLM call for the
generation step -- there's no meaningful toy substitute for "generate a
grounded answer," the way there was for embeddings. To run this fully:

    export ANTHROPIC_API_KEY=your-key-here
    pip install anthropic --break-system-packages
    python3 build_rag_pipeline.py

If you don't have a key, you can still complete and test steps 1, 2, and
4 entirely offline -- the bottom of this file includes an offline test
for format_context() and extract_citations() that doesn't require any
API access. Get those right first; they're most of the actual logic.
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Reproduced from Session 3.3 (same code, so this file is self-contained)
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
# NEW for Session 3.4
# ---------------------------------------------------------------------------

def format_context(search_results: list) -> str:
    """
    TODO: Turn a list of (chunk_text, similarity_score) tuples -- the
    output of VectorStore.search() -- into a single numbered context
    string ready to insert into a prompt. This is the "augment" step.

    Important: the similarity scores should NOT appear in the output --
    they were useful internally for retrieval, but the model doesn't
    need them and they don't belong in the final prompt (see the
    session's discussion of this exact translation step).

    Expected format (chunk numbers start at 1):

        [1] {first chunk's text}

        [2] {second chunk's text}

        [3] {third chunk's text}

    Returns a single string with all numbered chunks separated by blank
    lines.
    """
    raise NotImplementedError("Fill in format_context()")


RAG_PROMPT_TEMPLATE = """You are answering a question using ONLY the information in the provided context below. If the context does not contain enough information to answer the question, say so explicitly rather than guessing or using outside knowledge.

CONTEXT:
{context}

QUESTION: {question}

Answer the question, and cite which numbered context chunk(s) support each part of your answer using the format [1], [2], etc.
"""


def build_rag_prompt(question: str, context: str) -> str:
    """
    TODO: Fill in RAG_PROMPT_TEMPLATE's two variables (context and
    question) and return the complete prompt string, ready to send to
    the model.
    """
    raise NotImplementedError("Fill in build_rag_prompt()")


def call_llm(prompt: str) -> str:
    """
    Calls the Anthropic API and returns the model's raw text response.
    Requires ANTHROPIC_API_KEY to be set in your environment.
    """
    import anthropic

    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def extract_citations(answer_text: str) -> list:
    """
    TODO: Find every citation marker like [1], [2], [3] in the model's
    answer text, and return a sorted list of the unique chunk numbers
    cited (as integers), e.g. [1, 3] if the answer cited chunks 1 and 3
    (in any order, possibly more than once each).

    Hint: re.findall(r"\\[(\\d+)\\]", answer_text) finds all the bracketed
    numbers as strings -- convert them to int, deduplicate, and sort.
    """
    raise NotImplementedError("Fill in extract_citations()")


def answer_question(store: "VectorStore", vocab: list, question: str, k: int = 3) -> dict:
    """
    TODO: Tie the full pipeline together:
      1. Embed the question using embed_query().
      2. Retrieve the top-k chunks using store.search().
      3. Format those results into numbered context with format_context().
      4. Build the full prompt with build_rag_prompt().
      5. Call the model with call_llm().
      6. Extract which chunks were actually cited with extract_citations().

    Return a dict with keys:
      "answer": the model's raw text response
      "cited_chunk_numbers": the list from extract_citations()
      "retrieved_chunks": the list of (chunk_text, score) tuples from
                          step 2, so you can manually verify citations
                          against the real chunk text if you want to.
    """
    raise NotImplementedError("Fill in answer_question()")


# ---------------------------------------------------------------------------
# Offline test (no API key required) -- get this working first
# ---------------------------------------------------------------------------

def offline_test():
    """
    Tests format_context() and extract_citations() without needing any
    API access. Run this first to validate your logic before spending
    API calls on the full pipeline.
    """
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

    print("--- Testing extract_citations() ---")
    fake_answer = "Employees get 18 days of PTO [1]. Sick days do not roll over [2][2]."
    citations = extract_citations(fake_answer)
    print(f"Extracted citations: {citations}")
    assert citations == [1, 2], f"Expected [1, 2], got {citations}"
    print("extract_citations() looks correct.\n")

    print("All offline tests passed.")


# ---------------------------------------------------------------------------
# Full pipeline test (requires ANTHROPIC_API_KEY)
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


if __name__ == "__main__":
    offline_test()
    print("\n" + "=" * 70)
    print("Now attempting the full pipeline (requires ANTHROPIC_API_KEY)...")
    print("=" * 70)
    run_full_pipeline()
