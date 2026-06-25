"""
Exercise — Session 2.3: Prompting Techniques II

Multi-Step Reasoning Prompt: Direct vs. Chain-of-Thought.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python reasoning_compare.py
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"

# A genuinely multi-step problem with several compound calculations,
# chosen so that skipping or misordering a step produces a wrong answer.
PROBLEM = """A call center has 12 agents. Each agent can handle 8 calls per
hour. The center operates 10 hours per day. Average cost to handle a call is
$2.50. On a particular day, the center received 850 calls, but 15% of calls
were abandoned before being answered (no cost for abandoned calls).
Additionally, each agent gets a 30-minute paid break, which reduces their
effective working hours for the day.

What is the total cost of handled calls that day, and what percentage of
total daily capacity was actually used (calls handled / total capacity)?"""


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
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

    # TODO: write a DIRECT prompt — just the problem, asking for the final
    # answer, with no instruction to show reasoning steps.
    direct_prompt = None  # TODO

    # TODO: write a CHAIN-OF-THOUGHT prompt — the same problem, but
    # explicitly instructing the model to work through it step by step
    # before giving a final answer.
    cot_prompt = None  # TODO

    if not direct_prompt or not cot_prompt:
        print("Fill in direct_prompt and cot_prompt before running.")
        sys.exit(1)

    print("=== DIRECT PROMPT RESPONSE ===\n")
    print(ask(client, direct_prompt))

    print("\n\n=== CHAIN-OF-THOUGHT PROMPT RESPONSE ===\n")
    print(ask(client, cot_prompt))

    print("\n\n--- Now check both answers yourself ---")
    print("Work out the correct total cost and capacity percentage by hand")
    print("(or with a calculator), then compare. Which prompt got it right?")
    print("If they differ, where in the chain-of-thought version (if shown)")
    print("did things go right or wrong?")


if __name__ == "__main__":
    main()
