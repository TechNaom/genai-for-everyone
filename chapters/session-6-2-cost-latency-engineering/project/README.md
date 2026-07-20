# Session 6.2 Project: The Routing Strategy

The Pro path build for Session 6.2 — a routing exercise built directly on
Sub-topic 3 of the lesson ("Model Routing: Not Every Request Needs Your Best
Model"). Given a realistic mixed workload — some requests genuinely need your
best model, most don't — you design and implement a routing strategy, then
measure exactly how much it saves against the "everything goes to the
expensive model" baseline.

## What you'll build

`REQUEST_TYPES` models a support chatbot's traffic as four representative
request patterns, each with a share of total daily volume and an average
token profile:

| Type | Share of traffic | Avg input tokens | Avg output tokens |
|---|---|---|---|
| `simple_faq` | 55% | 150 | 60 |
| `order_status_lookup` | 20% | 300 | 100 |
| `billing_dispute` | 15% | 900 | 250 |
| `multistep_technical_troubleshooting` | 10% | 2,200 | 500 |

This is how real teams actually model production traffic — not one row per
request, but a handful of known patterns with known (or estimated) volume
shares. You'll implement:

- `requests_per_day_for_type` — a type's share of `TOTAL_REQUESTS_PER_DAY`
  (50,000)
- `daily_cost_for_type` — the dollar cost of serving all of a type's traffic
  on a given model tier
- `baseline_cost` — the "everything to the expensive model" baseline
- `route_tier` — the routing rule itself: below a token threshold, route to
  `"cheap"`; at or above it, stay on `"expensive"`
- `routed_cost` — total daily cost when every type is routed by that rule
- `print_comparison` — a report showing which types got routed where,
  baseline vs. routed daily/monthly cost, and the dollar and percent savings

## Example run (after completing all six)

```
=== ROUTING STRATEGY: threshold = 500 input tokens ===
Routing threshold: requests under 500 avg input tokens go to 'cheap'; everything else stays on 'expensive'.

Request type                             Share   Avg in   Routed to
simple_faq                                 55%      150       cheap
order_status_lookup                        20%      300       cheap
billing_dispute                            15%      900   expensive
multistep_technical_troubleshooting        10%     2200   expensive

                               Daily       Monthly (x30)
Baseline (all expensive)         $900.00          $27,000.00
Routed                       $610.68          $18,320.25

Monthly savings from routing: $8,679.75 (32.1% reduction)
```

## How to run it

```bash
python starter.py
```

No API key and no internet access needed — this is pure arithmetic on token
counts and traffic shares. Fill in the six functions, then re-run to see the
comparison printed. Want to see a finished version first? Run
`python solution.py`.

## The habit this trains

A threshold of 500 input tokens is a design *decision*, not a fact — it's the
line you're drawing between "simple enough for the cheap model" and "needs
the expensive model." Notice in the example run that 75% of traffic
(`simple_faq` + `order_status_lookup`) routes to the cheap tier while only
25% (the two harder types) stays on the expensive one, and that 25% of
traffic still accounts for the majority of the remaining cost — because
those requests also have the longest outputs. That's the real shape of a
production routing decision: most traffic is simple, but the hard slice is
disproportionately expensive, so routing the easy majority away is what
actually moves the bill.

## Ideas to make it your own (optional stretch goals)

- Add a fifth `REQUEST_TYPES` entry from a workload you've actually seen (at
  work, in a side project, or a hypothetical you find realistic) and see how
  it shifts the optimal threshold.
- Try several thresholds (`solution.py` already compares 500 vs. 350 tokens)
  and plot — even just by eye, from the printed numbers — the point of
  diminishing returns where a lower threshold barely improves savings but
  risks sending genuinely complex requests to the cheap model.
- Replace the single-number `avg_input_tokens` threshold with a two-signal
  rule (e.g., token count *and* a `requires_account_lookup` flag) and discuss
  why a length-only threshold is a reasonable first pass but an imperfect
  proxy for "actually simple."

## Why this project matters

Model routing is usually the single biggest cost lever in a production GenAI
system precisely because real traffic is skewed: most requests are simple,
and a cheap model handles them exactly as well as an expensive one would.
The engineering skill isn't just knowing routing exists — it's being able to
put a real number on it: given your actual traffic mix, exactly how much
does a specific threshold save, and is the trade-off (a small share of
borderline requests possibly under-served by the cheap model) worth the
dollars it saves? That's the calculation this project makes you actually run
instead of estimate.
