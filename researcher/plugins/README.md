# plugins/

Discovery mechanism for this skill's modules. `SKILL.md` does not hardcode a list of reference files — it points here instead, so adding or removing a module never requires editing the core file.

## How discovery works
`manifest.json` lists every active module (`type: "core"` — always loaded, part of the base skill — or `type: "plugin"` — optional, added later) plus a `planned` list of reserved-but-not-built ideas. When running this skill, check `manifest.json` to see what's currently active rather than assuming the original three reference files are the whole picture.

## Adding a new module
1. Add the file under `references/` (for a doc-style module) or `plugins/` (for a self-contained plugin with its own sub-files).
2. Add an entry to `manifest.json`'s `modules` list: `id`, `name`, `path`, `type` (`core` or `plugin`), `version`, `description`.
3. If it was in `planned`, remove it from there.
4. Bump `skill_version` in both `manifest.json` and `SKILL.md`'s frontmatter if the addition changes overall skill behavior (see `../CHANGELOG.md`).

Nothing else needs to change — `SKILL.md` reads the manifest rather than an inlined list, so this is the only file that needs a new line.

## Removing or disabling a module
Delete its entry from `manifest.json` (or move it to a `disabled` list, following the same shape as `planned`, if it should stay documented but inactive). Don't delete the underlying file unless it's genuinely obsolete — parking it costs nothing.

## Validating the manifest
`scripts/validate_manifest.py` checks that every `path` in `manifest.json` actually exists on disk and that the JSON is well-formed. Run it after editing the manifest by hand:

```
python3 scripts/validate_manifest.py
```
