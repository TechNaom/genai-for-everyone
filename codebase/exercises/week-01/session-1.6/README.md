# Exercise — Session 1.6: Week 1 Lab — Mini Build Day

## "Explain It To Me Simply" Tool

**Goal:** Integrate everything from Week 1 into one working tool — the predictive/generative distinction, context shaping, model choice, request/response mechanics, and honest hallucination-risk handling.

### Instructions

1. Copy `.env.example` (repo root) to `.env` and add your API key
2. Open `explainer.py` — the structure is scaffolded, with `# TODO` markers for the parts that integrate this week's concepts
3. Fill in the TODOs:
   - The three audience-level system prompts (Step 1-2 in the chapter)
   - The API call construction (Step 4)
   - The honesty-flag check (Step 5)
4. Run it: `python explainer.py --topic "black holes" --level beginner`
5. **Test across all three levels with the same topic** — this is the real test of whether your system prompts actually differentiate, or just produce similar output at different lengths

### What "done well" looks like

Run the same topic through all three levels. If the outputs sound meaningfully different — not just shorter/longer, but genuinely calibrated (different analogies, different assumed background, different vocabulary) — your system prompts are doing real work. If they sound suspiciously similar, revisit Part 2 of this session's chapter.

## Free/open path

Like Session 1.4, this needs a real LLM API call — use the free tier from any provider. If you don't have a key yet, trace through `codebase/solutions/week-01/session-1.6/explainer_solution.py` by hand to verify your understanding of the structure, even without running it live.

## Optional paid-API path

Works identically with any provider's SDK — the integration logic (roles, system prompt design, honesty flag) is provider-agnostic.

## Solution

See `codebase/solutions/week-01/session-1.6/explainer_solution.py` for a fully working reference version, including the comparison-mode extension from the Pro path.
