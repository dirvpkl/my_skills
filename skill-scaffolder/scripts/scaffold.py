#!/usr/bin/env python3
"""
Scaffold a new skill directory in the skill-scaffolder layout.

Usage:
    python3 scripts/scaffold.py <skill-name> [--out <output-dir>] [--minimal]

--minimal   creates only SKILL.md (for a skill with no reference material
            or modules yet) instead of the full references/plugins/scripts layout.

Fills in {{SKILL_NAME}} and {{DATE}} placeholders in the templates.
Everything else ({{...}} placeholders describing what to write) is left
in place intentionally — those are prompts for the author to replace,
not values this script can know.
"""

import argparse
import datetime
import shutil
import sys
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "assets" / "templates"


def render(text: str, skill_name: str) -> str:
    today = datetime.date.today().isoformat()
    return text.replace("{{SKILL_NAME}}", skill_name).replace("{{DATE}}", today)


def scaffold(skill_name: str, out_dir: Path, minimal: bool) -> Path:
    skill_dir = out_dir / skill_name
    if skill_dir.exists():
        print(f"ERROR: {skill_dir} already exists — aborting to avoid overwrite.",
              file=sys.stderr)
        sys.exit(1)

    skill_dir.mkdir(parents=True)

    skill_md = render(
        (TEMPLATES_DIR / "SKILL.md.template").read_text(encoding="utf-8"),
        skill_name,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    if minimal:
        print(f"Scaffolded minimal skill at {skill_dir} (SKILL.md only).")
        return skill_dir

    (skill_dir / "VERSION").write_text("1.0.0\n", encoding="utf-8")

    changelog = render(
        (TEMPLATES_DIR / "CHANGELOG.md.template").read_text(encoding="utf-8"),
        skill_name,
    )
    (skill_dir / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

    (skill_dir / "references").mkdir()
    (skill_dir / "references" / ".gitkeep").write_text("", encoding="utf-8")

    (skill_dir / "assets").mkdir()
    (skill_dir / "assets" / ".gitkeep").write_text("", encoding="utf-8")

    plugins_dir = skill_dir / "plugins"
    plugins_dir.mkdir()

    manifest = render(
        (TEMPLATES_DIR / "manifest.json.template").read_text(encoding="utf-8"),
        skill_name,
    )
    (plugins_dir / "manifest.json").write_text(manifest, encoding="utf-8")

    plugins_readme = render(
        (TEMPLATES_DIR / "plugins-readme.md.template").read_text(encoding="utf-8"),
        skill_name,
    )
    (plugins_dir / "README.md").write_text(plugins_readme, encoding="utf-8")

    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    validator = (TEMPLATES_DIR / "validate_manifest.py.template").read_text(encoding="utf-8")
    (scripts_dir / "validate_manifest.py").write_text(validator, encoding="utf-8")

    print(f"Scaffolded skill at {skill_dir}:")
    for p in sorted(skill_dir.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(skill_dir)}")

    return skill_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_name", help="Name of the new skill (used as folder name and in templates)")
    parser.add_argument("--out", default=".", help="Directory to create the skill folder in (default: cwd)")
    parser.add_argument("--minimal", action="store_true",
                         help="Create only SKILL.md, skip references/plugins/scripts/assets")
    args = parser.parse_args()

    scaffold(args.skill_name, Path(args.out), args.minimal)


if __name__ == "__main__":
    main()
