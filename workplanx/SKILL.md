---
name: workplanx
description: Task plan-and-log router — every non-trivial task opens a topic folder (plan, search, decision, log), gated structurally and closed with an afterword. ALWAYS invoke at task start, before any search or code, when the work is project-scale (a feature, a refactor, a migration); bare execution commands go to coding without a folder. Do not keep task logs in chat — the folder is the record. NOT for deciding what to build (mindstorm) or for implementing (coding).
version: 1.18.1
---

# workplanx

Owns the topic folder. Other skills don't log to chat — they log to the
folder, and the gate verifies the folder's shape (not the agent's words).
The folder is the agents' playground, not only a record: agents work FROM
it (read the plan, the decisions, the stances) and INTO it (write the log) —
the owner's framing: «workplanx это как бы плэйграунд для агентов».

- **references/layout.md** — folder shape + per-file contracts.
- **references/trigger-log.md** — append-only log of observed trigger
  misses (utterance, fired, should, resolution): the queue, the
  descriptions are the fix. Base's trigger-log moved here 2026-11-15 —
  trigger accounting is workplanx's domain.

## Sink directive

Everything the owner would otherwise read as chat text goes into the topic's
files instead: findings, decisions, positions, logs. Chat stays for the
conversation; the folder is the record. A skill that does not create or extend
a topic folder is breaking its declared `workplanx` dependency, not skipping
ceremony.

## Process

1. Create `<project>/.workplanx/<topic-slug>/` at task start. Ensure
   `.workplanx/` is gitignored (append if missing — that edit is allowed).
   Fallback outside a project: `%TEMP%/opencode-workplanx/<topic-slug>/`.
2. Files inside (see `references/layout.md` for contracts):
   `plan.md` → `search.md` → `decision.md` → `log.md` → `gate.log`. In that
   order. Every task in `plan.md` carries, fixed before the work starts:
   - **consumer** + a runtime-verifiable check — who uses the result and
     how the agent proves it is actually wired ("integrated != wired" —
     the consumer-trace rule shared with `fresh-eyes`);
   - **evidence** — what will be verified and what result counts as
     achieved, so the log records proof, not optimism;
   - **association** — the analogy that carries the task's structure (a
     dice with faces, throws and chances), never a decorative vibe.
   `decision.md` carries a `counter:` line — the best case against the
   agent's own recommendation, written before the `user-pick:` is
   requested (duel-lite: adversarial self-review, not a second agent).
   Cross-references between topic files and skills use `[[target]]`; the
   gate warns on dangling ones. Nothing gets built before `decision.md` has
   a user pick — that is what the `build` phase gate checks, not something
   the agent is trusted to remember.
3. After each phase, run `scripts/plan_gate.py --dir <topic-dir> --phase <phase>`
   (`plan` | `search` | `decision` | `build`; `code` is a legacy alias for
   `build`). Red gate = stop and write the user, don't proceed silently.
4. Every skill that acts on this task appends to `log.md` — what it did, what
   it found, what it left out. One entry per skill, not one per action, so the
   log stays readable at 200 skills. This is what "log to the folder" means;
   `gate.log` is only the gate's own run history and is not a substitute.
5. **The owner's voice lands in the folder, not only in chat.** Every owner
   message that carries a directive, a ruling, a correction, or a wish for
   the active topic (including mid-task asides, walk-away authorizations,
   and "do it later" thoughts) gets appended to `log.md` verbatim, quoted,
   with a date — same day it arrives. No pinned topic, or the message is
   session-general: pipe it verbatim through `scripts/log_owner_message.py`
   (message on stdin) — it lands in `<project>/.workplanx/_inbox/<date>.md`,
   the session inbox, a first-class recap/handoff source (base ¶2 carries
   the same rule). Skill-generated entries log what the
   agent did; this rule logs what the owner SAID. A ruling that lives only
   in the chat transcript is lost to the next session; the folder is the
   memory. Chat stays for the conversation — the folder stays the record.
6. Later skills (`mindstorm`, `coding`) read and extend the same folder —
   they never start a second log elsewhere.
7. **Delegation carries the record.** Every delegation prompt names the topic
   folder and the exact file the delegated agent must append to (one line per
   unit of work, plus a heartbeat line every 15 minutes inside long units).
   A delegated agent that reports only in chat has left no record; the prompt
   is what makes the recording duty travel with the task.
8. Judging finished work is not this skill's job — when the work is done and
   checks passed, the pass closes with `afterword.md` (a LOG: what worked,
   what was missing — recording, not proposals), then `fresh-eyes` runs.
   This skill only owns the folder, the gate, and the log — it never
   proposes work; the self-improve pass lives in `mindstorm` (owner ruling:
   «воркпланх не должен предлагать что-то сделать, он логирует»).

## Output format

Topic folder with the five files, each passing its phase gate. Folder path
is reported in chat so the user can inspect it.

## Attachments

The folder plays with two designed attachments (built as separate
projects, workplanx stays the record):

- **Kanban service: Planka** (mission cards) — PICKED (owner
  2026-11-19): self-hosted docker, Trello-like UI for the owner, REST for
  the agents. Reads/writes mission cards across agent sessions; agents
  are the primary consumers, the owner watches.
- **Graph: Obsidian** — the `.workplanx/` folder opens as an Obsidian
  vault: the topic graph becomes visible without an agent in the middle
  («чтобы не просто пустые мдшки были»). Verified: no better plain-md
  graph tool exists for the agent-raw-access requirement.

Both consume the folder's plain markdown — workplanx never depends on
them being installed.

## The hook watch

The metawatcher hook (parked design) watches this folder's usage: recent
responses with no `.workplanx` mention on project-scale work = a kick to
re-read the skills. The folder's usage is enforceable, not remembered.

## Declaring other skills as dependencies

`plugins/manifest.json` declares exactly one thing: the `dependencies`
array — names of other collection skills that load alongside this one.
That is the only place the relationship is written; the folder layout
itself is the module list (lean shape 2026-11-15: no modules, no
package_version, no dependencies_runtime). A name that resolves to no
sibling skill folder fails the repo validator loudly.

## Extending this skill

New file types or phases go into `references/`, registered in
`plugins/manifest.json` — see `plugins/README.md`.
