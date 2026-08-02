"""
Session 1.1 Project: The AI Request Decoder

The exercise had you hand-classify twelve isolated scenarios. This project
turns that judgment into a small, reusable tool: feed it one vague
"let's use AI on this" request, made of several sub-tasks, and it decodes
each sub-task as predictive or generative and flags its rollout risk --
the exact move the lesson's worked scenario makes by hand.

Run this file:  python starter.py
"""

# One vague request from a VP, already broken into its hidden sub-projects.
REQUEST = "We need to put AI on our customer support backlog"

SUBPROJECTS = [
    "Draft reply suggestions for agents to review",
    "Auto-route tickets to the right team",
    "Predict which tickets will escalate or churn",
    "Summarize long multi-message threads for agents",
]

# Keywords that give away each sub-task's category. Real classification
# needs judgment, not just keyword-matching -- this is a simplification
# that's right often enough to be a useful first pass.
PREDICTIVE_KEYWORDS = ("route", "predict", "escalate", "churn", "score", "classify", "detect", "flag")
GENERATIVE_KEYWORDS = ("draft", "write", "summarize", "generate", "translate", "compose", "reply")


def classify_subproject(description):
    # TODO 1: look at `description` (lowercase it first) and return
    # "predictive" if it contains any PREDICTIVE_KEYWORDS, or "generative"
    # if it contains any GENERATIVE_KEYWORDS. Return "unknown" if neither matches.
    return "unknown"


def risk_note(category):
    # TODO 2: return a one-line risk note.
    #   "generative" -> "Medium risk: needs human review before it reaches a customer."
    #   "predictive" -> "Lower risk: deterministic output, easy to audit."
    #   anything else -> "Unclear: classify by hand before estimating risk."
    return ""


def decode_request(request, subprojects):
    print(f"=== AI Request Decoder ===\nRequest: \"{request}\"\n")
    print(f"{'Sub-project':<50} {'Category':<12} Risk")
    print("-" * 100)

    # TODO 3: for each sub-project, classify it, look up its risk note, and
    # print a row. Then print a takeaway line counting how many sub-projects
    # came back "generative" vs. "predictive".


if __name__ == "__main__":
    decode_request(REQUEST, SUBPROJECTS)
