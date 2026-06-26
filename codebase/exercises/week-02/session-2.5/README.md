# Exercise — Session 2.5: Prompt Systems, Not Just Prompts

## Reusable Prompt Template Library

**Goal:** Build a small library of prompt templates with named variables, clear documentation, and lightweight tests — not exact-match tests, but checks for specific characteristics the output should have.

### Instructions

1. Open `prompt_library.py`
2. Fill in the TODOs: complete the 5 templates (3 are started for you, 2 are blank for you to design), each with a docstring listing expected variables
3. Write at least one lightweight test check per template in `TEST_CASES` — e.g., "output should contain the customer's name," "output should be under N words," "output should NOT mention competitor names"
4. Run it: `python prompt_library.py` (no API key needed — this exercise tests the templates' structure and your test-writing, not live model output)

### What "done well" looks like

Your tests shouldn't require an exact string match (that's unrealistic for LLM output) — they should check for specific, verifiable characteristics that a GOOD output must have, regardless of exact wording.

## Free/open path

No API calls needed for this exercise — it's about template structure and test design, which you can verify entirely offline. If you want to see live output, you're welcome to actually call a model with your finished templates afterward (optional, any provider's free tier).

## Optional paid-API path

Same as above — calling a model with your templates is an optional bonus, not required for the core exercise.

## Solution

See `codebase/solutions/week-02/session-2.5/` for a complete worked library with 5 templates and test checks.
