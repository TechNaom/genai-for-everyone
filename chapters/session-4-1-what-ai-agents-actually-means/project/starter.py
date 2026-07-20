"""
Session 4.1 Project — Pro Path
================================
The Core-path exercise had the agent react to a MISSING tool result (an
unknown city). This Pro-path project is harder: the tool result is present,
but it CONTRADICTS an assumption baked into the user's own question.

Example: "It's supposed to rain in Phoenix tomorrow, should I bring an
umbrella?" -- the question assumes rain. If the weather tool actually says
"sunny, 2% chance of rain," a naive system might still agree with the
question's framing and tell the user to bring an umbrella anyway. A genuinely
reactive agent has to notice the contradiction and correct the user instead
of politely agreeing with a false premise.

This is still fully offline -- no API key needed, no live model call. The
"planning" logic (comparing the observation to the question's assumption) is
what you're writing by hand here, exactly like the Core-path exercise, so you
can see the shape of the re-planning branch before Session 4.2's real
tool-calling agent has to do this kind of reasoning itself.
"""

import json

# ---------------------------------------------------------------------------
# Tools (already complete -- do not modify)
# ---------------------------------------------------------------------------

WEATHER_DB = {
    "Chicago": {"tomorrow": "rain", "chance_of_rain_pct": 80},
    "Phoenix": {"tomorrow": "sunny", "chance_of_rain_pct": 2},
    "Seattle": {"tomorrow": "rain", "chance_of_rain_pct": 65},
}


def weather_lookup(city: str) -> dict:
    """A real (toy, offline) weather lookup tool. Returns an 'error' key
    if the city isn't in the database -- it does NOT raise an exception."""
    if city not in WEATHER_DB:
        return {"error": f"No data for {city}"}
    return WEATHER_DB[city]


# ---------------------------------------------------------------------------
# TODO 1: Detect whether the user's question assumes rain tomorrow
# ---------------------------------------------------------------------------

def contains_assumed_rain(question: str) -> bool:
    """
    Return True if the question's own wording assumes it will rain
    tomorrow (a simple keyword check is fine -- this is a toy example,
    not real NLP). Look for words like "rain" or "raining" in the
    lowercased question text.
    """
    # TODO: implement the keyword check described above.
    return False  # <-- replace this


# ---------------------------------------------------------------------------
# TODO 2: The reactive agent -- checks the observation against the
# question's assumption, and re-plans (corrects the user) if they conflict
# ---------------------------------------------------------------------------

def run_agent_loop_pro(city: str, question: str) -> dict:
    """
    Plan -> act -> observe for the "does the forecast match what the
    question assumed" task.

    Returns a dict with at least:
      - "weather": the raw weather_lookup result
      - "assumed_rain": bool, whether the question assumed rain
      - "final_answer": str, built using ONLY the weather tool's data

    Rules for final_answer:
      - If weather_lookup returned an "error" key: say no data is
        available, and that the assumption can't be confirmed or
        corrected.
      - Else, compare assumed_rain to whether weather["tomorrow"] == "rain":
          - If the question assumed rain but the forecast is NOT rain:
            explicitly correct the user, citing the real forecast and
            chance_of_rain_pct.
          - If the question did NOT assume rain but the forecast IS rain:
            flag that a rain forecast exists anyway, citing the real data.
          - If they match (both rain, or both not-rain): confirm the
            forecast lines up with the question, citing the real data.
    """
    scratchpad = {}

    # TODO: call weather_lookup(city) and store the result.
    scratchpad["weather"] = None  # <-- replace this

    # TODO: call contains_assumed_rain(question) and store the result.
    scratchpad["assumed_rain"] = None  # <-- replace this

    # TODO: build final_answer following the rules in the docstring above.
    final_answer = None  # <-- replace this

    scratchpad["final_answer"] = final_answer
    return scratchpad


# ---------------------------------------------------------------------------
# TODO 3: The rigid workflow -- always defers to the question's framing,
# without ever checking it against what the tool actually returned
# ---------------------------------------------------------------------------

def rigid_workflow_pro(city: str, question: str) -> str:
    """
    A FIXED sequence: looks up the weather (so it looks like it's using
    real data), but the reply is built purely from the question's own
    framing -- it never compares that framing to weather["tomorrow"].
    This is deliberately wrong on contradiction cases; you are not meant
    to "fix" it, only to observe how it fails.
    """
    weather = weather_lookup(city)  # called, but its result is never checked below

    # TODO: if contains_assumed_rain(question) is True, return a string
    # that tells the user to bring an umbrella "as the question mentioned"
    # -- WITHOUT looking at `weather` at all. Otherwise, return a string
    # saying no rain was mentioned so they probably won't need one.
    return None  # <-- replace this


if __name__ == "__main__":
    print("=== Consistent case: Chicago (question assumes rain, forecast IS rain) ===")
    q_chicago = "It's supposed to rain in Chicago tomorrow, should I bring an umbrella?"
    print("Reactive agent:", json.dumps(run_agent_loop_pro("Chicago", q_chicago), indent=2))
    print("Rigid workflow:", rigid_workflow_pro("Chicago", q_chicago))

    print("\n=== Contradiction case: Phoenix (question assumes rain, forecast is SUNNY) ===")
    q_phoenix = "It's supposed to rain in Phoenix tomorrow, should I bring an umbrella?"
    print("Reactive agent:", json.dumps(run_agent_loop_pro("Phoenix", q_phoenix), indent=2))
    print("Rigid workflow:", rigid_workflow_pro("Phoenix", q_phoenix))
    print("\nNotice: the rigid workflow gives the same wrong advice regardless of what")
    print("the tool actually returned -- it only ever reads the question, not the result.")
