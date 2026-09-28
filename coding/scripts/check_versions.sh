#!/usr/bin/env bash
# check_versions.sh — validates the coding package's per-skill versioning
# against plugins/manifest.json. Per-skill versions are independent; this
# script does NOT require every SKILL.md to share one version. It checks:
#   1. Every module in manifest.json resolves to a real SKILL.md.
#   2. That SKILL.md's frontmatter `version` matches manifest.json's version
#      for that module (they drift when someone bumps one but not the other).
#   3. Every module's VERSION file matches its own frontmatter version.
#   4. (Report only, not an error) whether any module's version is ahead of
#      the package_version in manifest.json — a signal to consider bumping
#      package_version, not necessarily a mistake.
#
# Usage: ./check_versions.sh [path-to-coding-package]  (defaults to parent dir)

set -uo pipefail

ROOT_DIR="${1:-$(dirname "$0")/..}"
MANIFEST="$ROOT_DIR/plugins/manifest.json"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found — this script needs it to parse plugins/manifest.json."
  exit 1
fi

if [[ ! -f "$MANIFEST" ]]; then
  echo "ERROR: $MANIFEST not found."
  exit 1
fi

python3 - "$ROOT_DIR" "$MANIFEST" <<'PYEOF'
import json
import re
import sys
from pathlib import Path

root_dir = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])

try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    print(f"ERROR: plugins/manifest.json is not valid JSON: {e}")
    sys.exit(1)

package_version = manifest.get("package_version")
modules = manifest.get("modules", [])
issues = 0

if not package_version:
    print("ERROR: manifest.json is missing package_version.")
    issues += 1
else:
    print(f"Package version (manifest.json): {package_version}")

root_version_file = root_dir / "VERSION"
if root_version_file.exists():
    root_version = root_version_file.read_text(encoding="utf-8").strip()
    if root_version != package_version:
        print(f"MISMATCH: root VERSION file ({root_version}) != manifest package_version ({package_version})")
        issues += 1
else:
    print("MISSING: root VERSION file not found.")
    issues += 1

print()
print("== Checking modules ==")

seen_ids = set()

def parse_ver(v):
    # crude semver tuple for comparison; falls back to string compare on failure
    try:
        return tuple(int(x) for x in v.split("."))
    except (ValueError, AttributeError):
        return None

pkg_ver_tuple = parse_ver(package_version) if package_version else None

for mod in modules:
    mod_id = mod.get("id", "<no id>")
    print(f"-- {mod_id} --")

    if mod_id in seen_ids:
        print(f"   ERROR: duplicate module id '{mod_id}'")
        issues += 1
    seen_ids.add(mod_id)

    for field in ("id", "name", "path", "type", "version", "description"):
        if field not in mod:
            print(f"   ERROR: missing required field '{field}'")
            issues += 1

    rel_path = mod.get("path")
    if not rel_path:
        continue

    skill_md = root_dir / rel_path
    if not skill_md.exists():
        print(f"   ERROR: path does not resolve: {rel_path}")
        issues += 1
        continue
    print(f"   OK: path resolves ({rel_path})")

    text = skill_md.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    frontmatter_version = None
    if fm_match:
        v_match = re.search(r"^version:\s*(\S+)", fm_match.group(1), re.MULTILINE)
        if v_match:
            frontmatter_version = v_match.group(1).strip().strip('"').strip("'")

    if not frontmatter_version:
        print("   ERROR: no 'version' field found in SKILL.md frontmatter.")
        issues += 1
    elif frontmatter_version != mod.get("version"):
        print(f"   MISMATCH: SKILL.md frontmatter version ({frontmatter_version}) != manifest version ({mod.get('version')})")
        issues += 1
    else:
        print(f"   OK: frontmatter version matches manifest ({frontmatter_version})")

    skill_dir = skill_md.parent
    version_file = skill_dir / "VERSION"
    if version_file.exists():
        file_version = version_file.read_text(encoding="utf-8").strip()
        if frontmatter_version and file_version != frontmatter_version:
            print(f"   MISMATCH: VERSION file ({file_version}) != frontmatter version ({frontmatter_version})")
            issues += 1
        else:
            print(f"   OK: VERSION file matches ({file_version})")
    else:
        print(f"   MISSING: no VERSION file in {skill_dir}")
        issues += 1

    # Report-only drift check: is this module ahead of the package version?
    mod_ver_tuple = parse_ver(mod.get("version"))
    if pkg_ver_tuple and mod_ver_tuple and mod_ver_tuple > pkg_ver_tuple:
        print(f"   NOTE: module version ({mod.get('version')}) is ahead of package_version ({package_version}) — consider bumping package_version.")

    print()

print("== Summary ==")
if issues == 0:
    print("All modules valid, no version mismatches found.")
else:
    print(f"{issues} issue(s) found — see above.")

sys.exit(1 if issues else 0)
PYEOF
