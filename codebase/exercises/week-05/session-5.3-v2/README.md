# Session 5.3 (v2) Exercises: Safety Fundamentals for an Internal RAG Tool

## Overview

- **Core Path:** Red-team a permission-blind wiki search assistant across
  4 RAG-specific attack vectors
- **Pro Path:** Build the permission-aware retrieval pipeline and verify
  all 4 vectors are blocked

---

## Core Path: Red-Team the Vulnerable Assistant

**File:** `core_path_starter.py`

### What you'll do
1. `check_for_leakage()` (TODO 1) — detect permission leaks, sensitivity
   leaks, and fired injections in a response
2. `run_red_team_suite()` (TODO 2) — run 4 attack-vector queries and
   report which succeed

### Run it
```bash
python3 core_path_starter.py
```

### Expected result
All 4 attack vectors succeed against the vulnerable pipeline — including
one case where a single query triggers *multiple* distinct failure types
at once (a realistic compounding effect, not a bug in the exercise).

### Key learning
None of these "attacks" required malicious intent or clever prompting.
An ordinary question, asked by an ordinary employee, was enough — because
the retrieval step never checked who was asking or what it was about to
hand to the model.

---

## Pro Path: Build the Secured Pipeline

**File:** `pro_path_starter.py`

### What you'll do
1. `scan_for_injection_at_index_time()` (TODO 1) — catch poisoned docs
   before they're indexed at all
2. `flag_sensitive_content()` (TODO 2) — check title-based sensitivity
   independent of access control
3. `secured_retrieve()` (TODO 3) — filter by permission BEFORE content
   reaches the prompt context, and route sensitive-but-permitted docs
   to a flagged/review path instead of silent inclusion

### Run it
```bash
python3 pro_path_starter.py
```

### Expected result
```
Indexed 4/5 documents (excluded poisoned docs at index time)
...
✅ BLOCKED | Permission-blind retrieval
✅ BLOCKED | Confidential-by-convention bypass
✅ BLOCKED | Indirect injection via indexed content
✅ BLOCKED | Context accumulation (simplified single-turn version)

Result: 4/4 attack vectors blocked
```

Note that the HR employee's legitimate salary query still succeeds
normally (`comp_1` is included) — the fix blocks inappropriate access,
not all access.

### Key learning
Permission filtering has to happen before content reaches the model's
context, not just at the final answer. And index-time scanning for
poisoned content is strictly better than query-time defense, because
it protects every future user, not just the one who happens to trigger
a check.

---

*Session 5.3 (v2) | GenAI for Everyone | Week 5*
