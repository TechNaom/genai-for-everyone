"""
Session 4.1 Exercise — Core Path
==================================
Trace and break the plan-act-observe agent loop.

You won't write an LLM call in this exercise -- there's no live model API
in this sandbox, and more importantly, today's goal is to build the right
mental model of the LOOP STRUCTURE before you build a real tool-calling
agent next session (4.2).

Both tools below are real and actually execute. Your job is to:
  1. Complete the agent loop function so it runs both tools and combines
     their results into a grounded final answer (no invented numbers).
  2. Complete the REACTIVE version so it survives a tool failure that
     crashes the rigid version.
  3. Run both on a city that exists in the database and one that doesn't,
     and write down what you observe.
"""

import json

# ---------------------------------------------------------------------------
# Tools (already complete -- do not modify)
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
    """A real (toy, offline) weather lookup tool. Returns an 'error' key
    if the city isn't in the database -- it does NOT raise an exception."""
    if city not in WEATHER_DB:
        return {"error": f"No data for {city}"}
    return WEATHER_DB[city]


# ---------------------------------------------------------------------------
# TODO 1: Complete the plan-act-observe loop
# ---------------------------------------------------------------------------

def run_agent_loop(city: str, num_umbrellas: int = 3, price_each: float = 14.50):
    """
    Run the plan-act-observe loop for the umbrella/weather task.

    Returns a dict with at least:
      - "total_cost": float, the result of the calculator tool
      - "weather": dict, the result of the weather_lookup tool
      - "final_answer": str, a sentence combining both -- using ONLY
        values that came from the scratchpad (no invented numbers!)
    """
    scratchpad = {}

    # TODO: Call the calculator tool to compute num_umbrellas * price_each.
    # Store the result in scratchpad["total_cost"].
    # Hint: build the expression as a string, e.g. f"{num_umbrellas} * {price_each}"
    scratchpad["total_cost"] = None  # <-- replace this

    # TODO: Call weather_lookup(city) and store the result in
    # scratchpad["weather"].
    scratchpad["weather"] = None  # <-- replace this

    # TODO: Build a final_answer string using ONLY scratchpad values.
    # If scratchpad["weather"] contains an "error" key, your final_answer
    # should say data wasn't available -- do NOT try to read
    # chance_of_rain_pct in that case (that's the rigid-workflow bug
    # you're about to compare against in TODO 2).
    final_answer = None  # <-- replace this

    scratchpad["final_answer"] = final_answer
    return scratchpad


# ---------------------------------------------------------------------------
# TODO 2: Complete the rigid workflow (intentionally fragile -- this is
# the comparison point, not something to "fix" by adding error handling)
# ---------------------------------------------------------------------------

def rigid_workflow(city: str):
    """
    A FIXED sequence: always tries to read weather["chance_of_rain_pct"],
    no matter what weather_lookup returned. This is meant to crash on
    unknown cities -- that's the point of the comparison.
    """
    cost = calculator("3 * 14.50")

    weather = weather_lookup(city)

    # TODO: Write the line that reads weather["chance_of_rain_pct"]
    # directly (no try/except, no .get() with a default -- we want to
    # see it fail loudly on a city with no data).
    rain_chance = None  # <-- replace this: weather[???]

    return f"{rain_chance}% chance of rain. Total cost: ${cost:.2f}"


if __name__ == "__main__":
    print("=== run_agent_loop on Chicago ===")
    result = run_agent_loop("Chicago")
    print(json.dumps(result, indent=2))

    print("\n=== run_agent_loop on Nowheresville (not in DB) ===")
    result2 = run_agent_loop("Nowheresville")
    print(json.dumps(result2, indent=2))

    print("\n=== rigid_workflow on Chicago ===")
    print(rigid_workflow("Chicago"))

    print("\n=== rigid_workflow on Nowheresville (should crash) ===")
    try:
        print(rigid_workflow("Nowheresville"))
    except Exception as e:
        print(f"CRASHED as expected: {type(e).__name__}: {e}")
