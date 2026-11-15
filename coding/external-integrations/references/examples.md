# external-integrations — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Retry scope stays narrow and centralized

**Good:** one root request helper retries on rate limit and transient network errors, logs each retry, and raises when attempts are exhausted — call sites just call it.
**Bad:** a per-call-site `except Exception: retry` that also re-sends after a 400 validation error.
Rationale: only the narrow set of expected external failure modes gets retried, in one place — everything else is a bug that must fail loud, and scattered handlers hide it.

## No pick, no wiring

**Good:** `decision.md` in the topic folder has no filled `user-pick:` — routing back to solution-search instead of wiring anything.
**Bad:** "the pick is missing, so I wired the lib I know best."
Rationale: this skill wires the decided pick, never picks; searching or choosing here is the routing violation the phase gate exists to catch.

## Docs first, not freestyled params

**Good:** starting from `references/telegram-topics.md` and verifying `message_thread_id` + `parse_mode` against current Bot API docs before writing the call.
**Bad:** writing the topic call from memory and iterating five blind variations when it breaks.
Rationale: fiddly integrations break when written from memory — the reference plus current docs is where the specifics live; blind retries are guesswork, not debugging.

## Heartbeat is the mandatory floor

**Good:** the long-running poller pushes to its uptime-kuma monitor on every healthy loop tick, push URL from config.
**Bad:** shipping a `restart: always` service with only Prometheus metrics (opt-in) and no heartbeat.
Rationale: missed ticks make a dead service visible in kuma without reading logs — heartbeat is the mandatory floor; the rest of the observability stack is opt-in.

## External services stay black boxes

**Good:** the bug looks like the tunnel → diagnose up to the boundary, report the evidence, stop.
**Bad:** ssh into the VPS "just to check" — unasked.
Rationale: credentials there may be non-rotatable; a "fix" can lock the user out — the boundary is where the agent's reach stops.

**Good:** a hosted API misbehaves → capture the failing request/response, report, let the user decide whether to touch the vendor side.
**Bad:** poking the vendor's admin panel to "fix it while I'm here".
Rationale: the project adapts to infra, never the reverse — and a unilateral fix on someone else's service is an out-of-scope write.
