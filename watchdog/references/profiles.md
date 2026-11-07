# profiles.md — the tick profile catalogue

A profile is the whole behavior contract of a tick: read budget (what it may
look at), send budget (what it may deliver, how often, to whom), cadence,
state, and an explicit "never" list. The tick's only job is applying its
profile to the evidence; a need outside the budget is a new profile or a
stop-and-ask, never an improvise.

## Rules for every profile

- **Read budget is exhaustive.** Anything not listed may not be read, even
  when it sits right there. A profile that reads everything is not
  watching — it is doing the work.
- **Send budget is exhaustive.** What may be delivered, how often, to whom.
  Re-sending an unanswered message is a budget violation, not persistence.
- **State.** Where the tick's own ledger lines go (the tick log named in
  the profile or in `tracked.md`).
- **Stop.** When the watch is over, the schedule task is deleted in the
  same pass — a tick that outlives its predicate spams the session forever.
- **Determinism by default.** A profile that needs model judgment says so
  explicitly. Everything else is a deterministic check.

## sessions

Worker-session supervision (OpenChamber and equivalent session hosts).

- Reads: `state/tracked.md`, `session.messages` (`lastAssistant`), the
  session's ledger tail. `session.status` is never read.
- Sends: nudges (one concrete status question), hard pings, re-anchors
  (the session's `owes` line), per-session verdict lines to the user.
- Cadence: per the session's natural cadence recorded in `tracked.md`.
- Never: edits project files, relaxes a worker's predicate, declares work
  done, touches secrets.
- Mechanics: `references/checks.md`.

## skills-reminder

The matcher tick: argues named skills into a working agent's context.
Model judgment: yes.

- Reads: `runtime.toml` next to the live skill catalog (`[hotplug]` plus
  sections relevant to the current work), the freshest
  `.workplanx/<topic>/log.md` tail (else the live session context), the
  `description` frontmatter line of every installed skill.
- Sends: at most one brief per tick, at most 3 lines, specific imperative
  naming the skill and the current activity it is for; once per match;
  never a generic "check whether a skill fits" reminder.
- Cadence: 30 minutes (user-set).
- Never: invokes skills, performs the matched work, edits anything except
  `[hotplug]` in `runtime.toml` and its own log lines.
- Stop: the watched work ends or the user retires the tick — schedule task
  deleted in the same pass.

## Adding a profile

Write it here (read budget, send budget, cadence, state, never list),
register it in `plugins/manifest.json`, and name its ledger file. If it
needs model judgment, mark that in the entry — the catalogue is the only
place budgets may grow.
