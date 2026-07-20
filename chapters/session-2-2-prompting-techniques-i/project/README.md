# Session 2.2 Project: Fix the Zero-Shot Triage Classifier

The Pro-path build for Session 2.2 — the extended version of the lesson's
central idea, applied to a harder, more realistic failure than the exercise's
support-ticket classifier.

## What you'll build

You're handed a zero-shot prompt that classifies internal engineering tickets
into a company-specific priority scheme: `P0-Critical`, `P1-High`,
`P2-Normal`, `P3-Low`. It fails inconsistently — not because the instruction
is unclear, but because "how urgent is this, really?" is exactly the kind of
judgment call a zero-shot prompt can't reliably infer without seeing worked
examples of where *this specific company* draws the line (is a payment
webhook that occasionally drops events a P0 data-integrity risk, or just an
annoying P2 bug? Is a 3-second-slower dashboard a P1 or a P3?).

You'll score the zero-shot version against 6 held-out tickets with known
correct labels, convert it to a few-shot prompt with genuinely boundary-case
examples, re-score, and confirm the fix is real — the score should visibly
improve, not just look better on easy cases.

## Example run (after both TODOs are filled in)

```
--- Zero-shot ---
Ticket                                                        Expected     Got          Match
-----------------------------------------------------------------------------------------------
Production login endpoint is returning 500 errors for all... P0-Critical  P0-Critical  yes
Add a dark mode toggle to the settings page                  P3-Low       P2-Normal    no
Search results take ~3s to load during peak hours, used t... P1-High      P2-Normal    no
Typo in the footer copyright year                             P3-Low       P3-Low       yes
Payment webhook occasionally drops events, causing a few m... P0-Critical  P2-Normal    no
Could we get a CSV export button on the reports page?         P3-Low       P3-Low       yes

--- Few-shot ---
Ticket                                                        Expected     Got          Match
-----------------------------------------------------------------------------------------------
Production login endpoint is returning 500 errors for all... P0-Critical  P0-Critical  yes
Add a dark mode toggle to the settings page                  P3-Low       P3-Low       yes
Search results take ~3s to load during peak hours, used t... P1-High      P1-High      yes
Typo in the footer copyright year                             P3-Low       P3-Low       yes
Payment webhook occasionally drops events, causing a few m... P0-Critical  P0-Critical  yes
Could we get a CSV export button on the reports page?         P3-Low       P3-Low       yes

Zero-shot: 3/6 correct
Few-shot:  6/6 correct
```

(Exact scores can vary run to run — LLM outputs aren't perfectly
deterministic. The direction of the improvement is the point, not the exact
numbers.)

## How to run it

```bash
pip install anthropic python-dotenv
# copy .env.example (repo root) to .env and add your ANTHROPIC_API_KEY
python starter.py
```

## What to build

Fill in the two `# TODO` sections in `starter.py`:

- **TODO 1** — `FEW_SHOT_PROMPT_TEMPLATE`: convert the zero-shot prompt into a
  few-shot one. Add 3–4 worked `Ticket: ... / Priority: ...` examples covering
  each priority level, including at least one genuinely tricky boundary case.
  Don't reuse the exact `TEST_TICKETS` as your examples — that's memorization,
  not a fix.
- **TODO 2** — `score()`: for each `(ticket, expected)` pair, classify the
  ticket with the given prompt template, compare the result to `expected`,
  print a row, and return the count correct.
- **TODO 3** — in `run()`, print a one-line takeaway comparing the two scores.

Want to see one finished version first? Run `python solution.py`.

## Ideas to make it your own (optional stretch goals)

- Add a role prompt on top of the few-shot examples ("You are a meticulous
  on-call engineering triage lead...") and see if it changes the score.
- Add a genuinely ambiguous ticket of your own and see which tier the model
  picks — then decide if you agree, and if not, what example would fix it.
- Track *which* tickets fail, not just the count, and look for a pattern in
  what kind of boundary case still trips up the few-shot version.

## Why this project matters

This is the exact shape of a real prompt-debugging session: a prompt that
"mostly works," a handful of production examples where it doesn't, and the
diagnostic question that actually matters — not "is the instruction clear
enough?" but "did I ever show the model where this specific line gets drawn?"
Converting a failing zero-shot prompt into a working few-shot one, and proving
the fix with a real before/after score, is a skill you'll use constantly once
you're shipping AI features that touch company-specific rules.
