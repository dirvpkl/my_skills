#!/usr/bin/env python3
"""Scaffold a new skill folder in this repo via skill-scaffolder.

Usage:
    python scripts/new_skill.py <skill-name> [--minimal] [--out DIR]

Default output dir is the repo root. After scaffolding, fill in SKILL.md,
register modules in plugins/manifest.json, run scripts/validate.py, then
commit. See skill-scaffolder/SKILL.md for the full method.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "skill-scaffolder" / "scripts" / "scaffold.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="new skill folder name")
    ap.add_argument("--minimal", action="store_true",
                    help="SKILL.md only, no references/plugins/scripts")
    ap.add_argument("--out", default=str(ROOT),
                    help="parent dir for the new skill (default: repo root)")
    args = ap.parse_args()

    dest = Path(args.out) / args.name
    if dest.exists():
        print(f"ERROR: {dest} already exists", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(SCAFFOLD), args.name, "--out", str(args.out)]
    if args.minimal:
        cmd.append("--minimal")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        return r.returncode
    print(f"scaffolded: {dest}")
    print("next: fill in SKILL.md, register manifest, run scripts/validate.py, commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
