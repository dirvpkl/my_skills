# manifest-format — plugins/manifest.json (lean, 2026-11-15)

```json
{
  "skill": "skill-name",
  "dependencies": ["other-skill"],
  "planned": [
    { "id": "future-module", "name": "Future module", "description": "What it will be." }
  ]
}
```

The manifest answers ONE question: **which other collection skills load
alongside this one** (`dependencies`). Everything else about the skill's
insides lives where it belongs:

- the folder layout IS the module list — no `modules` array;
- versions live in `VERSION` (matching the SKILL.md frontmatter) and
  CHANGELOG.md — no `package_version` in the manifest;
- external (harness-side) skills are wired by the harness itself — no
  `dependencies_runtime`; if a machine fact is needed, it goes in the
  skill's own `runtime.toml`.

## Fields

- **`skill`** — the folder name; must match the directory it sits in
  (the repo validator errors on a mismatch).
- **`dependencies`** — collection-sibling skill names only, never paths,
  never self-reference. A name that resolves to no sibling folder fails
  the repo validator loudly.
- **`planned`** — reserved future pieces: `{id, name, description}` each.
  Planned entries build nothing; they mark intent.

## Validation

Repo-wide: `python -I scripts/validate.py --skills <name>` from the
collection root. There are no per-skill validator scripts (removed
2026-11-15) — the root walk checks frontmatter, VERSION sync, the lean
manifest shape, dependency resolution, per-skill runtime.toml parse, and
wiki-links.
