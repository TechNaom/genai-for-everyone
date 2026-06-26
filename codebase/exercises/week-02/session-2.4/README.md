# Exercise — Session 2.4: Structured Outputs

## Resume Parser Prompt

**Goal:** Build a structured-extraction prompt that reliably returns parseable JSON, with defensive parsing around it that doesn't crash on imperfect output.

### Instructions

1. Copy `.env.example` (repo root) to `.env` and add your API key
2. Open `resume_parser.py` — three sample resume texts are provided, including one deliberately missing an email
3. Fill in the TODOs: the extraction prompt (with explicit schema) and the defensive parsing function
4. Run it: `python resume_parser.py`
5. Check: did the missing-email case return `null` rather than a guessed email? Did the parser handle any wrapper text gracefully rather than crashing?

### What "done well" looks like

Your defensive parser should never crash the program, even if the model's output is imperfect — it should either successfully extract the JSON (handling minor wrapper text) or clearly signal failure (e.g., return `None`), never raise an uncaught exception that takes down the whole script.

## Free/open path

Needs a real LLM API call — use any provider's free tier.

## Optional paid-API path

Works identically with any provider's SDK; if your provider offers a dedicated JSON/structured-output mode, this exercise is also a good place to try it and compare reliability against plain prompt instructions.

## Solution

See `codebase/solutions/week-02/session-2.4/` for a worked version with type validation included.
