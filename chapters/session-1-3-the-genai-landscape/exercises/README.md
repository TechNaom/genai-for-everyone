# Session 1.3 Exercises: The GenAI Landscape

## Comparison Matrix

**Goal:** Build hands-on judgment for comparing models across the
dimensions that actually matter (capability, speed, cost) — not just
"which one feels smarter."

You don't need any API keys. Use whichever free chat interfaces you already
have access to (comparing free tiers of different providers' chat apps) and
time your own observations with a stopwatch or your phone's timer. The goal
is the comparison *process*, not lab-grade measurement.

## How to run

```bash
python starter.py
```

## Task 1 — Pick and record one identical task

Find `# TODO 1`. Choose ONE realistic test task (a few are suggested in the
script — e.g. summarizing a paragraph, or answering a multi-step reasoning
question) and write the exact task text into `TASK_USED`. You must run the
*same* task across every model so the comparison is fair.

## Task 2 — Fill in the comparison table

Find `# TODO 2`. Run your chosen task across at least 2 different models you
have access to. For each, fill in one dictionary in `RESULTS`: rough
response time, your subjective quality rating (1-5), and published
cost-per-million-tokens if you can find it (leave `None` if you can't —
never guess a number).

## Task 3 — Write a recommendation

Find `# TODO 3`. After running the script to print your formatted table,
write 2-3 sentences: which model would you pick for a real-time
customer-facing chat widget, and which for an overnight batch summarization
job — and why? Name the dimension that drove each choice.

## Task 4 — Debug the Code

This helper is supposed to report the *cheaper* model by output cost, but
it always reports the FIRST model regardless of price. Find and fix the bug.

```python
RESULTS = [
    {"model_name": "Frontier tier", "cost_per_million_output": 15.00},
    {"model_name": "Fast tier",     "cost_per_million_output": 1.25},
]

cheapest = RESULTS[0]
for r in RESULTS:
    if r["cost_per_million_output"] > cheapest["cost_per_million_output"]:
        cheapest = r

print("Cheapest by output cost:", cheapest["model_name"])
```

The comparison uses `>` where it should use `<` — it keeps whichever model
is *most* expensive instead of least. Flip the comparison to `<`.

## Optional paid-API path

If you have API access to more than one provider, you can call them
programmatically and measure response time precisely in code — there's a
commented-out example function in `starter.py` showing the pattern (install
that provider's SDK and add your own API key to an environment variable —
never hardcode a key directly in the script).

## Checking your work

See `solution.py` for a worked example with realistic illustrative numbers
(yours will differ — that's expected, since real performance changes over
time). Run it with `python solution.py`.
