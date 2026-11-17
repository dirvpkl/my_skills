# solution-search — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Verbs, not the whole task as one query

**Good:** "generate podcast covers" decomposed — one query for cover-art generation tools, one for batch-render pipelines.
**Bad:** a single query: "podcast cover generation workflow tool thing".
Rationale: one verb = one search unit; the whole task as one query anchors on the user's nouns and misses the class one level up.

**Good:** the verb is abstracted one level up before querying — "cover-art generation" becomes the prompt-to-image class, who else solves it, what primitives they use.
**Bad:** querying the user's exact nouns verbatim ("podcast cover art").
Rationale: if the user's nouns survive into the query unchanged, the abstraction failed — the candidates live in the class one level up.

## A decision, not the thing

**Good:** three candidates with tradeoffs, one recommendation — then stopping until the user picks.
**Bad:** picking the top candidate and scaffolding the project folder "to save a round-trip".
Rationale: this skill produces a decision and never the thing; building before the pick is what the workplanx phase gate blocks.

**Good:** the recommendation names the yes it waits for ("picking X needs your go — the gate blocks until then").
**Bad:** "I'll assume option A unless you object by tonight."
Rationale: a decision without a stop is an implementation with extra steps — the pick is transcribed, never assumed.

## user-pick transcribed verbatim, never invented

**Good:** the user replies "the oss one" — `decision.md` reads `user-pick: the oss one`.
**Bad:** `user-pick: open-source raster pipeline (paraphrased from the user's intent)`.
Rationale: the filled line is the entire handoff to the executor — an invented paraphrase is a pick the user never made.

**Good:** the reply is messy ("давай второй но без docker") → transcribed whole, quotes and all.
**Bad:** cleaned-up prose in the pick line.
Rationale: the verbatim mess is the record; tidiness smuggles the agent's interpretation into the one line that gates the build.

## No evidence = no result

**Good:** every candidate in `search.md` carries its evidence (URL, or file path + line for anything local) and ladder level; zero candidates is logged with the queries that found nothing.
**Bad:** "I checked, nothing suitable exists — go with own-make," with no query log.
Rationale: evidence per verb is the rule; a claim without URLs is a guess wearing a verdict.

**Good:** the zero-candidate verdict carries the exact queries AND the ladder level each was tried at.
**Bad:** "searched the internet, nothing."
Rationale: the zero-candidate path is legitimate only with the log — queries plus levels are what make "nothing exists" checkable.


## Verb radar (folded from the radar skill, 2026-11-14)

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Verb tool-class, not the noun's venue words

**Good:** "MCP server multi-registry publisher automation tool."
**Bad:** "MCP server marketplace directory list."
Rationale: marketplace/directory words drag the query back to object-land — venues everyone already knows; the verb's workers built the competitive class noun-queries cannot see.

**Good:** the noun's role is named before querying ("a source of material, not a sales channel").
**Bad:** inheriting the role from the noun's most famous example.
Rationale: one line of class + role keeps the search aimed at the job the noun actually does here, not the job its celebrities do.

## "Nobody built it" gets the radar pass first

**Good:** the research pass has mapped the venues and is about to conclude nobody built it → the verb radar runs before the verdict is emitted.
**Bad:** "object queries found nothing, so nothing exists — done."
Rationale: the ManyCP lesson — that verdict was invisible to object-search and wrong; the pre-verdict reminder exists for exactly this moment.

**Good:** the radar pass runs on the VERB's primitives (generation, publication, indexing), then the verdict lands.
**Bad:** concluding from venue search alone.
Rationale: venues see products; the verb's primitives see the workers nobody marketed.

## Provider order kept

**Good:** `exa-search` (semantic) first, `tavily-search` second — the provider that found the whole class leads.
**Bad:** leading with duckduckgo "since it's the default" (returned empty 4/4 on the founding case).
Rationale: the order is recorded evidence, not preference — re-leading with a proven-empty provider re-runs a known failure.

**Good:** a new provider earns its slot by beating the incumbent on a real query, and the result is recorded.
**Bad:** rotating providers to "try something fresh".
Rationale: order is evidence — a slot is earned by a measurement, not sampled for variety.

## Every hit classified and kept with its URL

**Good:** each hit logged with its URL and kind — twin (shouted loudly), prototype, meta-shelf (followed), monetization pages (logged, not competitors).
**Bad:** "found some similar tools, looks competitive" with nothing written down.
Rationale: no URLs = no result — an unlogged run can't be checked, re-run, or extended; the kinds decide what each hit means for the verdict.

**Good:** a hit that fits no existing kind gets its own kind, written down.
**Bad:** forcing every hit into the established kinds to keep the list tidy.
Rationale: a new kind is often the finding — the taxonomy grows when reality does not fit it.
