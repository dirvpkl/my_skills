# trigger-log — observed trigger misses, folded back into descriptions

Append-only data file (the researcher/source-log pattern). One row per
observed miss: date, the user's utterance, what fired (or nothing), what
should have fired, and the resolution. What belongs here: real misses observed
in live sessions, with enough context to reproduce. What does NOT belong here:
hypothetical edge cases, routing rules (those live in the skills), or session
logs. Fold a proven fix back into the skill's description, then mark the row
resolved — the log is the queue, the descriptions are the fix.

| date | utterance | fired | should | resolution |
|---|---|---|---|---|
| 2026-11-11 | "оцени мои проектики" | nothing (agent hand-rolled generic Explore agents) | spine (bare opinion turn) | owner ruling + sweep: spine 1.3.0 claims bare opinion turns; fresh-eyes NOT changed; thinking 1.1.0 carries the "подумай / можешь поискать чето" family — resolved |
| 2026-11-11 | (session start, no utterance) base never loaded | nothing | base (always loaded by design) | harness-level fix: user-scope `~/.zcode/AGENTS.md` says "invoke Skill(base) first"; base description states the exemption explicitly — resolved |
