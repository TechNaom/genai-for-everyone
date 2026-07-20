# Session 4.2 Project — A Third, Deliberately Ambiguous Tool

## Goal

Design and add a *third* tool with a deliberately ambiguous boundary
against one of the first two (`calculator` and `weather_lookup`) —
something where a reasonable question could plausibly call either
tool, or where a vague description would make the model's choice
unpredictable. Run a handful of real questions through your three-tool
setup and observe whether the model picks the tool you'd expect every
time.

This builds directly on the core exercise (`exercises/`) — complete
that first if you haven't. It also requires a real `ANTHROPIC_API_KEY`,
for the same reason the core exercise does: the model's actual
tool-choice decision is the entire point, and there's no free or open
substitute for watching a live model make that call.

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic --break-system-packages
python starter.py
```

## The setup

`starter.py` scaffolds a `unit_converter` tool as the deliberately
ambiguous third tool, because a question like *"What's 68 degrees
Fahrenheit in Celsius?"* is genuinely ambiguous against `calculator` —
it's pure arithmetic under the hood, and a human might reasonably call
it either "a conversion" or "some math." `convert_units()` — a real,
working function supporting Fahrenheit/Celsius and miles/kilometers —
is already provided; your job is the schema and the dispatch wiring,
then the actual investigation.

## Instructions

1. **TODO 1** — Write `unit_converter`'s tool schema in
   `build_tool_schemas()`. Start with something plausible but not yet
   fully disambiguated from `calculator`'s existing description.
2. **TODO 2** — Add the `"unit_converter"` dispatch branch in
   `execute_tool()`, calling `convert_units(value, from_unit, to_unit)`.
3. Run `run_ambiguity_test()`. Add a `print(block.name)` inside your
   `run_conversation()` tool-use loop (or just read `solution.py`'s
   version, which already prints each tool call) so you can actually
   see which tool got called for each question, not just the final
   answer.
4. **For any case where the model picks the "wrong" tool** (or
   hesitates, or calls both when only one made sense), rewrite that
   tool's description to resolve the ambiguity — an explicit "use this
   for X, not for Y" clause in both descriptions is usually enough.
5. **Verify, don't assume.** Re-run the exact same question after your
   fix and confirm the tool choice actually changed. A description that
   *reads* clearer to you is not the same as a description that
   produces a different, correct decision from the model — check.

## What "done" looks like

- `unit_converter`'s schema and dispatch are wired up and working.
- You've run the ambiguous test questions and recorded which tool got
  called for each, before making any changes to the descriptions.
- For at least one case that resolved "wrong" initially, you tightened
  the relevant description(s) and re-ran the same question to confirm
  the fix actually worked — not just that the wording looks better.

## Stuck?

A fully worked reference solution, including tightened descriptions and
notes on why they were tightened that way, is in `solution.py` — run it
with `python solution.py`.
