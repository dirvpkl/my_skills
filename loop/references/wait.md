# External wait — waiting on someone else's state

The default loop does one unit of work per iteration. This mode does no work
per round: each round only checks an external condition — session statuses, a
deploy answering, an external process exiting — after a short pause. The round
is a status check, not a unit of work.

## Predicate over someone else's state

The predicate names someone else's readiness, not your effort. Shape: "all
externals are ready and their verdicts are collected". Examples: "all listed
sessions are idle and each final answer is on record", "the deploy answers
200 on the health endpoint", "the external process exited and its exit code is
logged". Fix it before the first round, same as any predicate — frozen
afterwards, goalpost-moving rules from `stop-signals.md` apply unchanged.

## Round shape: pause briefly, check once, record

1. Sleep short, then run the status check once.
2. Append one ledger line with the observed evidence and the result
   (`pass`/`fail` against the fixed predicate).
3. Run `scripts/loop_state.py` and follow its verdict.

A round never performs the work itself: no re-sending requests (that is a
retry — `external-integrations`), no "one more fix while waiting", no scope
expansion. If the check needs credentials or decisions only a human can make,
that is a stop-and-write-the-user, not a wait.

## Short pauses only — long sleeps are forbidden

Long sleeps get killed by the infrastructure, so they are not a waiting
strategy — they are a way to lose the run silently. Wait with short pauses
plus a re-check every round. Pick the pause from the check's cost: seconds,
not minutes; if one status check is expensive, fewer rounds with a cheap
liveness probe beat rare expensive polls.

## Bounded rounds, fail loud

`max_iterations` is the round cap (required, same field as in
`references/contract.md`). Hitting it with the predicate unmet is a failure:
report "not ready in N rounds" with the last observed status — never extend
the sleep, never raise the cap and re-run, never declare readiness by
absence of news. No news is `fail` with evidence "still not ready", recorded
every round like any other observation.

## What counts as readiness proof

- A session status line showing idle/done plus the collected verdict text —
  "all quiet" without the verdicts is not proof.
- A command check exit 0 (`verify:`) re-run by `loop_state.py` — same rule as
  work loops: the ledger's `pass` decides nothing by itself.
- A criterion check against recorded evidence ("every listed session has a
  final line in the ledger") — the criterion names its evidence and threshold
  up front, same as in `references/contract.md`.
- A `pass` without evidence is a claim either way. Stagnation
  (`no_progress_limit` consecutive rounds with no new evidence) still stops
  the wait — polling an unchanged status forever is the wait-mode version of
  going in circles.

## `loop.md` shape for a wait

Same file as in `references/contract.md`, with the unit fixed as checking:

```
# Loop: <one-line name>

- condition: <their readiness — the predicate, for the human reading this>
- verify: <status command; exit 0 means ready — present for command checks>
- criterion: <fixed rule plus its evidence and threshold — present for criterion checks>
- max_iterations: <N rounds, required>
- no_progress_limit: <consecutive rounds with no new evidence before stopping; default 3>
- unit: check only — short pause, one status check, one ledger line; no work

## Ledger
- iter 1 | evidence <status output ref> | result: fail | <one line: what the check observed>
```
