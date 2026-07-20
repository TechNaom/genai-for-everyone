# Session 6.3 Project: The Fallback Rate Monitor

The Pro path build for Session 6.3 — on top of the adapter layer from the
exercises, implement a fallback wrapper, `call_model_with_fallback`, that
calls a primary provider, catches a simulated outage, automatically retries
against a fallback provider, and logs which provider actually served each
request. That log is what turns "we have a fallback" from a claim into a
measurable number.

## What you'll build

- `call_model(prompt, provider)` — the same adapter pattern from the lesson
  and exercises: look up a provider function, call it, raise a clear
  `ValueError` for an unrecognized name.
- `call_model_with_fallback(prompt, primary, fallback)` — call `primary`;
  if it raises a `ConnectionError` (the simulated outage), automatically
  retry against `fallback`. Tag the result with `used_provider` so the
  caller always knows which one actually answered, and append a record to
  `CALL_LOG` either way.
- `measure_fallback_rate(n_calls)` — fire `n_calls` requests through
  `call_model_with_fallback`, then use `CALL_LOG` to report how many of them
  actually needed the fallback, as both a count and a percentage.

Example run (after completing all three):

```
=== Single call with fallback ===
{'text': '[primary] answer to: What is a circuit breaker?', 'cost': 0.03, 'latency_ms': 30, 'used_provider': 'primary'}

=== Measuring the fallback rate over many calls ===
Fallback triggered on 11/50 calls (22.0%) -- expect roughly 25% given primary's simulated outage rate
```

Run it again and the exact numbers will shift a little — the outage is
randomized on purpose — but they should stay in the neighborhood of 25%.

## How to run it

```bash
python starter.py
```

No API key and no internet access needed — this is a fully offline exercise.
The primary provider's outage is simulated in-process with `random`, so the
whole thing runs deterministically-enough to grade without ever touching a
real network call. Fill in the three functions, then re-run to see the fallback rate
printed. Want to see one finished version first? Run `python solution.py`.

## The habit this trains

A fallback that exists in code but is never measured is a fallback nobody
actually trusts in production — when someone asks "how often does this
actually kick in?", the honest answer should come from a log, not a guess.
Tagging every response with `used_provider` and accumulating that into
`CALL_LOG` is the small habit that makes a reliability claim ("we have
automatic failover") into an observable fact you could put in a dashboard.

## Ideas to make it your own (optional stretch goals)

- Change `_call_primary`'s simulated outage rate and re-run
  `measure_fallback_rate` — confirm the measured rate tracks the change.
- Add a third provider and a `call_model_with_tiered_fallback` that tries
  primary, then secondary, then a last-resort tertiary provider, logging the
  full chain of providers attempted for each call.
- Add a basic circuit breaker: after 3 consecutive primary failures, skip
  calling primary entirely for the next 5 calls and go straight to the
  fallback — then measure how much that changes total latency across a
  batch of calls.

## Why this project matters

A fallback wrapper is easy to write and easy to leave completely untested in
the one situation that matters: a real outage. The value of this project
isn't the `try`/`except` — it's the discipline of logging which path served
every request, so "our fallback works" is something you can prove with a
number instead of assert with confidence. That's the same discipline that
lets a team say, during a real incident, "yes, the fallback is handling it,
here's the rate" instead of hoping quietly that it is.
