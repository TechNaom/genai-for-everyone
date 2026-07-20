# Session 6.5 Project: Prompt Version History & Rollback

The Pro path build for Session 6.5 — extend the single pass/fail regression
gate from the exercise into a small version-history system that stores every
version's score over time, supports rolling back to the previous version, and
produces a changelog report that answers the question that actually matters
during an incident: *when did this start getting worse, and what changed?*

## What you'll build

A `PromptVersionHistory` class that tracks a sequence of `PromptVersion`
entries (name, score, timestamp, and an optional note describing what
changed). Four methods to implement:

- `add_version(name, score, timestamp, note="")` — append a new version and
  move the "current" pointer to it, the way a new deploy becomes the live
  version.
- `rollback()` — move the "current" pointer back one version and return it,
  raising `IndexError` if there's nothing earlier to roll back to.
- `first_regression()` — scan the history in order and return the first
  version whose score dropped by more than `regression_threshold` compared
  to the version right before it — the version that actually introduced the
  problem.
- `changelog()` — render the full history as a readable report: each
  version's score, timestamp, and change vs. the previous version, with the
  regressing version and the current version both clearly flagged.

Example run (after completing all four):

```
=== PROMPT VERSION CHANGELOG ===
v1_baseline             92%  2026-01-05  -- Initial support bot prompt
v2_friendlier_tone      78%  2026-01-12  (-14%)  <-- regression started here  -- Reworded for a friendlier tone
v3_friendlier_fixed     90%  2026-01-14  (+12%)  -- Kept tone, restored refund-policy precision
v4_shorter_answers      91%  2026-01-20  (+1%)  (current)  -- Trimmed answers to cut cost

First regression detected at: v2_friendlier_tone (2026-01-12) -- Reworded for a friendlier tone

Current version: v4_shorter_answers
A production issue just came in -- rolling back...
Now on: v3_friendlier_fixed (90%)
```

## How to run it

```bash
python starter.py
```

No API key and no internet access needed — this is a pure data/scoring-logic
exercise, fully offline, built on top of the exercise's `check_regression`
gate. Fill in the four `NotImplementedError` methods, then re-run to see the
changelog printed. Want to see one finished version first? Run
`python solution.py`.

## The habit this trains

Notice that `first_regression` isn't just "the lowest-scoring version" — it's
the first version where the score *dropped* relative to what came right
before it. A later version could have an even lower score without being the
regression's origin, or a version could recover and dip again later.
Reporting *when* the drop first happened, not just *which* version currently
scores lowest, is exactly the diagnostic question a real incident review
asks: not "what's bad right now" but "what changed, and when."

## Ideas to make it your own (optional stretch goals)

- Add a `rollback_to(name)` method that jumps directly to a named version
  instead of only stepping back one at a time — useful when you already know
  exactly which version was last good.
- Extend `changelog()` to also print the number of versions shipped since the
  last regression, as a rough "time since last incident" counter.
- Swap the mocked scores for a real call into the Session 6.5 exercise's
  `check_regression` gate, so every `add_version` call runs an actual
  regression check against the previous version automatically.

## Why this project matters

A single pass/fail check answers "is this one change safe to merge?" —
useful, but narrow. A version history answers the questions that actually
come up during an incident review: which version introduced the problem, how
long has it been live, what changed in the versions since, and what's the
fastest safe version to roll back to right now. Real prompt-ops systems (and
real code deploy systems) keep exactly this kind of history for exactly this
reason — not for the day everything goes right, but for the ten minutes when
something has gone wrong and someone is asking "when did this start?"
