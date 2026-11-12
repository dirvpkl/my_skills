#!/usr/bin/env python3
"""
Validate plugins/manifest.json for this skill.

Checks:
  - manifest.json is valid JSON
  - every module's "path" exists on disk, relative to the skill root
  - no duplicate module ids
  - required fields are present on every module entry
  - a module's "type" is one of core / plugin / reference
  - "package_version" matches the root VERSION file
  - a module pointing at a SKILL.md has a "version" matching its frontmatter
  - every name in "dependencies" resolves to a real sibling skill folder
    (a folder with a SKILL.md next to this one)
  - every name in "dependencies_runtime" resolves through an external root
    declared in runtime.toml ([skills] external_roots, next to the live
    skill catalog); an unresolved name fails loudly, listing every root tried

Usage:
    python3 scripts/validate_manifest.py
Exit code 0 = clean, 1 = problems found (printed to stderr).
"""

import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = SKILL_ROOT / "plugins" / "manifest.json"
VERSION_PATH = SKILL_ROOT / "VERSION"
COLLECTION_ROOT = SKILL_ROOT.parent
RUNTIME_TOML = Path.home() / ".agents" / "skills" / "runtime.toml"
REQUIRED_FIELDS = ["id", "name", "path", "type", "version", "description"]
MODULE_TYPES = ("core", "plugin", "reference")


def frontmatter_version(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^---\s*$(.*?)^---\s*$", text, re.M | re.S)
    if not m:
        return None
    v = re.search(r"^version\s*:\s*(\S+)\s*$", m.group(1), re.M)
    return v.group(1) if v else None


def runtime_external_roots(problems: list) -> list[str]:
    """External skill roots from runtime.toml; a broken file is a problem, never silence."""
    if not RUNTIME_TOML.exists():
        return []
    try:
        import tomllib
    except ModuleNotFoundError:
        problems.append("python >= 3.11 required to read runtime.toml (tomllib missing)")
        return []
    try:
        data = tomllib.loads(RUNTIME_TOML.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"runtime.toml is not valid TOML: {RUNTIME_TOML}: {e}")
        return []
    roots = data.get("skills", {}).get("external_roots", [])
    if not isinstance(roots, list):
        problems.append(
            f"runtime.toml [skills] external_roots must be a list of paths: {RUNTIME_TOML}"
        )
        return []
    return [str(r) for r in roots]


def main() -> int:
    problems = []

    if not MANIFEST_PATH.exists():
        print(f"ERROR: manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        return 1

    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: manifest.json is not valid JSON: {e}", file=sys.stderr)
        return 1

    if VERSION_PATH.exists():
        declared = manifest.get("package_version")
        on_disk = VERSION_PATH.read_text(encoding="utf-8").strip()
        if declared is not None and declared != on_disk:
            problems.append(
                f"package_version '{declared}' != VERSION file '{on_disk}'"
            )

    modules = manifest.get("modules", [])
    seen_ids = set()

    for i, mod in enumerate(modules):
        missing = [f for f in REQUIRED_FIELDS if f not in mod]
        if missing:
            problems.append(f"module[{i}] missing required field(s): {missing}")
            continue

        if mod["id"] in seen_ids:
            problems.append(f"duplicate module id: '{mod['id']}'")
        seen_ids.add(mod["id"])

        if mod["type"] not in MODULE_TYPES:
            problems.append(
                f"module '{mod['id']}' type '{mod['type']}' must be one of "
                f"{', '.join(MODULE_TYPES)}"
            )

        mod_path = SKILL_ROOT / mod["path"]
        if not mod_path.exists():
            problems.append(
                f"module '{mod['id']}' points to missing file: '{mod['path']}'"
            )
        elif mod_path.name == "SKILL.md":
            fm = frontmatter_version(mod_path)
            if fm and fm != mod["version"]:
                problems.append(
                    f"module '{mod['id']}' version '{mod['version']}' != "
                    f"{mod['path']} frontmatter '{fm}'"
                )

    for dep in manifest.get("dependencies", []):
        dep_root = COLLECTION_ROOT / dep
        if not (dep_root / "SKILL.md").exists():
            problems.append(
                f"dependency '{dep}' has no SKILL.md at {dep_root}"
            )
        if dep == SKILL_ROOT.name:
            problems.append(f"skill '{dep}' depends on itself")

    runtime_deps = manifest.get("dependencies_runtime", [])
    if runtime_deps:
        roots = [Path(r).expanduser() for r in runtime_external_roots(problems)]
        for dep in runtime_deps:
            if dep == SKILL_ROOT.name:
                problems.append(f"skill '{dep}' depends on itself")
            found = any((root / dep / "SKILL.md").exists() for root in roots)
            if not found:
                searched = ", ".join(str(r) for r in roots) or "none declared"
                problems.append(
                    f"runtime dependency '{dep}' has no SKILL.md in any external root "
                    f"(runtime.toml [skills] external_roots searched: {searched})"
                )

    if problems:
        print("Manifest validation FAILED:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1

    print(f"Manifest OK: {len(modules)} active module(s), "
          f"{len(manifest.get('planned', []))} planned.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
