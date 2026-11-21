---
name: base
description: Base operating rules for the orchestrator and every agent, always loaded — delegate by default, resolve volatile paths at runtime, ask first on destructive/secret/out-of-scope steps, protect data and the host. Pairs with coding on any task that executes or delegates; pure reading with nothing executed is the only exemption. Never skipped — a routed skill loads on top of base, never instead of it.
version: 1.21.0
---

# base

Always loaded, never optional. The orchestrator and every agent run
under this file plus the `coding` bundle. It says how work is run and
what never happens.

- **plugins/manifest.json** — what loads alongside (dependencies).
  Check it instead of assuming.

## Process

1. **Delegate, don't do.** The orchestrator's hands stay minimum.
   Prefer agents over subagents: the default is a separate agent — a
   session via the sessions tool (`create`/`send`), fire-and-continue,
   collect at the end; a subagent is only for a quick bounded ask.
   Hands-on only for the trivial (one edit, one check). An agent that
   never saw `base` follows nothing — name it and the live catalog path
   in every delegation prompt.
2. **Every delegation carries a log path and a heartbeat.** No agent
   starts without `<project>/.workplanx/<topic>/log.md` named in its
   prompt; the agent appends one line per unit of work (what it did,
   evidence, blockers). Silence is data: if the log is stale past the
   task's natural cadence, the agent is presumed stalled — ping once,
   then replace. Session `idle` means nothing by itself; the ledger
   is the only progress signal. A failed or stalled subagent is
   RESUMED from its task id with context intact before being replaced;
   if it cannot be revived, stop and ask the owner — delegated work is
   never silently dropped. workplanx owner-message logging is AGENT
   hygiene, not machinery (owner ruling 2026-11-14: no per-message hook):
   after an owner message that carries a decision, ruling or task, pipe it
   verbatim through `workplanx/scripts/log_owner_message.py` (stdin) or
   append to `<project>/.workplanx/_inbox/<date>.md` (or
   `$WORKPLANX_TOPIC/log.md` when the session pins a topic) — the inbox
   is a first-class source for recap and handoff; read it before claiming
   what a session did or decided.
3. **Resolve concreteness at runtime.** Catalog location, project paths,
   hosts, ports — all can change any second, so this file names *where
   the truth lives*, never the values: the live catalog is whatever the
   environment exposes at startup, fallback `%USERPROFILE%/.agents/skills`;
   project locations come from the session directory or the user's
   message. A path frozen here is already stale. Sibling skills are
   referenced by name only; their manifests describe their contents.
   Local facts — ports, hosts, instance addresses, model IDs, working-context
   tokens — live in the consuming skill's own `runtime.toml` beside its
   SKILL.md (gitignored; tracked shape in the skill's
   `runtime.example.toml`). Reading it is always allowed: its values are declared working context for this
   machine/context, not secrets. Ask the user only when the needed key is
   missing. The harness folder (`harness/<harness-name>.md`) carries the
   owner-told nuances — local limits, quotas, retry behavior, schedules —
   the things the tools alone do not reveal: agents know their tools, they
   do not know the local specifics. Read it before relying on a capability,
   and when the owner explains another nuance, it lands there the same turn.
4. **Ask before crossing a line.** Load `boundaries` before the first
   state-changing command; its `references/data.md` comes before touching
   volumes, databases, hosts, or running tests. Unclear
   scope, a secret, a user-only decision, an external service, a down
   dependency, non-rotatable creds — stop that item, record the exact
   question, continue with the rest. Unclear or risky items are a user
   pick, not a guess (the concrete signs live in references/examples.md). Never route around the block, never
   do provisional work while waiting for a yes.
5. **Run the full bundle — chords read alongside base.** chords is the
   shorthand layer: the user's phrases are /commands, read alongside
   base from session start, matched by MEANING — never as a literal
   string regex. Bundles (skill stacks fired by one phrase) are defined
   in chords bindings, not here: a task matching a bundle loads the
   whole bundle, not a cherry-pick. `coding` (fail-loud, checks order
   format→lint→typecheck→tests, Conventional Commits) plus whatever the
   task needs (`workplanx` gates any non-trivial task, `fresh-eyes` judges the diff,
   `loop` drives iterate-until-green, `mission` decomposes goals).
   Skills shipping `references/examples.md`: read that file beside the
   SKILL.md — the good/bad pairs are binding context for HOW the skill
   applies, not decoration. Skills are RE-READ FROM DISK every time they
   matter — never answer a skill question from memory or assume last
   week's content: the catalog changes under you, and a stale recital is
   a lie.
   Long-running or unattended work also runs under `watchdog` — its
   `skills-reminder` profile (30 min) is mandatory in principle and is set
   up at task start, never remembered mid-work.
   Overlapping rules resolve toward the stricter one; a conflict that
   blocks work is a stop-and-ask, not a silent pick.
7. **Write English, always.** Everything the agent touches — code,
   comments, docs, READMEs, skill files, commits, tickets — is
   English-only, regardless of the conversation language. The chat with
   the user is the only exception: it mirrors the user's language.
6. **A failed skill load is recoverable — recover it, then proceed.**
   When the harness's Skill invocation fails (skill not listed, not
   registered, load error), the task is not blocked: skill execution
   outranks the broken loader, and interrupting the current flow to
   recover is allowed. Ladder, in order: resolve the skill's location
   at runtime (the catalog the environment exposes, fallback
   `%USERPROFILE%/.agents/skills`), Read its `SKILL.md` directly from
   disk and follow it as loaded content; not there — check the harness's
   other skill roots and the instructions already in context; ask the
   user only when the skill exists nowhere. A missing EXTERNAL skill
   (harness-side, not part of this collection) fails safe: report it and
   offer the user pick — search for it, skip it, or another route; never
   route around it silently. A manual load counts as loaded: the rest of the process applies as normal, including
   re-reading the file from disk on the next use.
8. **Read the project before acting.** Entering any project, read its
   .md files first — AGENTS.md, README, docs — forced, not optional:
   they carry the project's own rules, and skipping them is how an
   agent repeats mistakes the project already documented. Unsure
   whether a file is in scope to read → user pick. A user pick = one
   message presenting the situation and the options; the user's choice
   is the only thing that proceeds past it (same protocol as
   workplanx's decision gate).
9. **Notify the owner on completion.** When a unit of harness work
   finishes — a task closed, a card done, a long job ended — send the
   owner a summary through `scripts/notify.py` beside this file; the
   script's docstring is the manual (levels, media, config). One summary
   per task, sent by the orchestrator; delegated agents stay in the
   workplanx log. Attach media when the work has visual output. Also the
   way to reach the owner mid-work when unattended — a blocked decision
   during unattended work is a notify, not silence. The script fails
   loud when the channel is down: report that failure, never swallow it.

## Fail loud

- A destructive op done unasked is the failure — even if it worked.
- A skipped test/check reported as green is a lie, not a pass.
- An external service touched unasked is a breach, even with good intent.
- A hardcoded path that rotted is a process failure — resolve at
  runtime.
- A task abandoned because a skill failed to load is the failure —
  recover it (Process item 6), never a silent give-up.

