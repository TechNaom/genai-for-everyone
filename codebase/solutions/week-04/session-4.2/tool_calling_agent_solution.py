"""
Session 4.2 — Reference Solution
An LLM That Calls a Real Weather/Calculator Tool
===========================================================================

Try the exercise yourself first -- the value is in defining the tool
schemas carefully and implementing the loop logic, not in reading
someone else's implementation.

VERIFICATION NOTE: build_tool_schemas(), execute_tool(), and offline_test()
below are pure logic with no API dependency, and are fully tested with
no external calls required -- confirmed by actually running this file's
offline_test() in this environment. run_conversation() and run_full_demo()
require a live ANTHROPIC_API_KEY and were NOT run live in the environment
that wrote this solution (no key was available there) -- run them
yourself with your own key to see your own live output, which may vary
between runs since tool-calling decisions are made by the model itself.
"""

import json


def calculator(expression: str) -> float:
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
    if city not in WEATHER_DB:
        return {"error": f"No data for {city}"}
    return WEATHER_DB[city]


def build_tool_schemas() -> list:
    """Tool name/description/input_schema definitions for the Anthropic API."""
    return [
        {
            "name": "calculator",
            "description": (
                "Evaluates a safe arithmetic expression and returns a "
                "number. Use this whenever the user asks a question that "
                "requires computing a total, a sum, a product, or any "
                "other arithmetic result -- for example, computing the "
                "total cost of multiple items at a given price."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A safe arithmetic expression, e.g. '3 * 14.50'",
                    }
                },
                "required": ["expression"],
            },
        },
        {
            "name": "weather_lookup",
            "description": (
                "Looks up tomorrow's weather forecast for a specific "
                "city, including whether it will rain and the chance of "
                "rain as a percentage. Use this whenever the user asks "
                "about weather conditions, temperature, rain, or whether "
                "they'll need an umbrella."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'Chicago'",
                    }
                },
                "required": ["city"],
            },
        },
    ]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Dispatch a tool_use request to the correct real function."""
    if tool_name == "calculator":
        try:
            result = calculator(tool_input["expression"])
            return json.dumps({"result": result})
        except ValueError as e:
            return json.dumps({"error": str(e)})

    elif tool_name == "weather_lookup":
        result = weather_lookup(tool_input["city"])
        return json.dumps(result)

    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


def offline_test():
    print("--- Testing build_tool_schemas() ---")
    schemas = build_tool_schemas()
    assert len(schemas) == 2, f"Expected 2 tool schemas, got {len(schemas)}"
    names = {s["name"] for s in schemas}
    assert names == {"calculator", "weather_lookup"}, f"Unexpected tool names: {names}"
    for s in schemas:
        assert "description" in s and len(s["description"]) > 10
        assert "input_schema" in s and "properties" in s["input_schema"]
    print("build_tool_schemas() looks correct.\n")

    print("--- Testing execute_tool() ---")
    calc_result = execute_tool("calculator", {"expression": "3 * 14.5"})
    print(f"calculator result: {calc_result}")
    assert "43.5" in calc_result

    weather_result = execute_tool("weather_lookup", {"city": "Chicago"})
    print(f"weather_lookup result: {weather_result}")
    assert "rain" in weather_result

    missing_city_result = execute_tool("weather_lookup", {"city": "Miami"})
    print(f"weather_lookup (unknown city) result: {missing_city_result}")
    assert "error" in missing_city_result.lower() or "No data" in missing_city_result

    bad_expr_result = execute_tool("calculator", {"expression": "import os"})
    print(f"calculator (invalid input) result: {bad_expr_result}")
    assert "error" in bad_expr_result.lower() or "invalid" in bad_expr_result.lower()

    print("execute_tool() looks correct (including error-handling cases).\n")
    print("All offline tests passed.")


def run_conversation(user_message: str, max_rounds: int = 5) -> str:
    """The full tool-calling loop: send, check stop_reason, execute, repeat."""
    import anthropic

    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]
    tools = build_tool_schemas()

    for _ in range(max_rounds):
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return "(model finished with no text content)"

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result_str = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_str,
                })

        messages.append({"role": "user", "content": tool_results})

    return "(stopped after max_rounds without a final answer -- possible loop)"


TEST_QUESTIONS = [
    "What's 3 umbrellas at $14.50 each, and will I need one tomorrow in Chicago?",
    "Will it rain tomorrow in Phoenix?",
    "What's 127 times 38?",
    "Should I bring an umbrella tomorrow in Miami?",  # city not in the DB
]


def run_full_demo():
    for question in TEST_QUESTIONS:
        print(f"\n{'=' * 70}")
        print(f"Q: {question}")
        answer = run_conversation(question)
        print(f"\nA: {answer}")


# ---------------------------------------------------------------------------
# Pro path notes
# ---------------------------------------------------------------------------

PRO_PATH_NOTES = """
Pro path notes:

Adding a third, deliberately ambiguous tool is most useful when its
description overlaps with one of the existing two in some plausible
reading. For example, a "unit_converter" tool ("converts a number from
one unit to another, e.g. miles to kilometers or Fahrenheit to Celsius")
could plausibly be confused with calculator for a question like "what's
68 degrees Fahrenheit in Celsius" -- a pure arithmetic operation that a
human might also describe as a "conversion." Running that exact
question through a three-tool setup and watching which tool actually
gets called is a genuine test of whether your descriptions are precise
enough to disambiguate, or whether the model has to guess.

If the model picks the "wrong" tool (or hesitates, or tries both),
that's not a model failure to fix by changing the model -- it's a
specification gap to fix by changing the tool descriptions, exactly as
the session described. Tightening calculator's description to
explicitly exclude unit conversions ("for arithmetic only -- not for
unit conversions between different measurement systems") and tightening
unit_converter's description to explicitly claim that category back is
usually enough to resolve a genuine boundary case like this. The
verification step matters as much as the fix: rerun the same ambiguous
question afterward and confirm the tool choice actually changed, rather
than assuming the new wording worked.
"""


if __name__ == "__main__":
    offline_test()
    print("\n" + "=" * 70)
    print("Now attempting the full tool-calling loop (requires ANTHROPIC_API_KEY)...")
    print("=" * 70)
    run_full_demo()
    print(PRO_PATH_NOTES)
