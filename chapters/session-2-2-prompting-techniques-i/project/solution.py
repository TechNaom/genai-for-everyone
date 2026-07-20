"""
Session 2.2 Project: Fix the Zero-Shot Triage Classifier — reference solution.

Converts the zero-shot priority classifier into a few-shot one, using four
worked examples that specifically target the boundary judgments a
company-specific priority scheme requires (P0 vs P1, and P1/P2 vs P3), then
scores both versions against the same 6 held-out tickets to prove the fix
actually works -- not just that it looks better on easy cases.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python solution.py
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"
VALID_PRIORITIES = ("P0-Critical", "P1-High", "P2-Normal", "P3-Low")

TEST_TICKETS = [
    ("Production login endpoint is returning 500 errors for all users right now", "P0-Critical"),
    ("Add a dark mode toggle to the settings page", "P3-Low"),
    ("Search results take ~3s to load during peak hours, used to be under 1s", "P1-High"),
    ("Typo in the footer copyright year", "P3-Low"),
    ("Payment webhook occasionally drops events, causing a few missed charges", "P0-Critical"),
    ("Could we get a CSV export button on the reports page?", "P3-Low"),
]

ZERO_SHOT_PROMPT_TEMPLATE = """Classify this internal engineering ticket into one of: P0-Critical, P1-High, P2-Normal, P3-Low.

Ticket: "{ticket}"
Priority:"""

# Four worked examples, deliberately chosen to cover the boundary judgments
# that make this scheme "company-specific" rather than common sense:
#   - a P0 that's an outage (the obvious case)
#   - a P0 that's NOT an outage but IS a data-integrity risk (the tricky
#     boundary: "still technically working" but still P0)
#   - a P1 that's "slow, not down" -- distinguishing degraded from broken
#   - a P3 that's a feature request, not a bug at all -- distinguishing
#     "nothing is broken" from every other tier
FEW_SHOT_PROMPT_TEMPLATE = """Classify this internal engineering ticket into one of: P0-Critical, P1-High, P2-Normal, P3-Low.

Ticket: "Checkout page returns a blank screen for every user, no orders are going through."
Priority: P0-Critical

Ticket: "We discovered the nightly backup job has been silently failing for a week -- no data loss yet, but we have zero recovery point if something breaks now."
Priority: P0-Critical

Ticket: "Dashboard loads take 4-5 seconds instead of the usual 1 second during business hours; still works, just slow."
Priority: P1-High

Ticket: "Could we add a 'remember me' checkbox to the login form?"
Priority: P3-Low

Ticket: "{ticket}"
Priority:"""


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def classify(client, prompt_template, ticket: str) -> str:
    prompt = prompt_template.format(ticket=ticket)
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=20,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def score(client, label, prompt_template):
    correct = 0
    print(f"\n--- {label} ---")
    print(f"{'Ticket':<62} {'Expected':<12} {'Got':<12} {'Match'}")
    print("-" * 95)
    for ticket, expected in TEST_TICKETS:
        got = classify(client, prompt_template, ticket)
        is_match = got.strip() == expected
        if is_match:
            correct += 1
        short = ticket[:58] + ("..." if len(ticket) > 58 else "")
        print(f"{short:<62} {expected:<12} {got:<12} {'yes' if is_match else 'no'}")
    return correct


def run():
    client = get_client()

    zero_shot_correct = score(client, "Zero-shot", ZERO_SHOT_PROMPT_TEMPLATE)
    few_shot_correct = score(client, "Few-shot", FEW_SHOT_PROMPT_TEMPLATE)

    total = len(TEST_TICKETS)
    print(f"\nZero-shot: {zero_shot_correct}/{total} correct")
    print(f"Few-shot:  {few_shot_correct}/{total} correct")

    if few_shot_correct > zero_shot_correct:
        print(
            "\nFew-shot improved on zero-shot -- the added examples targeted the "
            "actual boundary judgments (outage vs. degraded, bug vs. feature "
            "request) that zero-shot had no way to infer on its own."
        )
    elif few_shot_correct == zero_shot_correct:
        print(
            "\nNo improvement yet. That usually means the few-shot examples "
            "don't cover the SAME kind of boundary the failing test tickets "
            "hit -- check which tickets are still wrong and add an example "
            "that targets that exact judgment call."
        )
    else:
        print(
            "\nFew-shot did WORSE -- double-check your examples aren't "
            "internally inconsistent (e.g. two similar tickets labeled two "
            "different priorities), which confuses the pattern instead of "
            "clarifying it."
        )


if __name__ == "__main__":
    run()
