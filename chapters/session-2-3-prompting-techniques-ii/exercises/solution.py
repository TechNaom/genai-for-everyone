"""
Reference solution — Session 2.3: Prompting Techniques II

Includes the independently-verified ground truth so you can check both
model responses against a real answer, not just against each other.

VERIFIED GROUND TRUTH (worked by hand, shown here for reference):
  Effective hours per agent after 30-min break: 10 - 0.5 = 9.5 hours
  Total daily capacity: 12 agents x 8 calls/hr x 9.5 hrs = 912 calls
  Calls abandoned: 850 x 0.15 = 127.5
  Calls handled: 850 - 127.5 = 722.5
  Total cost of handled calls: 722.5 x $2.50 = $1,806.25
  Percentage of capacity used: 722.5 / 912 = 79.22%

NOTE: the fractional "722.5 calls" is a realistic artifact of applying a
percentage to a whole-number count — worth noticing if a model's reasoning
either ignores this oddity or gets confused by it.
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"

PROBLEM = """A call center has 12 agents. Each agent can handle 8 calls per
hour. The center operates 10 hours per day. Average cost to handle a call is
$2.50. On a particular day, the center received 850 calls, but 15% of calls
were abandoned before being answered (no cost for abandoned calls).
Additionally, each agent gets a 30-minute paid break, which reduces their
effective working hours for the day.

What is the total cost of handled calls that day, and what percentage of
total daily capacity was actually used (calls handled / total capacity)?"""

DIRECT_PROMPT = f"{PROBLEM}\n\nGive only the final numeric answers."

COT_PROMPT = f"""{PROBLEM}

Think through this step by step:
1. First calculate each agent's effective working hours after their break.
2. Then calculate total daily capacity in calls.
3. Then calculate how many calls were actually handled (not abandoned).
4. Then calculate the total cost of handled calls.
5. Finally calculate the percentage of capacity used.

Show each step, then give your final answer."""

GROUND_TRUTH = {
    "effective_hours_per_agent": 9.5,
    "total_capacity": 912.0,
    "calls_abandoned": 127.5,
    "calls_handled": 722.5,
    "total_cost": 1806.25,
    "pct_capacity_used": 79.22,
}


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Set it as an environment variable "
              "(or in a local, un-committed .env file) before running this.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def ask(client, prompt: str) -> str:
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main():
    client = get_client()

    print("=== DIRECT PROMPT RESPONSE ===\n")
    print(ask(client, DIRECT_PROMPT))

    print("\n\n=== CHAIN-OF-THOUGHT PROMPT RESPONSE ===\n")
    print(ask(client, COT_PROMPT))

    print("\n\n=== VERIFIED GROUND TRUTH (computed independently) ===")
    for key, value in GROUND_TRUTH.items():
        print(f"  {key}: {value}")

    print(
        "\nCompare both responses against this ground truth, not just against "
        "each other. A common failure pattern in the DIRECT version is skipping "
        "the break-time adjustment to capacity entirely, or applying the "
        "abandonment rate to the wrong base number."
    )


if __name__ == "__main__":
    main()
