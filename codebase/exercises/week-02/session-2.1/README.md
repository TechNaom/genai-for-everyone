# Exercise — Session 2.1: Anatomy of a Great Prompt

## Prompt Rewrite Exercise (Bad → Great)

**Goal:** Build the habit of diagnosing exactly which pillar (clarity, context, constraints, format) is missing from a weak prompt, then fixing it deliberately — not just making the prompt "sound nicer."

### Instructions

1. Open `prompt_rewrite.py`
2. For each of the 5 weak prompts in `WEAK_PROMPTS`, fill in:
   - `missing_pillars`: which of the four pillars are missing (a list, can be more than one)
   - `rewritten_prompt`: your improved version
   - `why_better`: one sentence on what changed and why it matters
3. Run the script to see your rewrites laid out, then compare against the solution

### What "good" looks like

Your rewrite should be checkable against the test from this session's chapter: could a competent person, given ONLY your rewritten prompt, produce something close to what's actually needed, without guessing at anything important?

## Free/open path

No API calls needed — this is a prompt-design and reasoning exercise. You're welcome to test your rewritten prompts against a real model afterward (free tier of any provider) to see how the output changes, but it's optional for completing the exercise.

## Optional paid-API path

If you want to go further: run both the original weak prompt and your rewritten version through the same model, and compare the actual outputs side by side. This makes Part 1's "expectation gap" concept concrete.

## Solution

See `codebase/solutions/week-02/session-2.1/` for worked rewrites with reasoning.
