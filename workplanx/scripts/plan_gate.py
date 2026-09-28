#!/usr/bin/env python3
"""plan_gate.py — structural gate for workplanx topic folders.

Checks shape, not adjectives: sections/URLs/ladder-picks must exist.
A log full of "thoroughly searched" with zero URLs still fails.

Deliberately no banned-word list: word-matching is gameable and teaches
avoidance. Semantic judgment belongs to the fresh-eyes reviewer at the end
(see workplanx SKILL.md step 5), not to a regex here.

Usage:
    python3 plan_gate.py --dir <topic-dir> --phase plan|search|decision|build [--strict]

`code` is accepted as a legacy alias for `build` so topic folders written
before 1.3.0 keep validating.
"""
import argparse
import re
import sys
from pathlib import Path

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"

_URL_RE = re.compile(r"https://\S+/\S*")
# Ladder vocabulary is domain-neutral (see solution-search 1.8.0). Legacy
# spellings are still accepted so pre-1.8.0 topic folders keep passing.
_LADDER_RE = re.compile(
    r"hosted|open-project|oss|library|component|template|own-make|own code|own-code",
    re.I,
)
_PHASE_ALIASES = {"code": "build"}


def _read(d: Path, name: str) -> str:
    p = d / name
    return p.read_text(encoding="utf-8", errors="ignore") if p.exists() else ""


def gate(d: Path, phase: str):
    phase = _PHASE_ALIASES.get(phase, phase)
    results = []
    plan, search, decision = _read(d, "plan.md"), _read(d, "search.md"), _read(d, "decision.md")
    urls = _URL_RE.findall(search)

    if not plan.strip():
        results.append((FAIL, "plan", "plan.md missing or empty"))
    elif not re.search(r"^#{1,3}\s+\S+", plan, re.M):
        results.append((WARN, "plan", "plan.md has no section headers (verb sections expected)"))
    else:
        results.append((PASS, "plan", "plan.md present with sections"))

    if phase in ("search", "decision", "build"):
        queries = re.findall(r"quer(?:y|ies)\s*:", search, re.I)
        if not search.strip():
            results.append((FAIL, "search", "search.md missing or empty — nothing starts before evidence"))
        elif not urls:
            if queries:
                results.append((WARN, "search", "zero candidates but query log present — zero-candidate path: decide <own-make> with the log as reason"))
            else:
                results.append((FAIL, "search", "search.md has zero URLs — queries + candidate URLs required"))
        elif not _LADDER_RE.search(search):
            results.append((FAIL, "search", "search.md names no ladder level per verb"))
        else:
            results.append((PASS, "search", f"{len(urls)} URL(s), ladder levels present"))

    if phase in ("decision", "build"):
        m = re.search(r"user-pick\s*:(.*)", decision, re.I)
        pick = (m.group(1).strip() if m else "")
        if not pick or re.match(r"^(todo|tbd|none|n/a|—|-)?$", pick, re.I):
            results.append((FAIL, "decision", "decision.md has no user pick — stop, write the user"))
        else:
            results.append((PASS, "decision", f"user pick: {pick[:60]}"))

    if phase == "build" and not (d / "gate.log").exists():
        results.append((WARN, "gate.log", "no gate.log history yet — append this run"))

    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=False, default=".", help="topic folder")
    ap.add_argument(
        "--phase",
        default="search",
        choices=["plan", "search", "decision", "build", "code"],
        help="'code' is a legacy alias for 'build'",
    )
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    d = Path(args.dir)
    phase = _PHASE_ALIASES.get(args.phase, args.phase)
    results = gate(d, phase)
    fails = warns = 0
    for status, name, msg in results:
        print(f"[{status}] {name}: {msg}")
        fails += status == FAIL
        warns += status == WARN
    print(f"--- {len(results)-fails-warns} pass, {warns} warn, {fails} fail ---")
    log = d / "gate.log"
    try:
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"## phase={phase} pass={len(results)-fails-warns} warn={warns} fail={fails}\n")
            for status, name, msg in results:
                f.write(f"- [{status}] {name}: {msg}\n")
    except OSError:
        pass
    return 1 if (fails or (args.strict and warns)) else 0


if __name__ == "__main__":
    sys.exit(main())
