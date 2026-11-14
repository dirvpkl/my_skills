# plugins/

Discovery for `mission`. `SKILL.md` points here instead of hardcoding the
reference list.

## How discovery works
`manifest.json` lists active modules (`type: "core"` ships with the skill,
`type: "plugin"` added later), the `planned` array for reserved-but-not-built
ideas, and `dependencies` — the other skills in the collection that load with
this one.

## Adding a module
1. Add the file under `references/`.
2. Add an entry to `modules`: `id`, `name`, `path`, `type`, `version`, `description`.
3. Remove it from `planned` if it was there.
4. Bump `package_version` if behavior changed — log it in `../CHANGELOG.md`.

## Adding a dependency
Add the sibling skill folder name to `dependencies` and say in SKILL.md why it
loads alongside this one. A dependency is a top-level skill folder, not a module
inside a package.

## Validating
```
python scripts/validate_manifest.py
```