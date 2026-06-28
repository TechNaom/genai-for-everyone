# Session 4.2 Exercise — An LLM That Calls a Real Weather/Calculator Tool

## Goal

Wire up the same `calculator` and `weather_lookup` functions from Session
4.1 to a real LLM via the Anthropic API's tool-use feature, and watch
the model genuinely decide — on its own — whether a question needs a
tool, which one, and with what arguments.

## This one needs a real API key

Sessions 4.1's trace was a scripted simulation by design — there's no
live model in this environment to make real decisions. This exercise is
different: the model's actual tool-calling decision is the entire point,
so there's no meaningful offline substitute for the full loop. To run it
end to end:

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic --break-system-packages
python3 tool_calling_agent.py
```

If you don't have a key yet, you can still do real, verifiable work
offline — `build_tool_schemas()` and `execute_tool()` are pure logic
with no API dependency, and `offline_test()` validates both, including
two error-handling edge cases, without needing any API access. Get
those two functions right first; they're most of what makes the loop
actually work once you do have a key.

## Instructions

1. Open `tool_calling_agent.py`.
2. Fill in the three TODOs, in order:
   - `build_tool_schemas()` — define both tools' name, description, and
     input_schema for the Anthropic API. Write real, specific
     descriptions — vague ones produce unreliable tool-calling behavior,
     exactly as the session described.
   - `execute_tool()` — dispatch a tool name + input dict to the correct
     real function, handling the calculator's invalid-input case and an
     unknown-tool case defensively rather than letting either crash.
   - `run_conversation()` — the full loop: send the message, check
     `stop_reason`, execute any requested tools, send results back,
     repeat until the model produces a final answer.
3. Run `python3 tool_calling_agent.py`. This runs `offline_test()` first
   (no API key needed), then attempts the full loop against four real
   test questions (API key required for this part).

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

## Pro path — extended challenge

Design and add a *third* tool with a deliberately ambiguous boundary
against one of the first two — something where a reasonable question
could plausibly call either tool, or where a vague description would
make the model's choice unpredictable. Run a handful of real questions
through your three-tool setup and observe whether the model picks the
tool you'd expect every time. For any case where it picks the "wrong"
one, rewrite that tool's description to resolve the ambiguity, and
**verify** with the same question that the fix actually worked — don't
just assume it did because the new wording sounds clearer to you.

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

A fully worked reference solution, including the Pro path notes, is in
`codebase/solutions/week-04/session-4.2/`.
