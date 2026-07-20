"""
Session 3.3 Project: The Chunk-Size Showdown -- reference solution.

Note: the exact wording in ANALYSIS below isn't the point -- what matters
is that it accurately describes the real output printed by run_showdown().
Run this file yourself first and compare your own printed results against
these numbers; the pipeline is deterministic, so you should see the same
ranks and scores.

Run it: python3 solution.py
"""

import re

import numpy as np
import pdfplumber


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
        similarities = [
            cosine_similarity(query_vector, v) for v in self.vectors
        ]
        top_k_idx = np.argsort(similarities)[::-1][:k]
        return [(self.chunks[i], similarities[i]) for i in top_k_idx]


def build_store(pdf_path: str, chunk_size: int, overlap: int):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)

    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)

    return store, vocab, len(chunks)


SICK_LEAVE_QUESTION = "How many sick days do employees get and do they roll over?"

CHUNK_SETTINGS = [
    {"label": "Larger chunks", "chunk_size": 100, "overlap": 20},
    {"label": "Smaller chunks", "chunk_size": 30, "overlap": 5},
]


def run_showdown(pdf_path: str, k: int = 3):
    print(f'Q: "{SICK_LEAVE_QUESTION}"')

    results_by_setting = []
    for setting in CHUNK_SETTINGS:
        store, vocab, n_chunks = build_store(
            pdf_path, setting["chunk_size"], setting["overlap"]
        )
        query_vector = embed_query(SICK_LEAVE_QUESTION, vocab)
        results = store.search(query_vector, k=k)
        results_by_setting.append(results)

        print(
            f"\n--- {setting['label']} (chunk_size={setting['chunk_size']}, "
            f"overlap={setting['overlap']} -> {n_chunks} chunks) ---"
        )
        for rank, (chunk, score) in enumerate(results, start=1):
            preview = chunk[:150].replace("\n", " ")
            print(f"  [{rank}] sim={score:.3f}  {preview}...")

    return results_by_setting


# ---------------------------------------------------------------------------
# Analysis (based on the actual output above -- run it yourself to confirm)
# ---------------------------------------------------------------------------

ANALYSIS = {
    "larger_chunks_top_result_is_correct": False,
    # At chunk_size=100, rank [1] (sim=0.287) is a PTO-accrual chunk
    # ("20 hours per week accrue PTO on a pro-rated basis...") -- not the
    # sick-leave answer. The actual sick-leave sentence doesn't appear in
    # the top 3 at all at this chunk size.
    "smaller_chunks_correct_chunk_rank": 2,
    # At chunk_size=30, rank [2] (sim=0.310, tied with rank [1] to three
    # decimal places) is the genuinely correct chunk: "Sick days do not
    # carry over to the following year and are not paid out...". Rank [1]
    # is actually a different, unrelated chunk about a remote-work stipend
    # that happens to also say "does not roll over" -- so even the
    # improved setting doesn't produce a clean, unambiguous win.
    "why_chunk_size_changes_the_winner": (
        "At chunk_size=100 the sick-leave sentence sits inside a long "
        "chunk surrounded by other PTO-adjacent text, so its specific "
        "signal gets diluted into a bigger word-count vector that scores "
        "worse than a dedicated PTO chunk sharing 'days'/'employees' with "
        "the question. At chunk_size=30, the sick-leave sentence gets its "
        "own short, tightly-focused chunk, so its word-count vector is "
        "dominated by sick-leave-specific words instead of being diluted "
        "by surrounding unrelated text -- which is enough to pull it up "
        "into a near-tie for first, even though a different chunk still "
        "edges it out by sharing the exact phrase 'does not roll over'."
    ),
    "downstream_risk_of_the_wrong_chunk": (
        "If a RAG system fed only the top-1 PTO chunk from the larger "
        "setting to a model, the generated answer would confidently state "
        "the PTO rollover cap as if it were the sick-leave policy -- a "
        "wrong answer delivered with the same confident tone as a correct "
        "one, which is far more dangerous for an HR-facing tool than the "
        "system saying nothing at all."
    ),
}


def print_analysis():
    print("\n=== Analysis ===")
    print(f"Larger chunks (size=100) got the top result right: {ANALYSIS['larger_chunks_top_result_is_correct']}")
    print(f"Smaller chunks (size=30) rank of the correct chunk: {ANALYSIS['smaller_chunks_correct_chunk_rank']}")
    print(f"Why chunk size changes the winner: {ANALYSIS['why_chunk_size_changes_the_winner']}")
    print(f"Downstream risk of the wrong chunk: {ANALYSIS['downstream_risk_of_the_wrong_chunk']}")


if __name__ == "__main__":
    run_showdown("sample_handbook.pdf", k=3)
    print_analysis()
