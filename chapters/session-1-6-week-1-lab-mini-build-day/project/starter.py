"""
Week 1 Capstone Project — "Explain It To Me Simply"

This is the week's main deliverable: one complete tool that touches every idea
from Week 1 — generative output (1.1), context shaping (1.2), model choice
(1.3), request/response mechanics (1.4), and honest hallucination-risk
flagging (1.5).

Follow the six build steps from the lesson. The scaffold below marks the parts
that integrate this week's concepts with TODOs. The heart of the build is the
three system prompts — that's where "done well" and "done technically" diverge.

Setup (only needed for a LIVE explanation):
  pip install anthropic python-dotenv
  Copy .env.example (repo root) to .env and add your ANTHROPIC_API_KEY

Run a live explanation:
  python starter.py --topic "black holes" --level beginner

Run with no arguments for an offline self-check (no API key needed):
  python starter.py
"""

import argparse
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

# Step 3 (model choice): a fast, low-cost tier fits this well-scoped explanation
# task — you don't need a frontier-reasoning model here (Session 1.3 judgment).
MODEL_NAME = "claude-haiku-4-5-20251001"

# --- Steps 1 & 2: design the three audience levels and their system prompts ---
# TODO: replace each None with a system prompt full of CONCRETE behavioral
# instructions (banned jargon, required analogy type, assumed background,
# target length) — not just "explain simply".
SYSTEM_PROMPTS = {
    "beginner": None,        # TODO: curious 10-year-old, one everyday analogy, no jargon, 3-4 sentences
    "professional": None,    # TODO: working professional, moderate vocabulary, practical framing, 4-6 sentences
    "expert": None,          # TODO: domain expert, precise terminology, skip basics, 2-4 sentences
}

# --- Step 5: honesty flag (Session 1.5). Intentionally a simple heuristic. ---
VERIFICATION_FLAG_KEYWORDS = ["study", "statistic", "percent", "%", "according to", "exactly"]


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    if Anthropic is None:
        print("The 'anthropic' package isn't installed. Run: pip install anthropic")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def needs_verification_flag(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in VERIFICATION_FLAG_KEYWORDS)


def explain(client, topic: str, level: str) -> str:
    system_prompt = SYSTEM_PROMPTS.get(level)
    if not system_prompt:
        raise ValueError(f"No system prompt defined for level: {level} (did you fill in the TODO?)")

    # Step 4 (Session 1.4): construct the request with the right roles, send it,
    # and parse the response.
    # TODO: call client.messages.create(model=MODEL_NAME, max_tokens=400,
    #       system=system_prompt, messages=[{"role": "user",
    #       "content": f"Explain: {topic}"}]) and return response.content[0].text
    raise NotImplementedError("Fill in the TODO in explain() before running a live topic.")


def offline_self_check():
    """Runs with no API key. Reports unfilled TODOs and exercises the honesty flag."""
    print("=== Offline self-check (no API key needed) ===\n")

    unfilled = [level for level, prompt in SYSTEM_PROMPTS.items() if not prompt]
    if unfilled:
        print("System prompts still TODO for: " + ", ".join(unfilled))
        print("Write each with concrete behavioral instructions, then test all three levels.\n")
    else:
        print("All three system prompts are filled in — try a live topic next.\n")

    print("Step 5's honesty flag needs no API. Here it is running now:")
    for s in ["A 2020 study found 63 percent of cells react.",
              "Gravity pulls things toward the ground."]:
        print(f"  needs_verification_flag({s!r}) -> {needs_verification_flag(s)}")

    print(
        "\nWhen your prompts are written and you have an API key, run e.g.:\n"
        "  python starter.py --topic \"quantum entanglement\" --level beginner"
    )


def main():
    parser = argparse.ArgumentParser(description="Explain a topic, calibrated to an audience level.")
    parser.add_argument("--topic", help="The topic to explain")
    parser.add_argument("--level", choices=["beginner", "professional", "expert"],
                        help="Audience level")
    args = parser.parse_args()

    if not args.topic:
        offline_self_check()
        return

    if not args.level:
        print("Provide --level (beginner, professional, or expert) with --topic.")
        sys.exit(1)

    client = get_client()
    explanation = explain(client, args.topic, args.level)

    print(f"\n--- Explanation of '{args.topic}' for: {args.level} ---\n")
    print(explanation)

    # TODO (Step 5): if needs_verification_flag() is true for the explanation or
    # the topic, print a short, non-alarmist note to double-check specific claims.


if __name__ == "__main__":
    main()
