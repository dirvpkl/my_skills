---
name: thinking
description: Dispatcher for the think-first bundle — loads solution-search + workplanx + spine together for any request to think, brainstorm, or decide an approach before building. ALWAYS invoke this skill when the user says "давай подумаем", "побрейнштормим", "подумай", "можешь поискать чето", "надо чтобы ты…", "обсудим идею", "как лучше сделать X", "brainstorm", "help me think", "what are our options", "is there a better way", or starts weighing approaches/ideas aloud in any domain — even without an explicit "think" word. NOT for bare opinion requests with no think/search ask ("оцени мои проектики" → answer with a spine stance, no skill) and not for judging finished work (fresh-eyes) or executing a decided approach (coding).
version: 1.1.2
---

# thinking (dispatcher)

<!-- v1 - 2026-11-11: initial release. Router only — no rules live here; the three siblings carry them. -->
<!-- v1.1 - 2026-11-11: owner trigger family added ("подумай", "можешь поискать чето", "надо чтобы ты…"); bare opinion requests ("оцени мои проектики") explicitly routed OUT to a spine stance, not this skill. -->

This file is a router, not a rulebook. It contains no method, no stance rules, no
gate logic — those live in the sibling skills it loads. Its only job is: given a
think-first request, load the whole bundle at once and pick the lane.

## plugins/manifest.json

The authoritative list of what loads alongside (`dependencies`). The `modules`
list is empty on purpose: this package has no sub-folders, everything it needs
is a top-level sibling skill. If this file and the manifest disagree, the
manifest wins.

## Activation manifest — what loads together

- **Think-first request** (weigh approaches, brainstorm, decide how to do X)
  → `solution-search` + `workplanx` + `spine`, all three, in the same turn —
  not sequentially-if-remembered. This is one combined obligation, like the
  coding package's write-path set.
- Division of labor, so nothing gets duplicated:
  - `spine` governs **stance** during the discussion: own takes every turn,
    labeled wild-shots, no reflexive agreement, verdict before flattery.
  - `solution-search` drives the **method**: decompose into verbs, less-make
    ladder, URL evidence, max 2–3 candidates + one recommendation.
  - `workplanx` owns the **artifact path**: topic folder
    `plan → search → decision → log → gate`, and the transcribed `user-pick:`
    gate is the single bridge back to building.

## Two lanes — pick by what the user actually asked for

- **Idea talk** ("оцени идею", "как тебе", opinion-level, no decision pending)
  → `spine` stance from the first reply; `solution-search` method only if the
  user asks for evidence or options. **No topic folder, no gate** — ceremony at
  talk level is a routing violation. If the talk converges into "давай это
  сделаем", open the `workplanx` folder at that moment, not earlier.
- **Real pre-decision** ("как сделать X", "чем заменить Y", before anything is
  designed) → full bundle: `workplanx` topic folder opens, `solution-search`
  writes `search.md` + `decision.md`, and nothing gets built until
  `workplanx/scripts/plan_gate.py --phase build` is green on a transcribed
  `user-pick:`.

## Handoff after the gate

A green build gate hands off by scale: single task → `coding`; goal too big
for one pass → `mission`; repeat-until-green → `loop`. Open-ended research the
user asked for explicitly (`find what's new on X`) → `researcher` feeds
findings in as a one-line "what to decide + which verbs" handoff.

## Does NOT trigger on

- Judging finished work → `fresh-eyes` (nothing was decided here).
- Executing an already-decided approach → `coding` (the pick lives in a
  `decision.md`).
- Factual questions with no decision ("как работает X") → answer directly.

## Near-miss counterexamples

- "оцени мои проектики" (bare opinion request, no think/search ask) → answer
  directly with a spine stance; NOT this skill — the owner sets this skill's
  trigger family as "подумай", "можешь поискать чето", "надо чтобы ты…".
  NOT `fresh-eyes` either — nothing was built for it to judge.
- "оцени этот дифф / готовый проект" → `fresh-eyes`, not here.
- "сделай X по решению из вчера" → `coding`; the `user-pick:` already exists.
