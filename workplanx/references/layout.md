# Topic folder layout

`<project>/.workplanx/<topic-slug>/` — one folder per pass. Many passes per
project = many folders, never one shared log. `.workplanx/` is gitignored.

## Files (in order)

- `plan.md` — verbs of the task (`<verb-1>` + `<verb-2>` + ...), scope,
  non-goals. Each task also names its **consumer**, its **evidence** (what
  will be verified and what result counts as achieved, fixed before the
  work starts — "integrated != wired") and its **association**: an analogy
  that carries the task's structure (faces, throws, chances — not a
  decorative vibe). Written by the agent at task
  start; proceeding past it is not approval of anything — the only approval
  that gates code is `user-pick:` in `decision.md`.
- `search.md` — per verb: queries run, candidates (`<name>` + `<URL>` +
  ladder level), fit/no-fit, pick. Zero URLs fails — except the documented
  zero-candidate path (queries logged, no suitable candidates → decided as
  `<own-make>` with the query log as reason). Optional `serendipity:` block.
- `decision.md` — max 2-3 candidates with tradeoffs, one recommendation, a
  `counter:` line (the best case against that recommendation, written before
  the pick is requested — the duel-lite check: a recommendation that cannot
  survive its own counter is not ready), then the `user-pick:` line. The
  agent transcribes the user's reply verbatim into this line — never invents
  it. No implementation starts before this line is filled.
- `log.md` — what each skill did on this task, one section per skill: what it
  did, what it found, what it deliberately left out. Append-only, never
  rewritten. This is the file that makes "other skills log to the folder, not
  to chat" true — without it the promise has nowhere to land.
- `gate.log` — appended output of every `plan_gate.py` run (green or red +
  fixes). History, not a rewrite. Not a substitute for `log.md`: this is the
  gate's run history, not the work.
- `afterword.md` — written once at pass end, before `fresh-eyes`: what
  worked, what to add, what was missing, cool-to-have, one labeled
  wild-shot, and a `harvest:` block — 0-N concrete skill patches born in
  this pass, each naming the rule and the skill it belongs to (`none` is a
  legitimate harvest). Proposals wait for the user's bump and are then
  executed as normal edits; the pass never applies them itself. This is the
  collection audit's input (see `watchdog`'s `collection-audit` profile).
  The gate ignores it as an extra but scans it for dangling `[[links]]`.

## Contracts

- Positive structure only: the gate checks that sections exist (verb
  headers, query lines, URL lines, ladder lines, pick lines). It does not
  trust adjectives — "thoroughly searched" without URLs still fails.
- URLs must look like URLs (`https://<host>/<path>`). Reachability is not
  checked here (that's the reviewer's job) — shape is.
- `decision.md` without `user-pick:` blocks the build phase.
- The gate reads only the text on the **same line** after `user-pick:` — put
  the pick on that line, never on the next one; a pick written below the
  colon silently fails the decision phase (regex is single-line).
- Ladder levels are domain-neutral (`<hosted>` / `<open-project>` /
  `<component>` / `<template>` / `<own-make>`, see `solution-search`). The gate
  still accepts the older `library` / `oss` / `own-code` spellings so folders
  written before solution-search 1.8.0 keep validating.
- Phases: `plan` → `search` → `decision` → `build`. `code` is a legacy alias
  for `build`, accepted by `plan_gate.py` only — write `build` in new folders.
- `[[wiki-links]]` — topic files may reference other topics and skills as
  `[[target]]`; a target resolves when `<project>/.workplanx/<target>/` or
  `<project>/<target>/` exists. The gate warns (never fails) on dangling
  targets. Link when it helps the next reader, not for completeness.
- **Other skills may add their own files** to the topic folder (a loop's
  contract and ledger, for example). The gate checks only the five core files
  and ignores extras, which is deliberate: a second gate policing another
  skill's file is how two sources of truth appear. The skill that owns an extra
  file documents its shape in its own SKILL.md, and that's the only place it's
  described.
- Topic slug: `<date>-<short-topic>` (e.g. `09-22-<topic>`). Keep it
  filesystem-safe, lowercase, hyphens.

## Hashtag vocabulary

Single-word `#tags` agents may drop inline in any topic file (log.md,
decision.md, afterword.md, plan/search notes). They are rg-searchable
markers for the recap collector — `rg -n "#gem" <project>/.workplanx/` —
not decoration: write one where the thing it names actually happens.

- `#gem` — a unique find that passed the stock test.
- `#wildshot` — labeled intuition, not evidence.
- `#slot` — a lost fragment awaiting owner recall; recorded so nothing is
  lost.
- `#harvest` — a skill patch born in this pass.
- `#open` — an open question for the owner.
- `#decision` — an owner verdict.

## Owner-message logging (agent-driven)

The owner ruled (2026-11-14): no per-message harness hook — the AGENT does
the logging itself, as turn hygiene. After an owner message that carries a
decision, ruling, task or verbatim-worth material, pipe it through
`scripts/log_owner_message.py` (message on stdin) — it appends verbatim to
`$WORKPLANX_TOPIC/log.md` when the session pins a topic, else to
`<project>/.workplanx/_inbox/<date>.md` (the session inbox). Direct append
works too; the script just keeps the format uniform. The inbox is a
first-class source for recap and handoff — read it before claiming what a
session did or decided. (The harness hook registration was removed the same
day by owner ruling; the script stays as the agent's tool.)
