# Exercise — Session 6.6: Week 6 Lab — Mini Build Day

## Overview

Combine Week 6's pieces (service, logging, fallback, regression gate) into one deployable project with a `DEPLOY.md`.

- **Core path:** Flask service + logging/stats + `/health`, with a `DEPLOY.md` a stranger could follow in 5 minutes
- **Pro path:** Add the provider-fallback adapter and a startup-time regression gate that refuses to start if the golden dataset score is below threshold

## Setup

```bash
pip install -r requirements.txt
```

## Free/open path

Everything mocks the underlying model calls, so the whole lab runs and is gradeable with no API key or hosting account.

## Optional paid-API path

Swap the mocked `call_model()` for a real Anthropic/OpenAI call, and optionally deploy to a free tier of Render/Railway/Fly.io/PythonAnywhere for a real public URL.

## Starter code

See `starter.py` in this folder.

## Solution

See `codebase/solutions/week-06/session-6.6/` (don't peek before attempting!).
