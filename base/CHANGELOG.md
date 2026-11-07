# Changelog

## [1.4.0] - 2026-11-07
- runtime.toml convention: machine facts next to the live catalog, always readable, working-context values


## [1.3.0] - 2026-10-31
- Keep-the-host-intact: every Python action via uv venv, never global python/pip; create uv venv when the folder has none


## [1.2.3] - 2026-10-19
- Prefer agents over subagents in the delegation rule


## [1.2.2] - 2026-10-19
- Process list: fix duplicated step number (step 3 appeared twice)


## [1.2.1] - 2026-10-05
- Delegation requires log path and heartbeat, stale log means stalled


## [1.2.0] - 2026-10-04
- Full rewrite: always-loaded orchestrator rules, runtime path resolution, strictest-wins conflicts


## [1.1.0] - 2026-10-04
- Rename safety to base, orchestrator-first with runtime path resolution


All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job (that belongs in a dedicated references/ file — see references/anti-patterns.md in skill-scaffolder for why these should stay separate).

## 1.0.0 — 2026-10-04
- Initial version.
