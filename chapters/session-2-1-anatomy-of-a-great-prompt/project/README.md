# Session 2.1 Project: The Thoroughness Trap

The Pro path build for Session 2.1 — a diagnostic exercise built directly on
Part 4 of the lesson: a prompt can be long, well-formatted, and
detailed-*looking* while still missing the one critical piece of context that
actually matters. Length and apparent thoroughness don't guarantee
correctness.

## What you'll build

Four `CASES`, each with a prompt that reads as thorough on first glance (clear
task, decent length, reasonable tone/format guidance) — plus a short
`business_situation` paragraph revealing a real fact the prompt writer forgot
to include. For each case, you diagnose:

- `missing_critical_detail` — the ONE fact missing from the prompt
- `why_it_fails` — one sentence on what breaks downstream without it
- `fixed_prompt` — the original prompt, rewritten to actually include that fact

Example run (after completing all four):

```
1. Outage apology email
   Missing detail: The prompt never mentions the SLA service credit that
   Enterprise customers are contractually owed and are already receiving.
   Why it fails: Without that detail, the generated email apologizes but
   says nothing about the credit -- Enterprise customers who know their
   contract will notice the omission and may escalate a support ticket
   asking where their credit is, creating exactly the confusion the email
   was supposed to prevent.
   Fixed prompt: "Write an email to all customers explaining that our
   service had a 4-hour outage yesterday..."
```

## How to run it

```bash
python starter.py
```

No API key and no internet access needed — this is a pure diagnostic-reasoning
exercise. Fill in the three `None` fields for each case, then re-run to see
your diagnosis printed. Want to see one finished version first? Run
`python solution.py`.

## The habit this trains

Read each `thorough_prompt` on its own first — it should look genuinely
reasonable, even good. Then read the `business_situation` paragraph, which
contains the fact a real stakeholder in that scenario would already know. Your
job is to spot the gap between what the prompt says and what the situation
actually requires, exactly the way you'd have to on the job when a prompt
"looks fine" but the output still causes a real problem.

## Ideas to make it your own (optional stretch goals)

- Write a fifth case from your own work or coursework — a prompt that looked
  thorough to you at the time but was missing something you only noticed later.
- Run both the original `thorough_prompt` and your `fixed_prompt` through a
  real model (free tier of any provider) and compare how the outputs differ.

## Why this project matters

The most expensive prompt failures aren't the obviously lazy one-liners —
those get caught immediately because the output is obviously bad. The
expensive ones are prompts that look complete: good length, clear tone, solid
formatting, and one missing fact that nobody notices until it causes a real
support ticket, a compliance problem, or a production bug. Learning to
interrogate a "thorough-looking" prompt against the actual business situation,
not just against a length or formatting checklist, is the habit this project
is built to train.
