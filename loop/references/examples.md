# loop — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## The cap is a hard stop

**Good:** iteration 40 ends with the predicate unmet → verdict "capped run, failed," with the last check's output attached.
**Bad:** hitting the cap and closing the loop with "close enough — the suite is green-ish."
Rationale: a capped run is a failure reported as one; reclassifying it as good-enough is the goalpost failure in its most common disguise.

**Good:** `max_iterations: 8` written into `loop.md` before iteration 1, and the opening report names it.
**Bad:** "we'll iterate until it looks right" — no cap anywhere on disk.
Rationale: the cap is one of the five ingredients precisely so the loop can fail loud; an uncapped loop cannot stop honestly, it just fades.

## Predicate frozen — the fix is reported, not applied

**Good:** "the predicate as written is unreachable because the endpoint doesn't exist — stopping for a decision."
**Bad:** quietly editing `verify` mid-loop so the check starts passing.
Rationale: predicate, verify, and criterion are frozen after the first iteration; discovering they're wrong is a finding to report, not an edit to make.

**Good:** the owner re-scopes the task mid-loop → the loop stops ("the predicate no longer matches the task") and a NEW loop starts with the new predicate.
**Bad:** amending the running loop's predicate to track the changed requirement.
Rationale: frozen means frozen mid-run — a changed task is a new loop, otherwise the ledger's evidence no longer maps to the predicate it claims to serve.

## Editing the check instead of the thing

**Good:** the loop keeps failing because the code has a real bug — iterations fix the code.
**Bad:** iterations "fix" it by loosening the assertion or running fewer tests until green.
Rationale: that burns the entire cap while looking productive — it's the stop-signal `loop_state.py` cannot catch, which is why stop-signals.md is read before a long loop.

**Good:** the verify command itself turns out flaky (network timeout one run in three) → the loop stops: a broken check is an environment failure.
**Bad:** rerunning the flaky check until a lucky pass counts as predicate met.
Rationale: a lucky pass is not evidence — environment-vs-code is `testing`'s distinction, and a loop must not launder flakiness into a verdict.

## Every iteration appends a ledger line

**Good:** the command check fails → the failure and its output land in the ledger, `loop_state.py` says CONTINUE, next iteration starts fresh.
**Bad:** skipping the ledger line because "nothing changed since last round."
Rationale: a missing line is indistinguishable from a dead agent and the orchestrator treats it as one — the append happens every iteration without exception.

**Good:** the unit produced nothing observable → the line says exactly that, and the stagnation counter ticks.
**Bad:** padding the ledger with narration so the iteration looks busy.
Rationale: stagnation detection eats honest empty lines; padded lines hide it — the ledger's signal is deltas, not volume.
