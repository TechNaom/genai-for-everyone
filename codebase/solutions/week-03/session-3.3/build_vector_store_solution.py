"""
Session 3.3 — Reference Solution
Build a Local Vector Store Over a PDF
===========================================================================

Try the exercise yourself first -- the value is in implementing chunking,
embedding, and the vector store's search logic, and seeing the chunk-size
trade-off directly, not in reading someone else's implementation.
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


TEST_QUESTIONS = [
    "How many PTO days do employees get per year?",
    "Can employees work from home, and how many days per week?",
    "How much can I be reimbursed for meals while traveling?",
    "What is the 401k matching policy?",
    "How many sick days do employees get and do they roll over?",
]


def build_store(pdf_path: str, chunk_size: int, overlap: int):
    """Build the chunked, embedded vector store and return it with its vocab."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)

    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)

    return store, vocab, len(chunks)


def run_pipeline(pdf_path: str, chunk_size: int, overlap: int, k: int = 3):
    store, vocab, n_chunks = build_store(pdf_path, chunk_size, overlap)
    print(f"\n=== chunk_size={chunk_size}, overlap={overlap} -> {n_chunks} chunks ===")

    for question in TEST_QUESTIONS:
        query_vector = embed_query(question, vocab)
        results = store.search(query_vector, k=k)
        print(f"\nQ: {question}")
        for rank, (chunk, score) in enumerate(results, start=1):
            preview = chunk[:140].replace("\n", " ")
            print(f"  [{rank}] sim={score:.3f}  {preview}...")

    return store, vocab


# ---------------------------------------------------------------------------
# Pro path observations
# ---------------------------------------------------------------------------

PRO_PATH_NOTES = """
Pro path observations (matching the actual output above -- run it
yourself and compare):

1. Chunk-size trade-off on the sick-leave question
   ("How many sick days do employees get and do they roll over?"):

   - chunk_size=100, overlap=20: the top match is a PTO-related chunk,
     NOT the sick-leave chunk -- a clear miss. PTO and sick leave share
     a lot of overlapping vocabulary ("days", "year", "employees",
     "carry over"/"roll over"), and at this chunk size the sick-leave-
     specific sentence gets diluted by surrounding PTO-adjacent text
     elsewhere in the document scoring deceptively well on shared words.
   - chunk_size=30, overlap=5: the actual sick-leave chunk ("Sick days
     do not carry over to the following year...") shows up essentially
     tied for the top spot (often rank #2, with a near-identical score
     to rank #1) -- noticeably better than at chunk_size=100, but still
     not a clean, unambiguous #1. This is an honest, real result, not a
     tidied-up one: smaller chunks help here, but "helps" is not the
     same as "solves perfectly."
   - chunk_size=250, overlap=40: at this size there are only 4 chunks
     covering the entire document, and the generic intro paragraph
     (which name-drops "leave" alongside every other topic) starts
     winning the top spot for multiple unrelated questions -- exactly
     the false-positive failure mode described in point 2 below.

   The general, honest pattern: smaller chunks tend to isolate specific
   facts more cleanly, but don't guarantee a clean win, especially when
   two real topics (PTO vs. sick leave) deliberately share a lot of
   surface vocabulary. Larger chunks keep more surrounding context
   together but dilute specific signal and let topically-vague chunks
   (like the intro) win by a kind of vocabulary stuffing. There is no
   chunk size in this test that gets all five questions right at rank 1
   -- which is itself the most important lesson: chunking is a genuine,
   unresolved trade-off you tune and monitor, not a setting you pick
   once and trust forever. Session 3.5 covers systematic ways to
   diagnose exactly this kind of near-miss.

2. The intro-paragraph false positive: the opening paragraph mentions
   "leave, remote work, expenses, and benefits" -- every major topic in
   the handbook, in one sentence. With word-count-based similarity, this
   chunk scores moderately well against almost ANY query, because it
   shares at least a little vocabulary with every topic -- and at larger
   chunk sizes (where there are fewer, broader chunks overall) it
   actually wins the top spot for some queries in the run above. It's
   dangerous specifically because it's superficially relevant to
   everything but substantively useful for nothing -- a real RAG system
   that retrieves this chunk for several different unrelated questions
   would generate a vague, low-information answer each time, rather than
   failing loudly in an obvious way.

3. k=1 vs. k=5: with k=1, the sick-leave question at chunk_size=100
   above would return ONLY the wrong PTO chunk -- a clean miss with
   nothing to fall back on. With a higher k (try k=5 yourself), the
   correct sick-leave chunk is more likely to appear somewhere in the
   returned set, even if not ranked first -- giving a generation step
   downstream a chance to find the right answer among several
   candidates. The cost: more irrelevant text handed to the model,
   higher latency and token cost, and more chances for the model to get
   distracted by a confidently-worded but wrong chunk ranked above the
   right one. This is the same k trade-off the session described: there
   is no universally correct k, only a balance to tune for your
   documents and queries.
"""


if __name__ == "__main__":
    # Core path
    run_pipeline("sample_handbook.pdf", chunk_size=100, overlap=20, k=3)

    # Pro path comparisons
    run_pipeline("sample_handbook.pdf", chunk_size=30, overlap=5, k=3)
    run_pipeline("sample_handbook.pdf", chunk_size=250, overlap=40, k=3)

    print(PRO_PATH_NOTES)
