# Mode: conformance

Hand this file's contents to the judge agent verbatim, along with the
`workplanx` topic folder. The judge did not do the work and was not in the
planning conversation, so it can only compare artifacts to artifacts.

## What to check

1. **Requirement coverage**: every requirement in `plan.md` — does something in the diff actually satisfy it? Name the ones with nothing behind them.
2. **Decision fidelity**: `decision.md` names a pick and a ladder level. Does the wiring sit at that level, or was something hand-rolled below it?
3. **Scope creep**: changes in the diff that no requirement asked for. Not automatically wrong — flag it so the main agent can decide whether it was silent scope growth.
4. **Parked work**: anything the plan listed as out-of-scope that got implemented anyway.
5. **Verification honesty**: does the plan name a verify step per task, and does evidence in the folder or the run show it actually ran? A task marked done with no command output behind it is a finding.
6. **Non-goals**: the plan's non-goals — did any of them get touched?

## What NOT to do
- Don't fix anything, don't re-plan, don't decide whether the plan was a good plan — that's the user's call, not the judge's.
- Don't judge code quality here. If something is badly written but correctly matches the plan, that's not a conformance finding (that's `quality` mode).
- Don't talk to the user directly — report back to the main agent.

## Output shape
For each finding: the requirement or plan line it concerns, the artifact evidence (file/line in the diff, or absence of evidence), and a one-line verdict. Explicitly state which requirements you could not judge and why (missing artifact, ambiguous wording) — a silent skip is worse than an admitted gap.
