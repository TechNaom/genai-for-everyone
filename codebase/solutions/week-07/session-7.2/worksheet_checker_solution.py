"""
Reference solution — Session 7.2: Case Study Worksheet Completeness Checker

Run: python3 worksheet_checker_solution.py filled_worksheet_example.md
"""

import re
import sys

REQUIRED_SECTIONS = [
    "## Predictive vs. generative components",
    "## Where each Week 1-6 concept shows up",
    "## Root-cause analysis: the data-loss incident",
    "## What would you have caught earlier?",
]

MIN_WORDS_PER_SECTION = 15


def load_worksheet(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def split_sections(text: str) -> dict:
    sections = {}
    headers_pattern = "|".join(re.escape(h) for h in REQUIRED_SECTIONS)
    matches = list(re.finditer(headers_pattern, text))
    for i, match in enumerate(matches):
        header = match.group(0)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sections[header] = text[start:end].strip()
    return sections


def check_worksheet(path: str) -> None:
    text = load_worksheet(path)
    sections = split_sections(text)

    print(f"Checking {path}...\n")
    for header in REQUIRED_SECTIONS:
        body = sections.get(header, "")
        word_count = len(body.split())
        if header not in text:
            print(f"❌ Missing section: {header}")
        elif word_count < MIN_WORDS_PER_SECTION:
            print(f"⚠️  {header}: only {word_count} words — likely too thin (expected {MIN_WORDS_PER_SECTION}+)")
        else:
            print(f"✅ {header}: {word_count} words")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 worksheet_checker_solution.py filled_worksheet_example.md")
        sys.exit(1)
    check_worksheet(sys.argv[1])
