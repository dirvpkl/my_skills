# source-log

Staging area for newly-discovered research *channels/hubs/aggregators* — not findings, not skill changes.

Referenced by SKILL.md, section "Self-discovery of new sources." Append an entry here whenever a research session turns up a genuinely good channel that isn't already in `sources.md`. Once an entry has proven useful across more than one session, promote it into the proper checklist in `sources.md` and remove it from here.

## What goes here vs. elsewhere
- **Goes here**: a website/hub/aggregator/community that is itself a place to search — e.g. "found a niche GPU-rental Discord directory."
- **Does NOT go here**: an actual research finding (a specific tool, release, or fact) — that belongs only in the report given to the user for that session, nowhere in this skill's files.
- **Does NOT go here**: a change to how this skill itself behaves — that belongs in `../CHANGELOG.md`.

## Format
One line per entry:

`YYYY-MM-DD — [Channel name] — [source class: Contentsphere / Artifacts-residue / Registries] — surfaced while researching [topic] — [why it's worth checking again]`

## Log

2026-09-22 — ScriptBlox (scriptblox.com) — Registries — surfaced while researching roblox headless — structured listing of Roblox scripts with versions/executors, catches what isn't on GitHub (e.g. Infinite Yield builds)
2026-09-22 — DevForum Platform Usage Support — Contentsphere — surfaced while researching roblox headless — threads on VM/VPS detection and Hyperion, early signal on blockers before write-ups
2026-09-22 — WeAreDevs library+scripts+forum — Registries — surfaced while researching roblox headless/executors — executor hub with card statuses (PENDING/DISCONTINUED), scripts, obfuscator; live alternative to dead executor GitHub repos
2026-09-22 — RageInject executor comparison — Registries — surfaced while researching pulsery.gg — 15 executors side-by-side with SHA-256+VT per card, checked-date; ready-made download-verification workflow
2026-09-22 — ANY.RUN public report search — Artifacts-residue — surfaced while researching wearedevs safety — searching "<filename>" before downloading gives sandbox verdicts (JJSploit/Meduza, Solara/Lumma); verify the exact sample, some samples from shady mirrors
2026-09-22 — weao/WhatExpsAre.Online status tracker+API — Registries — surfaced via user tip weao.dev — live successor of WhatExploitsAre.Online with API for auto-checking statuses before launching a batch
2026-09-22 — nexomia.win executor UNC docs — Registries — surfaced via user tip — vendor with API docs, new, no reputation; watchlist
2026-10-31 — batch promotion — eight entries from the "what to sell" sessions promoted into `sources.md` (arxiv, verified-revenue registries, verified business listings, provider retrospective posts, demand radars) and `concept-chains.md` (association norms, clickstream dumps, paper graphs, embedding search). See CHANGELOG 1.4.0.
2026-10-31 — mnfst/awesome-free-llm-apis (github.com/mnfst/awesome-free-llm-apis) — Registries — surfaced while researching free AI agents — per-row probe-dated free-tier list of provider + inference APIs; probes dated within days of session, catches quota changes before write-ups
2026-10-31 — ayautomate.com/free-models — Registries — surfaced while researching free AI agents — ~294 genuinely-free models from 40+ providers with "the catch" column and dated verification rows; monthly email digest
2026-11-07 — TypingMind AI Skills Directory (typingmind.com/skills) — Registries — surfaced while researching agent skill triggering — structured community skill catalog with per-skill convention pages; one of the few indexed registries of published agent skills

- 2026-11-12: agentskill.sh (skill hosting + profile pages) — Registries — surfaced by omniroute/exa scan "tool to publish agent skill to multiple marketplaces".
- 2026-11-12: clawskills.sh (OpenClaw skill discovery) — Registries — surfaced by SearXNG "hosted SaaS skill publisher".
- 2026-11-12: manycp.com (hosted MCP multi-directory submitter; its /directories page is a live venue registry) — Registries — surfaced by omniroute/exa "MCP server multi-registry publisher".
- 2026-11-12: theaicemetery.com / killedbyai.net (graveyard of dead AI products; cautionary-tale channel) — Contentsphere — surfaced by tavily "ChatGPT plugin store shutdown lessons".
