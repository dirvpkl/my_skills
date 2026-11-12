---
name: watchdog
description: Universal supervision tick — watches something without doing its work, one loop wait-round per tick, behavior set by a profile (what it may read, what it may send, cadence). Built-in profiles: sessions (worker-session supervision — GREEN/WORKING/STALLED/BLOCKED, nudges, escalation ladder), skills-reminder (the 30-minute matcher that argues named skills into a working agent — "you are doing X, skill Y is exactly for this"), and collection-audit (the stocktaking that walks topic folders, the skills tree, and git history, then proposes one patch set: add / fix drift / retire dead). ALWAYS invoke this skill to set up any recurring supervision tick, skill reminder, or collection audit, and when the user asks to check on workers or sessions ("проверь воркеров", "что там с сессиями", "check the workers"); do not hand-roll scheduled nudges.
version: 3.3.2
---

# watchdog

One tick watches; it never does the watched work. The tick runs as a `loop`
external-wait round (see that skill's `wait.md`): the predicate, check, cap,
and ledger live in the loop file, and each tick does exactly one round —
check, ledger line, `loop_state.py` verdict — then stops.

What a tick reads and sends is decided by its **profile**, never improvised.
A profile is a named contract in `references/profiles.md`: read budget (what
it may look at), send budget (what it may deliver, how often), cadence,
state, and an explicit "never" list. A tick that steps outside its budget is
a broken tick — report it and stop, do not improvise a bigger one. The old
"cheap and dumb" guarantee survives as a profile property, not a skill
property: the sessions profile stays deterministic byte-compare;
skills-reminder is the only profile allowed model judgment, and it says so
in the catalogue.

- **references/profiles.md** — the profile catalogue: the contract rule and
  the built-in profiles.
- **references/checks.md** — sessions-profile check mechanics: how a check
  is performed and how each verdict is decided. Guidance only: no paths, no
  session IDs.
- **state/tracked.md** — the sessions profile's live registry (runtime
  data, not a reference): which sessions are tracked, what each one owes,
  and its natural cadence. Read every tick; a session not listed here is
  not checked.
- **plugins/manifest.json** — active modules. Check it instead of assuming.

## Trigger

- A tick fires — from a terminal (preferred) or a schedule — or the user
  says "check the workers" / "watch the skills" / "set up the reminder".
- Does NOT trigger on new work arriving: a fresh user task is handled by
  the orchestrator, not by this skill. This skill only watches
  already-running work.

## Profiles

### sessions — worker-session supervision

1. Read `state/tracked.md`. For every listed session: `session.messages`
   (`lastAssistant`, limit 1), then the session's ledger tail, exactly per
   `references/checks.md`. `session.status` is NEVER fetched — per
   `references/checks.md` it proves nothing and must not appear in evidence.
   Silence is data only against the session's cadence: a session is STALLED
   only when its ledger shows no new line past its natural cadence OR its
   `(last_msg_id, ledger_tail)` is byte-identical to the previous tick for
   the configured consecutive ticks. Every delegation prompt carries a
   heartbeat rule: one ledger line per unit of work AND at least one line
   every 15 minutes inside long units; a worker that hits a wall reports
   BLOCKED immediately with the exact missing input instead of sitting
   silent.
2. Classify each session: GREEN (verdict delivered — the session leaves
   tracking in the same tick), WORKING (fresh evidence within cadence),
   STALLED (stale past cadence — nudge once with a concrete question, then
   leave it), HUNG (idle + same last message + no ledger lines for 2+ ticks
   after a nudge went unanswered — escalation ladder below), BLOCKED (needs
   a human-only input: secret, decision, remote URL — report the exact
   question, do not retry).
3. Append one tick line per session to the tick log named in `tracked.md`
   (session, classification, evidence). No tick line = the watchdog itself
   is dead.
4. Re-anchor WORKING sessions against drift: when the tick log shows no
   re-anchor sent to a WORKING session for 60+ minutes, send that session
   its one-line task restatement — the session's `owes` line from
   `state/tracked.md`, nothing else. Never a new task, never destructive,
   never secret-touching; the restatement forces a drifted agent to re-read
   its instructions. Record every re-anchor in the tick log.
5. Report: one line per session (GREEN/STALLED/BLOCKED + evidence). Full
   verdicts are quoted, never paraphrased into claims. A tick that finds
   everything GREEN still reports the tick — silence is not a report.

