# fresh-eyes — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## The judge gets artifacts, not the story

**Good:** the judge receives the diff, the checks' output and the topic folder —
and is asked to judge them cold.
**Bad:** the judge receives a paragraph explaining why the change is correct,
then agrees with the paragraph.
Rationale: a clean-context judge is only clean if the author's narration does
not arrive with the artifacts; reasoning is exactly what it must not inherit.

**Good:** the judge gets the same skills the parent had loaded, plus read access
to the `workplanx` topic folder, and cross-checks the work against the records.
**Bad:** the judge is handed a bare diff and asked "does this look fine?" —
it can only judge style, not conformance.
Rationale: judging "as asked" requires the ask; a judge without the records
invents its own standard.

## Triage every finding

**Good:** the judge reports "the retry helper swallows the second attempt" →
the main agent checks the diff, accepts it with a one-line reason, fixes it.
**Bad:** the judge's raw report is pasted to the user verbatim, half of it
wrong about code the judge never saw.
Rationale: an agent can send back nonsense; the author is the filter, not a
relay.

**Good:** a rejected finding is dropped silently after a stated reason.
**Bad:** rejected findings are forwarded anyway "for transparency."
Rationale: a rejected finding is noise; forwarding it makes the user triage the
agent's triage.

## Integrated is not wired

**Good:** the new module exists, is imported by the service that needs it, and
the judge traces a real call from the entry point into it before calling the
work done.
**Bad:** "the module is implemented" — nothing constructs it, nothing calls it,
and the feature is still unreachable.
Rationale: the consumer trace is the cheapest test for the most common
half-done state: code that exists beside the product instead of inside it.
