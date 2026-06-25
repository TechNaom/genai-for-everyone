#!/usr/bin/env python3
"""
status.py — shows build progress across all 42 sessions at a glance.

Usage: python3 scripts/status.py

For each session, checks whether each deliverable is REAL content or still
a placeholder (using simple, honest heuristics — word count and known
placeholder markers). This is a quick visual progress tracker, not a
content-quality judge.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

WEEK_THEMES = {
    1: "foundations", 2: "prompt-engineering", 3: "embeddings-rag",
    4: "agents-automation", 5: "evaluation-safety", 6: "deployment-scaling",
    7: "capstone-career-prep",
}

SESSIONS_PER_WEEK = 6
CHAPTER_WORD_THRESHOLD = 800   # below this, treat as placeholder/stub
QUIZ_PLACEHOLDER_MARKERS = ["1. \n2. \n3. ", "1. \n2. \n3. \n4. \n5. "]


def word_count(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return len(text.split())


def looks_like_placeholder_quiz(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="ignore")
    # crude check: are the numbered lines all empty?
    lines = [l.strip() for l in text.splitlines() if re.match(r"^\d+\.\s*$", l.strip())]
    return len(lines) >= 3


def check_mark(done: bool) -> str:
    return "\u2705" if done else "\u23f3"


def main():
    print(f"{'Session':<8} {'Chapter':<10} {'Exercise':<10} {'Quiz':<8} {'Deck':<8}")
    print("-" * 50)

    total_done = 0
    total_sessions = 0

    for week in range(1, 8):
        week_slug = WEEK_THEMES[week]
        week_dir = REPO_ROOT / "weeks" / f"week-{week:02d}-{week_slug}"

        for session_in_week in range(1, SESSIONS_PER_WEEK + 1):
            session_num = f"{week}.{session_in_week}"
            total_sessions += 1

            # Find the chapter file (slug varies, so glob for it)
            chapter_matches = list(week_dir.glob(f"session-{session_num}-*.md")) if week_dir.exists() else []
            chapter_path = chapter_matches[0] if chapter_matches else None
            chapter_wc = word_count(chapter_path) if chapter_path else 0
            chapter_done = chapter_wc >= CHAPTER_WORD_THRESHOLD

            # Exercise folder: real if it has more than just README+starter.py stub
            exercise_dir = REPO_ROOT / "codebase" / "exercises" / f"week-{week:02d}" / f"session-{session_num}"
            exercise_files = list(exercise_dir.glob("*.py")) if exercise_dir.exists() else []
            non_starter_files = [f for f in exercise_files if f.name != "starter.py"]
            exercise_done = len(non_starter_files) > 0

            # Quiz
            quiz_path = REPO_ROOT / "assessments" / "quizzes" / f"week-{week:02d}" / f"session-{session_num}-quiz.md"
            quiz_done = quiz_path.exists() and not looks_like_placeholder_quiz(quiz_path)

            # Deck
            deck_path = REPO_ROOT / "assets" / "slides" / f"week-{week:02d}" / f"session-{session_num}.pptx"
            deck_done = deck_path.exists()

            row_done = chapter_done and exercise_done and quiz_done and deck_done
            if row_done:
                total_done += 1

            print(f"{session_num:<8} {check_mark(chapter_done):<10} {check_mark(exercise_done):<10} "
                  f"{check_mark(quiz_done):<8} {check_mark(deck_done):<8}")

        print()  # blank line between weeks

    print("-" * 50)
    print(f"Fully complete sessions: {total_done} / {total_sessions}")
    print(f"Progress: {round(100 * total_done / total_sessions)}%")


if __name__ == "__main__":
    main()
