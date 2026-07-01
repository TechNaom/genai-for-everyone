# Exercise — Session 6.4: Monitoring & Observability

## Overview

Add structured logging and stats to a mock LLM service.

- **Core path:** Log every request (input, output, latency, tokens) and expose a `/stats`-style summary
- **Pro path:** Add a feedback log and a drift check that flags when a re-scored golden dataset drops below a threshold

## Setup

```bash
pip install -r requirements.txt
```

## Free/open path

Everything runs with mocked requests and in-memory logging — no API key or network calls needed.

## Optional paid-API path

Point `mock_service_call()` at your real Session 6.1 Flask service or Week 3/4 project to log real requests instead of simulated ones.

## Starter code

See `starter.py` in this folder.

## Solution

See `codebase/solutions/week-06/session-6.4/` (don't peek before attempting!).
