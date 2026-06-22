#!/usr/bin/env python3
"""
Scaffold every session across all 7 weeks in one pass, using the exact
session list from the curriculum map. Safe to re-run — new_session.py
never overwrites existing files.

Usage: python scripts/scaffold_all_weeks.py
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# (week, session, title) — matches docs/curriculum/CURRICULUM_MAP.md exactly
SESSIONS = [
    # Week 1 — Foundations of GenAI & LLMs
    (1, "1.1", "What GenAI Actually Is (and Isn't)"),
    (1, "1.2", "How LLMs Work, Without the Math Fear"),
    (1, "1.3", "The GenAI Landscape"),
    (1, "1.4", "Your First GenAI Application"),
    (1, "1.5", "Limitations, Hallucination & Bias"),
    (1, "1.6", "Week 1 Lab — Mini Build Day"),

    # Week 2 — Prompt Engineering & Application Design
    (2, "2.1", "Anatomy of a Great Prompt"),
    (2, "2.2", "Prompting Techniques I"),
    (2, "2.3", "Prompting Techniques II"),
    (2, "2.4", "Structured Outputs"),
    (2, "2.5", "Prompt Systems, Not Just Prompts"),
    (2, "2.6", "Week 2 Lab — Mini Build Day"),

    # Week 3 — Working with Data: Embeddings & RAG
    (3, "3.1", "Why LLMs Need External Knowledge"),
    (3, "3.2", "Embeddings Demystified"),
    (3, "3.3", "Vector Databases & Retrieval"),
    (3, "3.4", "Building a RAG Pipeline"),
    (3, "3.5", "RAG Failure Modes & Fixes"),
    (3, "3.6", "Week 3 Lab — Mini Build Day"),

    # Week 4 — Tool Use, Agents & Automation
    (4, "4.1", "What \"AI Agents\" Actually Means"),
    (4, "4.2", "Function/Tool Calling"),
    (4, "4.3", "Multi-Step Task Agents"),
    (4, "4.4", "Multi-Agent Patterns"),
    (4, "4.5", "Automation Workflows (No/Low-code + Code)"),
    (4, "4.6", "Week 4 Lab — Mini Build Day"),

    # Week 5 — Evaluation, Safety & Responsible AI
    (5, "5.1", "Why \"It Looks Good\" Isn't Evaluation"),
    (5, "5.2", "Evaluation Methods"),
    (5, "5.3", "Safety Fundamentals"),
    (5, "5.4", "Responsible AI & Bias in Practice"),
    (5, "5.5", "Guardrails & Mitigations"),
    (5, "5.6", "Week 5 Lab — Mini Build Day"),

    # Week 6 — Deployment, Cost, Scaling & MLOps-for-GenAI
    (6, "6.1", "From Notebook to Application"),
    (6, "6.2", "Cost & Latency Engineering"),
    (6, "6.3", "Choosing & Switching Models"),
    (6, "6.4", "Monitoring & Observability"),
    (6, "6.5", "CI/CD & Versioning for Prompts"),
    (6, "6.6", "Week 6 Lab — Mini Build Day"),

    # Week 7 — Capstone, Real-World Case Studies & Career Prep
    (7, "7.1", "Capstone Kickoff"),
    (7, "7.2", "Real-World Case Study Day I"),
    (7, "7.3", "Capstone Build Day I"),
    (7, "7.4", "Real-World Case Study Day II + Capstone Build Day II"),
    (7, "7.5", "Mock Technical Interviews"),
    (7, "7.6", "Capstone Demo Day & Program Wrap"),
]


def main():
    script_path = REPO_ROOT / "scripts" / "new_session.py"
    created = 0
    skipped = 0

    for week, session, title in SESSIONS:
        result = subprocess.run(
            [sys.executable, str(script_path), "--week", str(week), "--session", session, "--title", title],
            capture_output=True, text=True
        )
        print(f"--- Week {week}, Session {session}: {title} ---")
        print(result.stdout.strip())
        if result.returncode != 0:
            print(f"ERROR: {result.stderr.strip()}")
        created += result.stdout.count("CREATED")
        skipped += result.stdout.count("SKIP")

    # Also create the per-week exam and interview-question files,
    # which new_session.py doesn't handle (those are weekly, not per-session).
    print("\n--- Weekly written exams & interview-question sets ---")
    for week in range(1, 8):
        exam_path = REPO_ROOT / "assessments" / "written-exams" / f"week-{week:02d}-exam.md"
        interview_path = REPO_ROOT / "assessments" / "interview-questions" / f"week-{week:02d}-interview-qs.md"

        if not exam_path.exists():
            exam_path.parent.mkdir(parents=True, exist_ok=True)
            exam_path.write_text(
                f"# Week {week} Written Exam\n\n"
                f"_Deeper, scenario-based exam covering all of Week {week}'s sessions._\n\n"
                f"## Section A — Short Answer\n\n1. \n2. \n3. \n\n"
                f"## Section B — Scenario Analysis\n\n1. \n2. \n",
                encoding="utf-8"
            )
            print(f"  CREATED: {exam_path.relative_to(REPO_ROOT)}")
            created += 1
        else:
            print(f"  SKIP (already exists): {exam_path.relative_to(REPO_ROOT)}")
            skipped += 1

        if not interview_path.exists():
            interview_path.parent.mkdir(parents=True, exist_ok=True)
            interview_path.write_text(
                f"# Week {week} Interview Questions\n\n"
                f"_Interview-style questions tied to this week's topics._\n\n"
                f"1. \n2. \n3. \n4. \n5. \n",
                encoding="utf-8"
            )
            print(f"  CREATED: {interview_path.relative_to(REPO_ROOT)}")
            created += 1
        else:
            print(f"  SKIP (already exists): {interview_path.relative_to(REPO_ROOT)}")
            skipped += 1

    print(f"\nDone. {created} files created, {skipped} already existed and were left untouched.")


if __name__ == "__main__":
    main()
