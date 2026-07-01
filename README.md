# GenAI for Everyone

Free, job-ready GenAI program for everyone — beginners to working professionals. 7 weeks, 40 live sessions covering LLMs, prompting, RAG, agents, evaluation & safety, and deployment. Includes lesson docs, slide decks, hands-on code, quizzes, exams & interview prep.

[![CI Checks](https://github.com/TechNaom/genai-for-everyone/actions/workflows/ci.yml/badge.svg)](https://github.com/TechNaom/genai-for-everyone/actions/workflows/ci.yml)

---

## What this is

A volunteer-run, cohort-based program that takes learners — complete beginners and working professionals alike, in the same room — from GenAI fundamentals to job-ready skills:

- Prompt engineering & application design
- Embeddings & Retrieval-Augmented Generation (RAG)
- AI agents & tool use
- Evaluation, safety & responsible AI
- Deployment, cost, and scaling

Every session ships with a **lesson doc**, **slide deck**, **hands-on Python exercise**, and a **quiz**. Every week adds a **written exam** and an **interview-question set**. The program closes with a real-world **capstone project**.

## Program structure

| Week | Theme |
|---|---|
| 1 | Foundations of GenAI & LLMs |
| 2 | Prompt Engineering & Application Design |
| 3 | Working with Data: Embeddings & RAG |
| 4 | Tool Use, Agents & Automation |
| 5 | Evaluation, Safety & Responsible AI |
| 6 | Deployment, Cost, Scaling & MLOps-for-GenAI |
| 7 | Capstone, Real-World Case Studies & Career Prep |

Full session-by-session breakdown: [`docs/curriculum/CURRICULUM_MAP.md`](docs/curriculum/CURRICULUM_MAP.md)

## Repo structure

```
genai-for-everyone/
├── docs/
│   ├── curriculum/        → master curriculum map, learning outcomes
│   └── program/            → how to run a cohort, program overview
├── weeks/
│   └── week-01-foundations/
│       └── session-1.1-what-genai-actually-is.md
├── codebase/
│   ├── exercises/          → starter code learners work from
│   ├── solutions/          → reference solutions
│   └── datasets/           → sample data used in exercises
├── assets/
│   └── slides/              → PPTX decks, one per session
├── assessments/
│   ├── quizzes/             → per-session quizzes
│   ├── written-exams/       → per-week exams
│   ├── interview-questions/ → per-week interview prep
│   └── answer-keys/         → answer keys for the above
└── .github/
    └── workflows/           → CI checks (see below)
```

## Getting started (as a learner)

1. Start at [`docs/curriculum/CURRICULUM_MAP.md`](docs/curriculum/CURRICULUM_MAP.md) for the full roadmap.
2. Go week by week — read the lesson doc, review the slides, do the exercise, take the quiz.
3. Most exercises run on free/open tools. Where a paid API is used, a free alternative is always documented alongside it.

## Getting started (running exercises locally)

```bash
git clone https://github.com/TechNaom/genai-for-everyone.git
cd genai-for-everyone
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in any API keys you choose to use (only needed for sessions that call a paid API — noted in that session's doc).

## Maintenance

This repo is solo-maintained and isn't open to external contributions — issues and PRs from outside contributors aren't reviewed. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the maintainer's own workflow notes, including the file-naming convention and the scaffold script used to add new sessions.

## CI

Every push/PR runs automated checks (`.github/workflows/ci.yml`):
- Folder structure & naming convention validation
- Placeholder/leftover-text detection
- Python syntax + lint checks on exercises
- Secret/API-key leak scanning
- PPTX file integrity checks

## License

Content is free to use for running your own cohort. (Add your preferred license here — e.g. MIT for code, CC-BY for course content.)
