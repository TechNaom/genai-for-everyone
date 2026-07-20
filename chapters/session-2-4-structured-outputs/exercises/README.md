# Session 2.4 Exercise: Resume Parser Prompt

**Goal:** Build a structured-extraction prompt that reliably returns
parseable JSON, with defensive parsing around it that doesn't crash on
imperfect output.

## Setup — API key

This exercise genuinely needs *some* LLM API to call — there's no way to
build a real extraction prompt without one. Install the dependencies and
copy the repo's `.env.example` to `.env`, adding `ANTHROPIC_API_KEY=your-key-here`:

```bash
pip install anthropic python-dotenv
```

The script loads the key with `python-dotenv`; if no key is found it prints
a friendly message and exits rather than crashing. Every major provider
offers a free tier or trial credits that easily cover the handful of test
calls here. No key at all? Read `solution.py` and trace the prompt and the
parsing logic by hand — the reasoning is the point, not the API call itself.

## How to run

```bash
python starter.py
```

Three sample resume texts are provided, including one deliberately missing
an email — that's the case that tests whether your prompt returns `null`
honestly instead of guessing.

## The task

Open `starter.py`. Fill in two things:

1. **`EXTRACTION_PROMPT_TEMPLATE`** — the extraction prompt, following the
   pattern from the lesson. It needs an explicit JSON schema with types
   (`name`, `email`, `years_experience`, `skills`), an instruction to use
   `null`/empty for missing fields rather than guessing, and an instruction
   to return nothing but the JSON object — no preamble, no closing remark.
2. **`parse_model_json`** — defensive parsing. Try `json.loads()` directly
   first. If that fails, try extracting the span between the first `{` and
   the last `}` and parse that instead. If everything fails, return `None`
   rather than letting an exception crash the program.

## Checking your work

Run the script and check two things:

- Did Resume 2 (no email listed) come back with `email: null`, rather than
  a plausible-looking guessed address? That's the single most important
  thing to verify in this exercise — it's the difference between honest
  missing-data handling and a quiet hallucination.
- If you deliberately make the model's raw output messy (for example, by
  loosening the "no other text" instruction), does `parse_model_json` still
  recover the JSON instead of crashing?

There's no automated grader for prompt wording — that's intentional. Compare
your reasoning against `solution.py` (run it with `python solution.py`),
which also adds a `validate_schema` type-check step to catch the case where
JSON parses successfully but a field has the wrong type (e.g.
`"years_experience": "8 years"` instead of `8`).
