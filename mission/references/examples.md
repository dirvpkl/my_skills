# mission — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## A card never shrinks its own condition

**Good:** the card said "auth works end-to-end" — it ships only when a real login round-trip passes.
**Bad:** "the auth module exists — counting the card done."
Rationale: a card whose condition quietly narrows leaves everything below it looking green while the mission is not actually closer to done.

## Stopped run reported as stopped

**Good:** "7 of 10 cards done; cards 8–10 open because X — next human action: decide Y."
**Bad:** presenting the run as "mostly done" with the open cards glossed over.
Rationale: a mission that stops with cards open is a stopped run, not a partial success — the board is the record and says so plainly.

## Evidence over the executor's word

**Good:** the card is marked done only after the orchestrator runs the card's own verify command and sees exit 0.
**Bad:** the card session reports "all tests pass," so the card is marked done without the check having run.
Rationale: done is declared on evidence, never on the card session's word — the executor optimizes for its own report unless the orchestrator verifies.

## Repeated failures re-cut the board

**Good:** three cards failing the same way → stop, back to decompose.md, re-cut the plan.
**Bad:** writing cards 4, 5, 6 in the same shape and hoping they pass this time.
Rationale: three cards failing identically means the decomposition is wrong, not the cards — re-running the same shape burns the budget without moving the goal.
