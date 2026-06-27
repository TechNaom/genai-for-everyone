"""
Session 3.3 Exercise — Build a Local Vector Store Over a PDF
===========================================================================

Goal: take a real PDF (a sample company handbook), chunk it, embed each
chunk, store the vectors, and retrieve the top-k most relevant chunks for
real test questions -- the full pipeline from today's session, minus the
final "generate an answer" step (that's Session 3.4).

This uses the same kind of word-count embedding approach from Session 3.2
-- no internet access or API key required. Unlike 3.2's short sentences,
today's chunks are full paragraphs of real text, which is enough for
plain word-count vectors to produce genuinely useful retrieval (you'll
verify this yourself with the sanity checks below). If you have an
OpenAI or Anthropic API key, see real_embeddings_optional() at the bottom
for how you'd swap in real embeddings instead.

WHAT YOU NEED TO BUILD
-----------------------
1. extract_text_from_pdf()  -- provided (uses pdfplumber)
2. chunk_text()             -- TODO: split text into overlapping chunks
3. build_vocabulary()       -- provided
4. embed_chunks()           -- TODO: build word-count vectors for chunks
5. cosine_similarity()      -- TODO: same formula from 3.2
6. VectorStore class        -- TODO: complete add() and search()
7. Try it on real questions -- provided, but you should also test your own

Run this file directly: python3 build_vector_store.py
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Step 1: Extract text from the PDF (provided)
# ---------------------------------------------------------------------------

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF, concatenated across pages."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages)


# ---------------------------------------------------------------------------
# Step 2 (TODO): Chunk the text
# ---------------------------------------------------------------------------

def chunk_text(text: str, chunk_size: int = 100, overlap: int = 20) -> list:
    """
    TODO: Split `text` into overlapping chunks of approximately
    `chunk_size` words each, with `overlap` words shared between
    consecutive chunks.

    Approach:
      1. Split `text` into a list of words (text.split() is fine here).
      2. Walk through the word list in steps of (chunk_size - overlap),
         taking chunk_size words at a time, and join each slice back into
         a string with " ".join(...).
      3. Stop once you've reached the end of the word list -- don't
         produce empty or tiny trailing chunks (skip any chunk with fewer
         than 15 words, since these are usually leftover fragments at
         the very end of the document).

    Returns a list of chunk strings.

    Example: with chunk_size=100 and overlap=20, consecutive chunks share
    their last/first 20 words -- so an idea split across the boundary in
    one chunk's ending is still fully present in the next chunk's
    beginning.
    """
    raise NotImplementedError("Fill in chunk_text()")


# ---------------------------------------------------------------------------
# Step 3: Build a shared vocabulary across all chunks (provided)
# ---------------------------------------------------------------------------

def tokenize(s: str) -> list:
    return re.findall(r"[a-z']+", s.lower())


def build_vocabulary(chunks: list) -> list:
    vocab = set()
    for chunk in chunks:
        vocab.update(tokenize(chunk))
    return sorted(vocab)


# ---------------------------------------------------------------------------
# Step 4 (TODO): Embed each chunk
# ---------------------------------------------------------------------------

def embed_chunks(chunks: list, vocab: list) -> np.ndarray:
    """
    TODO: Build a word-count vector for each chunk, exactly like the
    word-count component from Session 3.2 -- for each chunk, create a
    vector of length len(vocab) where position i counts how many times
    vocab[i] appears in that chunk.

    Returns a numpy array of shape (len(chunks), len(vocab)).

    Note: unlike Session 3.2's short sentences, these chunks are full
    paragraphs of real text -- plain word-count vectors work noticeably
    better here, because there's simply more text (and more genuine word
    overlap with related content) per chunk. No hand-seeded "concept
    anchors" needed this time -- verify that for yourself with the
    sanity checks at the bottom of this file.
    """
    raise NotImplementedError("Fill in embed_chunks()")


def embed_query(query: str, vocab: list) -> np.ndarray:
    """Embed a single query string using the same vocabulary as the chunks."""
    word_to_idx = {word: i for i, word in enumerate(vocab)}
    vec = np.zeros(len(vocab))
    for word in tokenize(query):
        if word in word_to_idx:
            vec[word_to_idx[word]] += 1
    return vec


# ---------------------------------------------------------------------------
# Step 5 (TODO): Cosine similarity
# ---------------------------------------------------------------------------

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    TODO: Implement cosine similarity, same formula as Session 3.2:
        cosine_similarity(A, B) = (A . B) / (|A| * |B|)
    Return 0.0 if either vector has zero length, to avoid dividing by zero.
    """
    raise NotImplementedError("Fill in cosine_similarity()")


