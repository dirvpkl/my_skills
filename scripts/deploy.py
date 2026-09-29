#!/usr/bin/env python3
"""Safe-deploy skills from this repo into a live agent skills directory.

Copies top-level skill folders (never README.md, AGENTS.md, scripts/,
.gitignore). coding/ sub-skills always travel with the coding/ package.

Per-skill decision (safe by default, nothing is overwritten blindly):
  - destination missing          -> install
  - source version > dest version -> upgrade (same lineage, safe)
  - same version, identical files -> skip (up to date)
  - same version, files differ    -> CONFLICT: warn, do not touch
  - source version < dest version -> CONFLICT: would be a downgrade
  - version missing/unparseable   -> hash compare: identical = skip,
                                     differ = CONFLICT

Usage:
    python scripts/deploy.py [--target DIR] [--skills a,b] [--dry-run]
                             [--force] [--backup DIR] [--diff]

Exit 0 = installed/upgraded/skipped, all clean. Exit 1 = at least one
conflict (listed, untouched) or a copy failure. Exit 2 = usage error
(unknown skill name).
"""

import argparse
import difflib
import hashlib
import os
import re
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGET = Path(
    os.environ.get("MY_SKILLS_TARGET", Path.home() / ".agents" / "skills")
)
DIFF_MAX_FILES = 10
DIFF_MAX_LINES = 50


def frontmatter_version(skill_md: Path) -> str | None:
    try:
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None
    m = re.search(r"^---\s*$(.*?)^---\s*$", text, re.M | re.S)
    if not m:
        return None
    v = re.search(r"^version\s*:\s*(\S+)\s*$", m.group(1), re.M)
    return v.group(1) if v else None


def parse_semver(v: str) -> tuple | None:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", v.strip())
    return tuple(map(int, m.groups())) if m else None


def tree_hashes(d: Path) -> dict:
    out = {}
    for p in sorted(d.rglob("*")):
        if p.is_file():
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            out[p.relative_to(d).as_posix()] = h.hexdigest()
    return out


def iter_diff_files(src: Path, dst: Path):
    a, b = tree_hashes(src), tree_hashes(dst)
    for rel in sorted(set(a) & set(b)):
        if a[rel] != b[rel]:
            yield rel, "modified"
    for rel in sorted(set(a) - set(b)):
        yield rel, "new-in-source"
    for rel in sorted(set(b) - set(a)):
        yield rel, "only-in-dest"


def show_diffs(src: Path, dst: Path, name: str):
    shown = 0
    for rel, kind in iter_diff_files(src, dst):
        if kind != "modified" or shown >= DIFF_MAX_FILES:
            if kind != "modified":
                print(f"    {kind}: {rel}")
            continue
        try:
            a = (src / rel).read_text(encoding="utf-8").splitlines()
            b = (dst / rel).read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            print(f"    modified (binary/unreadable): {rel}")
            continue
        print(f"    modified: {rel}")
        for line in list(difflib.unified_diff(
                b, a, fromfile=f"dest/{rel}", tofile=f"source/{rel}"))[:DIFF_MAX_LINES]:
            print(f"      {line.rstrip()}")
        shown += 1


def decide(src: Path, dst: Path) -> tuple:
    """Return (action, detail). action in install/upgrade/skip/conflict."""
    if not dst.exists():
        return "install", "not present at destination"
    if not (dst / "SKILL.md").exists():
        return "conflict", f"{dst} exists but is not a skill (no SKILL.md)"
    sv, dv = frontmatter_version(src / "SKILL.md"), frontmatter_version(dst / "SKILL.md")
    sp, dp = parse_semver(sv or ""), parse_semver(dv or "")
    if sp is not None and dp is not None:
        if sp > dp:
            return "upgrade", f"{dv} -> {sv}"
        if sp < dp:
            return "conflict", f"source {sv} older than dest {dv} (downgrade refused)"
    if tree_hashes(src) == tree_hashes(dst):
        return "skip", f"identical ({sv or 'unversioned'})"
    return "conflict", f"same version ({sv or 'unversioned'}) but files differ"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=str(DEFAULT_TARGET),
                    help="live skills directory (default: $MY_SKILLS_TARGET or ~/.agents/skills)")
    ap.add_argument("--skills", default="",
                    help="comma-separated skill folders (default: all)")
    ap.add_argument("--dry-run", action="store_true",
                    help="decide and report, copy nothing")
    ap.add_argument("--force", action="store_true",
                    help="overwrite conflicts too (still reported)")
    ap.add_argument("--backup", default="",
                    help="with --force: move replaced dirs to DIR/<name>-<timestamp> instead of deleting")
    ap.add_argument("--diff", action="store_true",
                    help="show unified diffs for conflicting text files")
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
        return 2
    if args.backup and not args.force:
        print("ERROR: --backup needs --force (nothing is replaced otherwise)",
              file=sys.stderr)
        return 2

    target = Path(args.target)
    conflicts, done = [], []
    for name in wanted:
        src, dst = ROOT / name, target / name
        action, detail = decide(src, dst)
        forced = action == "conflict" and args.force
        if action == "conflict" and not args.force:
            conflicts.append(name)
            print(f"CONFLICT {name}: {detail} — skipped, destination untouched")
            if args.diff:
                show_diffs(src, dst, name)
            continue
        if action == "skip":
            print(f"skip {name}: {detail}")
            continue
        label = "would " + action if args.dry_run else ("overwrite" if forced else action)
        extra = f" [FORCED, was: {detail}]" if forced else ""
        print(f"{label} {name}: {detail}{extra}")
        if args.dry_run:
            done.append(name)
            continue
        try:
            if dst.exists():
                if args.backup:
                    bdir = Path(args.backup)
                    bdir.mkdir(parents=True, exist_ok=True)
                    bdst = bdir / f"{name}-{time.strftime('%Y%m%d-%H%M%S')}"
                    shutil.move(str(dst), str(bdst))
                    print(f"  backup: {dst} -> {bdst}")
                else:
                    shutil.rmtree(dst)
            target.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)
            done.append(name)
        except OSError as e:
            print(f"ERROR deploying {name}: {e}", file=sys.stderr)
            return 1

    if conflicts:
        print(f"{len(conflicts)} conflict(s): {conflicts} — re-run with --force "
              f"(+ optional --backup DIR) to overwrite, or resolve by hand.",
              file=sys.stderr)
        return 1
    print(f"done: {len(done)} skill(s) installed/upgraded/skipped-clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
