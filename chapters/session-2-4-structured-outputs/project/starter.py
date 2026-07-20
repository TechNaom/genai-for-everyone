"""
Session 2.4 Project: Structured Output Regression Guard
See README.md in this folder for the full brief and an example run.

This is the takeaway build for Session 2.4's Pro path: you've diagnosed a
real failure pattern in a resume-parsing prompt (a non-standard date range
causing `years_experience` to come back as a string instead of a number),
and now you're building the regression guard that catches this
automatically in the future -- instead of relying on someone noticing it by
eye during a one-off test.

The three FIXTURES below are *recorded* raw model outputs -- as if captured
from earlier real API calls -- so this file runs entirely offline. No API
key, no network call, no cost. That's deliberate: a regression suite you
can run in seconds, with no external dependency, is exactly the kind of
check a real team would wire into CI.
"""

import json

# Recorded raw model outputs from three earlier real extraction calls,
# using the resume-parsing prompt from the Session 2.4 lesson.
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

# The schema the extraction prompt promises. A field's value must match one
# of its listed types, or the regression suite should flag it.
EXPECTED_SCHEMA = {
    "name": (str, type(None)),
    "email": (str, type(None)),
    "years_experience": (int, float, type(None)),
    "skills": (list,),
}


def parse_model_json(raw_text):
    """
    TODO 1: implement defensive parsing (same shape as the exercise).
    - Try json.loads() directly first.
    - If that fails, try extracting the span between the first '{' and the
      last '}' and parse that instead.
    - If everything fails, return None (don't let this crash the program).
    """
    raise NotImplementedError("Fill this in.")


def validate_schema(parsed):
    """
    TODO 2: return a list of validation problems (empty list = valid).
    For each field in EXPECTED_SCHEMA:
      - if the field is missing from `parsed`, add "missing field: <field>"
      - if the field's value isn't an instance of its expected type(s),
        add a message naming the field, its actual type, and what was
        expected (see the lesson's validate_schema for the exact format
        if you want to match it).
    This is the check that catches the years_experience regression: syntax-
    valid JSON with the wrong type in a field.
    """
    raise NotImplementedError("Fill this in.")


def run_regression_suite():
    """
    TODO 3: loop over FIXTURES. For each fixture:
      - parse raw_output with parse_model_json
      - if parsing failed (None), report a PARSE FAILURE for that label
      - otherwise, run validate_schema and report PASS (no problems) or
        FAIL (print the label and the list of problems)
    Finish by printing a one-line summary: how many fixtures passed out of
    the total. This function is what you'd wire into CI so a future prompt
    change that reintroduces the years_experience bug gets caught
    automatically, rather than silently shipping.
    """
    raise NotImplementedError("Fill this in.")


if __name__ == "__main__":
    run_regression_suite()
