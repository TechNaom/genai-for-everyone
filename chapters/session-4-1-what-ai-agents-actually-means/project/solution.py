"""
Session 4.1 Project — Pro Path — REFERENCE SOLUTION
======================================================
This solution is verified to run end-to-end. See README.md for the
expected output and what to look for.
"""

import json

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

WEATHER_DB = {
    "Chicago": {"tomorrow": "rain", "chance_of_rain_pct": 80},
    "Phoenix": {"tomorrow": "sunny", "chance_of_rain_pct": 2},
    "Seattle": {"tomorrow": "rain", "chance_of_rain_pct": 65},
}


def weather_lookup(city: str) -> dict:
    """A real (toy, offline) weather lookup tool."""
    if city not in WEATHER_DB:
        return {"error": f"No data for {city}"}
    return WEATHER_DB[city]


# ---------------------------------------------------------------------------
# TODO 1, solved
# ---------------------------------------------------------------------------

def contains_assumed_rain(question: str) -> bool:
    q = question.lower()
    return "rain" in q or "raining" in q


# ---------------------------------------------------------------------------
# TODO 2, solved -- the reactive agent
# ---------------------------------------------------------------------------

def run_agent_loop_pro(city: str, question: str) -> dict:
    scratchpad = {}

    weather = weather_lookup(city)
    scratchpad["weather"] = weather

    assumed_rain = contains_assumed_rain(question)
    scratchpad["assumed_rain"] = assumed_rain

    if "error" in weather:
        final_answer = (
            f"No weather data is available for {city}, so I can't confirm "
            f"or correct the assumption in your question -- check a live "
            f"weather source."
        )
    else:
        actual_rain = weather["tomorrow"] == "rain"
        pct = weather["chance_of_rain_pct"]

        if assumed_rain and not actual_rain:
            final_answer = (
                f"Actually, tomorrow's forecast for {city} is "
                f"{weather['tomorrow']} with only a {pct}% chance of rain -- "
                f"the opposite of what your question assumed. You likely "
                f"won't need an umbrella."
            )
        elif not assumed_rain and actual_rain:
            final_answer = (
                f"Worth flagging: tomorrow's forecast for {city} is "
                f"actually rain ({pct}% chance), even though your question "
                f"didn't mention rain. You'll probably want an umbrella."
            )
        elif actual_rain:
            final_answer = (
                f"That matches the forecast -- {city} is expecting rain "
                f"tomorrow ({pct}% chance), so bring an umbrella."
            )
        else:
            final_answer = (
                f"That matches the forecast -- {city} isn't expecting rain "
                f"tomorrow ({pct}% chance), so you likely won't need one."
            )

    scratchpad["final_answer"] = final_answer
    return scratchpad


# ---------------------------------------------------------------------------
# TODO 3, solved -- the rigid workflow (intentionally wrong on contradiction)
# ---------------------------------------------------------------------------

def rigid_workflow_pro(city: str, question: str) -> str:
    weather = weather_lookup(city)  # called, but never actually checked below

    if contains_assumed_rain(question):
        return "Yes, as your question mentioned, tomorrow's rain means you'll want an umbrella."
    else:
        return "No rain mentioned, so you probably won't need an umbrella."


if __name__ == "__main__":
    print("=== Consistent case: Chicago (question assumes rain, forecast IS rain) ===")
    q_chicago = "It's supposed to rain in Chicago tomorrow, should I bring an umbrella?"
    result_chicago = run_agent_loop_pro("Chicago", q_chicago)
    print("Reactive agent:", json.dumps(result_chicago, indent=2))
    print("Rigid workflow:", rigid_workflow_pro("Chicago", q_chicago))
    assert "matches the forecast" in result_chicago["final_answer"]

    print("\n=== Contradiction case: Phoenix (question assumes rain, forecast is SUNNY) ===")
    q_phoenix = "It's supposed to rain in Phoenix tomorrow, should I bring an umbrella?"
    result_phoenix = run_agent_loop_pro("Phoenix", q_phoenix)
    print("Reactive agent:", json.dumps(result_phoenix, indent=2))
    rigid_phoenix = rigid_workflow_pro("Phoenix", q_phoenix)
    print("Rigid workflow:", rigid_phoenix)
    assert "Actually" in result_phoenix["final_answer"]
    assert "won't need an umbrella" in result_phoenix["final_answer"]
    assert "you'll want an umbrella" in rigid_phoenix  # rigid version is wrong here, on purpose

    print("\nNotice: the rigid workflow gives the same wrong advice regardless of what")
    print("the tool actually returned -- it only ever reads the question, not the result.")

    print("\n=== No-data case: Nowheresville ===")
    result_unknown = run_agent_loop_pro("Nowheresville", "Is it raining in Nowheresville tomorrow?")
    print("Reactive agent:", json.dumps(result_unknown, indent=2))
    assert "No weather data is available" in result_unknown["final_answer"]

    print("\n[ALL ASSERTIONS PASSED]")
