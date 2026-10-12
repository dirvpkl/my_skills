# Changelog

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
