# roi — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## A stock answer priced HIGH

**Good:** the cold control's answer contains the same core claim → verdict STOCK, final score 0, nothing else runs.
**Bad:** "this is genuinely useful, I'll price it HIGH" without running the gate.
Rationale: the stock gate runs before ANY scoring — "would any cold LLM have said the same?" is the hard core; skipping it prices noise as value.

**Good:** a finding the owner "obviously wants" still goes through the control first.
**Bad:** pricing HIGH because the owner asked about the topic.
Rationale: enthusiasm is not a control — the gate exists precisely for the findings everyone wants to believe.

## Control runs on the original formulation

**Good:** the verbatim producer prompt goes to the control model as-is.
**Bad:** re-writing the prompt to be more specific before the control run "to give the control a fair chance."
Rationale: a prompt engineered to produce the finding proves nothing — the control must see the finding's original formulation or the gate is theater.

**Good:** the control sees the same system prompt, temperature, and context the producer had.
**Bad:** running the control with a stripped system prompt "to keep it clean".
Rationale: a control that differs from the producer in anything but the claim measures the setup, not the finding.

## Failed control = UNVERIFIED, never guessed

**Good:** control config missing or the control call fails → verdict `UNVERIFIED`, stated loudly.
**Bad:** "the control didn't run, but I'm confident it would have differed — scoring HIGH."
Rationale: no control, no score — a guessed pass is a fake pass, and the loud UNVERIFIED verdict is the fail-loud behavior this skill owes the owner.

**Good:** the failure mode (config missing / HTTP error) is recorded next to the UNVERIFIED verdict.
**Bad:** silently retrying the control until it works and presenting the verdict as clean.
Rationale: the retry itself is a fact about the gate's reliability — hidden retries are the same lie as a guessed pass.

## Append-only annotation

**Good:** the STOCK finding stays in the file with its verdict block appended to the record.
**Bad:** deleting the stock finding from the list so the output looks stronger.
Rationale: the gate annotates, never deletes — the record is the point, and a pruned list is a prettier lie about the same findings.

**Good:** a re-run with a different control model appends a new verdict block; the old one stays.
**Bad:** overwriting the old verdict with the new one "to keep the file clean".
Rationale: verdicts are measurements at a point in time — the history of re-measurement is part of the finding.
