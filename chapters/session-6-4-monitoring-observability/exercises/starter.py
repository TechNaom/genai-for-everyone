"""
Exercise -- Session 6.4: Monitoring & Observability

Task: log every request to a mock service, then report aggregate stats.
Bonus (optional, same shape as the Pro-path project): a feedback log and a
drift check against a golden dataset.

Run: python3 starter.py
"""

import random
import time
from typing import Dict, List

REQUEST_LOG: List[Dict] = []
FEEDBACK_LOG: List[Dict] = []

GOLDEN_DATASET = [
    {"input": "vacation days after 2 years", "expected": "18 days"},
    {"input": "parental leave policy", "expected": "12 weeks paid"},
    {"input": "remote work policy", "expected": "hybrid, 3 days in office"},
]


def mock_service_call(user_input: str) -> Dict:
    """Simulates calling a live GenAI service; randomizes latency/tokens for realism."""
    time.sleep(0.01)
    output = f"Answer to: {user_input}"
    return {
        "output": output,
        "latency_ms": random.randint(100, 900),
        "input_tokens": len(user_input.split()) * 2,
        "output_tokens": len(output.split()) * 2,
    }


def logged_call(user_input: str) -> Dict:
    """
    TODO 1: call mock_service_call, then append a log entry to REQUEST_LOG
    containing: input, output, latency_ms, input_tokens, output_tokens.
    Return the result.
    """
    raise NotImplementedError


def print_stats():
    """
    TODO 2: using REQUEST_LOG, print: total requests, average latency,
    total input+output tokens.
    """
    raise NotImplementedError


def log_feedback(request_index: int, thumbs_up: bool):
    """TODO 3 (bonus): append {request_index, thumbs_up} to FEEDBACK_LOG."""
    raise NotImplementedError


def check_drift(score_fn, threshold: float = 0.8) -> bool:
    """
    TODO 4 (bonus): re-score GOLDEN_DATASET using score_fn(input, expected) -> bool,
    compute pass rate, print it, and return True if pass rate >= threshold else False.
    """
    raise NotImplementedError


if __name__ == "__main__":
    for q in ["vacation days after 2 years", "parental leave policy", "how do I expense travel?"]:
        logged_call(q)

    print_stats()

    log_feedback(0, thumbs_up=True)
    log_feedback(1, thumbs_up=False)

    def mock_score(user_input, expected):
        # In a real system, this compares live service output to `expected`.
        return random.random() > 0.1

    check_drift(mock_score)
