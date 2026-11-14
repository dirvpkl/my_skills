# Changelog

## [1.11.0] - 2026-11-15
- references/data.md moved to `boundaries` (owner ruling: data/host
  integrity is a boundaries concern). Process item 5 repointed; the
  manifest data module removed; the "use the catalog" section died with
  the move — it duplicated Process item 6.

## [1.10.0] - 2026-11-15
- English-only rule moved here from AGENTS.md (owner: base is always
  loaded, duplication was pointless): everything written for a project is
  English, chat follows the user's language.
- workplanx obligation sharpened in Process item 6: it gates any
  non-trivial task, not a per-task option.

## [1.9.0] - 2026-11-15
- Skill-load failure fallback (owner ruling 2026-11-15): a failed harness
  Skill load is recovered, never a stop — resolve the catalog at runtime
  (environment-exposed, fallback `%USERPROFILE%/.agents/skills`), Read the
  SKILL.md from disk and follow it as loaded content, search other harness
  roots and instructions, ask the user only when the skill exists nowhere.
  Execution outranks the broken loader; interrupting the current flow to
  recover is allowed. Fail-loud line added.
- VERSION file synced (was stale at 1.7.2 while frontmatter said 1.8.0).

## [1.8.0] - 2026-11-14
- Released without a changelog entry at the time; per the 2026-11-14
  handoff it carried the subagent-revival rule in Process item 2. The
  VERSION file also missed this release — both synced retroactively by
  1.9.0.

## [1.7.2] - 2026-11-12
- validate_manifest.py: missing-runtime.toml diagnostic and non-table [skills] guard


## [1.7.1] - 2026-11-12
- validate_manifest.py: dependencies_runtime resolution and module type check


## [1.7.0] - 2026-11-12
- Repo pre-flight (owner ruling 2026-11-12: "always check git in the folder"): `git rev-parse --is-inside-work-tree` + `git status --porcelain` before the first state-changing command in any project folder; another session's uncommitted work is flagged and routed around, never mixed into commits. Parallel/risky repo work happens in a dedicated git worktree by default — the owner never has to ask.

## [1.6.0] - 2026-11-11
- Trigger contract sweep: description rewritten as a use-when / not-for / sibling contract with literal user phrases; rules and body unchanged.
- trigger-log module registered (`references/trigger-log.md`): append-only log of observed trigger misses, folded back into descriptions (researcher/source-log pattern); seeded with the two 2026-11-11 session misses.

## [1.5.0] - 2026-11-07
- skills-reminder tick mandated for long-running/unattended work (watchdog 3.0.0 profile)


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
