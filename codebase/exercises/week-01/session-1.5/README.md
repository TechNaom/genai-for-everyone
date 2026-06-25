# Exercise — Session 1.5: Limitations, Hallucination & Bias

## Hallucination Detection Exercise

**Goal:** Build the habit of spotting likely hallucinations by looking for the RIGHT signals — not confidence or fluency (both are useless signals), but specificity that can't be verified and suspiciously convenient details.

### Instructions

1. Open `hallucination_detector.py`
2. For each of the 10 statements in `STATEMENTS`, mark whether you believe it's likely accurate or likely fabricated, and write ONE sentence explaining the signal that led you there
3. Run the script to see your reasoning laid out, then compare against the solution file
4. Pay attention to the cases designed to trick you — some accurate-sounding statements are fabricated, and some statements that feel "suspiciously specific" are actually true

### What you'll notice

- Confidence and fluency tell you nothing — every statement here is written in the same confident tone
- Suspiciously precise, hard-to-verify details (an oddly specific page number, an oddly specific statistic) are a better red flag than vague statements
- Some of your intuitions will be wrong — that's the point. This exercise is humbling on purpose.

## Free/open path

No API calls needed — this is a pure reasoning and judgment exercise using a fixed set of provided statements. Runs entirely offline.

## Optional paid-API path

If you want to extend this exercise, you could generate your own batch of statements (some true, some deliberately fabricated) using any LLM API and a carefully designed prompt, then test your detection skills against your own set. Not required for the core exercise.

## Solution

See `codebase/solutions/week-01/session-1.5/` for the correct classification of each statement, with reasoning.
