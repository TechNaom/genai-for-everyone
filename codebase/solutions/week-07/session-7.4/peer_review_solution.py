"""
Reference solution — Session 7.4: Capstone Build Day II — Peer Review Checklist

Run: python3 peer_review_solution.py
"""

from typing import Dict

CHECKLIST_ITEMS = [
    "Runs end to end without manual intervention",
    "Uses at least 2 techniques from the program (per the Session 7.1 proposal)",
    "Success criteria from the proposal is actually being measured (not just 'it runs')",
    "At least one Week 5-style eval pass has been run",
    "Out-of-scope items from the proposal have been respected (no scope creep)",
]


def peer_review(project_name: str, answers: Dict[str, bool]) -> str:
    lines = [f"=== PEER REVIEW: {project_name} ==="]
    passed = 0
    for item in CHECKLIST_ITEMS:
        status = "✅" if answers.get(item) else "⚠️  NEEDS ATTENTION"
        lines.append(f"{status} — {item}")
        if answers.get(item):
            passed += 1
    readiness = passed / len(CHECKLIST_ITEMS) * 100
    lines.append(f"\nReadiness: {passed}/{len(CHECKLIST_ITEMS)} ({readiness:.0f}%)")
    if readiness < 100:
        lines.append("Recommendation: address the flagged items before demo day, "
                      "prioritizing the eval pass and success-criteria measurement — "
                      "these are what let you actually claim the capstone 'works.'")
    return "\n".join(lines)


if __name__ == "__main__":
    example_answers = {
        "Runs end to end without manual intervention": True,
        "Uses at least 2 techniques from the program (per the Session 7.1 proposal)": True,
        "Success criteria from the proposal is actually being measured (not just 'it runs')": False,
        "At least one Week 5-style eval pass has been run": False,
        "Out-of-scope items from the proposal have been respected (no scope creep)": True,
    }
    print(peer_review("My Capstone v1", example_answers))
