# Session 3.2 Exercise — Visualizing Embeddings of 20 Sentences in 2D

## Goal

Turn 20 real sentences into embedding vectors, reduce them to 2D, and plot
them — so you can directly *see* sentences with similar meaning cluster
together, exactly like the session described.

## Why a "toy" embedding, and why it's hybrid

This environment doesn't have network access to download real embedding
models (e.g. from Hugging Face) or call embedding APIs by default, so the
core exercise builds a small, fully transparent embedding out of two
ingredients you can read every line of:

1. A hand-built "concept anchor" score — how many words in a sentence
   belong to a small seed vocabulary for each topic. This stands in for
   the huge amount of training text a real embedding model uses to learn
   topic relationships automatically — with only 20 short sentences to
   work with, there isn't enough raw text for genuine unsupervised
   clustering to emerge from word counts alone (you can verify this
   yourself — it's worth trying pure word-count vectors first and seeing
   how little topic signal shows up, before adding the seed-concept
   layer).
2. The sentence's own raw word-count vector, which adds real,
   sentence-specific variation on top of the topic signal — this part is
   purely derived from the text itself.

If you have your own OpenAI or Anthropic API key, `real_embeddings_optional()`
at the bottom of the starter file shows how to swap in real embeddings for
comparison — entirely optional.

## Instructions

1. Open `visualize_embeddings.py`.
2. Fill in the two TODOs:
   - `build_concept_vectors()` — build the hybrid seed-topic + word-count
     vectors for each sentence.
   - `cosine_similarity()` — implement the formula from the session:
     `(A · B) / (|A| × |B|)`, handling the zero-vector edge case.
3. Run it:

   ```bash
   python3 visualize_embeddings.py
   ```

   This will print vocabulary size, vector shape, a few cosine-similarity
   sanity checks, and save a plot to `embeddings_plot.png`.

## Core path

Get the script running end-to-end. Open `embeddings_plot.png` and check:
do the four topics (pets, cooking, finance, space) visually separate into
roughly distinct regions of the plot, even though nothing in your code
ever told it which topic each sentence belonged to?

## Pro path — extended challenge

1. Add 5 more sentences of your own on a brand-new fifth topic (anything —
   sports, music, weather). Re-run the script and see whether your new
   topic forms its own visible cluster.
2. Try writing one sentence that's deliberately ambiguous between two
   topics (e.g. something about "a financial report on the pet food
   industry"). Where does it land on the plot relative to the two topic
   clusters — closer to one, or genuinely in between? Write 2-3 sentences
   on why you think it landed where it did, based on which words it shares
   with each topic's vocabulary.
3. This toy embedding is bag-of-words based — it has no sense of word
   order and no real understanding of meaning beyond shared vocabulary.
   Write one example sentence pair that you'd expect a REAL embedding
   model to correctly judge as similar, but that you'd expect this toy
   model to score as dissimilar (hint: think about synonyms that share no
   letters, like "puppy" and "canine").

## What "done" looks like

- The script runs with no errors and produces `embeddings_plot.png`.
- The four topic clusters are visually distinguishable in the plot (they
  won't be perfectly separated with this toy embedding — some overlap is
  expected and fine).
- Your cosine similarity sanity checks show clearly higher scores for
  same-topic pairs than for cross-topic pairs.

## Stuck?

A fully worked reference solution, including the Pro path answers, is in
`codebase/solutions/week-03/session-3.2/`.
