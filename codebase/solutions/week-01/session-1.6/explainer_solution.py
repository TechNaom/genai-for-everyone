"""
Reference solution — Session 1.6: Week 1 Lab — Mini Build Day

"Explain It To Me Simply" Tool, fully implemented, including the Pro path's
comparison mode (--compare flag runs all three levels side by side).

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run:
  python explainer_solution.py --topic "black holes" --level beginner
  python explainer_solution.py --topic "black holes" --compare
"""

import argparse
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"

SYSTEM_PROMPTS = {
    "beginner": (
        "You explain things to a curious 10-year-old with no background knowledge. "
        "Use ONE simple, everyday analogy (something from daily life, toys, animals, "
        "or food). NEVER use jargon or technical terms without immediately explaining "
        "them in plain words. Keep it to 3-4 short sentences. Be warm and encouraging."
    ),
    "professional": (
        "You explain things to an intelligent working professional with no specialized "
        "background in this specific topic. You can use moderate vocabulary and assume "
        "general education, but avoid deep technical jargon unless you define it. Use "
        "a practical, real-world framing where possible. Aim for 4-6 sentences."
    ),
    "expert": (
        "You give a quick, dense refresher to someone with deep domain expertise in "
        "this field. Skip all basic setup and definitions they would already know. "
        "Use precise field-specific terminology freely. Focus on nuance, recent context, "
        "or a non-obvious angle rather than restating fundamentals. 2-4 sentences."
    ),
}

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
    system_prompt = SYSTEM_PROMPTS[level]
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=400,
        system=system_prompt,
        messages=[{"role": "user", "content": f"Explain: {topic}"}],
    )
    return response.content[0].text


def print_with_flag(topic, level, explanation):
    print(f"\n--- Explanation of '{topic}' for: {level} ---\n")
    print(explanation)
    if needs_verification_flag(explanation) or needs_verification_flag(topic):
        print(
            "\n[Note: this explanation includes specific claims, statistics, or "
            "studies. Worth independently verifying anything you plan to rely on "
            "or repeat — see Session 1.5 on why.]"
        )


def main():
    parser = argparse.ArgumentParser(description="Explain a topic, calibrated to an audience level.")
    parser.add_argument("--topic", required=True, help="The topic to explain")
    parser.add_argument("--level", choices=["beginner", "professional", "expert"],
                         help="Audience level (omit if using --compare)")
    parser.add_argument("--compare", action="store_true",
                         help="Run all three levels side by side (Pro path extension)")
    args = parser.parse_args()

    if not args.compare and not args.level:
        print("Provide --level or use --compare.")
        sys.exit(1)

    client = get_client()

    if args.compare:
        for level in ["beginner", "professional", "expert"]:
            explanation = explain(client, args.topic, level)
            print_with_flag(args.topic, level, explanation)
        print(
            "\n--- Self-critique prompt (Pro path) ---\n"
            "Look at the three outputs above. Where did the differentiation work "
            "well? Where do two levels still sound too similar? That gap is exactly "
            "what a more specific system prompt would need to address."
        )
    else:
        explanation = explain(client, args.topic, args.level)
        print_with_flag(args.topic, args.level, explanation)


if __name__ == "__main__":
    main()
