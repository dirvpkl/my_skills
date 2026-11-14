# testing — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## E2E is offered, never launched unasked

**Good:** "Concept tests pass — want a full end-to-end run against the real services before we call this done?"
**Bad:** spinning up the whole stack "to be thorough" without asking.
Rationale: a heavy e2e run is always proposed and the owner decides — launching one unasked spends real resources on the agent's own initiative.

## Environment failure classified, not blamed on code

**Good:** pytest can't collect because the Docker daemon is down — reported as "verification did not complete — Docker daemon not running."
**Bad:** "tests fail, the change is broken" without ruling out daemon, port, or network first.
Rationale: conflating environment with code failure produces a false blame or a false pass; run the sanity checks first and report the two kinds differently.

## Test through the real path

**Good:** sending the actual bot command to the running service and reading the reply — the same path a user takes.
**Bad:** importing the handler in a REPL, seeing it return 200, and calling the bot verified.
Rationale: the thin client is the user's entry point; exercising internals directly proves nothing about the real path — that's exactly why service separation keeps testing honest.

## Fair comparison: one variable at a time

**Good:** benchmarking old vs new with identical fixtures, thresholds, dedup, and thread counts — only the engine differs.
**Bad:** "the new version is 2x faster" from runs that also changed preprocessing.
Rationale: two changed variables make the difference unattributable — the numbers compare rigs, not approaches; a prototype that can't lose isn't an experiment.
