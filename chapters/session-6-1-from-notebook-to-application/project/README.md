# Session 6.1 Project: Health, Validation & Fail-Fast Startup

The Pro path build for Session 6.1 — take the Core path `/ask` service and
make it operable: a `/health` endpoint for uptime checks, input validation
that always returns a proper 4xx instead of a stack trace, and a startup
check that refuses to boot with a clear error if a required environment
variable is missing.

## Setup

```bash
pip install flask
```

No real API key is required to complete this project — `call_llm()` stays
mocked, exactly like the Core path exercise. The startup check and the API
key are only connected through the `REQUIRE_API_KEY` flag, which you can
toggle on to see the fail-fast behavior without ever making a real call.

## What you'll build

Starting from the working `/ask` endpoint, add three things:

1. **A `/health` endpoint** — `GET /health` returns
   `{"status": "ok", "model": MODEL_NAME}` with a `200`. It must never call
   `call_llm()` or do anything expensive; infrastructure should be able to
   hit it constantly and cheaply.
2. **Real input validation** — reject a missing/invalid JSON body, a missing
   `question` field, a `question` that isn't a string, and an
   empty/whitespace-only `question`. Each case returns a `400` with a
   specific `error` message, never an unhandled exception.
3. **A fail-fast startup check** — if `REQUIRE_API_KEY` is `"true"` and
   `ANTHROPIC_API_KEY` isn't set, print a `FATAL:` message naming the exact
   missing variable to `stderr` and exit with a non-zero status, *before*
   the server starts listening.

## Example run

```
$ REQUIRE_API_KEY=true python3 starter.py
FATAL: REQUIRE_API_KEY is set but ANTHROPIC_API_KEY is missing from the environment.
$ echo $?
1

$ REQUIRE_API_KEY=true ANTHROPIC_API_KEY=sk-test-key python3 starter.py
 * Running on http://127.0.0.1:5000

$ curl http://localhost:5000/health
{"model": "claude-3-5-haiku-20241022", "status": "ok"}

$ curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{}'
{"error": "question is required"}
   (HTTP 400 -- not a stack trace)

$ curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{"question": 42}'
{"error": "question must be a non-empty string"}
   (HTTP 400)
```

## How to run it

```bash
python3 starter.py
```

Then in another terminal:

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'

curl http://localhost:5000/health
```

Want to see one finished version first? Run `python3 solution.py`.

## Why fail fast matters here specifically

`REQUIRE_API_KEY` defaults to `false`, so by default the mocked
`call_llm()` never actually needs a real key — this project is designed to
be fully testable with zero API cost. Flip it on and you can watch the exact
failure mode the lesson describes: the process refuses to boot at all, with
a message that tells whoever is deploying precisely what's missing, instead
of surfacing as a confusing crash the moment a real user's request reaches
the code path that needed the key.

## Ideas to make it your own (optional stretch goals)

- Add a request size limit (e.g. reject a `question` longer than 4,000
  characters with a `400`) — a real, cheap guard against a client
  accidentally sending an entire document.
- Extend the startup check to validate more than one required variable at
  once, and report all of the missing ones in a single message instead of
  stopping at the first.
- Swap the mocked `call_llm()` for a real Anthropic call (commented out in
  the starter) and confirm your validation still rejects bad input *before*
  a single token is spent calling the model.

## Why this project matters

The gap between "a service that works when I test it" and "a service that's
actually safe to deploy" is almost entirely about how it behaves at the
edges: what happens when a client sends garbage, and what happens when the
environment it's deployed into isn't fully configured yet. Neither of those
is an AI problem — they're the plain operability habits that separate a
take-home project from something a real team would trust in production. A
hiring manager who sees a `/health` endpoint, clean 4xx errors, and a
fail-fast startup check is seeing evidence you've shipped something real
before, even if this is the first time.
