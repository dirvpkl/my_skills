# Changelog

## [3.4.3] - 2026-11-19
- 3.4.2 REVERTED (owner ruling: «обязанности вотчера это вотчить»): the
  one-shot widening was wrong — the watcher watches (recurring ticks);
  a bare one-shot task execution is not its job. The autonomous-boss
  framing dropped; the merge direction (watchdog + metawatcher as one
  watching layer) recorded in the parked metawatcher design.

## [3.4.2] - 2026-11-18
- desc: one-shot audits and reminders are in-scope (the "to set up a
  recurring" framing repelled direct audit/remind requests — exam miss).

## [3.4.1] - 2026-11-17
- examples.md: every case now carries >=2 Good/Bad pairs (the collection convention) — one teaching couplet added per single-pair section.

## [3.4.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- `## Trigger` section removed; the owner's "watcher" word moved into the
  intro next to Profiles.
- Examples brought to two pairs per case.

## [3.3.2] - 2026-11-12
- validate_manifest.py: missing-runtime.toml diagnostic and non-table [skills] guard


## [3.3.1] - 2026-11-12
- validate_manifest.py: dependencies_runtime resolution and module type check


## [3.3.0] - 2026-11-11
- Trigger contract sweep: description rewritten as a use-when / not-for / sibling contract with literal user phrases; rules and body unchanged.

## [3.2.0] - 2026-11-08
- collection-audit aggregates un-executed harvest blocks; on-demand harvest of topic-less sessions


## [3.1.0] - 2026-11-08
- collection-audit profile: walks topics/skills tree/git log, proposes one patch set, one-shot by default


## [3.0.0] - 2026-11-07
- universal watcher: profile contracts (read/send/cadence/never), sessions profile preserved, new skills-reminder matcher profile (the 30-min tick)


## [1.1.2] - 2026-10-19
- Trigger wording: terminal preferred, schedule supported


## [1.1.1] - 2026-10-19
- checks.md: fix duplicated step number in the check order (1,3,3 -> 1,2,3)


## [1.1.0] - 2026-10-16
- status-blind ticks: never read session.status, stall only on identical (msg_id, ledger_tail), GREEN leaves tracking same tick


## [1.0.11] - 2026-10-13
- Hourly re-anchor: restate owes line to WORKING sessions idle 60+ min


## [1.0.10] - 2026-10-13
- Message-fetch discipline: ids, timestamps, stale rules.


## [1.0.9] - 2026-10-13
- Ban absence-proofs; event-based predicates only.


## [1.0.8] - 2026-10-12
- Message discipline: stale verdicts vs live logs.


## [1.0.7] - 2026-10-12
- Heartbeat cadence and fast BLOCKED reports.


## [1.0.6] - 2026-10-12
- Delete the schedule task when supervision ends.


## [1.0.5] - 2026-10-12
- Hard pings by default; mid-work ping is safe.


## [1.0.4] - 2026-10-11
- Hang detection and nudge escalation ladder.


## [1.0.3] - 2026-10-11
- Terse report mode for exhausted users.


## [1.0.2] - 2026-10-11
- Move tracking registry out of references into state/.


## [1.0.1] - 2026-10-11
- Watchdog ticks run as loop external-wait rounds.


All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job (that belongs in a dedicated references/ file — see references/anti-patterns.md in skill-scaffolder for why these should stay separate).

## 1.0.0 — 2026-10-11
- Initial version: independent supervision tick over tracked OpenChamber worker sessions (GREEN/WORKING/STALLED/BLOCKED), one nudge per stall, tick log per session.
