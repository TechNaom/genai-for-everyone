# Session 3.3 Project: The Chunk-Size Showdown

The Pro path build for Session 3.3 — the exercise had you run the
sick-leave question against the handbook at different chunk sizes
yourself, one at a time, and eyeball the difference. This project
packages that same trade-off as one direct, side-by-side comparison:
build two vector stores over the same PDF at two different chunk sizes,
run the exact same hard question against both, and read the actual
retrieved chunks next to each other.

## What you'll build

`starter.py` already contains the complete chunking/embedding/retrieval
pipeline — the same `chunk_text()`, `embed_chunks()`,
`cosine_similarity()`, and `VectorStore` you built in the Session 3.3
exercise. Running it builds two vector stores over `sample_handbook.pdf`
— one at `chunk_size=100`, one at `chunk_size=30` — and prints the top-3
retrieved chunks for the question *"How many sick days do employees get
and do they roll over?"* at each setting, one right after the other.

Your job is the `ANALYSIS` dictionary at the bottom of the file. Fill in
four fields based on what you actually see printed:

- `larger_chunks_top_result_is_correct` — does the top-ranked result at
  `chunk_size=100` actually answer the sick-leave question?
- `smaller_chunks_correct_chunk_rank` — at `chunk_size=30`, what rank does
  the genuinely correct sick-leave chunk land at?
- `why_chunk_size_changes_the_winner` — one to two sentences on why
  shrinking the chunk size changes which chunk wins.
- `downstream_risk_of_the_wrong_chunk` — one to two sentences on what
  breaks if a RAG system generated an answer from the wrong chunk.

Example run (after filling in `ANALYSIS`):

```
Q: "How many sick days do employees get and do they roll over?"

--- Larger chunks (chunk_size=100, overlap=20 -> 11 chunks) ---
  [1] sim=0.287  20 hours per week accrue PTO on a pro-rated basis, calculated
                 as a percentage of the full-time accrual rate equal to their
                 average weekly hours divide...
  [2] sim=0.176  employee per calendar year for employees in approved remote
                 or hybrid arrangements. This allowance does not roll over
                 between years and resets each Ja...
  [3] sim=0.175  Brightleaf Software Inc. -- Employee Handbook This handbook
                 describes company policies on leave, remote work, expenses,
                 and benefits. It is intended as...

--- Smaller chunks (chunk_size=30, overlap=5 -> 33 chunks) ---
  [1] sim=0.310  not roll over between years and resets each January 1st
                 regardless of how much of the prior year's allowance was
                 used. 5. Health and Retirement Benefi...
  [2] sim=0.310  available in full starting January 1st rather than accruing
                 monthly. Sick days do not carry over to the following year
                 and are not paid out upon separ...
  [3] sim=0.235  for accrued PTO under this policy. 2. Sick Leave Sick leave
                 is tracked separately from PTO. Full-time employees receive
                 10 sick days per calendar year...
```

## How to run it

```bash
pip install numpy pdfplumber --break-system-packages
python3 starter.py
```

No API key and no internet access needed — it's fully offline, and it
reuses the exact word-count embedding pipeline from the Session 3.3
exercise. `starter.py` needs `sample_handbook.pdf` in the same folder to
run. Want to see the finished comparison and analysis first? Run
`python3 solution.py`.

## The habit this trains

Don't guess at the four `ANALYSIS` answers before running the code — run
`starter.py` first, read the actual printed similarity scores and chunk
previews, and base your answers on what's really there. The honest result
here isn't a clean win for either setting: the smaller chunks get closer
to the right answer, but even they don't produce an unambiguous rank-1
hit — the correct sick-leave chunk lands in a near-tie for the top spot,
not a clean win. Reporting that honestly, instead of rounding it up to
"smaller chunks fixed it," is exactly the kind of judgment call a
retrieval system in production forces on you constantly.

## Ideas to make it your own (optional stretch goals)

- Add a third entry to `CHUNK_SETTINGS` (try `chunk_size=250, overlap=40`)
  and extend the printed comparison to three columns instead of two.
- Swap in one of the other four test questions from the exercise and see
  whether the same chunk-size pattern holds, or whether that question is
  already solved cleanly at the default setting.

## Why this project matters

Every retrieval system ships with a chunk-size decision baked in, and
that decision is invisible until a specific question exposes it — usually
in production, in front of a real user, not in a demo. The sick-leave
question here is a small, contained version of that exact failure: two
real policies (PTO and sick leave) share enough surface vocabulary that a
plausible-looking chunking choice can silently retrieve the wrong one.
Seeing the actual side-by-side comparison, with real similarity scores
instead of a hand-wavy description of the trade-off, is what makes "tune
your chunk size and monitor retrieval quality" a concrete practice
instead of a slide-deck platitude.
