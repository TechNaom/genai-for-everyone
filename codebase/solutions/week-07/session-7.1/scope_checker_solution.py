"""
Reference solution — Session 7.1: Capstone Proposal Scope Checker

Run: python3 scope_checker_solution.py example_proposal.md
"""

import re
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
    return [section for section in REQUIRED_SECTIONS if section not in text]


def check_vague_phrases(text: str) -> list:
    lowered = text.lower()
    return [phrase for phrase in VAGUE_PHRASES if phrase in lowered]


def check_success_criteria_has_number(text: str) -> bool:
    match = re.search(r"## Success criteria(.*?)(##|\Z)", text, re.DOTALL)
    if not match:
        return False
    section_text = match.group(1)
    return bool(re.search(r"\d", section_text))


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
        print("Usage: python3 scope_checker_solution.py example_proposal.md")
        sys.exit(1)
    check_proposal(sys.argv[1])
