#!/usr/bin/env python3
"""Deploy skills from this repo into a live agent skills directory.

Copies top-level skill folders (never README.md, AGENTS.md, scripts/,
.gitignore). coding/ sub-skills always travel with the coding/ package.

Usage:
    python scripts/deploy.py [--target DIR] [--skills a,b] [--dry-run]

Defaults: target = $MY_SKILLS_TARGET or ~/.agents/skills, all skills.
Exit 0 = done, 1 = unknown skill name or copy failure (fail loud, no partial
deploy: validation of names happens before anything is copied).
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = Path(
    os.environ.get("MY_SKILLS_TARGET", Path.home() / ".agents" / "skills")
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=str(DEFAULT_TARGET),
                    help="live skills directory (default: $MY_SKILLS_TARGET or ~/.agents/skills)")
    ap.add_argument("--skills", default="",
                    help="comma-separated skill folders to deploy (default: all)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print what would be copied, copy nothing")
    args = ap.parse_args()

    available = sorted(
        d.name for d in ROOT.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists() and not d.name.startswith(".")
    )
    wanted = [s.strip() for s in args.skills.split(",") if s.strip()] or available

    unknown = [s for s in wanted if s not in available]
    if unknown:
        print(f"ERROR: unknown skill(s): {unknown}. Available: {available}",
              file=sys.stderr)
        return 1

    target = Path(args.target)
    for name in wanted:
        src = ROOT / name
        dst = target / name
        if args.dry_run:
            print(f"would copy: {src} -> {dst}")
            continue
        try:
            target.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"deployed: {name} -> {dst}")
        except OSError as e:
            print(f"ERROR deploying {name}: {e}", file=sys.stderr)
            return 1
    if args.dry_run:
        print(f"(dry run, target {target} untouched)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
