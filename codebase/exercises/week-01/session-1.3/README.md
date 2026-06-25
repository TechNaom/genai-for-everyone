# Exercise — Session 1.3: The GenAI Landscape

## Comparison Matrix

**Goal:** Build hands-on judgment for comparing models across the dimensions that actually matter (capability, speed, cost) — not just "which one feels smarter."

### Instructions

1. Open `model_comparison.py`
2. Pick ONE realistic test task (a few are suggested in the script — e.g., summarizing a paragraph, or answering a multi-step reasoning question)
3. Run the same task across at least 2 different models you have access to (this could be two different chat apps you already use, or two API models if you have keys)
4. Fill in the `RESULTS` table with your observations: rough response time, your subjective quality rating (1-5), and published cost-per-million-tokens if you can find it
5. Run the script to get a formatted comparison table and a generated recommendation paragraph

### What you'll notice

- Faster models aren't always lower quality, and slower models aren't always better
- Published pricing varies enormously between a provider's tiers
- The "best" model often depends entirely on which dimension you weight most

## Free/open path

You don't need any API keys for this exercise. Use whichever free chat interfaces you already have access to (e.g., comparing free tiers of different providers' chat apps) and time your own observations with a stopwatch or your phone's timer. The goal is the comparison *process*, not perfect lab-grade measurement.

## Optional paid-API path

If you have API access to more than one provider, you can call them programmatically and measure response time precisely in code — there's a commented-out example function in `model_comparison.py` showing the pattern (you'll need to install that provider's SDK and add your own API key to `.env` — never hardcode a key directly in the script).

## Solution

See `codebase/solutions/week-01/session-1.3/` for a worked example with realistic illustrative numbers (yours will differ — that's expected, since real performance changes over time).
