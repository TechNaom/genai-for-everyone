"""
Session 2.4 Project: Structured Output Regression Guard -- reference solution.

Turns a diagnosed failure pattern (a non-standard date range causing
years_experience to come back as a string) into a small, reusable, fully
offline regression suite -- the exact shape of a check a real team would
wire into CI so this specific bug can never silently ship again.

Uses only the standard library. No API key, no network call, no cost.
"""

import json

FIXTURES = [
    {
        "label": "clean output, standard resume",
        "raw_output": (
            '{"name": "Jane Martinez", "email": "jane.martinez@email.com", '
            '"years_experience": 6, "skills": ["Python", "AWS"]}'
        ),
    },
    {
        "label": "wrapped output with conversational preamble",
        "raw_output": (
            "Sure, here is the JSON:\n"
            '{"name": "Aiden Cole", "email": null, "years_experience": 4, '
            '"skills": ["Node.js", "PostgreSQL"]}\n'
            "Let me know if you need anything else!"
        ),
    },
    {
        # The known regression: this resume listed a date RANGE
        # ("Jan 2019 - Present") rather than a duration in years. The
        # model echoed the range back verbatim instead of computing a
        # number, so years_experience comes back as a string.
        "label": "non-standard date range -> years_experience regression",
        "raw_output": (
            '{"name": "Priya Nair", "email": "priya.n@example.com", '
            '"years_experience": "Jan 2019 - Present", '
            '"skills": ["Java", "Kubernetes"]}'
        ),
    },
]

EXPECTED_SCHEMA = {
    "name": (str, type(None)),
    "email": (str, type(None)),
    "years_experience": (int, float, type(None)),
    "skills": (list,),
}


def parse_model_json(raw_text):
    """Defensive parsing: try direct parse, then try extracting {...} span."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_text[start:end + 1])
            except json.JSONDecodeError:
                pass
        return None


def validate_schema(parsed):
    """Returns a list of validation problems (empty list = valid)."""
    problems = []
    for field, expected_types in EXPECTED_SCHEMA.items():
        if field not in parsed:
            problems.append(f"missing field: {field}")
            continue
        if not isinstance(parsed[field], expected_types):
            problems.append(
                f"field '{field}' has type {type(parsed[field]).__name__}, "
                f"expected one of {[t.__name__ for t in expected_types]}"
            )
    return problems


def run_regression_suite():
    passed = 0
    for fixture in FIXTURES:
        label = fixture["label"]
        print(f"\n--- {label} ---")

        parsed = parse_model_json(fixture["raw_output"])
        if parsed is None:
            print("  PARSE FAILURE -- raw output did not contain valid JSON.")
            continue

        problems = validate_schema(parsed)
        if problems:
            print("  FAIL -- schema problems found:")
            for problem in problems:
                print(f"    - {problem}")
        else:
            print(f"  PASS -- {parsed}")
            passed += 1

    total = len(FIXTURES)
    print(f"\n{passed} of {total} fixtures passed.")
    if passed < total:
        print(
            "At least one regression is present -- this is exactly the "
            "years_experience type bug this guard exists to catch. Wire "
            "this suite into CI so a future prompt edit that reintroduces "
            "it fails the build instead of shipping silently."
        )


if __name__ == "__main__":
    run_regression_suite()
