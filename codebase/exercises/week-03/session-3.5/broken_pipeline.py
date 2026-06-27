"""
Session 3.5 Exercise — Debug a Broken RAG Pipeline (GIVEN)
===========================================================================

DO NOT FIX THE BUGS IN THIS FILE. This file is deliberately broken in
three places, each one a real-world instance of a failure mode from
today's session: a chunking error, a retrieval miss, and context
stuffing. Your job is diagnostic, not corrective -- run this file,
look at the actual output for each of the three test cases below, and
fill in your diagnosis in `diagnosis_worksheet.py` (a separate file).

This pipeline reuses the same chunking/embedding/retrieval code from
Sessions 3.3-3.4 -- if it looks familiar, that's intentional. The bugs
are all in HOW these working pieces are configured and used, not in the
underlying functions themselves.

Run this file directly: python3 broken_pipeline.py
Then open diagnosis_worksheet.py and do the actual diagnostic work.
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Unmodified building blocks from Sessions 3.3-3.4
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


# ---------------------------------------------------------------------------
# THREE BROKEN PIPELINE CONFIGURATIONS -- each one has exactly one bug.
# Do not fix these. Run them, observe the output, and diagnose.
# ---------------------------------------------------------------------------

def build_store(pdf_path: str, chunk_size: int, overlap: int):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vocab = build_vocabulary(chunks)
    chunk_vectors = embed_chunks(chunks, vocab)
    store = VectorStore()
    for chunk, vector in zip(chunks, chunk_vectors):
        store.add(chunk, vector)
    return store, vocab, len(chunks)


def case_1_broken():
    """
    Case 1: a coworker configured this pipeline to use very small chunks
    for "more precise" retrieval, and turned off overlap entirely to
    "save space." Test question: a fact that requires reading across a
    sentence boundary to get the complete picture.
    """
    store, vocab, n_chunks = build_store("sample_handbook.pdf", chunk_size=15, overlap=0)
    question = "How many sick days do employees get and do they roll over?"
    qv = embed_query(question, vocab)
    results = store.search(qv, k=3)

    print(f"\n{'=' * 70}")
    print("CASE 1")
    print(f"Pipeline config: chunk_size=15, overlap=0  ({n_chunks} chunks total)")
    print(f"Question: {question}")
    print("\nTop-3 retrieved chunks:")
    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"  [{rank}] sim={score:.3f}  {chunk}")


def case_2_broken():
    """
    Case 2: a real user asked this question using natural, everyday
    phrasing -- not the exact words used in the handbook.
    """
    store, vocab, n_chunks = build_store("sample_handbook.pdf", chunk_size=100, overlap=20)
    question = "Can I telecommute instead of going to the office?"
    qv = embed_query(question, vocab)
    results = store.search(qv, k=3)

    print(f"\n{'=' * 70}")
    print("CASE 2")
    print(f"Pipeline config: chunk_size=100, overlap=20  ({n_chunks} chunks total)")
    print(f"Question: {question}")
    print("\nTop-3 retrieved chunks:")
    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"  [{rank}] sim={score:.3f}  {chunk[:100]}...")


def case_3_broken():
    """
    Case 3: a coworker set k=10 because "retrieval seemed unreliable, so
    let's just grab more chunks to be safe." The handbook only has 11
    chunks total at this configuration.
    """
    store, vocab, n_chunks = build_store("sample_handbook.pdf", chunk_size=100, overlap=20)
    question = "How many PTO days do employees get per year?"
    qv = embed_query(question, vocab)
    results = store.search(qv, k=10)

    print(f"\n{'=' * 70}")
    print("CASE 3")
    print(f"Pipeline config: chunk_size=100, overlap=20, k=10  ({n_chunks} chunks total)")
    print(f"Question: {question}")
    print(f"\nTop-{len(results)} retrieved chunks (all {len(results)} would be sent to the model):")
    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"  [{rank}] sim={score:.3f}  {chunk[:80]}...")


if __name__ == "__main__":
    case_1_broken()
    case_2_broken()
    case_3_broken()

    print(f"\n{'=' * 70}")
    print("Now open diagnosis_worksheet.py and diagnose each case.")
