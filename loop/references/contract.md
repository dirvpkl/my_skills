# The loop contract

A loop is five things. If one is missing it isn't a loop, it's a retry loop
with extra steps — and those fail in predictable ways.

1. **Program** — what one iteration is allowed to do. One unit of work.
2. **Artifact slot** — what the iteration produces. Files, a commit, a deployed
   service. Something outside the model's head.
3. **Feedback signal** — the command whose exit code says whether this
   iteration improved anything. External, runnable, cheap.
4. **Run ledger** — append-only record of what each iteration did and observed.
   This is the only thing that crosses iteration boundaries.
5. **Termination** — the rules that end it: condition met, cap reached,
   stagnation, or a human said stop. All four, or at minimum the cap.

## Why fresh context per iteration

The conversation is not durable state — it's the one place that silently
truncates, and when it truncates it takes the reasoning with it. Everything the
next iteration needs has to be on disk: the artifact, the ledger, and whatever
external system holds the truth (git, CI, the service itself).

Corollary: the ledger is written *for a reader with no memory*. "Tried X, got
Y" is useful; "as discussed above" is worthless.

## `loop.md` — the file in the topic folder

One file, written into the `workplanx` topic folder. Config block at the top,
ledger appended below it. `scripts/loop_state.py` reads this file and nothing
else, so it's the single source for the loop's parameters.

```
# Loop: <one-line name>

- condition: <what "done" means in words — for the human reading this>
- verify: <shell command; exit 0 means the condition holds>
- max_iterations: <N, required — a loop without a cap is not runnable>
- no_progress_limit: <consecutive iterations with no new commit before stopping; default 3>
- unit: <what one iteration is allowed to do>

## Ledger
- iter 1 | commit <sha> | verify: fail | <one line: what was tried, what came back>
- iter 2 | commit <sha> | verify: fail | <...>
```

Rules for the file:
- The ledger is **append-only**. Never rewrite or reorder earlier lines — the
  history of a run is evidence, and a loop that cleans up its own log is a loop
  you can't debug.
- The commit sha is the agent's *claim*; `loop_state.py` checks it against git.
  A wrong or reused sha counts as no progress, so faking progress buys nothing.
- `verify:` in a ledger line is the result the agent recorded. The script
  re-runs the command itself when deciding, so a false `pass` here doesn't stop
  the loop — it just makes the ledger a lie you can see.
- Config changes after the first iteration are allowed (the condition turned out
  to be wrong) but must be called out in the report, with the old and new value.
  Silently editing `verify` to make a run succeed is the failure this format
  makes visible.

## The cap is part of the contract, not a safety net

Pick it from the unit of work: a unit that takes a minute and an iteration that
should take a minute or two, `max_iterations: 40` is generous. A unit that
needs a human to review each pass does not belong in an unattended loop. When
the cap is hit, the honest report is "stopped at the cap, last failure was X" —
not a re-run with a bigger number, which is how a 40-iteration failure becomes a
400-iteration failure.
