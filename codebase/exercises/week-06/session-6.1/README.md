# Exercise — Session 6.1: From Notebook to Application

## Overview

Wrap an LLM-calling function in a minimal Flask service with proper config and error handling.

- **Core path:** A single `/ask` endpoint, config from environment variables
- **Pro path:** Add `/health`, input validation with proper error codes, and fail-fast startup config checks

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # add ANTHROPIC_API_KEY if you want to call a real model
```

## Free/open path

The starter code defaults to a mock `call_llm()` function so the whole exercise works with zero API cost and no key required. Run it, test it with `curl`, and everything below works exactly the same either way.

## Optional paid-API path

Set `ANTHROPIC_API_KEY` in your `.env` and swap the mock `call_llm()` for a real Anthropic API call (a few lines — see the comment in `starter.py`) to see the same service pattern with a real model.

## Starter code

See `starter.py` in this folder. Run with:
```bash
python3 starter.py
```
Then in another terminal:
```bash
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{"question": "What is RAG?"}'
```

## Solution

See `codebase/solutions/week-06/session-6.1/` (don't peek before attempting!).
