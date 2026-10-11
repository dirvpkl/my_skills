---
name: watchdog
description: Independent supervision tick over tracked OpenChamber worker sessions — checks each session's status and latest verdict, nudges stalled ones once, reports GREEN/STALLED/BLOCKED. Runs on a schedule without the user or the orchestrator asking. Use when workers run unattended and callbacks do not arrive.
version: 1.0.2
---

# watchdog

One tick supervises tracked worker sessions without human prompting. It runs
as a `loop` external-wait round (see that skill's `wait.md`): the predicate,
check, cap, and ledger live in the loop file named below, and each tick does
exactly one round — check, ledger line, `loop_state.py` verdict — then stops.
It reads only: session status, latest assistant message, and each session's
log tail. It never does the workers' work and never edits project files.

- **references/checks.md** — how a check is performed and how each verdict
  is decided. Guidance only: no paths, no session IDs.
- **state/tracked.md** — the live registry (runtime data, not a reference):
  which sessions are tracked, what each one owes, and its natural cadence.
  Read it every tick; a session not listed here is not checked.
- **plugins/manifest.json** — active modules. Check it instead of assuming.

## Trigger

- A scheduled tick fires (cron), or the user says "check the workers" / "loop".
- Does NOT trigger on new work arriving: a fresh user task is handled by the
  orchestrator, not by this skill. This skill only watches already-running work.

## Process

1. Read `state/tracked.md`. For every listed session: `session.status`,
   then `session.messages` (`lastAssistant`, limit 1). Silence is data only
   against the session's cadence: a session is STALLED only when its log shows
   no new line past its natural cadence — `idle` alone means nothing.
2. Classify each session: GREEN (verdict delivered), WORKING (fresh
   evidence within cadence), STALLED (stale past cadence — nudge once with a
   concrete question, then leave it), BLOCKED (needs a human-only input:
   secret, decision, remote URL — report the exact question, do not retry).
3. Append one tick line per session to the tick log named in `tracked.md`
   (session, classification, evidence). No tick line = the watchdog itself
   is dead.
4. Report: one line per session (GREEN/STALLED/BLOCKED + evidence). Full
   verdicts are quoted, never paraphrased into claims. A tick that finds
   everything GREEN still reports the tick — silence is not a report.

## Fail loud

- A session removed from tracking without a delivered verdict is reported as
  DROPPED, never silently forgotten.
- A nudge that would be destructive, secret-touching, or out of scope is not
  sent — the session is BLOCKED instead, with the exact question.
- The tick never relaxes a worker's predicate or declares its work done.

## Report

Per-session one-liners plus the list of exact human-needed inputs. Short, no
narration.

## Extending this skill

New capability goes into `references/` or `plugins/`, then gets registered
in `plugins/manifest.json` — see `plugins/README.md`.
