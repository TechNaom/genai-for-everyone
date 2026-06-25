# Exercise — Session 2.2: Prompting Techniques I

## Few-Shot Classifier Prompt

**Goal:** Build a working few-shot prompt for a company-specific classification task, including a boundary case, and verify it actually generalizes to new inputs — not just the examples you wrote.

### Instructions

1. Copy `.env.example` (repo root) to `.env` and add your API key
2. Open `classifier.py` — the support-ticket few-shot prompt from this session's chapter is provided as a starting point
3. Fill in the TODOs: add at least one more few-shot example of your own choosing, then test the classifier against the 5 new test tickets provided
4. Run it: `python classifier.py`
5. Check: did every test ticket get classified into a sensible category, including the "Other" boundary case? If something misclassified, look at whether your examples actually covered that kind of input.

### What "done well" looks like

Your few-shot examples should generalize — getting all 5 test tickets right isn't about memorizing those exact 5 tickets, it's about whether your examples taught a pattern general enough to handle inputs you didn't specifically write for.

## Free/open path

Needs a real LLM API call to actually test generalization (that's the whole point of the exercise) — use any provider's free tier.

## Optional paid-API path

Works identically with any provider's SDK.

## Solution

See `codebase/solutions/week-02/session-2.2/` for a worked version with reasoning on why each example was chosen.
