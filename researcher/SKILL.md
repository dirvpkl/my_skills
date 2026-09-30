---
name: researcher
description: Autonomous open-ended research for surfacing recent or non-obvious findings on a topic — new releases, niche tools, buried resources, underrated services. Searches abstraction chains (topic → topic class → who else solves it), not just literal queries. Hands pre-decision choices off to solution-search (brainstorm). Not a comparison of predefined options against criteria. Triggers only on explicit request to find/dig up/check what's new on a topic.
version: 1.3.1
---

# researcher

Core behavior lives here. Everything else this skill draws on — channel checklist, search technique, and the list of currently-loaded modules — lives in `references/` and `plugins/`, loaded on demand. Extend those, not this file.

- **plugins/manifest.json** — the list of active modules for this skill (what's loaded, from where, and why). Read this first if you're unsure what's currently plugged in.
- **references/sources.md** — the three source classes (Contentsphere / Artifacts-residue / Registries) and the channel checklist within each.
- **references/patterns.md** — how to search once inside a channel (sort-by-new, cross-domain transfer, raw-data-over-writeups, RSS-as-radar) and optional search engines (Brave, SearXNG, Exa, dorking).
- **references/source-log.md** — a running log of research *sources/channels* (websites, hubs, aggregators) discovered mid-session that weren't already in the checklist. Not a log of findings, not a log of skill changes — specifically new places to look, so they can be folded into `sources.md` later once they've proven useful more than once. See "Self-discovery" below for when to write to it.

## Trigger
Only on explicit user request ("find what's new on X", "dig into topic X", "what's the current state of X"). Does not trigger itself on unfamiliar errors or knowledge gaps during other tasks.

## Handoff to solution-search (brainstorm)
`solution-search` is declared in this skill's `dependencies` — it loads alongside this one rather than being looked up by name at runtime. If the research question is really a pre-decision choice ("what should we build this with", "is there something ready for X") — research the abstraction chains, then hand the topic to `solution-search`: it decomposes into verbs, walks the ladder with URL evidence, and returns candidates with a user pick. Researcher surfaces findings; it never picks stacks or writes decisions. The handoff is one line in the report: what to decide + which verbs it splits into.

## Goal
Not a comparison of options against criteria. The goal is to surface genuinely useful findings on a topic — things the user likely doesn't already know. A finding qualifies if it's **recent** (new release, announcement, shift in the field) **or** **non-obvious** (niche, underrated, not what shows up in a five-second search) — ideally both. Skip anything that's common knowledge, a rehash, or something the user has almost certainly already seen given their background.

## Frame the topic broadly before narrowing
Search the underlying category first, without user-supplied constraints like "free", "cheap", "best" baked into the query — those filter out things that qualify but don't market themselves that way. Apply constraints afterward, when filtering results, not before, when forming the query. If the topic has an alternate framing (e.g. "free LLM API providers" vs "cheap GPU inference clouds to self-host on"), treat both as separate angles worth running, not as the same search.

## Process — think out loud
This skill runs autonomously, but every step gets narrated, not just the final report. At each move, say what's happening and why:
- What's being searched and why this angle was picked next.
- Which channel type is being checked and why it fits this topic (or why a channel is being skipped as inapplicable).
- What came back — a real lead, noise, or nothing — and what that changes about the next move.
- When switching angles or channels, say what didn't work about the previous one.
- When two sources disagree, say so as it's noticed, not just in the final report.

This isn't decoration — the reasoning itself needs to be visible and followable step by step, not just the output at the end.

## Search methodology
- Prioritize primary sources (official announcements, repos, changelogs, pricing pages) over rewrites and SEO content. The Registries class (pricing pages, HF listings, package registries — see `references/sources.md`) is itself primary source material, not a rewrite; the distinction that matters is structured reference data vs. opinion/rehash content, not whether something looks like a "list."
- Prefer recent material; if something older is included because it's genuinely non-obvious, say why it's still relevant now.
- Don't stop at the first page of results. Vary query angles (different keywords, different channel types) before concluding there's nothing more.
- Stop condition, two levels:
  - **Per angle**: if 2-3 reformulations of the same query on the same channel keep returning the same results, that angle is exhausted — move to a different channel or source class, don't keep rephrasing the same search.
  - **Overall**: wrap up once every applicable source class (Contentsphere, Artifacts/residue, Registries) has been checked at least once for this topic and recent angle-switches aren't turning up anything new — not after a fixed number of searches.
- Quoting limited to short exact phrases (a few words) where wording matters — everything else paraphrased. Hard constraint, not a style preference.
- If a claim can't be traced to a source, don't include it as fact — flag it as unverified or drop it.
- When sources conflict (e.g. a channel-search result says one thing, a repo says another), report both with a "sources disagree" note rather than picking one to present as settled.
- Actively filter out noise: don't pad the report with mainstream/obvious stuff just to have more items. Fewer good findings beat many mediocre ones.

## Ground it in context
Where relevant, note briefly why a finding matters given what's known about the user's setup/interests — but don't force this if it's a stretch.

## Before the final report — check what to exclude
Search widely across all applicable channels as normal — don't pre-filter during search. But before writing the final report, ask the user: are there specific services/tools/sources already known or not of interest that should be left out of this report? Exclude those from the final list based on the answer. This keeps search broad while keeping the report free of things the user has already seen or doesn't care about — filtering happens once, at the end, not throughout the search.

## Report format
Flat list, no filler:
- **[Finding name/title]** — one line on what it is, link, one line on why it's worth attention (recent / non-obvious / both).
- Group loosely by sub-theme only if the topic is broad enough to need it — otherwise just a plain list.
- End with what's left unclear or unverified, if anything — don't guess to fill gaps.

## Self-discovery of new *sources* (not new skill features)
If a genuinely good research channel/hub/aggregator turns up during a session that isn't already listed in `references/sources.md`, append a one-line entry to `references/source-log.md` — what it is, which source class it belongs to (Contentsphere / Artifacts-residue / Registries), and which topic surfaced it. Do this after the session, not in the final report to the user — it's bookkeeping for this skill's own reference material, separate from what gets shown to the user. Periodically (e.g. when `source-log.md` accumulates several entries, or when asked), fold proven-useful entries into `references/sources.md` proper and clear them from the log.

This is strictly about *where to search* (websites, channels, aggregators). It is not a log of skill changes — those go in `CHANGELOG.md` — and not a log of research findings — those live only in the report given to the user.

## Extending this skill
New capability (a new module, not just a new source) is added as a file under `references/` or `plugins/`, then registered in `plugins/manifest.json` with a name, path, version, and one-line description of what it adds. Nothing outside the manifest needs to change — this file doesn't hardcode a list of modules to avoid going stale as things are added or removed. See `plugins/manifest.json` for the current module list and `plugins/README.md` for the format.

Planned/reserved module ideas (not built yet — add to the manifest once they exist):
- **Session tracker** — a running plan/todo file so a long or repeated research session doesn't lose track of what's been checked.
- **Findings memory** — a running log of past *findings* (distinct from `source-log.md`, which logs channels, not findings) so repeat runs on a similar topic don't re-surface the same thing as if it were new.
- **Output formatter** — a plugin to reshape the final report into a user-specified style/format. Deliberately not built yet — it should hook into however this environment already handles user output-style preferences, rather than duplicating that mechanism inside this skill.
