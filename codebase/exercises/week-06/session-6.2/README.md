# Exercise — Session 6.2: Cost & Latency Engineering

## Overview

Build a cost calculator for an LLM workload, then use it to compare optimizations.

- **Core path:** Calculate daily/monthly cost across model tiers for a given workload, and show the impact of one optimization (shorter prompts, cheaper model)
- **Pro path:** Design a routing strategy that sends simple requests to a cheap model and complex ones to an expensive model, and show the blended cost savings

## Setup

```bash
pip install -r requirements.txt
```

## Free/open path

Everything here is pure arithmetic on token counts and published price-per-million-token rates (provided as constants in the starter code) — no API calls needed, no cost to run this exercise.

## Optional paid-API path

If you want real numbers instead of estimates, call your Week 3/4 project with `tiktoken` (already in `requirements.txt`) to count actual tokens used per request, then feed those real numbers into the calculator.

## Starter code

See `starter.py` in this folder.

## Solution

See `codebase/solutions/week-06/session-6.2/` (don't peek before attempting!).
