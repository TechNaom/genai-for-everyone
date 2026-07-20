# Exercise — Session 7.1: Capstone Kickoff

## Overview

Write a one-page capstone proposal, and run a scope-checker script against
it that flags common vagueness problems before you show it to anyone else.

- **Core path:** Fill in `proposal_template.md`, then get it passing the
  checks in `starter.py`
- **Pro path:** Write two competing proposals (narrow vs. ambitious) for the
  same problem and justify your pick in writing

## Setup

No dependencies beyond the Python standard library — nothing to `pip
install`.

## Free/open path

This exercise is pure writing plus a small Python checklist script — no API
calls, no cost.

## Optional paid-API path

Not applicable — this session is about scoping, not building.

## Starter code

See `starter.py` in this folder.

1. Copy `proposal_template.md` and fill it in for your own capstone idea.
2. Run `python3 starter.py your_proposal.md` to check it against common
   vagueness red flags (missing sections, filler phrases like
   "everything"/"anything", a success criteria section with no measurable
   number in it, etc.)

## How to work through it

1. **`check_required_sections()`**: return the subset of `REQUIRED_SECTIONS`
   that's missing from the proposal text.
2. **`check_vague_phrases()`**: return the subset of `VAGUE_PHRASES` (case-
   insensitive) that shows up anywhere in the proposal text.
3. **`check_success_criteria_has_number()`**: pull out just the "Success
   criteria" section's content and check whether it contains at least one
   digit — a simple proxy for "this is actually measurable," not just a
   feeling.
4. Run it against your own filled-in proposal: `python3 starter.py
   your_proposal.md`

### Expected output shape

```
Checking your_proposal.md...

✅ All required sections present
✅ No vague phrases detected
✅ Success criteria includes a measurable number
```

If any check fails, the output names exactly what's missing or vague so you
can tighten the proposal before moving on.

## Pro path — extended challenge

Write two competing one-pagers for the same underlying problem: one
narrow-and-finishable, one ambitious-and-risky. Then write a short, explicit
case for which you'd actually choose to build, given the 2-3 sessions
remaining — using the same scope-vs-time-vs-risk reasoning a real team would
use in a project kickoff meeting. Both proposals should still pass the
scope-checker cleanly; the point of the pro path is the written trade-off
reasoning, not looser scoping discipline.

## Solution

See `solution.py` (a full reference implementation of the checker) and
`example_proposal.md` (a filled-in reference proposal that passes all three
checks cleanly) in this folder — don't peek before attempting your own!

## Checking your work

There's no automated grader beyond the checker script itself. Confirm: your
proposal passes all three checks (`starter.py`, once implemented, run
against your own filled-in file), and — the check the script *can't*
automate — that a stranger reading your one-pager in two minutes could
actually picture the end-to-end system and tell what's explicitly out of
scope.

---

*Session 7.1 | GenAI for Everyone | Week 7: Capstone, Career Prep*
