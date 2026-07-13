# Session 1.4 Project: Debug the Forgetful Chatbot

A pro-path extended challenge. You're given a broken chatbot script with
the exact "forgetful" bug from the lesson (Part 4). You'll **diagnose the
bug from the code alone** (not just from watching it run), fix it, then add
a feature: a `/reset` command that clears conversation history without
exiting the program.

## What you'll build

Starting from a chatbot that works for the first exchange but loses all
context on any follow-up, you'll:

1. **Diagnose** — read the loop in `starter.py` and identify *why* it
   forgets. It builds a brand-new one-message list every turn, so the
   stateless model never receives anything said earlier.
2. **Fix** — keep a single running `conversation_history` list across
   turns: append the user's message, send the whole history, then append
   the assistant's reply too.
3. **Extend** — add a `/reset` command that rebinds the history to a fresh
   empty list without exiting. This tests whether you understand exactly
   *what* the history list represents and *when* it's safe to clear it.

## Example run (after your fix)

```
Chatbot ready. Type 'quit' to exit, '/reset' to clear history.

You: summarize the solar system
Bot: The solar system is the Sun and everything bound to it by gravity —
     eight planets, their moons, plus dwarf planets, asteroids, and comets.

You: now do that in one sentence
Bot: The solar system is the Sun and all the planets, moons, and smaller
     bodies orbiting it.

You: /reset
(history cleared — starting fresh)

You: do that in one sentence
Bot: Sure — do what in one sentence? I don't have anything to shorten yet.
```

That last exchange is the point: after `/reset`, the bot genuinely has no
memory of the earlier answer, exactly as designed.

## How to run it

```bash
pip install anthropic python-dotenv
python starter.py
```

## Setup — API key

Copy the repo's `.env.example` to `.env` and add `ANTHROPIC_API_KEY`. The
script loads it with `python-dotenv`. Every major provider's free tier
covers the few test messages here (see the exercise README's "Free/open
path"). No key handy? Read `solution.py` and trace the logic by hand.

## Ideas to make it your own (optional stretch goals)

- Add a `/history` command that prints how many turns are currently stored.
- Cap the history length so very long conversations don't grow unbounded.
- Give the bot a different persona by editing `SYSTEM_PROMPT`.

## Why this project matters

Maintaining and correctly clearing conversation state is the single most
common source of real chatbot bugs. The list-is-the-memory mental model you
practice here carries directly into every multi-turn GenAI app you'll build
later in this course. Want to see one finished version? Read `solution.py`.
