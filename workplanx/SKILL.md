---
name: workplanx
description: Task plan-and-log router — every non-trivial task gets a topic folder with plan/search/decision/gate files that later skills verify structurally, plus a fresh-eyes review at the end. Use at task start before any search or code.
version: 1.5.0
---

# workplanx

Owns the topic folder. Other skills don't log to chat — they log to the
folder, and the gate verifies the folder's shape (not the agent's words).

- **references/layout.md** — folder shape + per-file contracts.
- **plugins/manifest.json** — active modules, check it.

## Trigger

- Any non-trivial task (new feature, integration, replacement, multi-step fix).
- Does NOT trigger on trivial edits (typo, rename, comment, no logic change).
- `workplanx` is in the `dependencies` list of every other skill in the
  collection. A skill that doesn't create a topic folder isn't skipping
  ceremony, it's breaking its own declared dependency.

## Process

1. Create `<project>/.workplanx/<topic-slug>/` at task start. Ensure
   `.workplanx/` is gitignored (append if missing — that edit is allowed).
   Fallback outside a project: `%TEMP%/opencode-workplanx/<topic-slug>/`.
2. Files inside (see `references/layout.md` for contracts):
   `plan.md` → `search.md` → `decision.md` → `log.md` → `gate.log`. In that
   order. Nothing gets built before `decision.md` has a user pick — that is
   what the `build` phase gate checks, not something the agent is trusted to
   remember.
3. After each phase, run `scripts/plan_gate.py --dir <topic-dir> --phase <phase>`
   (`plan` | `search` | `decision` | `build`; `code` is a legacy alias for
   `build`). Red gate = stop and write the user, don't proceed silently.
4. Every skill that acts on this task appends to `log.md` — what it did, what
   it found, what it left out. One entry per skill, not one per action, so the
   log stays readable at 200 skills. This is what "log to the folder" means;
   `gate.log` is only the gate's own run history and is not a substitute.
5. Later skills (`solution-search`, `coding`) read and extend the same folder —
   they never start a second log elsewhere.
6. Judging finished work is not this skill's job — when the work is done and
   checks passed, `fresh-eyes` runs. This skill only owns the folder, the
   gate, and the log.

## Output format

Topic folder with the five files, each passing its phase gate. Folder path
is reported in chat so the user can inspect it.

## Declaring other skills as dependencies

`plugins/manifest.json` has a top-level `dependencies` array — names of other
skills in the collection that load alongside this one. It is the only place
that relationship is written: `SKILL.md` never lists dependency names inline,
because a hand-maintained list in prose is exactly what rots. `modules` answers
"what files are inside this skill", `dependencies` answers "which other skills
come with it" — different questions, don't merge them.

## Extending this skill

New file types or phases go into `references/`, registered in
`plugins/manifest.json` — see `plugins/README.md`.
