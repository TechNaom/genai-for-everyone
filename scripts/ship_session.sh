#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# ship_session.sh — one-command pipeline for landing new session content.
#
# Usage:
#   bash scripts/ship_session.sh path/to/downloaded-bundle.tar.gz "commit message"
#
# What it does, in order:
#   1. Inspects the bundle's internal weeks/week-0N-* path(s) and checks them
#      against folders that actually exist in THIS repo. If a bundle path's
#      slug doesn't match but exactly one week-0N-* folder does exist, it
#      rewrites the bundle's internal path to the real one before
#      extracting -- so a wrong slug self-corrects instead of creating a
#      duplicate folder. If it can't find a confident match, it stops and
#      tells you exactly what it found instead of guessing.
#   2. Extracts the (possibly path-corrected) tarball into the repo
#   3. Runs the same checks CI runs (scripts/local_check.sh)
#   4. Shows you a summary of what changed (git status, short diff stats)
#   5. Asks for confirmation before committing
#   6. Commits with your message
#   7. Syncs with the remote (fetch + rebase) BEFORE pushing, so a stale
#      local branch never causes a rejected push
#   8. Pushes
#
# If checks fail, it stops BEFORE committing — nothing gets pushed broken.
# If the remote has diverged in a way that can't auto-rebase cleanly, it
# stops and tells you exactly what to do — it will never force-push or
# silently discard anything, yours or the remote's.
# ---------------------------------------------------------------------------

set -e
cd "$(dirname "$0")/.."
REPO_ROOT="$(pwd)"

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

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

echo "== Step 1: Checking bundle paths against your real repo structure =="

# Unpack into a scratch dir first (not the repo) so we can inspect/fix paths
# before anything touches your actual files.
tar -xzf "$BUNDLE" -C "$WORKDIR"

# The bundle should have exactly one top-level wrapper folder.
WRAPPER=$(find "$WORKDIR" -maxdepth 1 -mindepth 1 -type d | head -1)
if [ -z "$WRAPPER" ]; then
  echo "Could not find a top-level folder inside the bundle. Aborting."
  exit 1
fi

PATH_FIXED=0
# Find every weeks/week-0N-* path inside the bundle (there should be at most
# one per session, but loop in case a bundle ever carries more than one).
while IFS= read -r BUNDLE_WEEK_DIR; do
  [ -z "$BUNDLE_WEEK_DIR" ] && continue
  BUNDLE_SLUG=$(basename "$BUNDLE_WEEK_DIR")
  WEEK_NUM=$(echo "$BUNDLE_SLUG" | grep -oE 'week-[0-9]+' | head -1)

  if [ -z "$WEEK_NUM" ]; then
    continue
  fi

  # Does this exact slug already exist in the real repo?
  if [ -d "$REPO_ROOT/weeks/$BUNDLE_SLUG" ]; then
    echo "  '$BUNDLE_SLUG' matches an existing repo folder exactly. Good."
    continue
  fi

  # It doesn't match exactly. Look for real repo folders with the same
  # week number but a different theme slug.
  mapfile -t REAL_MATCHES < <(find "$REPO_ROOT/weeks" -maxdepth 1 -type d -name "${WEEK_NUM}-*" -printf "%f\n" 2>/dev/null)

  if [ "${#REAL_MATCHES[@]}" -eq 1 ]; then
    REAL_SLUG="${REAL_MATCHES[0]}"
    echo "  Bundle has '$BUNDLE_SLUG' but your repo's real folder is '$REAL_SLUG'."
    echo "  Auto-correcting the bundle's internal path before extracting..."
    mv "$BUNDLE_WEEK_DIR" "$(dirname "$BUNDLE_WEEK_DIR")/$REAL_SLUG"
    PATH_FIXED=1
  elif [ "${#REAL_MATCHES[@]}" -eq 0 ]; then
    echo ""
    echo "=========================================================="
    echo "NO MATCHING WEEK FOLDER FOUND"
    echo "=========================================================="
    echo "The bundle expects a folder for '$WEEK_NUM' (bundle calls it"
    echo "'$BUNDLE_SLUG'), but your repo has no 'weeks/${WEEK_NUM}-*' folder"
    echo "at all. Nothing has been extracted or committed."
    echo ""
    echo "Real week folders in this repo right now:"
    find "$REPO_ROOT/weeks" -maxdepth 1 -mindepth 1 -type d -printf "  %f\n" 2>/dev/null
    echo ""
    echo "If this is genuinely a new week, create the folder first, then re-run."
    exit 1
  else
    echo ""
    echo "=========================================================="
    echo "AMBIGUOUS — MULTIPLE MATCHING WEEK FOLDERS FOUND"
    echo "=========================================================="
    echo "The bundle expects '$WEEK_NUM' but your repo has more than one"
    echo "folder for that week number, so I won't guess which is real:"
    printf '  %s\n' "${REAL_MATCHES[@]}"
    echo ""
    echo "This usually means a stale duplicate folder exists from an"
    echo "earlier mistake. Clean up so only one '${WEEK_NUM}-*' folder"
    echo "remains under weeks/, then re-run this script."
    exit 1
  fi
