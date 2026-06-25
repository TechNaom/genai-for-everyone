# Exercise — Session 2.3: Prompting Techniques II

## Multi-Step Reasoning Prompt

**Goal:** Compare a direct prompt against a chain-of-thought prompt on a real multi-step business problem, and actually check whether the reasoning trail holds up — not just whether the final number looks plausible.

### Instructions

1. Copy `.env.example` (repo root) to `.env` and add your API key
2. Open `reasoning_compare.py` — a multi-step staffing/cost problem is provided
3. Fill in the TODOs: write the direct prompt and the chain-of-thought version
4. Run it: `python reasoning_compare.py`
5. Manually verify the correct answer yourself (work it out on paper or with a calculator), then check: did the direct prompt get it right? Did the chain-of-thought version? If they differ, look at WHERE in the reasoning trail (if shown) things went right or wrong.

### What "done well" looks like

This exercise is most valuable if you genuinely check the math yourself rather than trusting either output by default — that's the whole point of Session 1.5 and this chapter's "honest limit" discussion.

## Free/open path

Needs a real LLM API call — use any provider's free tier.

## Optional paid-API path

Works identically with any provider's SDK.

## Solution

See `codebase/solutions/week-02/session-2.3/` for a worked version with the correct answer computed independently, for comparison.
