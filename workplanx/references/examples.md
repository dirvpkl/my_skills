# workplanx — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Topic folder before the first search

**Good:** `.workplanx/11-14-parser-refactor/` created at task start, plan.md drafted, every step logged there from step one.
**Bad:** agent searches, codes, and keeps progress notes in the chat window.
Rationale: chat is the conversation; the folder is the record the next session and the gate actually read.

**Good:** even a "quick question" task that will touch code opens the folder first.
**Bad:** "this is quick, I'll log it after."
Rationale: the folder is cheap to open and expensive to reconstruct — after-the-fact logs are fiction written from memory.

## Owner's voice lands in the folder

**Good:** owner's «потом сделай» appended to log.md verbatim, quoted, dated, same day it arrived.
**Bad:** log entry paraphrases it as "owner agreed to defer" — the exact words live only in the chat transcript.
Rationale: a ruling that lives only in chat is lost to the next session; verbatim is the difference between the owner's words and the agent's summary of them.

**Good:** the append keeps the whole sentence, not just the "actionable part".
**Bad:** trimming the message to the task it names.
Rationale: the non-actionable part carries tone and scope — the next agent reads the whole sentence to know how far the ruling reaches.

## user-pick gates the build

**Good:** decision.md written with its `counter:` line, pick requested, nothing built until the pick lands on the same line after `user-pick:`.
**Bad:** agent reads plan.md as approval and starts implementing because "the scope is obvious."
Rationale: proceeding past plan.md approves nothing — the only gate the build phase checks is the pick.

**Good:** the gate runs even when the pick "obviously" matches the recommendation.
**Bad:** skipping plan_gate.py because the pick was unanimous.
Rationale: the gate checks the folder's shape, not the agent's confidence — unanimity is exactly when the ritual gets skipped and the record rots.

## counter: written before the pick

**Good:** `counter:` — "the reverse-index approach fails on write-heavy repos" — written while the recommendation is still unowned, before the pick is requested.
**Bad:** `counter:` line filled in after the owner already picked, as a rubber stamp.
Rationale: a recommendation that can't survive its own counter isn't ready — and a post-pick counter is theater, not the duel-lite check.

**Good:** a strong counter revises the recommendation before the pick is requested.
**Bad:** a counter the recommendation obviously beats, chosen to look thorough.
Rationale: a strawman counter is the duel-lite failure — the check exists to break weak recommendations, not to decorate them.

## Harvest waits for the bump

**Good:** afterword's `harvest:` block lists patches (rule + target skill), the pass ends, patches are applied only after the owner's bump.
**Bad:** agent edits another skill's SKILL.md mid-pass because the rule "obviously belongs there."
Rationale: the pass proposes, the owner applies — self-applied harvest is how a collection drifts out of consistency.

**Good:** the harvest entry names the exact file and line the patch would touch.
**Bad:** "should add something about timing to some skill."
Rationale: a patch proposal without a target is a wish — the bump executes it only when it is concrete.

## Delegation carries a log path

**Good:** `Session for the parser refactor: append to <project>/.workplanx/11-14-parser/log.md, one line per unit of work.`
**Bad:** "Go fix the parser, report back when done."
Rationale: the log path is the only progress signal — silence past the natural cadence means stalled, and without a path there is no signal.

**Good:** the delegated agent appends even when blocked: "blocked: no credentials — pinged owner."
**Bad:** silence, because "nothing to report yet".
Rationale: silence is indistinguishable from death; a blocked line is a signal, silence is nothing.

## The owner's voice sinks verbatim

**Good:** owner's message carries a ruling → piped verbatim into the workplanx sink (`log_owner_message.py` / inbox) the same turn.
**Bad:** "I'll remember that" — a ruling that lives only in the chat transcript is lost to the next session.
Rationale: the folder is the memory; the agent's recall is not.

**Good:** the owner's casual aside («кстати потом докрути») lands in the inbox the same turn.
**Bad:** treating asides as chat noise because they do not name a task.
Rationale: asides are where parked ideas live — the sink exists so nothing said once is lost.
