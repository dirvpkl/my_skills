---
name: external-integrations
description: Wiring rules for an already-chosen integration — centralized retry, docs-first connection, Telegram forum-topics alerts (critical/info/service), uptime-kuma heartbeat, portrait defaults. Never searches for alternatives or picks stacks (that's solution-search via the topic folder). Use when connecting code to something external.
version: 1.6.0
---

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-13: added the test-seam exception for a thin client-boundary wrapper (one instance per project, no business logic inside). -->
<!-- v1.2 - 2026-09-22: less-code ladder (code is last resort), decompose-into-verbs + per-subtask OSS search with evidence, dumb-constitutional gate loop (scripts/gate.py), Telegram forum topics with 3 levels (references/telegram-topics.md is canonical example), uptime-kuma heartbeat requirement. -->
<!-- v1.2.1 - 2026-09-22: spam policy correction — info/service spammy by default, off only on explicit user opt-out, never throttled on agent initiative. -->
<!-- v1.3 - 2026-09-22: narrowed to wiring-only — search/decompose/proposals moved to solution-search; this skill requires decision.md user-pick and never picks stacks. -->
<!-- v1.3.1 - 2026-09-22: ladder reworded as verification lens (was: search order); trigger points at dispatcher manifest. -->
<!-- v1.4 - 2026-09-23: removed gate.py (grep-checks deleted as useless) — verification is workplanx phase gate + fresh-eyes; rules live in this file and references/. -->
<!-- v1.5 - 2026-09-23: portrait defaults moved in from solution-search (default-stack, known-services, holes, scan-protocol) — concrete knowledge lives on the implementation side, brainstorm keeps method only. -->
<!-- v1.6 - 2026-09-26: decoupling — own copy of the ladder rank names removed (`solution-search` is the single vocabulary), Telegram section reduced to wiring only (levels + spam policy live in `logging`), verification points at `fresh-eyes` conformance mode. No wiring rule changed. -->
<!-- Continues prior content that lived under a package-wide v3 marker before the coding package moved to per-skill versioning; see coding/CHANGELOG.md. -->

# external-integrations

## Trigger
Wiring an already-decided external integration (a `decision.md` user-pick exists in the topic folder). Not for internal function calls, never for searching or picking stacks. Bundled per the `coding` dispatcher's activation manifest — that manifest is the dispatch logic, this Trigger line is scope only.

## Base dependency: logging
Every retry attempt gets logged (per the `logging` skill) — at minimum a WARNING when a retry kicks in, and an ERROR when retries are exhausted and it fails loud. Without this, rate limits and transient failures happen invisibly until they pile up into a real outage nobody saw coming. This isn't optional instrumentation, it's part of what "centralized handling" means below.

## Centralized handling, not scattered try/except
- Retries are for a narrow, specific set of failure modes: rate limits and transient network/connectivity errors (timeouts, connection resets). Nothing else gets retried by default — a validation error, a non-rate-limit 4xx, a bad response shape, etc. are not retry candidates, they're bugs or fail-loud cases.
- Once retries are exhausted (max attempts hit), fail loud (per `code-quality`'s fail-loud section, which is the canonical definition) — raise, don't swallow, don't fall back to a placeholder. Retry logic delays the failure to give a transient problem a chance to resolve itself; it doesn't replace fail-loud, it postpones it.
- Known, expected failure modes in that narrow set get handled once, in a root-level helper for that integration — not with a try/except wherever the call happens to be made.
- Example shape: a single request helper that itself knows how to retry on rate limit / transient network errors, with retry parameters (max attempts, backoff) coming from config, not hardcoded (see `code-quality`'s no-hardcoding section) — call sites just call the helper and don't think about retries at all. Once its retries run out, it raises.
- If an established client library for that integration already implements proper retry/backoff handling for these cases, use that instead of writing it yourself — check before building.
- This isn't the same thing as swallowing unknown errors (see `code-quality`'s fail-loud section) — only this narrow set of expected, external failure modes gets retried; everything else still fails loud immediately, no retry involved.

## Verify the decided level, don't hand-roll (less-code ladder)

Code is the last resort, not the default. The pick arrives from
`solution-search`; its ladder is the single vocabulary for this — this file
doesn't keep a second copy of the rank names, because two lists drift and
then nothing can be checked against anything.

- The wired solution must sit at the decided level, not below it. A
  hand-rolled subprocess wrapper where the decision says project/component is
  a mismatch failure, not a shortcut.
- Don't hardcode a specific stack choice in advance — the stack arrives from
  `solution-search` via the topic folder. If the decision is genuinely missing
  or ambiguous, stop and route back to search — don't silently pick here
  (see below).

## Portrait defaults (implementation side)

Concrete portrait knowledge lives here, not in brainstorm:
- `references/default-stack.md` — blessed defaults per need. A verb matching
  a default is reuse: record the pick in the topic folder's `decision.md`,
  skip the web for that verb.
- `references/known-services.md` — per-machine registry shell (rebuild locally
  per `references/scan-protocol.md`); `references/holes.md` — repair backlog.
- `references/telegram-topics.md` — canonical topic wiring example.

## No search here — solution-search owns it

- This skill never searches for alternatives and never picks stacks. The pick
  arrives via the topic folder (`decision.md` with a filled `user-pick:`,
  see `workplanx`). No pick = no wiring. Searching here instead of reusing
  the decision is a routing violation.
- The ladder below is a verification lens, not a search order: the wired
  solution must match the decided ladder level. Mismatch (decided lib, wired
  hand-rolled client) fails the gate.

## Verification (no separate gate script)

This skill ships no checker of its own — the rules above are verified by:
- `workplanx` phase gate (`plan_gate.py`) on the topic folder before code;
- `fresh-eyes` review after code (topic folder + diff, clean context) — mode
  `conformance` is the one that catches a wiring job that sat below its
  decided ladder level.
What used to be script checks now lives as plain rules in this file and in
`references/telegram-topics.md` — read them, don't grep around them.

## Telegram forum topics — wiring only

The three levels (`critical` / `info` / `service`) and the spam policy are
defined once, in `logging`. This file only owns how a thread ID gets wired and
called, and the canonical copy-paste example is
`references/telegram-topics.md`. Don't restate the level rules here — that's
how two lists end up disagreeing about what's mandatory.

- Thread routing is by `message_thread_id`, markdown via `parse_mode`. Don't
  re-derive this from memory — start from `references/telegram-topics.md`, put
  thread IDs in config (not code), adapt text only.
- Telegram sending itself goes through the established bot lib with centralized
  retry (see below) — never a hand-rolled `requests.post` to `api.telegram.org`.

## Uptime-kuma heartbeat (long-running services)

- Any long-running service (`restart: always/unless-stopped`, poller, parser,
  poster) gets a heartbeat push to a local uptime-kuma (simple self-hosted
  pinger, one docker container, push + http monitors, web UI).
- One push URL per service from config, pushed on healthy loop tick. Missed
  ticks = dead service, visible in kuma without reading logs.
- Prometheus metrics / log centers / webhook centers are opt-in by need
  (long-running + load, or user asked) — heartbeat is the mandatory floor,
  not the full observability stack.

## Test seam at the client boundary
- A thin wrapper around an external client, kept specifically so tests can substitute it, is a legitimate exception to "no wrapper for its own sake" — the alternative (hand-rolled async fakes per test) is more expensive and more fragile. Keep it under two conditions: exactly one instance per project (it doesn't multiply per module), and it sits only at the boundary between our code and the external client — no business logic lives inside it.

## Proposing options without prescribing a stack
- Proposals live in `solution-search`, not here. If the topic folder has no
  filled `user-pick:`, stop and route back — don't present alternatives and
  don't build. This skill wires the pick, nothing else.

## Check docs and examples before implementing
- Before writing integration code for something with known-fiddly behavior, search for current documentation and real working examples rather than guessing from general knowledge or trial-and-error in the codebase.
- Telegram topics break constantly when written from memory — always start from
  `references/telegram-topics.md`, then verify `message_thread_id` + `parse_mode`
  against current Bot API docs. Don't freestyle the params.
- If the first approach doesn't work, don't just retry variations blindly — go back to docs/search for what changed or what was missed, rather than iterating five times by trial and error.

## Report
Note which integrations were touched, where the centralized retry/handling lives for each, and whether behavior was confirmed against current docs or just assumed. Plus, every time:
- topic folder + `decision.md` pick this wiring implements (no pick = no wiring);
- telegram topics wired (which threads, where IDs live) and heartbeat URL wired (which monitor);
- docs confirmed (current Bot API / lib docs checked this session) vs assumed.
