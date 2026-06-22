# Contributing / Adding Content

This doubles as the standard workflow for adding a new session, week, or fixing existing content — useful even working solo, so nothing drifts from the naming convention as the repo grows to 40 sessions.

## Workflow for adding a new session

1. **Create a branch**
   ```bash
   git checkout -b add/week-0X-session-X.Y
   ```

2. **Scaffold the files** using the helper script (creates all files in the right place with the right names):
   ```bash
   python scripts/new_session.py --week 1 --session 1.2 --title "How LLMs Work, Without the Math Fear"
   ```
   This creates:
   - `weeks/week-01-foundations/session-1.2-how-llms-work-without-the-math-fear.md`
   - `codebase/exercises/week-01/session-1.2/`
   - `assessments/quizzes/week-01/session-1.2-quiz.md`
   - A placeholder note for the slide deck in `assets/slides/week-01/`

3. **Fill in content** following the templates already in `docs/program/TEMPLATES.md`.

4. **Run checks locally before pushing** (same checks CI runs):
   ```bash
   bash scripts/local_check.sh
   ```

5. **Commit with a clear message**
   ```bash
   git add .
   git commit -m "Add Week 1 Session 1.2: How LLMs Work"
   ```

6. **Push and open a PR**
   ```bash
   git push -u origin add/week-0X-session-X.Y
   ```
   Open a PR into `main` on GitHub. CI will run automatically. Merge once green.

## File naming convention (must match for CI to pass)

```
weeks/week-{NN}-{week-slug}/session-{N.N}-{session-slug}.md
assets/slides/week-{NN}/session-{N.N}.pptx
codebase/exercises/week-{NN}/session-{N.N}/
assessments/quizzes/week-{NN}/session-{N.N}-quiz.md
assessments/written-exams/week-{NN}-exam.md
assessments/interview-questions/week-{NN}-interview-qs.md
```

- Week numbers are zero-padded: `week-01`, `week-02`, ... `week-07`
- Session slugs are lowercase, hyphenated, no special characters
- Session numbers use the `week.session` format: `1.1`, `1.2`, ... `7.6`

## Content standards

- **No placeholder text** in anything merged to `main` — no `TODO`, `Lorem ipsum`, `[insert X]`. CI blocks these.
- **No API keys or secrets** committed anywhere, ever. Use `.env` (already gitignored) and reference `os.environ.get(...)` in code.
- **Every exercise needs a free/open path.** If a paid API is used, document the free alternative in the same file.
- **Every session doc needs:** learning objective, concept explanation, Core path activity, Pro path activity, and a link to its quiz.

## Updating existing content

Same branch → edit → local check → PR flow. Small fixes (typos, broken links) can skip the scaffold script and just edit directly.

## Questions / issues

Open a GitHub Issue using the templates in `.github/ISSUE_TEMPLATE/`.
