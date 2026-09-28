# Changelog

All notable changes to this skill are logged here. This tracks changes to the *skill itself* (structure, behavior, modules) — not research findings (those go only in the report given to the user) and not newly-discovered research channels (those go in `references/source-log.md`).

## 1.3.0 — 2026-09-26
- `dependencies: ["solution-search"]` added to the manifest. The link was previously only prose in SKILL.md — a hand-maintained list in the core file, which is exactly what the manifest exists to replace. No research rule changed.
- Flagged, not fixed: this skill's manifest uses `skill_version` while `manifest-format.md` mandates `package_version`. Renaming a field other tooling may read isn't a drive-by change — needs its own pass.

## 1.2.0 — 2026-09-22
- Handoff to solution-search (brainstorm): pre-code decisions route out with verbs; researcher surfaces findings, never picks stacks.

## 1.1.0 — 2026-09-22
- `patterns` (1.0.0 → 1.1.0): abstraction chains — climb topic → topic class → who else solves it (≥2 hops) before the first literal query, search each hop, log which hop each finding came from. Placeholders-only, no product names.

## 1.0.0 — 2026-09-06
- Restructured from three loose files (`researcher.md`, `researcher-patterns.md`, `researcher-sources.md`) into a standard skill layout: `SKILL.md` + `references/` + `plugins/` + `scripts/`.
- Added `plugins/manifest.json` as an explicit discovery mechanism, so new modules are registered in one place instead of requiring edits to `SKILL.md` every time.
- Added `references/source-log.md`: a dedicated staging log for newly-discovered *research channels*, split out from `SKILL.md`. Previously this lived as a single ambiguous line in the core file ("mention a good source as a bonus note at the end") which conflated three different things — skill changes, research findings, and new channels. Now each has exactly one place to live.
- Added `scripts/validate_manifest.py` to catch manifest/file mismatches.
- Added `VERSION` and this changelog.
- Translated all reference material to English (source files were already in English; only the core skill file's structure/wording was tightened).
- Reserved (not yet built) module ideas moved into `plugins/manifest.json`'s `planned` list instead of prose in `SKILL.md`.
