# Session 2.1 Exercise: Prompt Rewrite Exercise (Bad → Great)

**Goal:** Build the habit of diagnosing exactly which pillar (clarity, context,
constraints, format) is missing from a weak prompt, then fixing it
deliberately — not just making the prompt "sound nicer."

This exercise needs no API calls and no paid keys. It's a pure prompt-design
and reasoning exercise: plain Python, runs anywhere.

## How to run

You'll need Python 3 installed. Check with:

```bash
python --version
```

Then run the starter file:

```bash
python starter.py
```

It prints each weak prompt and flags any entry you haven't filled in yet.

## The task

Open `starter.py`. For each of the 5 weak prompts in `WEAK_PROMPTS`, fill in:

- `missing_pillars` — a list containing any of `"clarity"`, `"context"`,
  `"constraints"`, `"format"`
- `rewritten_prompt` — your improved version
- `why_better` — one sentence on what changed and why it matters

Run the script again after each edit to see your rewrites laid out.

## What "good" looks like

Your rewrite should be checkable against the test from this session's lesson:
could a competent person, given ONLY your rewritten prompt, produce something
close to what's actually needed, without guessing at anything important?

## Checking your work

There's no automated grader — that's intentional. Several of these prompts
could reasonably be missing a slightly different combination of pillars
depending on how you read them. The goal isn't perfect agreement with
`solution.py`; it's being able to **defend your diagnosis and your rewrite**.

Compare your reasoning against `solution.py` (run it with
`python solution.py`) once you've made a genuine attempt.

## Free/open path

No API calls needed — this is a prompt-design and reasoning exercise. You're
welcome to test your rewritten prompts against a real model afterward (free
tier of any provider) to see how the output changes, but it's optional for
completing the exercise.

## Optional paid-API path

If you want to go further: run both the original weak prompt and your
rewritten version through the same model, and compare the actual outputs side
by side. This makes the lesson's "expectation gap" concept concrete.
