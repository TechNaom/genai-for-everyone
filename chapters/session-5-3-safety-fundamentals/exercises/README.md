# Session 5.3 Exercises: Red-Team the Vulnerable Wiki Assistant

## Overview

Red-team a permission-blind wiki search assistant across the 4 RAG-specific
attack vectors from the lesson: permission-blind retrieval, confidential-by-
title bypass, indirect prompt injection via indexed content, and context
accumulation.

**File:** `starter.py` (identical to `solution.py` &mdash; see note below)

## What this code does

1. `vulnerable_retrieve()` / `vulnerable_answer()` &mdash; a deliberately
   unsafe wiki assistant. Retrieval matches purely on keyword/semantic
   overlap, with no permission check and no separation between retrieved
   content and instructions.
2. `check_for_leakage()` &mdash; inspects a result for three failure types:
   a permission leak (a retrieved doc from a space this user can't access),
   a sensitivity leak (a retrieved doc with a sensitive title pattern,
   regardless of whether the space technically permits it), and a fired
   injection (evidence the embedded "SYSTEM NOTE" caused the response to
   surface compensation data the query never asked about).
3. `run_red_team_suite()` &mdash; runs one query per attack vector and
   reports which vulnerabilities each one triggers.

### Run it
```bash
python3 starter.py
```

### Expected result
All 4 attack vectors succeed against the vulnerable pipeline &mdash;
including one case (the `hr_employee` query) where a single query triggers
*multiple* distinct failure types at once, a realistic compounding effect
rather than a bug in the exercise.

### A note on this file

Unlike some exercises in this course, `starter.py` and `solution.py` here
are **identical** &mdash; both TODOs are already filled in. There's nothing
missing to fill in blank-by-blank. Instead, treat this as a **trace-and-extend**
exercise:

1. Read `check_for_leakage()` line by line and confirm you can explain, for
   each of the 4 red-team cases in `run_red_team_suite()`, exactly *why*
   `permission_leak`, `sensitivity_leak`, or `injection_fired` comes back
   `True`.
2. Then extend it: add a 5th red-team case of your own (a different
   cross-department query, a differently-worded targeted-summarization
   request, or a second poisoned-document scenario) and confirm your new
   case also gets correctly flagged as a leak by the existing
   `check_for_leakage()` logic. If it doesn't, that's a real gap in the
   leakage checker worth noting &mdash; not every possible leak shape is
   covered by three simple checks.

### Key learning
None of these "attacks" required malicious intent or clever prompting. An
ordinary question, asked by an ordinary employee, was enough &mdash; because
the retrieval step never checked who was asking or what it was about to
hand to the model.

---

*Session 5.3 | GenAI for Everyone | Week 5*
