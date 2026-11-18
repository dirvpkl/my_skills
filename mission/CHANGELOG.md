# Changelog

## [1.6.0] - 2026-11-19
- Identity sharpened (owner ruling): mission's MAIN task = the board
  (dispatch, verify, move) + result logging — NOT coding, NOT anything
  else; card sessions build with coding; execution follows the kanban
  service / obsidian graph when the attachments exist. Desc + intro +
  Process step 6 (the outcome line logged the same step).

## [1.5.1] - 2026-11-17
- examples.md: every case now carries >=2 Good/Bad pairs (the collection convention) — one teaching couplet added per single-pair section.

## [1.5.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- `## Trigger` section removed (cargo-cult per the owner ruling); its scope
  lines already live in the description. Description unchanged.

## [1.4.2] - 2026-11-12
- validate_manifest.py: missing-runtime.toml diagnostic and non-table [skills] guard


## [1.4.1] - 2026-11-12
- validate_manifest.py: dependencies_runtime resolution and module type check


## [1.4.0] - 2026-11-11
- Trigger contract sweep: description rewritten as a use-when / not-for / sibling contract with literal user phrases; rules and body unchanged.

## [1.3.0] - 2026-11-08
- directive description: imperative trigger + negative constraint (trigger reliability sweep)


## [1.2.0] - 2026-10-04
- Wire base as mandatory dependency


## [1.1.0] - 2026-10-03
- Session orchestration: one full session per card (session.create/send/messages), subagents banned; conformance review by orchestrator or clean-context session; 2-3 approach tradeoffs in own words; drop unavailable deps


## 1.0.0 — 2026-09-26
New skill: long-running objective decomposed into a board of cards, worked by subagents, judged at the end.
- `references/decompose.md` — the four-part test for a workable card (own condition, fits a fresh context, one outcome, no human mid-card), dependency-then-risk ordering, when the goal is too vague to split, and the special card shapes: spike, migration, cleanup, loop, last mile.
- `references/board.md` — `mission.md` format in the `workplanx` topic folder, card lifecycle across `## Board` / `## Done` / `## Dropped`, per-card fresh-subagent dispatch (card only, never the whole board), supervisor-verifies-done, loop cards, and reporting.
- Deliberately one file, not a folder: the board lives next to `loop.md` in the same topic folder, so there's one source of truth per task.
- Depends on `workplanx` (folder + phase gate), `coding` (`testing`'s environment-vs-code rule), `loop` (the engine for a card that needs repetition) and `fresh-eyes` (conformance on the board before work starts, and on the goal when the board empties).
- A conformance pass on the board *before* starting work is the load-bearing step: a clean-context reviewer catching a bad decomposition while it still costs nothing beats discovering it at card 9.
