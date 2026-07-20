"""
Session 6.3 Exercises: The Model Adapter -- reference solution.

Run: python solution.py
"""

import random
import time
from typing import Dict


def _call_provider_a(prompt: str) -> Dict:
    """Mock 'strong but occasionally unavailable' provider."""
    if random.random() < 0.3:  # simulate a 30% outage rate for the exercise
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


QUALITY_NOTES = {
    "provider_a": "solid, more detailed answers -- but occasionally unavailable",
    "provider_b": "fast and cheap, terser answers",
}


def build_comparison_table(prompt: str) -> None:
    rows = []
    for provider in PROVIDERS:
        try:
            result = call_model(prompt, provider=provider)
            rows.append(
                {
                    "provider": provider,
                    "cost": f"${result['cost']:.3f}",
                    "latency_ms": result["latency_ms"],
                    "quality_note": QUALITY_NOTES[provider],
                }
            )
        except ConnectionError as e:
            rows.append(
                {
                    "provider": provider,
                    "cost": "n/a",
                    "latency_ms": "n/a",
                    "quality_note": f"FAILED this run ({e})",
                }
            )

    header = f"{'Provider':<12} {'Cost':<10} {'Latency':<10} Quality note"
    print(header)
    print("-" * len(header))
    for row in rows:
        latency = f"{row['latency_ms']}ms" if row["latency_ms"] != "n/a" else "n/a"
        print(f"{row['provider']:<12} {row['cost']:<10} {latency:<10} {row['quality_note']}")


if __name__ == "__main__":
    print("=== Comparing providers directly ===")
    for provider in PROVIDERS:
        try:
            result = call_model("What is RAG?", provider=provider)
            print(f"{provider}: {result}")
        except ConnectionError as e:
            print(f"{provider}: FAILED — {e}")

    print("\n=== Cost / latency / quality comparison table ===")
    build_comparison_table("Summarize the key trade-offs of self-hosting a model.")
