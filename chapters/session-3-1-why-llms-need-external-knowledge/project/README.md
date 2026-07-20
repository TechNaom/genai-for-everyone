# Session 3.1 Project: The Wrong-Direction Failure Report

The Pro path build for Session 3.1 — a diagnostic exercise built directly on
the lesson's core judgment call: knowing when RAG is the right tool and when
it isn't. The exercises worksheet asked you to make the *right* call on six
scenarios. This project asks the sharper question: what actually breaks when
someone makes the *wrong* call, in the opposite direction from the mistake
you'd expect?

## What you'll build

The same six scenarios from the exercises worksheet, each paired with its
correct call and the specific wrong-direction mistake to analyze:

- Scenarios 1, 3, 4, and 6 genuinely need RAG — for these, the wrong call is
  handling them with **prompting alone, no retrieval**.
- Scenarios 2 and 5 don't need RAG at all — for these, the wrong call is
  **building a full RAG pipeline anyway**.

For each scenario, fill in:

- `wrong_call` — one sentence on what the opposite-direction mistake looks
  like in practice (what someone actually builds or does instead of the
  right call)
- `failure_mode` — 2–3 sentences on what concretely breaks: who notices, how,
  and why it's bad — not just "it's wrong," the specific, realistic
  consequence
- `cost_of_the_mistake` — one sentence naming the type of cost (wasted
  engineering time, latency, a wrong answer shipped to a real user, a
  compliance risk, and so on)

Example run (after completing all six):

```
======================================================================
Scenario 1: A legal tech startup wants their AI assistant to answer
questions like 'What does Section 4.2 of our standard NDA template say
about confidentiality duration?' by quoting the exact clause.
Correct call: RAG
Wrong-direction mistake: handled with prompting alone, no retrieval
----------------------------------------------------------------------
  What the wrong call looks like: Someone writes a well-crafted prompt
  asking the model to 'quote Section 4.2 of our standard NDA template'
  and ships it without ever giving the model the actual template text.
  Failure mode:                   The model has never seen this
  company's specific NDA template -- it's private content, not public
  training data -- so it generates a plausible-sounding clause that
  resembles a typical confidentiality-duration clause but isn't the
  real one...
  Cost of the mistake:            A real legal/compliance risk --
  someone could act on a quoted clause that was never actually in the
  contract.
```

## How to run it

```bash
python3 starter.py
```

No API key and no internet access needed — this is a pure diagnostic-
reasoning exercise. Fill in the three `None` fields for each of the six
cases, then re-run to see your analysis printed. Want to see one finished
version first? Run `python3 solution.py`.

## The habit this trains

It's easy to memorize "these four scenarios need RAG, these two don't" as a
checklist. It's much more valuable — and much closer to what real GenAI
engineering judgment looks like — to be able to explain the *cost* of getting
it wrong in either direction. Skipping retrieval on a genuine RAG scenario
ships a confidently wrong answer to a real user. Building retrieval
infrastructure for a scenario that never needed it burns engineering time and
adds latency for no accuracy gain. Both are real mistakes engineers make on
the job, and being able to name the specific failure — not just "that's the
wrong call" — is what this project is built to train.

## Ideas to make it your own (optional stretch goals)

- Pick one scenario and sketch what the *fix* would look like in code or
  pseudocode once the wrong call has already shipped — how would you detect
  it in production before a customer does?
- Write a seventh scenario from your own work or coursework where you've
  seen (or could imagine) someone reach for RAG when they didn't need it, or
  skip it when they did — and analyze it the same way.

## Why this project matters

Session 3.1's real lesson isn't "here's what RAG is" — it's "here's how to
tell when you need it." That judgment only sharpens once you can articulate
the cost of getting it wrong in both directions, not just recite the right
answer. An engineer who can say "skipping retrieval here means a support bot
confidently misstates a return policy to a real customer" or "adding
retrieval here means burning latency and engineering time on a task the
model already does well" is demonstrating exactly the judgment real GenAI
work demands — and exactly what the rest of Week 3's engineering will assume
you already have.
