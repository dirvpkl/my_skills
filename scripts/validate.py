#!/usr/bin/env python3
"""Repo-wide skill validation.

For every directory under the repo root that contains a SKILL.md:
  1. frontmatter has name, description, version;
  2. VERSION file (if present) matches the frontmatter version;
  3. the skill's own scripts/validate_manifest.py (if present) passes.

Repo-side checks that run alongside the per-skill walk:
  4. runtime.toml next to the live catalog parses, and every
     [skills] external_roots entry exists on disk (an absent file is a
     WARN: a fresh machine simply has no roots configured yet);
  5. double-bracket wiki-links in skill markdown resolve to a topic or
     repo directory (dangling = WARN, workplanx semantics; backticked
     mentions are documentation, not links, and are skipped — so are
     CHANGELOG files, which quote the convention as history).

Missing VERSION/manifest is a warning, not an error (small skills are allowed
a scaled-down layout per skill-scaffolder) — except a sub-skill registered in
its parent package's manifest, which needs no manifest of its own. Any
mismatch is an error.

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
RUNTIME_TOML = Path.home() / ".agents" / "skills" / "runtime.toml"


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


def registered_in_parent(d: Path) -> bool:
    """True when d is a sub-skill registered as a module of its parent package."""
    if not (d.parent / "SKILL.md").exists():
        return False
    parent_manifest = d.parent / "plugins" / "manifest.json"
    if not parent_manifest.exists():
        return False
    try:
        data = json.loads(parent_manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    want = f"{d.name}/SKILL.md"
    return any(m.get("path") == want for m in data.get("modules", []))


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


def check_runtime_toml() -> tuple[list, list]:
    """runtime.toml: absent = WARN (unconfigured machine), broken = error."""
    errors, warnings = [], []
    if not RUNTIME_TOML.exists():
        warnings.append(
            f"runtime.toml not found ({RUNTIME_TOML}) — external skill roots "
            f"unconfigured on this machine"
        )
        return errors, warnings
    try:
        import tomllib
    except ModuleNotFoundError:
        warnings.append("python >= 3.11 (tomllib) — cannot verify runtime.toml")
        return errors, warnings
    try:
        data = tomllib.loads(RUNTIME_TOML.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"runtime.toml is not valid TOML: {e}")
        return errors, warnings
    roots = data.get("skills", {}).get("external_roots", [])
    if not isinstance(roots, list):
        errors.append("runtime.toml [skills] external_roots must be a list of paths")
        return errors, warnings
    for r in roots:
        if not Path(str(r)).expanduser().is_dir():
            errors.append(f"runtime.toml external root does not exist: {r}")
    return errors, warnings


def check_wiki_links() -> list:
    """[[target]] in skill markdown resolves like workplanx topics; dangling = WARN.

    Code (fenced blocks and backticked spans) documents the convention itself,
    so mentions inside it are stripped before scanning — a literal `[[example]]`
    in prose docs is not a link and must not warn.
    """
    warnings = []
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        rel = md.relative_to(ROOT)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if md.name.upper().startswith("CHANGELOG"):
            continue  # history quotes the convention; it is not navigation
        text = md.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        for target in re.findall(r"\[\[([^\]]+)\]\]", text):
            if not ((ROOT / ".workplanx" / target).exists() or (ROOT / target).exists()):
                warnings.append(f"{rel.as_posix()}: dangling [[{target}]]")
    return warnings


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
        elif not registered_in_parent(d):
            warnings.append(f"{rel}: no plugins/manifest.json")

        checker = d / "scripts" / "validate_manifest.py"
        if checker.exists():
            r = subprocess.run([sys.executable, str(checker)],
                               capture_output=True, text=True)
            if r.returncode != 0:
                errors.append(f"{rel}: own validate_manifest.py failed:\n{r.stderr.strip()}")

    rt_errors, rt_warnings = check_runtime_toml()
    errors.extend(rt_errors)
    warnings.extend(rt_warnings)
    warnings.extend(check_wiki_links())

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
