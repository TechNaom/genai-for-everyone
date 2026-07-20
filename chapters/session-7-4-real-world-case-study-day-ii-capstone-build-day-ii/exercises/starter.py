"""
Session 7.4: Capstone Build Day II — Peer Review Checklist

Task: score a capstone project's self-report against a checklist derived
from the Session 7.1 proposal requirements, to catch gaps before demo day.

Run: python3 starter.py
"""

from typing import Dict, List

CHECKLIST_ITEMS = [
    "Runs end to end without manual intervention",
    "Uses at least 2 techniques from the program (per the Session 7.1 proposal)",
    "Success criteria from the proposal is actually being measured (not just 'it runs')",
    "At least one Week 5-style eval pass has been run",
    "Out-of-scope items from the proposal have been respected (no scope creep)",
]


def peer_review(project_name: str, answers: Dict[str, bool]) -> str:
    """
    TODO 1: given a dict mapping each CHECKLIST_ITEMS entry to True/False,
    return a formatted report: which items pass, which need attention, and
    an overall readiness percentage.
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Example self-review — replace with your own honest answers.
    example_answers = {
        "Runs end to end without manual intervention": True,
        "Uses at least 2 techniques from the program (per the Session 7.1 proposal)": True,
        "Success criteria from the proposal is actually being measured (not just 'it runs')": False,
        "At least one Week 5-style eval pass has been run": False,
        "Out-of-scope items from the proposal have been respected (no scope creep)": True,
    }
    print(peer_review("My Capstone v1", example_answers))
