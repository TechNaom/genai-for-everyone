# Exercise — Session 7.3: Capstone Build Day I

## Overview

Use a checkpoint tracker to log progress on your actual capstone build,
practicing the MVP-first/checkpoint discipline from the lesson.

- **Core path:** Log start/finish times for Checkpoints 1-3 and get a status report
- **Pro path:** Require a justification note for each checkpoint before it can be marked complete

## Setup

No API key and no extra dependencies — everything in `starter.py` runs with
the Python standard library.

## Free/open path

This is a plain time/progress tracker — no API calls, no cost. Use it
alongside whatever capstone project you're actually building.

## Optional paid-API path

Not applicable.

## Starter code

See `starter.py` in this folder.

## How to work through it

1. Open `starter.py` and read `BuildDayTracker` — it tracks elapsed time
   against a total build-day budget and logs each checkpoint you complete.
2. **Core path — TODO 1:** implement `complete_checkpoint()` so it appends a
   dict with the checkpoint name, the current `elapsed_percent()`, and the
   optional justification to `self.log`.
3. **Core path — TODO 2:** implement `status_report()` so it returns a
   formatted string listing each logged checkpoint and the elapsed percent
   at which it was completed, flagging Checkpoint 1 specifically if it was
   completed after 25% elapsed — the "you should have simplified" signal
   from the lesson.
4. **Pro path:** don't just accept an optional justification — require one
   before a checkpoint can be marked complete (raise if it's missing or
   empty), and write a real one-sentence justification for each checkpoint
   as you actually build your capstone, practicing the scope-discipline
   judgment call from the lesson's Pro path challenge.
5. Run it: `python3 starter.py`

### Expected output shape

```
=== BUILD DAY STATUS ===
Checkpoint 1: thinnest end-to-end pipeline — completed at 12.0% elapsed
    justification: Hard-coded 3 docs, crude prompt, prints an answer.
Checkpoint 2: core path works on golden dataset — completed at 48.0% elapsed
    justification: All 6 golden-dataset questions run through the pipeline.
```

If Checkpoint 1 is logged after 25% elapsed, an extra warning line appears
underneath it — that's the tracker doing its job, not a bug.

### Key learning

- Turning the MVP-first, checkpoint-driven discipline from the lesson into
  something you actually run and consult during your own build, rather than
  a rule you only nod along to
- Practicing the "why move on now" judgment call as an explicit, written
  justification instead of an unexamined habit

## Solution

See `solution.py` in this folder (don't peek before attempting!). It's a
full reference implementation of both TODOs, run against a short simulated
build.

## Checking your work

There's no automated grader — that's intentional, the same way a real build
day doesn't come with one either. Confirm instead: `complete_checkpoint()`
records the elapsed percent at the moment it's called (not at the moment the
report is printed), and `status_report()` correctly flags Checkpoint 1 if
its logged `elapsed_percent` is over 25. Compare against `solution.py` once
you've made a genuine attempt.

## Extending it (optional)

Once the core path works, try the pro path: require a non-empty
justification for every checkpoint, and — while you build your actual
capstone alongside this tracker — write one honest sentence per checkpoint
explaining why you're moving on now rather than polishing further.

---

*Session 7.3 | GenAI for Everyone | Week 7: Capstone, Career Prep*
