# The founding case: ManyCP (2026-11-12)

Task: find analogs of "API as a product, cross-listed on marketplaces"
(the ampm project). Owner-approved for reuse as this skill's teaching
example.

## What object-queries returned

Searched first (noun-queries):

- "list of MCP marketplaces"
- "where to sell APIs"

Every hit was a VENUE — RapidAPI, apilayer, PromptBase and friends.
Useful, but each was a shelf everyone already knows, all SEO-optimized
landing pages. They answer "where do I list?" — never "who else builds
the plumbing?".

## The breakthrough — one verb-tool query

`MCP server multi-registry publisher automation tool`

Run through omniroute's `exa-search` provider (semantic/neural
retrieval, not keyword match). One page of results returned the ENTIRE
competitive class:

- **ManyCP** [hosted-service] — ampm's twin: "paste your repo, we
  publish to 26 directories". The owner's favorite find.
- **mcptower.com "Distribute"** [hosted-service] — a second hosted twin.
- 4 OSS repos [oss-repo] — skill-publisher style, mcp-submit, mcpx-cli —
  prototypes of the same verb.

Owner's verdict (paraphrased): "manycp is actually quite good — I don't
even know where you found it" — and the technique was promoted to memory as
`search-the-verbs-tool-not-the-thing`.

## Teaching points

1. The class was INVISIBLE to object-search — the same session had
   already mapped the venues without seeing a single twin.
2. "The slot is occupied" and "nobody built it" are verdicts
   object-search cannot reach — only a verb-tool query gets there.
3. One semantic query beat every keyword reformulation; the provider
   mattered as much as the phrasing.
4. This skill is that memory's generalization: decompose the thing into
   verbs, query each verb's tool class, classify what comes back.
