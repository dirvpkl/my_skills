---
name: workplanx
description: Task plan-and-log router — every non-trivial task opens a topic folder (plan, search, decision, log), gated structurally and closed with an afterword. ALWAYS invoke at task start, before any search or code; a trivial one-line edit is the only exemption. Do not keep task logs in chat — the folder is the record. NOT for deciding what to build (solution-search) or for implementing (coding).
version: 1.14.0
---

# workplanx

Owns the topic folder. Other skills don't log to chat — they log to the
folder, and the gate verifies the folder's shape (not the agent's words).

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
   order. Each task in `plan.md` names its **consumer** and a
   runtime-verifiable check: who uses the result and how the agent can prove
   it is actually wired, not merely written ("integrated != wired" — the
   consumer-trace rule shared with `fresh-eyes`), and its **evidence**:
   what will be verified and what result counts as achieved — fixed before
   the work starts, so the log records proof, not optimism.
   `decision.md` carries a
   `counter:` line — the best case against
   the agent's own recommendation, written before the `user-pick:` is
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
6. Later skills (`solution-search`, `coding`) read and extend the same folder —
   they never start a second log elsewhere.
7. **Delegation carries the record.** Every delegation prompt names the topic
   folder and the exact file the delegated agent must append to (one line per
   unit of work, plus a heartbeat line every 15 minutes inside long units).
   A delegated agent that reports only in chat has left no record; the prompt
   is what makes the recording duty travel with the task.
8. Judging finished work is not this skill's job — when the work is done and
   checks passed, the pass closes with `afterword.md` (what worked, what to
   add, what was missing, cool-to-have, one labeled wild-shot), then
   `fresh-eyes` runs. The afterword carries the harvest: a `harvest:` block
   listing 0-N concrete skill patches born in this pass — a rule from the
   conversation plus the skill it belongs to (`none` is a legitimate
   harvest). Proposals wait for the user's bump and are then executed as
   normal edits; this skill never applies them itself. The afterword is the
   collection audit's input. This
   skill only owns the folder, the gate, and the log.

## Output format

Topic folder with the five files, each passing its phase gate. Folder path
is reported in chat so the user can inspect it.

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
