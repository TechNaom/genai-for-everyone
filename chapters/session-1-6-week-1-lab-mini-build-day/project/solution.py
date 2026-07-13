"""
Week 1 Capstone Project — "Explain It To Me Simply" (reference solution)

A complete, polished version of the week's deliverable, including the Pro-path
comparison mode (--compare runs all three audience levels side by side and
prompts you to critique your own prompt design).

What each part touches:
  - generative output (1.1): every explanation is freshly composed
  - context shaping (1.2): the system prompt shapes what the model considers
  - model choice (1.3): a fast, low-cost tier for a well-scoped task
  - request/response (1.4): system/user roles, one create() call, parse response
  - honesty flag (1.5): a heuristic that pairs output with a "verify this" signal

Setup (only needed for a LIVE explanation):
  pip install anthropic python-dotenv
  Copy .env.example (repo root) to .env and add your ANTHROPIC_API_KEY

Run:
  python solution.py --topic "black holes" --level beginner
  python solution.py --topic "black holes" --compare
  python solution.py                      # offline demo, no API key needed
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
    if Anthropic is None:
        print("The 'anthropic' package isn't installed. Run: pip install anthropic")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def needs_verification_flag(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in VERIFICATION_FLAG_KEYWORDS)


def explain(client, topic: str, level: str) -> str:
    system_prompt = SYSTEM_PROMPTS[level]
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=400,
            system=system_prompt,
            messages=[{"role": "user", "content": f"Explain: {topic}"}],
        )
    except Exception as err:  # network issue, invalid key, rate limit, etc.
        return f"[The API call failed: {err}. Check your key and connection, then try again.]"
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


def offline_demo():
    """Runs with no API key. Shows the prompts and the honesty flag heuristic."""
    print("=== Offline demo (no API key needed) ===\n")
    print("The quality of this tool lives in these three system prompts:\n")
    for level, prompt in SYSTEM_PROMPTS.items():
        print(f"[{level}]\n{prompt}\n")

    print("The honesty flag is a plain Python heuristic — here it is running now:")
    for s in ["A 2020 study found 63 percent of cells react.",
              "Gravity pulls things toward the ground."]:
        print(f"  needs_verification_flag({s!r}) -> {needs_verification_flag(s)}")

    print(
        "\nFor a live explanation, add an API key and run e.g.:\n"
        "  python solution.py --topic \"black holes\" --level beginner\n"
        "  python solution.py --topic \"black holes\" --compare"
    )


def main():
    parser = argparse.ArgumentParser(description="Explain a topic, calibrated to an audience level.")
    parser.add_argument("--topic", help="The topic to explain")
    parser.add_argument("--level", choices=["beginner", "professional", "expert"],
                        help="Audience level (omit if using --compare)")
    parser.add_argument("--compare", action="store_true",
                        help="Run all three levels side by side (Pro path extension)")
    args = parser.parse_args()

    if not args.topic:
        offline_demo()
        return

    if not args.compare and not args.level:
        print("Provide --level or use --compare.")
        sys.exit(1)

    client = get_client()

    if args.compare:
        for level in ["beginner", "professional", "expert"]:
            print_with_flag(args.topic, level, explain(client, args.topic, level))
        print(
            "\n--- Self-critique prompt (Pro path) ---\n"
            "Look at the three outputs above. Where did the differentiation work "
            "well? Where do two levels still sound too similar? That gap is exactly "
            "what a more specific system prompt would need to address."
        )
    else:
        print_with_flag(args.topic, args.level, explain(client, args.topic, args.level))


if __name__ == "__main__":
    main()
