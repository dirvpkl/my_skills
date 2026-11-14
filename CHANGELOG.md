# CHANGELOG — collection level

Per-skill history lives in each skill's CHANGELOG.md; this file records
collection-wide passes.

## 2026-11-12/14 — dialog-analysis rework (base 1.8.0)

Owner-driven rework after mining 1351 owner prompts across 49 dialogs
(exports: Desktop\ZCode_dialogs_*.md).

New skills: roi 1.0.1 (stock-gate value scoring), recap (full workplanx +
chat-context retelling), handoff (agent-to-agent context files),
boundaries 1.0.1 (security + sensitive-data memo, split from coding).
Promoted top-level: proxy-egress 1.2.1 (coding+autonomous = always proxy),
git-workflow 1.1.0 (version control for ALL project work).
Deleted: thinking (folded into the «думалка» mega-bundle chord), radar
(method → solution-search references/verb-radar.md), tldr — tombstones in
_graveyard/.
coding 1.22.2: 6 modules left (docker, process-tiers, code-quality,
testing, logging, external-integrations); boundaries/proxy-egress/
git-workflow stay mandatory deps.
Chords v2: 21 rows — «автономно» (risk-class fence), «думалка» mega-bundle
(recap + solution-search + workplanx + spine + roi + busywork; morning
variant recap-first), «на сегодня», «что я забыла?», «добить проект»,
busywork (LBDN = Look Busy Do Nothing), «пиши» = autonomous go-ahead;
cheatsheet generator (scripts/make_cheatsheet.py → Desktop card).
Collection conventions: examples-everywhere (20 files, 64+ good/bad pairs,
base Mode-recognition section), hashtag vocabulary #gem/#wildshot/#slot/
#harvest/#open/#decision, descriptions strict-YAML clean (no `: `),
agent-driven owner-message logging (scripts/log_owner_message.py →
.workplanx/_inbox), skills re-read from disk always (never from memory),
subagent revival before replace.
base 1.8.0: revival rule, examples binding, re-read rule, always-on
workplanx logging, worktree/pre-flight unchanged.
