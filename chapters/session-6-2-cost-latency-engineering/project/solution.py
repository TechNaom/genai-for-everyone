"""
Reference solution — Session 6.2 Project: The Routing Strategy

Run: python3 solution.py
"""

from typing import Dict, List

MODEL_PRICING = {
    "cheap":     {"input_per_million": 0.80,  "output_per_million": 4.00},
    "expensive": {"input_per_million": 15.00, "output_per_million": 75.00},
}

TOTAL_REQUESTS_PER_DAY = 50_000

REQUEST_TYPES = [
    {
        "name": "simple_faq",
        "share_of_traffic": 0.55,
        "avg_input_tokens": 150,
        "avg_output_tokens": 60,
    },
    {
        "name": "order_status_lookup",
        "share_of_traffic": 0.20,
        "avg_input_tokens": 300,
        "avg_output_tokens": 100,
    },
    {
        "name": "billing_dispute",
        "share_of_traffic": 0.15,
        "avg_input_tokens": 900,
        "avg_output_tokens": 250,
    },
    {
        "name": "multistep_technical_troubleshooting",
        "share_of_traffic": 0.10,
        "avg_input_tokens": 2200,
        "avg_output_tokens": 500,
    },
]


def cost_per_request(model: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing["input_per_million"]
    output_cost = (output_tokens / 1_000_000) * pricing["output_per_million"]
    return input_cost + output_cost


def requests_per_day_for_type(request_type: dict) -> float:
    return request_type["share_of_traffic"] * TOTAL_REQUESTS_PER_DAY


def daily_cost_for_type(request_type: dict, model: str) -> float:
    per_request = cost_per_request(
        model,
        request_type["avg_input_tokens"],
        request_type["avg_output_tokens"],
    )
    return per_request * requests_per_day_for_type(request_type)


def baseline_cost() -> float:
    return sum(daily_cost_for_type(rt, "expensive") for rt in REQUEST_TYPES)


def route_tier(request_type: dict, threshold_input_tokens: int) -> str:
    if request_type["avg_input_tokens"] < threshold_input_tokens:
        return "cheap"
    return "expensive"


def routed_cost(threshold_input_tokens: int) -> float:
    total = 0.0
    for rt in REQUEST_TYPES:
        tier = route_tier(rt, threshold_input_tokens)
        total += daily_cost_for_type(rt, tier)
    return total


def print_comparison(threshold_input_tokens: int):
    print(f"Routing threshold: requests under {threshold_input_tokens} avg input "
          f"tokens go to 'cheap'; everything else stays on 'expensive'.\n")

    print(f"{'Request type':<38} {'Share':>7} {'Avg in':>8} {'Routed to':>11}")
    for rt in REQUEST_TYPES:
        tier = route_tier(rt, threshold_input_tokens)
        print(f"{rt['name']:<38} {rt['share_of_traffic'] * 100:>6.0f}% "
              f"{rt['avg_input_tokens']:>8} {tier:>11}")

    baseline_daily = baseline_cost()
    routed_daily = routed_cost(threshold_input_tokens)
    baseline_monthly = baseline_daily * 30
    routed_monthly = routed_daily * 30
    savings_monthly = baseline_monthly - routed_monthly
    savings_pct = (savings_monthly / baseline_monthly) * 100

    print(f"\n{'':<20}{'Daily':>16}{'Monthly (x30)':>20}")
    print(f"{'Baseline (all expensive)':<20}{'$' + format(baseline_daily, ',.2f'):>16}"
          f"{'$' + format(baseline_monthly, ',.2f'):>20}")
    print(f"{'Routed':<20}{'$' + format(routed_daily, ',.2f'):>16}"
          f"{'$' + format(routed_monthly, ',.2f'):>20}")
    print(f"\nMonthly savings from routing: ${savings_monthly:,.2f} "
          f"({savings_pct:.1f}% reduction)")


if __name__ == "__main__":
    print("=== ROUTING STRATEGY: threshold = 500 input tokens ===")
    print_comparison(threshold_input_tokens=500)

    print("\n=== FOR COMPARISON: a tighter threshold (350 tokens) ===")
    print_comparison(threshold_input_tokens=350)
