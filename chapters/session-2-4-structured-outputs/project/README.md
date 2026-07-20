# Session 2.4 Project: Structured Output Regression Guard

The Pro path build for Session 2.4 — you've diagnosed a real failure
pattern in the resume-parsing prompt from the lesson (a non-standard date
range causing `years_experience` to come back as a string instead of a
number), and now you're building the check that catches it automatically
in the future, rather than relying on someone noticing it by eye.

## What you'll build

A small, fully offline regression suite. `FIXTURES` holds three *recorded*
raw model outputs — as if captured from earlier real API calls against the
Session 2.4 extraction prompt:

1. A clean output from a standard resume.
2. An output wrapped in conversational preamble text ("Sure, here is the
   JSON:...").
3. The known regression: a resume that listed a date range ("Jan 2019 -
   Present") instead of a plain duration, which caused the model to echo
   the range back as a string in `years_experience` instead of computing a
   number.

Your job is to build the suite that runs all three through defensive
parsing and schema validation, and reports which ones pass and which fail
— specifically catching case 3 by its wrong type, not by any special-casing.

Example run (against the reference solution):

```
--- clean output, standard resume ---
  PASS -- {'name': 'Jane Martinez', 'email': 'jane.martinez@email.com', 'years_experience': 6, 'skills': ['Python', 'AWS']}

--- wrapped output with conversational preamble ---
  PASS -- {'name': 'Aiden Cole', 'email': None, 'years_experience': 4, 'skills': ['Node.js', 'PostgreSQL']}

--- non-standard date range -> years_experience regression ---
  FAIL -- schema problems found:
    - field 'years_experience' has type str, expected one of ['int', 'float', 'NoneType']

2 of 3 fixtures passed.
At least one regression is present -- this is exactly the years_experience
type bug this guard exists to catch. Wire this suite into CI so a future
prompt edit that reintroduces it fails the build instead of shipping
silently.
```

Because everything runs against recorded fixtures, this needs **no API key
and no network access** — it's the exact shape of a fast, free, deterministic
check a real team would run on every commit.

## How to run it

```bash
python starter.py
```

Fill in the three `# TODO` sections. Want to see one finished version
first? Run `python solution.py`.

## What to build

- **TODO 1** — `parse_model_json`: the same defensive-parsing shape from
  the exercise — try a direct `json.loads()`, fall back to extracting the
  span between the first `{` and last `}`, and return `None` rather than
  raising if both fail.
- **TODO 2** — `validate_schema`: check each field in `EXPECTED_SCHEMA`
  against the parsed dict, reporting a missing field or a wrong type as a
  problem string. This is the specific check that catches the
  `years_experience` regression.
- **TODO 3** — `run_regression_suite`: loop over `FIXTURES`, parse and
  validate each one, print PASS/FAIL with details, and finish with a
  summary line of how many passed out of the total.

## Ideas to make it your own (optional stretch goals)

- Add a fourth fixture for a candidate whose email is missing but the model
  guessed one anyway (a hallucinated field, not a type bug) — you'll need a
  different kind of check to catch that one, since it's syntactically and
  type-correct but factually wrong.
- Have `run_regression_suite` return a nonzero process exit code when any
  fixture fails, so it behaves like a real CI check (`sys.exit(1)`).
- Write the corresponding *prompt* fix as a comment: what instruction would
  you add to `EXTRACTION_PROMPT_TEMPLATE` (from the lesson) to tell the
  model to convert a date range into a number of years, rather than echoing
  it back verbatim?

## Why this project matters

Diagnosing a bug once is easy to forget about. The habit that actually
protects a real GenAI feature in production is turning that diagnosis into
an automated check — a small, fast, offline test that fails loudly the
moment the same failure pattern reappears, instead of silently shipping a
string where your downstream code expected a number.
