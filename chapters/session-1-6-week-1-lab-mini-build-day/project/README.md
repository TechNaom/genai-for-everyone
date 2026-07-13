# Week 1 Capstone Project — "Explain It To Me Simply"

This is Week 1's main deliverable: one complete, polished tool that touches
almost every idea from the week. Building it well is how you prove to yourself
that the five sessions actually connect — not as five separate facts, but as one
working artifact.

## What you'll build

A command-line tool that takes any topic and an audience level and produces an
explanation calibrated to that audience — a curious 10-year-old gets a different
explanation than a working professional, who gets a different one than a domain
expert wanting a quick refresher.

```
$ python solution.py --topic "black holes" --level beginner

--- Explanation of 'black holes' for: beginner ---

Imagine a drain in a bathtub, but so strong that even the water's *reflection*
gets pulled down and can't climb back out. A black hole is a spot in space that
pulls so hard that nothing nearby — not even light — can escape once it gets too
close. That's why it looks black: no light can bounce back to your eyes. It's one
of the most powerful things in the whole universe!
```

## What you built this week

Each earlier session shows up as a concrete design decision in this one tool:

- **Session 1.1 — predictive vs. generative:** every explanation is *freshly
  composed* for the specific topic and audience, not selected from a fixed list.
  This is a generative tool.
- **Session 1.2 — how LLMs work:** audience-appropriate explanations are a
  *context* problem — the system prompt shapes what the model considers when it
  generates.
- **Session 1.3 — the landscape:** you make a real, defensible model-tier choice.
  This is a well-scoped explanation task, so a smaller, faster tier is the right
  call — not a frontier-reasoning model.
- **Session 1.4 — your first application:** the literal foundation — system/user
  roles, constructing the request, parsing the response, failing gracefully.
- **Session 1.5 — hallucination & bias:** the honesty flag pairs every output
  with a "verify this" signal when the text contains specific, checkable claims.

## How to run it

```bash
# Offline self-check / demo (no API key needed):
python starter.py          # scaffold — reports which TODOs remain
python solution.py         # reference — prints the prompts + honesty flag

# Live explanation (needs the SDK + a key):
pip install anthropic python-dotenv
# copy .env.example (repo root) to .env and add your ANTHROPIC_API_KEY
python starter.py --topic "black holes" --level beginner
python solution.py --topic "black holes" --compare
```

Fill in the `# TODO` sections in `starter.py` to build your own version. The
six build steps are laid out in the lesson. Want to see one finished version
first? Run `python solution.py`.

## "Done well" vs. "done technically"

It's possible to build something that runs without errors and still misses the
point. If your three levels sound nearly identical — just shorter or longer —
that's a **system-prompt** problem, not a code problem. The quality of this tool
lives almost entirely in how specific each level's system prompt is: banned
jargon, required analogy types, assumed background. Vague instructions produce
vague differentiation.

## Ideas to make it your own (optional stretch goals)

- **Comparison mode (Pro path):** given one topic, generate all three levels in
  a single run and display them side by side (`--compare` in `solution.py` does
  this), then write a short paragraph critiquing your own prompts — where did
  the differentiation work, and where do two levels still sound too similar?
- Add a fourth audience level (e.g. "skeptical teenager") and see how hard it is
  to keep it genuinely distinct from the others.
- Make the honesty flag smarter — but notice how quickly a keyword heuristic
  stops scaling. That limitation is exactly what later weeks (grounding,
  retrieval, evaluation) address.

## Why this project matters

With just five ideas from one week, you can already build a complete, genuinely
useful GenAI tool — and, more importantly, you can *reason* about every design
decision inside it. That reasoning, especially the system-prompt judgment you
exercised here, becomes the explicit subject of Week 2: Prompt Engineering.
