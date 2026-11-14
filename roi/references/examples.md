# roi — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## A stock answer priced HIGH

**Good:** the cold control's answer contains the same core claim → verdict STOCK, final score 0, nothing else runs.
**Bad:** "this is genuinely useful, I'll price it HIGH" without running the gate.
Rationale: the stock gate runs before ANY scoring — "would any cold LLM have said the same?" is the hard core; skipping it prices noise as value.

## Control runs on the original formulation

**Good:** the verbatim producer prompt goes to the control model as-is.
**Bad:** re-writing the prompt to be more specific before the control run "to give the control a fair chance."
Rationale: a prompt engineered to produce the finding proves nothing — the control must see the finding's original formulation or the gate is theater.

## Failed control = UNVERIFIED, never guessed

**Good:** control config missing or the control call fails → verdict `UNVERIFIED`, stated loudly.
**Bad:** "the control didn't run, but I'm confident it would have differed — scoring HIGH."
Rationale: no control, no score — a guessed pass is a fake pass, and the loud UNVERIFIED verdict is the fail-loud behavior this skill owes the owner.

## Append-only annotation

**Good:** the STOCK finding stays in the file with its verdict block appended to the record.
**Bad:** deleting the stock finding from the list so the output looks stronger.
Rationale: the gate annotates, never deletes — the record is the point, and a pruned list is a prettier lie about the same findings.
