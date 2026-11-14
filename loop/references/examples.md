# loop — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## The cap is a hard stop

**Good:** iteration 40 ends with the predicate unmet → verdict "capped run, failed," with the last check's output attached.
**Bad:** hitting the cap and closing the loop with "close enough — the suite is green-ish."
Rationale: a capped run is a failure reported as one; reclassifying it as good-enough is the goalpost failure in its most common disguise.

## Predicate frozen — the fix is reported, not applied

**Good:** "the predicate as written is unreachable because the endpoint doesn't exist — stopping for a decision."
**Bad:** quietly editing `verify` mid-loop so the check starts passing.
Rationale: predicate, verify, and criterion are frozen after the first iteration; discovering they're wrong is a finding to report, not an edit to make.

## Editing the check instead of the thing

**Good:** the loop keeps failing because the code has a real bug — iterations fix the code.
**Bad:** iterations "fix" it by loosening the assertion or running fewer tests until green.
Rationale: that burns the entire cap while looking productive — it's the stop-signal `loop_state.py` cannot catch, which is why stop-signals.md is read before a long loop.

## Every iteration appends a ledger line

**Good:** the command check fails → the failure and its output land in the ledger, `loop_state.py` says CONTINUE, next iteration starts fresh.
**Bad:** skipping the ledger line because "nothing changed since last round."
Rationale: a missing line is indistinguishable from a dead agent and the orchestrator treats it as one — the append happens every iteration without exception.
