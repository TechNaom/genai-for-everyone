# Session 3.2 Project: Word Counts Alone

The Pro path build for Session 3.2 — a direct, hands-on follow-up to the Core
path exercise's final question: what happens if you rebuild the same 20
sentences' vectors using *only* raw word counts, with no hand-seeded "concept
anchor" topic scores at all?

## What you'll build

`starter.py` reuses the exact same 20 sentences, topic labels, tokenizer, and
plotting code as the Core path exercise (`../exercises/`), so the two plots
are a fair, apples-to-apples comparison. One function is left for you to fill
in:

- `build_wordcount_only_vectors(sentences, vocab)` — for each sentence, build
  a vector of length `len(vocab)` where position `i` counts how many times
  `vocab[i]` appears in that sentence, then L2-normalize each sentence's
  vector (guarding against dividing by zero for any all-zero row). This is
  exactly the "word-count matrix" half of the Core path exercise's hybrid
  embedding — minus the concept-anchor seed score half, and minus the final
  `np.hstack` concatenation step.

`cosine_similarity()`, `reduce_to_2d()`, and `plot_embeddings()` are already
provided, identical in mechanism to the Core path exercise.

## How to run it

```bash
pip install numpy scikit-learn matplotlib
python3 starter.py
```

No API key and no internet access needed — this is a fully offline exercise,
using the same libraries as the Core path exercise. It prints a vocabulary
size, a vector matrix shape, cosine-similarity sanity checks for four sentence
pairs, and saves a plot to `wordcount_only_plot.png`.

Want to see a finished version first? Run `python3 solution.py` — it saves to
`wordcount_only_plot_solution.png` and prints comparison notes explaining what
to expect.

## The comparison to make

Once your script runs end-to-end, open `wordcount_only_plot.png` side by side
with `embeddings_plot.png` from the Core path exercise (`../exercises/`). Do
the four topic clusters (pets, cooking, finance, space) still separate
clearly, or does the clustering largely disappear now that the concept-anchor
scores are gone?

The cosine-similarity sanity checks printed to the terminal are a good early
signal: compare the gap between the same-topic pairs (e.g. "two pet
sentences") and the cross-topic pair (e.g. "a pet sentence vs. a finance
sentence") against what the Core path exercise printed. That gap should be
noticeably smaller here.

## What you should see, and why

The lesson's prediction is that clustering should largely disappear — not
because the math changed (it's the exact same word-count vectors, cosine
similarity formula, and PCA reduction as before), but because these 20
sentences were deliberately written with varied vocabulary even within the
same topic ("puppy," "cat," "dog," "parrot," and "kitten" barely overlap with
each other despite all being about pets). Twenty short sentences simply don't
contain enough raw text for topic structure to emerge from word statistics
alone.

A real production embedding model doesn't have this problem: it has learned,
from billions of words of training text, that those words all relate to the
same underlying concept, so clustering by meaning emerges automatically with
no human ever hand-seeding topic categories. Scale of training data — not
different math — is what makes the difference.

## Common bug: forgetting to guard the zero-vector case

Exactly like the Core path exercise, if a sentence's word-count vector
happens to be all zeros, dividing by its norm without a guard crashes with a
`ZeroDivisionError` or silently produces `NaN` values that quietly corrupt the
whole plot. Guard it the same way: check whether the norm is `0` before
dividing, and leave the row as zeros if it is.

## Ideas to make it your own

- Try weighting the word-count vector differently (e.g. down-weighting
  extremely common words like "the" and "a") and see whether that recovers
  any of the lost clustering without reintroducing hand-seeded topic scores.
- Write five new sentences of your own, deliberately reusing the same few
  words within each topic (unlike this exercise's varied vocabulary), and see
  whether raw word counts alone can cluster them — a live demonstration of
  how much shared vocabulary actually matters for word-count-only clustering.

## Why this project matters

It's easy to walk away from the Core path exercise thinking embeddings work
by matching words in disguise — after all, the hybrid vectors did include
word counts. This project exists to break that assumption with your own
generated output: remove the hand-seeded signal, and the clustering weakens
sharply, even though nothing about the underlying math changed. That gap is
exactly what separates a small, engineered toy model from a real embedding
model trained on a genuinely large amount of text. Understanding *why* scale
matters — not just that it does — is what lets you reason clearly about
embedding quality, model selection, and retrieval failures once you're
building real RAG systems in the sessions ahead.
