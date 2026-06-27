# Session 3.3 Exercise — Build a Local Vector Store Over a PDF

## Goal

Take a real PDF — `sample_handbook.pdf`, a small company employee
handbook — and build the full retrieval pipeline from this session:
chunk it, embed each chunk, store the vectors, and retrieve the top-k
most relevant chunks for real test questions. This stops right before
generation — Session 3.4 adds that final step.

## Why word-count vectors work here (unlike in 3.2)

Session 3.2's exercise needed hand-seeded "concept anchors" because 20
short sentences didn't share enough vocabulary for plain word counts to
show real topic clustering. Today's chunks are full paragraphs of real
text, which changes the math: there's simply more shared, topically
relevant vocabulary per chunk, so plain word-count vectors produce
genuinely useful retrieval without any hand-seeding. You'll verify this
yourself — no concept-anchor trick needed this time.

If you have your own OpenAI or Anthropic API key, `real_embeddings_optional()`
at the bottom of the starter file shows how to swap in real embeddings —
entirely optional.

## Instructions

1. Open `build_vector_store.py`.
2. Fill in the TODOs, in order:
   - `chunk_text()` — split text into overlapping word-count chunks.
   - `embed_chunks()` — build word-count vectors for each chunk.
   - `cosine_similarity()` — same formula as Session 3.2.
   - `VectorStore.add()` and `VectorStore.search()` — a minimal
     brute-force vector store.
3. Run it:

   ```bash
   python3 build_vector_store.py
   ```

   This runs the full pipeline at chunk_size=100, overlap=20, and prints
   the top-3 retrieved chunks for five real test questions about the
   handbook.

## Core path

Get the pipeline running end-to-end with the default chunk size and
overlap. For each test question, read the top-1 retrieved chunk: does it
actually contain the information needed to answer the question? Note any
cases where it doesn't — you'll come back to this.

## Pro path — extended challenge

1. **Feel the chunk-size trade-off directly.** Call `run_pipeline()`
   three more times with different settings — try `chunk_size=30,
   overlap=5`, then `chunk_size=250, overlap=40` — on the same five test
   questions. For the sick-leave question in particular ("How many sick
   days do employees get and do they roll over?"), compare what each
   chunk size retrieves as its top result. Don't expect a perfectly clean
   win at any single setting — PTO and sick leave share a lot of
   vocabulary, so this is a genuinely hard case. Write 3-4 sentences on
   what you observe: does a smaller chunk size get closer to the right
   answer? Does a larger chunk size start pulling in the generic intro
   paragraph instead, because it mentions every topic in passing?
2. **Diagnose a real false-positive.** The handbook's opening paragraph
   mentions "leave, remote work, expenses, and benefits" — every topic in
   the document, in one sentence. At larger chunk sizes, watch for this
   intro chunk showing up as a top match for unrelated questions purely
   because it shares surface vocabulary with everything. This is a real,
   common retrieval failure mode, not a bug in your code. Write 2-3
   sentences on why a chunk like this is dangerous for a retrieval
   system, and what about it makes it score deceptively high.
3. **Try k=1 vs. k=5.** Run the same question through your store with
   `k=1` and then `k=5`. When would retrieving only the single best match
   risk missing the answer? When would retrieving 5 chunks instead of 1
   risk diluting the context handed to a model later?

## What "done" looks like

- The full pipeline runs end-to-end with no errors at the default
  settings.
- For most of the five test questions, the top-1 or top-2 retrieved chunk
  genuinely contains the answer.
- You've run the pipeline at least once more with a different chunk size
  and can describe, in your own words, how the retrieved results changed.

## Stuck?

A fully worked reference solution, including the Pro path observations,
is in `codebase/solutions/week-03/session-3.3/`.
