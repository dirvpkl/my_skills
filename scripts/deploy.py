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
                             [--force] [--backup DIR] [--diff] [--symlink]

Exit 0 = installed/upgraded/skipped, all clean. Exit 1 = at least one
conflict (listed, untouched) or a copy failure. Exit 2 = usage error
(unknown skill name).
"""

import argparse
import difflib
import hashlib
import os
import re
import stat
import subprocess
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


def _digest(p: Path) -> str:
    """Content hash that ignores line endings for text files.

    A repo checked out on Windows carries CRLF while a copy deployed on either
    platform carries LF, so a byte-identical comparison reports a conflict for
    every text file in the skill. That is noise, and it is not harmless noise:
    the conflict path refuses to touch the destination, so a genuine fix to one
    file cannot be deployed at all until the whole tree is forced.

    Normalize newlines for anything that decodes as UTF-8 and contains no NUL;
    hash raw bytes for everything else, so a real change in a binary asset — or
    a change that is only that the file stopped being text — still registers.
    """
    raw = p.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return "raw:" + hashlib.sha256(raw).hexdigest()
    if "\0" in text:
        return "raw:" + hashlib.sha256(raw).hexdigest()
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return "text:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def tree_hashes(d: Path) -> dict:
    out = {}
    for p in sorted(d.rglob("*")):
        if p.is_file():
            out[p.relative_to(d).as_posix()] = _digest(p)
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


def is_link_path(p: Path) -> bool:
    """True for real OS symlinks and Windows directory junctions/reparse points."""
    try:
        st = p.lstat()
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(st.st_mode):
        return True
    # Windows reparse point (junction or symlink created without POSIX mode).
    return bool(getattr(st, "st_file_attributes", 0) & 0x0400)


def link_target(p: Path) -> Path | None:
    try:
        raw = os.readlink(str(p))
    except OSError:
        return None
    if raw.startswith("\\\\?\\"):
        raw = raw[4:]
    target = Path(raw)
    if not target.is_absolute():
        target = p.parent / target
    try:
        return target.resolve(strict=False)
    except OSError:
        return target


def same_link(dst: Path, src: Path) -> bool:
    if not is_link_path(dst):
        return False
    t = link_target(dst)
    if t is None:
        return False
    try:
        return t == src.resolve(strict=False)
    except OSError:
        return t == src


def remove_destination(dst: Path, backup_dir: Path | None = None) -> None:
    """Remove a file/dir/link without following a junction into its target."""
    if is_link_path(dst):
        if os.name == "nt":
            subprocess.run(["cmd", "/c", "rmdir", str(dst)],
                          check=True, capture_output=True, text=True)
        else:
            os.unlink(dst)
        return
    if backup_dir is not None:
        backup_dir.mkdir(parents=True, exist_ok=True)
        bdst = backup_dir / (dst.name + "-" + time.strftime("%Y%m%d-%H%M%S"))
        shutil.move(str(dst), str(bdst))
        print(f"  backup: {dst} -> {bdst}")
        return
    if dst.is_dir() and not dst.is_symlink():
        shutil.rmtree(dst)
    else:
        dst.unlink()


def create_link(dst: Path, src: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        # Prefer a junction: needs no SeCreateSymbolicLink privilege.
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(dst), str(src)],
            check=True, capture_output=True, text=True,
        )
    else:
        os.symlink(src, dst, target_is_directory=True)


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
    ap.add_argument("--symlink", "--link", dest="link", action="store_true",
                    help="create directory symlinks/junctions instead of copying")
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
        if args.link:
            if same_link(dst, src):
                print(f"skip {name}: already linked -> {src}")
                continue
            if dst.exists() or dst.is_symlink() or is_link_path(dst):
                if not args.force:
                    conflicts.append(name)
                    print(f"CONFLICT {name}: destination exists and is not the same link - skipped")
                    if args.diff and dst.exists():
                        show_diffs(src, dst, name)
                    continue
                backup_dir = Path(args.backup) if args.backup else None
                if args.dry_run:
                    repl = (f"backup -> {backup_dir}" if backup_dir
                            else "delete destination")
                    print(f"would replace {name}: {repl}")
                else:
                    try:
                        remove_destination(dst, backup_dir)
                    except OSError as e:
                        print(f"ERROR deploying {name}: {e}", file=sys.stderr)
                        return 1
            label = "would link" if args.dry_run else "link"
            print(f"{label} {name}: {src} -> {dst}")
            if args.dry_run:
                done.append(name)
                continue
            try:
                create_link(dst, src)
                done.append(name)
            except (OSError, subprocess.CalledProcessError) as e:
                print(f"ERROR deploying {name}: {e}", file=sys.stderr)
                return 1
            continue

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
