"""
Exercise — Session 1.5: Limitations, Hallucination & Bias

Hallucination Detection Exercise.

For each statement, fill in:
  - your_classification: "accurate" or "fabricated"
  - your_reasoning: ONE sentence on the signal that led you there

Remember: confidence and fluency are USELESS signals here — every statement
below is written in the same confident tone, true or false. Look instead for
suspiciously specific, hard-to-verify details.

Run this file: python starter.py
"""

STATEMENTS = [
    {
        "statement": "The Eiffel Tower was completed in 1889 for the World's Fair held in Paris.",
        "your_classification": None,   # TODO: "accurate" or "fabricated"
        "your_reasoning": None,         # TODO
    },
    {
        "statement": "A 2019 Stanford study found that exactly 73.4% of remote workers report higher productivity, according to lead researcher Dr. Marina Chen.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "Mount Everest's summit sits at 8,848.86 meters above sea level.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "Shakespeare's play 'Hamlet' contains the line 'To be, or not to be, that is the question' in Act 3, Scene 1.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "The human body contains exactly 37.2 trillion cells, as measured in a landmark 2013 cell-counting study.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "Python's `sorted()` function returns a new sorted list and does not modify the original list in place.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "According to historian Dr. Lisa Whitfield's 2008 paper, exactly 12,847 ships crossed the Atlantic in 1850.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "The original recipe for Coca-Cola, as documented in company founder John Pemberton's personal 1886 notebook (page 47), called for exactly 2.5 grams of a secret ingredient still used today.",
        "your_classification": None,
        "your_reasoning": None,
    },
    {
        "statement": "JSON (JavaScript Object Notation) is a lightweight data format that is easy for both humans and machines to read and write.",
        "your_classification": None,
        "your_reasoning": None,
    },
]


def review():
    print(f"{'#':<4} {'Your call':<14} {'Statement (truncated)'}")
    print("-" * 90)

    incomplete = 0
    for i, item in enumerate(STATEMENTS, 1):
        if item["your_classification"] is None:
            incomplete += 1
            continue
        short = item["statement"][:65] + ("..." if len(item["statement"]) > 65 else "")
        print(f"{i:<4} {item['your_classification']:<14} {short}")
        if item["your_reasoning"]:
            print(f"     Reasoning: {item['your_reasoning']}")
        print()

    if incomplete:
        print(f"\n{incomplete} statement(s) not yet classified.")
    else:
        print("\nAll classified. Compare your answers against solution.py")


if __name__ == "__main__":
    review()
