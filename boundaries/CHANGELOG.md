# Changelog

## [1.0.1] - 2026-11-14
- Scaffolding (conformance pass): added minimal `plugins/manifest.json` — the sensitive-data memo is a registered module, and future memo extensions land there as new modules instead of new hand-written path references in SKILL.md. VERSION/CHANGELOG already existed; version bumped for the manifest addition.

## [1.0.0] - 2026-11-14
- Initial version. Promoted out of the coding bundle (was `coding/security` 1.0.0) — same rules, universal scope: loads on any task that could touch secrets, logs, chat output, browser data, or files outside the project, not only code.
- New section "Chat & transcript hygiene" built from the owner's sensitive-data memo; memo preserved verbatim in `references/sensitive-data-memo.md`; its golden rule (chat/transcript content is compromised; show the FORM, not the values) is a hard rule.
