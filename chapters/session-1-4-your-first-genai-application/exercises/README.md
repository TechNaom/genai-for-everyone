# Session 1.4 Exercises: Your First GenAI Application

## Working CLI Chatbot

**Goal:** Build a real, working command-line chatbot that correctly
maintains conversation history — so follow-up questions like "make that
shorter" actually work, instead of confusing the model.

These exercises use exactly what Session 1.4 covered: the three roles
(system / user / assistant), statelessness, and the request-response
cycle.

## How to run

```bash
pip install anthropic python-dotenv
python starter.py
```

## Setup — API key

This exercise genuinely needs *some* LLM API to call — there's no way to
build a real chatbot without one. Copy the repo's `.env.example` to `.env`
and add your key:

```
ANTHROPIC_API_KEY=your-key-here
```

The script loads it with `python-dotenv` (see `requirements.txt` for the
pinned versions). If no key is found, the script prints a friendly message
and exits rather than crashing.

## Free/open path

Every major provider offers a free tier or trial credits that easily cover
the handful of test messages this exercise involves. Get a free API key
from Anthropic's console (or any provider you prefer) and you won't be
charged. If you genuinely cannot get any key right now, read `solution.py`
and trace the history-handling logic by hand — you won't get the hands-on
feel, but you can still verify you understand what each line does.

## Task 1 — Append the user's message

Find `# TODO 1`. Append the user's input to `conversation_history` as a
dict with `"role"` and `"content"` keys, e.g.
`{"role": "user", "content": user_input}`.

## Task 2 — Send the whole history

Find `# TODO 2`. Call `client.messages.create(...)` passing `model`,
`max_tokens=500`, `system=SYSTEM_PROMPT`, and `messages=conversation_history`
— the **entire** history, not just this turn.

## Task 3 — Extract and show the reply

Find `# TODO 3` and `# TODO 4`. Pull the generated text from
`response.content[0].text` and print it.

## Task 4 — Append the assistant's reply (the step everyone forgets)

Find `# TODO 5`. Append `{"role": "assistant", "content": assistant_reply}`
to `conversation_history`. Skip this and the model can't see its own
previous answers on the next turn — the #1 cause of a "forgetful" chatbot.

## Debug the Code — the `/reset` command

Find the `/reset` branch. It's supposed to clear the conversation history
without exiting the program, but as written it only prints a message and
changes nothing. Fix it so history is actually wiped — think about exactly
what "clearing history" means in terms of the list, and what it should look
like right after a reset.

## What "done" looks like

Ask something, then ask a follow-up that only makes sense in light of the
previous answer (e.g. "summarize the solar system" then "now do that in one
sentence"). If the bot responds correctly — not confused, not asking
"summarize what?" — your history-handling is correct.

## Checking your work

Compare against `solution.py` (a fully working reference version).
