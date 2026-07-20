"""
Session 2.3 Project: Self-Consistency Checker — reference solution.

Asks a real model the same question several times (with sampling randomness
enabled), extracts a comparable short answer from each response, and detects
whether the answers converge or diverge — the core mechanic behind
self-consistency prompting from this session.

Setup:
  pip install anthropic python-dotenv
  Set the ANTHROPIC_API_KEY environment variable (or put it in a local .env
  file that you do NOT commit) with your own API key.

Run: python solution.py
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

FINAL_ANSWER_RE = re.compile(r"final answer\s*:\s*(.+)", re.IGNORECASE)


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
    prompt = question + ANSWER_FORMAT_INSTRUCTION
    return [query_once(client, prompt) for _ in range(n)]


def extract_answer(response_text: str) -> str:
    """Pull the short answer out of a 'Final answer: ...' line."""
    match = FINAL_ANSWER_RE.search(response_text)
    if not match:
        return "UNPARSEABLE"
    answer = match.group(1).strip()
    # Drop a trailing period/exclamation if the model added one.
    answer = answer.rstrip(".!")
    # Normalize whitespace so "0.05" and "0.05 " tally as the same answer.
    return " ".join(answer.split())


def check_convergence(answers: list[str]) -> tuple[str, float, Counter]:
    """Return (majority_answer, convergence_ratio, full_tally) for a list of answers."""
    tally = Counter(answers)
    winner, votes = tally.most_common(1)[0]
    convergence_ratio = votes / len(answers)
    return winner, convergence_ratio, tally


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
