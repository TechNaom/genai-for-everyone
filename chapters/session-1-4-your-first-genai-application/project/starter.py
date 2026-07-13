"""
Project (Pro path) — Session 1.4: Debug the Forgetful Chatbot

This script has the EXACT "forgetful" bug described in the lesson (Part 4):
it works for the first exchange, but a follow-up question like
"can you make that shorter?" confuses it — the model replies as if it has
no idea what "that" refers to.

Your job:
  1. Diagnose the bug FROM THE CODE ALONE (don't just watch it fail).
     Read the loop below carefully — what does it send to the model on
     each turn, and what does it leave out?
  2. Fix it so conversation history is maintained across turns.
  3. Add a NEW feature: a '/reset' command that clears the conversation
     history WITHOUT exiting the program — testing whether you understand
     exactly what the history list represents and when it's safe to clear.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python starter.py
Type 'quit' to exit.
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

SYSTEM_PROMPT = (
    "You are a friendly, concise assistant. Keep answers short unless the "
    "user asks for more detail."
)

MODEL_NAME = "claude-haiku-4-5-20251001"


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found in your environment.")
        print("Copy .env.example to .env and add your key, then try again.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def main():
    client = get_client()

    print("Chatbot ready. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            break

        # --- THE BUG IS HERE ---
        # Each turn builds a brand-new one-message list from scratch, so the
        # model never receives anything said earlier in the conversation.
        # From its perspective, every message arrives standalone and
        # contextless. (See lesson Part 4 for exactly why this "forgets".)
        messages = [{"role": "user", "content": user_input}]

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=messages,
        )

        assistant_reply = response.content[0].text
        print(f"Bot: {assistant_reply}\n")

        # Note: nothing is ever remembered between turns above. There is no
        # running history list at all — that's the bug you need to fix, and
        # then the '/reset' command you need to add depends on there being
        # one to clear.


if __name__ == "__main__":
    main()