Terse mode: when the user signals exhaustion (tired, "can't read", one-word
replies), drop everything except verdicts and the exact inputs needed from
them — one short line per item, no background, no options lecture. A pending
question is repeated at most every third tick, not every tick. If nothing is
needed from the user, say exactly that in one line.

#### Escalation ladder (stalled → hung → replaced)

1. Nudge once: one concrete status question, nothing else. Nudges are HARD
   by default: demand a one-line status plus one ledger line, and an
   explicit continue ("answer and keep working"). A mid-work ping never
   breaks anything — it lands as the next message the worker reads and does
   not restart, kill, or redirect the task — so ping freely.
2. If the next tick still shows silence, hard-ping once: "answer in one
   line or you are presumed hung" — still nothing destructive, still no new
   task.
3. If silence persists past the hard ping, presume HUNG and report it with
   the evidence (last message id, last ledger line). Replacement (a fresh
   session with the full task context + log path, old row retired) is
   proposed, never done silently — a replaced session loses its context, so
   the call needs the orchestrator's explicit go.

### skills-reminder — the matcher tick

Watches a working agent and argues concrete skills into its context. The
goal is fresh eyes, not nagging: the agent does not see the connection
between its current work and the catalog on its own (user-confirmed failure
mode), so the tick names both sides of the connection. This profile uses
model judgment — it is the only one allowed to.

1. Establish the evidence picture (read budget, in order):
   - `runtime.toml` next to the live skill catalog: `[hotplug] skills` plus
     any section relevant to the work at hand (instance addresses, ports);
   - the active `.workplanx/<topic>/` tail — the topic with the freshest
     `log.md` — when one exists;
   - no active topic: the live session's recent context — what the user and
     the agent are actually doing right now. A missing `log.md` is not a
     stop condition; the tick builds its own picture.
   - catalog descriptions: the `description` frontmatter line of every
     installed skill, one line each.
2. Match. For each candidate: is the current work exactly what this skill's
   description says it is for? Ambiguous connections are dropped, not
   stretched.
3. Send at most one brief, at most 3 lines, argumentative and imperative:
   name the skill, name the current activity, say why this skill is for it
   ("you are editing Docker files — the `docker` skill covers exactly this;
   invoke it before the next step"). A generic reminder ("check whether a
   skill fits") is forbidden — it measures as a coin flip; specific or
   nothing.
4. Silent tick when nothing matches: one ledger line, no message.
5. The tick owns `[hotplug]` in `runtime.toml`: when a match repeats or the
   evidence names a skill family, add it there. Never the worker — a worker
   asked to maintain the list is one more thing to forget.
6. A brief is sent once per match. No answer is data: record it in the tick
   log and move on — re-sending turns the reminder into noise the parent
   correctly ignores.
7. Cadence: 30 minutes (user-set). When the watched work ends or the user
   retires the tick, the schedule task is deleted in the same pass.

## Fail loud

- A tick that exceeds its profile's read or send budget is a broken tick:
  report and stop, never improvise.
- The tick never does the watched work. sessions: never edits project
  files, never relaxes a worker's predicate, never declares work done.
  skills-reminder: never invokes skills, never performs the matched work,
  never edits anything except `[hotplug]` and its own log lines.
- A session removed from tracking without a delivered verdict is reported
  as DROPPED, never silently forgotten.
- A nudge or brief that would be destructive, secret-touching, or out of
  scope is not sent — the session is BLOCKED instead, with the exact
  question.
- Predicates are event-based, never absence-based: "5 calm minutes" on a
  system that drops connections by nature is an unprovable predicate and is
  forbidden — proof is a successful round-trip (`/start` answered, probe
  200), not an empty tail. An agent demanding repeated absence-proofs is
  stopped and repredicated instead of funded for another round.
- When the loop STOPs (condition met, cap honestly reported, or the user
  retires supervision), the schedule task that sends the ticks is deleted
  in the same pass — if the ticks came from a terminal, they simply stop
  there. A supervision loop that outlives its predicate spams the session
  forever. Stopping the ticks is part of finishing, not a separate chore.

## Extending this skill

New capability goes into `references/` or `plugins/`, then gets registered
in `plugins/manifest.json`. A new watch target is a new profile: write it in
`references/profiles.md` (read budget, send budget, cadence, state, never
list), register it, give it a ledger file. If the profile needs model
judgment, say so explicitly in the catalogue — the default assumption is a
deterministic check.
