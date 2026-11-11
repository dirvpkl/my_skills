#!/usr/bin/env python3
"""trigger_check.py — keep skill descriptions honest as trigger contracts.

The description line is the only trigger surface an agent sees before routing
(under-triggering is the common failure mode). This script verifies the
contract mechanically and measures routing accuracy through a fresh agent.

Modes:
  --lint            mechanical checks over every SKILL.md frontmatter
                    description: literal user phrase present, negative trigger
                    present, vague filler banned, length sane.
  --battery         print a copy-paste routing prompt (descriptions + fixture
                    utterances) for a fresh agent that sees ONLY descriptions —
                    no skill bodies, no bindings table.
  --answers FILE    diff the fresh agent's answers {"<fixture_id>": "<skill-or-
                    none>"} against the expected routing; exit 1 below
                    --threshold (default 0.9).

Usage from the repo root:
  python scripts/trigger_check.py --lint
  python scripts/trigger_check.py --battery
  python scripts/trigger_check.py --answers answers.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "trigger_fixtures.json"

VAGUE = ["when appropriate", "as needed", "use your judgment", "if needed",
         "when you see fit", "посчитаешь нужным"]
MAX_DESC = 1200


def skills():
    out = {}
    for d in sorted(ROOT.iterdir()):
        f = d / "SKILL.md"
        if not d.is_dir() or not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        name = re.search(r"^name: (\S+)", fm, re.M)
        desc = re.search(r"^description: (.*)$", fm, re.M)
        ver = re.search(r"^version: (\S+)", fm, re.M)
        if name and desc:
            out[name.group(1)] = {"description": desc.group(1).strip(),
                                  "version": ver.group(1) if ver else "?"}
    return out


def lint() -> int:
    issues = 0
    for name, s in skills().items():
        d = s["description"]
        low = d.lower()
        probs = []
        if len(d) > MAX_DESC:
            probs.append(f"description too long ({len(d)} > {MAX_DESC})")
        always_loaded = "always loaded" in low
        if not always_loaded and not re.search(r'"[^"]{3,}"', d):
            probs.append("no quoted literal user phrase")
        if not any(k in low for k in ("not for", "do not", "never", "not a ")):
            probs.append("no negative trigger (NOT for / Do not / never)")
        for v in VAGUE:
            if v in low:
                probs.append(f"vague filler: {v!r}")
        if not re.search(r"ALWAYS invoke|ALWAYS load", d) and not always_loaded:
            probs.append("no ALWAYS-invoke imperative")
        if probs:
            issues += len(probs)
            print(f"FAIL {name}:")
            for pr in probs:
                print(f"  - {pr}")
        else:
            print(f"OK   {name} ({s['version']})")
    print(f"\n{issues} issue(s) found." if issues else "\nLint green: every description is a trigger contract.")
    return 1 if issues else 0


def battery() -> int:
    ss = skills()
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    lines = ["You will see skill descriptions, then user utterances.",
             "For each utterance, name the ONE skill to invoke, or the word none.",
             "Answer with a JSON object {\"<utterance number>\": \"<skill-or-none>\"} only.", "",
             "## Skill descriptions"]
    for name, s in ss.items():
        lines.append(f"- {name} ({s['version']}): {s['description']}")
    lines += ["", "## Utterances"]
    for i, fx in enumerate(fixtures, 1):
        lines.append(f"{i}. {fx['utterance']}")
    print("\n".join(lines))
    return 0


def answers(path: str, threshold: float) -> int:
    given = json.loads(Path(path).read_text(encoding="utf-8"))
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    correct = 0
    rows = []
    for i, fx in enumerate(fixtures, 1):
        got = str(given.get(str(i), given.get(fx["id"], "<missing>"))).strip()
        ok = got == fx["expect"]
        correct += ok
        rows.append(f"{'OK  ' if ok else 'MISS'} {fx['id']}: expect {fx['expect']!r}, got {got!r}")
    acc = correct / len(fixtures)
    print("\n".join(rows))
    print(f"\naccuracy: {correct}/{len(fixtures)} = {acc:.0%} (threshold {threshold:.0%})")
    return 0 if acc >= threshold else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", action="store_true")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--answers")
    ap.add_argument("--threshold", type=float, default=0.9)
    a = ap.parse_args()
    if a.lint:
        return lint()
    if a.battery:
        return battery()
    if a.answers:
        return answers(a.answers, a.threshold)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
