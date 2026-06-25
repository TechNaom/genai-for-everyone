"""
Exercise — Session 1.6: Week 1 Lab — Mini Build Day

"Explain It To Me Simply" Tool.

Integrates: generative output (1.1), context shaping (1.2), model choice (1.3),
request/response mechanics (1.4), and honest hallucination-risk flagging (1.5).

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run:
  python explainer.py --topic "black holes" --level beginner
  python explainer.py --topic "black holes" --level professional
  python explainer.py --topic "black holes" --level expert
"""

import argparse
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

# A fast, low-cost tier is the right choice for this task (Session 1.3 judgment):
# this isn't a frontier-reasoning task, it's a well-scoped explanation task.
MODEL_NAME = "claude-haiku-4-5-20251001"

# TODO: Design the three system prompts below. Each should specify concrete
# behavioral instructions, not just "explain simply" — see this session's
# chapter, Part 2, for the "done technically" vs. "done well" distinction.
#
# Think about, for each level:
#   - What vocabulary is appropriate or forbidden?
#   - What kind of analogy should be used (if any)?
#   - What background knowledge can you assume?
#   - How long should the explanation be?

SYSTEM_PROMPTS = {
    "beginner": None,        # TODO: write this system prompt
    "professional": None,    # TODO: write this system prompt
    "expert": None,          # TODO: write this system prompt
}

# Words/patterns that suggest a topic or explanation contains specific,
# independently-verifiable claims worth flagging (Session 1.5's lesson).
# This is intentionally simple — not a robust fact-checker, just a basic
# heuristic flag.
VERIFICATION_FLAG_KEYWORDS = ["study", "statistic", "percent", "%", "according to", "exactly"]


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def needs_verification_flag(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in VERIFICATION_FLAG_KEYWORDS)


def explain(client, topic: str, level: str) -> str:
    system_prompt = SYSTEM_PROMPTS.get(level)
    if not system_prompt:
        raise ValueError(f"No system prompt defined for level: {level}")

    # TODO: construct and send the request.
    # You need: model=MODEL_NAME, max_tokens=400, system=system_prompt,
    # and a messages list with a single user turn asking to explain `topic`.
    # response = client.messages.create(...)
    # return response.content[0].text

    raise NotImplementedError("Fill in the TODO above before running.")


def main():
    parser = argparse.ArgumentParser(description="Explain a topic, calibrated to an audience level.")
    parser.add_argument("--topic", required=True, help="The topic to explain")
    parser.add_argument("--level", required=True, choices=["beginner", "professional", "expert"],
                         help="Audience level")
    args = parser.parse_args()

    client = get_client()
    explanation = explain(client, args.topic, args.level)

    print(f"\n--- Explanation of '{args.topic}' for: {args.level} ---\n")
    print(explanation)

    # TODO: check the explanation (or the topic) for verification-worthy
    # content using needs_verification_flag(), and if flagged, print a
    # short, non-alarmist note suggesting the user double-check specific
    # factual claims.


if __name__ == "__main__":
    main()
