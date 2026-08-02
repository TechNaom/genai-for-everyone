"""
Session 1.1 Project: The AI Request Decoder -- reference solution.

Turns "let's put AI on this" into a decoded list of its hidden sub-projects,
each tagged predictive or generative with a rollout risk note.
"""

REQUEST = "We need to put AI on our customer support backlog"

SUBPROJECTS = [
    "Draft reply suggestions for agents to review",
    "Auto-route tickets to the right team",
    "Predict which tickets will escalate or churn",
    "Summarize long multi-message threads for agents",
]

PREDICTIVE_KEYWORDS = ("route", "predict", "escalate", "churn", "score", "classify", "detect", "flag")
GENERATIVE_KEYWORDS = ("draft", "write", "summarize", "generate", "translate", "compose", "reply")


def classify_subproject(description):
    # TODO 1: keyword-match against PREDICTIVE_KEYWORDS / GENERATIVE_KEYWORDS.
    text = description.lower()
    if any(keyword in text for keyword in PREDICTIVE_KEYWORDS):
        return "predictive"
    if any(keyword in text for keyword in GENERATIVE_KEYWORDS):
        return "generative"
    return "unknown"


def risk_note(category):
    # TODO 2: map category -> a one-line risk note.
    notes = {
        "generative": "Medium risk: needs human review before it reaches a customer.",
        "predictive": "Lower risk: deterministic output, easy to audit.",
    }
    return notes.get(category, "Unclear: classify by hand before estimating risk.")


def decode_request(request, subprojects):
    print(f"=== AI Request Decoder ===\nRequest: \"{request}\"\n")
    print(f"{'Sub-project':<50} {'Category':<12} Risk")
    print("-" * 100)

    # TODO 3: classify each sub-project, print a row, then a takeaway.
    counts = {"predictive": 0, "generative": 0, "unknown": 0}
    for sub in subprojects:
        category = classify_subproject(sub)
        counts[category] = counts.get(category, 0) + 1
        print(f"{sub:<50} {category.upper():<12} {risk_note(category)}")

    print(
        f"\nTakeaway: this one sentence hides {counts['generative']} generative "
        f"and {counts['predictive']} predictive sub-project(s) -- each needs its "
        f"own data, evaluation approach, and rollout plan."
    )


if __name__ == "__main__":
    decode_request(REQUEST, SUBPROJECTS)
