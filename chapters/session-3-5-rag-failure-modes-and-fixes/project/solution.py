"""
Session 3.5 Project: The Surface-Word Overlap Investigation -- Solution
See README.md in this folder for the full brief. Try the exercise
yourself before reading this -- the value is in the investigation, not
the answer.

Case 2's exact question and configuration, reproduced on purpose (not
modified): "Can I telecommute instead of going to the office?" against
chunk_size=100, overlap=20.
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Unmodified building blocks from Sessions 3.3-3.5 (provided)
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


QUESTION = "Can I telecommute instead of going to the office?"
CORRECT_CHUNK_KEYWORD = "remote work policy"


def shared_words(query: str, chunk: str) -> list:
    query_words = set(tokenize(query))
    chunk_words = set(tokenize(chunk))
    return sorted(query_words & chunk_words)


def find_chunk_by_keyword(full_ranking: list, keyword: str):
    keyword = keyword.lower()
    for rank, (chunk, score) in enumerate(full_ranking, start=1):
        if keyword in chunk.lower():
            return (rank, chunk, score)
    return None


# ---------------------------------------------------------------------------
# Findings, from actually running this against sample_handbook.pdf
# ---------------------------------------------------------------------------

ANALYSIS = {
    "coincidental_shared_word": (
        "'instead'. The #3-ranked chunk (sim=0.384) is about parental "
        "leave -- entirely unrelated to remote work -- but it contains "
        "the sentence 'Employees with less than 12 months of tenure ... "
        "are eligible for 6 weeks of paid parental leave instead of the "
        "full 16 weeks.' The word 'instead' is rare across the handbook, "
        "so under raw word-count cosine similarity, one coincidental "
        "match on a low-frequency word contributes disproportionately to "
        "the score -- enough, combined with the generic stopword overlap "
        "every chunk gets ('of', 'the'), to push an off-topic chunk above "
        "the chunk that actually answers the question."
    ),
    "would_a_bigger_k_reliably_fix_this": (
        "Not reliably. The correct chunk does rank #5 of 11 here (sim="
        "0.315), only two spots below the k=3 cutoff, so k=5 happens to "
        "work for THIS exact phrasing. But that's a coincidence of this "
        "one query, not a fix for the underlying cause: the correct "
        "chunk's score is low because 'telecommute' shares zero "
        "vocabulary with 'remote'/'remotely'/'hybrid', not because it's "
        "a narrowly-missed near-match. A slightly different phrasing "
        "(more synonyms, fewer coincidental stopword/rare-word overlaps "
        "with an off-topic chunk) could easily push the correct chunk to "
        "rank #8 or #15 instead of #5, at which point no reasonable k "
        "would recover it. Trusting 'just raise k' here means trusting a "
        "coincidence, not fixing the mismatch that caused it."
    ),
    "proposed_fix": (
        "The durable fix is the same one the exercises' solution "
        "reaches: a real trained embedding model, which would place "
        "'telecommute' close to 'remote work' in vector space regardless "
        "of shared letters, rather than a raw word-count model that can "
        "only match on literal shared vocabulary (including, as seen "
        "here, coincidentally shared stopwords and rare words that have "
        "nothing to do with the query's actual intent). Short of that, "
        "a re-ranking step over a wider candidate pool -- one that scores "
        "semantic relevance directly rather than re-sorting by the same "
        "word-overlap signal -- would also recognize that the parental-"
        "leave chunk's 'instead' match is not meaningful, while the "
        "remote-work chunk genuinely answers the question."
    ),
}


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
    print("Analysis:")
    for key, value in ANALYSIS.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    investigate()
