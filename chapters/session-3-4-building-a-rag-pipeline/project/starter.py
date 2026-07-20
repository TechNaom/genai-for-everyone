"""
Project (Pro path) — Session 3.4: Verifying an Honest "I Don't Know"
===========================================================================

Goal: take the completed RAG pipeline from the Session 3.4 exercises and
push it on the exact question the lesson's Pro path challenge asks about --
not "does retrieval find a weak match," but "when the fact is genuinely
absent from the entire document set, does the system say so honestly, or
does it produce a fluent, confident-sounding guess anyway?"

This file reproduces the completed pipeline from exercises/solution.py
(chunking, embedding, VectorStore, format_context, build_rag_prompt,
call_llm, extract_citations, answer_question) so it's self-contained --
that part is already-taught material, not new work. What's new here:

WHAT YOU NEED TO BUILD
-----------------------
1. is_grounded_refusal()      -- TODO: pure-logic check for whether an
                                  answer honestly says "not enough
                                  information," using no API call at all.
2. run_verification_challenge() -- TODO: run the unanswerable questions
                                  below through the full pipeline and
                                  check citations + is_grounded_refusal()
                                  agree that the system refused honestly.

REQUIRES AN API KEY FOR THE LIVE PART
---------------------------------------
Same situation as the Session 3.4 exercises: there's no meaningful toy
substitute for "generate a real answer and see whether it's honest." To
run the full challenge:

    export ANTHROPIC_API_KEY=your-key-here
    pip install anthropic pdfplumber numpy --break-system-packages
    python3 starter.py

If you don't have a key yet, is_grounded_refusal() is pure string logic
with no API dependency -- offline_test() below validates it against fake
answer text with no network access required. Get that right first; it's
the part of this project that's actually new.
"""

import re

import numpy as np
import pdfplumber


# ---------------------------------------------------------------------------
# Reproduced from the Session 3.4 exercises (already-completed pipeline)
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


def format_context(search_results: list) -> str:
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
# NEW for this project
# ---------------------------------------------------------------------------

# Questions that are genuinely unanswerable from sample_handbook.pdf -- not
# a weak retrieval match, but a fact that simply never appears anywhere in
# the source document. Verify this claim yourself: none of "tuition",
# "education", or "degree" appear anywhere in the handbook text, so there
# is no chunk retrieval could ever surface that actually supports an answer.
UNANSWERABLE_QUESTIONS = [
    "Does the company offer tuition reimbursement or a continuing "
    "education benefit for employees pursuing a degree?",
    "What is the company's policy on bereavement leave?",
]

# Phrases a model uses when it's honestly declining to answer beyond what
# the context supports. Not exhaustive -- good enough to catch the common
# ways Claude phrases "I don't have enough information."
REFUSAL_PHRASES = [
    "not enough information",
    "does not contain",
    "doesn't contain",
    "no information",
    "not mentioned",
    "not addressed",
    "not covered",
    "cannot determine",
    "can't determine",
    "unable to determine",
    "does not mention",
    "doesn't mention",
    "not specify",
    "doesn't specify",
    "does not specify",
    "i don't have",
    "i do not have",
    "context does not",
    "context doesn't",
]


def is_grounded_refusal(answer_text: str) -> bool:
    """
    TODO: Pure-logic check, no API call. Given the model's raw answer
    text, return True if the answer honestly indicates the context
    doesn't contain enough information to answer the question, and False
    if it looks like the model answered anyway (grounded or not).

    Hint: lowercase the answer text and check whether ANY phrase in
    REFUSAL_PHRASES appears as a substring.
    """
    raise NotImplementedError("Fill in is_grounded_refusal()")


def run_verification_challenge():
    """
    TODO: For each question in UNANSWERABLE_QUESTIONS:
      1. Run it through answer_question() against sample_handbook.pdf.
      2. Check whether is_grounded_refusal(result["answer"]) is True.
      3. Print a clear VERIFIED / FAILED line for each question, plus the
         model's actual answer text so a human can double check the
         automatic classification isn't fooling itself.

    A "PASS" here means the system chose honesty over a fluent guess on a
    fact that plainly doesn't exist in the source. A "FAIL" -- an answer
    that doesn't explicitly refuse, especially one with citations attached
    to a fact the source doesn't contain -- is the exact ungrounded-guess
    failure mode this whole exercise exists to catch.
    """
    raise NotImplementedError("Fill in run_verification_challenge()")


# ---------------------------------------------------------------------------
# Offline test (no API key required) -- get this working first
# ---------------------------------------------------------------------------

def offline_test():
    """
    Validates is_grounded_refusal() against fake answer text -- no API
    access needed. Run this first.
    """
    print("--- Testing is_grounded_refusal() ---")

    honest_refusal = (
        "The provided context does not contain information about tuition "
        "reimbursement or continuing education benefits, so I cannot "
        "answer this question."
    )
    assert is_grounded_refusal(honest_refusal) is True, (
        "An explicit 'context does not contain' refusal should be detected "
        "as a grounded refusal."
    )

    fluent_guess = (
        "Yes, the company offers a tuition reimbursement program covering "
        "up to $5,000 per year for approved degree programs [1]."
    )
    assert is_grounded_refusal(fluent_guess) is False, (
        "A confident, cited-sounding answer should NOT be classified as a "
        "refusal, even though this specific fact is fabricated -- "
        "is_grounded_refusal() only detects the refusal LANGUAGE, not "
        "whether a claim is actually true. That's exactly why it has to "
        "be paired with a human checking the cited chunk text by hand."
    )

    grounded_answer = (
        "Full-time employees accrue 18 days of PTO per calendar year [1]."
    )
    assert is_grounded_refusal(grounded_answer) is False, (
        "A normal grounded answer with a real citation is not a refusal."
    )

    print("is_grounded_refusal() looks correct.\n")
    print("All offline tests passed.")


if __name__ == "__main__":
    offline_test()
    print("\n" + "=" * 70)
    print("Now attempting the verification challenge (requires ANTHROPIC_API_KEY)...")
    print("=" * 70)
    run_verification_challenge()
