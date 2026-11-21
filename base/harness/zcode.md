# zcode — harness nuances (what the tools alone do not tell you)

This file carries the owner-told nuances of the zcode harness — the local
limits, quotas and quirks the agent cannot guess from the tools themselves.
Agents know their tools; they do not know these. When the owner explains
another nuance, it lands here the same turn.

## Agents
- Parallel agent limit: 3 — TOTAL, including the orchestrator session itself
  and every session-dispatched agent (owner ruling 2026-11-19, after a
  10-session dispatch wave was sent at once: «параллельно максимум 3 могут
  работать включая тебя»). While orchestrating, wave size = 2 dispatched;
  wait for a running agent to finish before admitting the next.
- Empirical caveat: parallel background agents have failed one-on-one —
  verify a second agent actually started before planning around it.

## Load and retries
- When the load is high or the concurrency limit is hit — RETRY: wait and
  retry is the correct move, not a fail and not a workaround.
- GUI session-flip (owner-told 2026-11-20): the desktop GUI sometimes flips
  the owner into another session — she may look like she is "working" in a
  session the orchestrator dispatched to, and may manually INTERRUPT that
  run thinking it is the flipped one. A `interrupted` status on a dispatched
  op usually means owner touch, not a crash: confirm with the owner before
  re-dispatching, and don't treat her presence in a session as owner-lock.

## Tokens
- The owner may have bonus tokens that work until 4:00 — or may not.
  When a long run would burn through the quota, ask the owner whether
  bonus tokens apply tonight.

## The rule

Only owner-told or practice-bitten nuances live here — never the generic
tool behavior the agent already knows.
