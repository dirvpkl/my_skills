# Changelog

## [2.5.1] - 2026-10-19
- Trigger mechanics: prefer terminal, schedule as the second option


## [2.5.0] - 2026-10-16
- schedule.md: schedule as pure cron mechanics, mandatory named supervision for waits


## [2.4.2] - 2026-10-05
- Missing ledger line equals dead agent


## [2.4.1] - 2026-10-05
- Record active standing rules: merge, redeploy, push to own origin, orphan delete, one quota spend


## [2.4.0] - 2026-10-05
- Standing approvals: repeated yes becomes standing rule, stop re-asking


## [2.3.0] - 2026-10-04
- Full rewrite: silence rule integrated into process, scope note in trigger, base wired


## [2.2.1] - 2026-10-04
- Dialog rule scope: conversational sessions only, subagent reports are delivery


## [2.2.0] - 2026-10-03
- Dialog rule: no user answer until STOP except destructive/harmful; short-sleep polling note


## [2.1.0] - 2026-10-03
- External-wait mode: references/wait.md (no-work rounds, short pauses, bounded cap) plus two-mode note in SKILL.md


## [2.0.0] - 2026-10-03
- Abstract core: fixed predicate with command-or-criterion check, evidence ledger, hardened stop rules; tests and deploys are examples, not the definition
- Why: v1 targeted tests/deploys (a verify command whose exit code was the only judge), which excluded legitimate loops — converged search, stabilized answer, exhausted moves — where no command can decide. The loop's essence is iterating until a predicate holds, not until a command exits 0.
- `SKILL.md` — predicate plus check fixed before the first iteration; check is `verify` (exit 0 decides) and/or `criterion` (frozen rule judged against recorded evidence); "no command = no loop" replaced with "no decidable predicate = no loop, just a conversation".
- `references/contract.md` — five ingredients redefined (program, predicate, check, ledger, termination); command-vs-criterion section; `loop.md` shape gains `criterion:` and `evidence`/`result:` ledger fields (legacy `commit`/`verify:` lines still parse); check frozen after the first iteration (was: editable with a callout).
- `references/stop-signals.md` — generalized off tests: criterion edits (threshold lowered, evidence redefined) count as goalpost-moving; same-observation-different-wording and volume-without-signal replace test-only wording.
- `scripts/loop_state.py` — requires `condition` and at least one of `verify`/`criterion` (`STOP:no-contract` otherwise); command path re-runs the command as before; criterion path reads the recorded `result:` (nothing else can decide it); stagnation generalized from "no new commit" to "no new evidence", with commit shas still verified against git.


## 1.0.0 — 2026-09-26
New skill: bounded autonomous iteration with a mechanical verdict.
- `references/contract.md` — the five ingredients (program, artifact slot, feedback signal, run ledger, termination), why context resets per iteration, and the `loop.md` shape: config block plus append-only ledger, living in the `workplanx` topic folder. No second folder, no second source of truth.
- `references/stop-signals.md` — the semantic layer a script can't check: goalpost-moving (editing the check instead of the thing), activity without progress, solving a different problem, and an explicit list of what is *not* a stop signal.
- `scripts/loop_state.py` — prints exactly one verdict (CONTINUE / STOP:condition-met / STOP:iteration-cap / STOP:no-progress / STOP:no-ledger / STOP:no-contract) and exits 0 or 1. Progress is derived from git and re-run by the verify command, never from the agent's claim: a reused or nonexistent sha counts as no progress, and a false `pass:` in the ledger doesn't stop anything.
- Depends on `workplanx` (the folder), `coding` (the `testing` environment-vs-code rule) and `fresh-eyes` (judging the result). The phase gate stays `workplanx`'s job — this skill never re-litigates whether the task was allowed to start.
