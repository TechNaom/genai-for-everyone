# Session 4.1 Project (Pro Path) — The Contradiction Case

## What you're building

The Core-path exercise had the agent react to a **missing** tool result (an
unknown city). This Pro-path project is harder: the tool result is present,
but it **contradicts** an assumption baked into the user's own question.

Example: *"It's supposed to rain in Phoenix tomorrow, should I bring an
umbrella?"* — the question assumes rain. The weather tool actually says
`{"tomorrow": "sunny", "chance_of_rain_pct": 2}`. A naive system might still
agree with the question's framing and tell the user to bring an umbrella
anyway. A genuinely reactive agent has to notice the contradiction and
correct the user instead of politely agreeing with a false premise.

This is still fully offline — no API key needed, no live model call. The
"planning" logic (comparing the observation to the question's assumption) is
what you write by hand here, exactly like the Core-path exercise, so you can
see the shape of a real re-planning branch before Session 4.2's tool-calling
agent has to do this kind of reasoning itself.

## Files

- `starter.py` — has 3 TODOs for you to complete
- `solution.py` — verified reference solution (run it, then compare)

## TODOs

**TODO 1 — `contains_assumed_rain`**
A simple keyword check on the question text: does it contain "rain" or
"raining"? This stands in for the "assumption" a real agent would have to
extract from the user's phrasing.

**TODO 2 — `run_agent_loop_pro`**
Call `weather_lookup`, then compare `assumed_rain` to whether
`weather["tomorrow"] == "rain"`. If they conflict, the `final_answer` must
explicitly correct the user and cite the real `chance_of_rain_pct` — not just
answer the literal question as if the premise were true. If the city has no
data, say so honestly (same pattern as the Core-path exercise). If they
agree, confirm the forecast lines up with the question.

**TODO 3 — `rigid_workflow_pro`**
Deliberately wrong: it calls `weather_lookup` (so it looks like it's using
real data) but the reply is built purely from whether the question mentioned
rain — it never actually checks that assumption against what the tool
returned. This is not a bug to fix; it's the comparison point.

## Running it

```bash
python3 starter.py
```

Once all three TODOs are filled in, you should see:
- The Chicago case (question assumes rain, forecast **is** rain): both versions give reasonable, matching advice.
- The Phoenix case (question assumes rain, forecast is **sunny**): the reactive agent explicitly corrects the user with the real forecast; the rigid workflow confidently gives the *wrong* advice, because it never checked.

Compare against `solution.py`:

```bash
python3 solution.py
```

## Verified output (from `solution.py`)

```
=== Consistent case: Chicago (question assumes rain, forecast IS rain) ===
Reactive agent: {
  "weather": {"tomorrow": "rain", "chance_of_rain_pct": 80},
  "assumed_rain": true,
  "final_answer": "That matches the forecast -- Chicago is expecting rain tomorrow (80% chance), so bring an umbrella."
}
Rigid workflow: Yes, as your question mentioned, tomorrow's rain means you'll want an umbrella.

=== Contradiction case: Phoenix (question assumes rain, forecast is SUNNY) ===
Reactive agent: {
  "weather": {"tomorrow": "sunny", "chance_of_rain_pct": 2},
  "assumed_rain": true,
  "final_answer": "Actually, tomorrow's forecast for Phoenix is sunny with only a 2% chance of rain -- the opposite of what your question assumed. You likely won't need an umbrella."
}
Rigid workflow: Yes, as your question mentioned, tomorrow's rain means you'll want an umbrella.

Notice: the rigid workflow gives the same wrong advice regardless of what
the tool actually returned -- it only ever reads the question, not the result.

=== No-data case: Nowheresville ===
Reactive agent: {
  "weather": {"error": "No data for Nowheresville"},
  "assumed_rain": true,
  "final_answer": "No weather data is available for Nowheresville, so I can't confirm or correct the assumption in your question -- check a live weather source."
}

[ALL ASSERTIONS PASSED]
```

## Reflection: what would the workflow version need to hard-code?

Write a short note answering this: to make `rigid_workflow_pro` handle the
Phoenix case correctly *without* becoming genuinely reactive, a programmer
would have to write an explicit branch — "if `contains_assumed_rain` is
True and `weather["tomorrow"] != "rain"`, output the correction sentence
instead" — anticipating this exact contradiction in advance. That branch
would still miss the next contradiction nobody thought to check for (e.g. a
question that assumes *snow* instead of rain, or one that assumes a specific
temperature). The reactive agent's advantage isn't that it happens to handle
this one case; it's that the comparison — assumption vs. observation — is a
general pattern it applies every time, not a growing list of special cases a
person has to keep adding to by hand.
