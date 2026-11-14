# process-tiers — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## One concrete question, not a dilemma

**Good:** "This touches formatting on files you didn't ask about — apply autoformat per code-quality, or skip it for this task?"
**Bad:** a five-option menu of formatting policies laid out in chat "so the user can choose".
Rationale: a rule conflict gets one short specific question with a named default; an open-ended dilemma is a wall of text that offloads the decision.

## Tier ambiguity named, not silently downgraded

**Good:** "This edit touches a shared module used by three services — treating it as small-feature tier (mini-design first) instead of routine. OK?"
**Bad:** quietly coding it as a routine fix because the diff itself looks small.
Rationale: blast radius sets the tier, not diff size; guessing down to a lighter tier is exactly the silent-improvisation failure.

## Review runs regardless of who writes the code

**Good:** the user said "work it directly yourself," yet the lint/test agent and fresh-eyes review still run after the non-trivial change, without asking.
**Bad:** "You said work directly, so I skipped the review to keep it simple."
Rationale: the direct-work answer is Axis 1 only — routine checks and review are Axis 2 and always run; skipping them produces a false green.

## Trivial tier never drops the approval gate

**Good:** a "one-line typo fix" that would also touch a compose port stops at the port ask first.
**Bad:** invoking "this is trivial tier" to justify adding `ports: ["8080:8080"]` without asking.
Rationale: tiers scale the ceremony (baseline, fresh-eyes, test coverage) — the ask-first rules (secrets, out-of-project files, docker ports, side effects) never drop.
