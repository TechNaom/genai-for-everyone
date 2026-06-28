# Session 4.1 Exercise — What "AI Agents" Actually Means

## What you're building

Two small, fully-offline programs that make the chapter's central
distinction concrete: a **reactive agent loop** (plan → act → observe,
where the next step depends on what a tool actually returned) versus a
**rigid workflow** (a fixed sequence that assumes a tool result will
always look a certain way).

No live LLM calls are used here — there's no model API access in this
sandbox, and that's fine: today's goal is to internalize the *loop
structure* itself before you build a real tool-calling agent in Session
4.2. Both tools (`calculator` and `weather_lookup`) are real, fully
working Python functions, even though the "planning" decisions in this
exercise are ones you write yourself rather than ones a model makes.

## Files

- `starter.py` — has 2 TODOs for you to complete
- `solution.py` — verified reference solution (run it, then compare)

## TODOs

**TODO 1 — `run_agent_loop`**
Complete the loop so it:
1. Calls `calculator` to get the umbrella total cost.
2. Calls `weather_lookup` for the given city.
3. Builds a `final_answer` string using *only* values that came from
   the tool calls — no invented numbers. If the weather lookup returns
   an `"error"` key, your answer must say data isn't available; it must
   **not** try to read `chance_of_rain_pct` in that case.

**TODO 2 — `rigid_workflow`**
Complete the one missing line so it directly indexes
`weather["chance_of_rain_pct"]` with no error handling. This is
deliberately fragile — you are not meant to "fix" it. The point is to
watch it crash on a city `weather_lookup` doesn't know about, and
compare that to how your `run_agent_loop` from TODO 1 handles the exact
same situation.

## Running it

```bash
python3 starter.py
```

Once both TODOs are filled in, you should see:
- `run_agent_loop("Chicago")` produce a grounded final answer recommending an umbrella
- `run_agent_loop("Nowheresville")` produce an honest "no data" answer, with no crash
- `rigid_workflow("Chicago")` succeed
- `rigid_workflow("Nowheresville")` raise a `KeyError` — this crash is **expected**, not a bug to fix

Compare against `solution.py`:

```bash
python3 solution.py
```

## Verified output (from `solution.py`)

```
=== run_agent_loop on Chicago ===
{
  "total_cost": 43.5,
  "weather": {
    "tomorrow": "rain",
    "chance_of_rain_pct": 80
  },
  "final_answer": "3 umbrellas at $14.50 each = $43.50 total. Chicago's forecast for tomorrow is rain with an 80% chance of rain, so yes, you will likely need one."
}

=== run_agent_loop on Nowheresville (not in DB) ===
{
  "total_cost": 43.5,
  "weather": {
    "error": "No data for Nowheresville"
  },
  "final_answer": "3 umbrellas at $14.50 each = $43.50 total. No weather data is available for Nowheresville, so I can't tell you if you'll need an umbrella tomorrow -- check a live weather source."
}

=== rigid_workflow on Chicago ===
80% chance of rain. Total cost: $43.50

=== rigid_workflow on Nowheresville (should crash) ===
CRASHED as expected: KeyError: 'chance_of_rain_pct'

[ALL ASSERTIONS PASSED]
```

## Reflection questions (write a few sentences on each)

1. In `run_agent_loop`, which line is the "decision point" that makes
   this an agent rather than a workflow? (Hint: it's the `if "error" in
   weather:` branch — this is the model/program reacting to what it
   just observed, rather than assuming a fixed shape.)
2. `rigid_workflow` crashed only when given a city outside `WEATHER_DB`.
   Why did it work fine for Chicago? What does that tell you about why
   broken workflows often look correct in demos?
3. Could you "fix" `rigid_workflow` with a `try/except` around the
   `KeyError`? Yes — but what's the difference between that fix and
   what `run_agent_loop` does? (Hint: think about how many *different*
   unanticipated tool failures each approach could handle without a
   programmer writing a new branch for each one.)

## Pro path

See the chapter's "Pro path" section for the harder variant: a task
where the tool's result *contradicts* an assumption baked into the
question itself, and you have to design the re-planning branch that
makes the agent override the user's framing when the evidence demands
it.
