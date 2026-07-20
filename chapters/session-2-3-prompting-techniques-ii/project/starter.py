"""
Session 2.3 Project: Self-Consistency Checker
See README.md in this folder for the full brief and an example run.

The Pro path challenge for this session: implement a basic self-consistency
check. Ask a real model the same question several times (with sampling
randomness enabled), extract a comparable short answer from each response,
and detect whether the answers converge or diverge. Test it on an easy
question (expect high convergence) and a genuinely tricky one (expect more
divergence) to see the signal actually behave the way this chapter predicts.

Setup:
  pip install anthropic python-dotenv
  Set the ANTHROPIC_API_KEY environment variable (or put it in a local .env
  file that you do NOT commit) with your own API key.

Run: python starter.py
"""

import os
import re
import sys
from collections import Counter
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"
RUNS_PER_QUESTION = 5

# An easy question with one unambiguous correct answer -- expect the model
# to converge on the same final answer almost every run.
EASY_QUESTION = "What is 12 times 4?"

# The classic "bat and ball" cognitive-reflection question. The intuitive
# answer ($0.10) is wrong; the correct answer is $0.05. Models sometimes
# get pulled toward the intuitive-but-wrong answer, so runs can genuinely
# diverge here -- a good stand-in for a "tricky" case.
TRICKY_QUESTION = (
    "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than "
    "the ball. How much does the ball cost?"
)

ANSWER_FORMAT_INSTRUCTION = (
    "\n\nShow your reasoning briefly, then end your response with exactly "
    "one line in this format: Final answer: <your answer>"
)


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Set it as an environment variable "
              "(or in a local, un-committed .env file) before running this.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def query_once(client, prompt: str) -> str:
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=400,
        temperature=1.0,  # sampling randomness -- required for runs to differ
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def query_n_times(client, question: str, n: int = RUNS_PER_QUESTION) -> list[str]:
    """Ask the same question n independent times and return the raw responses."""
    # TODO 1: call query_once() n times with the same prompt (question +
    # ANSWER_FORMAT_INSTRUCTION) and return a list of the raw response
    # strings. Each call is independent -- don't reuse a previous answer.
    return []


def extract_answer(response_text: str) -> str:
    """Pull the short answer out of a 'Final answer: ...' line."""
    # TODO 2: search response_text for a line matching "Final answer: X" and
    # return X, stripped of whitespace and any trailing punctuation. If no
    # such line is found, return "UNPARSEABLE" instead of crashing.
    return "UNPARSEABLE"


def check_convergence(answers: list[str]) -> tuple[str, float, Counter]:
    """Return (majority_answer, convergence_ratio, full_tally) for a list of answers."""
    # TODO 3: use collections.Counter to tally the answers, find the most
    # common one, and compute convergence_ratio = votes for the winner /
    # total number of answers. Return all three.
    return "", 0.0, Counter()


def run_self_consistency_check(client, label: str, question: str):
    print(f"=== {label} ===")
    print(f"Question: {question}\n")

    raw_responses = query_n_times(client, question)
    answers = [extract_answer(r) for r in raw_responses]
    winner, convergence, tally = check_convergence(answers)

    print(f"{len(answers)} runs, extracted answers: {answers}")
    print(f"Tally: {dict(tally)}")
    print(f"Majority answer: {winner!r}  (convergence: {convergence:.0%})")

    if convergence >= 0.8:
        print("-> High convergence: treat this as a reasonably reliable answer.")
    elif convergence >= 0.5:
        print("-> Moderate convergence: worth a second look before trusting it.")
    else:
        print("-> Low convergence: this is a genuinely hard case for the model.")
        print("   Don't trust any single run at face value -- get a human to check.")
    print()


def main():
    client = get_client()
    run_self_consistency_check(client, "EASY QUESTION", EASY_QUESTION)
    run_self_consistency_check(client, "TRICKY QUESTION", TRICKY_QUESTION)

    print("Compare the two convergence percentages above. If the easy question")
    print("converged much more than the tricky one, that's the self-consistency")
    print("signal from this chapter behaving exactly as predicted.")


if __name__ == "__main__":
    main()
