"""
Session 3.2 Project: Word Counts Alone (the Pro path)
See README.md in this folder for the full brief.

This is the Pro path build for Session 3.2 -- the extended challenge from
the lesson's final section ("What '20 sentences in 2D' is actually showing
you"). The Core path exercise (../exercises/starter.py) built a HYBRID toy
embedding: a hand-seeded "concept anchor" topic score, PLUS each sentence's
own raw word-count vector. That hybrid is what made the four topic clusters
(pets, cooking, finance, space) visually separate in the plot.

This project asks a sharper question: what happens if you remove the
hand-seeded part entirely, and build vectors from NOTHING but raw word
counts? The lesson's prediction is that clustering should largely
disappear -- not because the math changes, but because 20 short sentences,
deliberately written with varied vocabulary even within the same topic,
don't contain enough raw text for topic structure to emerge from word
statistics alone. This is the exact gap that separates a hand-seeded toy
model from what a real embedding model does automatically after learning
from billions of words of training text.

No API calls needed -- this is a pure, fully offline exercise. Only numpy,
scikit-learn, and matplotlib are required (the same libraries as the Core
path exercise).
"""

import re

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# The same 20 sentences as the Core path exercise, so the two plots are a
# fair, apples-to-apples comparison.
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tokenize and build a vocabulary (provided -- identical to the Core path)
# ---------------------------------------------------------------------------

def tokenize(sentence: str) -> list:
    """Lowercase and split into words, stripping punctuation."""
    return re.findall(r"[a-z']+", sentence.lower())


def build_vocabulary(sentences: list) -> list:
    """Return a sorted list of every unique word across all sentences."""
    vocab = set()
    for sentence in sentences:
        vocab.update(tokenize(sentence))
    return sorted(vocab)


# ---------------------------------------------------------------------------
# TODO: Build vectors from RAW WORD COUNTS ONLY -- no concept-anchor scores
# ---------------------------------------------------------------------------

def build_wordcount_only_vectors(sentences: list, vocab: list) -> np.ndarray:
    """
    TODO: Build a word-count-only vector for each sentence -- deliberately
    WITHOUT the hand-seeded "concept anchor" topic scores the Core path
    exercise added.

    For each sentence, build a vector of length len(vocab) where position i
    counts how many times vocab[i] appears in that sentence (the same raw
    word-count vector the Core path exercise used as HALF of its hybrid --
    here it's the WHOLE vector). Then L2-normalize each sentence's vector
    (divide by its own np.linalg.norm), guarding against dividing by zero
    for any row that happens to be all zeros.

    Returns a numpy array of shape (len(sentences), len(vocab)).

    Hint: this is exactly the "word-count matrix" half of
    build_concept_vectors() from the Core path exercise, minus the seed
    score half and minus the final np.hstack concatenation step.
    """
    raise NotImplementedError("Fill in build_wordcount_only_vectors()")


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Cosine similarity, same formula as the lesson and the Core path
    exercise: (A . B) / (|A| * |B|), with a zero-vector guard.
    Provided here so you can reuse it for the sanity checks below without
    re-implementing it.
    """
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def print_similarity_examples(vectors: np.ndarray, sentences: list):
    """Same sanity-check pairs as the Core path exercise, for comparison."""
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


# ---------------------------------------------------------------------------
# Reduce to 2D and plot (provided -- identical mechanism to the Core path)
# ---------------------------------------------------------------------------

def reduce_to_2d(vectors: np.ndarray) -> np.ndarray:
    """Reduce high-dimensional vectors down to 2D using PCA, so we can plot them."""
    pca = PCA(n_components=2, random_state=42)
    return pca.fit_transform(vectors)


def plot_embeddings(coords_2d: np.ndarray, labels: list, out_path: str):
    """Scatter-plot the 2D coordinates, colored by topic, saved to out_path."""
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


# ---------------------------------------------------------------------------
# Run it
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    vocab = build_vocabulary(SENTENCES)
    print(f"Vocabulary size: {len(vocab)} unique words")

    vectors = build_wordcount_only_vectors(SENTENCES, vocab)
    print(f"Vector matrix shape: {vectors.shape}")

    print_similarity_examples(vectors, SENTENCES)

    coords_2d = reduce_to_2d(vectors)
    plot_embeddings(coords_2d, TOPIC_LABELS, "wordcount_only_plot.png")

    print(
        "\nCompare wordcount_only_plot.png against embeddings_plot.png from "
        "the Core path exercise (../exercises/). Do the four topic clusters "
        "still separate clearly, or does the clustering largely disappear "
        "now that the concept-anchor scores are gone?"
    )
