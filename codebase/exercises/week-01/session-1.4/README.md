# Exercise — Session 1.4: Your First GenAI Application

## Working CLI Chatbot

**Goal:** Build a real, working command-line chatbot that correctly maintains conversation history — so follow-up questions like "make that shorter" actually work, instead of confusing the model.

### Instructions

1. Copy `.env.example` (in the repo root) to `.env` and add your API key — see "Free/open path" below if you don't have one yet
2. Open `chatbot.py` and read through the comments — the structure is mostly built, but a few key lines are marked `# TODO`
3. Fill in the TODOs: constructing the message list correctly, and appending both the user message and the assistant's response after each turn
4. Run it: `python chatbot.py`
5. Test that memory actually works: ask something, then ask a follow-up that depends on the previous answer (e.g., "summarize the solar system" then "now do that in one sentence")

### What "done" looks like

If you ask a follow-up question that only makes sense in light of the previous answer, and the chatbot responds correctly (not confused, not asking "summarize what?"), your history-handling is correct.

## Free/open path

This specific exercise genuinely needs *some* LLM API to call — there's no way to build a real chatbot without one. The good news: every major provider offers a free tier or trial credits sufficient for this exercise many times over. Get a free API key from Anthropic's console (or any provider you prefer), add it to your `.env` file, and you won't be charged for the small number of test messages this exercise involves.

If you genuinely cannot get any API key right now, read `codebase/solutions/week-01/session-1.4/chatbot_solution.py` and trace through the logic by hand instead — you won't get the hands-on feel, but you can still verify you understand exactly what each part of the history-handling code does.

## Optional paid-API path

If you already have a paid API key for any provider, this exercise works identically — just point the script at your provider's SDK (the example uses Anthropic's, but the conversation-history logic is the same regardless of provider).

## Solution

See `codebase/solutions/week-01/session-1.4/chatbot_solution.py` for a fully working reference version.
