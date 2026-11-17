# mission — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## A card never shrinks its own condition

**Good:** the card said "auth works end-to-end" — it ships only when a real login round-trip passes.
**Bad:** "the auth module exists — counting the card done."
Rationale: a card whose condition quietly narrows leaves everything below it looking green while the mission is not actually closer to done.

**Good:** the card's verify can't run yet (environment not up) → the card stays open with the blocker named on the board.
**Bad:** swapping in a cheaper check that passes ("the module imports cleanly") to close the card.
Rationale: closing a card with a check it was never given is the same narrowing one step removed — the condition travels with the card, not with whatever check is handy.

## Stopped run reported as stopped

**Good:** "7 of 10 cards done; cards 8–10 open because X — next human action: decide Y."
**Bad:** presenting the run as "mostly done" with the open cards glossed over.
Rationale: a mission that stops with cards open is a stopped run, not a partial success — the board is the record and says so plainly.

**Good:** the owner pauses the mission mid-board → the board records the pause and which cards were mid-flight.
**Bad:** the session just ends, leaving the board looking live.
Rationale: the board is the coordination record across fresh sessions — an unstated pause makes the next session guess at reality.

## Evidence over the executor's word

**Good:** the card is marked done only after the orchestrator runs the card's own verify command and sees exit 0.
**Bad:** the card session reports "all tests pass," so the card is marked done without the check having run.
Rationale: done is declared on evidence, never on the card session's word — the executor optimizes for its own report unless the orchestrator verifies.

**Good:** the verify was stale (it exercised the old endpoint) → the card is re-opened and re-checked against the named condition.
**Bad:** accepting "done" because the session ran *something* green.
Rationale: green output from the wrong check is the same as no output — the check named on the card is the only one that counts.

## Repeated failures re-cut the board

**Good:** three cards failing the same way → stop, back to decompose.md, re-cut the plan.
**Bad:** writing cards 4, 5, 6 in the same shape and hoping they pass this time.
Rationale: three cards failing identically means the decomposition is wrong, not the cards — re-running the same shape burns the budget without moving the goal.

**Good:** ONE card failing three times in three different ways → it gets a `loop`, not a re-cut.
**Bad:** treating every failure as a decomposition failure and shredding the whole board.
Rationale: repeated identical failures say the cut is wrong; varied failures on one card say the card needs its own iteration engine — the diagnoses differ.
