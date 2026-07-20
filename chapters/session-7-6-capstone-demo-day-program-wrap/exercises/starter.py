"""
Session 7.6: Core Path — Portfolio README Checker

Run: python3 starter.py your_readme.md
"""

import sys

REQUIRED_SECTIONS = {
    "what_and_who": ["what this does", "what it does", "for whom", "problem"],
    "evidence_it_works": ["screenshot", "demo", "gif", "example"],
    "techniques_and_why": ["rag", "agent", "evaluation", "used", "technique"],
    "eval_numbers": ["%", "accuracy", "golden", "eval"],
    "how_to_run": ["pip install", "run", "setup", "deploy"],
}


def load_readme(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def check_readme(text: str) -> dict:
    """
    TODO 1: for each section in REQUIRED_SECTIONS, check (case-insensitive)
    whether ANY of its keyword list appears in `text`. Return a dict
    {section_name: True/False}.
    """
    raise NotImplementedError


def print_report(path: str):
    text = load_readme(path)
    results = check_readme(text)
    print(f"Checking {path}...\n")
    for section, present in results.items():
        status = "✅" if present else "⚠️  missing"
        print(f"{status} — {section.replace('_', ' ')}")
    score = sum(results.values())
    print(f"\n{score}/{len(REQUIRED_SECTIONS)} sections present")
    if score == len(REQUIRED_SECTIONS):
        print("Ready for demo day.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 starter.py your_readme.md")
        sys.exit(1)
    print_report(sys.argv[1])
