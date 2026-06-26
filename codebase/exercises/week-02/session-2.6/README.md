# Session 2.6 Exercise — Customer Support Reply Generator with Tone Control

## Your task

Open `support_reply_generator.py` and complete the six TODOs:

1. **TODO(1)** — Write few-shot example replies for each of the three tones
   (`empathetic`, `professional`, `concise`) inside the prompt template.
2. **TODO(2)** — Write the internal-reasoning instructions: ask the model to
   think through the customer's actual need, whether it has enough
   information, and whether escalation is warranted — *before* writing the
   final JSON, without leaking that reasoning into the output.
3. **TODO(3)** — In `build_prompt()`, validate the `tone` argument and fill
   in the template's variables.
4. **TODO(4)** *(optional)* — Wire up a real LLM call in `call_llm()` if you
   have API access. The stub works fine without this.
5. **TODO(5)** — Implement `parse_reply()`: strip wrapper text, parse JSON,
   validate every field, and raise clear `ValueError`s on any problem.
6. **TODO(6)** — Implement the fallback path in `generate_reply()` so a
   parsing failure becomes a safe escalation instead of a crash.

## Running it

```bash
python3 support_reply_generator.py
```

With the provided stub `call_llm()`, this tests your parsing and validation
logic against a deliberately messy model response (wrapped in markdown code
fences) without needing API access.

To test against a real model, set `USE_REAL_LLM=1` and complete TODO(4) with
your own API call.

## What "done" looks like

- All three sample tickets produce valid, schema-matching JSON output.
- Passing a `tone` value outside `VALID_TONES` raises a clear `ValueError`
  immediately in `build_prompt()`, not a confusing failure later.
- Deliberately feeding `parse_reply()` broken input (try editing the stub's
  return value to remove a field, or to return non-JSON text) raises a
  `ValueError` with a message that tells you exactly what's wrong.
- If you set the result of `call_llm()` to something unparseable,
  `generate_reply()` still returns a valid `SupportReply` — with
  `escalate: True` — rather than crashing.

## Why this exercise matters

This is the session where the five techniques from earlier in the week stop
being separate party tricks and become one system. If you find yourself
tempted to skip the few-shot examples or the reasoning step "because the
stub doesn't really need them" — try removing them anyway and see how much
less trustworthy your design feels even before you've run a single LLM
call. That instinct (trustworthy vs. not) is the thing this whole week has
been training.

## Stuck?

A fully worked reference solution is in
`codebase/solutions/week-02/session-2.6/`. Try to get through TODO(5) on
your own first — the defensive parsing logic is the part most worth
struggling with, since it's the part that quietly makes or breaks a real
production prompt system.
