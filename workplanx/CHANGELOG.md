# Changelog

## 1.4.0 — 2026-09-26
- New file `log.md` in the topic folder — one section per skill: what it did, what it found, what it left out. The skill claimed "other skills log to the folder, not to chat" while owning no file where such a log could land; `gate.log` is the gate's own run history and never was that file.
- `plugins/manifest.json` gains a top-level `dependencies` array (other skills in the collection that load alongside this one). `modules` answers "what's inside this skill", `dependencies` answers "which other skills come with it" — documented in SKILL.md so the two aren't conflated. This skill's own list is empty: it's the root, everything else depends on it.
- The fresh-eyes finale is no longer described here — it moved to the `fresh-eyes` skill (mode `conformance` + the subagent-triage canon). This skill keeps the folder, the gate, and the log.
- `layout` (1.1.0 → 1.2.0): `log.md` documented, and `gate.log` explicitly marked as not a substitute.

## 1.3.0 — 2026-09-26
Vocabulary aligned with solution-search 1.8.0 — the gate was the last place in the chain that still spoke only in code terms.
- `layout` (1.1.0 → 1.2.0): zero-candidate path decided as `<own-make>`; "no code before this line" → "no implementation starts"; explicit phase list `plan → search → decision → build` with `code` marked as legacy alias; ladder levels documented as domain-neutral.
- `plan-gate` (1.2.0 → 1.3.0): phase `code` renamed `build` (`code` still accepted and mapped, so existing topic folders keep validating); ladder regex accepts `<open-project>` / `<component>` / `<own-make>` alongside legacy `oss` / `library` / `own-code`; gate messages de-coded ("nothing starts before evidence", "decide <own-make>").
- The gate is now the single binding enforcement point for "no implementation before a user pick" — SKILL.md step 2 says so explicitly instead of stating the rule as agent discipline.

## 1.2.0 — 2026-09-22
- `layout` (1.0.0 → 1.1.0): plan.md proceeding is not approval; user-pick transcribed verbatim, never invented; zero-candidate path documented.
- `plan-gate` (1.1.0 → 1.2.0): zero URLs + query log = WARN (own-code path) instead of FAIL.
- Fresh-eyes triage done in the open (accept/reject per finding in report).

All notable changes to this skill are logged here — not runtime data (that lives in topic folders).

## 1.1.0 — 2026-09-22
- Removed hashed deny-list from plan_gate.py (gameable, teaches avoidance) — gate is structural-only now.
- Added fresh-eyes finale: clean-context review of topic folder + diff as the semantic layer.

## 1.0.0 — 2026-09-22
- Initial version: topic-folder router (plan/search/decision/gate), structural gate with hashed deny-list.
