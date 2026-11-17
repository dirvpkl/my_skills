# watchdog — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## The tick watches, never works

**Good:** the tick sees the worker's tests failing, records WORKING with evidence, and stops.
**Bad:** the tick hops in and edits the failing test file to unblock the worker.
Rationale: one tick watches without doing the watched work — a tick that edits is a broken tick, reported and stopped, not improvised wider.

**Good:** the tick notices the worker drifting off-profile and reports it as evidence.
**Bad:** the tick "helpfully" finishing the worker's step because the deadline is close.
Rationale: the closer the deadline, the stronger the pull — and the tick's entire value is that it did NOT join the work.

## Event-based predicate, not absence

**Good:** "the worker is alive" is proven by a successful round-trip — probe 200, `/start` answered.
**Bad:** "no errors for 5 calm minutes" on a system that drops connections by nature.
Rationale: absence on a noisy channel is unprovable; proof is a positive round-trip — an absence-based predicate is forbidden and gets repredicated.

**Good:** the predicate names the event AND the interval: "probe answers within 30s, checked every 5 min."
**Bad:** "alive if the process exists" — a pid without an answer.
Rationale: existence is not liveness; the predicate must be an event the tick can actually observe, or it reports a corpse as alive.

## Specific brief or silence

**Good:** "you are editing Docker files — the `docker` skill covers exactly this; invoke it before the next step."
**Bad:** "just checking: does any skill fit your current task?"
Rationale: a generic reminder measures as a coin flip — skills-reminder names both sides of the connection, specific or nothing; a silent tick with one ledger line is the fallback.

**Good:** the brief quotes the exact line the worker seems to be violating.
**Bad:** a scolding about tone: "be careful with the skills."
Rationale: a brief that cannot point at the line cannot be followed — specificity is what makes the reminder actionable.

## Replacement proposed, never silent

**Good:** after the hard ping goes unanswered, reporting HUNG with evidence (last message id, last ledger line) and proposing the replacement for the orchestrator's explicit go.
**Bad:** quietly spawning a fresh session and retiring the old row.
Rationale: a replaced session loses its context — the call needs the orchestrator's explicit go, and the old session leaves tracking as DROPPED if it never delivered a verdict.

**Good:** the replacement proposal carries the old session's task id for resumption.
**Bad:** proposing a replacement without the resume handle, so the context just dies.
Rationale: replacement without a resume path is amputation — the handle is what makes the swap survivable.
