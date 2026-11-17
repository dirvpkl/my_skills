# plugins/

Discovery mechanism for this skill's modules. `SKILL.md` points here instead of hardcoding a list of reference files, so adding or removing a module never requires editing the core file.

## How discovery works
`manifest.json` lists every active module (`type: "core"` — part of the base skill — or `type: "plugin"` — added later) plus a `planned` list of reserved-but-not-built ideas.

## Adding a module
1. Add the file under `references/` or `plugins/`.
2. Add an entry to `manifest.json`'s `modules` list: `id`, `name`, `path`, `type`, `version`, `description`.
3. Remove it from `planned` if it was there.
4. Bump `package_version` if the addition changes overall behavior — log it in `../CHANGELOG.md`.

## Removing or disabling a module
Delete its entry from `manifest.json` (or move to a `disabled` list of the same shape). Leave the underlying file unless it's genuinely obsolete.

## Validating
```
python3 scripts/validate_manifest.py
```
