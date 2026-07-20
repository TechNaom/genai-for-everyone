# Session 5.2 Exercises: Eval Harness for a Contract-Clause Summarizer

## Overview

`starter.py` is a **fully working** evaluation harness, not a
fill-in-the-blank file. It scores three prompt variants of a
contract-clause summarizer using:

1. A mocked semantic-similarity metric (`mock_semantic_similarity()`),
   calibrated to reproduce the same "rewards the gist, misses the
   omitted detail" blind spot real sentence embeddings have for this
   task.
2. A mocked LLM-as-judge score (`llm_judge_score()`) with an explicit
   partial-failure cap — if a legally significant detail was omitted,
   the score is capped at 5/10 regardless of how high raw similarity
   looks.
3. The chapter's human-review routing logic (`needs_human_review()`) —
   flag if the clause type is high-risk (arbitration,
   indemnification), OR the LLM-judge score is in the uncertain middle
   (4–7), OR semantic similarity is in the deceptive middle band
   (0.70–0.85).

## What to do

This exercise is a **trace-then-extend** exercise, not a fill-in-the-blank
one — there's nothing broken to fix in the base harness.

### Part 1 — Trace it before you run it
Work through `mock_semantic_similarity()`, `llm_judge_score()`, and
`needs_human_review()` by hand for Variant A's `arb_1` clause (the one
that omits the class-action waiver). Predict:
- Its semantic similarity score (how many of the 4 tracked concepts does
  its summary actually hit?)
- Its LLM-judge score after the partial-failure cap
- Whether it gets flagged for human review, and why

Then run `python starter.py` and confirm your predictions against the
printed per-clause output.

### Part 2 — Extend it
1. Add a fourth clause (a `non_compete` type, not in the high-risk set)
   with a summary you write yourself that omits a real detail (e.g. a
   geographic scope or duration limit) and deliberately lands in the
   0.70–0.85 similarity band. Confirm the LLM-judge cap — not the
   clause-type override — is what catches it.
2. Temporarily narrow the routing band in `needs_human_review()` from
   0.70–0.85 to 0.78–0.82 and re-run. Does your new case still get
   flagged? Put the band back afterward.

### Debug the Code
A "simplified" version of `llm_judge_score()` that just returns the
scaled similarity score (deleting the partial-failure cap) silently
reintroduces the too-generous LLM-judge failure mode from Part 2 of the
lesson. See `../interview-questions.html` and the lesson's Part 2/3 for
the full explanation.

## Run it

```bash
python3 starter.py
```

No packages, no API key, no network calls needed — everything here is
pure, offline Python.

## Checking your work

Your traced predictions for `arb_1` should match exactly: similarity
0.75 (3 of 4 concepts hit), LLM-judge capped at 5/10, and flagged (both
for clause type and for landing in the middle band). `solution.py` is
the same fully-worked harness as `starter.py` — use it to confirm you
haven't changed the base behavior while adding your own extensions.

---

*Session 5.2 Exercises | GenAI for Everyone | Week 5*
