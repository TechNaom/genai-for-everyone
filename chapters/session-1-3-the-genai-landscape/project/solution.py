"""
Session 1.3 Project: The Model Selector — reference solution.

The tier scores and briefs are illustrative, not live measurements. What
matters is the decision PROCESS: filter on hard constraints first, then rank
the survivors on the one dimension that actually drives the brief.
"""

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
    """Return the single best-fit tier dict for one application brief."""
    # 1. Hard constraint first: if compliance is required, keep only the
    #    tiers that can satisfy it. This can eliminate an otherwise-stronger
    #    model entirely — exactly the point of the healthcare example.
    if app["requires_compliance"]:
        candidates = [t for t in tiers if t["compliant"]]
    else:
        candidates = list(tiers)

    if not candidates:
        return None

    # 2. Among the survivors, pick the highest score on the priority dimension.
    return max(candidates, key=lambda t: t[app["priority"]])


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
        print(f"  Recommendation: {pick['name']} [{pick['kind']}]")
        print(f"    {app['priority']} score: {pick[app['priority']]}/5\n")

    print("--- Why these differ ---")
    print(
        "The chat widget optimizes for speed, so the fast closed tier wins even "
        "though it's the weakest reasoner. The overnight batch job has no speed "
        "pressure and a high cost of a missed clause, so the frontier tier's "
        "capability is worth its slowness and price. The clinical assistant looks "
        "like a capability contest too, but the compliance constraint filters the "
        "closed tiers out first, so the self-hosted open-weight model wins by being "
        "the strongest option that is even eligible. Same framework, three "
        "different answers: filter on hard constraints, then rank on what the brief "
        "actually needs."
    )


if __name__ == "__main__":
    print_report(APPLICATIONS, MODEL_TIERS)
