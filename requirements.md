# requirements — skills

The collection's registry in Python-requirements format: what exists,
why, and whether it already replaces something else. One block = one
skill: `[Skill](where-from)` — what it is for — plus replacement notes.

## Core (always)

- [base](./base/SKILL.md) — base agent rules: delegation, confirmed
  destructive ops, data integrity; governs every task, including
  talk-only turns. No replacement.
- [chords](./chords/SKILL.md) — the owner's shortcuts: phrase →
  skill/action ("think it through", "what's done?"). Replaces
  "remember my habits".

## Think-first (loaded by the think-first chord)

- [solution-search](./solution-search/SKILL.md) — the method for finding
  an approach: verbs, the less-make ladder, URL evidence, 2-3 candidates.
- [spine](./spine/SKILL.md) — own position in ideation: a take every
  turn, labeled wild-shots, no reflexive agreement or flattery.
- [workplanx](./workplanx/SKILL.md) — topic folder
  (plan/search/decision/log/gate) + the owner's voice in the log (1.10.0).

(replaced: [thinking] dispatcher — folder deleted 2026-11-14, folded
into the think-first mega-bundle chord; history in _graveyard.)

## Code (coding package)

- [coding](./coding/SKILL.md) — coding dispatcher: docker, process-tiers,
  code-quality, testing, logging, external-integrations live inside the
  package; boundaries, proxy-egress, git-workflow moved out to top level
  as mandatory sibling dependencies (split 2026-11-14).
- [ponytail](../../.zcode/skills/ponytail/SKILL.md) — lazy senior
  (vendored from DietrichGebert/ponytail, MIT): the minimal-change
  ladder, lite/full/ultra tiers. LIVES IN BUILT-IN
  (.zcode/skills), not in the collection.
- [frontend-design](../../.zcode/skills/frontend-design/SKILL.md) — taste
  and overall look when building/redesigning UI: tokens, typography,
  "not an AI template"; installed both as a critic and as wiring for the
  build. From anthropics/skills (MIT), vendored into .zcode/skills.

## Split out of coding (split 2026-11-14)

- [boundaries](./boundaries/SKILL.md) — secrets, credentials, logs,
  chat/transcript hygiene, browser data, out-of-project access; loads on
  ANY task that could touch sensitive data, not only code. Was
  coding/security; stays a mandatory coding dependency.
- [proxy-egress](./proxy-egress/SKILL.md) — outbound proxy wiring with no
  silent direct fallbacks: per-library behavior, fallback hunting, live
  verification. Was coding/proxy-egress; stays a mandatory coding
  dependency.
- [git-workflow](./git-workflow/SKILL.md) — version control for any project
  work (code, notes, brainstorms, reverse-engineering, montage, scripts),
  not only code. Was coding/git-workflow; stays a mandatory coding
  dependency.

## Process

- [fresh-eyes](./fresh-eyes/SKILL.md) — clean-context acceptance of
  finished work (quality/conformance) by a fresh agent that never saw
  how it was written.
- [mission](./mission/SKILL.md) — big goal → board of cards, worked
  card-by-card in card sessions.
- [loop](./loop/SKILL.md) — run a task in iterations until a green
  predicate.
- [handoff](./handoff/SKILL.md) — context handover between agents: one
  self-sufficient file so a fresh agent continues without the conversation.
- [recap](./recap/SKILL.md) — project recap collector: rebuilds the
  story from records (workplanx topics, chat thread), not from memory.
- [skill-scaffolder](./skill-scaffolder/SKILL.md) — scaffolds a new
  skill's file layout (SKILL.md + manifest + references + VERSION) and
  restructures loose skills into the modular shape.
- [researcher](./researcher/SKILL.md) — autonomous research for new/niche
  findings on a topic.
- [watchdog](./watchdog/SKILL.md) — supervision tick over a
  process/session without interfering with its work.
- [roi](./roi/SKILL.md) — value-scoring for produced findings: cold-model
  stock gate + six criteria (lens/staleness/actionability/cost/verifiability),
  verdict blocks. Replaces nothing; researcher finds — roi prices what was
  found.

## Domain-specific

- [davinci-editing](./davinci-editing/SKILL.md) — rules for driving
  DaVinci Resolve Studio via davinci-resolve-mcp: preflight, rollback
  points, destructive operations only with explicit confirmation. Loads
  on any Resolve task.

## Built-in, outside the collection folder

- [reverse-engineer-anything](../../.zcode/skills/reverse-engineer-anything/SKILL.md) —
  REA: reverse-engineering binaries/Electron/firmware via the REA MCP;
  loads on an explicit reverse-engineering task. No replacement in the
  collection.
- [ponytail](../../.zcode/skills/ponytail/SKILL.md) — lazy senior;
  a coding dependency (see the line above in "Code").
- chords — [chords](./chords/SKILL.md) from the collection; its bindings
  table is references/bindings.md, updated per the owner's word.

## External, not in the registry

- ZCode's built-in scaffolders (skill-creator, plugin-creator) —
  built in, live in ZCode, not here.
