# Session 4.3 Project: Fact-Checking Agent (Pro Path)

## Overview

Build a **fact-checking agent** that:
1. Takes a claim as input
2. Plans searches to verify it
3. Finds supporting and contradicting evidence
4. Scores the claim's veracity (0–100%)
5. Outputs a brief report with a confidence score, citing conflicting sources
   when they exist

This is the less-scaffolded, harder sibling of the `exercises/` research
agent — it requires handling ambiguity and genuinely conflicting evidence,
not just gathering facts.

## Learning objectives

- Extend the plan → execute → stop loop to a task where "enough evidence" is
  a judgment call, not a fixed step count
- Practice deferring categorization: log raw evidence as it's gathered, and
  let the model do the supporting/contradicting/conflict split once it has
  full context, rather than guessing at each intermediate step
- Parse a structured JSON verdict out of a final model response

## Setup

1. Download `starter.py` below.
2. Install the SDK:
   ```bash
   pip install anthropic
   ```
3. Set your API key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

## Files in this project

- `starter.py` — skeleton with TODOs (pro path)
- `solution.py` — reference implementation

## The task

Open `starter.py`. Complete the three TODO sections:

1. **TODO 1 — the fact-checking plan prompt.** Ask the agent to break the
   claim into verifiable parts and plan searches for both supporting and
   contradicting evidence, without searching yet.
2. **TODO 2 — the evidence-gathering loop.** Same shape as the exercises/
   research agent's loop (extract tool calls, check the stopping condition,
   process each tool call), but here you should just log each raw
   `{query, result}` pair — resist the urge to bucket each result into
   "supporting" or "contradicting" as it comes in. A single simulated source
   in this exercise (see `SOURCES` in `starter.py`) can itself contain
   agreeing *and* disagreeing statements, so per-result categorization is
   fragile. Let the final judgment step do it once, with full context.
3. **TODO 3 — the final judgment.** Ask the model for one JSON object with
   `veracity_score`, `confidence`, `supporting_evidence`,
   `contradicting_evidence`, `conflicts`, and `reasoning`. Parse it (defensively
   — models occasionally wrap JSON in a sentence even when told not to) and
   build a `FactCheckResult` from the parsed fields.

## Testing your code

```bash
python3 starter.py
```

Test with claims like:
- `"GPT-4 was released in March 2023"` (verifiable, mostly consistent sources)
- `"Python is the most popular programming language"` (debatable — the
  simulated sources deliberately disagree depending on context)
- `"AI model training is free"` (false, and the simulated sources say so)

Expected behavior:
- The agent prints a plan before any searches.
- It searches for both supporting and contradicting angles, not just one.
- The final report includes a veracity score, a confidence score, and — for
  the "most popular language" claim especially — at least one noted conflict
  between sources.

## Troubleshooting

**Agent never mentions the conflicting sources:**
- Check your judgment prompt actually asks for a `conflicts` field, and that
  your plan/execution prompts told the agent to search for disagreement, not
  just confirmation.

**JSON parsing fails / `FactCheckResult` ends up with placeholder values:**
- Print `judgment_text` and inspect it — the model may have added a sentence
  before or after the JSON. `_extract_json` in `solution.py` handles this by
  slicing from the first `{` to the last `}` before calling `json.loads`.

**Agent runs all 8 iterations every time:**
- Same stopping-condition bug as the exercises/ agent — double-check you're
  filtering for `block.type == "tool_use"`, not just checking `if response.content`.

## Submission checklist

- [ ] Fact-checker completes without errors on all three test claims
- [ ] Output includes a plan, the searches performed, and a final JSON verdict
- [ ] At least one test claim surfaces a noted conflict between sources
- [ ] `veracity_score` and `confidence` are populated from the model's actual
      judgment, not left at the placeholder defaults

---

**Next:** Session 4.4 (Multi-Agent Patterns) — what happens when you run
multiple agents that work together or critique each other.
