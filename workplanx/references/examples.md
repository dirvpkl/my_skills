# workplanx — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Topic folder before the first search

**Good:** `.workplanx/11-14-parser-refactor/` created at task start, plan.md drafted, every step logged there from step one.
**Bad:** agent searches, codes, and keeps progress notes in the chat window.
Rationale: chat is the conversation; the folder is the record the next session and the gate actually read.

## Owner's voice lands in the folder

**Good:** owner's «потом сделай» appended to log.md verbatim, quoted, dated, same day it arrived.
**Bad:** log entry paraphrases it as "owner agreed to defer" — the exact words live only in the chat transcript.
Rationale: a ruling that lives only in chat is lost to the next session; verbatim is the difference between the owner's words and the agent's summary of them.

## user-pick gates the build

**Good:** decision.md written with its `counter:` line, pick requested, nothing built until the pick lands on the same line after `user-pick:`.
**Bad:** agent reads plan.md as approval and starts implementing because "the scope is obvious."
Rationale: proceeding past plan.md approves nothing — the only gate the build phase checks is the pick.

## counter: written before the pick

**Good:** `counter:` — "the reverse-index approach fails on write-heavy repos" — written while the recommendation is still unowned, before the pick is requested.
**Bad:** `counter:` line filled in after the owner already picked, as a rubber stamp.
Rationale: a recommendation that can't survive its own counter isn't ready — and a post-pick counter is theater, not the duel-lite check.

## Harvest waits for the bump

**Good:** afterword's `harvest:` block lists patches (rule + target skill), the pass ends, patches are applied only after the owner's bump.
**Bad:** agent edits another skill's SKILL.md mid-pass because the rule "obviously belongs there."
Rationale: the pass proposes, the owner applies — self-applied harvest is how a collection drifts out of consistency.
