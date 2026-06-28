#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# ship_session.sh — one-command pipeline for landing new session content.
#
# Usage:
#   bash scripts/ship_session.sh path/to/downloaded-bundle.tar.gz "commit message"
#
# What it does, in order:
#   1. Extracts the tarball into the repo (stripping the outer wrapper folder)
#   2. Runs the same checks CI runs (scripts/local_check.sh)
#   3. Shows you a summary of what changed (git status, short diff stats)
#   4. Asks for confirmation before committing
#   5. Commits with your message and pushes to the current branch
#
# If checks fail, it stops BEFORE committing — nothing gets pushed broken.
# ---------------------------------------------------------------------------

set -e
cd "$(dirname "$0")/.."

BUNDLE="$1"
MESSAGE="$2"

if [ -z "$BUNDLE" ] || [ -z "$MESSAGE" ]; then
  echo "Usage: bash scripts/ship_session.sh path/to/bundle.tar.gz \"commit message\""
  echo ""
  echo "Example:"
  echo "  bash scripts/ship_session.sh ~/Downloads/session-1.3-review.tar.gz \"Add Session 1.3: The GenAI Landscape\""
  exit 1
fi

if [ ! -f "$BUNDLE" ]; then
  echo "File not found: $BUNDLE"
  echo "Check the path — on WSL, Windows Downloads is usually at /mnt/c/Users/<you>/Downloads/"
  exit 1
fi

echo "== Step 1: Extracting $BUNDLE =="
tar -xzf "$BUNDLE" --strip-components=1 -C .
echo "Extraction complete."
echo ""

echo "== Step 2: Running local checks =="
if ! bash scripts/local_check.sh; then
  echo ""
  echo "Checks FAILED. Nothing has been committed or pushed."
  echo "Fix the issue above, then re-run this script (it's safe to re-run)."
  exit 1
fi
echo ""

echo "== Step 3: What changed =="
git add -A
git status --short
echo ""
git diff --cached --stat
echo ""

read -p "Commit and push these changes? [y/N] " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted. Changes are staged but not committed — run 'git reset' to unstage if needed."
  exit 0
fi

echo ""
echo "== Step 4: Committing =="
git commit -m "$MESSAGE"

echo ""
echo "== Step 5: Pushing =="
git push

echo ""
echo "Done. Check https://github.com/TechNaom/genai-for-everyone/actions for CI status."
