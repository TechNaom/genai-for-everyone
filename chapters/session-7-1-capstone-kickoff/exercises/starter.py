"""
Session 7.1: Core Path — Capstone Proposal Scope Checker

Task: check a filled-in proposal_template.md for common scoping red flags.

Run: python3 starter.py your_proposal.md
"""

import sys

VAGUE_PHRASES = ["everything", "anything", "all my", "helps with", "some kind of"]
REQUIRED_SECTIONS = [
    "## Problem + user",
    "## Solution sketch",
    "## Techniques used (and why)",
    "## Success criteria",
    "## Out of scope",
]


def load_proposal(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def check_required_sections(text: str) -> list:
    """
    TODO 1: return a list of missing section headers (from REQUIRED_SECTIONS)
    that aren't present in `text`.
    """
    raise NotImplementedError


def check_vague_phrases(text: str) -> list:
    """
    TODO 2: return a list of vague phrases (from VAGUE_PHRASES, case-insensitive)
    that appear in `text`.
    """
    raise NotImplementedError


def check_success_criteria_has_number(text: str) -> bool:
    """
    TODO 3: extract the "Success criteria" section's content and check whether
    it contains at least one digit (a proxy for "has a measurable target").
    Return True if it does, False otherwise.
    """
    raise NotImplementedError


def check_proposal(path: str) -> None:
    text = load_proposal(path)
    missing = check_required_sections(text)
    vague = check_vague_phrases(text)
    has_number = check_success_criteria_has_number(text)

    print(f"Checking {path}...\n")
    if missing:
        print(f"❌ Missing sections: {missing}")
    else:
        print("✅ All required sections present")

    if vague:
        print(f"⚠️  Vague phrases found: {vague} — consider being more specific")
    else:
        print("✅ No vague phrases detected")

    if has_number:
        print("✅ Success criteria includes a measurable number")
    else:
        print("❌ Success criteria has no number — is it actually checkable?")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 starter.py your_proposal.md")
        sys.exit(1)
    check_proposal(sys.argv[1])
