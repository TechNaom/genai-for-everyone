#!/usr/bin/env python3
"""
Scaffold all files for a new session in the GenAI for Everyone curriculum.

Usage:
    python scripts/new_session.py --week 1 --session 1.2 --title "How LLMs Work, Without the Math Fear"

Creates (if they don't already exist):
    weeks/week-01-foundations/session-1.2-how-llms-work-without-the-math-fear.md
    codebase/exercises/week-01/session-1.2/  (with a starter README)
    assessments/quizzes/week-01/session-1.2-quiz.md
    assets/slides/week-01/  (note file pointing to where the .pptx should go)

Existing files are never overwritten — the script tells you if a file
already exists instead of clobbering it.
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

WEEK_THEMES = {
    1: "foundations",
    2: "prompt-engineering",
    3: "embeddings-rag",
    4: "agents-automation",
    5: "evaluation-safety",
    6: "deployment-scaling",
    7: "capstone-career-prep",
}


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def write_if_absent(path: Path, content: str) -> None:
    if path.exists():
        print(f"  SKIP (already exists): {path.relative_to(REPO_ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  CREATED: {path.relative_to(REPO_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new curriculum session.")
    parser.add_argument("--week", type=int, required=True, help="Week number, e.g. 1")
    parser.add_argument("--session", type=str, required=True, help="Session number, e.g. 1.2")
    parser.add_argument("--title", type=str, required=True, help="Session title")
    args = parser.parse_args()

    week_num = args.week
    session_num = args.session
    title = args.title

    if week_num not in WEEK_THEMES:
        print(f"Warning: week {week_num} has no known theme slug; using 'misc'.")
    week_slug = WEEK_THEMES.get(week_num, "misc")
    week_dir_name = f"week-{week_num:02d}-{week_slug}"
    title_slug = slugify(title)

    print(f"Scaffolding Week {week_num}, Session {session_num}: {title}\n")

    # 1. Lesson doc
    lesson_path = (
        REPO_ROOT / "weeks" / week_dir_name / f"session-{session_num}-{title_slug}.md"
    )
    lesson_template = f"""# Session {session_num}: {title}

**Week:** {week_num} ({week_slug.replace('-', ' ').title()})
**Format:** Live session + self-paced exercise + quiz

## Learning objective

_What should a learner be able to DO after this session that they couldn't before?_

## Concept (shared by everyone)

_Core explanation, plain language first, examples before formalism._

## Core path — guided activity

_Scaffolded hands-on activity for learners newer to the material._

## Pro path — extended challenge

_Same topic, less scaffolding, closer to a real-world scenario._

## Real-world scenario

_A concrete situation a working professional would hit on the job._

## Key takeaways

- 
- 
- 

## Quiz

See [`assessments/quizzes/week-{week_num:02d}/session-{session_num}-quiz.md`](../../assessments/quizzes/week-{week_num:02d}/session-{session_num}-quiz.md)

## Slide deck

See `assets/slides/week-{week_num:02d}/session-{session_num}.pptx`
"""
    write_if_absent(lesson_path, lesson_template)

    # 2. Exercise folder + starter README
    exercise_dir = REPO_ROOT / "codebase" / "exercises" / f"week-{week_num:02d}" / f"session-{session_num}"
    exercise_readme = exercise_dir / "README.md"
    exercise_template = f"""# Exercise — Session {session_num}: {title}

## Setup

```bash
pip install -r requirements.txt  # if this exercise has its own deps
```

## Free/open path

_Instructions using free/open tools — always works, no cost._

## Optional paid-API path

_If applicable: how to swap in a paid API for stronger results, and why you might want to._

## Starter code

See `starter.py` in this folder.

## Solution

See `codebase/solutions/week-{week_num:02d}/session-{session_num}/` (don't peek before attempting!).
"""
    write_if_absent(exercise_readme, exercise_template)
    write_if_absent(exercise_dir / "starter.py", f'"""\nStarter code for Session {session_num}: {title}\n"""\n\n# TODO: learner fills this in\n')

    # 3. Quiz
    quiz_path = REPO_ROOT / "assessments" / "quizzes" / f"week-{week_num:02d}" / f"session-{session_num}-quiz.md"
    quiz_template = f"""# Quiz — Session {session_num}: {title}

_5-8 questions, mixed format. Answer key in `assessments/answer-keys/`._

1. 
2. 
3. 
4. 
5. 
"""
    write_if_absent(quiz_path, quiz_template)

    # 4. Slide deck placeholder note (actual .pptx built separately)
    slides_note = REPO_ROOT / "assets" / "slides" / f"week-{week_num:02d}" / f"session-{session_num}-NOTE.md"
    slides_note_template = f"Slide deck for this session should be saved as:\n\nsession-{session_num}.pptx\n\n(in this same folder)\n"
    write_if_absent(slides_note, slides_note_template)

    print("\nDone. Fill in the generated files, then run scripts/local_check.sh before pushing.")


if __name__ == "__main__":
    main()
