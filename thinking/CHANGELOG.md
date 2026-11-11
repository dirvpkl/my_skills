# Changelog

All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job (that belongs in a dedicated references/ file — see references/anti-patterns.md in skill-scaffolder for why these should stay separate).

## 1.1.0 — 2026-11-11
- Owner trigger family added to the description: "подумай", "можешь поискать чето", "надо чтобы ты…".
- Bare opinion requests ("оцени мои проектики") explicitly routed OUT: answer with a spine stance, no skill loads — neither this skill nor `fresh-eyes`.
- Near-miss counterexamples updated accordingly.

## 1.0.0 — 2026-11-11
- Initial release: dispatcher for the think-first bundle — `solution-search` + `workplanx` + `spine` load together as one obligation.
- Two lanes: idea talk (spine stance, no folder, no gate) and real pre-decision (topic folder + transcribed `user-pick:` gate before anything is built).
- Near-miss counterexamples included: "оцени мои проектики" is idea talk, not `fresh-eyes`; judging finished work is `fresh-eyes`, executing a decided approach is `coding`.
- No modules by design — the bundle members are top-level sibling skills; they are declared in `plugins/manifest.json` → `dependencies`, never hand-listed in prose.
