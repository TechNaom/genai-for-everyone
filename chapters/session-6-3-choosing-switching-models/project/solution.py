"""
Session 6.3 Project: The Fallback Rate Monitor -- reference solution.

Run: python solution.py
"""

import random
import time
from typing import Dict, List


def _call_primary(prompt: str) -> Dict:
    """Mock primary provider: strong, but simulates a 25% outage rate."""
    if random.random() < 0.25:
        raise ConnectionError("primary: simulated outage")
    time.sleep(0.03)
    return {"text": f"[primary] answer to: {prompt}", "cost": 0.03, "latency_ms": 30}


def _call_secondary(prompt: str) -> Dict:
    """Mock secondary provider: always available, a bit weaker/cheaper."""
    time.sleep(0.015)
    return {"text": f"[secondary] answer to: {prompt}", "cost": 0.008, "latency_ms": 15}


PROVIDERS = {"primary": _call_primary, "secondary": _call_secondary}

CALL_LOG: List[Dict] = []


def call_model(prompt: str, provider: str = "primary") -> Dict:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider!r}. Known providers: {list(PROVIDERS)}")
    return PROVIDERS[provider](prompt)


def call_model_with_fallback(prompt: str, primary: str, fallback: str) -> Dict:
    try:
        result = call_model(prompt, provider=primary)
        result["used_provider"] = primary
        CALL_LOG.append({"prompt": prompt, "used_provider": primary, "fell_back": False})
        return result
    except ConnectionError as e:
        result = call_model(prompt, provider=fallback)
        used = f"{fallback} (fallback from {primary})"
        result["used_provider"] = used
        CALL_LOG.append(
            {
                "prompt": prompt,
                "used_provider": used,
                "fell_back": True,
                "primary_error": str(e),
            }
        )
        return result


def measure_fallback_rate(n_calls: int = 50) -> None:
    start_index = len(CALL_LOG)  # so re-running doesn't double-count earlier calls
    for i in range(n_calls):
        call_model_with_fallback(f"request #{i}", primary="primary", fallback="secondary")

    window = CALL_LOG[start_index:]
    fallback_count = sum(1 for entry in window if entry["fell_back"])
    rate = fallback_count / len(window) * 100

    print(f"Fallback triggered on {fallback_count}/{len(window)} calls "
          f"({rate:.1f}%) -- expect roughly 25% given primary's simulated outage rate")


if __name__ == "__main__":
    print("=== Single call with fallback ===")
    result = call_model_with_fallback("What is a circuit breaker?", primary="primary", fallback="secondary")
    print(result)

    print("\n=== Measuring the fallback rate over many calls ===")
    measure_fallback_rate(50)
