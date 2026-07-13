"""
Project (Pro path) — Session 1.4: Debug the Forgetful Chatbot (SOLUTION)

The two things that make this the "fixed" version:

  1. THE BUG FIX — a single running `conversation_history` list is kept
     across turns. Every turn appends the user's new message, sends the
     ENTIRE history to the model (not just the latest turn), and then
     appends the assistant's reply too. That second append is the step
     beginners most often skip — without it, the model's own previous
     answers are invisible on the next turn.

  2. THE NEW FEATURE — a '/reset' command that clears the history WITHOUT
     exiting. "Clearing history" means rebinding the list to a fresh,
     empty list: the model then behaves as if the conversation started
     over, because the list IS the conversation's entire memory.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python solution.py
Type 'quit' to exit, '/reset' to clear conversation history.
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

    # THE FIX: one running list, created once, that survives across turns.
    # This list IS the conversation's memory — nothing outside it is
    # "remembered" by the stateless model between calls.
    conversation_history = []

    print("Chatbot ready. Type 'quit' to exit, '/reset' to clear history.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            break

        # THE NEW FEATURE: /reset wipes memory without leaving the program.
        if user_input == "/reset":
            conversation_history = []  # fresh, empty list — a clean slate
            print("(history cleared — starting fresh)\n")
            continue

        # Append the user's new message to the running history.
        conversation_history.append({"role": "user", "content": user_input})

        # Send the ENTIRE history so the model can see the whole conversation.
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )

        assistant_reply = response.content[0].text
        print(f"Bot: {assistant_reply}\n")

        # Append the assistant's reply too — the step that's easy to forget,
        # and skipping it is the #1 cause of a chatbot that seems to "forget"
        # what it itself just said one turn ago.
        conversation_history.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    main()
