#!/usr/bin/env bash
# Run the same checks locally that CI runs on push/PR.
# Usage: bash scripts/local_check.sh

set -e
cd "$(dirname "$0")/.."

echo "== 1. Checking required folders =="
for dir in docs weeks codebase assets/slides assessments; do
  if [ ! -d "$dir" ]; then
    echo "MISSING: $dir"
    exit 1
  fi
done
echo "OK"

echo ""
echo "== 2. Scanning for placeholder text =="
if grep -rniE "lorem ipsum|\[insert[^]]*\]|\bTODO\b|\bFIXME\b|xxx{2,}" \
    --include="*.md" weeks/ docs/ assessments/ 2>/dev/null; then
  echo "Found placeholder text above — fix before pushing."
  exit 1
fi
echo "OK"

echo ""
echo "== 3. Python syntax check =="
shopt -s globstar nullglob
FILES=(codebase/**/*.py)
if [ ${#FILES[@]} -eq 0 ]; then
  echo "No Python files yet — skipping."
else
  python -m py_compile "${FILES[@]}"
  echo "OK"
fi

echo ""
echo "== 4. Scanning for likely secrets =="
PATTERN='sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|api[_-]?key\s*=\s*["\047][A-Za-z0-9]{16,}'
if grep -rniE "$PATTERN" \
    --include="*.py" --include="*.md" --include="*.json" --include="*.yml" --include="*.yaml" \
    --exclude-dir=".git" . 2>/dev/null; then
  echo "Possible secret detected above — remove before pushing."
  exit 1
fi
echo "OK"

echo ""
echo "All local checks passed. Safe to push."
