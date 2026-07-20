"""
Session 4.2 Project (Pro Path) — A Third, Deliberately Ambiguous Tool
===========================================================================

This builds on the core exercise (exercises/starter.py). If you haven't
completed that yet, do it first -- this file assumes build_tool_schemas(),
execute_tool(), and run_conversation() are already working, and gives you
those three as a solved starting point below.

THE CHALLENGE
--------------
Design and add a *third* tool with a deliberately ambiguous boundary
against one of the first two -- something where a reasonable question
could plausibly call either tool, or where a vague description would
make the model's choice unpredictable.

This file scaffolds a `unit_converter` tool as that third tool, because
a question like "What's 68 degrees Fahrenheit in Celsius?" is genuinely
ambiguous against `calculator` -- it's pure arithmetic, and a human might
describe it as either "a conversion" or "some math."

REQUIRES A REAL API KEY -- same as the core exercise:

    export ANTHROPIC_API_KEY=your-key-here
    pip install anthropic --break-system-packages
    python starter.py

WHAT YOU NEED TO BUILD
-----------------------
1. Fill in `unit_converter`'s tool schema in build_tool_schemas() below
   (TODO 1) -- start with something plausible but not yet
   disambiguated from calculator's description.
2. Add the dispatch case for "unit_converter" in execute_tool() (TODO 2).
3. Run run_ambiguity_test() and watch which tool the model picks for
   each ambiguous question.
4. If the model picks the "wrong" tool (or hesitates), rewrite
   `unit_converter`'s description (and/or calculator's) to resolve the
   ambiguity -- then RE-RUN the same questions and confirm the fix
   actually worked. Don't just assume new wording is clearer.
"""

import json


# ---------------------------------------------------------------------------
# The two tools from the core exercise, already solved -- do not modify
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# The new, third tool -- a real, working function. Do not modify the
# function itself; only its tool *description* is part of the challenge.
# ---------------------------------------------------------------------------

_CONVERSIONS = {
    ("fahrenheit", "celsius"): lambda v: (v - 32) * 5 / 9,
    ("celsius", "fahrenheit"): lambda v: v * 9 / 5 + 32,
    ("miles", "kilometers"): lambda v: v * 1.60934,
    ("kilometers", "miles"): lambda v: v / 1.60934,
}


def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """A real unit-conversion tool. Supports temperature (fahrenheit/celsius)
    and distance (miles/kilometers). Returns an 'error' key for any
    unsupported pair instead of raising."""
    key = (from_unit.lower(), to_unit.lower())
    if key not in _CONVERSIONS:
        return {"error": f"No conversion available from {from_unit} to {to_unit}"}
    return {"result": round(_CONVERSIONS[key](value), 2)}


# ---------------------------------------------------------------------------
# TODO 1: Add unit_converter's schema alongside the two solved schemas
# ---------------------------------------------------------------------------

def build_tool_schemas() -> list:
    calculator_schema = {
        "name": "calculator",
        "description": (
            "Evaluates a safe arithmetic expression and returns a "
            "number. Use this whenever the user asks a question that "
            "requires computing a total, a sum, a product, or any "
            "other arithmetic result."
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
    }

    weather_schema = {
        "name": "weather_lookup",
        "description": (
            "Looks up tomorrow's weather forecast for a specific city, "
            "including whether it will rain and the chance of rain as a "
            "percentage. Use this whenever the user asks about weather "
            "conditions, temperature, rain, or whether they'll need an "
            "umbrella."
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
    }

    # TODO: write unit_converter's schema. Start deliberately plain/vague
    # (e.g. "Converts a number from one unit to another") and see what
    # happens against calculator on a question like "What's 68 degrees
    # Fahrenheit in Celsius?" -- then tighten both descriptions until the
    # model's choice is reliable, and verify with the same question.
    unit_converter_schema = None  # TODO: replace with a real dict

    schemas = [calculator_schema, weather_schema]
    if unit_converter_schema is not None:
        schemas.append(unit_converter_schema)
    return schemas


# ---------------------------------------------------------------------------
# TODO 2: Add the dispatch case for "unit_converter"
# ---------------------------------------------------------------------------

def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "calculator":
        try:
            result = calculator(tool_input["expression"])
            return json.dumps({"result": result})
        except ValueError as e:
            return json.dumps({"error": str(e)})

    elif tool_name == "weather_lookup":
        result = weather_lookup(tool_input["city"])
        return json.dumps(result)

    # TODO: add an "elif tool_name == 'unit_converter':" branch here that
    # calls convert_units(tool_input["value"], tool_input["from_unit"],
    # tool_input["to_unit"]) and returns json.dumps(result).

    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


def run_conversation(user_message: str, max_rounds: int = 5) -> str:
    """The full tool-calling loop -- identical to the core exercise's
    working version. Not part of the Pro-path challenge; provided as-is."""
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


# ---------------------------------------------------------------------------
# Ambiguous test questions -- the whole point of this project
# ---------------------------------------------------------------------------

AMBIGUOUS_QUESTIONS = [
    "What's 68 degrees Fahrenheit in Celsius?",       # unit_converter vs. calculator
    "If it's 30 degrees Celsius, what's that times 2?",  # genuinely needs both
    "How many kilometers is 10 miles?",
]


def run_ambiguity_test():
    """Run each ambiguous question and print the final answer. To actually
    see WHICH tool got called, add a print(block.name) inside
    run_conversation()'s tool_use loop while you're debugging."""
    for question in AMBIGUOUS_QUESTIONS:
        print(f"\n{'=' * 70}")
        print(f"Q: {question}")
        answer = run_conversation(question)
        print(f"\nA: {answer}")


if __name__ == "__main__":
    print("Add unit_converter's schema and dispatch case (TODOs 1 and 2)")
    print("before running the ambiguity test.\n")
    run_ambiguity_test()
