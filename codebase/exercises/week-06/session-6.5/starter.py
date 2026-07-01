"""
Session 6.5: CI/CD & Versioning for Prompts

Task: build a CI-style regression gate for prompt versions, then (Pro path)
a version history with rollback.

Run: python3 starter.py
"""

from typing import Dict, List

GOLDEN_DATASET = [
    {"input": "vacation days after 2 years", "expected": "18"},
    {"input": "parental leave weeks", "expected": "12"},
    {"input": "remote work days per week", "expected": "2"},
]


def mock_score_prompt(prompt_version: str) -> float:
    """
    Mock scorer: pretend each prompt version has a fixed 'quality' baked in,
    for deterministic grading. In a real system this would call the model
    with `prompt_version` as the system prompt and score against GOLDEN_DATASET.
    """
    scores = {
        "v1_baseline": 0.92,
        "v2_friendlier_tone": 0.78,   # regression: friendlier wording hurt precision
        "v3_friendlier_fixed": 0.90,
    }
    return scores.get(prompt_version, 0.5)


def check_regression(new_version: str, baseline_version: str, threshold_drop: float = 0.05) -> Dict:
    """
    TODO 1: score both versions with mock_score_prompt, compute the drop
    (baseline_score - new_score), and return a dict with at least:
    {"new_score": ..., "baseline_score": ..., "passed": bool, "message": str}
    "passed" should be False if the drop exceeds threshold_drop.
    """
    raise NotImplementedError


class PromptVersionHistory:
    """Pro path: track prompt versions with scores, support rollback."""

    def __init__(self):
        self.versions: List[Dict] = []
        self.current_index = -1

    def add_version(self, name: str, score: float):
        # TODO 2: append {"name": name, "score": score} and update current_index
        raise NotImplementedError

    def rollback(self) -> Dict:
        # TODO 3: move current_index back by 1 (if possible) and return that version
        raise NotImplementedError

    def changelog(self) -> str:
        # TODO 4: return a formatted string showing each version, its score,
        # and the score change from the previous version
        raise NotImplementedError


if __name__ == "__main__":
    result = check_regression("v2_friendlier_tone", baseline_version="v1_baseline")
    print(result)

    history = PromptVersionHistory()
    history.add_version("v1_baseline", mock_score_prompt("v1_baseline"))
    history.add_version("v2_friendlier_tone", mock_score_prompt("v2_friendlier_tone"))
    history.add_version("v3_friendlier_fixed", mock_score_prompt("v3_friendlier_fixed"))
    print(history.changelog())

    print("Rolling back from v3...")
    print(history.rollback())
