# radar — the full method

The founding case that proves the whole thing: `case-manycp.md`.

## 1. Input

A thing (noun): a product class, project, or idea — from the active
research pass or the owner's phrase ("who else does this?" about X). If
the owner names a specific product, name its class first (ampm →
"API as a product, cross-listed on marketplaces").

## 2. Decompose into verbs (1–4 per topic)

What does one DO with this thing? Pick the verbs that carry the
business: publish, list, submit, discover, track, monetize, cross-list,
syndicate, distribute. 1–4 verbs; each verb is one query angle. When
solution-search is loaded, its verb decomposition is the same move —
reuse it.

## 3. Per verb, build the tool-class query

```
<noun> <verb> automation tool
optionally: <noun> <verb> service hosted
```

The founding query, built this way: `MCP server multi-registry
publisher automation tool`.

**HARD RULE — never add the noun's marketplace words**: marketplace,
directory, "where to", "list of". Those words drag the query back to
object-land and the results become venue landing pages. The tool class
lives behind them, invisible to that phrasing — this is exactly what the
founding case demonstrated (see `case-manycp.md`).

## 4. Provider order (measured 2026-11-12/14)

1. **router `exa-search` FIRST** — semantic/neural retrieval; it
   returned the entire class in one page where keyword engines returned
   shelves.
2. **`tavily-search` second** — works, weaker on class-level phrasing.
3. **Never lead with `duckduckgo-free`** — returned empty on 4/4 queries
   on 2026-11-12/14. SearXNG keyword search is a last resort and misses
   semantic classes.

Omniroute call:

```
POST {router}/v1/search
{"query": "<verb-tool query>", "provider": "exa-search", "count": 5}
```

`{router}` base URL and the API key come from this skill's runtime
context (`runtime.toml` next to this SKILL.md, `[router]`
section), resolved at run time — never hardcoded in this skill, a
script, or a prompt. No key available = loud fail, never a silent
fallback to another provider without saying so.

If exa is down, tavily works. The method uses whatever search tooling
the session has — no script ships with this skill.

## 5. Classify every hit by kind

| kind | meaning | action |
|---|---|---|
| hosted-service | a live twin selling the same verb | shout loudly — this is the find |
| oss-repo | a prototype of the same verb | log — competitor or free alternative |
| directory-of-tools | a meta-shelf of tools | follow it — mine it for more hits and venues |
| venue | the noun's own marketplace | noise here; already mapped by researcher |
| noise | SEO filler, unrelated | drop |

Edge cases:

- **Advertise / paid-ads pages are NOT competitors** — they are
  monetization evidence, still logged (that is how the mcpwell/mcpvault
  featured slots were found on 2026-11-14).
- **A hosted twin is not doom**: log its shape (pricing, directory
  count, rails, claimed savings — ManyCP's "~6h saved per server").
  That is free market validation.

## 6. Stop condition

2–3 reformulations of the same verb-query returning the same hits = that
angle is exhausted (researcher's per-angle rule). Move to the next verb.
All verbs exhausted = radar done.

## 7. Output — one block per verb, URLs never dropped

No URLs = no result (solution-search rule). Exact format:

```
verb: publish (to many registries)
  query: "MCP server multi-registry publisher automation tool" [exa]
  → ManyCP [hosted-service] — ampm's twin, 26 directories, freemium
  → mcptower.com/distribute [hosted-service] — second twin
  → github.com/x/mcp-submit [oss-repo] — CLI prototype
verb: monetize
  …
```

End with one line per verb left empty (no hits after the stop condition)
and an overall verdict: does "nobody built it" stand? (After the founding
case, it usually does not.)

## Triggers and auto-attach

- Owner phrases: "who else does this?", "find competitors/twins",
  "is there a tool that automates this?", "who builds the same
  thing?", "verb radar".
- Inside researcher/solution-search passes: after mapping venues, ALWAYS
  run one verb-tool query before concluding "nobody built it" — the
  ManyCP lesson: "the slot is occupied" was invisible to object-search.
