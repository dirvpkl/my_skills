# radar-method.md — the query rubric and classification

## Verb decomposition

Decompose the noun into what one DOES with it. Typical verb families:

- **publish / submit** — who ships the thing to venues?
- **syndicate / cross-list** — who multiplies it across shelves?
- **monetize / meter** — who bills for it?
- **discover / track** — who watches it, prices it, refreshes it?
- **automate** — who removes the manual hop?

Pick 1–4 verbs per topic; the verbs that define the product's CORE loop
come first.

## Query patterns

| pattern | example | what it catches |
|---|---|---|
| `<noun> <verb> automation tool` | `dataset publish automation tool` | OSS + hosted builders |
| `<noun> <verb> service hosted` | `dataset syndication service hosted` | SaaS twins |
| `<noun> batch <verb> tool` | `prompts batch submit tool` | bulk operators |

Anti-patterns (never in a radar query): `marketplace`, `directory`,
`best`, `where to`, `top 10`. Those are object-words — they return
shelves, not plumbers.

## Provider order (measured behavior)

1. **`exa-search`** — semantic/neural retrieval. Found a full competitive
   class (hosted twins + 4 OSS repos + a second twin) on ONE query where
   keyword engines returned venue landing pages only.
2. **`tavily-search`** — solid fallback.
3. **Local SearXNG** — keyword; last resort, misses semantic classes.
4. **Keyword-only engines** (duckduckgo-free et al.) — returned empty on
   4/4 radar queries in one measured session; never lead with them.

Endpoint: `POST {omniroute}/v1/search`, body
`{"query": "...", "provider": "exa-search", "count": 5}`; the key and
base URL come from the machine's runtime context (`runtime.toml`
`[omniroute]`), never hardcoded, never logged.

## Hit classification

| kind | tell | action |
|---|---|---|
| **hosted-service** | landing page selling the automation; /pricing, /advertise, /sell | report LOUDLY — a twin exists; log its shape (pricing, scale numbers, rails) as free market validation |
| **oss-repo** | github/repo link, README-shaped | prototype; check stars/activity |
| **directory-of-tools** | a page listing many tools/stores of the class | meta-shelf — follow it; it yields more venues |
| **venue** | a place to list the thing itself | out of radar scope; route to researcher's venue map |
| **noise** | nothing of the above | drop, but count it for the stop condition |

## Stop condition

2–3 reformulations of the same verb-query returning the same hits = the
angle is exhausted. Move to the next verb or close radar with the verdict
block.

## Worked generic example

Topic: "sell datasets". Verbs: publish, monetize.
- Query 1: `dataset publish automation tool` → an OSS repo that bulk-
  submits datasets to registries (oss-repo), a hosted "list your data
  product" service (hosted-service — twin).
- Query 2: `dataset monetization metering service` → a paywall/metering
  SaaS (hosted-service), a directory of data-marketplace fee pages
  (directory-of-tools → meta-shelf).
Verdict: `radar: 2 twins, 1 prototype, 1 meta-shelf — slot: OCCUPIED`.

## Relation to siblings

- **researcher** maps shelves (venues) and finds content — radar runs
  AFTER venue mapping and BEFORE "nobody built it" conclusions.
- **roi** prices radar's finds (a twin sighting is itself a finding —
  price it before acting).
- **solution-search** decomposes to verbs — feed radar those verbs
  instead of re-decomposing.
