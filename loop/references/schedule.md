# Schedule — the loop's alarm clock, nothing more

A schedule wakes the loop; it never steers it. The schedule knows WHEN to
run. Everything about WHAT and WHY lives in the loop file. A schedule entry
that carries task specifics is a second source of truth — see
`references/contract.md` on why that fails.

## What a schedule entry holds

- The loop file path (the single source: predicate, check, cap, ledger).
- The tick cadence (cron expression or interval).
- The skill + model to run the tick.

Nothing else. No task description, no session IDs baked in (the loop file
already names them), no thresholds, no "also check X while you're at it".
If the entry needs a sentence to explain itself beyond the loop file path,
that sentence belongs in the loop file, not in the schedule.

## What a tick does

Exactly one `loop` round (see `references/wait.md` for waits, `references/contract.md`
for work loops): run the check once, append one ledger line, follow the
`loop_state.py` verdict. A tick that performs the work itself, retries
something, expands scope, or edits the loop contract is not a tick — it is
unplanned work wearing a cron mask.

## Supervision is automatic, not optional

Any `loop` in external-wait mode over someone else's sessions MUST name its
supervision in the loop file: which watchdog (skill name + version) watches
it, where that watchdog's tick log lives, and the cadence. The watchdog
skill depends on `loop` (see its manifest); `loop` does NOT depend back —
the link is procedural (named in the loop file), not a manifest cycle.
A wait loop with no named supervision is an unrunnable contract:
`loop_state.py` cannot see other sessions, so without a watchdog nobody
ever evaluates the wait.

## Forbidden

- A schedule without a loop file (a cron that "just checks something").
- Task specifics inside the schedule entry (duplicated predicate, pasted
  session IDs, inline thresholds).
- Two schedules ticking the same loop file (double ticks = double ledger
  lines = fake stagnation signal).
- Deleting the schedule while the loop is still open (the loop keeps
  running with nobody watching), or keeping the schedule after the loop
  STOPs (spam — stopping the ticks is part of finishing).
