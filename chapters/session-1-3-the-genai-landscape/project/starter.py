"""
Session 1.3 Project: The Model Selector
See README.md in this folder for the full brief and an example run.

In the exercise you compared models by hand on ONE task. This project turns
that judgment into a small, reusable decision tool: given a short application
brief (its priority dimension and any hard constraints), it recommends which
KIND of model to reach for and explains why — exactly the framework from the
lesson (start general, question the capability you pay for, let hard
constraints override, re-evaluate on a cadence).

No API keys, no external libraries. The model tiers below are generic and
illustrative on purpose — the lesson teaches a durable framework, not a
leaderboard of this month's model names.

Fill in the TODO sections, then run:  python starter.py
"""

# A tiny, deliberately generic catalog of model *tiers* (not live product
# names). Scores are 1-5 and illustrative:
#   speed      -> higher = faster to respond
#   capability -> higher = stronger reasoning / nuance
#   value      -> higher = cheaper per token
#   context_k  -> approximate context window, in thousands of tokens
#   compliant  -> can satisfy a signed compliance / data-residency requirement
MODEL_TIERS = [
    {
        "name": "Fast tier (closed)",
        "kind": "closed/proprietary",
        "speed": 5, "capability": 3, "value": 5, "context_k": 128,
        "compliant": False,
    },
    {
        "name": "Frontier tier (closed)",
        "kind": "closed/proprietary",
        "speed": 2, "capability": 5, "value": 1, "context_k": 1000,
        "compliant": False,
    },
    {
        "name": "Self-hosted open-weight",
        "kind": "open-weight",
        "speed": 3, "capability": 4, "value": 3, "context_k": 256,
        "compliant": True,
    },
]

# Three realistic briefs, in the spirit of the lesson's worked comparison.
# priority names the ONE dimension that should drive the choice.
# requires_compliance is a HARD constraint that overrides pure capability.
APPLICATIONS = [
    {
        "name": "Live customer-facing chat widget",
        "priority": "speed",
        "requires_compliance": False,
    },
    {
        "name": "Overnight legal-contract summarizer (batch)",
        "priority": "capability",
        "requires_compliance": False,
    },
    {
        "name": "Clinical documentation assistant (patient data)",
        "priority": "capability",
        "requires_compliance": True,
    },
]


def recommend(app, tiers):
    """Return the single best-fit tier dict for one application brief.

    The rule mirrors the lesson's framework:
      1. If the brief has a HARD compliance constraint, first FILTER the
         candidates down to only the compliant ones.
      2. Then, among the remaining candidates, pick the tier that scores
         highest on the brief's priority dimension.
    Return None if no candidate can satisfy the constraint.
    """
    # TODO 1: If app["requires_compliance"] is True, build a list of only the
    # tiers whose "compliant" value is True. Otherwise, all tiers are
    # candidates. If the filtered list is empty, return None.
    candidates = None  # replace this

    # TODO 2: From candidates, return the tier with the highest score on
    # app["priority"] (e.g. "speed" or "capability"). Hint: max(..., key=...).
    return None  # replace this


def print_report(applications, tiers):
    print("=== Model Selector Report ===\n")
    for app in applications:
        pick = recommend(app, tiers)
        print(f"App: {app['name']}")
        print(f"  Priority dimension: {app['priority']}"
              + ("  (+ compliance required)" if app["requires_compliance"] else ""))
        if pick is None:
            print("  Recommendation: NONE of the available tiers satisfy the "
                  "hard constraint.\n")
            continue
        # TODO 3: print the chosen tier's name, kind, and its score on the
        # priority dimension, e.g.:
        #   Recommendation: Fast tier (closed) [closed/proprietary]
        #     speed score: 5/5
        print()


if __name__ == "__main__":
    print_report(APPLICATIONS, MODEL_TIERS)
