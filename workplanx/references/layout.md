# Topic folder layout

`<project>/.workplanx/<topic-slug>/` — one folder per pass. Many passes per
project = many folders, never one shared log. `.workplanx/` is gitignored.

## Files (in order)

- `plan.md` — verbs of the task (`<verb-1>` + `<verb-2>` + ...), scope,
  non-goals. Written by the agent at task start; proceeding past it is not
  approval of anything — the only approval that gates code is `user-pick:`
  in `decision.md`.
- `search.md` — per verb: queries run, candidates (`<name>` + `<URL>` +
  ladder level), fit/no-fit, pick. Zero URLs fails — except the documented
  zero-candidate path (queries logged, no suitable candidates → decided as
  `<own-make>` with the query log as reason). Optional `serendipity:` block.
- `decision.md` — max 2-3 candidates with tradeoffs, one recommendation,
  `user-pick:` line. The agent transcribes the user's reply verbatim into
  this line — never invents it. No implementation starts before this line is
  filled.
- `log.md` — what each skill did on this task, one section per skill: what it
  did, what it found, what it deliberately left out. Append-only, never
  rewritten. This is the file that makes "other skills log to the folder, not
  to chat" true — without it the promise has nowhere to land.
- `gate.log` — appended output of every `plan_gate.py` run (green or red +
  fixes). History, not a rewrite. Not a substitute for `log.md`: this is the
  gate's run history, not the work.

## Contracts

- Positive structure only: the gate checks that sections exist (verb
  headers, query lines, URL lines, ladder lines, pick lines). It does not
  trust adjectives — "thoroughly searched" without URLs still fails.
- URLs must look like URLs (`https://<host>/<path>`). Reachability is not
  checked here (that's the reviewer's job) — shape is.
- `decision.md` without `user-pick:` blocks the build phase.
- Ladder levels are domain-neutral (`<hosted>` / `<open-project>` /
  `<component>` / `<template>` / `<own-make>`, see `solution-search`). The gate
  still accepts the older `library` / `oss` / `own-code` spellings so folders
  written before solution-search 1.8.0 keep validating.
- Phases: `plan` → `search` → `decision` → `build`. `code` is a legacy alias
  for `build`, accepted by `plan_gate.py` only — write `build` in new folders.
- **Other skills may add their own files** to the topic folder (a loop's
  contract and ledger, for example). The gate checks only the five core files
  and ignores extras, which is deliberate: a second gate policing another
  skill's file is how two sources of truth appear. The skill that owns an extra
  file documents its shape in its own SKILL.md, and that's the only place it's
  described.
- Topic slug: `<date>-<short-topic>` (e.g. `09-22-<topic>`). Keep it
  filesystem-safe, lowercase, hyphens.
