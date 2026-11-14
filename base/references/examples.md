# base — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Resolve paths at runtime

**Good:** catalog location read from what the environment exposes at startup, fallback `%USERPROFILE%/.agents/skills`; local facts checked in `runtime.toml`.
**Bad:** `<machine-path>\my_skills\...` pasted from last month's session and applied without a check.
Rationale: a path frozen in the plan is already stale — runtime truth is wherever the environment says it is today.

## Repo check before the first write

**Good:** `git rev-parse --is-inside-work-tree` + `git status --porcelain` first; another session's dirty files flagged and routed around.
**Bad:** straight to `git add -A && git commit` on a checkout holding someone else's uncommitted work.
Rationale: uncommitted foreign work is never mixed into your commit — routing around it is the point of the check.

## Ask-first is per item, not whole task

**Good:** the out-of-scope item stopped, exact question recorded in the log, the rest of the batch continues.
**Bad:** the whole task blocked pending the answer — or the item done provisionally "to keep momentum."
Rationale: one unclear item does not authorize provisional work or a silent route-around; it becomes a recorded question while the rest moves.

## Fail loud on skipped checks

**Good:** "typecheck green, 2 tests skipped — not green, here's why."
**Bad:** "All done!" with the two skipped tests unmentioned.
Rationale: a skipped check reported green is a lie, not a pass.

## Run the bundle, not just the code

**Good:** code task → `coding` bundle loads (quality, testing, logging), checks run format→lint→typecheck→tests. **Bad:** a "quick fix" that edits and reports done, checks skipped.
Rationale: undispatched skills don't exist for the reader — the bundle is the standard, not an option.

## A failed skill load is recovered

**Good:** Skill invocation fails → resolve the catalog at runtime, Read the SKILL.md from disk, follow it as loaded content; ask only if it exists nowhere. **Bad:** "skill unavailable" and the task quietly dies.
Rationale: execution outranks the broken loader — a manual load counts as loaded.

## Write English into the repo

**Good:** mid-Russian chat, the fix lands in tracked files — English everywhere, even comments. **Bad:** a Russian sentence slips into a tracked file outside the allowed zones.
Rationale: the collection is public-facing and portable; the chat's language stops at chat.

## External service stays a black box

**Good:** the bug looks like the tunnel → diagnose up to the boundary, report evidence, stop. **Bad:** ssh into the VPS "just to check" — unasked.
Rationale: credentials there may be non-rotatable; a "fix" can lock the user out.

## Mode recognition — read the chat before choosing the stack

**Good:** owner pastes another agent's spec + "чудо" as a queue message → process the queue, load the stack the spec implies, no re-asking what was already answered.
**Bad:** answering the previous reply's open question first, or "what do you want me to do with this?" when the spec already says it.
Rationale: queue messages arrive without reply chains — the newest item supersedes.

**Good:** «побрейнштормим» → think-first stack (solution-search + workplanx + spine), zero code written.
**Bad:** jumping to implementation because the idea sounded concrete.
Rationale: think-first requests route to the think stack; code waits for the user-pick.

**Good:** «на сегодня» → afterword + fresh-eyes + morning extract, all wired, no re-negotiation.
**Bad:** "what should I do before you go?" when the chord defines the close-out.
Rationale: end-of-night rituals are bindings — run them.

**Good:** owner mourns a lost idea («мне так грустно, что из головы вылетело») → presence first, hold the `#slot`.
**Bad:** rebuilding the idea for them or opening a task list mid-comfort.
Rationale: comfort register is not a task register; the slot keeps fragments safe until they re-derive it.

**Good:** «много букв» → skeleton answer in chat, full state sinks to the topic folder the same turn.
**Bad:** shrinking the answer AND the record together.
Rationale: terse ≠ lossy — the folder remembers what the chat drops.
