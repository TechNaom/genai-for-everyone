"""
Reference solution — Session 6.3: Choosing & Switching Models — Adapter + Fallback

Run: python3 model_switching_solution.py
"""

import random
import time
from typing import Dict


def _call_provider_a(prompt: str) -> Dict:
    """Mock 'strong but occasionally unavailable' provider."""
    if random.random() < 0.3:
        raise ConnectionError("provider_a: simulated outage")
    time.sleep(0.05)
    return {"text": f"[provider_a] answer to: {prompt}", "cost": 0.02, "latency_ms": 50}


def _call_provider_b(prompt: str) -> Dict:
    """Mock 'faster, cheaper, slightly weaker' provider."""
    time.sleep(0.02)
    return {"text": f"[provider_b] answer to: {prompt}", "cost": 0.005, "latency_ms": 20}


PROVIDERS = {"provider_a": _call_provider_a, "provider_b": _call_provider_b}


def call_model(prompt: str, provider: str = "provider_a") -> Dict:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider!r}. Known providers: {list(PROVIDERS)}")
    return PROVIDERS[provider](prompt)


def call_model_with_fallback(prompt: str, primary: str, fallback: str) -> Dict:
    try:
        result = call_model(prompt, provider=primary)
        result["used_provider"] = primary
        return result
    except ConnectionError:
        result = call_model(prompt, provider=fallback)
        result["used_provider"] = f"{fallback} (fallback from {primary})"
        return result


if __name__ == "__main__":
    print("=== Comparing providers directly ===")
    for provider in PROVIDERS:
        try:
            result = call_model("What is RAG?", provider=provider)
            print(f"{provider}: {result}")
        except ConnectionError as e:
            print(f"{provider}: FAILED — {e}")

    print("\n=== With fallback (run several times to see the fallback trigger) ===")
    fallback_used_count = 0
    for _ in range(20):
        result = call_model_with_fallback("What is RAG?", primary="provider_a", fallback="provider_b")
        if "fallback" in result["used_provider"]:
            fallback_used_count += 1
    print(f"Fallback triggered on {fallback_used_count}/20 calls "
          f"(expect roughly 30% given provider_a's simulated outage rate)")
