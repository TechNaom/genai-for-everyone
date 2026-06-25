"""
Reference solution — Session 1.4: Your First GenAI Application

A fully working CLI chatbot with correct conversation-history handling.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python chatbot_solution.py
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

    # This list IS the conversation's memory. See Session 1.4's chapter,
    # Part 2 — nothing outside this list is "remembered" by the model.
    conversation_history = []

    print("Chatbot ready. Type 'quit' to exit, '/reset' to clear history.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            break

        if user_input == "/reset":
            conversation_history = []  # a fresh, empty list — the model "forgets" everything before this point
            print("(history cleared)\n")
            continue

        # Step 1: append the user's new message to history.
        conversation_history.append({"role": "user", "content": user_input})

        # Step 2: send the ENTIRE history (not just this turn) to the model.
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=conversation_history,
        )

        # Step 3: extract the generated text from the structured response.
        assistant_reply = response.content[0].text

        # Step 4: show it to the user.
        print(f"Bot: {assistant_reply}\n")

        # Step 5: append the assistant's reply to history too — this is the
        # step that's easy to forget, and skipping it is the #1 cause of a
        # chatbot that seems to "forget" what it itself just said.
        conversation_history.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    main()
