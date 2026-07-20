"""
Session 2.2 Project: Fix the Zero-Shot Triage Classifier
See README.md in this folder for the full brief and an example run.

The Pro-path challenge for this session: you're handed a zero-shot prompt
that classifies internal engineering tickets into a company-specific
priority scheme (P0-Critical, P1-High, P2-Normal, P3-Low). It fails
inconsistently -- not because the instruction is unclear, but because
"how urgent is this, really?" is exactly the kind of judgment call a
zero-shot prompt can't reliably infer without seeing worked examples of
where this specific company draws the line.

You'll: (1) run the zero-shot version and score it against known-correct
labels, (2) convert it to a few-shot prompt with boundary-case examples,
(3) re-score, and (4) confirm the failure mode is actually fixed -- not
just hidden by an easier test set.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python starter.py
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"
VALID_PRIORITIES = ("P0-Critical", "P1-High", "P2-Normal", "P3-Low")

# Held-out tickets with their known-correct priority, per this (fictional)
# company's internal triage rules:
#   P0 = production down, or user-facing data loss/integrity risk, right now
#   P1 = degraded but not down -- real users affected, no full outage
#   P2 = a real bug, but low-traffic/non-blocking, or affects few users
#   P3 = cosmetic issues and feature requests -- nothing broken
TEST_TICKETS = [
    ("Production login endpoint is returning 500 errors for all users right now", "P0-Critical"),
    ("Add a dark mode toggle to the settings page", "P3-Low"),
    ("Search results take ~3s to load during peak hours, used to be under 1s", "P1-High"),
    ("Typo in the footer copyright year", "P3-Low"),
    ("Payment webhook occasionally drops events, causing a few missed charges", "P0-Critical"),
    ("Could we get a CSV export button on the reports page?", "P3-Low"),
]

# The zero-shot prompt as originally written. It states the categories, but
# gives the model no worked examples of where THIS company draws the line
# between, say, "a slow page" (P1) and "a minor bug" (P2), or between "data
# loss risk" (P0) and "an annoying bug" (P2). Run this first and see how
# many of the 6 tickets it gets right against the known labels above.
ZERO_SHOT_PROMPT_TEMPLATE = """Classify this internal engineering ticket into one of: P0-Critical, P1-High, P2-Normal, P3-Low.

Ticket: "{ticket}"
Priority:"""

# TODO 1: Convert the zero-shot prompt above into a few-shot prompt.
# Add 3-4 worked examples as "Ticket: ... / Priority: ..." pairs, covering
# each priority level, and pick at least one genuinely tricky boundary case
# (e.g. a bug that's real but not urgent, or a slow-but-not-down feature).
# Do NOT reuse any of the exact TEST_TICKETS above as your examples -- that
# would just be memorization, not a fix.
FEW_SHOT_PROMPT_TEMPLATE = """Classify this internal engineering ticket into one of: P0-Critical, P1-High, P2-Normal, P3-Low.

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
    # TODO 2: for each (ticket, expected) pair in TEST_TICKETS, call
    # classify() with the given prompt_template, compare the result to
    # `expected`, and print a row showing ticket / expected / got / match.
    # Return the number correct out of len(TEST_TICKETS).
    correct = 0
    print(f"\n--- {label} ---")
    print(f"{'Ticket':<62} {'Expected':<12} {'Got':<12} {'Match'}")
    print("-" * 95)
    return correct


def run():
    client = get_client()

    zero_shot_correct = score(client, "Zero-shot", ZERO_SHOT_PROMPT_TEMPLATE)
    few_shot_correct = score(client, "Few-shot", FEW_SHOT_PROMPT_TEMPLATE)

    total = len(TEST_TICKETS)
    print(f"\nZero-shot: {zero_shot_correct}/{total} correct")
    print(f"Few-shot:  {few_shot_correct}/{total} correct")

    # TODO 3: print a one-line takeaway comparing the two scores, and a
    # warning if few-shot did NOT clearly outperform zero-shot (that would
    # mean the examples chosen didn't actually target the failure mode).


if __name__ == "__main__":
    run()
