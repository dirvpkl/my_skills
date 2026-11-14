# handoff form

One file per handover. Sections in this order; keep each section tight —
the file is a work order, not a story.

```markdown
# handoff — <one-line task name>
- from: <agent/session> | to: <agent/session or "any fresh agent">
- date: <YYYY-MM-DD HH:MM> | topic: <workplanx topic path, if any>

## Goal
What this work IS, in two sentences. The fresh agent should be able to
restate the goal after reading only this.

## Current state
What exists right now: done vs in-flight vs untouched. Facts, with paths.

## Decisions & verdicts
Owner words VERBATIM (quoted, dated) — picks, rulings, corrections. The
fresh agent inherits positions, not summaries of positions.

## Blockers & gotchas
What will bite: known traps, dead ends already walked, flaky deps,
permissions still pending.

## Commands & paths
Exact runnable commands and absolute paths — build, test, deploy, logs.
No placeholders; anything not runnable is marked as such.

## Files & artifacts
Everything touched or needed, with absolute paths and one line on role.

## Expected next result
What the fresh agent should produce first, and how its owner will judge
it (checks to run, gate to pass).

## What NOT to do
Explicit fence: mass/prod/destructive/unsafe/no-proxy/credentials actions
always stop and ask; anything task-specific the owner fenced.
```

## Verification checklist (run before delivering)

- [ ] A zero-context agent can restate the Goal from section 1 alone.
- [ ] Every path is absolute and exists (or is marked "to be created").
- [ ] Every decision is quoted verbatim, with a date.
- [ ] No term is used that the file does not define or reference.
- [ ] The fence section names the deny classes, not just "be careful".
- [ ] A `#slot` travels as a slot — nothing invented to close it.
