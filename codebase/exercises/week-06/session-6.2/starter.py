"""
Session 6.2: Cost & Latency Engineering — Cost Calculator

Task: given a workload (requests/day, avg input/output tokens), compute
daily/monthly cost across model tiers, then show the cost impact of one
optimization.

Run: python3 starter.py
"""

from typing import Dict

# Illustrative per-million-token prices (USD). Not live pricing — replace with
# current provider pricing if you want exact real-world numbers.
MODEL_PRICING = {
    "small":  {"input_per_million": 0.80,  "output_per_million": 4.00},
    "medium": {"input_per_million": 3.00,  "output_per_million": 15.00},
    "large":  {"input_per_million": 15.00, "output_per_million": 75.00},
}


def cost_per_request(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    TODO 1: compute the dollar cost of a single request for the given model tier.
    Remember: prices above are PER MILLION TOKENS.
    """
    raise NotImplementedError


def daily_cost(model: str, requests_per_day: int, avg_input_tokens: int, avg_output_tokens: int) -> float:
    """TODO 2: compute total daily cost for a workload on a given model tier."""
    raise NotImplementedError


def compare_models(requests_per_day: int, avg_input_tokens: int, avg_output_tokens: int) -> Dict[str, float]:
    """TODO 3: return {model_tier: daily_cost} for every tier in MODEL_PRICING."""
    raise NotImplementedError


def print_report(requests_per_day: int, avg_input_tokens: int, avg_output_tokens: int):
    # TODO 4: print a clear report: daily cost per tier, monthly cost per tier (x30)
    raise NotImplementedError


if __name__ == "__main__":
    print("=== BASELINE WORKLOAD ===")
    print_report(requests_per_day=50_000, avg_input_tokens=1500, avg_output_tokens=300)

    print("\n=== OPTIMIZATION: shorter prompts (1500 -> 600 input tokens) ===")
    # TODO 5: print the same report with reduced input tokens and compare the
    # monthly savings against the baseline on the "medium" model tier.
    raise NotImplementedError
