# Session 3.2 Exercise: Visualize Embeddings of 20 Sentences in 2D

**Goal:** Turn 20 real sentences into embedding vectors, reduce them to 2D,
and plot them — so you can directly *see* sentences with similar meaning
cluster together, exactly like the session described.

## Why a "toy" embedding, and why it's hybrid

Building a real, trained embedding model from scratch isn't something you'll
do today (or, frankly, something almost anyone builds from scratch at all —
you'll typically call an existing embedding model, the way you called LLM
APIs in Week 1). So this exercise builds a small, fully transparent embedding
out of two ingredients you can read every line of:

1. A hand-built "concept anchor" score — how many words in a sentence belong
   to a small seed vocabulary for each topic. This stands in for the huge
   amount of training text a real embedding model uses to learn topic
   relationships automatically — with only 20 short sentences to work with,
   there isn't enough raw text for genuine unsupervised clustering to emerge
   from word counts alone (it's worth trying pure word-count vectors first
   and seeing how little topic signal shows up, before adding the
   seed-concept layer — that comparison is exactly what the Pro path project
   for this session builds).
2. The sentence's own raw word-count vector, which adds real,
   sentence-specific variation on top of the topic signal — this part is
   purely derived from the text itself.

If you have your own OpenAI or Anthropic API key, `real_embeddings_optional()`
at the bottom of the starter file shows how to swap in real embeddings for
comparison — entirely optional.

## How to run

You'll need Python 3, plus `numpy`, `scikit-learn`, and `matplotlib`:

```bash
pip install numpy scikit-learn matplotlib
```

Then run the starter file:

```bash
python3 starter.py
```

## The task

Open `starter.py`. Fill in the two `TODO` functions:

- **`build_concept_vectors()`** — build the hybrid seed-topic + word-count
  vectors for each sentence. For each sentence, count how many of its words
  appear in each topic's seed list (a 4-number "seed score"), L2-normalize
  it, then do the same for the sentence's raw word-count vector, and
  concatenate the two (seed score weighted 2.0x, word counts weighted 1.0x)
  so topic identity dominates while each sentence still keeps its own
  specific variation.
- **`cosine_similarity()`** — implement the formula from the lesson:
  `(A · B) / (|A| × |B|)`, handling the zero-vector edge case by returning
  `0.0`.

Run it again after each edit. It prints the vocabulary size, the vector
matrix shape, a handful of cosine-similarity sanity checks (same-topic pairs
should score noticeably higher than cross-topic pairs), and saves a plot to
`embeddings_plot.png`.

## Core path

Get the script running end-to-end. Open `embeddings_plot.png` and check: do
the four topics (pets, cooking, finance, space) visually separate into
roughly distinct regions of the plot, even though nothing in your code ever
told it which topic each sentence belonged to?

An example of what a correct run produces is included in this folder as
[`embeddings_plot_solution.png`](embeddings_plot_solution.png) — your own
plot's exact layout will differ (PCA is sensitive to the input vectors), but
the four topic clusters should be similarly distinguishable.

## Pro path — extended challenge

Once the Core path is working, head to [`../project/`](../project/) for the
extended challenge: rebuild the same 20 sentences' vectors using *only* raw
word counts, with no concept-anchor scores at all, and compare the resulting
plot to your Core path version. You should see the clustering largely
disappear — direct, hands-on evidence for why scale of training data (not
different math) is what lets real embedding models cluster by meaning
without anyone hand-seeding topic categories.

## What "done" looks like

- The script runs with no errors and produces `embeddings_plot.png`.
- The four topic clusters are visually distinguishable in the plot (they
  won't be perfectly separated with this toy embedding — some overlap is
  expected and fine).
- Your cosine similarity sanity checks show clearly higher scores for
  same-topic pairs than for cross-topic pairs.

## Stuck?

A fully worked reference solution is in [`solution.py`](solution.py) — try
the exercise yourself first. The value is in implementing the hybrid
embedding and cosine similarity from the formula, and watching real
clustering emerge, not in reading someone else's implementation.
