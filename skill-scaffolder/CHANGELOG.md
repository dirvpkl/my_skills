# Changelog

## [1.5.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- `## Trigger` section removed (cargo-cult per the owner ruling); its live
  lines (extend-existing, skill-creator caveat) already live in the
  description and Process.
- references/examples.md added (the skill had none).

## [1.4.0] - 2026-11-15
- Lean manifest convention (owner ruling: the manifest must not duplicate
  what the project already contains): {skill, dependencies, planned} only —
  modules, package_version and dependencies_runtime are gone. Validator
  shipping removed (repo-wide scripts/validate.py is the one validator);
  scaffold.py stops copying it; manifest-format.md rewritten.

## [1.3.2] - 2026-11-12
- validator template: missing-runtime.toml diagnostic and non-table [skills] guard


## [1.3.1] - 2026-11-12
- manifest contract: dependencies_runtime field in validator, templates, and manifest-format reference


## [1.3.0] - 2026-11-11
- Trigger contract sweep: description rewritten as a use-when / not-for / sibling contract with literal user phrases; rules and body unchanged.

## [1.2.0] - 2026-11-08
- directive description: imperative trigger + negative constraint (trigger reliability sweep)


## [1.1.0] - 2026-10-31
- references/anti-patterns (1.0.0 -> 1.1.0): new anti-pattern 7 — no session data or personal details inside a skill; write the lesson, not the story; session-proven cases stay in the planning folder's log.


## [1.0.1] - 2026-10-19
- Complete the standard layout: VERSION, CHANGELOG, plugins/manifest.json and the runnable validate_manifest.py; fix template name references


## 1.0.0 — 2026-09-29
- Initial version: scaffolds a new skill's standard layout (`SKILL.md`, `VERSION`, `CHANGELOG.md`, `references/`, `plugins/`, `scripts/`, `assets/`) and restructures loose or flat skills into it.

All notable changes to this skill are logged here — changes to the scaffolding method, the target layout, or the templates. Not a log of skills it has produced, and not runtime data (it produces none).
