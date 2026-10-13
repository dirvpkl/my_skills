# checks.md — how a supervision check is performed

Per session, in this order:

1. `session.status` — `idle` vs `busy`. Records activity, proves nothing
   about progress. Never classify on this alone. `busy` means mid-step:
   do not conclude, come back next tick.
2. `session.messages` with `lastAssistant: true`, limit 1 — then ALWAYS
   read `id`, `createdAt`, `completedAt`. Rules:
   - `completedAt: null` = still writing; the text is partial, never quote
     it as a verdict.
   - `createdAt` older than the task send time = stale; fetch deeper
     (`limit 5`, role `all`) before concluding anything.
   - A non-assistant role in the result = fetch deeper, the view slipped.
   - One message is never the whole story: progress notes are not
     verdicts; only a message that answers the tasked question with
     evidence counts as a verdict.
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

Message discipline (messages arrive with lag — live logs are always
fresher than words):

- Fetch with `lastAssistant` and read `createdAt`: a verdict older than
  the live red log lines is STALE until re-verified, never GREEN.
- Cross-verify every green verdict against the live tail by timestamps
  before reporting it upward; on mismatch, hard-ping with the fresh
  evidence attached instead of relaying the verdict.
- A nudge is a plain status question, never a new task, never destructive,
  never secret-touching.
- A re-anchor is a status question, not a new task: resend the session's
  `owes` line only. Skip re-anchor for GREEN/BLOCKED sessions and within
  15 minutes after a nudge.
