# Changelog

## [1.17.0] - 2026-11-18
- references/harness.md added (owner question: where do harness-tool
  specifics live — background execs, agent limits, sessions, hooks):
  the current harness's capability catalog, resolved by skills before
  relying on a capability. Process item 3 points at it.

## [1.16.0] - 2026-11-17
- Description trimmed to ~400 chars; the contract is unchanged
  (what it is + ALWAYS invoke + NOT for).

## [1.15.0] - 2026-11-15
- Owner review round 3: the self-referential Trigger section deleted
  (base is already loaded — writing that it should be loaded was
  circular); the git preflight item moved out to `git-workflow` (its
  only home), Process renumbered 5-9 -> 4-8; the Trigger CONCEPT moved
  to the README concepts doc.

## [1.14.0] - 2026-11-15
- Owner review round 2: the delegation-situational note removed (the
  Agent tool docs cover it); the pick signs moved out of the skill text
  into examples (skills are abstract, patterns live in examples);
  Trigger rewritten in plain language; the Report section removed
  (per-skill reports own the format).

## [1.13.0] - 2026-11-15
- Forced project-.md reading (owner ruling, Process item 9): read
  AGENTS.md/README/docs before acting; unsure = user pick; the user-pick
  protocol defined inline.
- Process item 5: unclear/risky/guessable ("hmm", "let me think",
  "what does the user mean") is a user pick, not a guess. Item 1:
  delegation-vs-hands-on is situational — unsure = user pick.
- Item 7 extended: a missing EXTERNAL skill fails safe — report + user
  pick (search/skip/other), never a silent route-around.
- Item 8 widened: English in everything the agent touches, the user
  chat is the only exception. Item 6: chords read alongside base,
  phrases matched by meaning; bundle definitions live in chords.


## [1.12.0] - 2026-11-15
- references/boundaries.md merged into the `boundaries` skill (owner:
  duplicates are forbidden) — base depends on the skill now, the file is
  gone. references/trigger-log.md moved to `workplanx` (trigger misses
  are its domain). Dependencies narrowed to workplanx + boundaries:
  coding and mission dropped from base's manifest.

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
