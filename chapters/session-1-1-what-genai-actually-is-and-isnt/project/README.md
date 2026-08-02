# Session 1.1 Project: The AI Request Decoder

The exercise had you hand-classify twelve isolated scenarios. This project
turns that judgment into a small, reusable tool: feed it one vague
"let's use AI on this" request — already split into its sub-tasks — and it
decodes each one as predictive or generative and flags its rollout risk.

## What you'll build

A script holding one request and a list of its sub-project descriptions. For
each sub-project, `classify_subproject()` guesses predictive vs. generative
from keywords, and `risk_note()` attaches a one-line rollout warning based on
that category.

Example run:

```
=== AI Request Decoder ===
Request: "We need to put AI on our customer support backlog"

Sub-project                                        Category     Risk
----------------------------------------------------------------------------------------------------
Draft reply suggestions for agents to review       GENERATIVE   Medium risk: needs human review before it reaches a customer.
Auto-route tickets to the right team               PREDICTIVE   Lower risk: deterministic output, easy to audit.
Predict which tickets will escalate or churn       PREDICTIVE   Lower risk: deterministic output, easy to audit.
Summarize long multi-message threads for agents    GENERATIVE   Medium risk: needs human review before it reaches a customer.

Takeaway: this one sentence hides 2 generative and 2 predictive sub-project(s) -- each needs its
own data, evaluation approach, and rollout plan.
```

One sentence from a VP, four different engineering projects — the lesson's
"four hidden projects" example, decoded automatically instead of by hand.

## How to run it

```bash
python starter.py
```

Fill in the `# TODO` sections in `starter.py`. Want to see one finished
version first? Run `python solution.py`.

## Ideas to make it your own (optional stretch goals)

- Swap in a request from your own job or a news story and write its
  sub-projects by hand.
- Add a third category, `"unclear"`, for sub-tasks that genuinely blend both
  (recommendation systems are a good test case).
- Sort the printed rows so all the higher-risk generative sub-projects
  surface first.

## Why this project matters

This is the chapter's central habit, made mechanical: before writing any
code, split a vague "add AI" request into its real sub-projects and name each
one's category. Predictive and generative sub-tasks need different data,
different evaluation, and carry different rollout risk — catching that up
front is worth more than a week of building against the wrong target.
