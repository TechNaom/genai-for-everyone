# Exercise — Session 7.4: Case Study Day II + Capstone Build Day II

## Overview

Complete a second case study worksheet, then run a peer-review checklist
against your capstone v1.

- **Core path:** Fill in the Session 7.4 case study worksheet
  (`case_study_worksheet.md`).
- **Pro path:** Implement `peer_review()` in `starter.py` and run it against
  your own capstone (self-review) or a peer's, then write up your findings.

## Setup

No dependencies beyond the Python standard library — no API key needed for
either path.

## Free/open path

Pure analysis and writing — no API calls, no cost. Both the worksheet and
the peer-review checker run entirely offline.

## Optional paid-API path

Not applicable — this exercise doesn't call an LLM.

## Starter code

See `starter.py`. It scaffolds `peer_review()`, which takes a project name
and a dict mapping each `CHECKLIST_ITEMS` entry to `True`/`False`, and
should return a formatted report showing which items pass, which need
attention, and an overall readiness percentage.

## How to work through it

1. **Core path:** Open `case_study_worksheet.md` and fill in all four
   questions in your own words, based on the Contract Review Assistant case
   study from the lesson. Compare against `filled_worksheet_example.md`
   once you've made a genuine attempt — it's one reasonable answer, not the
   only correct one.
2. **Pro path:** Open `starter.py`, implement `peer_review()` so it prints a
   report line for each checklist item (✅ or ⚠️  NEEDS ATTENTION) and an
   overall readiness percentage. Fill in `example_answers` with your own
   honest, specific answers about your actual capstone v1 (or hand the
   checklist to a peer and fill it in with their answers), then run:
   ```bash
   python3 starter.py
   ```
3. Write up your peer-review findings: one thing that's working well, one
   specific risk you'd want addressed before this went further, and whether
   the success criteria from your Session 7.1 proposal are actually being
   measured yet.

### Expected output shape

```
=== PEER REVIEW: My Capstone v1 ===
✅ — Runs end to end without manual intervention
✅ — Uses at least 2 techniques from the program (per the Session 7.1 proposal)
⚠️  NEEDS ATTENTION — Success criteria from the proposal is actually being measured (not just 'it runs')
⚠️  NEEDS ATTENTION — At least one Week 5-style eval pass has been run
✅ — Out-of-scope items from the proposal have been respected (no scope creep)

Readiness: 3/5 (60%)
Recommendation: address the flagged items before demo day, prioritizing the
eval pass and success-criteria measurement — these are what let you
actually claim the capstone 'works.'
```

### Key learning

- Applying a case study's lesson concretely to your own project's design,
  not just summarizing the case study.
- Reading your own (or a peer's) system critically, the same skill from
  Session 7.2, now applied to something with real stakes.
- Checking success criteria against reality instead of just shipping more
  features.

## Solution

See `solution.py` (don't peek before attempting!). It's a full reference
implementation of `peer_review()`. See also `filled_worksheet_example.md`
for a reference worksheet.

## Checking your work

There's no automated grader — the same way there's no automated grader for
a real peer review. Confirm instead: your worksheet answers are specific to
the actual case study (not generic restatements), your `peer_review()`
output correctly separates passing items from ones needing attention and
computes the right percentage, and your written findings name one concrete
risk rather than a vague reassurance that everything looks fine.

---

*Session 7.4 | GenAI for Everyone | Week 7: Capstone, Career Prep*
