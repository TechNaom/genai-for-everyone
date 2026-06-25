"""
Exercise — Session 2.2: Prompting Techniques I

Few-Shot Classifier Prompt.

Builds on this session's chapter example: classifying support tickets into
company-specific categories that a zero-shot prompt would struggle with.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python classifier.py
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"

# The few-shot prompt template. TODO: add at least ONE more example of your
# own choosing before the final "Ticket: {ticket}\nCategory:" line — pick
# something that covers a case the existing examples don't, to genuinely
# strengthen the pattern rather than just adding a near-duplicate.
FEW_SHOT_PROMPT_TEMPLATE = """Classify the following support ticket into one of: Billing, Technical, Account Access, Other.

Ticket: "I was charged twice for my subscription this month."
Category: Billing

Ticket: "The app crashes every time I try to upload a photo."
Category: Technical

Ticket: "I can't log in, it says my password is wrong even after I reset it."
Category: Account Access

Ticket: "Can you tell me when paddle boarding season starts?"
Category: Other

# TODO: add your own example here, in the same format, before the line below.

Ticket: "{ticket}"
Category:"""

# Test tickets the classifier has NOT seen as examples — this is the real
# test of whether the few-shot pattern generalizes.
TEST_TICKETS = [
    "My invoice shows a fee I don't recognize from last week.",
    "The export button just spins forever and never finishes.",
    "I think someone else logged into my account, I see purchases I didn't make.",
    "What's your favorite color?",
    "Why was I charged $4.99 extra this month?",
]


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def classify(client, ticket: str) -> str:
    prompt = FEW_SHOT_PROMPT_TEMPLATE.format(ticket=ticket)
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=20,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def main():
    client = get_client()
    print(f"{'Ticket':<65} {'Category'}")
    print("-" * 90)
    for ticket in TEST_TICKETS:
        category = classify(client, ticket)
        short = ticket[:60] + ("..." if len(ticket) > 60 else "")
        print(f"{short:<65} {category}")

    print("\nDid every ticket land in a sensible category? If something looks")
    print("wrong, check whether your few-shot examples actually covered that")
    print("kind of case — that's almost always the real fix.")


if __name__ == "__main__":
    main()
