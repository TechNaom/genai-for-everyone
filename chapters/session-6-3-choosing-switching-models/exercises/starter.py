"""
Session 6.3 Exercises: The Model Adapter
See README.md in this folder for the full brief.

Build a thin adapter layer over two mocked model providers, then run the same
task across both and compare cost, latency, and quality -- the exact habit
that makes switching providers (or adding a fallback) cheap later instead of
a codebase-wide rewrite.

No API key, no internet access, no external libraries needed -- this is a
fully offline exercise with the "outage" simulated in-process.

Run: python starter.py
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
    """
    TODO 1: look up the provider function in PROVIDERS and call it.
    Raise a clear ValueError if the provider name isn't recognized -- don't
    let an unknown provider fail silently or return None.
    """
    raise NotImplementedError


def build_comparison_table(prompt: str) -> None:
    """
    TODO 2: call every provider in PROVIDERS once with `prompt`, and print a
    side-by-side comparison of cost, latency_ms, and a short subjective
    quality_note for each (e.g. "solid, slightly slower" / "fast, terser
    answers"). If a provider raises a ConnectionError, note that it failed
    instead of crashing the whole comparison.
    """
    raise NotImplementedError


QUALITY_NOTES = {
    "provider_a": "solid, more detailed answers -- but occasionally unavailable",
    "provider_b": "fast and cheap, terser answers",
}


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
