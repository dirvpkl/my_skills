---
name: logging
description: Structured logging rules — one format and one correlation ID across services, when a fail-loud raise also needs to be visible, and Telegram forum-topics alerts (critical/info/service, spammy-by-default). This is a base dependency every other skill (code-quality, external-integrations, testing) assumes is already applied whenever code is built or changed — not a separate feature to bolt on later.
version: 1.2.1
---

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-15: added Processor TypeAlias single-source contract, no private-helper + public-wrapper forwarding pair, unused processor params must be _-prefixed. -->
<!-- v1.2 - 2026-09-22: Telegram section aligned with forum-topics + spammy-by-default (was: admin-DM + no-spam); wiring canonical in external-integrations/references/telegram-topics.md. -->
<!-- Continues prior content that lived under a package-wide v3 marker before the coding package moved to per-skill versioning; see coding/CHANGELOG.md. -->

# logging

## Trigger
Writing or reviewing code that logs something, raises/handles errors that should be visible, or when setting up a new service that needs observability. In practice this fires alongside any code write/edit — see the `coding` dispatcher's activation manifest, which is the actual dispatch logic; don't wait to read this file only when something explicitly mentions logging by name.

## This is a base dependency, not a standalone task
`code-quality`, `external-integrations`, and `testing` all assume this skill's rules are already applied whenever something is built or changed — logging isn't a separate feature to add later, it's part of doing the work correctly the first time.

## What fail-loud implies for logging
- A loud failure (per `code-quality`'s fail-loud section, the canonical definition — this file doesn't redefine it) still needs to actually be seen. Raising an exception that dies silently in a container nobody's watching isn't meaningfully different from swallowing it — pair fail-loud with logging that surfaces the failure somewhere a human will notice.
- Structured, consistent logs: what happened, in which service, with enough context to act on it (not just a bare stack trace with no surrounding info).

## What "structured logging" means here (baseline requirements)
- Each log entry is a set of labeled fields (timestamp, level, service name, message, relevant IDs), not a free-text sentence — this makes logs greppable/filterable instead of just readable one at a time.
- One consistent format across all services in the project. If services are in different languages, "consistent" means the same shape/fields, not necessarily the same library — but don't let one service log plain text lines while another logs structured JSON with no plan to reconcile them.
- Every request that flows through multiple services (e.g. Telegram message → API → worker → LLM call) carries one shared request/correlation ID through all of them, so logs from different services about the same request can be tied together. Generate it once at the entry point, pass it through, don't invent a new one per service.
- Don't invent a bespoke logging setup from scratch per service — if the language has a well-established structured-logging library (e.g. `structlog` for Python), default to that rather than hand-rolling JSON formatting. Pick one approach and reuse it across services in the same language.
- Never log secrets — this is already a hard rule in `security`; it applies here too.
- One processor contract. Logging processors are typed once as a shared TypeAlias in the project's contracts module and reused — never re-spell the `(logger, method_name, event_dict)` triple per file (single-source contract per `code-quality`).
- No private-helper + public-wrapper forwarding pair. A processor that only forwards to a same-named helper with no added logic is a `No trivial delegating wrapper` violation — keep one function with the processor signature and inline the logic; don't keep two names for one transformation.
- No dangling processor params. If a processor doesn't use `logger`/`method_name`, name them `_logger`/`_method_name` and document ` # why: structlog Processor protocol` — see `code-quality` `No unused parameters` (`ruff` `ARG001/ARG002` must stay green). Bare `logger: Any` that is never read is not allowed.

## Telegram as a logging/alerting channel
- If the project already has a Telegram bot, use it as a channel for logs/alerts rather than building separate notification infra from scratch — send meaningful events/errors there instead of only writing to a log file nobody checks.
- Forum topics, not one chat and not bare admin DMs: `critical` (crashes, security, needs-human-now), `info` (mandatory operational events — spammy by default, off only on explicit user opt-out), `service` (stats/noise, aggregated). Wiring details (thread IDs, levels, call shape) live in `external-integrations/references/telegram-topics.md` — that file is canonical, this section only states the levels.

## Report
When adding logging to something, note where it logs to (stdout/file/Telegram) and what's covered vs. what's still silent.
