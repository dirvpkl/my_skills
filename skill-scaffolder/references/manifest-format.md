# manifest-format

Referenced by SKILL.md. The exact shape of `plugins/manifest.json` and the discovery mechanism it implements.

## Why a manifest at all
Without it, a growing skill tends toward one of two failure modes: either SKILL.md accumulates an inline, hand-maintained list of every reference file (which someone forgets to update when a file is added or removed), or new files get added with no reference anywhere and quietly go unused. A manifest fixes both: SKILL.md points at *the manifest*, not at individual files, so the file list only needs to be correct in one place.

## Schema
```json
{
  "skill": "skill-name",
  "package_version": "1.0.0",
  "dependencies": ["other-skill", "another-skill"],
  "modules": [
    {
      "id": "short-identifier",
      "name": "Human-readable title",
      "path": "references/example.md",
      "type": "core",
      "version": "1.0.0",
      "description": "One line: what this module adds and when it's loaded."
    }
  ],
  "planned": [
    {
      "id": "future-module-id",
      "name": "Future module title",
      "type": "plugin",
      "status": "not built",
      "description": "One line: what this would add, once built."
    }
  ]
}
```
`package_version` is the field name — not `skill_version`. Keep it consistent: any validator or version-check script written against this manifest reads `package_version`, and a manifest using a different key name for the same concept will silently fail that check rather than error clearly.

## `modules` vs `dependencies` — different questions, don't merge them

- **`modules`** — what's *inside this skill*: reference docs, or (package-level) nested sub-skills. Read them when this skill runs.
- **`dependencies`** — *other skills in the collection* that load alongside this one. Read them when this skill runs too, but they live in their own folders with their own `SKILL.md`.

Putting a sibling skill into `modules` doesn't work and shouldn't be made to: the validator requires `path`/`type`/`version` and checks that the path exists, and a sibling skill has none of those. Conversely, a dependency has no manifest entry here — it's owned by its own skill.

**Why this key exists at all.** The tempting alternative is to name the other skills in SKILL.md prose ("see `x` for Y, hand off to `z`"). That's the hardcoded-list anti-pattern in `anti-patterns.md` §2: a list maintained by hand in the file most likely to be edited for unrelated reasons, which rots silently and produces a link nobody notices is dead. In a manifest it's one place, and a validator can check it.

**Shape rules:**
- Names only — a **top-level** skill folder name, no paths, no versions, no "why". Why a dependency is needed belongs in that skill's own SKILL.md; the manifest records the fact of the link.
- **A package is the unit, not a module inside it.** If `other-skill` is a dispatcher package whose sub-skills live in folders beside its `SKILL.md`, depend on the package: `"dependencies": ["coding"]`, and name `coding/code-quality` in prose where you need the specific one. A dependency must resolve to a sibling folder that has a `SKILL.md` directly inside it — `validate_manifest.py` checks that, so a nested module name fails loudly instead of silently never loading.
- `dependencies` is optional. Omit it (or use `[]`) when a skill genuinely stands alone.
- A skill must not list itself. A dependency must resolve to a real sibling folder containing a `SKILL.md` — `validate_manifest.py` checks both, so a typo'd or renamed dependency fails loudly instead of quietly not loading.
- **Don't duplicate it in frontmatter.** The manifest is the single source. A `dependencies:` key in the YAML frontmatter would be a second copy that drifts, and no tool reads it anyway.

## Two levels of "module" — don't conflate them
This format supports two different granularities, and a skill should pick one and be consistent about it, not drift between them:
- **Reference-level** (the common case): each `modules` entry is a `references/*.md` file *within this one skill*. There's a single `SKILL.md`, a single `VERSION`, and the manifest tracks which reference docs are currently wired in. This is what the rest of this doc and the templates assume by default.
- **Package-level** (for a skill that is itself a dispatcher over several self-contained sub-skills, each with its own `SKILL.md`, its own `version`, and its own `VERSION` file — e.g. a `coding` package containing `git-workflow/SKILL.md`, `docker/SKILL.md`, etc.): each `modules` entry's `path` points at a *sub-skill's* `SKILL.md`, not a bare reference doc, and each sub-skill versions independently. `package_version` at the root is then "everything in this package is in sync as of this state," bumped whenever *any* sub-skill's meaning changes — not on every file's own version bump.
- Decide which level applies before scaffolding a manifest, and say so explicitly in the dispatcher's `SKILL.md` (see the `coding` package's own "Skill versioning" section for a worked example of the package-level case). Mixing the two — some entries pointing at reference docs, others at sub-skill `SKILL.md` files, in the same manifest — defeats the point of having one flat, predictable shape.

### Field notes
- **`type`**: `"core"` for modules that are always loaded as part of the base skill (the original reference files it shipped with), `"plugin"` for optional modules added later. This distinction matters for anyone reading the manifest to understand what's foundational vs. what's an add-on.
- **`modules`** only lists things that exist as real files right now. Anything not yet built goes in **`planned`** instead, with `"status": "not built"` — this keeps aspirational ideas visibly separate from what's actually active, so a reader (human or model) never mistakes a planned idea for something they can currently rely on.
- **`path`** is relative to the skill's root folder (the folder containing SKILL.md), not to `plugins/`.
- Keep `description` to one line. If a module needs more explanation than that, the explanation belongs in the module's own file, not in the manifest.

## Adding a module
1. Create the file (under `references/` for a doc, or a subfolder under `plugins/` for something more self-contained).
2. Add an entry to `modules` with all required fields.
3. If it existed in `planned`, remove it from there.
4. Bump `package_version` if the addition changes overall skill behavior in a way worth marking as a new version — log the bump in `CHANGELOG.md`.
5. Run `scripts/validate_manifest.py` to confirm the new path resolves.

## Adding a dependency
1. Add the sibling skill's folder name to the `dependencies` array.
2. Say in your own SKILL.md *why* it loads alongside this one and what each skill owns — the manifest records the link, the prose records the division of labor. One without the other is the failure mode: a link nobody can act on, or a dependency with no documented reason.
3. Run `scripts/validate_manifest.py` — it fails if the name doesn't resolve to a real sibling skill folder, or if a skill lists itself.

## Removing or disabling a module
Delete the `modules` entry (or move it to a `disabled` array using the same shape, if it should stay documented but inactive — some skills prefer this over deletion so the history of what was tried isn't lost). Leave the underlying file in place unless it's genuinely obsolete; keeping an unused file around costs nothing, but a manifest entry pointing at a deleted file breaks validation.

## Validating
`scripts/validate_manifest.py` (copied into every scaffolded skill from `assets/templates/`) checks: valid JSON, every module's `path` exists on disk, no duplicate `id`s, and all required fields present on every module. Run it after any manual edit to the manifest.
