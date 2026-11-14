# watchdog — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## The tick watches, never works

**Good:** the tick sees the worker's tests failing, records WORKING with evidence, and stops.
**Bad:** the tick hops in and edits the failing test file to unblock the worker.
Rationale: one tick watches without doing the watched work — a tick that edits is a broken tick, reported and stopped, not improvised wider.

## Event-based predicate, not absence

**Good:** "the worker is alive" is proven by a successful round-trip — probe 200, `/start` answered.
**Bad:** "no errors for 5 calm minutes" on a system that drops connections by nature.
Rationale: absence on a noisy channel is unprovable; proof is a positive round-trip — an absence-based predicate is forbidden and gets repredicated.

## Specific brief or silence

**Good:** "you are editing Docker files — the `docker` skill covers exactly this; invoke it before the next step."
**Bad:** "just checking: does any skill fit your current task?"
Rationale: a generic reminder measures as a coin flip — skills-reminder names both sides of the connection, specific or nothing; a silent tick with one ledger line is the fallback.

## Replacement proposed, never silent

**Good:** after the hard ping goes unanswered, reporting HUNG with evidence (last message id, last ledger line) and proposing the replacement for the orchestrator's explicit go.
**Bad:** quietly spawning a fresh session and retiring the old row.
Rationale: a replaced session loses its context — the call needs the orchestrator's explicit go, and the old session leaves tracking as DROPPED if it never delivered a verdict.
