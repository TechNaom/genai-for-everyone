"""
Session 1.5 Project: Hallucination Red-Flag Detector — reference solution.

We can't write code that knows whether a claim is TRUE — that would require
verifying it against the real world. What we CAN do is scan for the SHAPE of
a likely hallucination: the red-flag signals from the lesson (false precision,
an unverifiable named source, an oddly specific page citation).

The crucial lesson this project teaches: this detector flags risk-SHAPE, not
truth. It will sometimes flag a true statement (a precise-but-real fact) and
that is the point — a high score means "verify this," never "this is false."
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
    """Flag the word 'exactly' — the classic tell of fabricated false precision."""
    return "exactly" in text.lower()


def has_unverifiable_source(text):
    """Flag an appeal to a named source that the claim gives you no way to check."""
    lowered = text.lower()
    return any(marker in lowered for marker in SOURCE_MARKERS)


def has_page_citation(text):
    """Flag a specific 'page N' citation — a hallmark of citation-shaped text."""
    return re.search(r"page \d+", text.lower()) is not None


def has_precise_number(text):
    """Flag a suspiciously precise decimal figure (e.g. 73.4, 8,848.86, 2.5)."""
    return re.search(r"\d+\.\d+", text) is not None


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

    print("\n" + "-" * 70)
    print(
        "Reminder: statement 3 (Everest, 8,848.86 m) is precise but TRUE, and\n"
        "this heuristic can't tell the difference. Confidence and fluency are\n"
        "useless signals; even shape-based signals only tell you WHERE to look.\n"
        "The only real fix for a factual claim is verification (grounding / RAG)."
    )


if __name__ == "__main__":
    scan()
