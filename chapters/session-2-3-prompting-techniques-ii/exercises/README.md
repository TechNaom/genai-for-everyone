# Session 2.3 Exercise: Multi-Step Reasoning Prompt

**Goal:** Compare a direct prompt against a chain-of-thought prompt on a real
multi-step business problem, and actually check whether the reasoning trail
holds up &mdash; not just whether the final number looks plausible.

## How to run

Install the dependencies:

```bash
pip install anthropic python-dotenv
```

Set your API key as an environment variable (or in a local, un-committed
`.env` file) before running anything:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

Then run the starter file:

```bash
python starter.py
```

## The task

Open `starter.py` &mdash; a multi-step call-center staffing/cost problem is
provided. Fill in the two `# TODO` sections:

- `direct_prompt` &mdash; the problem, asking only for the final answer, no
  reasoning instructions.
- `cot_prompt` &mdash; the *same* problem, with explicit step-by-step
  reasoning instructions appended. Keep the underlying problem identical
  between the two prompts, so any difference in the final answer is
  attributable to the technique, not to a reworded question.

Run it, then **manually verify the correct answer yourself** (work it out on
paper or with a calculator) before trusting either response. Check: did the
direct prompt get it right? Did the chain-of-thought version? If they differ,
look at *where* in the reasoning trail (if shown) things went right or wrong.

## What "done well" looks like

This exercise is most valuable if you genuinely check the math yourself
rather than trusting either output by default &mdash; that's the whole point
of Session 1.5's warning and this chapter's "honest limit" discussion.

## Checking your work

`solution.py` in this folder includes a worked, independently-verified
ground truth for this exact problem so you can compare both model responses
against a real answer, not just against each other. Run it with:

```bash
python solution.py
```
