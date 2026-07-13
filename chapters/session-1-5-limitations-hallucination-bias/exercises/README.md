# Session 1.5 Exercises: Hallucination Detection

Build the habit of spotting likely hallucinations by looking for the RIGHT
signals — not confidence or fluency (both are useless signals), but
specificity that can't be verified and suspiciously convenient details.

## How to run

```bash
python starter.py
```

## The task

Open `starter.py`. For each of the 10 statements in `STATEMENTS`, fill in
two fields:

- `your_classification`: `"accurate"` or `"fabricated"`
- `your_reasoning`: ONE sentence explaining the signal that led you there

Then run the script to see your reasoning laid out, and compare against
`solution.py`.

## What you'll notice

- Confidence and fluency tell you nothing — every statement here is written
  in the same confident tone, true or false.
- Suspiciously precise, hard-to-verify details (an oddly specific page
  number, an oddly specific statistic attached to a named researcher) are a
  far better red flag than vague statements.
- Some of your intuitions will be wrong — that's the point. A few
  accurate-sounding statements are fabricated, and some statements that feel
  "suspiciously specific" are actually true. This exercise is humbling on
  purpose.

## Free / open path

No API calls needed — this is a pure reasoning and judgment exercise using a
fixed set of provided statements. Runs entirely offline.

## Optional paid-API path

If you want to extend this, generate your own batch of statements (some true,
some deliberately fabricated) using any LLM API and a carefully designed
prompt, then test your detection skills against your own set. Not required
for the core exercise.

## Checking your work

Run `python solution.py` for the correct classification of each statement,
with the reasoning signal that should have flagged it.
