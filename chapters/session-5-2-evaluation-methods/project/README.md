# Session 5.2 Project (Pro Path): Routing Logic Stress Test

## Overview

`starter.py` is a **fully working** comparison harness, not a
fill-in-the-blank file. It builds and runs two human-review routing
strategies against a fixed 8-case test set:

1. `naive_threshold_review()` — flags a clause for human review only if
   its semantic similarity score is below 0.5.
2. `proper_routing_review()` — the chapter's full routing logic: flag
   if the clause type is high-risk (arbitration, indemnification), OR
   the LLM-judge score is in the uncertain middle (4–7), OR semantic
   similarity is in the deceptive middle band (0.70–0.85).

`evaluate_routing_strategy()` runs either strategy against all 8 cases
and reports the **false negative rate specifically among the real
omission cases** — not overall accuracy — since that's the number that
actually reflects the cost of missing the failure type this task cares
about most.

## The test set

`TEST_CASES` has 8 clause/summary pairs. 5 of the 8
(`case_2`, `case_3`, `case_4`, `case_6`, `case_7`) genuinely omit a
legally significant detail. 3 of those 5 (`case_2`, `case_4`, `case_7`)
sit in the deceptive 0.70–0.85 similarity band — moderately high
scores that still hide a real omission.

## What to do

This is a **trace-then-extend** exercise like the core path — there's
nothing broken in the base harness to fix.

### Part 1 — Trace `case_2` by hand
`case_2` is arbitration, similarity 0.75, LLM-score 5, and genuinely
omits a detail. Work out which of `proper_routing_review()`'s three
conditions actually fire for it, then check whether
`naive_threshold_review(0.75)` would flag it.

### Part 2 — Run the full comparison
```bash
python3 starter.py
```
Confirm the printed false-negative rates: the naive threshold should
miss 60% of the 5 real omission cases (3 of 5: `case_2`, `case_4`,
`case_7`), while the proper routing logic should miss only 20% (1 of
5).

### Part 3 — Find the proper rule's own remaining gap
Look at `case_3`: notice_period (not high-risk), LLM-score 3 (not in
4–7), similarity 0.40 (not in 0.70–0.85). It's an "obviously bad" case
that the *naive* threshold actually catches (0.40 < 0.5), but the
*proper* rule's three conditions were purpose-built around the
deceptive middle band, not around catching every low score too — so it
slips through. Add a code comment explaining why a routing rule built
from exactly these three signals can still have a gap, and sketch
(in a comment, no need to implement) what a fourth signal might look
like to close it without reintroducing the naive rule's whole class of
misses.

## Checking your work

`solution.py` is the same fully-worked harness as `starter.py` — use
it to confirm your understanding of the base comparison logic, not to
find a "correct" answer to Part 3's open-ended design question.

---

*Session 5.2 Project (Pro Path) | GenAI for Everyone | Week 5*
