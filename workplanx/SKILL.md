---
name: workplanx
description: Task plan-and-log router — every non-trivial task gets a topic folder with plan/search/decision/gate files that later skills verify structurally, plus a fresh-eyes review at the end. ALWAYS invoke this skill at task start, before any search or code, on any non-trivial task (new feature, integration, replacement, multi-step fix — "давай сделаем", "реализуй", "make it happen" once a pick exists). Do not start working without a topic folder and do not keep task logs in chat — use this skill first. Trivial one-line edits are the only exemption.
version: 1.11.0
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
   order. `decision.md` carries a `counter:` line — the best case against
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
   and "потом сделай" thoughts) gets appended to `log.md` verbatim, quoted,
   with a date — same day it arrives. Skill-generated entries log what the
   agent did; this rule logs what the owner SAID. A ruling that lives only
   in the chat transcript is lost to the next session; the folder is the
   memory. Chat stays for the conversation — the folder stays the record.
6. Later skills (`solution-search`, `coding`) read and extend the same folder —
   they never start a second log elsewhere.
7. Judging finished work is not this skill's job — when the work is done and
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

`plugins/manifest.json` has a top-level `dependencies` array — names of other
skills in the collection that load alongside this one. It is the only place
that relationship is written: `SKILL.md` never lists dependency names inline,
because a hand-maintained list in prose is exactly what rots. `modules` answers
"what files are inside this skill", `dependencies` answers "which other skills
come with it" — different questions, don't merge them.

`dependencies_runtime` is the sibling array for skills that load alongside but
live OUTSIDE the collection (harness built-ins and the like). Those names are
never resolved against the collection: `scripts/validate_manifest.py` resolves
them through the external roots declared in `runtime.toml` (`[skills]
external_roots`, next to the live catalog; shape documented in the repo's
`runtime.example.toml`). Same rule as `dependencies` — the manifest is the only
place the names are written, and a name that resolves nowhere fails
validation loudly, listing every root it tried.

## Extending this skill

New file types or phases go into `references/`, registered in
`plugins/manifest.json` — see `plugins/README.md`.
