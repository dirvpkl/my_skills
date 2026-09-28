# sources

Referenced by SKILL.md. Channel checklist — where to look, grouped by source class.

## Source classes
Before reaching for the channel checklist, place the topic in one or more of these three classes — they explain *why* a given channel is worth checking, not just that it's on a list:

- **Contentsphere** — content people deliberately made and published: chats, posts, threads, videos, curated link-feeds. The packaging differs (messenger vs forum vs video) but the nature is the same: someone chose to say this publicly.
- **Artifacts / residue** — technical leftovers nobody wrote as content: archived snapshots, crawl indexes, changelogs, data dumps, code containing literal config strings. Nobody authored these for reading; they're a byproduct of something happening, which is exactly why they surface things before anyone writes about them.
- **Registries** — structured, maintained reference data: pricing pages, model/package listings, directories kept as a table of facts rather than a narrative. Not opinion, not residue — deliberately organized as a reference.

## Source channels — run the applicable ones every time
This is a fixed checklist of channel *types*, grouped by the source class above. For each research task, go through it and skip only what's genuinely inapplicable — don't skip for convenience. Within each type, which specific instance to check (which forum, which registry) is a judgment call based on the topic, not fixed.

**Contentsphere**
- **Telegram** — tgstat or equivalent channel-search, for topics where Telegram is a primary venue. Telegram has no real substitute for this: the combination of unauthenticated-viewable public channels, a scrapeable API, and dense niche/gray-area Russian-language content isn't replicated elsewhere. Discord covers similar community energy but is closed to indexing; Reddit is open and indexable but lacks the same niche RU-language density. Treat Telegram as its own category, not one to find an equivalent for.
- **Discord** — check server *directories/catalogs* (listing sites), not in-server search — in-server search is poor and most content sits behind invites anyway. Useful for dev/AI/GPU-rental communities specifically.
- **QQ / WeChat groups** — relevant when a topic has a Chinese-development angle (common in LLM/inference/GPU-cloud spaces). Currently disabled/parked: access typically needs a phone number or a paid account (roughly $1k-range at last check), not worth it yet. Revisit if the topic is China-heavy enough to justify it.
- **VK** — parked for now (not currently used, may be added later). Would otherwise be the closest match to Telegram's combination of open unauthenticated public pages + a well-documented API + dense Russian-language content — noted here as a placeholder, not yet part of the active checklist.
- **X/Twitter** — fast-moving, especially for AI/ML real-time takes and announcements.
- **Reddit** — broader international community takes, sanity-check against the above.
- **Video/short-form** — YouTube, TikTok, Instagram. Good for hype-cycle and visual/demo-driven topics; treat as a signal of what's trending, verify claims elsewhere.
- **Forums & marketplaces** — general-purpose forums and marketplaces relevant to the topic's community (which specific ones depends on topic and language — pick what's actually where that community lives; e.g. wmcentre, ggsel for RU-language digital goods marketplaces, Pikabu for RU-language general forum/social content).
- **News/link aggregators (Google News, Hacker News, Lobste.rs)** — treat "new" listings as a radar (see `patterns.md`), not just as a place to search a specific query. Smaller/more niche aggregators like Lobste.rs matter precisely because low reach means something can be true and posted there without having "broken out" yet.
- **GitHub / GitLab / Codeberg (discussion side)** — issues and discussions on relevant repos, which often surface real-world usage before it's written up anywhere.
- **Async niche formats** — newsletters (Substack, Buttondown), computational notebooks (Observable, Kaggle Notebooks), and publicly shared Notion-style docs. Structurally distinct from forums/chats: no back-and-forth thread, often single-author, but still deliberately published — worth checking as their own format, not folded into "forums."
- **Legacy/alternative code & mod hosts** — SourceForge (older projects that never migrated to GitHub and don't rank in current searches), Steam Workshop (mods/maps deliberately published by their creators), Itch.io (indie game/software publishing, broader than just mods). Worth checking specifically because mainstream searches skew toward GitHub/current platforms and miss what's parked on these.

**Artifacts / residue**
- **GitHub / GitLab / Codeberg (artifact side)** — awesome-lists, gists, and code search for literal config strings/domains — finding what people actually use, not what they say they use.
- **Raw data dumps** — changelogs, patch notes, API/data dumps (e.g. game data via SteamDB-style tools). Relevant whenever the topic has a technical artifact trail, not just write-ups about it.
- **Technical exhaust logs** — public CI/CD build logs, certificate transparency logs, DNS records — these require more technical handling than the other artifacts here, but qualify whenever the topic is technical enough that infrastructure activity itself is a signal (e.g. a new service standing up, a domain going live before it's announced).
- **Torrent trackers** — rare distributions, datasets, and software that never had an official release channel end up here; nobody wrote it up as content, it's just sitting in a swarm. Check for topics where the thing being searched for is unlikely to have a clean official distribution.
- **Web Archive** — not just a "how did this look before" tool. Its CDX API supports searching indexed content by domain, URL pattern, and file type — useful for surfacing files/pages that no longer exist on the live web but are still gems. Relevant even when nothing "new" is expected: old-but-buried counts as a valid finding.
- **Common Crawl** — a separate, broader open web-crawl index (billions of pages per pass) with its own domain/URL-searchable index. Not a Wayback replacement, a parallel one with different coverage — worth checking when Wayback comes up empty.
- **Archive.today** — no searchable index/API of its own, but ignores robots.txt, so it can hold snapshots Wayback was blocked from capturing. Use as a manual spot-check when a specific URL is blocked elsewhere, not as a search source.

**Registries**
- **Aggregators/registries** — structured, non-social listings maintained by infrastructure rather than opinion: API/provider directories (e.g. OpenRouter's model list), package registries, HuggingFace model/Spaces listings, pricing pages of the services themselves. These are the "not from people" source — check them, they exist. Not limited to AI/ML — apply this same logic to whatever niche the topic is in; the class is defined by "structured reference data," not by subject matter.

## Adding a new channel here
New channels discovered mid-session first go into `source-log.md`, not directly here — this file is the curated, proven checklist; `source-log.md` is the staging area. Promote an entry here once it's shown up as useful more than once.
