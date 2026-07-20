"""
Session 3.3 Project: The Chunk-Size Showdown
See README.md in this folder for the full brief.

The exercise's Pro path had you run the sick-leave question yourself at
different chunk sizes and eyeball the difference. This project packages
that same trade-off as a single, direct side-by-side comparison: build two
vector stores over the same handbook PDF at two different chunk sizes, run
the exact same question against both, and print the actual retrieved
chunks next to each other so the difference is impossible to miss.

Question under test: "How many sick days do employees get and do they
roll over?" -- PTO and sick leave share a lot of surface vocabulary
("days", "employees", "roll over"/"carry over"), which makes this a
genuinely hard, realistic retrieval case, not a rigged one.

The chunking/embedding/retrieval pipeline below is the same word-count
approach from Session 3.2 and the Session 3.3 exercise (build_vector_store)
-- it's provided complete here since you already built it in the exercise.
Your job in this project is the ANALYSIS at the bottom: read the two
side-by-side result sets that get printed and fill in what you actually
observe.

No API key and no internet access needed -- this is fully offline, using
pdfplumber to read the PDF and numpy for the vector math.

Run it: python3 starter.py
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# The pipeline (same approach as the Session 3.3 exercise's build_vector_store)
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF, concatenated across pages."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)


def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list:
    """Split text into overlapping word-count chunks, skipping tiny trailing
    fragments under 15 words."""
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
    """Word-count vector for each chunk against the shared vocabulary."""
    word_to_idx = {word: i for i, word in enumerate(vocab)}
    vectors = np.zeros((len(chunks), len(vocab)))
    for row, chunk in enumerate(chunks):
        for word in tokenize(chunk):
            if word in word_to_idx:
                vectors[row, word_to_idx[word]] += 1
    return vectors


def embed_query(query: str, vocab: list) -> np.ndarray:
    """Embed a single query string using the same vocabulary as the chunks."""
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
    """A minimal brute-force local vector store: holds chunk texts and their
    embedding vectors, and supports top-k similarity search."""

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
    """Build a chunked, embedded vector store and return it with its vocab
    and chunk count."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)

    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)

    return store, vocab, len(chunks)


# ---------------------------------------------------------------------------
# The showdown: one question, two chunk sizes, side by side
# ---------------------------------------------------------------------------

SICK_LEAVE_QUESTION = "How many sick days do employees get and do they roll over?"

# Two settings to compare directly. chunk_size=100 is the exercise's default;
# chunk_size=30 is the "go smaller" setting from the exercise's debug task.
CHUNK_SETTINGS = [
    {"label": "Larger chunks", "chunk_size": 100, "overlap": 20},
    {"label": "Smaller chunks", "chunk_size": 30, "overlap": 5},
]


def run_showdown(pdf_path: str, k: int = 3):
    """Build a vector store at each setting in CHUNK_SETTINGS, run
    SICK_LEAVE_QUESTION against each, and print the top-k results for both
    settings side by side (one after another, same question, easy to
    compare by eye)."""
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
# Your analysis: fill this in after reading the printed results above
# ---------------------------------------------------------------------------

# TODO: run this file, read the two result sets printed above, and fill in
# the four fields below based on what you actually see -- not what you'd
# expect in theory. There's no single "correct" wording; what matters is
# that your answers describe the real output.
ANALYSIS = {
    # At chunk_size=100 (the larger setting), does the TOP-ranked ([1])
    # result actually contain the sick-leave answer, or is it a different
    # policy (e.g. PTO) that just shares vocabulary with the question?
    "larger_chunks_top_result_is_correct": None,  # TODO: True or False

    # At chunk_size=30 (the smaller setting), does the correct sick-leave
    # chunk ("Sick days do not carry over...") appear anywhere in the top-k
    # results printed above? What rank is it at?
    "smaller_chunks_correct_chunk_rank": None,  # TODO: an int (1, 2, 3...) or None if absent

    # One to two sentences: why does reducing chunk_size change which chunk
    # wins here, given that PTO and sick leave share so much vocabulary?
    "why_chunk_size_changes_the_winner": None,  # TODO: str

    # One to two sentences: if this retrieval step fed a real RAG system,
    # what would go wrong downstream if the wrong chunk were retrieved and
    # handed to a model as its only context for this question?
    "downstream_risk_of_the_wrong_chunk": None,  # TODO: str
}


def print_analysis():
    missing = [k for k, v in ANALYSIS.items() if v is None]
    if missing:
        print(f"\n{len(missing)} of {len(ANALYSIS)} ANALYSIS field(s) not yet filled in.")
        return

    print("\n=== Your analysis ===")
    print(f"Larger chunks (size=100) got the top result right: {ANALYSIS['larger_chunks_top_result_is_correct']}")
    print(f"Smaller chunks (size=30) rank of the correct chunk: {ANALYSIS['smaller_chunks_correct_chunk_rank']}")
    print(f"Why chunk size changes the winner: {ANALYSIS['why_chunk_size_changes_the_winner']}")
    print(f"Downstream risk of the wrong chunk: {ANALYSIS['downstream_risk_of_the_wrong_chunk']}")


if __name__ == "__main__":
    run_showdown("sample_handbook.pdf", k=3)
    print_analysis()
