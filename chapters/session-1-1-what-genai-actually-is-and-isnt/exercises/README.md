# Session 1.1 Exercise: The AI Capability Map

**Goal:** Build the habit of classifying any "let's use AI" request *before*
writing a single line of code — the single most valuable instinct from this
chapter.

This exercise needs no API calls and no paid keys. It's a pure
classification-and-reasoning exercise: plain Python, runs anywhere.

## How to run

You'll need Python 3 installed. Check with:

```bash
python --version
```

Then run the starter file:

```bash
python starter.py
```

It prints a formatted table and flags any scenario you haven't filled in yet.

## The task

Open `starter.py`. For each of the 12 scenarios in the `SCENARIOS` list, fill
in three fields:

- `category` — `"predictive"` or `"generative"`
- `io_description` — one sentence describing input → output
- `example_tool` — a real tool/product that does this

The tell for each row: **could the output have been listed in advance
(predictive), or is it composed fresh (generative)?**

Run the script again after each edit — it will show which scenarios are still
`None` and count how many remain.

## Checking your work

There's no automated grader — that's intentional. A few scenarios are
genuinely debatable at the edges (recommendation systems, for instance,
sometimes blend predictive scoring with generative explanation text). The goal
isn't perfect agreement with the reference; it's being able to **defend your
classification with the input→output framing.**

Compare your reasoning against `solution.py` (run it with
`python solution.py`) once you've made a genuine attempt.
