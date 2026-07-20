# Session 6.4 Exercise: Structured Logging & Stats

**Goal:** Build the habit of logging every request to a GenAI service in a
consistent, aggregable shape, then computing real stats from that log instead
of guessing at how the system is behaving.

This exercise is fully self-contained: it simulates a service call with
`mock_service_call()` rather than requiring a real running Flask app, so it
needs no API calls, no paid keys, and no other session's code to run. It's a
pure logging-and-aggregation exercise: plain Python, runs anywhere.

## How to run

You'll need Python 3 installed. Check with:

```bash
python --version
```

Then run the starter file:

```bash
python starter.py
```

It will raise `NotImplementedError` until you fill in the functions below.

## The task

Open `starter.py`. Four functions need implementing:

- **`logged_call(user_input)`** (Core, Task 1) — call `mock_service_call`, then
  append one consistent log entry to `REQUEST_LOG` containing `input`,
  `output`, `latency_ms`, `input_tokens`, and `output_tokens`. Return the
  result.
- **`print_stats()`** (Core, Task 2) — using `REQUEST_LOG`, print total
  requests, average latency, and total tokens (input + output combined). This
  is your `/stats`-equivalent: a summary computed entirely from logged data.
- **`log_feedback(request_index, thumbs_up)`** (bonus, Task 3) — append
  `{"request_index": ..., "thumbs_up": ...}` to `FEEDBACK_LOG`.
- **`check_drift(score_fn, threshold=0.8)`** (bonus, Task 4) — re-score
  `GOLDEN_DATASET` using `score_fn`, compute the pass rate, print it against
  the threshold, and return whether it passed.

Tasks 1–2 are the Core path for this session. Tasks 3–4 preview the same
mechanics as this session's Pro-path project (feedback loop + drift check) —
attempt them here for a warm-up, or skip straight to the fuller build in
`../project/`.

## What "good" looks like

`print_stats()` should never crash on an empty log, and every request you log
should carry the exact same fields — that consistency is what makes
aggregation possible. If `logged_call` and `print_stats` are correct, running
`starter.py` should print three requests' worth of stats followed by a drift
check result, with no errors.

## Checking your work

There's no automated grader — that's intentional. Compare your implementation
against `solution.py` (run it with `python solution.py`) once you've made a
genuine attempt. The shapes should match closely; minor formatting
differences are fine.

## Free/open path

Everything runs with a mocked service call and in-memory logging — no API key
or network access needed.

## Optional paid-API path

Once `logged_call` and `print_stats` work, try pointing `mock_service_call()`
at a real model call (any provider, free tier is fine) instead of the
simulated response, and watch the logged latency and token counts become real
measurements instead of random placeholders.
