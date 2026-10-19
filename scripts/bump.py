#!/usr/bin/env python3
"""Bump a skill version across all four places at once.

Updates SKILL.md frontmatter + VERSION file + manifest package_version and
prepends a CHANGELOG.md entry. For a coding/* sub-skill the coding/ package
version bumps too (repo rule), unless --no-package is passed.

A coding/* sub-skill logs its bumps in the package CHANGELOG (entries are
prefixed with the sub-skill path), so bump.py never creates a CHANGELOG.md
for one; a sub-skill that already has its own (proxy-egress) still gets
updated.

Usage:
    python scripts/bump.py <skill> [--major|--minor|--patch] -m "message" [--no-package]

<skill> is a repo-relative path: loop, workplanx, coding/testing, ...
Default bump is --patch. Date is stamped into CHANGELOG automatically.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def bump_version(v: str, part: str) -> str:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", v.strip())
    if not m:
        print(f"ERROR: version '{v}' is not X.Y.Z", file=sys.stderr)
        sys.exit(1)
    major, minor, patch = map(int, m.groups())
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def bump_one(skill_dir: Path, part: str, message: str,
             create_changelog: bool = True) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: no SKILL.md in {skill_dir}", file=sys.stderr)
        sys.exit(1)
    text = skill_md.read_text(encoding="utf-8")
    m = re.search(r"(?m)^version\s*:\s*(\S+)\s*$", text)
    if not m:
        print(f"ERROR: no version in {skill_md} frontmatter", file=sys.stderr)
        sys.exit(1)
    new = bump_version(m.group(1), part)
    text = text[:m.start(1)] + new + text[m.end(1):]
    skill_md.write_text(text, encoding="utf-8")

    ver_file = skill_dir / "VERSION"
    ver_file.write_text(new + "\n", encoding="utf-8")

    manifest = skill_dir / "plugins" / "manifest.json"
    if manifest.exists():
        mtext = manifest.read_text(encoding="utf-8")
        m2, n = re.subn(r'("package_version"\s*:\s*")[^"]*(")', rf"\g<1>{new}\g<2>", mtext, count=1)
        if n != 1:
            print(f"ERROR: package_version not found in {manifest}", file=sys.stderr)
            sys.exit(1)
        manifest.write_text(m2, encoding="utf-8")

    changelog = skill_dir / "CHANGELOG.md"
    if changelog.exists() or create_changelog:
        today = datetime.date.today().isoformat()
        entry = f"## [{new}] - {today}\n- {message}\n\n"
        if changelog.exists():
            old = changelog.read_text(encoding="utf-8")
            if old.startswith("# Changelog\n"):
                new_text = old.replace("# Changelog\n", f"# Changelog\n\n{entry}", 1)
            else:
                new_text = entry + old
        else:
            new_text = "# Changelog\n\n" + entry
        changelog.write_text(new_text, encoding="utf-8")
    return new


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill", help="repo-relative skill path, e.g. loop or coding/testing")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--major", action="store_true")
    group.add_argument("--minor", action="store_true")
    group.add_argument("--patch", action="store_true")
    ap.add_argument("-m", "--message", required=True, help="CHANGELOG entry (one line)")
    ap.add_argument("--no-package", action="store_true",
                    help="for coding/*: skip the coding/ package bump")
    args = ap.parse_args()

    part = "major" if args.major else "minor" if args.minor else "patch"
    rel = Path(args.skill).as_posix()
    is_sub_skill = rel.startswith("coding/") and rel != "coding"
    skill_dir = ROOT / args.skill
    new = bump_one(skill_dir, part, args.message,
                   create_changelog=not is_sub_skill)
    print(f"{args.skill}: -> {new}")

    if is_sub_skill and not args.no_package:
        pkg_new = bump_one(ROOT / "coding", part,
                           f"{rel} {new}: {args.message}")
        print(f"coding (package): -> {pkg_new}")
    print("next: run scripts/validate.py, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
