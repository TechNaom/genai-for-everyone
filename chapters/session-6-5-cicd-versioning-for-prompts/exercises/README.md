# Session 6.5 Exercise: The CI Regression Gate

**Goal:** Build a CI-style check function for prompt changes — the same
shape as a real CI job's exit code, applied to prompt quality instead of
passing tests.

This exercise needs no API calls and no paid keys. It's a pure
scoring-and-comparison exercise: plain Python, runs anywhere.

## How to run

You'll need Python 3 installed. Check with:

```bash
python --version
```

Then run the starter file:

```bash
python starter.py
```

It will raise `NotImplementedError` until you fill in `check_regression`.

## The task

Open `starter.py`. There's one function to complete: `check_regression(new_version,
baseline_version, threshold_drop=0.05)`. Given a new prompt version and a
baseline version, it should:

1. Score both versions with the provided `mock_score_prompt` (a stand-in for
   "run this prompt against the golden dataset and grade the responses" —
   exactly Session 5.1's regression suite, just wired to run automatically).
2. Compute the drop: `baseline_score - new_score`.
3. Decide `passed`: `False` if the drop exceeds `threshold_drop`, `True`
   otherwise.
4. Build a clear, one-line `message` — something you'd want to actually read
   in a CI log, including both scores, the drop, and the threshold.
5. Return a dict: `{"new_score": ..., "baseline_score": ..., "passed": ...,
   "message": ...}`.

The tell for the whole exercise: **compare against the last known-good
baseline, not a fixed absolute number** — a fixed threshold alone can't tell
you whether a new version is worse than what it's replacing, only whether it
cleared some bar in isolation.

## Checking your work

The starter's `__main__` block includes two `assert` statements: one prompt
version (`v2_friendlier_tone`) is a known regression and should fail the
gate; another (`v3_friendlier_fixed`) fixed that regression and should pass.
If both asserts run without an `AssertionError`, your gate is behaving
correctly. Compare your implementation against `solution.py` (run it with
`python solution.py`) once you've made a genuine attempt.

## Want to go further?

The Pro path project extends this single check into a small version-history
system — storing every version's score with a timestamp, supporting
rollback, and producing a changelog report that shows score trends across
versions. See [`../project/`](../project/).
