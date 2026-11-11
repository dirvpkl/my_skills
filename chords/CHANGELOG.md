# Changelog

All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job (that belongs in a dedicated references/ file — see references/anti-patterns.md in skill-scaffolder for why these should stay separate).

## 1.0.0 — 2026-11-11
- Initial release: personal shortcut bindings. `references/bindings.md` holds the phrase → target table (kinds: `skill` / `bundle` / `action`); the table is user-edited data — row edits never bump the version and never pass a gate.
- Resolution is same-turn and step-aside: load the mapped target as if the user had typed /name; unknown binding = one-line "not bound", never a guessed target.
- Initial table carries this session's real phrases (thinking, fresh-eyes, loop, mission, researcher, one action row); RU and EN aliases in the same rows.
- Near-miss counterexamples: actual music chord questions are answered directly; explicit /commands and skill names always win over a binding.
- `planned` registers the parked `trigger-log` module (fold observed trigger misses back into bindings/descriptions).