# ---------------------------------------------------------------------------
# Step 6 (TODO): A minimal vector store
# ---------------------------------------------------------------------------

class VectorStore:
    """
    A minimal local vector store: holds chunk texts and their embedding
    vectors, and supports top-k similarity search.

    This is a brute-force (exhaustive) implementation -- it checks every
    stored vector on every search, exactly as described in the session.
    That's fine at the scale of one handbook; production vector stores
    use ANN indexing to avoid this at scale, but the search LOGIC -- find
    the k nearest vectors by cosine similarity -- is the same idea either
    way.
    """

    def __init__(self):
        self.chunks = []      # list of chunk text strings
        self.vectors = []     # list of corresponding embedding vectors

    def add(self, chunk_text: str, vector: np.ndarray):
        """
        TODO: Store the chunk text and its vector so they can be
        retrieved together later. Append to self.chunks and self.vectors.
        """
        raise NotImplementedError("Fill in VectorStore.add()")

    def search(self, query_vector: np.ndarray, k: int = 3) -> list:
        """
        TODO: Return the top-k most similar chunks to `query_vector`.

        Steps:
          1. Compute cosine_similarity(query_vector, v) for every stored
             vector v in self.vectors.
          2. Sort chunks by similarity score, descending.
          3. Return a list of (chunk_text, similarity_score) tuples for
             the top k results.

        Hint: np.argsort(similarities)[::-1][:k] gives you the indices of
        the top k scores in descending order.
        """
        raise NotImplementedError("Fill in VectorStore.search()")


# ---------------------------------------------------------------------------
# Run it: build the store and test real questions
# ---------------------------------------------------------------------------

TEST_QUESTIONS = [
    "How many PTO days do employees get per year?",
    "Can employees work from home, and how many days per week?",
    "How much can I be reimbursed for meals while traveling?",
    "What is the 401k matching policy?",
    "How many sick days do employees get and do they roll over?",
]


def run_pipeline(pdf_path: str, chunk_size: int, overlap: int, k: int = 3):
    """Build the full pipeline and print top-k results for each test question."""
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    print(f"\n=== chunk_size={chunk_size}, overlap={overlap} -> {len(chunks)} chunks ===")

    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)

    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)

    for question in TEST_QUESTIONS:
        query_vector = embed_query(question, vocab)
        results = store.search(query_vector, k=k)
        print(f"\nQ: {question}")
        for rank, (chunk, score) in enumerate(results, start=1):
            preview = chunk[:140].replace("\n", " ")
            print(f"  [{rank}] sim={score:.3f}  {preview}...")


# ---------------------------------------------------------------------------
# OPTIONAL PAID-API PATH (not required)
# ---------------------------------------------------------------------------

def real_embeddings_optional(chunks: list) -> np.ndarray:
    """
    OPTIONAL: if you have an OpenAI API key, use real embeddings instead
    of the word-count vectors above, for comparison.
    Requires: pip install openai --break-system-packages
    Requires: OPENAI_API_KEY environment variable set.
    """
    import os
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-small", input=chunks)
    return np.array([item.embedding for item in response.data])


if __name__ == "__main__":
    # Core path: a reasonable default chunk size and overlap.
    run_pipeline("sample_handbook.pdf", chunk_size=100, overlap=20, k=3)