done < <(find "$WRAPPER/weeks" -maxdepth 1 -mindepth 1 -type d 2>/dev/null)

if [ "$PATH_FIXED" -eq 1 ]; then
  echo "Path correction applied. Re-packing bundle for extraction..."
fi
echo ""

echo "== Step 2: Extracting into repo =="
tar -czf "$WORKDIR/corrected.tar.gz" -C "$WORKDIR" "$(basename "$WRAPPER")"
tar -xzf "$WORKDIR/corrected.tar.gz" --strip-components=1 -C "$REPO_ROOT"
echo "Extraction complete."
echo ""

echo "== Step 3: Running local checks =="
if ! bash scripts/local_check.sh; then
  echo ""
  echo "Checks FAILED. Nothing has been committed or pushed."
  echo "Fix the issue above, then re-run this script (it's safe to re-run)."
  exit 1
fi
echo ""

echo "== Step 4: What changed =="
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
echo "== Step 5: Committing =="
git commit -m "$MESSAGE"

echo ""
echo "== Step 6: Syncing with remote before push =="
git fetch origin

LOCAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
BEHIND_COUNT=$(git rev-list --count HEAD..origin/"$LOCAL_BRANCH" 2>/dev/null || echo 0)

if [ "$BEHIND_COUNT" -gt 0 ]; then
  echo "Remote has $BEHIND_COUNT commit(s) you don't have locally. Rebasing your new commit on top..."
  if git pull --rebase origin "$LOCAL_BRANCH"; then
    echo "Rebase succeeded — your commit is now on top of the latest remote history."
  else
    echo ""
    echo "=========================================================="
    echo "AUTOMATIC REBASE FAILED — there's a real conflict."
    echo "=========================================================="
    echo "This means a file you changed in this session was ALSO changed"
    echo "on the remote since your last pull. Git can't guess which version"
    echo "you want, so nothing has been pushed."
    echo ""
    echo "To resolve it:"
    echo "  1. Run: git status"
    echo "     (shows which files are conflicted)"
    echo "  2. Open each conflicted file, look for <<<<<<< / ======= / >>>>>>>"
    echo "     markers, and edit it down to the version you want to keep."
    echo "  3. Run: git add <the files you fixed>"
    echo "  4. Run: git rebase --continue"
    echo "  5. Re-run this script's push step manually: git push origin $LOCAL_BRANCH"
    echo ""
    echo "Your commit and the bundle's content are safe — nothing was lost."
    exit 1
  fi
else
  echo "Local branch is already up to date with remote. No rebase needed."
fi
echo ""

echo "== Step 7: Pushing =="
git push origin "$LOCAL_BRANCH"

echo ""
echo "Done. Check https://github.com/TechNaom/genai-for-everyone/actions for CI status."
