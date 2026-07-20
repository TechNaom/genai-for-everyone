"""
Session 6.5 Exercise: The CI Regression Gate -- reference solution.

Run: python3 solution.py
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
        f"(drop of {drop:.0%} exceeds {threshold_drop:.0%} threshold -- blocking merge)"
    )

    return {
        "new_score": new_score,
        "baseline_score": baseline_score,
        "passed": passed,
        "message": message,
    }


if __name__ == "__main__":
    result = check_regression("v2_friendlier_tone", baseline_version="v1_baseline")
    print(result["message"])
    assert result["passed"] is False, "v2_friendlier_tone should FAIL against v1_baseline"

    result = check_regression("v3_friendlier_fixed", baseline_version="v1_baseline")
    print(result["message"])
    assert result["passed"] is True, "v3_friendlier_fixed should PASS against v1_baseline"

    print("\nAll checks ran. If you see this with no AssertionError, the gate works.")
