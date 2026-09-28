# Changelog

## 1.0.0 — 2026-09-26
New skill: bounded autonomous iteration with a mechanical verdict.
- `references/contract.md` — the five ingredients (program, artifact slot, feedback signal, run ledger, termination), why context resets per iteration, and the `loop.md` shape: config block plus append-only ledger, living in the `workplanx` topic folder. No second folder, no second source of truth.
- `references/stop-signals.md` — the semantic layer a script can't check: goalpost-moving (editing the check instead of the thing), activity without progress, solving a different problem, and an explicit list of what is *not* a stop signal.
- `scripts/loop_state.py` — prints exactly one verdict (CONTINUE / STOP:condition-met / STOP:iteration-cap / STOP:no-progress / STOP:no-ledger / STOP:no-contract) and exits 0 or 1. Progress is derived from git and re-run by the verify command, never from the agent's claim: a reused or nonexistent sha counts as no progress, and a false `pass:` in the ledger doesn't stop anything.
- Depends on `workplanx` (the folder), `coding` (the `testing` environment-vs-code rule) and `fresh-eyes` (judging the result). The phase gate stays `workplanx`'s job — this skill never re-litigates whether the task was allowed to start.
