# Changelog

## 1.9.0 — 2026-09-26
- `dependencies: ["workplanx"]` declared in the manifest. This skill's output only exists as files in a workplanx topic folder — that was already true, but the link was prose in SKILL.md, which is the list-that-rots pattern.
- The ladder rank names in this file are now the collection's single vocabulary; `coding/external-integrations` deleted its own copy (1.6.0) rather than keeping a second list that could drift.

## 1.8.0 — 2026-09-26
De-coded: the skill claimed any domain while its method was software-only.
- `method` (1.3.0 → 1.4.0): ladder is now domain-neutral — `<oss-project>` → `<open-project>`, `<library>` → `<component>`, `<own-code>` → `<own-make>`; "hand-rolled I/O"/"maintained code" tradeoffs → "doing it from scratch"/"what you carry afterwards"; "wiring belongs to the implementation skill" → "doing belongs to whatever acts on the decision". Registry/lift-implementation anti-pattern generalized (the registry itself moved to the executing side in 1.7.0).
- SKILL.md: description and Trigger no longer mention code, migrations or configs; the `external-integrations` route-out is gone (that skill no longer receives anything from here). Duplicated "decompose into verbs" step collapsed into one.
- New section "Where 'nothing gets made yet' is actually enforced" — points at the `workplanx` build gate and the `coding` dispatcher, since a prose rule inside this file is not a gate.
- `scripts/validate_manifest.py` added — `plugins/README.md` referenced a script the skill did not ship.

## 1.7.0 — 2026-09-23
- Brainstorm generalized: works for any domain (code, video, anything) — trigger covers "how to / what to use / find technique".
- Moved out to coding/external-integrations: default-stack, known-services, holes, scan-protocol (concrete portrait knowledge lives on the implementation side). This skill keeps method only.

## 1.6.1 — 2026-09-22
- Alias: brainstorm. Description + header now name it so triggering by "brainstorm" works; researcher links here.

## 1.6.0 — 2026-09-22
- `default-stack` (1.3.0 → 1.4.0): libs section — tenacity (retry), cachetools (TTL/LRU), dataclasses/pydantic (typed models at medium+, pydantic under API server), dynaconf-class (layered config, optional), SQLAlchemy (relational access). Hand-rolled loops/dicts/env-parsing/raw-SQL are replace-candidates.

## 1.5.0 — 2026-09-22
- `known-services` (1.0.0 → 1.1.0): portability purge — all machine-local rows removed; registry is a shell with regen note, patterns live in default-stack. Skills must work on any machine.

## 1.4.0 — 2026-09-22
- `default-stack` (1.2.0 → 1.3.0): inference section (CPU-only always, infinity-class embedding sidecar); holes moved to `references/holes.md`.
- `method` (1.2.0 → 1.3.0): zero-candidate escape hatch (queries + no candidates = legitimate own-code decision); SKILL output now names topic-folder files; disk-lifting ban.
- New modules: `holes` + `scan-protocol` (split out of default-stack/known-services per fresh-eyes).

## 1.3.0 — 2026-09-22
- `default-stack` (1.1.0 → 1.2.0): de-concretized — all project names removed, entries describe pattern shape + why; blessed product names kept (they are the answers). Hard rule: never open inventoried repos on disk to copy implementation.
- `method` (1.1.0 → 1.2.0): disk-lifting ban added to anti-patterns.

## 1.2.0 — 2026-09-22
- `method` (1.0.0 → 1.1.0): serendipity capture — up to 3 off-track finds with URLs in `search.md`, never promoted into the decision unasked.
- `default-stack` (1.0.0 → 1.1.0): store split into db rule (joins → postgres, docs → mongo) + files ladder (mount → S3 → telegram-drive cold); infra-verify rule (infra rots fastest, confirm docs per session); Alertmanager only with metrics, TG send until then.

All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job.

## 1.1.0 — 2026-09-22
- Added `references/default-stack.md`: blessed portrait defaults per need (serve/tasks/schedule/NATS-default stream/logging/health/alerter/store/post) + known holes. Step 1 now checks defaults first — matching verb = reuse, not search.

## 1.0.0 — 2026-09-22
- Initial version: pre-code search split out of external-integrations. Placeholders-only core, concrete inventory in references/known-services.md.
