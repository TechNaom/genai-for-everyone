"""
Session 3.2 Project -- Reference Solution
Word Counts Alone (the Pro path)
===========================================================================

Try the exercise yourself first -- the value is in building the word-count
vectors yourself and watching the clustering weaken with your own eyes, not
in reading someone else's implementation.

See the docstring in the starter file (starter.py) for the full explanation
of why this project removes the hand-seeded "concept anchor" scores that the
Core path exercise (../exercises/) relied on.
"""

import re

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


SENTENCES = [
    # Topic: pets / animals
    "I adopted a puppy from the shelter last weekend",
    "My cat loves to nap in the sunny window",
    "The dog ran across the park chasing a ball",
    "She trained her parrot to say a few words",
    "Our new kitten knocked a plant off the shelf",
    # Topic: cooking / food
    "I baked a loaf of sourdough bread this morning",
    "The recipe calls for two cups of flour and butter",
    "We grilled vegetables and chicken for dinner tonight",
    "She added fresh basil to the tomato sauce",
    "The chef plated the dessert with a drizzle of caramel",
    # Topic: finance / markets
    "Stock prices fell sharply after the earnings report",
    "The central bank raised interest rates again this quarter",
    "Investors are worried about rising inflation numbers",
    "The company's revenue grew by double digits last year",
    "Markets rallied after the merger was announced",
    # Topic: space / astronomy
    "The telescope captured a stunning image of a distant galaxy",
    "Astronomers discovered a new exoplanet orbiting a faint star",
    "The rocket launched successfully into low Earth orbit",
    "Scientists are studying the rings around Saturn",
    "The space station crew conducted a spacewalk yesterday",
]

TOPIC_LABELS = (
    ["pets"] * 5 + ["cooking"] * 5 + ["finance"] * 5 + ["space"] * 5
)
TOPIC_COLORS = {
    "pets": "#D17A22",
    "cooking": "#2E7D5B",
    "finance": "#1E2761",
    "space": "#7B2D8E",
}


def tokenize(sentence: str) -> list:
    return re.findall(r"[a-z']+", sentence.lower())


def build_vocabulary(sentences: list) -> list:
    vocab = set()
    for sentence in sentences:
        vocab.update(tokenize(sentence))
    return sorted(vocab)


def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
    """L2-normalize each row, guarding against rows that are all zero."""
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0  # avoid divide-by-zero; zero rows stay zero
    return matrix / norms


def build_wordcount_only_vectors(sentences: list, vocab: list) -> np.ndarray:
    """Raw word-count vectors only -- no concept-anchor seed scores at all."""
    word_to_idx = {word: i for i, word in enumerate(vocab)}

    word_count_matrix = np.zeros((len(sentences), len(vocab)))
    for row, sentence in enumerate(sentences):
        for word in tokenize(sentence):
            word_count_matrix[row, word_to_idx[word]] += 1

    return _normalize_rows(word_count_matrix)


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """cosine_similarity(A, B) = (A . B) / (|A| * |B|)"""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def print_similarity_examples(vectors: np.ndarray, sentences: list):
    pairs_to_check = [
        (0, 1, "two pet sentences"),
        (0, 10, "a pet sentence vs. a finance sentence"),
        (5, 8, "two cooking sentences"),
        (15, 17, "two space sentences"),
    ]
    print("\n--- Cosine similarity sanity checks (word counts only) ---")
    for i, j, label in pairs_to_check:
        sim = cosine_similarity(vectors[i], vectors[j])
        print(f"{label}: {sim:.3f}")
        print(f"  '{sentences[i]}'")
        print(f"  '{sentences[j]}'\n")


def reduce_to_2d(vectors: np.ndarray) -> np.ndarray:
    pca = PCA(n_components=2, random_state=42)
    return pca.fit_transform(vectors)


def plot_embeddings(coords_2d: np.ndarray, labels: list, out_path: str):
    plt.figure(figsize=(10, 7))
    for topic, color in TOPIC_COLORS.items():
        idxs = [i for i, label in enumerate(labels) if label == topic]
        plt.scatter(
            coords_2d[idxs, 0], coords_2d[idxs, 1],
            label=topic, color=color, s=80, alpha=0.85, edgecolors="white",
        )
    plt.title("20 Sentences in 2D -- Raw Word Counts Only (no concept anchors)")
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"\nPlot saved to {out_path}")


COMPARISON_NOTES = """
What to expect, compared to the Core path plot (../exercises/):

With the concept-anchor scores removed, the cosine-similarity sanity checks
above should show a much smaller gap between the "two pet sentences" pair
and the "pet vs. finance" pair than the Core path exercise did -- because
these 20 sentences were deliberately written with varied vocabulary even
within the same topic ("puppy", "cat", "dog", "parrot", "kitten" barely
overlap with each other despite all being about pets). With no hand-seeded
signal telling the vectors which words relate to which topic, raw word
counts alone have very little shared vocabulary to latch onto within a
topic, so the four clusters in wordcount_only_plot.png should look
noticeably more scattered and overlapping than in the Core path's
embeddings_plot.png.

This isn't a bug or a weaker implementation -- it's the whole point of the
Pro path challenge. It demonstrates, with your own generated output, why a
toy model needs engineered help to cluster with only 20 short sentences,
while a real production embedding model doesn't: it has learned, from
billions of words of training text, that "puppy," "cat," "dog," "parrot,"
and "kitten" all relate to the same underlying concept, even without ever
sharing a letter with each other. Scale of training data -- not different
math -- is what lets real embeddings cluster by meaning without anyone
hand-seeding topic categories.
"""


if __name__ == "__main__":
    vocab = build_vocabulary(SENTENCES)
    print(f"Vocabulary size: {len(vocab)} unique words")

    vectors = build_wordcount_only_vectors(SENTENCES, vocab)
    print(f"Vector matrix shape: {vectors.shape}")

    print_similarity_examples(vectors, SENTENCES)

    coords_2d = reduce_to_2d(vectors)
    plot_embeddings(coords_2d, TOPIC_LABELS, "wordcount_only_plot_solution.png")

    print(COMPARISON_NOTES)
