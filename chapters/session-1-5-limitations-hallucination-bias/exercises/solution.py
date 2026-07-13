"""
Reference solution — Session 1.5: Limitations, Hallucination & Bias

Ground truth for each statement, with the reasoning signal that should have
flagged it — verified against real sources, not assumed. This is the entire
point of the exercise: don't trust "sounds right," verify.

Run this file: python solution.py
"""

ANSWERS = [
    {
        "statement": "The Eiffel Tower was completed in 1889 for the World's Fair held in Paris.",
        "classification": "accurate",
        "reasoning": "Verifiably true (completed/dedicated 1889, centerpiece of that year's Exposition Universelle). No suspiciously specific unverifiable detail — a good example of a true, simple factual claim.",
    },
    {
        "statement": "A 2019 Stanford study found that exactly 73.4% of remote workers report higher productivity, according to lead researcher Dr. Marina Chen.",
        "classification": "fabricated",
        "reasoning": "RED FLAG PATTERN: an oddly precise statistic (73.4%) plus a named 'lead researcher' that sounds plausible but isn't independently verifiable from the statement alone. This is the classic shape of a fabricated citation — specific enough to sound authoritative, vague enough to never check.",
    },
    {
        "statement": "Mount Everest's summit sits at 8,848.86 meters above sea level.",
        "classification": "accurate",
        "reasoning": "Verifiably true — this is the official height from the 2020 joint Nepal-China survey. Note: this ALSO looks 'suspiciously precise' at first glance, which is exactly why this item is included — specificity alone isn't the signal; specificity that can't be independently corroborated is.",
    },
    {
        "statement": "Shakespeare's play 'Hamlet' contains the line 'To be, or not to be, that is the question' in Act 3, Scene 1.",
        "classification": "accurate",
        "reasoning": "Verifiably true — well-documented, easily corroborated across many independent sources.",
    },
    {
        "statement": "The human body contains exactly 37.2 trillion cells, as measured in a landmark 2013 cell-counting study.",
        "classification": "fabricated",
        "reasoning": "RED FLAG PATTERN: real estimates for human cell count exist (commonly cited around 37 trillion as a rough estimate from a real 2013 paper), but the word 'exactly' attached to a number like this is the tell — no real biological measurement of this kind produces an 'exact' count. The fabrication here is subtle: it's built around a kernel of real research, with fabricated false precision layered on top.",
    },
    {
        "statement": "Python's `sorted()` function returns a new sorted list and does not modify the original list in place.",
        "classification": "accurate",
        "reasoning": "Verifiably true and independently checkable in seconds by running it yourself — a good reminder that for technical/code claims, you often don't need to trust ANY source, you can just verify directly.",
    },
    {
        "statement": "According to historian Dr. Lisa Whitfield's 2008 paper, exactly 12,847 ships crossed the Atlantic in 1850.",
        "classification": "fabricated",
        "reasoning": "RED FLAG PATTERN: same shape as item 2 — an absurdly precise historical statistic attached to a named researcher and a specific year, none of which is independently checkable from the statement itself. Historical shipping counts from 1850 would not realistically be known to this level of precision.",
    },
    {
        "statement": "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
        "classification": "accurate",
        "reasoning": "Verifiably true (the exact defined value is 299,792.458 km/s) — note the word 'approximately' here is doing honest work, rounding a known exact constant rather than fabricating false precision.",
    },
    {
        "statement": "The original recipe for Coca-Cola, as documented in company founder John Pemberton's personal 1886 notebook (page 47), called for exactly 2.5 grams of a secret ingredient still used today.",
        "classification": "fabricated",
        "reasoning": "RED FLAG PATTERN, with a twist worth knowing: there IS a real, published Pemberton notebook recipe (discovered by journalists and historians), which makes this trickier than it looks. But the specific details here — 'page 47,' a single ingredient measured in '2.5 grams,' and the claim that it's 'still used today' — are fabricated. The real published notebook recipe lists multiple flavoring oils in drops/ounces, not one mystery ingredient in grams, and Coca-Cola's actual CURRENT formula remains a genuinely guarded secret, not something derived from that old notebook. This is the most instructive item in the set: a fabrication built by layering invented specifics on top of a real, verifiable core fact.",
    },
    {
        "statement": "JSON (JavaScript Object Notation) is a lightweight data format that is easy for both humans and machines to read and write.",
        "classification": "accurate",
        "reasoning": "Verifiably true and a standard, uncontroversial description — included as a 'plain, unremarkable true statement' to show that not every accurate statement needs a dramatic verification step.",
    },
]


def print_solution():
    for i, item in enumerate(ANSWERS, 1):
        print(f"\n{i}. {item['statement']}")
        print(f"   Classification: {item['classification'].upper()}")
        print(f"   Reasoning: {item['reasoning']}")

    print("\n--- The pattern across all the fabricated items ---")
    print(
        "Every fabricated statement here followed the same shape: a specific, "
        "named source (a researcher, a notebook, a page number) attached to a "
        "precise number, presented with the exact same confident tone as the "
        "true statements. Confidence and fluency were USELESS as signals — "
        "every statement in this set was written in identical tone. The real "
        "signal was: can this specific detail be independently verified, or "
        "does it just SOUND like the kind of thing that could be verified?"
    )


if __name__ == "__main__":
    print_solution()
