# Exercise — Session 6.3: Choosing & Switching Models

## Overview

Build a provider adapter layer, then add a fallback strategy on top of it.

- **Core path:** Implement `call_model(prompt, provider=...)` for 2+ mocked providers/tiers and compare cost/latency/quality
- **Pro path:** Add `call_model_with_fallback(prompt, primary, fallback)` that automatically falls back when the primary provider fails

## Setup

```bash
pip install -r requirements.txt
```

## Free/open path

The starter code mocks provider calls (including a simulated random outage) so the whole exercise is free and deterministic to grade. Swap in real API calls if you want real cost/latency numbers.

## Optional paid-API path

Replace `_call_provider_a` / `_call_provider_b` with real Anthropic/OpenAI calls to compare real models side by side.

## Starter code

See `starter.py` in this folder.

## Solution

See `codebase/solutions/week-06/session-6.3/` (don't peek before attempting!).
