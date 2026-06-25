# Contributing / Adding Content

This doubles as the standard workflow for adding a new session, week, or fixing existing content — useful even working solo, so nothing drifts from the naming convention as the repo grows to 40 sessions.

## The fast path: shipping a session Claude built for you

When Claude hands you a downloaded `.tar.gz` bundle for a session (chapter + exercise + quiz + deck), you don't need to manually extract, check, commit, and push as separate steps. One script does all of it:

```bash
bash scripts/ship_session.sh ~/Downloads/session-1.3-review.tar.gz "Add Session 1.3: The GenAI Landscape"
```

This will, in order:
1. Extract the bundle into the right folders
2. Run the same checks CI runs (so you catch problems before pushing, not after)
3. Show you exactly what changed (`git status` + diff stats)
4. Ask you to confirm before committing — nothing happens silently
5. Commit and push

If checks fail, it stops immediately — nothing gets committed or pushed broken. Fix the issue and re-run; it's safe to re-run any time.

**On WSL**, your Windows Downloads folder is usually at `/mnt/c/Users/<your-username>/Downloads/` — adjust the path above accordingly.

## Checking overall progress

To see, at a glance, which of the 42 sessions are fully built versus still placeholder:

```bash
python3 scripts/status.py
```

This checks each session's chapter, exercise, quiz, and slide deck, and prints a simple done/pending table plus an overall percentage. It's a quick visual tracker, not a content-quality judge — a session can show "done" and still be worth a closer read.

## Workflow for adding a new session manually

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
