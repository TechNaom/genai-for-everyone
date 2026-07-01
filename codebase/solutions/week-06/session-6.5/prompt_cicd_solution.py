"""
Reference solution — Session 6.5: CI/CD & Versioning for Prompts

Run: python3 prompt_cicd_solution.py
"""

from typing import Dict, List

GOLDEN_DATASET = [
    {"input": "vacation days after 2 years", "expected": "18"},
    {"input": "parental leave weeks", "expected": "12"},
    {"input": "remote work days per week", "expected": "2"},
]


def mock_score_prompt(prompt_version: str) -> float:
    scores = {
        "v1_baseline": 0.92,
        "v2_friendlier_tone": 0.78,
        "v3_friendlier_fixed": 0.90,
    }
    return scores.get(prompt_version, 0.5)


def check_regression(new_version: str, baseline_version: str, threshold_drop: float = 0.05) -> Dict:
    new_score = mock_score_prompt(new_version)
    baseline_score = mock_score_prompt(baseline_version)
    drop = baseline_score - new_score
    passed = drop <= threshold_drop
    message = (
        f"PASS: {new_version} scored {new_score:.0%} vs baseline {baseline_score:.0%} "
        f"(drop of {drop:.0%}, within {threshold_drop:.0%} threshold)"
        if passed else
        f"FAIL: {new_version} scored {new_score:.0%} vs baseline {baseline_score:.0%} "
        f"(drop of {drop:.0%} exceeds {threshold_drop:.0%} threshold — blocking merge)"
    )
    return {"new_score": new_score, "baseline_score": baseline_score, "passed": passed, "message": message}


class PromptVersionHistory:
    def __init__(self):
        self.versions: List[Dict] = []
        self.current_index = -1

    def add_version(self, name: str, score: float):
        self.versions.append({"name": name, "score": score})
        self.current_index = len(self.versions) - 1

    def rollback(self) -> Dict:
        if self.current_index <= 0:
            raise IndexError("No previous version to roll back to.")
        self.current_index -= 1
        return self.versions[self.current_index]

    def changelog(self) -> str:
        lines = ["=== PROMPT VERSION CHANGELOG ==="]
        prev_score = None
        for v in self.versions:
            change = "" if prev_score is None else f" ({v['score'] - prev_score:+.0%})"
            lines.append(f"{v['name']}: {v['score']:.0%}{change}")
            prev_score = v["score"]
        return "\n".join(lines)


if __name__ == "__main__":
    result = check_regression("v2_friendlier_tone", baseline_version="v1_baseline")
    print(result["message"])

    history = PromptVersionHistory()
    history.add_version("v1_baseline", mock_score_prompt("v1_baseline"))
    history.add_version("v2_friendlier_tone", mock_score_prompt("v2_friendlier_tone"))
    history.add_version("v3_friendlier_fixed", mock_score_prompt("v3_friendlier_fixed"))
    print("\n" + history.changelog())

    print("\nRolling back from v3...")
    print(history.rollback())
