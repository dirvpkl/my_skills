# Changelog

## [1.4.3] - 2026-11-18
- desc: questions ABOUT the domain ("what are the access protocols for
  production data?") route here — the skill is the knowledge home for its
  own rules, not only the touch-guard (exam miss, same pattern as
  git-workflow 1.4.1's procedure questions).

## [1.4.2] - 2026-11-17
- System boundaries: concrete host-app names (owner's personal setup) generalized to classes — media players, browsers, proxy clients; the personalization left the tracked file (owner ruling 2026-11-17).
- examples.md: "Host apps are the user's personal space" case added (2 pairs).

## [1.4.1] - 2026-11-17
- Chat hygiene: the checklist bullet that duplicated the pre-show check and pointed at the deleted memo file ("memo's checklist, section 7") removed — the surviving bullet (form-not-values, leak classes, revocability) is the single checklist.

## [1.4.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- Description updated to match the new body classes (the surfacing contract).
- Log-redaction rule moved to `logging` (owner ruling 2026-11-17): chat
  hygiene stays here; logs and library loggers are logging's domain.
- Never-do list reduced to classes; the command spellings (`rm -rf`,
  `docker compose down -v`, `volume prune`, `git reset --hard`) moved to
  references/examples.md.
- New classes from the analogue research: credential lifecycle +
  pre-commit secret scan, workspace vs home credential stores (env vars
  are the normal config channel), untrusted content is data, egress as a
  boundary.
- references/sensitive-data-memo.md removed: its golden rule, leak
  protocol and checklist live in SKILL.md; concrete recipes (curl filter,
  .env check, docker restart) moved to examples. Recoverable from git.

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
