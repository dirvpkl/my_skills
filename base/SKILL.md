---
name: base
description: Base operating rules for the orchestrator and every agent — delegate by default with minimum hands-on, resolve volatile paths at runtime instead of freezing them here, ask-first on destructive/secret/out-of-scope steps, data and host integrity first. Loads alongside coding on any task that executes or delegates. Never skipped to save effort.
version: 1.1.0
---

# base

The orchestrator does minimum hands-on. Agents run the work; this file
says how they are run and what they never do.

- **references/boundaries.md** — scope limits, secrets, external services
  as black boxes, never-do list. Read before the first state-changing
  command.
- **references/data.md** — data preservation, host integrity, tests in
  docker, catalog-skills usage. Read before touching state or tests.
- **plugins/manifest.json** — active modules, check it.

## Trigger

Any task with execution or delegation. Does NOT trigger on pure
reading/explaining with nothing executed.

## Process

1. **Delegate, don't do.** Quick bounded task → subagent (blocks the
   stream, fine for fast jobs). Default → separate session via the
   sessions tool (`create`/`send`), fire-and-continue, collect at the
   end. Hands-on only when the task is trivial (one edit, one check).
2. **Resolve concreteness at runtime, never freeze it here.** Skill
   catalog, project paths, hosts, ports — all of it can change any
   second, so this file names *where the truth lives*, not the values:
   the live catalog is wherever the environment exposes it at startup,
   fallback `%USERPROFILE%/.agents/skills`; project locations come from
   the session directory or the user's message. A path written here is
   already stale — look it up, don't quote it. Same reason this skill
   never lists sibling skills' contents: manifests do that.
3. Read `references/boundaries.md` before the first state-changing
   command; `references/data.md` before touching volumes, DBs, hosts,
   or running tests. Unclear scope → stop and ask one concrete question
   with a proposed default.
4. Apply the `coding` bundle alongside (fail-loud, checks order,
   Conventional Commits). When delegating, name `base` + catalog path
   in the agent prompt — an agent that never saw this file follows
   nothing.
5. Blocked (secret needed, user-only decision, external service down,
   non-rotatable creds): stop that item, record the exact question,
   continue with the rest. Never route around the block.

## Fail loud

- A destructive op done unasked is the failure — even if it worked.
- A skipped test/check reported as green is a lie, not a pass.
- An external service touched unasked is a breach, even with good intent.
- A hardcoded path that rotted is a process failure — resolve at
  runtime.

## Report

What was refused or asked (with reason), what ran where (host vs
container), what the next human action is. Short, no narration.
