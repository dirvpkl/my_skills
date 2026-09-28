# Abstract search method

Core rules for pre-decision search. No product names, no concrete picks, no
ready-to-use artifacts here — this file is method only. Placeholders like
`<verb>`, `<hosted>`, `<open-project>` are intentional: the agent fills
them per task, it does not copy them.

## 1. Decompose into verbs

- Split the feature into `<verb-1>` + `<verb-2>` + ... before any search.
- One verb = one need (e.g. `<acquire>` + `<enrich>` + `<publish>` +
  `<observe>`). If two verbs share one query, the split is wrong — redo it.
- Never emit the thing itself at this stage — no artifacts, no configs, no
  scaffolds. Verbs only.

## 2. Abstract one level up before querying

- For each verb: task → task class → who else solves it → what primitives
  they use. Follow the chain at least two hops before querying.
- If the user's nouns survive unchanged into the query, the abstraction
  failed — generalize again.
- Each verb gets 2-3 queries at different abstraction levels, not one
  literal query.

## 3. Ladder per verb (top-down, stop at first fit)

`<hosted>` > `<open-project>` > `<component>` > `<template>` > `<own-make>`.

- `<hosted>`: someone else runs it, we just use it. Highest leverage.
- `<open-project>`: a unit you obtain and run yourself (container-ready
  preferred). Reuse it, don't rebuild it.
- `<component>`: a ready-made piece that does the subtask (package, preset,
  template, service). Default over doing it from scratch.
- `<template>`: working starting point, adapted rather than built.
- `<own-make>`: you do it yourself. Allowed only with a written reason why
  all higher levels don't fit that verb.

## 4. Evidence (mandatory, no exceptions)

Per verb: queries run → candidates (`<name>` + `<URL>` + ladder level) →
fit/no-fit reason → pick. Rules:

- No URLs = no result — except the zero-candidate path: a verb with queries
  logged and zero suitable candidates is a legitimate result, decided as
  `<own-make>` with the query log attached as the reason. "Nothing exists"
  without a query log is not a result; with a query log, it is.
- A candidate without a URL doesn't exist — URLs are what make a candidate real.
- Max 2-3 candidates in the proposal. More = the verbs were too coarse.
- Every `<own-make>` pick names the higher levels tried and why each failed.

## 5. Propose, don't build

- Lead with one recommendation + why. List tradeoffs per candidate:
  scope fit, upkeep cost, lock-in. Ask for a pick. Stop.
- Output is a decision, not an execution. Doing belongs to whatever acts on
  the decision, after approval — never here.

## 6. Serendipity (surfacing off-track finds)

- While surfing, the agent will trip over valuable things that don't answer
  the current verb (a tool for a neighboring problem, a better primitive).
  Don't swallow them and don't wedge them into the proposal.
- Log up to 3 in `search.md` under a `serendipity:` block: `<name>` + `<URL>` +
  one line why it's valuable + which future verb it might serve. Never more
  than 3, never without a URL, never inside the decision.
- The user decides whether any of them becomes a new verb. Unasked promotion
  of a serendipitous find into the recommendation is a violation — surfacing
  is the job, selling is not.

## Anti-patterns (banned)

- Searching the whole feature as one query, then declaring "nothing found".
- Anchoring queries on the user's nouns without abstracting first.
- Proposing `<own-make>` first because it's "simpler" — simplicity is measured
  in what you carry afterwards, and carrying nothing always wins.
- Copying a concrete answer from memory instead of searching. Memory is not
  evidence.
- Opening repositories on disk to lift the implementation. Reuse means the
  same approach rebuilt fresh from current sources — a repo tells you what
  exists, never how it is written.
- Emitting the artifact "while we're here". This skill produces decisions,
  not things.
