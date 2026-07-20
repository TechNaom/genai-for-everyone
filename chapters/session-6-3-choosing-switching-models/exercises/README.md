# Exercises — Session 6.3: The Model Adapter

## Overview

Build a thin adapter layer over two mocked model providers, then run the same
task across both and compare cost, latency, and quality — the exact habit
that makes switching providers (or adding a fallback) cheap later instead of
a codebase-wide rewrite.

- **Task 1:** Implement `call_model(prompt, provider=...)` so it looks up a
  provider function and raises a clear `ValueError` for an unknown provider.
- **Task 2:** Run the same prompt across both mocked providers and watch
  `provider_a`'s simulated outage trigger on roughly 3 out of every 10 runs.
- **Task 3:** Implement `build_comparison_table()` so it prints cost,
  latency, and a subjective quality note for both providers side by side.
- **Task 4 (Debug):** Fix a buggy provider lookup that silently returns
  `None` for an unknown provider instead of failing loudly.

## How to run it

```bash
python starter.py
```

No API key, no internet access, and no external libraries needed — this is a
fully offline exercise. The "outage" is simulated in-process with `random`,
so it runs the same way every time regardless of network conditions.

## Free/open path

Everything here is mocked and deterministic-enough to grade for free: no
signup, no paid tier, no internet access required.

## Optional paid-API path

Once you're comfortable with the adapter shape, try swapping
`_call_provider_a` / `_call_provider_b` for real calls to two different
providers (for example, Anthropic and OpenAI, or two different model tiers
from the same provider) using their free trial credits, so your cost and
latency numbers reflect real API responses instead of mocked ones.

## Checking your work

There's no automated grader — that's intentional. Run `python starter.py` a
handful of times: because `provider_a`'s outage is randomized, you should see
it succeed most runs and fail roughly 3 times out of 10. Compare your
comparison table's numbers and your quality notes against `solution.py` (run
it with `python solution.py`) once you've made a genuine attempt.

## Solution

See `solution.py` in this folder (don't peek before attempting!).
