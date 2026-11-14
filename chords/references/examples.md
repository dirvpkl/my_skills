# chords — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Bound phrase loads in the same turn

**Good:** the user says «думалки» → the thinking bundle (solution-search + workplanx + spine) loads this turn, then chords steps out of the way.
**Bad:** "I see that's one of your shortcuts — want me to load it?"
Rationale: the binding is a keypress, not a question — resolve and load in the same turn; the target skill's own process governs from there.

## No match says so, never guesses

**Good:** the phrase isn't in the table → "not bound — want me to add it?"
**Bad:** "that phrase is close enough to «пока не зелёное», I'll run the loop skill."
Rationale: resolving an unbound phrase to a guessed target invents routing the user never set — no match is a one-line answer plus an offer to add the binding.

## Explicit form wins on collision

**Good:** the user types `/loop` while a chord phrase collides with it → the explicit command runs, the collision is noted in the row's note.
**Bad:** intercepting the explicit /command because a binding "covers the same words."
Rationale: chords never outranks the explicit path — a colliding bound phrase loses to the explicit form, and the table records the collision rather than removing the explicit route.

## The metaphor name doesn't hijack the domain

**Good:** "какие аккорды в этой песне?" is answered directly as a music question.
**Bad:** routing the music question through `references/bindings.md` as if it were a trigger phrase.
Rationale: the skill name is a metaphor — chords is not a music skill, and its trigger is bound phrases, not the word "chord".
