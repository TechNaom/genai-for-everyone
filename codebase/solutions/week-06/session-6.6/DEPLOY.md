# Deploying the Week 6 Lab Service

## Requirements
- Python 3.10+
- `pip install -r requirements.txt` (from the repo root)

## Environment variables
None are required to run with the mocked model calls. To point at a real
model, set `ANTHROPIC_API_KEY` and swap `_call_primary`/`_call_fallback` for
real API calls (see Session 6.1's example).

## Run it
```bash
python3 week6_lab_solution.py
```
The service starts on port 5000 (override with `PORT=8080`). If the startup
regression check fails, the process exits immediately with a clear error
instead of starting in a broken state.

## Verify it's healthy
```bash
curl http://localhost:5000/health
```

## Try it
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "vacation days after 2 years"}'
```

## Optional: free-tier hosting
Any of Render, Railway, Fly.io, or PythonAnywhere's free tiers can run this
as-is (`python3 week6_lab_solution.py`, exposing `$PORT`). Check each
platform's current free-tier terms before relying on one long-term.
