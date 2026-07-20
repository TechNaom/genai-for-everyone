# Session 6.6 — Week 6 Lab: Mini Build Day

## What you're building

One deployable Flask project that combines every piece from Week 6 into a
single running process:

- **Core path:** the service wrapper, request logging, and a `/health`
  endpoint, plus a `DEPLOY.md` a stranger could follow in under 5 minutes.
- **Pro path:** a provider-fallback adapter and a startup-time regression
  gate that refuses to start the service if a golden dataset score falls
  below threshold.

| Week 6 session | What you're reusing here |
|---|---|
| 6.1 Service wrapper | The Flask app, `/ask` endpoint, env-based `PORT` config |
| 6.2 Cost & latency | Per-request timing returned as `latency_ms` |
| 6.3 Provider fallback | `call_model_with_fallback()` |
| 6.4 Logging & feedback | `REQUEST_LOG`, `/health` |
| 6.5 CI/CD & regression gates | `run_regression_check()`, `GOLDEN_DATASET` |

## Files

- `starter.py` — your starter file. Every `# TODO` needs filling in.
- `solution.py` — the reference answer key. Don't open it until you've
  given the Core and Pro paths a real attempt.

## Setup

```bash
pip install flask
```

No paid API key or hosting account is required. `_call_primary` and
`_call_fallback` are mocked, so the whole lab runs and is gradeable offline.

## How to work through it

1. **Core path.** Fill in `call_model_with_fallback()` (Task 1) and the
   `# TODO` inside the `ask()` view (Task 2). Run:
   ```bash
   python3 starter.py
   ```
   Verify it with:
   ```bash
   curl http://localhost:5000/health
   curl -X POST http://localhost:5000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "vacation days after 2 years"}'
   ```
   Then write your own `DEPLOY.md` (Task 3) describing exactly how someone
   else would run this project — setup, environment variables (there are
   none for the mocked version — say so explicitly), the start command, and
   how to confirm it's healthy.

2. **Pro path — this is the real lesson of the lab.** Fill in
   `run_regression_check()` (Task 4): score `GOLDEN_DATASET` against
   `call_model_with_fallback()`, compute a pass rate, and return `True` only
   if it clears `REGRESSION_THRESHOLD`. The `__main__` block already calls
   this *before* `app.run()` and exits non-zero if it fails — don't just
   trust that it works. Prove it (Task 5):
   - Temporarily lower `REGRESSION_THRESHOLD` past what your implementation
     can hit, or make `_call_primary` always raise `ConnectionError` with no
     working fallback path, and confirm the service refuses to start with a
     clear `FATAL` message — no port opens.
   - Restore the threshold and confirm it starts normally again.

   That's the actual point of a *startup-time* gate versus a CI-only one: it
   catches bad configuration the moment the process tries to boot, regardless
   of how it got into that state — not just when a change goes through a
   pull request.

3. **Debug task.** A teammate's fallback catches `Exception` instead of the
   specific `ConnectionError` it's meant to recover from, which hides real
   bugs behind a fallback answer instead of surfacing them. Find and fix it
   (Task 6, in the exercises page).

## A note on the Pro-path gate

This is a different kind of "gate" than a CI check you may have built in
Session 6.5. The underlying idea is the same — score a golden dataset,
compare to a threshold — but *where* it runs is the point: a CI check only
fires when code goes through the normal PR pipeline, so it can't catch a
manual deploy, a stale environment variable, or a wrong dataset file loaded
outside that pipeline. A startup-time gate re-runs on every single boot, so
it catches exactly the class of bug a CI-only check structurally can't see.

## Deploying it further (optional)

Once your Core and Pro paths both pass locally, you can go one step further
and give the service a real public URL — this isn't required for the lab,
but it's a natural next step if you want the "it's actually live" experience:

- Swap `_call_primary` / `_call_fallback` for real Anthropic or OpenAI API
  calls, guarded behind an `ANTHROPIC_API_KEY` (or equivalent) environment
  variable — see Session 6.1's example for the pattern.
- Deploy to a free tier of Render, Railway, Fly.io, or PythonAnywhere. All
  of these can run this project as-is with `python3 starter.py` (or
  `solution.py`), reading the port from the `$PORT` environment variable
  they provide automatically. Check each platform's current free-tier terms
  before relying on one long-term — they change.
- Update your `DEPLOY.md` to describe the real steps you actually followed
  on that platform, not the steps you assumed would work. A `DEPLOY.md`
  written before you've actually deployed is a guess, not documentation.

## Pro path: extend it further

If you finish early: deliberately trigger the primary's ~20% simulated
failure rate enough times to watch `REQUEST_LOG` fill up with a mix of
`[primary]` and `[fallback]` answers, and confirm every one of them still
returns a normal 200 response to the caller — the entire point of a
fallback is that the caller should never be able to tell, from the outside,
that anything went wrong upstream.
