"""
Session 4.1 Exercise — Core Path — REFERENCE SOLUTION
========================================================
This solution is verified to run end-to-end. See README.md for the
expected output and what to look for.
"""

import json

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def calculator(expression: str) -> float:
    """A real calculator tool. Only allows safe arithmetic characters."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        raise ValueError("Invalid characters in expression")
    return eval(expression)


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
# Reactive agent loop (TODO 1, solved)
# ---------------------------------------------------------------------------

def _a_or_an(n) -> str:
    """Returns 'an' if n's spoken form starts with a vowel sound, else 'a'.
    Good enough for the percentage numbers this tool ever produces."""
    return "an" if str(n).startswith(("8", "11", "18")) else "a"


def run_agent_loop(city: str, num_umbrellas: int = 3, price_each: float = 14.50):
    scratchpad = {}

    cost = calculator(f"{num_umbrellas} * {price_each}")
    scratchpad["total_cost"] = cost

    weather = weather_lookup(city)
    scratchpad["weather"] = weather

    if "error" in weather:
        final_answer = (
            f"{num_umbrellas} umbrellas at ${price_each:.2f} each = "
            f"${cost:.2f} total. No weather data is available for "
            f"{city}, so I can't tell you if you'll need an umbrella "
            f"tomorrow -- check a live weather source."
        )
    else:
        rain_chance = weather["chance_of_rain_pct"]
        needs_umbrella = rain_chance >= 50
        final_answer = (
            f"{num_umbrellas} umbrellas at ${price_each:.2f} each = "
            f"${cost:.2f} total. {city}'s forecast for tomorrow is "
            f"{weather['tomorrow']} with {_a_or_an(rain_chance)} {rain_chance}% chance of "
            f"rain, so "
            f"{'yes, you will likely need one' if needs_umbrella else 'you probably will not need one'}."
        )

    scratchpad["final_answer"] = final_answer
    return scratchpad


# ---------------------------------------------------------------------------
# Rigid workflow (TODO 2, solved -- intentionally fragile)
# ---------------------------------------------------------------------------

def rigid_workflow(city: str):
    cost = calculator("3 * 14.50")
    weather = weather_lookup(city)
    rain_chance = weather["chance_of_rain_pct"]  # crashes if "error" key present
    return f"{rain_chance}% chance of rain. Total cost: ${cost:.2f}"


if __name__ == "__main__":
    print("=== run_agent_loop on Chicago ===")
    result = run_agent_loop("Chicago")
    print(json.dumps(result, indent=2))
    assert result["total_cost"] == 43.5
    assert "yes, you will likely need one" in result["final_answer"]

    print("\n=== run_agent_loop on Nowheresville (not in DB) ===")
    result2 = run_agent_loop("Nowheresville")
    print(json.dumps(result2, indent=2))
    assert "No weather data is available" in result2["final_answer"]

    print("\n=== rigid_workflow on Chicago ===")
    print(rigid_workflow("Chicago"))

    print("\n=== rigid_workflow on Nowheresville (should crash) ===")
    try:
        print(rigid_workflow("Nowheresville"))
        print("UNEXPECTED: did not crash")
    except KeyError as e:
        print(f"CRASHED as expected: KeyError: {e}")

    print("\n[ALL ASSERTIONS PASSED]")
