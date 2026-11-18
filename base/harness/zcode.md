# zcode — harness nuances (what the tools alone do not tell you)

This file carries the owner-told nuances of the zcode harness — the local
limits, quotas and quirks the agent cannot guess from the tools themselves.
Agents know their tools; they do not know these. When the owner explains
another nuance, it lands here the same turn.

## Agents
- Parallel agent limit: 3.
- Empirical caveat: parallel background agents have failed one-on-one —
  verify a second agent actually started before planning around it.

## Load and retries
- When the load is high or the concurrency limit is hit — RETRY: wait and
  retry is the correct move, not a fail and not a workaround.

## Tokens
- The owner may have bonus tokens that work until 4:00 — or may not.
  When a long run would burn through the quota, ask the owner whether
  bonus tokens apply tonight.

## The rule

Only owner-told or practice-bitten nuances live here — never the generic
tool behavior the agent already knows.
