---
name: loop
description: Runs a task as repeated autonomous iterations until a fixed predicate holds or a stop rule fires — fresh context per iteration, state on disk instead of in conversation, progress from ledger evidence. The predicate check is a command and/or a pre-fixed criterion (tests and deploys are examples, not the core). Covers iterate-until-met, bounded retry with a hard cap, and stagnation detection. Use when the user asks to keep going until X holds, to converge a search, or to run unattended for N iterations. Fails loud at the cap.
version: 2.0.0
---

# loop

One iteration does one unit of work, checks it against a fixed predicate,
records evidence, and stops. The next iteration starts fresh and reads only
what is on disk. That's the whole mechanism — there is no daemon, no
scheduler, no plugin.

- **references/contract.md** — the five ingredients every loop needs (program,
  predicate, check, ledger, termination), command vs criterion checks, and the
  `loop.md` file shape written into the topic folder.
- **references/stop-signals.md** — the rationality catalogue: what "the agent is
  wasting iterations" actually looks like, and which ones stop the loop early.
- **plugins/manifest.json** — active modules, check it.

## Trigger

- "Keep going until X holds" — the tests pass, the deploy answers, the search
  converged, the answer stabilized, the meaningful moves are exhausted.
- "Check your own work N times."
- Run unattended for a bounded number of iterations, come back to a result.
- Does NOT trigger on "retry this once" — that's an integration's centralized
  retry (`external-integrations`), not an agent loop. The difference: a retry
  re-sends the same request; a loop re-asks the agent to do the next unit of
  work with what it learned.

## Process

1. Write `loop.md` into the `workplanx` topic folder (shape in
   `references/contract.md`). It holds the predicate, the check, the cap, and
   the append-only ledger. If there is no topic folder, make one —
   this skill is a `workplanx` dependency and the ledger has to live somewhere
   durable.
2. **Fix the predicate and its check before the first iteration.** The predicate
   is one sentence stating what "done" means. The check is how that sentence is
   decided: a `verify` command (exit 0 means the predicate holds), a
   `criterion` (a fixed rule judged against recorded evidence), or both for the
   same predicate. Tests, deploys, and builds are examples of command checks;
   convergence ("two reformulations return nothing new"), stabilization, and
   exhaustion ("no meaningful moves left") are examples of criterion checks. If
   neither a command nor a fixed criterion can be written, there is no loop —
   there is a conversation to have before starting.
3. Evaluate the check **before** the first iteration. If the predicate already
   holds, the loop is pointless — say so and stop. This is the cheapest
   iteration there is.
4. One unit of work per iteration. Not "and then also fix the other thing" —
   that makes the per-iteration signal meaningless.
5. After the unit: evaluate the check, append one ledger line carrying the
   evidence and the result, then run `scripts/loop_state.py --dir <topic-dir>`.
   It prints `CONTINUE` or `STOP:<reason>` and its exit code is the loop's
   verdict. **Follow it.** If it says stop, the loop stops — you don't get a
   vote. For command checks the script re-runs the command itself, so a false
   `pass` in the ledger buys nothing; for criterion checks the script reads the
   recorded result, which is why the criterion must be fixed up front and every
   claim must carry evidence.
6. New iteration: fresh context, read `loop.md` and the ledger, pick the next
   unit. Don't carry reasoning forward in prose; that's what the ledger is for.
7. On `STOP`, report per `references/contract.md` — verdict, iterations used,
   what the predicate was, what the last check observed.

## Fail loud

- **The cap is a hard stop, not a suggestion.** Hitting `max_iterations` with
  the predicate unmet is a failure and is reported as one, with the last
  observed check output. Never "close the loop" by relaxing the predicate,
  editing the check, loosening the criterion, or reclassifying the run as good
  enough.
- **Never move the goalposts mid-loop.** Predicate, `verify`, and `criterion`
  are frozen after the first iteration. If any of them turns out to be wrong,
  that's a finding to report, not a reason to quietly rewrite it. Say:
  "the predicate as written is unreachable because X" and stop.
- A run that ends with the predicate unmet and no failure recorded is a broken
  ledger, not a successful loop.

## Verifying it's not wasting iterations

`loop_state.py` catches what is mechanical: predicate met, cap reached,
stagnation (no new evidence). It cannot catch an agent that's busy but going
in circles — that needs `references/stop-signals.md`, read before starting a
long loop. The two most valuable entries there are *editing the check instead
of the thing* and *adding volume while the observation stays the same*; both
burn a full cap while looking productive.

## When a loop is the wrong tool

- No decidable predicate can be fixed up front → there's no loop, there's a
  conversation.
- One iteration would plausibly finish it → just do it.
- The blocker is a missing secret, a decision only the user can make, or an
  environment failure → stop and write the user. `testing` owns the
  environment-vs-code distinction; a loop that retries a broken Docker daemon
  for 40 iterations is a loop that wasted 40 iterations.
- The task needs judgment about *which* thing to do next → that's `mission`,
  which decomposes; a loop on an un-decomposed goal just re-does the same step.

## Report

Verdict and reason (predicate met / iteration cap / stagnation / stopped by
rule), iterations used, the check's last output or evidence, and what the next
human action is. Don't present a capped run as a success, and don't pad the
report with a per-iteration narration.
