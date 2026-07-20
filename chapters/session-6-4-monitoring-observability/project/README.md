# Session 6.4 Project (Pro path): Feedback Loop + Drift Check

**Goal:** Extend a small Flask service with a feedback endpoint and a drift
check that compares each check against the *previous* one — not just a fixed
absolute threshold — so a system that's still "passing" but visibly sliding
gets flagged before it fully fails.

This is fully offline: `call_llm()` is a mock grounded in an in-memory
`KNOWLEDGE_BASE` dict (standing in for a RAG index), so no API key or network
access is needed. A `/simulate-policy-update` endpoint lets you manufacture
drift on demand, the same way an un-refreshed retrieval index would silently
go stale after a real policy change — so you can watch your own `/drift`
check catch it.

## Setup

```bash
pip install flask
```

## How to run

```bash
python starter.py
```

The service starts on `http://localhost:5000`. In a second terminal:

```bash
# Ask a question -- logs the request, returns a request_id + answer
curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
  -d '{"question": "remote work policy"}'

# Check aggregate stats
curl http://localhost:5000/stats

# Log feedback against a request_id from the /ask response above
curl -X POST http://localhost:5000/feedback -H "Content-Type: application/json" \
  -d '{"request_id": "<paste request_id here>", "thumbs_up": true}'

# Run a drift check -- first call just records a baseline
curl http://localhost:5000/drift

# Manufacture drift (simulates a policy change nobody re-indexed)
curl -X POST http://localhost:5000/simulate-policy-update

# Run the drift check again -- this one should flag it
curl http://localhost:5000/drift
```

## The task

Open `starter.py`. `/ask`, `/stats`, and `call_llm` are already implemented
(the Core-path logging pattern from the exercises) — the Pro-path work is two
functions:

1. **`POST /feedback`** — read `request_id` (string, must match a request
   already in `REQUEST_LOG`) and `thumbs_up` (bool) from the JSON body.
   Validate both; return a 400 with a JSON error on anything malformed or
   unmatched. On success, append the record to `FEEDBACK_LOG` and return it.

2. **`check_drift(threshold=0.15)`** — re-score `GOLDEN_DATASET` against the
   live `KNOWLEDGE_BASE` using `score_fn`, compute the pass rate, and append
   it to `DRIFT_HISTORY`. Compare against the *previous* entry in
   `DRIFT_HISTORY` (not the first run — there's nothing to compare against
   yet). Flag `drifted=True` if the pass rate dropped by more than
   `threshold` since that previous check.

## Why compare to the last run, not just a fixed threshold

A fixed threshold alone (e.g. "flag if pass rate < 80%") can hide a system
that's steadily sliding — 98% this week, 84% next week, both still "passing"
individually, while something is clearly getting worse. Comparing each check
to the one before it catches the *trend*, which is the thing you actually
want to know about. In a real system you'd keep both: an absolute floor you
never want to cross, and a relative-drop check that catches a slide before it
reaches that floor.

## Checking your work

There's no automated grader — that's intentional. Verify by hand:

- `POST /feedback` with a valid `request_id` and `thumbs_up: true/false`
  returns 200 and the record appears in `FEEDBACK_LOG`.
- `POST /feedback` with a made-up `request_id`, a missing field, or a
  non-boolean `thumbs_up` returns 400 with a clear error — it should never
  crash the server.
- The first `GET /drift` call reports a baseline with `drifted: false`.
- After `POST /simulate-policy-update`, the next `GET /drift` call reports
  `drifted: true` with a message describing the drop.

Compare your implementation against `solution.py` once you've made a genuine
attempt.

## Ideas to make it your own

- Add a `/feedback/summary` endpoint that reports the thumbs-up rate overall
  and per logged request.
- Persist `REQUEST_LOG`, `FEEDBACK_LOG`, and `DRIFT_HISTORY` to a file between
  runs instead of resetting every time the process restarts.
- Swap the fixed `DRIFT_DROP_THRESHOLD` for one read from an environment
  variable, so ops can tune sensitivity without a code change (the same
  environment-based configuration habit from Session 6.1).

## Free/open path

Everything above runs fully offline with the mock `call_llm()` — no API key,
no network calls.

## Optional paid-API path

Swap `call_llm()` for a real model call (see the commented example in
`starter.py`), and adapt `KNOWLEDGE_BASE`/`score_fn` into a real similarity or
exact-match check against your provider's actual output.
