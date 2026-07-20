"""
Session 4.2 Project — Reference Solution (Pro Path)
A Third, Deliberately Ambiguous Tool
===========================================================================

Try the project yourself first -- the value is in watching the model
actually confuse two tools, then fixing the descriptions and verifying
the fix, not in reading someone else's finished descriptions.

VERIFICATION NOTE: run_conversation() and run_ambiguity_test() require
a live ANTHROPIC_API_KEY and were not run live in the environment that
wrote this solution (no key was available there) -- run them yourself
to see your own live output, which may vary between runs since
tool-calling decisions are made by the model itself.
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


def build_tool_schemas() -> list:
    """All three tool schemas. calculator and unit_converter's
    descriptions have been deliberately tightened to resolve the
    ambiguity between them -- see PRO_PATH_NOTES below for why."""
    return [
        {
            "name": "calculator",
            "description": (
                "Evaluates a safe arithmetic expression (addition, "
                "subtraction, multiplication, division) and returns a "
                "number. Use this for arithmetic ONLY -- totals, sums, "
                "products, and other plain arithmetic. Do NOT use this "
                "for converting a value between different measurement "
                "units (e.g. Fahrenheit to Celsius, miles to kilometers) "
                "-- use unit_converter for those instead, even though "
                "they also involve a numeric formula."
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
        {
            "name": "unit_converter",
            "description": (
                "Converts a numeric value from one measurement unit to "
                "another -- for example, Fahrenheit to Celsius, Celsius "
                "to Fahrenheit, miles to kilometers, or kilometers to "
                "miles. Use this whenever the user is asking to translate "
                "a quantity between two different measurement systems, "
                "even though the underlying operation involves numbers. "
                "Do NOT use calculator for unit conversions -- use this "
                "tool instead."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "The numeric value to convert, e.g. 68",
                    },
                    "from_unit": {
                        "type": "string",
                        "enum": ["fahrenheit", "celsius", "miles", "kilometers"],
                        "description": "The unit the value is currently in",
                    },
                    "to_unit": {
                        "type": "string",
                        "enum": ["fahrenheit", "celsius", "miles", "kilometers"],
                        "description": "The unit to convert the value into",
                    },
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        },
    ]


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

    elif tool_name == "unit_converter":
        result = convert_units(
            tool_input["value"], tool_input["from_unit"], tool_input["to_unit"]
        )
        return json.dumps(result)

    else:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


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
                print(f"  [tool call] {block.name}({block.input})")
                result_str = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_str,
                })

        messages.append({"role": "user", "content": tool_results})

    return "(stopped after max_rounds without a final answer -- possible loop)"


AMBIGUOUS_QUESTIONS = [
    "What's 68 degrees Fahrenheit in Celsius?",          # unit_converter vs. calculator
    "If it's 30 degrees Celsius, what's that times 2?",  # genuinely needs both, in sequence
    "How many kilometers is 10 miles?",
]


def run_ambiguity_test():
    for question in AMBIGUOUS_QUESTIONS:
        print(f"\n{'=' * 70}")
        print(f"Q: {question}")
        answer = run_conversation(question)
        print(f"\nA: {answer}")


PRO_PATH_NOTES = """
Pro path notes:

Adding a third, deliberately ambiguous tool is most useful when its
description overlaps with one of the existing two in some plausible
reading. Here, "unit_converter" ("converts a number from one unit to
another, e.g. miles to kilometers or Fahrenheit to Celsius") could
plausibly be confused with calculator for a question like "what's 68
degrees Fahrenheit in Celsius" -- a pure arithmetic operation that a
human might also describe as a "conversion." Running that exact
question through a three-tool setup and watching which tool actually
gets called is a genuine test of whether your descriptions are precise
enough to disambiguate, or whether the model has to guess.

If the model picks the "wrong" tool (or hesitates, or tries both),
that's not a model failure to fix by changing the model -- it's a
specification gap to fix by changing the tool descriptions, exactly as
the lesson described. Tightening calculator's description to explicitly
exclude unit conversions ("for arithmetic only -- not for unit
conversions between different measurement systems") and tightening
unit_converter's description to explicitly claim that category back
(as done above) is usually enough to resolve a genuine boundary case
like this. The verification step matters as much as the fix: rerun the
same ambiguous question afterward and confirm the tool choice actually
changed, rather than assuming the new wording worked because it reads
more clearly to you.
"""


if __name__ == "__main__":
    print("Now attempting the ambiguity test (requires ANTHROPIC_API_KEY)...")
    run_ambiguity_test()
    print(PRO_PATH_NOTES)
