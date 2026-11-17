# Changelog

## [1.4.0] - 2026-11-18
- Framing corrected (owner ruling): workplanx is NOT the resource base —
  it and the harness DB are ADDITIONAL sources, extra info; the REAL base
  is the current context the agent holds. Section renamed accordingly.

## [1.3.0] - 2026-11-18
- "workplanx is the resource base" section (owner rulings): USE workplanx
  and all its resources — hashtag meanings are looked up in workplanx's
  own docs, never restated here; compare dates (old records are stale);
  bind the records to the CURRENT context — the handoff's value is the
  current-context binding, not a copy of durable records anyone can read.
- Harness mention: the harness may compress sessions on its own — ask it
  directly for session data (where the DB, schema, what to read).
- Owner declined the comprehension-receipt wildshot — the skill stays
  simple; the receiving flow keeps verify-and-report only.

## [1.2.0] - 2026-11-17
- Description trimmed to ~400 chars; the contract is unchanged
  (what it is + ALWAYS invoke + NOT for).

## [1.1.0] - 2026-11-15
- Per-skill review round. Trigger-restatement block removed ("Owner requests
  that summon this file...") — the description and chords bindings own the
  summon phrases.
- Collect gained the owner-message inbox (`_inbox/<date>.md`) as the first
  source — verbatim rulings, named first-class for handoff by base, workplanx
  and README but never read here.
- New section: Receiving a handoff — the consumer side was undefined (read,
  verify against the checklist, report gaps, continue).
- examples.md: +2 cases (collect from records; receiving side verifies) — 6
  cases × 2 pairs.

## [1.0.0] - 2026-11-15
- Modular shape applied per skill-scaffolder (owner directive): manifest, VERSION, CHANGELOG, own validator; content unchanged.
