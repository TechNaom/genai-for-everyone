"""
Session 3.2 — Reference Solution
Visualizing Embeddings of 20 Sentences in 2D
===========================================================================

Try the exercise yourself first -- the value is in implementing the
hybrid embedding and cosine similarity from the formula, and seeing real
clustering emerge, not in reading someone else's implementation.

See the docstring in the starter file (visualize_embeddings.py) for the
full explanation of why this toy embedding combines hand-seeded "concept
anchor" scores with raw word counts, instead of using pure word-count
vectors alone.
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

SEED_WORDS = {
    "pets": ["puppy", "cat", "dog", "parrot", "kitten", "pet", "shelter", "adopted",
             "nap", "sunny", "window", "ran", "park", "chasing", "ball", "trained",
             "words", "knocked", "plant", "shelf", "loves", "say", "few"],
    "cooking": ["bread", "recipe", "flour", "butter", "grilled", "vegetables",
                "chicken", "basil", "tomato", "sauce", "chef", "dessert", "caramel",
                "baked", "loaf", "sourdough", "morning", "cups", "dinner", "tonight",
                "fresh", "added", "plated", "drizzle"],
    "finance": ["stock", "prices", "bank", "interest", "rates", "investors",
                "inflation", "revenue", "markets", "earnings", "merger", "quarter",
                "company's", "economy", "fell", "sharply", "report", "raised",
                "worried", "rising", "numbers", "grew", "double", "digits", "year",
                "rallied", "announced", "central"],
    "space": ["telescope", "galaxy", "astronomers", "exoplanet", "star", "rocket",
              "orbit", "saturn", "scientists", "space", "spacewalk", "captured",
              "stunning", "image", "distant", "discovered", "faint", "launched",
              "successfully", "low", "earth", "studying", "rings", "station",
              "crew", "conducted", "yesterday"],
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


def build_concept_vectors(sentences: list, vocab: list) -> np.ndarray:
    """Hybrid embedding: normalized seed-topic score + normalized word counts."""
    word_to_idx = {word: i for i, word in enumerate(vocab)}
    topics = list(SEED_WORDS.keys())

    # (a) Seed score: count of seed words per topic, per sentence
    seed_matrix = np.zeros((len(sentences), len(topics)))
    for row, sentence in enumerate(sentences):
        words = tokenize(sentence)
        for col, topic in enumerate(topics):
            seed_matrix[row, col] = sum(1 for w in words if w in SEED_WORDS[topic])

    # (b) Raw word-count vector per sentence
    word_count_matrix = np.zeros((len(sentences), len(vocab)))
    for row, sentence in enumerate(sentences):
        for word in tokenize(sentence):
            word_count_matrix[row, word_to_idx[word]] += 1

    # Normalize each block independently, then weight and concatenate
    seed_norm = _normalize_rows(seed_matrix)
    word_count_norm = _normalize_rows(word_count_matrix)

    return np.hstack([seed_norm * 2.0, word_count_norm * 1.0])


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
    print("\n--- Cosine similarity sanity checks ---")
    for i, j, label in pairs_to_check:
        sim = cosine_similarity(vectors[i], vectors[j])
        print(f"{label}: {sim:.3f}")
        print(f"  '{sentences[i]}'")
        print(f"  '{sentences[j]}'\n")


def reduce_to_2d(vectors: np.ndarray) -> np.ndarray:
    pca = PCA(n_components=2, random_state=42)
    return pca.fit_transform(vectors)


TOPIC_LABELS = (
    ["pets"] * 5 + ["cooking"] * 5 + ["finance"] * 5 + ["space"] * 5
)
TOPIC_COLORS = {
    "pets": "#D17A22",
    "cooking": "#2E7D5B",
    "finance": "#1E2761",
    "space": "#7B2D8E",
}


def plot_embeddings(coords_2d: np.ndarray, sentences: list, labels: list, out_path: str):
    plt.figure(figsize=(10, 7))
    for topic, color in TOPIC_COLORS.items():
        idxs = [i for i, label in enumerate(labels) if label == topic]
        plt.scatter(
            coords_2d[idxs, 0], coords_2d[idxs, 1],
            label=topic, color=color, s=80, alpha=0.85, edgecolors="white",
        )
    plt.title("20 Sentences in 2D Embedding Space (toy embeddings, PCA-reduced)")
    plt.xlabel("Component 1")
    plt.ylabel("Component 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"\nPlot saved to {out_path}")


# ---------------------------------------------------------------------------
# Pro path answers
# ---------------------------------------------------------------------------

PRO_PATH_ANSWERS = """
Pro path answers:

1. Adding a 5th topic: five sentences about a new topic (e.g. weather)
   that don't share seed words with the other four topics' SEED_WORDS
   lists will land in their own region of the plot, dominated by their
   own word-count signal alone (since they'd score 0 on all four
   existing topic seed lists) -- a good illustration of what happens
   when this toy model encounters a topic it has no "concept anchor"
   for at all, similar to how a real embedding model can still represent
   genuinely novel text, just without any special boost from prior
   topic structure.

2. Ambiguous sentence ("a financial report on the pet food industry"):
   this sentence would score on BOTH the finance seed list ("report",
   "financial"-adjacent words) and the pets seed list ("pet"). Where it
   lands depends on which seed score is larger -- if it has more finance
   seed words than pet seed words, the 2.0-weighted seed component pulls
   it toward the finance cluster, with the pet-seed component pulling
   slightly the other way. This demonstrates a real, general property of
   embeddings: a text that's genuinely ambiguous between two topics
   often lands geometrically *between* their respective regions, rather
   than cleanly inside either one.

3. Synonym example a real model would catch but this toy embedding would
   miss: "I adopted a puppy" vs. "I welcomed a new canine companion" --
   "puppy" is in our pets seed list, but "canine" is not (since we only
   hand-seeded a specific list of words that actually appear in our 20
   sentences). A real embedding model, trained on enormous amounts of
   text, has learned that "puppy" and "canine" appear in highly similar
   contexts and would score these as highly similar regardless of seed
   lists. This is the central limitation of any hand-seeded toy model:
   it can only recognize concept words it was explicitly told about,
   while a real embedding model generalizes to synonyms and related
   concepts it was never explicitly given a list for.
"""


if __name__ == "__main__":
    vocab = build_vocabulary(SENTENCES)
    print(f"Vocabulary size: {len(vocab)} unique words")

    vectors = build_concept_vectors(SENTENCES, vocab)
    print(f"Vector matrix shape: {vectors.shape}")

    print_similarity_examples(vectors, SENTENCES)

    coords_2d = reduce_to_2d(vectors)
    plot_embeddings(coords_2d, SENTENCES, TOPIC_LABELS, "embeddings_plot_solution.png")

    print(PRO_PATH_ANSWERS)
