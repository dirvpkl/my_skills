---
name: radar
description: Competitor/twin finder for any product class — decompose the topic into verbs and search the TOOL of each verb ("X publisher/submitter/automation tool") through semantic search, which surfaces hosted twins, OSS prototypes and directories-of-tools that object-queries (marketplace lists, "where to sell X") structurally miss. ALWAYS invoke before concluding "nobody built it" — the occupied-slot fact is invisible to object-queries. Triggers: "кто ещё это делает", "найди конкурентов", "есть ли инструмент, который это автоматизирует", "кто строит то же самое", "radar", "проверь двойников". Runs AFTER venue mapping (researcher maps shelves; radar finds who else builds the plumbing), BEFORE any build decision.
version: 1.0.0
---

# radar — search the tool of the verb, not the thing

A noun-query ("list of X marketplaces", "where to sell X") hits what
markets itself: venue landing pages and SEO listicles. It answers "where
do I list?" — never "who else builds the plumbing?". The plumbing is where
twins, competitors and prototypes live. radar runs one tool-class query
per verb and returns the competitive class in a single sweep.

## The rule (hard)

Before ANY build decision on a researched topic, radar runs at least one
verb-tool query. "The slot is occupied" is a radar finding — an
object-query cannot prove or disprove it.

## Method

1. **Decompose the topic into verbs** (1–4): what does one DO with the
   thing — publish, submit, syndicate, monetize, discover, track.
2. **One tool-class query per verb**: `<noun> <verb> automation tool`
   (optionally `… service hosted`). NEVER add marketplace words
   (marketplace / directory / where-to / best) — they drag results back
   to object-land.
3. **Provider order** (measured): omniroute `exa-search` first — semantic
   retrieval finds the class; `tavily-search` second; local SearXNG last
   resort. Keyword engines are a fallback, not the lead.
4. **Classify every hit** (see references/radar-method.md):
   hosted-service (a twin — report loudly, log its shape: pricing,
   scale, rails — free market validation), OSS-repo (a prototype),
   directory-of-tools (a meta-shelf — follow it for more venues),
   venue, noise.
5. **Stop condition**: 2–3 reformulations returning the same hits — the
   angle is exhausted.
6. **URLs mandatory**: no URL = no result. Advertise/featured pages are
   logged as monetization evidence, not discarded.

Full rubric, query patterns and the worked generic example live in
`references/radar-method.md`. The search wrapper is `scripts/radar_search.py`
(provider fallback chain + heuristic kind hints; `--selftest` runs offline).

## Output

Per verb: the query + hits with URL, kind, one-line "why it matters".
Verdict block at the end: `radar: <n> twins, <n> prototypes, <n> meta-shelves`
— and the loud line if twins exist: `slot: OCCUPIED`.

## Does NOT trigger on

- "find venues/shelves for X" — that is researcher (object side).
- Judging or pricing findings — that is roi.
- Ideation takes — spine.

## Boundaries

- Method only: no session cases, no project names in this skill (OSS rule).
- radar never deletes or rewrites earlier research — it appends a radar
  block and flags contradictions ("sources disagree" style).
