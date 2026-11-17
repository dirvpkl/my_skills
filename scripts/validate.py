#!/usr/bin/env python3
"""Repo-wide skill validation — the ONE validator (owner ruling 2026-11-15:
per-skill validate_manifest.py copies are deleted; this walk does all checks).

For every directory under the repo root that contains a SKILL.md:
  1. frontmatter has name, description, version;
  2. VERSION file (if present) matches the frontmatter version;
  3. plugins/manifest.json (if present) follows the LEAN shape:
     {skill, dependencies, planned} — no modules, no package_version,
     no dependencies_runtime (legacy keys = WARN); every dependency
     resolves to a sibling skill folder; planned entries carry an id;
  4. the skill's own runtime.toml (if present) parses — per-skill machine
     values, gitignored;
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
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGACY_MANIFEST_KEYS = ("modules", "package_version", "dependencies_runtime")


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
    """True when d is a sub-skill nested under a parent skill folder.

    The parent folder carrying a SKILL.md is the whole registration since
    the lean-manifest convention (2026-11-15) removed module lists — the
    folder layout is the module list.
    """
    return (d.parent / "SKILL.md").exists()


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


def check_manifest(d: Path, rel: str) -> tuple[list, list]:
    """LEAN manifest shape: {skill, dependencies, planned} only.

    dependencies resolve to sibling skill folders; legacy keys
    (modules/package_version/dependencies_runtime) warn — the convention
    is dead since 2026-11-15.
    """
    errors, warnings = [], []
    manifest = d / "plugins" / "manifest.json"
    if not manifest.exists():
        return errors, warnings
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{rel}: manifest.json invalid JSON: {e}"], []

    for key in LEGACY_MANIFEST_KEYS:
        if key in data:
            warnings.append(
                f"{rel}: manifest has legacy key '{key}' — lean shape since "
                f"2026-11-15 is {{skill, dependencies, planned}}"
            )
    if "skill" in data and data["skill"] != d.name:
        errors.append(f"{rel}: manifest 'skill' is '{data['skill']}' but the folder is '{d.name}'")
    deps = data.get("dependencies", [])
    if not isinstance(deps, list):
        errors.append(f"{rel}: manifest 'dependencies' must be a list")
    for dep in deps:
        if not (d.parent / dep / "SKILL.md").exists():
            errors.append(f"{rel}: manifest dependency has no skill folder: '{dep}'")
    planned = data.get("planned", [])
    if not isinstance(planned, list):
        errors.append(f"{rel}: manifest 'planned' must be a list")
    for entry in planned:
        if not isinstance(entry, dict) or not entry.get("id"):
            errors.append(f"{rel}: manifest planned entry missing 'id'")
    return errors, warnings


def check_skill_runtime(d: Path) -> tuple[list, list]:
    """A skill's own runtime.toml: values live per-skill, not at the root.

    Present file must parse; absent is fine (the skill simply needs no
    runtime values). The tracked runtime.example.toml beside the skill
    documents the shape, so a syntax error in it is an error too.
    """
    errors, warnings = [], []
    runtime = d / "runtime.toml"
    example = d / "runtime.example.toml"
    if example.exists():
        try:
            import tomllib
            tomllib.loads(example.read_text(encoding="utf-8"))
        except ModuleNotFoundError:
            pass
        except Exception as e:
            errors.append(f"{d.name}/runtime.example.toml is not valid TOML: {e}")
    if not runtime.exists():
        return errors, warnings
    try:
        import tomllib
    except ModuleNotFoundError:
        warnings.append("python >= 3.11 (tomllib) — cannot verify runtime.toml")
        return errors, warnings
    try:
        tomllib.loads(runtime.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"{d.name}/runtime.toml is not valid TOML: {e}")
    return errors, warnings


def check_exam_currency(warnings: list) -> None:
    """Descriptions changed in the working tree = the exam is stale.

    The exam (trigger_check --exam, 3+ models, 100%) is the only way to
    know how the changed descriptions surface — owner ruling 2026-11-15:
    it runs by default, there is no not-by-exam variant. The check is a
    git diff on description lines; a bare marker file (EXAM_RUN) newer
    than the last description change silences the warning.
    """
    import subprocess
    try:
        diff = subprocess.run(
            ["git", "diff", "HEAD", "--name-only"],
            capture_output=True, text=True, cwd=ROOT, timeout=30,
        ).stdout
    except Exception:
        return  # not a git checkout or git missing — nothing to compare
    changed = []
    for line in diff.splitlines():
        line = line.strip()
        if not line.endswith("SKILL.md") or "/" not in line:
            continue
        d = subprocess.run(
            ["git", "diff", "HEAD", "--", line],
            capture_output=True, text=True, cwd=ROOT, timeout=30,
        ).stdout
        for hunk in d.splitlines():
            if (hunk.startswith("+") and hunk[1:].startswith("description:")
                    and not hunk[1:].startswith("description: " + "#")):
                changed.append(line)
                break
    if changed:
        marker = ROOT / ".exam-run"
        if not (marker.exists()
                and marker.stat().st_mtime > __import__("time").time() - 3600 * 24):
            warnings.append(
                "descriptions changed without a fresh exam run: "
                + ", ".join(sorted(set(changed)))
                + " — run the exam (3+ models, 100%) before committing"
            )

    # Window 2 — descriptions drifting after the exam. The working-tree
    # diff goes silent after the commit (found live 2026-11-15), and a
    # commit-time comparison false-alarms on commits that carry exactly
    # what the exam verified. The .exam-run marker therefore stores a
    # hash of every description at exam time; drift in either direction
    # (edited after the exam, never re-examined) re-arms the warning.
    marker = ROOT / ".exam-run"
    if not marker.exists():
        warnings.append(
            "no exam-run marker — the surfacing of every description is "
            "unverified; run the exam (3+ models, 100%)"
        )
        return
    try:
        import hashlib
        import json as _json
        import sys as _sys
        # trigger_check.skills() is the single source of truth for how the
        # hashed payload is built — the same function the exam-time marker
        # was written from. The sibling import needs the script directory
        # on sys.path (isolated mode does not put it there).
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        from trigger_check import skills
        recorded = _json.loads(marker.read_text(encoding="utf-8"))
        payload = _json.dumps(
            {n: s["description"] for n, s in skills().items()},
            sort_keys=True, ensure_ascii=False)
        digest = hashlib.sha256(payload.encode()).hexdigest()[:16]
        if digest != recorded.get("desc_hash"):
            warnings.append(
                "descriptions drifted after the last exam pass — run the "
                "exam (3+ models, 100%) before treating the surfacing as "
                "verified"
            )
    except Exception:
        warnings.append(
            "the .exam-run marker is unreadable — run the exam "
            "(3+ models, 100%) to restore the verification record"
        )


def check_machine_values(errors: list) -> None:
    """Nothing machine-local lives in tracked files (owner rule, enforced —
    not remembered): runtime literals from any runtime.toml plus generic
    loopback/key patterns fail the validation with file:line."""
    import subprocess
    tracked = subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True, cwd=ROOT, timeout=30).stdout.splitlines()
    lits = set()
    for rt in ROOT.rglob("runtime.toml"):
        for m in re.finditer(r'"(http://[^"]{10,}|[0-9a-f]{32,})"', rt.read_text(encoding="utf-8")):
            lits.add(m.group(1))
    allow = ("chords/", "proxy-egress/")
    for f in tracked:
        if f.startswith(allow) or f.endswith("runtime.example.toml"):
            continue
        try:
            text = Path(f).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for lit in lits:
            if lit in text and len(lit) > 10:
                errors.append(f"{f}: machine value leaked into a tracked file ({lit[:16]}...)")
        m = re.search(r"127\.0\.0\.1:\d+|sk-[0-9a-f]{12,}", text)
        if m:
            errors.append(f"{f}: machine-local pattern {m.group(0)[:20]!r} — move it to a runtime.toml")


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

        if not (d / "plugins" / "manifest.json").exists() and not registered_in_parent(d):
            warnings.append(f"{rel}: no plugins/manifest.json")

        m_errors, m_warnings = check_manifest(d, rel)
        errors.extend(m_errors)
        warnings.extend(m_warnings)
        rt_errors, rt_warnings = check_skill_runtime(d)
        errors.extend(rt_errors)
        warnings.extend(rt_warnings)

    check_exam_currency(warnings)
    check_machine_values(errors)
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
