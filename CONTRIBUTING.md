# Maintenance Guide (Solo-Maintained Project)

This repo is maintained solely by its owner  — it is **not open to external contributions**. Issues and pull requests from outside contributors are not reviewed or merged. If you found this repo useful, feel free to fork it for your own cohort per the license, but please don't open issues or PRs here.

This doc is my own working reference for how content gets added/updated, so nothing drifts from the naming convention as the repo grows.

## The fast path: shipping a session Claude built for me

When Claude hands me a downloaded `.tar.gz` bundle for a session (chapter + exercise + quiz + deck), I don't need to manually extract, check, commit, and push as separate steps. One script does all of it:

```bash
bash scripts/ship_session.sh ~/Downloads/session-1.3-review.tar.gz "Add Session 1.3: The GenAI Landscape"
```

This will, in order:
1. Extract the bundle into the right folders
2. Run the same checks CI runs (so problems get caught before pushing, not after)
3. Show exactly what changed (`git status` + diff stats)
4. Ask for confirmation before committing — nothing happens silently
5. Commit and push directly to `main`

If checks fail, it stops immediately — nothing gets committed or pushed broken. Fix the issue and re-run; it's safe to re-run any time.

**On WSL**, the Windows Downloads folder is usually at `/mnt/c/Users/<your-username>/Downloads/` — adjust the path above accordingly.

## Checking overall progress

To see, at a glance, which of the 42 sessions are fully built versus still placeholder:

```bash
python3 scripts/status.py
```

This checks each session's chapter, exercise, quiz, and slide deck, and prints a simple done/pending table plus an overall percentage. It's a quick visual tracker, not a content-quality judge — a session can show "done" and still be worth a closer read. Note: it checks exact non-`-v2` file paths, so any session rebuilt as `-v2` (e.g., 4.3, 4.4, 5.2, 5.3) will under-report here even though the content is real — check those manually.

## Workflow for adding or updating a session manually

1. **Scaffold the files** using the helper script (creates all files in the right place with the right names):
   ```bash
   python scripts/new_session.py --week 1 --session 1.2 --title "How LLMs Work, Without the Math Fear"
   ```
   This creates:
   - `weeks/week-01-foundations/session-1.2-how-llms-work-without-the-math-fear.md`
   - `codebase/exercises/week-01/session-1.2/`
   - `assessments/quizzes/week-01/session-1.2-quiz.md`
   - A placeholder note for the slide deck in `assets/slides/week-01/`

2. **Fill in content** following the pattern of already-completed sessions in the same week.

3. **Run checks locally before pushing** (same checks CI runs):
   ```bash
   bash scripts/local_check.sh
   ```

4. **Commit and push directly to `main`** with a clear message:
   ```bash
   git add .
   git commit -m "Add Week 1 Session 1.2: How LLMs Work"
   git push
   ```
   No branch/PR ceremony needed for a solo-maintained repo — `local_check.sh` (and CI, as a backstop) is the safety net.

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
- If a session gets rebuilt, keep the `-v2` suffix in the filename permanently rather than renaming back — this is the established convention (see sessions 4.3, 4.4, 5.2, 5.3) and keeps history/links traceable.

## Content standards

- **No placeholder text** in anything merged to `main` — no `TODO`, `Lorem ipsum`, `[insert X]`. CI blocks these.
- **No API keys or secrets** committed anywhere, ever. Use `.env` (already gitignored) and reference `os.environ.get(...)` in code.
- **Every exercise needs a free/open path.** If a paid API is used, document the free alternative in the same file.
- **Every session doc needs:** learning objective, concept explanation, Core path activity, Pro path activity, and a link to its quiz.
- **Before declaring a batch of sessions "done," read a sample of the actual content** — file existence at the right path is not evidence the content is real; scaffolded placeholder files look identical to real ones in a directory listing.
