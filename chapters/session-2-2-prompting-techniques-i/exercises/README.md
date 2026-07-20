# Exercise — Session 2.2: Prompting Techniques I

## Few-Shot Classifier Prompt

**Goal:** Build a working few-shot prompt for a company-specific classification task, including a boundary case, and verify it actually generalizes to new inputs — not just the examples you wrote.

### Instructions

1. Install dependencies: `pip install anthropic python-dotenv`
2. Copy `.env.example` (repo root) to `.env` and add your `ANTHROPIC_API_KEY`
3. Open `starter.py` — the support-ticket few-shot prompt from this session's lesson is provided as a starting point
4. Fill in the TODO: add at least one more few-shot example of your own choosing, then test the classifier against the 5 held-out test tickets provided
5. Run it: `python starter.py`
6. Check: did every test ticket get classified into a sensible category, including the "Other" boundary case? If something misclassified, look at whether your examples actually covered that kind of input.

### What "done well" looks like

Your few-shot examples should generalize — getting all 5 test tickets right isn't about memorizing those exact 5 tickets, it's about whether your examples taught a pattern general enough to handle inputs you didn't specifically write for.

## Free/open path

Needs a real LLM API call to actually test generalization (that's the whole point of the exercise) — use any provider's free tier and swap the SDK call if you're not using Anthropic.

## Optional paid-API path

Works identically with any provider's SDK.

## Solution

See `solution.py` in this folder for a worked version with reasoning on why its added example was chosen.
