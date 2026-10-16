#!/usr/bin/env python3
"""Repo-wide skill validation.

For every directory under the repo root that contains a SKILL.md:
  1. frontmatter has name, description, version;
  2. VERSION file (if present) matches the frontmatter version;
  3. the skill's own scripts/validate_manifest.py (if present) passes.

Missing VERSION/manifest is a warning, not an error (small skills are allowed
a scaled-down layout per skill-scaffolder). Any mismatch is an error.

Usage:
    python scripts/validate.py [--skills a,b]
Exit 0 = clean, 1 = problems found.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^---\s*$(.*?)^---\s*$", text, re.M | re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^(\w+)\s*:\s*(.+?)\s*$", line)
        if mm:
            out[mm.group(1)] = mm.group(2)
    return out


def iter_skills():
    for skill_md in sorted(ROOT.rglob("SKILL.md")):
        d = skill_md.parent
        if ".git" in d.parts:
            continue
        if any(part.startswith(".") for part in d.relative_to(ROOT).parts):
            continue
        if d == ROOT:
            continue
        yield d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", default="",
                    help="comma-separated skill dir names to check (default: all)")
    args = ap.parse_args()
    only = {s.strip() for s in args.skills.split(",") if s.strip()}

    errors, warnings = [], []

    for d in iter_skills():
        if any(part.startswith(".") for part in d.relative_to(ROOT).parts):
            continue
        rel = d.relative_to(ROOT).as_posix()
        if only and d.name not in only and rel not in only:
            continue

        fm = frontmatter(d / "SKILL.md")
        for field in ("name", "description", "version"):
            if not fm.get(field):
                errors.append(f"{rel}: SKILL.md frontmatter missing '{field}'")

        ver_file = d / "VERSION"
        if ver_file.exists():
            on_disk = ver_file.read_text(encoding="utf-8").strip()
            if fm.get("version") and on_disk != fm["version"]:
                errors.append(
                    f"{rel}: VERSION file '{on_disk}' != frontmatter '{fm['version']}'"
                )
        else:
            warnings.append(f"{rel}: no VERSION file (scaled-down layout?)")

        manifest = d / "plugins" / "manifest.json"
        if manifest.exists():
            try:
                json.loads(manifest.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                errors.append(f"{rel}: manifest.json invalid JSON: {e}")
        else:
            warnings.append(f"{rel}: no plugins/manifest.json")

        checker = d / "scripts" / "validate_manifest.py"
        if checker.exists():
            r = subprocess.run([sys.executable, str(checker)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                errors.append(f"{rel}: own validate_manifest.py failed:\n{r.stderr.strip()}")

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("All skills valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
