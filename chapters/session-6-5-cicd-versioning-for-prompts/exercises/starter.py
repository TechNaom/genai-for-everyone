"""
Session 6.5 Exercise: The CI Regression Gate

Task: build a CI-style regression gate for prompt versions -- given a new
prompt version and a golden dataset, score it, compare against a stored
baseline score, and return pass/fail with a clear message. Same shape as a
real CI job's exit code.

No API key, no internet access, no external libraries -- mock_score_prompt
stands in for "run this prompt against the golden dataset and compute a
quality score," exactly like Session 5.1's regression suite, just wired to
run automatically instead of by hand.

Run: python3 starter.py
"""

from typing import Dict, List

# The golden dataset this gate is scoring against (Session 5.1/6.4 territory).
# In a real system, mock_score_prompt would run each prompt version against
# every item here and grade the responses. Here it's mocked for determinism.
GOLDEN_DATASET = [
    {"input": "vacation days after 2 years", "expected": "18"},
    {"input": "parental leave weeks", "expected": "12"},
    {"input": "remote work days per week", "expected": "2"},
]


def mock_score_prompt(prompt_version: str) -> float:
    """
    Mock scorer: pretend each prompt version has a fixed 'quality' score,
    for deterministic grading of this exercise. In a real system this would
    call the model with `prompt_version` as the system prompt and score its
    answers against GOLDEN_DATASET (e.g. with the LLM-as-judge rubric from
    Session 5.2).
    """
    scores = {
        "v1_baseline": 0.92,
        "v2_friendlier_tone": 0.78,   # regression: friendlier wording hurt precision
        "v3_friendlier_fixed": 0.90,
    }
    return scores.get(prompt_version, 0.5)


def check_regression(new_version: str, baseline_version: str, threshold_drop: float = 0.05) -> Dict:
    """
    TODO 1: Build the CI regression check.

    Steps:
      1. Score `new_version` and `baseline_version` with mock_score_prompt.
      2. Compute the drop: baseline_score - new_score.
         (A negative drop means the new version actually improved.)
      3. Decide "passed": False if drop exceeds threshold_drop, True otherwise.
      4. Build a one-line human-readable `message` summarizing the result --
         something you'd be happy to see in a CI log (include both scores,
         the drop, and the threshold).
      5. Return a dict with exactly these keys:
         {"new_score": float, "baseline_score": float, "passed": bool, "message": str}

    Hint: format scores as percentages in the message, e.g. f"{score:.0%}".
    """
    raise NotImplementedError


if __name__ == "__main__":
    # A version that regressed -- should fail the gate.
    result = check_regression("v2_friendlier_tone", baseline_version="v1_baseline")
    print(result["message"])
    assert result["passed"] is False, "v2_friendlier_tone should FAIL against v1_baseline"

    # A version that fixed the regression -- should pass the gate.
    result = check_regression("v3_friendlier_fixed", baseline_version="v1_baseline")
    print(result["message"])
    assert result["passed"] is True, "v3_friendlier_fixed should PASS against v1_baseline"

    print("\nAll checks ran. If you see this with no AssertionError, the gate works.")
