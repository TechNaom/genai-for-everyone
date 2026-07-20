"""
Session 6.2 Project: The Routing Strategy
See README.md in this folder for the full brief.

This is the Pro path build for Session 6.2: given a realistic MIXED
workload -- some requests genuinely need your best model, most don't --
design and implement a routing strategy that sends simple requests to a
cheap model and complex requests to an expensive model, then report the
blended cost against an "everything goes to the expensive model" baseline.

No API key, no internet access, no external libraries needed -- this is
pure arithmetic on token counts and traffic shares, plain Python, runs
anywhere.

Run: python3 starter.py
"""

from typing import Dict, List

# Two model tiers, illustrative pricing (USD per MILLION tokens, input and
# output priced separately -- not live provider rates).
MODEL_PRICING = {
    "cheap":    {"input_per_million": 0.80,  "output_per_million": 4.00},
    "expensive": {"input_per_million": 15.00, "output_per_million": 75.00},
}

# A support chatbot's traffic, broken into representative request TYPES
# rather than one row per request. Each type carries the SHARE of total
# daily traffic it represents and its average token profile. This mirrors
# how you'd actually model a real production workload: a handful of
# distinct request patterns, each with a known (or estimated) volume share.
TOTAL_REQUESTS_PER_DAY = 50_000

REQUEST_TYPES = [
    {
        "name": "simple_faq",
        "share_of_traffic": 0.55,     # "What are your hours?" / "Where's my order?"
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
        "share_of_traffic": 0.15,     # needs real reasoning over account history
        "avg_input_tokens": 900,
        "avg_output_tokens": 250,
    },
    {
        "name": "multistep_technical_troubleshooting",
        "share_of_traffic": 0.10,     # long, multi-part, genuinely hard
        "avg_input_tokens": 2200,
        "avg_output_tokens": 500,
    },
]


def cost_per_request(model: str, input_tokens: int, output_tokens: int) -> float:
    """Same cost math as the Core path calculator -- reused here."""
    pricing = MODEL_PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing["input_per_million"]
    output_cost = (output_tokens / 1_000_000) * pricing["output_per_million"]
    return input_cost + output_cost


def requests_per_day_for_type(request_type: dict) -> float:
    """
    TODO 1: how many requests/day does this request type represent?
    Use request_type["share_of_traffic"] and TOTAL_REQUESTS_PER_DAY.
    """
    raise NotImplementedError


def daily_cost_for_type(request_type: dict, model: str) -> float:
    """
    TODO 2: total daily cost of serving ALL of this request type's traffic
    on the given model tier. Combine cost_per_request(...) with
    requests_per_day_for_type(...).
    """
    raise NotImplementedError


def baseline_cost() -> float:
    """
    TODO 3: the "everything to the expensive model" baseline -- sum
    daily_cost_for_type(request_type, "expensive") across every entry in
    REQUEST_TYPES.
    """
    raise NotImplementedError


def route_tier(request_type: dict, threshold_input_tokens: int) -> str:
    """
    TODO 4: the routing rule. Return "cheap" if this request type's
    avg_input_tokens is BELOW threshold_input_tokens, otherwise "expensive".
    This is the core design decision of the whole project -- keep it this
    simple for now; see the README for ideas on making it smarter.
    """
    raise NotImplementedError


def routed_cost(threshold_input_tokens: int) -> float:
    """
    TODO 5: total daily cost when every request type is routed according to
    route_tier(...) instead of always going to "expensive". Sum
    daily_cost_for_type(request_type, route_tier(request_type, threshold))
    across every entry in REQUEST_TYPES.
    """
    raise NotImplementedError


def print_comparison(threshold_input_tokens: int):
    """
    TODO 6: print a report showing, for the given threshold:
      - which request types got routed to "cheap" vs "expensive"
      - baseline daily/monthly cost (everything to expensive)
      - routed daily/monthly cost
      - dollar savings and percent savings, monthly
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("=== ROUTING STRATEGY: threshold = 500 input tokens ===")
    print_comparison(threshold_input_tokens=500)
