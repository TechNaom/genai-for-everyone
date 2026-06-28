"""
Session 4.2 Exercise — An LLM That Calls a Real Weather/Calculator Tool
===========================================================================

Goal: take the same `calculator` and `weather_lookup` functions from
Session 4.1 -- already real, already tested -- and wire them up to an
ACTUAL LLM via the Anthropic API's tool-use feature. Instead of a
scripted policy standing in for the model's decisions (Session 4.1),
the model itself decides whether a question needs a tool, which one,
and with what arguments.

REQUIRES A REAL API KEY TO RUN END TO END
-------------------------------------------
There's no meaningful offline substitute for "does the model decide to
call a tool" -- that decision is the entire point of this exercise.
To run it:

    export ANTHROPIC_API_KEY=your-key-here
    pip install anthropic --break-system-packages
    python3 tool_calling_agent.py

If you don't have a key yet, you can still do real work offline:
`build_tool_schemas()` and the tool-execution dispatch logic in
`execute_tool()` are pure logic with no API dependency, and
`offline_test()` validates both without needing any API access. Get
those right first.

WHAT YOU NEED TO BUILD
-----------------------
1. build_tool_schemas()   -- TODO: define the tools' name/description/
                              input_schema for the Anthropic API
2. execute_tool()         -- TODO: dispatch a tool_use block to the
                              right real function and return the result
3. run_conversation()     -- TODO: the full tool-calling loop --
                              send message, check stop_reason, execute
                              tools, send results back, repeat
"""

import json
import os


# ---------------------------------------------------------------------------
# The real tools, unchanged from Session 4.1 -- do not modify
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
# TODO 1: Define the tool schemas for the Anthropic API
# ---------------------------------------------------------------------------

def build_tool_schemas() -> list:
    """
    TODO: Return a list of two tool definitions, formatted exactly as
    the Anthropic API expects: each one a dict with "name",
    "description", and "input_schema" keys.

    For "calculator":
      - name: "calculator"
      - description: explain what it does AND when to use it (e.g. for
        arithmetic questions, computing totals, etc.) -- be specific,
        per the session's discussion of why vague descriptions produce
        unreliable tool-calling behavior
      - input_schema: a JSON Schema object requiring one string field,
        "expression" (e.g. "3 * 14.50")

    For "weather_lookup":
      - name: "weather_lookup"
      - description: explain what it does AND when to use it (weather
        questions, whether an umbrella is needed, etc.)
      - input_schema: a JSON Schema object requiring one string field,
        "city"

    Example shape for one tool's input_schema:
        {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A safe arithmetic expression, e.g. '3 * 14.50'"
                }
            },
            "required": ["expression"]
        }
    """
    raise NotImplementedError("Fill in build_tool_schemas()")


# ---------------------------------------------------------------------------
# TODO 2: Execute whichever tool the model actually requested
# ---------------------------------------------------------------------------

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    TODO: Given a tool name and its input arguments (both come directly
    from the model's tool_use block), call the correct real function
    and return a JSON-serializable STRING result.

    - If tool_name == "calculator": call calculator(tool_input["expression"]).
      If it raises a ValueError (invalid characters), catch it and return
      a string describing the error instead of letting it crash --
      remember Session 4.1's lesson about tools reporting failure
      honestly rather than crashing silently.
    - If tool_name == "weather_lookup": call weather_lookup(tool_input["city"]).
    - For any other tool_name: return an error string saying the tool
      is unknown (this should never happen if your schemas are correct,
      but defensive code doesn't assume that).

    Use json.dumps(...) to turn dict/float results into a string before
    returning, since tool_result content must be a string.
    """
    raise NotImplementedError("Fill in execute_tool()")


def offline_test():
    """Tests build_tool_schemas() and execute_tool() with no API access."""
    print("--- Testing build_tool_schemas() ---")
    schemas = build_tool_schemas()
    assert len(schemas) == 2, f"Expected 2 tool schemas, got {len(schemas)}"
    names = {s["name"] for s in schemas}
    assert names == {"calculator", "weather_lookup"}, f"Unexpected tool names: {names}"
    for s in schemas:
        assert "description" in s and len(s["description"]) > 10, \
            f"Tool {s['name']} needs a real description, not a placeholder"
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


# ---------------------------------------------------------------------------
# TODO 3: The full tool-calling loop (requires ANTHROPIC_API_KEY)
# ---------------------------------------------------------------------------

def run_conversation(user_message: str, max_rounds: int = 5) -> str:
    """
    TODO: Implement the full tool-calling loop:

      1. Start `messages` as a list containing one user message with
         the given user_message content.
      2. Loop (up to max_rounds times, as a safety limit):
         a. Call client.messages.create(model="claude-haiku-4-5-20251001",
            max_tokens=1024, tools=build_tool_schemas(), messages=messages).
         b. If response.stop_reason != "tool_use": the model is done --
            return the text from response.content (the first text block).
         c. Otherwise: append the assistant's response.content to
            `messages`. Then, for EACH content block in response.content
            where block.type == "tool_use": call execute_tool(block.name,
            block.input), and build a tool_result dict:
                {"type": "tool_result", "tool_use_id": block.id,
                 "content": <the string result>}
         d. Append a new user message to `messages` whose content is the
            list of tool_result dicts you built, then continue the loop.
      3. If the loop runs out of rounds without stop_reason becoming
         something other than "tool_use", return a clear message saying
         so rather than silently returning nothing.

    Returns the model's final text answer as a string.
    """
    import anthropic

    client = anthropic.Anthropic()
    raise NotImplementedError("Fill in run_conversation()")


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


if __name__ == "__main__":
    offline_test()
    print("\n" + "=" * 70)
    print("Now attempting the full tool-calling loop (requires ANTHROPIC_API_KEY)...")
    print("=" * 70)
    run_full_demo()
