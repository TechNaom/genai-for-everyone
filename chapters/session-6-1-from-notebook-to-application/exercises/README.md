# Session 6.1 Exercise: Wrap an LLM Call in a Flask Service

**Goal:** Turn a plain `call_llm()` function into a real, running HTTP
service with one `/ask` endpoint — config read from the environment, and no
crashes on a malformed request. This is the Core path build for Session 6.1.

## Setup

```bash
pip install flask
```

## Free/open path

The starter code defaults to a mock `call_llm()` function, so the whole
exercise works with zero API cost and no key required — you're practicing the
service-wrapping pattern, not the model call itself.

## Optional paid-API path

Want to call a real model? Install `pip install anthropic`, set
`ANTHROPIC_API_KEY` in your environment, and swap the mock body of
`call_llm()` for the real API call shown commented out in `starter.py`.

## How to run

```bash
python3 starter.py
```

Then in another terminal:

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

## The task

Open `starter.py`. Two pieces are missing:

- **TODO 1** — read `MODEL_NAME` from an environment variable
  (`os.environ.get("MODEL_NAME", ...)`) with a sensible default, instead of
  hard-coding it.
- **TODO 2** — inside the `/ask` route, validate that the request's JSON body
  includes a non-empty `"question"` field. If it's missing, return a `400`
  with a JSON error body (`{"error": "question is required"}`) — do not let
  it crash with an unhandled exception. If it's present, call `call_llm()`
  and return the answer as JSON.

## Debug the code

A buggy version of the route calls `request.get_json()` (without
`silent=True`) and then `.get("question", "")` directly on the result. When a
client sends a request with **no body at all**, `get_json()` returns `None`,
and calling `.get()` on `None` crashes with an `AttributeError` — a `500`
with a raw stack trace instead of a clean `400`. The fix: use
`request.get_json(silent=True)` and check for the `None`/missing case
explicitly before touching `.get()`.

## What "done" looks like

- A valid request (`{"question": "What is RAG?"}`) returns a `200` with an
  `answer` field.
- A request with no `question` field returns a clean `400` with an `error`
  field — never a stack trace.
- Changing `MODEL_NAME` in your shell before running the script (e.g.
  `MODEL_NAME=claude-sonnet-4-5 python3 starter.py`) changes the model name
  in the response with zero code edits.

Compare your version against `solution.py` (run it with
`python3 solution.py`) once you've made a genuine attempt.
