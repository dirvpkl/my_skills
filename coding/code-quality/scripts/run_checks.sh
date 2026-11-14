#!/usr/bin/env bash
# run_checks.sh — code-quality's fixed check order for Python projects.
# Format -> lint -> typecheck -> test, per code-quality/SKILL.md.
# Usage: ./run_checks.sh [path-to-project]  (defaults to current directory)
#
# This script only *reports*. It never auto-fixes — that decision (silent fix
# on touched files vs. ask-first for bulk formatting) belongs to the agent,
# not this script.

set -uo pipefail

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR" || { echo "ERROR: cannot cd into $PROJECT_DIR"; exit 1; }

FAILED=0

section () {
  echo
  echo "== $1 =="
}

run_check () {
  local label="$1"
  shift
  if ! command -v "${1%% *}" >/dev/null 2>&1 && [[ "$1" != uvx* ]] && [[ "$1" != uv* ]]; then
    echo "SKIP: $label — command not found in environment"
    return
  fi
  echo "-- $label --"
  if "$@"; then
    echo "PASS: $label"
  else
    echo "FAIL: $label"
    FAILED=1
  fi
}

section "1. Format checks"
run_check "black --check"        uvx black --check .
run_check "ruff format --check"  uvx ruff format --check .

section "2. Lint checks"
run_check "ruff check"           uvx ruff check .
run_check "isort --check-only"   uvx isort --check-only .
run_check "pyflakes"             uvx pyflakes .

section "3. Type-check"
run_check "mypy"                 uv run mypy .

section "4. Tests"
run_check "pytest"               uv run pytest

echo
if [[ "$FAILED" -eq 0 ]]; then
  echo "All checks passed."
else
  echo "One or more checks FAILED — see above. Do not report this as done until fixed."
fi
exit "$FAILED"
