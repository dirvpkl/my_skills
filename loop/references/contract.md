# The loop contract

A loop is five things. If one is missing it isn't a loop, it's open-ended work
with extra steps — and those fail in predictable ways.

1. **Program** — what one iteration is allowed to do. One unit of work.
2. **Predicate** — what "done" means, in one fixed sentence. Examples: "the
   suite passes", "the deploy answers", "the search converged", "the answer
   stabilized", "no meaningful moves remain".
3. **Check** — how the predicate is decided. A `verify` command (exit 0 means
   the predicate holds), a `criterion` (a fixed rule applied to recorded
   evidence), or both for the same predicate. Frozen before the first
   iteration. Tests and deploys are instances of command checks, not the
   definition of checking.
4. **Run ledger** — append-only record of what each iteration did and observed.
   This is the only thing that crosses iteration boundaries.
5. **Termination** — the rules that end it: predicate met, cap reached,
   stagnation, continuation senseless, or a human said stop. The cap is always
   present.

## Command checks vs criterion checks

- **Command check (`verify:`).** External, runnable, cheap. Exit 0 decides;
  the ledger's word does not. `loop_state.py` re-runs it when deciding, so a
  false `pass` in the ledger is a visible lie, not a stop.
- **Criterion check (`criterion:`).** A rule fixed up front, judged against
  evidence recorded that iteration. Examples: "two consecutive reformulations
  return the same top results", "the answer is byte-identical across two
  passes", "every listed move was tried and each observation is on record".
  The rule must name its evidence (what counts as an observation) and its
  threshold (how many repetitions count as done). No command can decide these
  — the agent judges, but only against the frozen rule and only with evidence
  on record.
- **Both.** Allowed when they check the same predicate (the command is the
  floor, the criterion is the ceiling). They never check different
  predicates — that is two loops sharing one ledger.

## Why fresh context per iteration

The conversation is not durable state — it's the one place that silently
truncates, and when it truncates it takes the reasoning with it. Everything the
next iteration needs has to be on disk: the artifact, the ledger, and whatever
external system holds the truth (git, CI, the service itself, the recorded
observations).

Corollary: the ledger is written *for a reader with no memory*. "Tried X, got
Y" is useful; "as discussed above" is worthless.

## `loop.md` — the file in the topic folder

One file, written into the `workplanx` topic folder. Config block at the top,
ledger appended below it. `scripts/loop_state.py` reads this file and nothing
else, so it's the single source for the loop's parameters.

```
# Loop: <one-line name>

- condition: <what "done" means in words — the predicate, for the human reading this>
- verify: <shell command; exit 0 means the predicate holds — present for command checks>
- criterion: <fixed rule plus its evidence and threshold — present for criterion checks>
- max_iterations: <N, required — a loop without a cap is not runnable>
- no_progress_limit: <consecutive iterations with no new evidence before stopping; default 3>
- unit: <what one iteration is allowed to do>

## Ledger
- iter 1 | evidence <ref> | result: fail | <one line: what was tried, what came back>
- iter 2 | evidence <ref> | result: fail | <...>
```

`evidence` is whatever the check observes: a commit sha for code loops
(checked against git — a reused or nonexistent sha counts as no progress), a
file or artifact path, a query id, an observation hash. `result:` is `pass` or
`fail` against the check. The legacy shape (`commit <sha> | verify:
<pass|fail>`) still parses — it is the same fields under older names.

Rules for the file:
- The ledger is **append-only**. Never rewrite or reorder earlier lines — the
  history of a run is evidence, and a loop that cleans up its own log is a loop
  you can't debug.
- At least one of `verify` / `criterion` is required. A loop with neither has
  no decidable check and is not runnable — `loop_state.py` stops it with
  `STOP:no-contract`.
- The check is **frozen** after the first iteration. `condition`, `verify`,
  and `criterion` do not change mid-run. If any of them turns out to be wrong,
  stop and report the old and new value as a finding; silently editing the
  check to make a run succeed is the failure this format makes visible.
- Every ledger line carries evidence and a result. A `pass` without evidence
  is a claim, not an observation. For command checks the script re-runs the
  command, so a false `pass` doesn't stop anything — it just makes the ledger
  a lie you can see. For criterion checks the script reads the recorded
  result, which is exactly why the criterion is frozen and the evidence is
  mandatory.

## The cap is part of the contract, not a safety net

Pick it from the unit of work: a unit that takes a minute and a check that
takes a minute or two, `max_iterations: 40` is generous. A unit that
needs a human to review each pass does not belong in an unattended loop. When
the cap is hit, the honest report is "stopped at the cap, last observation was
X" — not a re-run with a bigger number, which is how a 40-iteration failure
becomes a 400-iteration failure.
