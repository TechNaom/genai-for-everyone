# Session 4.2 Exercise — An LLM That Calls a Real Weather/Calculator Tool

## Goal

Wire up the same `calculator` and `weather_lookup` functions from Session
4.1 to a real LLM via the Anthropic API's tool-use feature, and watch
the model genuinely decide — on its own — whether a question needs a
tool, which one, and with what arguments.

## Free/open vs. paid API — read this first

Most of this course's exercises run entirely free and offline. This one
is the exception, and deliberately so: the model's actual tool-calling
*decision* is the entire point of the exercise, and there is no free or
open substitute for a live model making that decision. The Anthropic
API is a paid, metered service (Session 4.1's simulated trace was
designed specifically to avoid this cost while you learned the
concepts; this session is where that training wheel comes off).

To run it end to end:

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic --break-system-packages
python starter.py
```

**If you don't have a key yet, you can still do real, verifiable work
offline.** `build_tool_schemas()` and `execute_tool()` are pure logic
with no API dependency, and `offline_test()` validates both — including
two error-handling edge cases — without needing any API access. Get
those two functions right first; they're most of what makes the loop
actually work once you do have a key. It's also fine to test the
*shape* of `run_conversation()`'s request with a fake placeholder key —
`anthropic.Anthropic()` constructs without ever touching the network,
so you can confirm your request is built correctly and only see it fail
once it actually reaches the API.

## Instructions

1. Open `starter.py`.
2. Fill in the three TODOs, in order:
   - `build_tool_schemas()` — define both tools' name, description, and
     input_schema for the Anthropic API. Write real, specific
     descriptions — vague ones produce unreliable tool-calling behavior,
     exactly as the lesson described.
   - `execute_tool()` — dispatch a tool name + input dict to the correct
     real function, handling the calculator's invalid-input case and an
     unknown-tool case defensively rather than letting either crash.
   - `run_conversation()` — the full loop: send the message, check
     `stop_reason`, execute any requested tools, send results back,
     repeat until the model produces a final answer.
3. Run `python starter.py`. This runs `offline_test()` first (no API key
   needed), then attempts the full loop against four real test
   questions (API key required for this part).

## Core path

Get `offline_test()` passing first. Then, if you have an API key, run
the full demo against all four test questions. Pay close attention to
the third question ("What's 127 times 38?") — does the model call the
calculator tool, or does it just answer directly from its own
arithmetic ability? Either is a legitimate, observable outcome — the
point is to actually watch what the model decides, not assume.

Also watch the fourth question (Miami, a city not in `WEATHER_DB`). Does
the model report the tool's honest error back to you clearly, or does
it try to guess at Miami's weather anyway despite the tool telling it
there's no data?

## What "done" looks like

- `offline_test()` passes with no assertion errors.
- If you have an API key: all four test questions return a sensible
  final answer, with the calculator and weather questions actually
  triggering the corresponding tool (you can confirm this by adding a
  print statement inside your loop, or by trusting the answer's content
  — e.g. the umbrella-cost question should produce the correct total).
- The Miami question (unknown city) produces an honest "no data
  available" type of answer, not a guessed weather report.

## Stuck?

A fully worked reference solution is in `solution.py` — run it with
`python solution.py`. Once you've got the core path working, head to
the project for the Pro-path extended challenge: adding a third tool
with a deliberately ambiguous boundary against one of these two.
