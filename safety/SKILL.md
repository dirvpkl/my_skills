---
name: safety
description: Agent operating rules — ask before anything destructive, secret-touching, or out-of-scope; data preservation and host integrity come first; tests run in docker containers, never on the host. Loads alongside coding on any task that touches repos, containers, volumes, or external services. Never skips itself to save effort.
version: 1.0.0
---

# safety

How agents work without losing data or breaking the host. Goal priority:
**don't lose data, keep the host intact** — everything else is ask-and-fix
with the user, never silent action.

- **references/boundaries.md** — scope limits: assigned projects only,
  external services are black boxes, secrets/creds handling, what is
  never visible and never touched.
- **references/data.md** — data preservation (volumes, DBs, backups before
  migrate), host integrity, tests-in-docker rule, catalog-skills usage.
- **plugins/manifest.json** — active modules, check it.

## Trigger

Any task touching repos, containers, volumes, databases, tunnels, host
config, or an external service — or delegating such a task to a subagent.
Does NOT trigger on pure reading/explaining with no execution.

## Process

1. Read `references/boundaries.md` before the first state-changing command.
   If the task's scope is unclear, stop and ask — one concrete question
   with a proposed default.
2. Read `references/data.md` before touching volumes, databases, or the
   host, and before running tests.
3. Apply the `coding` bundle alongside (fail-loud, checks order,
   Conventional Commits). Skill rules override habits on conflict.
4. When delegating: paste the boundaries + data rules into the subagent
   prompt verbatim-ish and name `my_skills` as mandatory. A subagent that
   never saw this file follows nothing.
5. Blocked (secret needed, user-only decision, external service down,
   non-rotatable creds involved): stop that item, record the exact
   question, keep going with the rest. Never route around the block.

## Fail loud

- A destructive op done unasked is the failure — even if it worked.
- A skipped test/check reported as green is a lie, not a pass.
- An external service touched unasked is a breach, even with good intent.

## Report

What was refused or asked (with reason), what ran where (host vs
container), what the next human action is. Short, no narration.
