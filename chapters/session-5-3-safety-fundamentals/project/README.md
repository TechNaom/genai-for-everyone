# Session 5.3 Project: Build the Permission-Aware Retrieval Pipeline

## Overview

Build the secured version of the wiki search assistant from the exercises
&mdash; implementing all three defenses from the lesson and confirming
that all 4 red-team attack vectors are blocked.

**File:** `starter.py` (identical to `solution.py` &mdash; see note below)

## What this code does

1. `scan_for_injection_at_index_time()` &mdash; catches poisoned documents
   (hidden "SYSTEM NOTE" instructions) before they're ever indexed at all,
   the Part 4 defense.
2. `flag_sensitive_content()` &mdash; checks a document's title for
   sensitivity signals ("confidential," "do not distribute," "layoffs,"
   "restructur-," "under investigation") independent of the document's
   formal access-control space, the Part 3 defense.
3. `build_clean_index()` &mdash; builds an index-time-scanned index,
   excluding poisoned documents entirely.
4. `secured_retrieve()` &mdash; the Part 2 defense: filters candidates by
   the requesting user's permission *before* anything reaches the prompt
   context, then routes sensitive-but-permitted documents to a flagged/
   review path instead of silently including them.
5. `run_secured_red_team_suite()` &mdash; re-runs the same 4 red-team
   queries from the exercises against the secured pipeline and reports how
   many are now blocked.

### Run it
```bash
python3 starter.py
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
normally (`comp_1` is included) &mdash; the fix blocks inappropriate
access, not all access.

### A note on this file

As with the exercises, `starter.py` and `solution.py` here are
**identical** &mdash; every TODO is already filled in. Treat this as a
**trace-and-extend** exercise rather than a fill-in-the-blank one:

1. Trace each of the three defense functions against the mock
   `WIKI_INDEX` and confirm you can explain, for every one of the 5
   documents, whether it gets excluded at index time, included normally,
   or flagged for review &mdash; and why.
2. Then extend it. Two concrete directions:
   - Add a document that's sensitive-by-title (matches
     `flag_sensitive_content`) **and** genuinely poisoned (matches
     `scan_for_injection_at_index_time`), and confirm the pipeline handles
     the overlap sensibly (it should be excluded at index time before
     sensitivity flagging is ever reached for it).
   - Add a 5th red-team case that specifically targets the flagged/review
     path &mdash; a query where the correct behavior is neither a clean
     answer nor a hard block, but a response noting content was withheld
     pending review &mdash; and confirm `secured_answer()` produces that.

### Key learning
Permission filtering has to happen before content reaches the model's
context, not just at the final answer. And index-time scanning for
poisoned content is strictly better than query-time defense, because it
protects every future user, not just the one who happens to trigger a
check.

---

*Session 5.3 | GenAI for Everyone | Week 5*
