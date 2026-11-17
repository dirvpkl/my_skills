# Changelog

## [1.4.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- Per-skill review round: `## Trigger` section removed (cargo-cult per the
  owner ruling; the coding dependency is declared in the manifest).
- Description rewritten as the surfacing contract: ALWAYS-invoke imperative
  + NOT-for rule (lint was FAIL, now OK).

## [1.3.0] - 2026-11-15
- Repo preflight absorbed from base (owner: the preflight lives only
  here): repo check + dirty-files + foreign-work routing + worktree.

## [1.2.0] - 2026-11-15
- Git-everywhere principle written into the skill (owner: version control
  is the default for any project); repo-check example moved in from base
  with a second pair (init detector).


## [1.1.0] - 2026-11-14
- Promoted out of the coding bundle to a top-level skill; Trigger/description made project-agnostic per the owner — version control covers any project work (notes, brainstorms, reverse-engineering, montage, scripts), not only code. Owner approval phrasings carried over unchanged. (Recorded only as an inline comment in SKILL.md until this file was added.)

## [1.0.0] - 2026-09-06
- First version of the version-control conventions (v1, 2026-09-06), originally scoped to the coding bundle.
