#!/usr/bin/env bash
# baseline_diff.sh — compare a check command's result against the pre-change
# baseline via git stash, per testing/SKILL.md's regression-check process.
#
# Usage: ./baseline_diff.sh "<check command to run>"
# Example: ./baseline_diff.sh "uv run pytest"
#
# This only makes sense inside a git repo with uncommitted changes to compare
# against. It stashes your current changes, runs the check on the clean tree,
# pops the stash, runs the check again, and prints both outputs so you (or
# the agent) can compare them side by side instead of guessing.

set -uo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"<check command>\""
  exit 1
fi

CHECK_CMD="$1"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git repository."
  exit 1
fi

if git diff --quiet && git diff --cached --quiet; then
  echo "ERROR: no uncommitted changes to compare — nothing to stash."
  exit 1
fi

echo "== Stashing current changes =="
git stash push -m "baseline_diff.sh temp stash" || { echo "ERROR: stash failed"; exit 1; }

echo
echo "== Running check on BASELINE (pre-change) tree =="
eval "$CHECK_CMD" > /tmp/baseline_diff_before.log 2>&1
BEFORE_STATUS=$?
cat /tmp/baseline_diff_before.log

echo
echo "== Restoring changes =="
git stash pop || { echo "ERROR: stash pop failed — resolve manually, changes are still in the stash list."; exit 1; }

echo
echo "== Running check on CHANGED (post-change) tree =="
eval "$CHECK_CMD" > /tmp/baseline_diff_after.log 2>&1
AFTER_STATUS=$?
cat /tmp/baseline_diff_after.log

echo
echo "== Comparison =="
echo "Baseline exit code: $BEFORE_STATUS"
echo "Changed  exit code: $AFTER_STATUS"
if [[ "$BEFORE_STATUS" -ne 0 && "$AFTER_STATUS" -ne 0 ]]; then
  echo "Both baseline and changed tree fail — this failure likely pre-dates your change. Confirm by diffing the two logs:"
  echo "  diff /tmp/baseline_diff_before.log /tmp/baseline_diff_after.log"
elif [[ "$BEFORE_STATUS" -eq 0 && "$AFTER_STATUS" -ne 0 ]]; then
  echo "Baseline passed, changed tree failed — this is very likely a real regression caused by your change."
elif [[ "$BEFORE_STATUS" -ne 0 && "$AFTER_STATUS" -eq 0 ]]; then
  echo "Baseline failed, changed tree passed — your change may have fixed a pre-existing issue. Confirm this was intentional."
else
  echo "Both passed — no regression detected by this check."
fi
