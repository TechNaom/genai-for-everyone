# Session 1.5 Project: Hallucination Red-Flag Detector

You can't write code that knows whether a claim is TRUE — that would require
verifying it against the real world. What you CAN do is scan for the SHAPE of
a likely hallucination: the red-flag signals from the lesson (false precision,
an unverifiable named source, an oddly specific page citation, a suspiciously
precise number).

## What you'll build

A script that scores each statement for hallucination *risk* by counting how
many red-flag signals it trips — LOW / MEDIUM / HIGH.

Example run (the finished version):

```
2. [HIGH RISK, score 3] A 2019 Stanford study found that exactly 73.4% of
   remote workers report higher productivity, according to lead researcher
   Dr. Marina Chen.
     - FALSE PRECISION ('exactly' + a number)
     - UNVERIFIABLE NAMED SOURCE
     - SUSPICIOUSLY PRECISE NUMBER

3. [MEDIUM RISK, score 1] Mount Everest's summit sits at 8,848.86 meters
   above sea level.
     - SUSPICIOUSLY PRECISE NUMBER
```

## How to run it

```bash
python starter.py
```

The starter already runs — but until you implement the four `# TODO` detector
functions, every statement scores LOW. Want to see a finished version first?
Run `python solution.py`.

## The key insight this project teaches

Look at statement 3 in the finished output: Mount Everest, 8,848.86 m — that
figure is precise but **true**, and the detector flags it anyway. That is not
a bug; it is the whole lesson. A high score means **"verify this"**, never
**"this is false."** Confidence and fluency are useless signals, and even
shape-based signals only tell you *where to look* — never what's actually true.

## Ideas to make it your own (optional stretch goals)

- Add a new signal (e.g. a specific-year-plus-named-person pattern).
- Weight the signals instead of counting them equally.
- Feed in your own batch of statements — some true, some fabricated — and see
  where the heuristic gets fooled in both directions.

## Why this project matters

This is a miniature version of a real guardrail: a cheap, fast pre-filter that
routes risky-looking claims to human review or to a grounding/verification
step (RAG, Week 3). No such filter can determine truth on its own — the
structural fix for a factual claim is always verification, never a cleverer
guess.
