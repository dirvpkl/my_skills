# plugins/

Discovery for `fresh-eyes`. `SKILL.md` points here instead of hardcoding the
reference list, so adding a mode never means editing the core file's list.

## How discovery works
`manifest.json` lists every active module (`type: "core"` — ships with the
skill — or `type: "plugin"` — added later) plus a `planned` array for
reserved-but-not-built ideas. `dependencies` lists other skills in the
collection that load alongside this one.

## Adding a module
1. Add the file under `references/`.
2. Add an entry to `modules`: `id`, `name`, `path`, `type`, `version`, `description`.
3. Remove it from `planned` if it was there.
4. Bump `package_version` if behavior changed — log it in `../CHANGELOG.md`.

## Removing or disabling a module
Delete its entry (or move it to a `disabled` array of the same shape). A
manifest entry pointing at a deleted file breaks validation, so the file goes
only when the entry does.

## Validating
```
python scripts/validate_manifest.py
```
