"""
Session 1.5 Project: Hallucination Red-Flag Detector
See README.md in this folder for the full brief and example output.

You can't write code that knows whether a claim is TRUE — that would require
verifying it against the real world. What you CAN do is scan for the SHAPE of
a likely hallucination: the red-flag signals from the lesson.

Fill in the four detector functions below. This starter already runs — but
until you implement the TODOs, every statement is scored LOW.

Run this file: python starter.py
"""

import re

STATEMENTS = [
    "The Eiffel Tower was completed in 1889 for the World's Fair held in Paris.",
    "A 2019 Stanford study found that exactly 73.4% of remote workers report higher productivity, according to lead researcher Dr. Marina Chen.",
    "Mount Everest's summit sits at 8,848.86 meters above sea level.",
    "The human body contains exactly 37.2 trillion cells, as measured in a landmark 2013 cell-counting study.",
    "According to historian Dr. Lisa Whitfield's 2008 paper, exactly 12,847 ships crossed the Atlantic in 1850.",
    "The original recipe for Coca-Cola, as documented in company founder John Pemberton's personal 1886 notebook (page 47), called for exactly 2.5 grams of a secret ingredient still used today.",
    "JSON is a lightweight data format that is easy for both humans and machines to read and write.",
]

# Words/phrases that lean on a source you can't check from the claim itself.
SOURCE_MARKERS = ["dr.", "according to", "researcher", "study", "paper", "notebook"]


def has_false_precision(text):
    # TODO 1: return True if the word "exactly" appears (case-insensitive).
    return False


def has_unverifiable_source(text):
    # TODO 2: return True if any marker in SOURCE_MARKERS appears in the text
    # (case-insensitive).
    return False


def has_page_citation(text):
    # TODO 3: return True if the text contains a "page N" citation.
    # Hint: re.search(r"page \d+", text.lower())
    return False


def has_precise_number(text):
    # TODO 4: return True if the text contains a decimal number like 73.4 or
    # 8,848.86. Hint: re.search(r"\d+\.\d+", text)
    return False


def score_statement(text):
    """Return (risk_score, list_of_fired_flags) for one statement."""
    flags = []
    if has_false_precision(text):
        flags.append("FALSE PRECISION ('exactly' + a number)")
    if has_unverifiable_source(text):
        flags.append("UNVERIFIABLE NAMED SOURCE")
    if has_page_citation(text):
        flags.append("ODDLY SPECIFIC PAGE CITATION")
    if has_precise_number(text):
        flags.append("SUSPICIOUSLY PRECISE NUMBER")
    return len(flags), flags


def risk_label(score):
    if score == 0:
        return "LOW"
    if score == 1:
        return "MEDIUM"
    return "HIGH"


def scan():
    print("=" * 70)
    print("HALLUCINATION RED-FLAG DETECTOR")
    print("Flags risk-SHAPE, not truth. A high score means VERIFY — not FALSE.")
    print("=" * 70)

    for i, statement in enumerate(STATEMENTS, 1):
        score, flags = score_statement(statement)
        print(f"\n{i}. [{risk_label(score)} RISK, score {score}] {statement}")
        if flags:
            for flag in flags:
                print(f"     - {flag}")
        else:
            print("     - no red-flag signals detected")


if __name__ == "__main__":
    scan()
