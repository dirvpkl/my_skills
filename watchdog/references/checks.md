# checks.md — how a supervision check is performed

Per session, in this order:

1. `session.status` — `idle` vs `busy`. Records activity, proves nothing
   about progress. Never classify on this alone.
2. `session.messages` with `lastAssistant: true`, limit 1 — the latest
   verdict or progress note. Compare its timestamp against the session's
   cadence from `tracked.md`.
3. The session's log tail (project `.workplanx/<topic>/log.md`, last ~10
   lines) — the only progress signal. A fresh ledger line within cadence
   means WORKING even when `status` is `idle`. Inside long units the bar is
   the heartbeat: no line for 15+ minutes while tasked = STALLED, even
   mid-unit. A quiet session with a live heartbeat is WORKING, however long
   the unit runs.

Classification:

- GREEN — a final verdict was delivered (commit/push/redeploy confirmed or
  honest FAIL with evidence).
- WORKING — fresh ledger evidence within cadence.
- STALLED — ledger stale past cadence. Nudge once with one concrete
  question, then leave it until next tick.
- HUNG — `idle` + same last message + no ledger lines for 2+ ticks after
  the nudge went unanswered. Hard-ping once, then presume hung and escalate
  per the ladder in SKILL.md. A quiet session with a long but live task is
  NOT hung — hung requires the nudge to have been ignored.
- BLOCKED — the session names a human-only input (secret, decision, URL).
  Report the exact question verbatim; never retry or route around it.

A nudge is a plain status question, never a new task, never destructive,
never secret-touching.
