# Changelog

## 1.0.0 — 2026-09-26
New skill: long-running objective decomposed into a board of cards, worked by subagents, judged at the end.
- `references/decompose.md` — the four-part test for a workable card (own condition, fits a fresh context, one outcome, no human mid-card), dependency-then-risk ordering, when the goal is too vague to split, and the special card shapes: spike, migration, cleanup, loop, last mile.
- `references/board.md` — `mission.md` format in the `workplanx` topic folder, card lifecycle across `## Board` / `## Done` / `## Dropped`, per-card fresh-subagent dispatch (card only, never the whole board), supervisor-verifies-done, loop cards, and reporting.
- Deliberately one file, not a folder: the board lives next to `loop.md` in the same topic folder, so there's one source of truth per task.
- Depends on `workplanx` (folder + phase gate), `coding` (`testing`'s environment-vs-code rule), `loop` (the engine for a card that needs repetition) and `fresh-eyes` (conformance on the board before work starts, and on the goal when the board empties).
- A conformance pass on the board *before* starting work is the load-bearing step: a clean-context reviewer catching a bad decomposition while it still costs nothing beats discovering it at card 9.
