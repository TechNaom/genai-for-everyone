"""
Reference solution — Session 2.2: Prompting Techniques I

Adds one new few-shot example (a "Technical" case that looks different from
the existing crash example, to broaden rather than duplicate the pattern)
and tests against the same 5 held-out tickets.
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"

FEW_SHOT_PROMPT_TEMPLATE = """Classify the following support ticket into one of: Billing, Technical, Account Access, Other.

Ticket: "I was charged twice for my subscription this month."
Category: Billing

Ticket: "The app crashes every time I try to upload a photo."
Category: Technical

Ticket: "I can't log in, it says my password is wrong even after I reset it."
Category: Account Access

Ticket: "Can you tell me when paddle boarding season starts?"
Category: Other

Ticket: "The export button just spins forever and never finishes."
Category: Technical

Ticket: "{ticket}"
Category:"""

# NOTE ON THE ADDED EXAMPLE: the original set already had one "Technical"
# example (a crash). Rather than adding a near-duplicate crash example, this
# adds a DIFFERENT kind of technical failure (a stuck/unresponsive feature,
# not a crash) — broadening what "Technical" covers rather than reinforcing
# the same narrow case. This is the point made in the chapter: examples too
# similar to each other don't teach the model much beyond the first one.

TEST_TICKETS = [
    "My invoice shows a fee I don't recognize from last week.",
    "The export button just spins forever and never finishes.",  # near-duplicate of new example, on purpose
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

    print(
        "\nExpected pattern: tickets 1 & 5 -> Billing, ticket 2 -> Technical, "
        "ticket 3 -> Account Access, ticket 4 -> Other."
    )
    print(
        "If ticket 4 ('favorite color') gets misclassified into a real category "
        "instead of 'Other', that's the most instructive failure to debug — it's "
        "exactly the boundary case the chapter calls out as hardest to convey "
        "through instruction alone."
    )


if __name__ == "__main__":
    main()
