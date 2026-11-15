# Changelog

## [1.3.0] - 2026-11-15
- Per-skill review round: the ## Trigger section removed (cargo-cult
  restatement of the description); the description rewritten as the
  surfacing contract (ALWAYS-invoke imperative + NOT-for, intent only —
  no keyword lists); the data.md pointer unwedged from the Chat &
  transcript hygiene header into its own section; System boundaries
  bullet duplicated by Assigned scope removed; examples.md added
  (two pairs per case).

## [1.2.0] - 2026-11-15
- Merged in from base (owner: no duplicates — one source per rule): assigned
  scope (with the read-only-diagnosis nuance), external services as black
  boxes, the never-do list. The secrets principles were already covered by
  the permission rule and the .env section; base now depends on this skill
  instead of carrying its own boundaries file.

## [1.1.0] - 2026-11-15
- Data preservation moved in from base (owner: data/host integrity is a
  boundaries concern, not base): volumes/DB backup before migrate, host
  integrity (uv venv, never global python/pip), tests in docker. The
  "use the catalog" section was dropped — it duplicated base Process
  item 6.

## [1.0.1] - 2026-11-14
- Scaffolding (conformance pass): added minimal `plugins/manifest.json` — the sensitive-data memo is a registered module, and future memo extensions land there as new modules instead of new hand-written path references in SKILL.md. VERSION/CHANGELOG already existed; version bumped for the manifest addition.

## [1.0.0] - 2026-11-14
- Initial version. Promoted out of the coding bundle (was `coding/security` 1.0.0) — same rules, universal scope: loads on any task that could touch secrets, logs, chat output, browser data, or files outside the project, not only code.
- New section "Chat & transcript hygiene" built from the owner's sensitive-data memo; memo preserved verbatim in `references/sensitive-data-memo.md`; its golden rule (chat/transcript content is compromised; show the FORM, not the values) is a hard rule.
