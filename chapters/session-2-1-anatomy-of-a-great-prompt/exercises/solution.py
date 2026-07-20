"""
Reference solution — Session 2.1: Anatomy of a Great Prompt

Worked rewrites. Note: there's no single "correct" rewrite for any of these —
what matters is that your version closes the specific gaps identified, not
that it matches this exact wording.

Run this file: python solution.py
"""

SOLUTIONS = [
    {
        "weak_prompt": "Write a blog post about productivity.",
        "missing_pillars": ["context", "constraints", "format"],
        "rewritten_prompt": (
            "Write a 600-word blog post for a B2B SaaS audience about how "
            "remote team leads can reduce meeting overload. Include 3 concrete "
            "tactics with one short example each. Tone: practical, not preachy. "
            "Format: an intro paragraph, 3 subheadings (one per tactic), and a "
            "1-sentence conclusion."
        ),
        "why_better": (
            "The original gave a topic but no audience, no angle, no length, and no structure — "
            "the model would have to invent all of that itself, likely producing something generic."
        ),
    },
    {
        "weak_prompt": "Can you help me with my resume?",
        "missing_pillars": ["clarity", "context", "format"],
        "rewritten_prompt": (
            "Review the resume bullet points below and rewrite each one to start with "
            "a strong action verb and include a quantified result where possible. "
            "Keep each bullet to one line. Here are the bullets: [paste bullets]"
        ),
        "why_better": (
            "\"Help with my resume\" could mean formatting, content review, rewriting, or career advice — "
            "the rewrite specifies the EXACT task (rewriting bullets with action verbs + quantification) "
            "and the exact output shape (one line each)."
        ),
    },
    {
        "weak_prompt": "Give me some marketing ideas.",
        "missing_pillars": ["context", "constraints", "format"],
        "rewritten_prompt": (
            "Give me 5 low-budget marketing ideas for a local independent coffee shop "
            "trying to attract students during a slow weekday afternoon period. "
            "Each idea should be implementable within a week with a budget under $200. "
            "Format as a numbered list with a one-sentence rationale under each idea."
        ),
        "why_better": (
            "Without knowing the business, budget, audience, or timeframe, 'marketing ideas' "
            "could mean anything from a Super Bowl ad strategy to a single Instagram post — "
            "the rewrite narrows this to something genuinely actionable."
        ),
    },
    {
        "weak_prompt": "Explain machine learning.",
        "missing_pillars": ["context", "constraints", "format"],
        "rewritten_prompt": (
            "Explain what machine learning is to a small business owner with no technical "
            "background, who is trying to decide if it's relevant to their business. "
            "Use one everyday analogy. Avoid jargon. Maximum 4 sentences."
        ),
        "why_better": (
            "\"Explain machine learning\" with no audience could produce a textbook-level answer "
            "or a one-line oversimplification — equally unhelpful for different reasons. Specifying "
            "the audience and their actual goal (deciding relevance to their business) shapes a "
            "genuinely useful answer."
        ),
    },
    {
        "weak_prompt": "Write code to process the data.",
        "missing_pillars": ["clarity", "context", "constraints", "format"],
        "rewritten_prompt": (
            "Write a Python function that takes a list of dictionaries representing "
            "customer orders (each with 'customer_id', 'amount', and 'date' keys) and "
            "returns a dictionary mapping each customer_id to their total spend. "
            "Include a docstring and handle the case where the input list is empty."
        ),
        "why_better": (
            "\"Process the data\" with no specification of what the data looks like, what "
            "processing means, or what output is needed is essentially unanswerable precisely — "
            "the model would have to invent an entire data shape and task from nothing. This is "
            "the most extreme example in the set: every single pillar was missing."
        ),
    },
]


def print_solution():
    for i, item in enumerate(SOLUTIONS, 1):
        print(f"\n{i}. WEAK: \"{item['weak_prompt']}\"")
        print(f"   Missing pillars: {item['missing_pillars']}")
        print(f"   Rewritten: \"{item['rewritten_prompt']}\"")
        print(f"   Why better: {item['why_better']}")


if __name__ == "__main__":
    print_solution()
