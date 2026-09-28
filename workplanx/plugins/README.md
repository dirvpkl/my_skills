# plugins/

Discovery for this skill's modules. `SKILL.md` points here instead of hardcoding lists.

## Adding a module
1. Add the file under `references/` or `scripts/`.
2. Register `id`, `name`, `path`, `type`, `version`, `description` in `manifest.json`.
3. Bump `package_version` on behavior change — log in `../CHANGELOG.md`.
