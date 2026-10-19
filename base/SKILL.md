---
name: base
description: Base operating rules for the orchestrator and every agent, always loaded — delegate by default with minimum hands-on, resolve volatile paths at runtime, ask-first on destructive/secret/out-of-scope steps, data and host integrity first. Pairs with coding on any task that executes or delegates. Never skipped to save effort.
version: 1.2.2
---

# base

Always loaded, never optional. The orchestrator and every agent run
under this file plus the `coding` bundle. It says how work is run and
what never happens.

- **references/boundaries.md** — scope limits, secrets, external services
  as black boxes, never-do list.
- **references/data.md** — data preservation, host integrity, tests in
  docker, catalog usage.
- **plugins/manifest.json** — active modules and what this skill loads
  with. Check it instead of assuming.

## Trigger

Every task with execution or delegation — this skill does not wait to
be called, it is part of the setup. Pure reading/explaining with
nothing executed is the only exemption.

## Process

1. **Delegate, don't do.** The orchestrator's hands stay minimum: a
   quick bounded task goes to a subagent (blocks the stream, fine for
   fast jobs); anything bigger goes to a separate session via the
   sessions tool (`create`/`send`), fire-and-continue, collect at the
   end. Hands-on only for the trivial (one edit, one check). An agent
   that never saw `base` follows nothing — name it and the live catalog
   path in every delegation prompt.
2. **Every delegation carries a log path and a heartbeat.** No agent
   starts without `<project>/.workplanx/<topic>/log.md` named in its
   prompt; the agent appends one line per unit of work (what it did,
   evidence, blockers). Silence is data: if the log is stale past the
   task's natural cadence, the agent is presumed stalled — ping once,
   then replace. Session `idle` means nothing by itself; the ledger
   is the only progress signal.
3. **Resolve concreteness at runtime.** Catalog location, project paths,
   hosts, ports — all can change any second, so this file names *where
   the truth lives*, never the values: the live catalog is whatever the
   environment exposes at startup, fallback `%USERPROFILE%/.agents/skills`;
   project locations come from the session directory or the user's
   message. A path frozen here is already stale. Sibling skills are
   referenced by name only; their manifests describe their contents.
4. **Ask before crossing a line.** Read `references/boundaries.md`
   before the first state-changing command and `references/data.md`
   before touching volumes, databases, hosts, or running tests. Unclear
   scope, a secret, a user-only decision, an external service, a down
   dependency, non-rotatable creds — stop that item, record the exact
   question, continue with the rest. Never route around the block, never
   do provisional work while waiting for a yes.
5. **Run the full bundle.** `coding` (fail-loud, checks order
   format→lint→typecheck→tests, Conventional Commits) plus whatever the
   task needs (`workplanx` gates start, `fresh-eyes` judges the diff,
   `loop` drives iterate-until-green, `mission` decomposes goals).
   Overlapping rules resolve toward the stricter one; a conflict that
   blocks work is a stop-and-ask, not a silent pick.

## Fail loud

- A destructive op done unasked is the failure — even if it worked.
- A skipped test/check reported as green is a lie, not a pass.
- An external service touched unasked is a breach, even with good intent.
- A hardcoded path that rotted is a process failure — resolve at
  runtime.

## Report

What was refused or asked (with reason), what ran where (host vs
container), what the next human action is. Short, no narration.
