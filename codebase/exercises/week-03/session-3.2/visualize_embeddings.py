"""
Session 3.2 Exercise — Visualizing Embeddings of 20 Sentences in 2D
===========================================================================

Goal: take 20 real sentences, turn them into embedding vectors, reduce
those vectors down to 2 dimensions, and plot them -- so you can SEE
sentences with similar meaning cluster together, exactly like the
session described.

TWO PATHS:

  FREE/OFFLINE PATH (default, what the TODOs below build):
    A small, fully transparent "toy" embedding built from two ingredients:
      (a) a hand-built "concept anchor" score -- how many words in each
          sentence belong to a small seed vocabulary for each of the
          four topics. This is a deliberately simplified stand-in for
          what a real embedding model learns automatically from huge
          amounts of training text -- we don't have huge amounts of
          training text here (just 20 short sentences), so we hand-seed
          the topic signal instead of trying to learn it statistically.
      (b) the sentence's own raw word-count vector, which adds genuine,
          sentence-specific variation on top of the topic signal -- this
          part IS purely derived from the text itself, nothing hand-fed.
    No internet access or API key required, which matters because this
    environment doesn't have access to download real embedding models
    or call embedding APIs.

  OPTIONAL PAID-API PATH:
    If you have an Anthropic or OpenAI API key and want to see what a
    REAL production embedding model's clusters look like by comparison,
    see the `real_embeddings_optional()` function at the bottom -- it's
    commented out and not required to complete the exercise.

WHY NOT JUST RAW WORD COUNTS? If you try building vectors from nothing
but raw word counts across these 20 sentences, you'll find topic
clustering barely shows up at all -- these sentences were deliberately
written using varied vocabulary (different specific nouns like "puppy",
"cat", "dog", "parrot" within the SAME topic), so they share almost no
literal words with each other. That's not a bug in the exercise -- it's
an honest demonstration of a real limitation: meaningful semantic
clustering from raw word overlap alone needs much more text than 20
short sentences can provide. Real embedding models solve this by
learning from billions of words of training text, which is exactly why
they can tell "puppy" and "canine" are related despite zero letter
overlap. Our small hand-seeded concept signal is a simplified stand-in
for that learned knowledge, scaled down to work with almost no data.

WHAT YOU NEED TO BUILD
-----------------------
1. build_vocabulary()        -- collect every unique word across all sentences (provided)
2. build_concept_vectors()   -- TODO: build the hybrid seed+word-count vectors
3. cosine_similarity()       -- TODO: implement the formula from the session
4. reduce_to_2d()            -- provided (uses scikit-learn's PCA)
5. plot_embeddings()         -- provided (uses matplotlib)

Run this file directly: python3 visualize_embeddings.py
It will save a plot to embeddings_plot.png
"""

import re

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Step 1: The 20 sentences -- four topics, five sentences each
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

# A small hand-built "concept anchor" seed vocabulary for each topic. This
# stands in for the huge amount of training text a real embedding model
# would use to learn that these words relate to a shared topic -- see the
# module docstring above for why this is necessary with so little text.
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


# ---------------------------------------------------------------------------
# Step 2: Tokenize and build a vocabulary (provided)
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
# Step 3 (TODO): Build the hybrid embedding vectors
# ---------------------------------------------------------------------------

def build_concept_vectors(sentences: list, vocab: list) -> np.ndarray:
    """
    TODO: Build a hybrid embedding vector for each sentence, combining two
    ingredients:

      (a) SEED SCORE (4 numbers per sentence): for each topic in
          SEED_WORDS, count how many of the sentence's words appear in
          that topic's seed list. This gives a vector of length 4 per
          sentence -- e.g. a sentence that uses 5 "pets" seed words and 0
          of any other topic's seed words gets [5, 0, 0, 0].

      (b) WORD-COUNT VECTOR (len(vocab) numbers per sentence): the same
          kind of raw word-count vector from the lesson -- position i
          counts how many times vocab[i] appears in that sentence.

    Then:
      1. L2-normalize each sentence's seed-score vector (divide by its
         own length, i.e. np.linalg.norm) -- guard against dividing by
         zero for sentences with no seed words at all.
      2. L2-normalize each sentence's word-count vector the same way.
      3. Concatenate them as: (seed_vector_normalized * 2.0) followed by
         (word_count_vector_normalized * 1.0). The 2.0/1.0 weighting
         makes topic identity the dominant signal while still letting
         each sentence's own specific words add real variation.

    Returns a numpy array of shape (len(sentences), 4 + len(vocab)).

    Hint: build the seed-score matrix and the word-count matrix
    separately first (each as its own small loop), normalize each one,
    then use np.hstack to concatenate them column-wise.
    """
    raise NotImplementedError("Fill in build_concept_vectors()")


# ---------------------------------------------------------------------------
# Step 4 (TODO): Cosine similarity, from the session's formula
# ---------------------------------------------------------------------------

def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    TODO: Implement cosine similarity exactly as shown in the session:

        cosine_similarity(A, B) = (A · B) / (|A| × |B|)

    Where A · B is the dot product, and |A|, |B| are the vector lengths
    (Euclidean norms).

    Handle the edge case where either vector is all zeros (length 0) --
    return 0.0 in that case rather than dividing by zero.
    """
    raise NotImplementedError("Fill in cosine_similarity()")


def print_similarity_examples(vectors: np.ndarray, sentences: list):
    """
    Prints cosine similarity between a few interesting sentence pairs,
    so you can sanity-check your implementation before trusting the plot.
    """
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


# ---------------------------------------------------------------------------
# Step 5: Reduce to 2D and plot (provided)
# ---------------------------------------------------------------------------

def reduce_to_2d(vectors: np.ndarray) -> np.ndarray:
    """
    Reduce high-dimensional vectors down to 2D using PCA, so we can plot
    them. This is the same general idea -- preserve relative distances
    while flattening dimensions -- that the session described as
    "flattening a globe into a 2D map."
    """
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
    """Scatter-plot the 2D coordinates, colored by topic, saved to out_path."""
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
# OPTIONAL PAID-API PATH (not required -- see docstring at top of file)
# ---------------------------------------------------------------------------

def real_embeddings_optional(sentences: list) -> np.ndarray:
    """
    OPTIONAL: if you have an OpenAI API key, this shows how you'd get
    REAL embeddings instead of the toy ones above, for comparison.
    Requires: pip install openai --break-system-packages
    Requires: OPENAI_API_KEY environment variable set.

    Not required to complete this exercise -- the toy embeddings above
    are sufficient to see real clustering behavior.
    """
    import os
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=sentences,
    )
    return np.array([item.embedding for item in response.data])


# ---------------------------------------------------------------------------
# Run it
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    vocab = build_vocabulary(SENTENCES)
    print(f"Vocabulary size: {len(vocab)} unique words")

    vectors = build_concept_vectors(SENTENCES, vocab)
    print(f"Vector matrix shape: {vectors.shape}")

    print_similarity_examples(vectors, SENTENCES)

    coords_2d = reduce_to_2d(vectors)
    plot_embeddings(coords_2d, SENTENCES, TOPIC_LABELS, "embeddings_plot.png")
