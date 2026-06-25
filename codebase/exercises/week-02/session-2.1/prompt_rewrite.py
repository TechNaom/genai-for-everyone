"""
Exercise — Session 2.1: Anatomy of a Great Prompt

Prompt Rewrite Exercise (Bad -> Great).

For each weak prompt, identify which pillar(s) are missing, then rewrite it.

Run this file: python prompt_rewrite.py
"""

WEAK_PROMPTS = [
    {
        "weak_prompt": "Write a blog post about productivity.",
        "missing_pillars": None,     # TODO: list, e.g. ["clarity", "context", "constraints", "format"]
        "rewritten_prompt": None,    # TODO
        "why_better": None,          # TODO
    },
    {
        "weak_prompt": "Can you help me with my resume?",
        "missing_pillars": None,
        "rewritten_prompt": None,
        "why_better": None,
    },
    {
        "weak_prompt": "Give me some marketing ideas.",
        "missing_pillars": None,
        "rewritten_prompt": None,
        "why_better": None,
    },
    {
        "weak_prompt": "Explain machine learning.",
        "missing_pillars": None,
        "rewritten_prompt": None,
        "why_better": None,
    },
    {
        "weak_prompt": "Write code to process the data.",
        "missing_pillars": None,
        "rewritten_prompt": None,
        "why_better": None,
    },
]

VALID_PILLARS = {"clarity", "context", "constraints", "format"}


def review():
    incomplete = 0
    for i, item in enumerate(WEAK_PROMPTS, 1):
        print(f"\n{i}. WEAK: \"{item['weak_prompt']}\"")

        if item["missing_pillars"] is None or item["rewritten_prompt"] is None:
            incomplete += 1
            print("   (not yet filled in)")
            continue

        invalid = [p for p in item["missing_pillars"] if p not in VALID_PILLARS]
        if invalid:
            print(f"   WARNING: unrecognized pillar(s): {invalid}. Valid: {VALID_PILLARS}")

        print(f"   Missing pillars: {item['missing_pillars']}")
        print(f"   Rewritten: \"{item['rewritten_prompt']}\"")
        if item["why_better"]:
            print(f"   Why better: {item['why_better']}")

    if incomplete:
        print(f"\n{incomplete} prompt(s) not yet rewritten.")
    else:
        print("\nAll rewritten. Compare against codebase/solutions/week-02/session-2.1/")


if __name__ == "__main__":
    review()
