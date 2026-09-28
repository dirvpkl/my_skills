---
name: loop
description: Runs a task as repeated autonomous iterations until an external condition holds or a stop rule fires — fresh context per iteration, state on disk instead of in conversation, progress measured by a real command and by git rather than by the agent's own say-so. Covers iterate-until-green (tests, deploy, inference, build), bounded retry with a hard iteration cap, and no-progress detection. Use when the user asks to keep going until X works, to self-verify until clean, or to run unattended for N iterations. Fails loud at the cap.
version: 1.0.0
---

# loop

One iteration does one unit of work, proves something, records it, and stops.
The next iteration starts fresh and reads only what's on disk. That's the whole
mechanism — there is no daemon, no scheduler, no plugin.

- **references/contract.md** — the five ingredients every loop needs, and the
  `loop.md` file shape written into the topic folder.
- **references/stop-signals.md** — the rationality catalogue: what "the agent is
  wasting iterations" actually looks like, and which ones stop the loop early.
- **plugins/manifest.json** — active modules, check it.

## Trigger

- "Keep going until the tests pass / the deploy works / inference responds."
- "Check your own work N times."
- Run unattended for a bounded number of iterations, come back to a result.
- Does NOT trigger on "retry this once" — that's an integration's centralized
  retry (`external-integrations`), not an agent loop. The difference: a retry
  re-sends the same request; a loop re-asks the agent to do the next unit of
  work with what it learned.

## Process

1. Write `loop.md` into the `workplanx` topic folder (shape in
   `references/contract.md`). It holds the condition, the verify command, the
   cap, and the append-only ledger. If there is no topic folder, make one —
   this skill is a `workplanx` dependency and the ledger has to live somewhere
   durable.
2. **Define the condition as a command whose exit code means done.** Not "the
   output looks right" — a command. If you can't write one, that's a
   conversation to have before starting, not a reason to start a loop with a
   soft condition. A loop whose only judge is the agent judging itself is the
   failure mode this skill exists to prevent.
3. Run the verify command **before** the first iteration. If it already passes,
   the loop is pointless — say so and stop. This is the cheapest iteration
   there is.
4. One unit of work per iteration. Not "and then also fix the other thing" —
   that makes the per-iteration signal meaningless.
5. After the unit: run the verify command, append one ledger line, then run
   `scripts/loop_state.py --dir <topic-dir>`. It prints `CONTINUE` or
   `STOP:<reason>` and its exit code is the loop's verdict. **Follow it.** If
   it says stop, the loop stops — you don't get a vote.
6. New iteration: fresh context, read `loop.md` and the ledger, pick the next
   unit. Don't carry reasoning forward in prose; that's what the ledger is for.
7. On `STOP`, report per `references/contract.md` — verdict, iterations used,
   what the condition was, what the last failure was.

## Fail loud

- **The cap is a hard stop, not a suggestion.** Hitting `max_iterations` without
  the condition met is a failure and is reported as one, with the last observed
  failure. Never "close the loop" by relaxing the condition, editing the verify
  command, or reclassifying the run as good enough.
- **Never move the goalposts mid-loop.** If the condition turns out to be
  wrong, that's a finding to report, not a reason to quietly rewrite it. Say:
  "the condition as written is unreachable because X" and stop.
- A run that ends with the condition unmet and no failure recorded is a broken
  ledger, not a successful loop.

## Verifying it's not wasting iterations

`loop_state.py` catches mechanical stagnation (no new commit, cap, condition
met). It cannot catch an agent that's busy but going in circles — that needs
`references/stop-signals.md`, read before starting a long loop. The two most
valuable entries there are *editing the check instead of the thing* and
*writing more code each pass while the failure stays the same*; both burn a
full cap while looking productive.

## When a loop is the wrong tool

- The work can't be verified by a command → there's no loop, there's a
  conversation.
- One iteration would plausibly finish it → just do it.
- The blocker is a missing secret, a decision only the user can make, or an
  environment failure → stop and write the user. `testing` owns the
  environment-vs-code distinction; a loop that retries a broken Docker daemon
  for 40 iterations is a loop that wasted 40 iterations.
- The task needs judgment about *which* thing to do next → that's `mission`,
  which decomposes; a loop on an un-decomposed goal just re-does the same step.

## Report

Verdict and reason (condition met / iteration cap / no-progress / stopped by
rule), iterations used, the verify command's last output, and what the next
human action is. Don't present a capped run as a success, and don't pad the
report with a per-iteration narration.
