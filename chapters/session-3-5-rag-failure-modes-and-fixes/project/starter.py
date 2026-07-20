"""
Session 3.5 Project: The Surface-Word Overlap Investigation
See README.md in this folder for the full brief.

This is the Pro path build for Session 3.5, extending Case 2 of the
exercises' broken pipeline (../exercises/broken_pipeline.py): a retrieval
miss where the query "Can I telecommute instead of going to the office?"
fails to surface the handbook's actual Remote Work Policy section in its
top-3 results.

The exercises worksheet asks you to confirm the correct chunk is ABSENT
from the top-3. This project asks the sharper question the lesson's Pro
path text poses: don't just confirm the absence -- look at what DID get
retrieved instead, and find the specific surface-level word overlap that
let each wrong chunk outrank the chunk that actually answers the question.

No API key and no internet access needed -- this reuses the exact same
offline chunking/embedding/retrieval code as the exercises, run against
the same sample_handbook.pdf, with chunk_size=100 and overlap=20 (Case
2's exact configuration -- reproduced here on purpose, not modified).
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Unmodified building blocks from Sessions 3.3-3.5 (provided, same as
# exercises/broken_pipeline.py)
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


def build_store(pdf_path: str, chunk_size: int, overlap: int):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)
    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)
    return store, vocab, len(chunks)


# ---------------------------------------------------------------------------
# Case 2's exact question and configuration, reproduced on purpose
# ---------------------------------------------------------------------------

QUESTION = "Can I telecommute instead of going to the office?"

# The one phrase that appears in the chunk that actually answers this
# question (the handbook's numbered "3. Remote Work Policy" section) --
# used below to locate it in the FULL ranking, not just the top-3.
CORRECT_CHUNK_KEYWORD = "remote work policy"


# ---------------------------------------------------------------------------
# TODO 1: which words does a wrongly-retrieved chunk actually share with
# the query?
# ---------------------------------------------------------------------------

def shared_words(query: str, chunk: str) -> list:
    """
    TODO: Return a sorted list of the words that appear in BOTH the query
    and the chunk. Use tokenize() (provided above) on each string, turn
    the results into sets, and return the sorted intersection.

    This is the concrete, checkable version of "surface-level word
    overlap" -- rather than just asserting a chunk "seems unrelated,"
    this shows exactly which words the word-count embedding actually
    matched on.
    """
    raise NotImplementedError("Fill in shared_words()")


# ---------------------------------------------------------------------------
# TODO 2: where does the correct chunk actually rank, across ALL chunks --
# not just the top-3 the broken pipeline handed to the model?
# ---------------------------------------------------------------------------

def find_chunk_by_keyword(full_ranking: list, keyword: str):
    """
    TODO: `full_ranking` is a list of (chunk_text, score) tuples, already
    sorted best-to-worst, covering EVERY chunk in the store (not just a
    top-k slice). Find and return a tuple (rank, chunk_text, score) for
    the first chunk (1-indexed rank) whose text contains `keyword`,
    case-insensitively. Return None if no chunk contains it.

    Hint: enumerate(full_ranking, start=1) gives you the 1-indexed rank
    directly.
    """
    raise NotImplementedError("Fill in find_chunk_by_keyword()")


# ---------------------------------------------------------------------------
# TODO 3: after running the investigation below, fill in your findings.
# ---------------------------------------------------------------------------

ANALYSIS = {
    # Of the top-3 wrongly-retrieved chunks, one shares a single specific
    # CONTENT word with the query that the other two don't (not one of the
    # generic "the" / "of" / "to" words nearly every chunk shares). Which
    # word is it, and which chunk (by topic) does it come from?
    "coincidental_shared_word": None,   # TODO
    # The correct chunk's true rank (from find_chunk_by_keyword) is close
    # to, but just outside, the k=3 cutoff. Does that mean a slightly
    # larger k (e.g. k=5) would reliably fix THIS question? What would you
    # need to check before trusting that as a general fix, rather than a
    # coincidence of this one specific phrasing?
    "would_a_bigger_k_reliably_fix_this": None,   # TODO
    "proposed_fix": None,   # TODO
}


# ---------------------------------------------------------------------------
# Run the investigation
# ---------------------------------------------------------------------------

def investigate():
    store, vocab, n_chunks = build_store("sample_handbook.pdf", chunk_size=100, overlap=20)
    query_vector = embed_query(QUESTION, vocab)

    print(f"{'=' * 70}")
    print(f"Question: {QUESTION}")
    print(f"Pipeline config: chunk_size=100, overlap=20  ({n_chunks} chunks total)")

    top_3 = store.search(query_vector, k=3)
    print(f"\n--- Top-3 retrieved (what the broken pipeline actually hands the model) ---")
    for rank, (chunk, score) in enumerate(top_3, start=1):
        overlap_words = shared_words(QUESTION, chunk)
        print(f"\n[{rank}] sim={score:.3f}")
        print(f"    shared words with query: {overlap_words}")
        print(f"    chunk: {chunk[:160]}...")

    full_ranking = store.search(query_vector, k=n_chunks)
    found = find_chunk_by_keyword(full_ranking, CORRECT_CHUNK_KEYWORD)

    print(f"\n--- Where the chunk that actually answers the question really ranks ---")
    if found is None:
        print(f"No chunk containing {CORRECT_CHUNK_KEYWORD!r} was found at all.")
    else:
        rank, chunk, score = found
        print(f"Rank #{rank} of {n_chunks}, sim={score:.3f}")
        print(f"chunk: {chunk[:200]}...")

    print(f"\n{'=' * 70}")
    print("Your analysis:")
    for key, value in ANALYSIS.items():
        status = value if value is not None else "[NOT FILLED IN YET]"
        print(f"  {key}: {status}")


if __name__ == "__main__":
    investigate()
