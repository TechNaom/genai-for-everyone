# Session 3.5 Project: The Surface-Word Overlap Investigation

The Pro path build for Session 3.5 — a direct extension of the exercises'
Case 2 (`../exercises/broken_pipeline.py`), built on the lesson's own
Pro path challenge: for the retrieval-miss case, don't just confirm the
correct chunk is absent from the top-3 — look at what *did* get
retrieved instead, and find the specific surface-level word overlap that
let each wrong chunk outrank the one that actually answers the question.

## The setup

Case 2's exact question and configuration, reproduced here on purpose
(not modified): `"Can I telecommute instead of going to the office?"`
against `chunk_size=100, overlap=20`. The exercises worksheet already
established this is a retrieval miss — the handbook's Remote Work
Policy section never appears in the top-3. This project goes one layer
deeper into *why*.

## What you'll build

Two functions and a written analysis:

- `shared_words(query, chunk)` — returns the sorted list of words that
  literally appear in both the query and a given chunk, using the
  provided `tokenize()`. This turns "surface-level word overlap" from a
  vague phrase into something concrete and checkable.
- `find_chunk_by_keyword(full_ranking, keyword)` — searches the FULL
  ranking (every chunk in the store, not just the top-3 the broken
  pipeline actually used) for the first chunk containing a known
  keyword, and reports its true rank and score.
- An `ANALYSIS` dict with three fields to fill in after running the
  investigation:
  - `coincidental_shared_word` — of the top-3 wrongly-retrieved chunks,
    one shares a specific, low-frequency *content* word with the query
    that the others don't (not a generic stopword like "the" or "of").
    Which word, and which chunk does it come from?
  - `would_a_bigger_k_reliably_fix_this` — the correct chunk's true rank
    turns out to be close to, but just outside, the k=3 cutoff. Does
    that mean a slightly larger k would reliably fix this question? What
    would you need to check before trusting that as a general fix,
    rather than a coincidence of this one phrasing?
  - `proposed_fix` — what you'd actually change.

## How to run

```bash
pip install pdfplumber numpy --break-system-packages
python3 starter.py
```

No API key and no internet access needed — this is a pure offline
investigation against the included `sample_handbook.pdf`. Want to see a
finished version first? Run `python3 solution.py`.

## The habit this trains

"The correct chunk didn't make the top-3" is a useful diagnosis, but
it's an incomplete one — it tells you a miss happened without telling
you anything about *why the wrong chunks won*. In a raw word-count
similarity system (and, less obviously, in some real embedding failures
too), the answer is often mundane and specific: a completely unrelated
chunk happens to share one rare word with the query, and that single
coincidental match is enough to outscore a chunk that's actually on
topic but phrased differently. Learning to go find that specific word
— rather than stopping at "retrieval missed it" — is what turns a
diagnosis into something you can actually act on: you now know not just
*that* the embedding is weak, but a concrete example of *how* it gets
fooled, which is exactly the kind of evidence that convinces a team to
invest in a better embedding model or a re-ranking step.

## Ideas to make it your own (optional stretch goals)

- Run the same investigation against Case 1's question ("How many sick
  days do employees get and do they roll over?") using
  `chunk_size=15, overlap=0` instead — does a similar coincidental
  word-overlap pattern show up there, or is that case purely a chunking
  problem with no interesting overlap story?
- Try rephrasing the query to remove the coincidental overlap (e.g. drop
  "instead of") and see whether the correct chunk's rank improves,
  stays the same, or gets worse — this tests directly whether the
  overlap you identified was actually load-bearing for the wrong
  chunk's score.

## Why this project matters

"The retrieval missed it" is where most debugging stops in practice,
and it's not wrong — but it's also not specific enough to fix anything
with confidence. The engineers who get RAG systems to actually work in
production are the ones who go one step further and ask "missed it in
favor of *what*, and *why did that win*?" That's the difference between
noticing a fire and finding the spark — and it's the same instinct that
will matter next session, when you're building a system with no
failure mode handed to you and have to find your own sparks.
