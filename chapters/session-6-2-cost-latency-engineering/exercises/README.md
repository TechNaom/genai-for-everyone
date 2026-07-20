# Session 6.2 Exercise: The Cost Calculator

**Goal:** Build a reusable tool that turns "requests per day, average tokens
in and out" into a real dollar figure across model tiers, then use it to
quantify one concrete optimization instead of eyeballing it.

This exercise needs no API calls and no paid keys. It's pure arithmetic on
token counts and illustrative price-per-million-token rates: plain Python,
runs anywhere.

## How to run

You'll need Python 3 installed. Check with:

```bash
python --version
```

Then run the starter file:

```bash
python starter.py
```

Once complete, it prints a baseline cost report across three model tiers
(small, medium, large), then a second report for the same workload with a
trimmed input prompt, plus the exact monthly dollar savings that trim
produces.

## The task

Open `starter.py`. `MODEL_PRICING` defines three illustrative model tiers,
each priced per million tokens with input and output priced separately
(matching Sub-topic 1 of the lesson — output is priced higher than input).
Fill in:

- `cost_per_request(model, input_tokens, output_tokens)` — dollar cost of one
  request on a given tier
- `daily_cost(model, requests_per_day, avg_input_tokens, avg_output_tokens)` —
  total cost for a day's workload
- `compare_models(...)` — daily cost across every tier at once
- `print_report(...)` — a readable report: daily cost and monthly cost
  (daily × 30) per tier
- the `__main__` block's optimization comparison — a second report with
  `avg_input_tokens` trimmed from 1500 to 600, plus the exact monthly savings
  on the `"medium"` tier

Run the script again after each edit to see your report take shape.

## Checking your work

This one has a clean right answer — it's arithmetic, not judgment. Run
`python solution.py` and compare the printed numbers exactly. The baseline
medium-tier daily cost should be **$450.00** (50,000 requests × ((1500 /
1,000,000 × $3.00) + (300 / 1,000,000 × $15.00))). If yours doesn't match,
work backward through `cost_per_request` first — that's almost always where
the bug lives.
