# Session 1.3 Project: The Model Selector

In the exercise you compared models by hand on one task. This project turns
that judgment into a small, reusable **decision tool**: feed it a short
application brief and it recommends which *kind* of model to reach for — and
explains why. It's the lesson's decision framework, written as code.

## What you'll build

A script that holds a tiny catalog of generic model *tiers* (a fast closed
tier, a frontier closed tier, and a self-hosted open-weight tier) and a set of
application briefs. For each brief it filters on hard constraints first, then
ranks the survivors on the one dimension that actually drives the choice.

Example run:

```
=== Model Selector Report ===

App: Live customer-facing chat widget
  Priority dimension: speed
  Recommendation: Fast tier (closed) [closed/proprietary]
    speed score: 5/5

App: Overnight legal-contract summarizer (batch)
  Priority dimension: capability
  Recommendation: Frontier tier (closed) [closed/proprietary]
    capability score: 5/5

App: Clinical documentation assistant (patient data)
  Priority dimension: capability  (+ compliance required)
  Recommendation: Self-hosted open-weight [open-weight]
    capability score: 4/5
```

Notice the third app: the frontier tier is the strongest reasoner, but the
compliance constraint eliminates the closed tiers *before* capability is even
compared — so the strongest **eligible** model wins instead.

## How to run it

```bash
python starter.py
```

Fill in the `# TODO` sections in `starter.py`. Want to see one finished
version first? Run `python solution.py`.

## Ideas to make it your own (optional stretch goals)

- Add a fourth brief whose priority is `value` (cheapest per token) and see
  which tier wins.
- Add a `min_context_k` field to a brief and filter out any tier whose
  `context_k` is too small — a second hard constraint alongside compliance.
- Print a one-line justification per recommendation that names the runner-up
  and why it lost.

## Why this project matters

This is the actual skill the session teaches, made mechanical: **filter on the
hard constraints that can eliminate options entirely (compliance, residency),
then rank whatever survives on the dimension the task really needs.** Real
teams run exactly this reasoning when they pick a different model for
autocomplete than for their hardest reasoning feature — no "house model," just
per-task fit.
