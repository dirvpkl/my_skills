# patterns

Referenced by SKILL.md. How to search once inside a channel, plus optional search engines.

## Search patterns, not just channels
The channel checklist (`sources.md`) is *where* to look. These are *how* to look once there — apply them regardless of which channel is in use:
- **Sort by new, not by top/hot.** A gem lives in the gap between "posted" and "went viral." By the time something is top-voted, it's already common knowledge. Low-engagement recent posts are where the unclaimed stuff is.
- **Follow specific sources, not just topics.** A search re-run from scratch every time re-finds the same mainstream results. Specific repos, specific accounts, specific niche sites that have a track record of surfacing things early are worth checking directly, not just searching around.
- **Cross-domain transfer.** The best find for a topic sometimes sits in an adjacent community solving a related problem (e.g. crypto-mining communities and AI-inference communities both obsess over cheap compute). When a topic search runs dry, try the neighboring niche.
- **Abstraction chains.** Before searching the topic literally, climb it: `<task>` → `<task class>` → `<who else solves it>` → `<what primitives they use>`. At least two hops up before the first literal query — if the user's nouns survive unchanged into the query, the abstraction failed, generalize again. Then search *each hop*, not just the original: the alternate framing often has its own vocabulary, registries, and communities that the literal query never reaches. Narrate the chain (think-out-loud) so the jumps stay followable; log which hop each finding came from in the report.
- **Raw data over write-ups.** Changelogs, patch notes, API dumps, game data-mines — anything with no journalist/blogger in the middle — often reveals something before anyone writes about it. Worth checking directly rather than waiting for a summary to appear.
- **RSS/feeds as a radar, not a query.** Site-wide "new" feeds (Google News, Hacker News/new, Lobste.rs) surface things nobody searched for yet. This is push, not pull — skim broadly rather than looking for something specific.

## Search engines (optional, not default)
The channel checklist is about *where* content lives; this is about which engine does the crawling. Default is plain web_search — it's free and sufficient for most tasks. Worth having on the radar if it ever stops being enough:
- **Brave Search API** — independent index (not a Google/Bing wrapper), 2,000 free queries/month, no card required. Best free-forever option if a dedicated search API is ever needed.
- **SearXNG** — free, self-hosted metasearch aggregating multiple engines. No usage cap, but requires running and maintaining the instance yourself. Supports dorking-style operators (site:, filetype:, etc.) for narrowing to a specific domain or file type.
- **Exa** — neural/semantic search (finds conceptually similar content, not just keyword matches) — a different capability, not a replacement. One-time signup credit only, not free-forever.

## SearXNG rules (binding, not optional)
- **Always ask the user for their SearXNG instance address at session start.** Never assume it, never reuse one from memory — the address is per-session user input.
- **Never touch the instance config.** No `settings.yml` reads, no file edits, no admin API — stock SearXNG exposes no REST endpoint for the enabled-engines list (its Search API is query-only: `/search?q=&format=json` with `categories`/`language`/`pageno`/`time_range`/`safesearch`). If the enabled set matters, ask the user to paste engine names from the instance preferences page — names only, no secrets, no keys.
- **No static engine snapshot in this skill.** The upstream inventory changes (hundreds of engines, shifting defaults) — per session, check the live docs instead of anything written here: engine loader inventory at `https://docs.searxng.org/dev/engines/engines.html`, defaults at `https://searxng.github.io/searxng/user/configured_engines.html`. Per-engine capabilities (`time_range`, `safesearch`) are on the instance preferences page, not in the docs.
- **The enabled set is readable without touching config.** `GET <instance>/config` returns JSON (read-only, no secrets): `engines[]` with `name`, `enabled`, `categories`, `shortcut`, `safesearch`, `time_range_support`. Use it to see which engines this instance actually runs before planning queries — still never edit `settings.yml` or call the admin API.

Dorking (site:, filetype:, intitle:, inurl:) is a query technique, not a separate engine — use it through SearXNG, or through plain web_search if the operator is supported there.

Currently not worth adopting dedicated APIs (free tiers are one-time credits or too limited to rely on) — noted here as an option to revisit.
