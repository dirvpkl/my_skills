---
name: solution-search
description: Brainstorm (aka solution-search) — pre-decision approach search for any domain ("how to do X", "what to use for X", "find me a technique for X", "what to replace it with", "is there a better way") — decompose into verbs, walk the less-make ladder top-down with URL evidence, propose 2-3 candidates with tradeoffs and one recommendation. A second mode handles the stuck case ("what could we do about this", "run a brainstorm") — inventory the assets, diverge into routes with real costs, close the dead ends with their evidence, converge on a pick. ALWAYS invoke this skill before anything is designed, built, or made, and whenever the user asks how to do or what to use for something. Do not pick a stack or start building without the user's pick from this skill's candidates — use this skill first. Method only, no domain knowledge, produces a decision and never the thing itself. The think-first dispatcher `thinking` loads this skill as part of its bundle — after thinking fires, this skill is already loaded; do not re-invoke it separately.
version: 1.16.2
---

# solution-search (aka brainstorm)

Finds the way to do a thing before anyone does it. Pure mechanics — no
product names, no domain defaults, no concrete picks in this file. Anything
concrete (stacks, registries, catalogs, fix lists) lives on the executing
side, never here.

- **references/method.md** — the abstract search method (verbs, ladders, chains).
- **references/brainstorm.md** — the brainstorm mode: inventory, divergent
  routes with real costs, closed dead ends, convergence to a pick.
- **plugins/manifest.json** — active modules. Check it, don't assume this file
  lists everything.

## Trigger

- Any "how to do <X>?", "what to use for <X>?", "find me a technique/reference
  for <X>?" — any domain, digital or physical.
- New capability, new component, or "we already made <X> ourselves, is there a
  better way?" — before design.
- **Brainstorm mode** — "we are stuck, what could we do about this?", "run a
  brainstorm", "what are our options?", or a blocker that the default mode
  already came back empty on. Same skill, different shape: see
  `references/brainstorm.md`.
- **Fog mode (shot-in-the-dark)** — the user says they have an idea but
  cannot describe it, or the request is deliberately vague ("there's
  something here, I don't know what"). React, don't interrogate: see
  Process, fog mode.
- Does NOT trigger on executing an already-chosen approach. That belongs to
  whichever skill implements, and it loads only after `decision.md` carries a
  user pick (see `workplanx`).
- Owner summon register also counts: "fire up the solution searcher",
  "brainstorming", "use it as the last resort" — same skill, any spelling.

## Process

Two modes. The default finds the technique; the brainstorm finds the routes.
Both end in a pick, and neither executes.

**Default mode (find the technique):**

1. Decompose the task into verbs (`<verb-1>` + `<verb-2>` + ...). One verb =
   one search unit. Never search the whole task as one query. (Domain defaults,
   if the executing side has any, are checked against verbs there — never
   here.)
2. Generalize each verb one level up before querying (task → task class →
   who else solves it → what primitives they use). Follow the chain, don't
   anchor on the user's nouns.
3. Walk the ladder per verb, top-down: `<hosted>` > `<open-project>` >
   `<component>` > `<template>` > `<own-make>`. Stop at the first level that
   fits. `<own-make>` needs a written reason why higher levels don't fit.
4. Evidence per verb in the topic folder's `search.md`: queries run,
   candidates with URLs, fit/no-fit reason, ladder level, pick. No URLs =
   no result — except the zero-candidate path: queries logged + zero
   suitable candidates = legitimate result, decided as `<own-make>` with
   the query log as the reason (see `method.md`).
5. Propose 2-3 candidates max with tradeoffs (scope, upkeep cost, lock-in),
   lead with one recommendation and why. Wait for the user's pick before
   anything is made. This skill produces a decision, not the thing — no
   artifacts, no configs, no scaffolding.

**Brainstorm mode (find the routes):** when the question is what to do about
a dead end rather than which technique to use. Inventory the spendable assets
first, then diverge into four to six routes (cost, risk, what it unblocks, a
checkable condition each), keep the previously rejected routes and say whether
their rejection still holds, close the dead ends with their evidence, then
converge on 2-3 proposed routes with one recommendation and the `user-pick:`
line. The mechanics are in `references/brainstorm.md`.

**Fog mode (shot-in-the-dark):** when the user has an idea they cannot
articulate. Do not ask them to describe it — reacting to misses is easier
than describing from scratch. Fire up to three concrete candidate
interpretations per round, each a labeled wild-shot (spine's
one-wild-shot-per-turn cap is waived here by the user's explicit request for
volleys), and let them correct the misses. Shots within a volley must
differ in essence — three variants of one interpretation are one shot read
three times and leak nothing. Corrections are data: each round
narrows the fog; when a real question remains, the default mode takes over
with its verbs and ladder. Stop after two fruitless rounds and ask one
direct question instead — volleys that keep missing are interrogation in
disguise.

## Output format

All output goes to the `workplanx` topic folder (see that skill's layout),
never only chat:
- `search.md` per verb: `verb | queries | candidates (name + URL + ladder level) | pick + why`, plus optional `serendipity:` block (max 3, URLs required).
- `decision.md`: max 2-3 candidates with tradeoffs, one recommendation,
  `user-pick:` filled by transcribing the user's reply verbatim (never
  invented by the agent). That filled line is the entire handoff to whoever
  executes the decision — nothing else crosses over.
- `brainstorm.md` (brainstorm mode only, this skill owns the file): the
  inventory, the routes, the closed directions with their evidence, the
  recommendation, and the open questions for the user.
- Fog volleys live in chat only — they are reactive, not artifacts; the
  converged question continues in the normal mode with its own files.

## Where "nothing gets made yet" is actually enforced

Not here — here it is self-restraint, and prose is not a gate. The binding
check lives one level up: `workplanx`'s phase gate
(`plan_gate.py --phase build`) fails until `decision.md` carries a real
`user-pick:`, and the `coding` dispatcher routes every pre-decision question
here instead of searching in place. Skip this skill and the gate still blocks;
skip the gate and `coding`'s activation manifest is the thing to point at.

## Extending this skill

New capability goes into `references/` or `plugins/`, then gets registered
in `plugins/manifest.json` — see `plugins/README.md`.
