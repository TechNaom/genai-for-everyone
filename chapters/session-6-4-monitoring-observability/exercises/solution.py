"""
Reference solution -- Session 6.4: Monitoring & Observability

Run: python3 solution.py
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
    time.sleep(0.01)
    output = f"Answer to: {user_input}"
    return {
        "output": output,
        "latency_ms": random.randint(100, 900),
        "input_tokens": len(user_input.split()) * 2,
        "output_tokens": len(output.split()) * 2,
    }


def logged_call(user_input: str) -> Dict:
    result = mock_service_call(user_input)
    REQUEST_LOG.append({
        "input": user_input,
        "output": result["output"],
        "latency_ms": result["latency_ms"],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
    })
    return result


def print_stats():
    if not REQUEST_LOG:
        print("No requests logged yet.")
        return
    total = len(REQUEST_LOG)
    avg_latency = sum(r["latency_ms"] for r in REQUEST_LOG) / total
    total_tokens = sum(r["input_tokens"] + r["output_tokens"] for r in REQUEST_LOG)
    print("=== STATS ===")
    print(f"Total requests: {total}")
    print(f"Average latency: {avg_latency:.0f}ms")
    print(f"Total tokens (in+out): {total_tokens}")


def log_feedback(request_index: int, thumbs_up: bool):
    FEEDBACK_LOG.append({"request_index": request_index, "thumbs_up": thumbs_up})


def check_drift(score_fn, threshold: float = 0.8) -> bool:
    results = [score_fn(ex["input"], ex["expected"]) for ex in GOLDEN_DATASET]
    pass_rate = sum(results) / len(results)
    print(f"\n=== DRIFT CHECK === pass rate: {pass_rate:.0%} (threshold: {threshold:.0%})")
    if pass_rate < threshold:
        print("WARNING: drift detected -- pass rate dropped below threshold.")
        return False
    print("No drift detected.")
    return True


if __name__ == "__main__":
    for q in ["vacation days after 2 years", "parental leave policy", "how do I expense travel?"]:
        logged_call(q)

    print_stats()

    log_feedback(0, thumbs_up=True)
    log_feedback(1, thumbs_up=False)
    print(f"\nFeedback log: {FEEDBACK_LOG}")

    def mock_score(user_input, expected):
        return random.random() > 0.1

    check_drift(mock_score)
