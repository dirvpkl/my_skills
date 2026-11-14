# solution-search — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Verbs, not the whole task as one query

**Good:** "generate podcast covers" decomposed — one query for cover-art generation tools, one for batch-render pipelines.
**Bad:** a single query: "podcast cover generation workflow tool thing".
Rationale: one verb = one search unit; the whole task as one query anchors on the user's nouns and misses the class one level up.

## A decision, not the thing

**Good:** three candidates with tradeoffs, one recommendation — then stopping until the user picks.
**Bad:** picking the top candidate and scaffolding the project folder "to save a round-trip".
Rationale: this skill produces a decision and never the thing; building before the pick is what the workplanx phase gate blocks.

## user-pick transcribed verbatim, never invented

**Good:** the user replies "the oss one" — `decision.md` reads `user-pick: the oss one`.
**Bad:** `user-pick: open-source raster pipeline (paraphrased from the user's intent)`.
Rationale: the filled line is the entire handoff to the executor — an invented paraphrase is a pick the user never made.

## No URLs = no result

**Good:** every candidate in `search.md` carries its URL and ladder level; zero candidates is logged with the queries that found nothing.
**Bad:** "I checked, nothing suitable exists — go with own-make," with no query log.
Rationale: evidence per verb is the rule; a claim without URLs is a guess wearing a verdict.


## Verb radar (folded from the radar skill, 2026-11-14)

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Verb tool-class, not the noun's venue words

**Good:** "MCP server multi-registry publisher automation tool."
**Bad:** "MCP server marketplace directory list."
Rationale: marketplace/directory words drag the query back to object-land — venues everyone already knows; the verb's workers built the competitive class noun-queries cannot see.

## "Nobody built it" gets the radar pass first

**Good:** the research pass has mapped the venues and is about to conclude nobody built it → the verb radar runs before the verdict is emitted.
**Bad:** "object queries found nothing, so nothing exists — done."
Rationale: the ManyCP lesson — that verdict was invisible to object-search and wrong; the pre-verdict reminder exists for exactly this moment.

## Provider order kept

**Good:** `exa-search` (semantic) first, `tavily-search` second — the provider that found the whole class leads.
**Bad:** leading with duckduckgo "since it's the default" (returned empty 4/4 on the founding case).
Rationale: the order is recorded evidence, not preference — re-leading with a proven-empty provider re-runs a known failure.

## Every hit classified and kept with its URL

**Good:** each hit logged with its URL and kind — twin (shouted loudly), prototype, meta-shelf (followed), monetization pages (logged, not competitors).
**Bad:** "found some similar tools, looks competitive" with nothing written down.
Rationale: no URLs = no result — an unlogged run can't be checked, re-run, or extended; the kinds decide what each hit means for the verdict.
