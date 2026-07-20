# Session 2.5 Project: Three-Step Prompt Chain

The Pro-path build for Session 2.5 — a small, working demonstration of the
classify → extract → draft-reply chain from Part 4 of the lesson, where each
step's output feeds into the next and every intermediate step can be
inspected and logged independently.

## What you'll build

A `run_chain()` function that processes an incoming customer email through
three focused steps:

1. **Classify** — assign the email a fixed category (`shipping`, `billing`,
   `returns`, or `other`).
2. **Extract** — pull out any order numbers mentioned, as structured data.
3. **Draft** — write a short reply, using the category and extracted data
   from steps 1–2 as context.

Run with `verbose=True` and you'll see each step's formatted prompt and
output printed as it happens — the exact debuggability advantage chaining
provides over one large combined prompt: if the final reply is wrong, you can
check each step independently to find exactly where things went wrong.

Example run (`python solution.py`):

```
--- Step 1: classify -- prompt ---
Classify the category of this customer email as exactly
one of: "shipping", "billing", "returns", "other".
...
--- Step 1: classify -- output: shipping ---

--- Step 2: extract -- prompt ---
...
--- Step 2: extract -- output: {'order_numbers': ['ORD-77410'], 'dates': []} ---

--- Step 3: draft reply -- prompt ---
...
--- Step 3: draft reply -- output ---
Thanks for reaching out regarding order ORD-77410. We've logged this as a
shipping request and a member of our team will follow up shortly with an
update. We appreciate your patience.

=== Chain result ===
Category:  shipping
Extracted: {'order_numbers': ['ORD-77410'], 'dates': []}
Reply:     Thanks for reaching out regarding order ORD-77410. ...
```

## How to run it

No installation and no API key needed:

```bash
python starter.py
```

`simulate_model()` stands in for a real LLM call so the exercise runs
anywhere, offline, for free — the point is the **chain structure** (three
prompt templates, each with a documented job, each independently inspectable),
not live model output. Want to see one finished version first? Run
`python solution.py`.

## What to build

Fill in the three `# TODO` functions in `starter.py`:

- **TODO 1** — `classify_step`: format `CLASSIFY_TEMPLATE`, then use the
  simple keyword rule described in the comment to return a category.
- **TODO 2** — `extract_step`: format `EXTRACT_TEMPLATE`, then pull out any
  `ORD-`-prefixed tokens as order numbers.
- **TODO 3** — `draft_step`: format `DRAFT_REPLY_TEMPLATE` with the category
  and extracted data, then build a short reply string.

Each function should print its formatted prompt when `verbose=True` — that's
what makes the chain's intermediate steps inspectable.

## Ideas to make it your own (optional stretch goals)

- Swap `simulate_model()` for a real API call (same client pattern from
  Week 3) and let the model actually classify, extract, and draft.
- Add a fourth category and a corresponding keyword rule.
- Log each step's output to a list instead of just printing it, so you can
  write an automated check that the chain produced a non-empty reply for
  every sample email you try.

## Why this project matters

A single combined prompt trying to classify, extract, and draft all at once
is much harder to debug when something goes wrong — you'd have no way to tell
which part of the instruction the model failed to follow. This chain makes
that failure mode visible: every step has one job, one documented prompt, and
one inspectable output, which is exactly the shape of a real production
pipeline you'd build once a task has genuinely distinct sub-problems.
