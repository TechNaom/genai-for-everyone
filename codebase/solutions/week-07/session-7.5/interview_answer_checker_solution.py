"""
Reference solution — Session 7.5: "Walk Me Through Your Project" Self-Checker

Run: python3 interview_answer_checker_solution.py example_answer.txt
"""

import sys

REQUIRED_ELEMENTS = {
    "problem_and_user": ["user", "problem", "who"],
    "approach_and_why": ["because", "chose", "instead of", "why"],
    "hard_tradeoff": ["trade-off", "tradeoff", "decided", "harder", "difficult"],
    "success_criteria": ["success", "measure", "eval", "%", "accuracy", "golden"],
}


def load_answer(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def check_answer(text: str) -> dict:
    lowered = text.lower()
    return {
        element: any(keyword in lowered for keyword in keywords)
        for element, keywords in REQUIRED_ELEMENTS.items()
    }


def print_report(path: str):
    text = load_answer(path)
    results = check_answer(text)
    print(f"Checking {path}...\n")
    for element, present in results.items():
        status = "✅" if present else "⚠️  missing"
        print(f"{status} — {element.replace('_', ' ')}")
    score = sum(results.values())
    print(f"\n{score}/{len(REQUIRED_ELEMENTS)} elements present")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 interview_answer_checker_solution.py example_answer.txt")
        sys.exit(1)
    print_report(sys.argv[1])
