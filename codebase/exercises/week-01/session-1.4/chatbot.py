"""
Exercise — Session 1.4: Your First GenAI Application

Working CLI Chatbot.

Fill in the TODOs to build a chatbot that correctly maintains conversation
history across turns. Test it by asking a follow-up question that only
makes sense in light of the previous answer (e.g. "summarize the solar
system" then "now do that in one sentence").

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python chatbot.py
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

MODEL_NAME = "claude-haiku-4-5-20251001"  # a fast, low-cost model is plenty for this exercise


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found in your environment.")
        print("Copy .env.example to .env and add your key, then try again.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def main():
    client = get_client()

    # This list IS the conversation's memory. Nothing outside this list
    # is "remembered" by the model between turns — see Session 1.4's
    # chapter, Part 2, for why this matters.
    conversation_history = []

    print("Chatbot ready. Type 'quit' to exit, '/reset' to clear history.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "quit":
            break

        if user_input == "/reset":
            # TODO: clear the conversation history here.
            # Think about exactly what "clearing history" means in terms
            # of this list — what should it look like right after reset?
            print("(history cleared)\n")
            continue

        # TODO 1: Append the user's message to conversation_history.
        # Each entry should be a dict with "role" and "content" keys,
        # matching the format described in this session's chapter, Part 1.
        # e.g. {"role": "user", "content": user_input}

        # TODO 2: Send the request to the model.
        # You need to pass:
        #   - model=MODEL_NAME
        #   - max_tokens=500
        #   - system=SYSTEM_PROMPT
        #   - messages=conversation_history   <-- the ENTIRE history, not just this turn
        # response = client.messages.create(...)

        # TODO 3: Extract the text from the response.
        # The generated text is at response.content[0].text
        # assistant_reply = ...

        # TODO 4: Print the assistant's reply.
        # print(f"Bot: {assistant_reply}\n")

        # TODO 5: Append the assistant's reply to conversation_history too.
        # This is the step beginners most often forget — without it, the
        # model's own previous answers are invisible on the NEXT turn.
        # e.g. {"role": "assistant", "content": assistant_reply}

        pass  # remove this once your TODOs are filled in


if __name__ == "__main__":
    main()
