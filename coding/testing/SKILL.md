---
name: testing
description: How to verify a feature actually works after implementing or changing it — beyond just running the default test suite. Covers coverage gaps, the UX-level pass from the real entry point a user would use, respecting service boundaries when testing, regression checks against baseline, fair comparisons, and telling apart an environment failure from a code failure. Use this after any code change, before reporting it as done.
version: 1.2.0
---

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-22: added fair comparisons (one variable at a time). -->
<!-- v1.2 - 2026-09-26: decoupling — UX pass marked as the artifact handed to a `fresh-eyes` quality-mode judge; report section states the review verdict is `fresh-eyes`'s to give, not this file's. No testing rule changed. -->
<!-- Continues prior content that lived under a package-wide v3 marker before the coding package moved to per-skill versioning; see coding/CHANGELOG.md. -->

# testing

## Trigger
After implementing or changing a feature, before reporting it as done. Bundled per the `coding` dispatcher's activation manifest (full set, not a subset) — see that manifest for the dispatch logic; this Trigger line is scope only.

## Base dependency: logging
Whatever's being tested should already have logging wired in per the `logging` skill — that's not optional groundwork, it's assumed to already be there by the time testing starts. If it isn't, that's a gap to flag, not something to route around while testing.

## Coverage
- Every change gets covered by tests. If existing tests don't cover it, write the missing tests yourself; if a proper test isn't feasible in the time/tooling available, write a .sh/.ps1 check script instead and explicitly tell the user coverage is incomplete and why.
- If the task had a plan file (big/architectural per `process-tiers`): cross-check it — every planned requirement maps to a task and a test. Flag gaps, don't imply coverage.
- Regression check: for any change where it's unclear whether a failure is new or pre-existing, use `code-quality`'s baseline-comparison process (`git stash`, re-run, `git stash pop`, compare) rather than guessing from the diff alone. This applies here as much as it does during a refactor — a failing test after a feature change is not automatically "caused by" the change until compared against baseline. `scripts/baseline_diff.sh` automates the stash/re-run/pop/compare cycle.

## Default tests are a floor, not proof it works
- Running the existing test suite (pytest, etc.) is necessary but not sufficient. A green test suite doesn't mean the feature actually works for a real user — the tests in the repo can themselves be wrong, stale, or covering the wrong thing. Don't treat "tests pass" as equivalent to "verified."

## UX pass — look at it like the user would
- After default tests pass, separately walk through the feature from the actual entry point a real user/client would use, not by calling internal functions directly.
- Ask: does this actually feel right, or just technically not-crash? A response that's technically correct but clunky, slow, or wrong-shaped is still a problem.
- This section is also what a `fresh-eyes` quality-mode judge gets handed, alongside the code checklist. Running the pass and judging the result are different jobs: you do the pass, `fresh-eyes` owns the review.

## Report
State plainly which layer was tested: default suite (pass/fail numbers) and UX/end-to-end pass (what was tried, what was observed). If only the default suite was run and the UX pass was skipped, say so explicitly rather than implying full coverage. If any failure was environment-classified rather than code-classified, say which check and why. Independent judging of the result belongs to `fresh-eyes` — don't restate its verdict here, run it or say it didn't run.

## Respect service boundaries when testing
- If the architecture has a thin client talking to a service (e.g. a Telegram bot that's just a frontend to a service's API), test through that real path — send the actual commands/messages the client would send, against the running service — rather than exercising the service's internals directly and calling it done.
- This is exactly why service separation matters (see `code-quality`): a thin client is cheap to test end-to-end; a monolith isn't, and it's tempting to skip this step when everything's tangled together.

## Environment failures vs code failures
- Before reporting any test/lint/verification failure as a problem with the code, rule out that it's actually an environment problem: Docker daemon not running, a port already in use, no network access, a missing dependency that was never about the code at all.
- These two failure kinds get reported differently and never conflated:
  - **Code failure**: the change caused it. Report it as a bug, investigate per `code-quality`'s verification section, fix it.
  - **Environment failure**: verification couldn't run to completion for reasons unrelated to the change. Report this explicitly as "verification did not complete — [specific reason]," not as a pass, not as a code bug, and not silently worked around.
- Never resolve ambiguity here by assuming the code is fine because "it's probably just the environment" — that's a silent fallback (see `code-quality`'s fail-loud section) applied to verification itself. State the ambiguity and, if it can't be resolved, say so rather than reporting either a false pass or a false blame.
- `scripts/classify_failure.sh` runs a handful of quick environment sanity checks (Docker daemon up, port availability, network reachability) — run it first when a check fails and it's unclear which bucket the failure belongs to.

## Fair comparisons — one variable at a time
- An A/B experiment (old vs new approach, benchmark of two engines, prototype against baseline) proves nothing unless both sides share the harness, the data, and every step except the one under test. Different dedup, thresholds, preprocessing, thread counts, or fixtures between runs make the difference unattributable — re-run fair before concluding anything.
- Design the comparison so a negative result is possible and visible: if the new variant ties or loses, report that and don't ship it. A prototype that can't lose isn't an experiment.
- Applies to benchmarks too: same input, same knobs — note every setting that differs, or the numbers compare rigs, not approaches.

