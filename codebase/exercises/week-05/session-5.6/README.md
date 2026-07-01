# Exercise — Session 5.6: Week 5 Lab — Mini Build Day

## Overview

Produce a four-section **eval + safety report** for a system you built in Week 3 (policy Q&A bot) or Week 4 (research agent) — or, if you didn't finish either, a simple chatbot with a single system prompt.

- **Core path:** Fill in all four sections of the report against a mocked target system (provided)
- **Pro path:** Same report, plus implement one real guardrail as working code and show a measurable before/after

## Setup

```bash
pip install -r requirements.txt
```

No API key is required — this exercise mocks the target system so grading is deterministic and free. If you'd rather point it at your real Session 3.6 or 4.6 project, replace `mock_target_system()` with a call to your actual system.

## Free/open path

Everything in `starter.py` runs with the standard library plus `requirements.txt` — no paid API calls needed.

## Optional paid-API path

If you want to test against your *real* Session 3.6/4.6 project (which likely calls the Anthropic or OpenAI API), swap `mock_target_system()` for your real function. The report structure doesn't change either way.

## Starter code

See `starter.py` in this folder. It scaffolds all four report sections:
1. Golden dataset + scoring (`GoldenDataset`, reuses the Session 5.1/5.2 pattern)
2. Red-team log (`RedTeamLog`)
3. Bias comparison (`BiasCheck`)
4. Guardrail + residual risk log (`GuardrailLog`)

Fill in the TODOs, then run:
```bash
python3 starter.py
```

## Solution

See `codebase/solutions/week-05/session-5.6/` (don't peek before attempting!).
