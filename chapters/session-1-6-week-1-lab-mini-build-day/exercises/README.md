# Exercise — Session 1.6: Week 1 Lab — Mini Build Day

## "Explain It To Me Simply" Tool

**Goal:** Integrate everything from Week 1 into one working tool — the
predictive/generative distinction, context shaping, model choice,
request/response mechanics, and honest hallucination-risk handling.

## How to run

You need Python 3 installed. For a **live** explanation you also need the
`anthropic` SDK and an API key; without them you can still run the file's
offline self-check.

```bash
# Offline self-check (no API key needed) — reports unfilled TODOs and
# demonstrates the honesty flag, which is plain Python with no API call:
python starter.py

# Live explanation (needs the SDK + a key):
pip install anthropic python-dotenv
# copy .env.example (repo root) to .env and add your ANTHROPIC_API_KEY
python starter.py --topic "black holes" --level beginner
```

## Instructions

1. Open `starter.py` — the structure is scaffolded, with `# TODO` markers for
   the parts that integrate this week's concepts.
2. Fill in the TODOs:
   - The three audience-level system prompts (Steps 1–2 in the lesson)
   - The API call construction (Step 4)
   - The honesty-flag check in `main()` (Step 5)
3. Run it: `python starter.py --topic "black holes" --level beginner`
4. **Test across all three levels with the same topic** — this is the real test
   of whether your system prompts actually differentiate, or just produce
   similar output at different lengths.

### What "done well" looks like

Run the same topic through all three levels. If the outputs sound meaningfully
different — not just shorter/longer, but genuinely calibrated (different
analogies, different assumed background, different vocabulary) — your system
prompts are doing real work. If they sound suspiciously similar, revisit the
"done well vs. done technically" section of this session's lesson.

## Free/open path

Like Session 1.4, a live run needs a real LLM API call — use the free tier from
any provider. If you don't have a key yet, run `python starter.py` for the
offline self-check, and trace through `solution.py` by hand to verify your
understanding of the structure, even without running it live.

## Optional paid-API path

Works identically with any provider's SDK — the integration logic (roles,
system-prompt design, honesty flag) is provider-agnostic.

## Solution

See `solution.py` for a fully working reference version, including the
comparison-mode extension from the Pro path (`--compare` runs all three levels
side by side). Run `python solution.py` with no arguments for an offline demo.
