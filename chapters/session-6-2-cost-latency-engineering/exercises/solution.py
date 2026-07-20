"""
Reference solution — Session 6.2 Exercise: The Cost Calculator

Run: python3 solution.py
"""

from typing import Dict

MODEL_PRICING = {
    "small":  {"input_per_million": 0.80,  "output_per_million": 4.00},
    "medium": {"input_per_million": 3.00,  "output_per_million": 15.00},
    "large":  {"input_per_million": 15.00, "output_per_million": 75.00},
}


def cost_per_request(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing["input_per_million"]
    output_cost = (output_tokens / 1_000_000) * pricing["output_per_million"]
    return input_cost + output_cost


def daily_cost(model: str, requests_per_day: int, avg_input_tokens: int, avg_output_tokens: int) -> float:
    per_request = cost_per_request(model, avg_input_tokens, avg_output_tokens)
    return per_request * requests_per_day


def compare_models(requests_per_day: int, avg_input_tokens: int, avg_output_tokens: int) -> Dict[str, float]:
    return {
        model: daily_cost(model, requests_per_day, avg_input_tokens, avg_output_tokens)
        for model in MODEL_PRICING
    }


def print_report(requests_per_day: int, avg_input_tokens: int, avg_output_tokens: int):
    print(f"Workload: {requests_per_day:,} requests/day, "
          f"avg {avg_input_tokens} input / {avg_output_tokens} output tokens")
    print(f"{'Model':<10} {'Daily cost':>14} {'Monthly cost (x30)':>22}")
    for model, cost in compare_models(requests_per_day, avg_input_tokens, avg_output_tokens).items():
        print(f"{model:<10} ${cost:>12,.2f} ${cost * 30:>20,.2f}")


if __name__ == "__main__":
    print("=== BASELINE WORKLOAD ===")
    print_report(requests_per_day=50_000, avg_input_tokens=1500, avg_output_tokens=300)

    print("\n=== OPTIMIZATION: shorter prompts (1500 -> 600 input tokens) ===")
    print_report(requests_per_day=50_000, avg_input_tokens=600, avg_output_tokens=300)

    baseline_medium = daily_cost("medium", 50_000, 1500, 300)
    optimized_medium = daily_cost("medium", 50_000, 600, 300)
    monthly_savings = (baseline_medium - optimized_medium) * 30
    print(f"\nMedium-tier monthly savings from prompt trimming: ${monthly_savings:,.2f}")
