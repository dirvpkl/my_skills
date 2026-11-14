#!/usr/bin/env bash
# classify_failure.sh — quick sanity checks to help decide whether a failed
# verification step is an environment problem or an actual code problem.
# Per testing/SKILL.md's "Environment failures vs code failures" section.
#
# This does NOT prove a failure is code or environment on its own — it just
# surfaces common environment culprits fast so you don't have to check each
# by hand. Use its output as evidence in the report, not as a final verdict.
#
# Usage: ./classify_failure.sh [port-to-check]

set -uo pipefail
PORT_TO_CHECK="${1:-}"

echo "== Environment sanity checks =="

echo
echo "-- Docker daemon --"
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    echo "OK: Docker daemon is running."
  else
    echo "SUSPECT: Docker daemon does not appear to be running or reachable."
  fi
else
  echo "SKIP: docker command not found."
fi

echo
echo "-- Network reachability --"
if command -v curl >/dev/null 2>&1; then
  if curl -s --max-time 3 -o /dev/null -w "%{http_code}" https://pypi.org >/dev/null 2>&1; then
    echo "OK: outbound network reachable (tested pypi.org)."
  else
    echo "SUSPECT: outbound network check failed — could explain dependency/API errors."
  fi
else
  echo "SKIP: curl not found, can't check network reachability."
fi

echo
echo "-- Disk space --"
df -h . 2>/dev/null | tail -n 1 | awk '{
  gsub("%","",$5);
  if ($5+0 >= 95) print "SUSPECT: disk usage at " $5 "% — could cause write/build failures.";
  else print "OK: disk usage at " $5 "%.";
}'

if [[ -n "$PORT_TO_CHECK" ]]; then
  echo
  echo "-- Port $PORT_TO_CHECK availability --"
  if command -v lsof >/dev/null 2>&1; then
    if lsof -i ":$PORT_TO_CHECK" >/dev/null 2>&1; then
      echo "SUSPECT: port $PORT_TO_CHECK is already in use:"
      lsof -i ":$PORT_TO_CHECK"
    else
      echo "OK: port $PORT_TO_CHECK appears free."
    fi
  else
    echo "SKIP: lsof not found, can't check port usage."
  fi
fi

echo
echo "== Done. Any SUSPECT line above is a candidate environment cause — =="
echo "== investigate those before concluding the code itself is broken.  =="
