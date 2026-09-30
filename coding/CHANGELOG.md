## [1.14.1] - 2026-09-30
- manifest: sync the proxy-egress module entry (1.1.0) with its own SKILL.md frontmatter (1.1.1), which scripts/validate.py was failing on. The package version moves so the change is deployable: same version plus differing files is a conflict deploy.py refuses.

## [1.14.0] - 2026-09-29
- coding/proxy-egress 1.1.0: Node.js env-proxy flag, TCP forwarder sidecar pattern, local-mode file download via shared volume, dummy-proxy test setup

## [1.13.3] - 2026-09-29
- Route proxy/egress tasks to proxy-egress (default set + explicit route); cross-link with external-integrations

## [1.13.2] - 2026-09-29
- coding/proxy-egress 1.0.2: Added references/telegram-sidecar.md: the Bot API image that can carry a proxy, the entrypoint splitting PROXY_URL into TDLib flags, volume ownership, and keeping the internal client-to-sidecar hop direct.

## [1.13.1] - 2026-09-29
- coding/proxy-egress 1.0.1: Added the silent-fallbacks grep catalog, the failure-signature table, and the ask-where-the-proxy-lives rule.

# CHANGELOG — coding package

History of changes to the skill package itself (structure, dispatch logic, sub-skill additions/removals). Not a log of project code changes (that's git history in whatever project is being worked on) and not a log of runtime data (this package doesn't produce any).

## 1.13.0 — 2026-09-26
Two new siblings close the scale gap: until now the package had a dispatcher but nothing between "one task" and "start from scratch".
- New `loop` 1.0.0 — bounded autonomous iteration. Owns the iteration cap, the verify command and the stop signals. `process-tiers` still decides the ceremony of the first iteration; `loop` decides how many iterations there are.
- New `mission` 1.0.0 — goal decomposed into a board of cards, worked by fresh subagents, judged at the end. Sits above `loop`: a card that needs repetition hands off to it.
- Activation manifest gains two entry points: "a goal too big for one pass" → `mission`; "repeat one unit until a condition holds" → `loop`. Both are named as routes out, not as things to re-describe here.
- `dependencies` extended to `[workplanx, solution-search, fresh-eyes, loop, mission]`.
- No sub-skill changed. Note the scale ladder is now explicit and worth keeping: `solution-search` picks the approach → `workplanx` gates whether work may start → `mission` decides what the units are → `loop` runs one unit repeatedly → this package implements a unit → `fresh-eyes` judges the result.

## 1.12.0 — 2026-09-26
Decoupling pass: one owner per responsibility, cross-skill links declared instead of prose.
- `dependencies: ["workplanx", "solution-search", "fresh-eyes"]` added to the manifest — the activation manifest's cross-skill routes are now a machine-readable fact, not something a reader has to infer from prose.
- `code-quality` (1.4.0 → 1.5.0): fresh-eyes section removed — the procedure moved to the new `fresh-eyes` skill, `references/fresh-eyes-checklist.md` deleted. The "flag security holes proactively" rule stayed behind, since this file is its only owner. Tier rules removed from Working order (`process-tiers` owns them). No code rule changed.
- `testing` (1.1.1 → 1.2.0): the UX pass is now explicitly the artifact a `fresh-eyes` quality-mode judge receives; report section notes the review verdict isn't this file's to give. No testing rule changed.
- `external-integrations` (1.5.0 → 1.6.0): own copy of the ladder rank names deleted — `solution-search` is the single vocabulary, so a wiring job and a search job can't disagree about what "component level" means. Telegram section cut to wiring only; the three levels and the spam policy live in `logging`.
- `process-tiers`: now the only place tier rules and the two delegation axes are stated; its references to the review point at `fresh-eyes` instead of `code-quality`.
- New skill `fresh-eyes` 1.0.0 (mode `quality`, mode `conformance`, subagent-triage canon).
- Companions outside the package: `workplanx` 1.3.0 → 1.4.0 (added `log.md`, the file that makes "skills log to the folder" true), `researcher` 1.2.0 → 1.3.0, `solution-search` 1.8.0 → 1.9.0.

## 1.11.0 — 2026-09-26
The "no implementation before the user picked" rule moved out of prose and into a check.
- Activation manifest: the pre-decision bullet now names the enforcement point — `solution-search` writes only `search.md` + `decision.md`, this package loads only after `workplanx/scripts/plan_gate.py --phase build` is green on a transcribed `user-pick:`. Previously the rule was stated in three places (this file, `workplanx` SKILL.md, `solution-search`) and verified in none.
- Companions outside this package: `solution-search` 1.7.0 → 1.8.0 (ladder made domain-neutral), `workplanx` 1.2.0 → 1.3.0 (phase `code` → `build`, neutral vocabulary, gate accepts both spellings).
- No sub-skill file changed; dispatcher version bump only.

## 1.10.0 — 2026-09-23
- `external-integrations` (1.4.0 → 1.5.0): portrait defaults moved in from solution-search (`references/default-stack.md`, `known-services.md`, `holes.md`, `scan-protocol.md`) — concrete knowledge lives on the implementation side; brainstorm keeps method only.

## 1.9.0 — 2026-09-23
- `external-integrations` (1.3.1 → 1.4.0): `scripts/gate.py` deleted (grep-checks removed as useless) — verification is the `workplanx` phase gate + fresh-eyes; rules live in the SKILL file and `references/` only.

## 1.8.0 — 2026-09-22
Portability purge (skills must work on any machine, e.g. laptop):
- `code-quality` (1.3.1 → 1.4.0): all project-local paths/names (`services/gate/*`, `contracts/*`, `handlers/*`, `thewarmer-*`, `paster-*`, `sing-box`) generalized to placeholders. Rules unchanged.
- `logging` (1.2.0 → 1.2.1): processor-contract paths generalized (same rules).
- Kept: public product/API names (Bot API, linters) and history comments (logs, not instructions).

## 1.7.0 — 2026-09-22
Fresh-eyes alignment pass (two clean-context reviewers):
- `logging` (1.1.0 → 1.2.0): Telegram section now forum-topics + spammy-by-default, wiring canonical in external-integrations (was: admin-DM + no-spam — contradicted dispatcher).
- `external-integrations` (1.3.0 → 1.3.1): ladder reworded as verification lens (was: search order — contradicted wiring-only split); trigger points at dispatcher manifest; gate.py docstring fixed.
- Trigger one-liners now defer to the manifest everywhere (testing 1.1.1, code-quality 1.3.1, process-tiers 1.1.1 + solution-search route) instead of partial bundle lists.
- Parked (not fixed): code-quality core still embeds project-local paths/strings as canonical examples (purge into references/ later); Prefect/Alertmanager thresholds have no verifier (accepted — reviewer layer covers).

## 1.6.0 — 2026-09-22
- `external-integrations` (1.2.1 → 1.3.0): narrowed to wiring-only — search/decompose/proposals moved to `solution-search`; requires `decision.md` user-pick from the `workplanx` topic folder, never picks stacks.
- Dispatcher routing: pre-code search routes out to `solution-search` + `workplanx`; coding loads only after a user pick.
- Package bumped to `1.6.0`.

## 1.5.1 — 2026-09-22
- `external-integrations` (1.2.0 → 1.2.1): spam policy correction — info/service spammy by default, off only on explicit user opt-out.
- Package bumped to `1.5.1`.

## 1.5.0 — 2026-09-22
Content additions to one existing sub-skill; no dispatch-logic change beyond version bump.
- `external-integrations` (1.1.0 → 1.2.0): added — less-code ladder (SaaS > OSS project > lib > template > own code, code is last resort); decompose-into-verbs + per-subtask abstract OSS search with URL evidence; dumb-constitutional gate loop (`scripts/gate.py --strict`, P1-P5); Telegram forum topics with 3 levels (critical/info-mandatory/service, `references/telegram-topics.md` canonical, `message_thread_id` + `parse_mode`, IDs from config); uptime-kuma heartbeat floor for long-running services (Prometheus/log-centers opt-in).
- Root `SKILL.md` and `plugins/manifest.json` package versions bumped to `1.5.0`; skill-index one-liners updated.
- Note: `plugins/manifest.json` package_version was stale at `1.3.0` vs root `1.4.0`; fixed in this bump.
Content additions to one existing sub-skill; no dispatch-logic change beyond version bump.
- `testing` (1.0.0 → 1.1.0): added — fair comparisons, one variable at a time (an A/B or benchmark proves nothing unless both sides share harness, data and every step except the one under test; design so a negative result is possible and visible, don't ship on a tie).
- Root `SKILL.md` and `plugins/manifest.json` package versions bumped to `1.4.0`; skill-index one-liners updated.

## 1.3.0 — 2026-09-15
Content additions to one existing sub-skill; no dispatch-logic change beyond version bump.
- `code-quality` (1.2.0 → 1.3.0): added — no single-use private helpers (`_busy_detail` in `services/gate/server.py:87` used once in `100`, `_ReportedFlood` synthetic exception used once — inline or replace with typed model); expanded single-source contracts to explicitly cover domain `Exception` classes and `BaseModel`/`TypedDict`/`Enum` schemas (`_ReportedFlood`, `LeaseRequest`/`ReportRequest`/`LeaseBusy` belong in `contracts/`, not `services/gate/server.py`); no exception-to-bool adapters (`_is_alive(healthcheck, proxy) -> bool` in `services/gate/proxies.py:31` with `except Exception: return False` hides real bugs — keep raise-vs-pass contract and handle `try/except` at caller or use `assert`); no duplicated `SERVICE_NAME` literals (each service's name lives once in its `logutil.py`/`config`, `handlers/warmup/_common.py:36` duplicating `workers/executor/logutil.py:7` `"thewarmer-executor-worker"` violates `one-place config`); no untyped `dict[str, Any]` domain payloads (use `BaseModel`/`TypedDict` from `contracts`, not bare dict builder); extended `No trivial delegating wrappers` examples to `content_length` in `handlers/warmup/_common.py:65` (`return len(x)`).
- Root `SKILL.md` and `plugins/manifest.json` package versions bumped to `1.3.0`; skill-index one-liners updated.

## 1.2.0 — 2026-09-15
Content additions to two existing sub-skills; no dispatch-logic change beyond version bump.
- `code-quality` (1.1.0 → 1.2.0): added — no trivial delegating wrappers (`return other_fn(args)` / `return builtin(args)` / `return CONST[k]` with no added value; encapsulating private state like `ContextVar` is exempt, forwarding between same-domain public helpers like `_strip_secrets` → `drop_secrets` `contracts/logging_conf.py:55-81` or `len` → `content_length` is banned); no unused parameters (every param must be used; protocol-forced unused must be `_`-prefixed and typed via shared `Processor` TypeAlias from `contracts/types.py`; `ruff` `ARG001/ARG002` must stay green).
- `logging` (1.0.0 → 1.1.0): added — single `Processor: TypeAlias = Callable[[Any, str, dict[str, Any]], dict[str, Any]]` in `contracts/types.py` (single-source contract); no private-helper + public-wrapper forwarding pair for processors; no dangling `logger`/`method_name` params — must be `_logger`/`_method_name` with ` # why: structlog Processor protocol` when unused.
- Root `SKILL.md` and `plugins/manifest.json` package versions bumped to `1.2.0`; skill-index one-liners updated.

## 1.1.0 — 2026-09-13
Content additions to four existing sub-skills; no dispatch-logic or structural changes.
- `code-quality` (1.0.0 → 1.1.0): added — constant-vs-function distinction; no pointless import aliases; no wrapper function around a single condition; single-source-of-truth requirement for contracts shared between two pieces of code; no sync/async adapter layers (honest async signatures throughout); no catching an exception just to re-raise it unchanged; no re-wrapping another error except when the original is mute or this is the designated root boundary; unwired stubs must be a loud `NotImplementedError` naming the owner and the gap, not silent `pass`/`TODO`/`return None`; validate a value once at the boundary, trust it after; a default argument matching the real prod value is hidden config; every config value lives in exactly one place; all imports at the top of the file with a cost comment on heavy ones; no handwritten `isinstance` type checks in business logic (mypy/schema only); concrete types for dependencies, `Any` only as a justified last resort.
- `external-integrations` (1.0.0 → 1.1.0): added the test-seam exception — a thin external-client wrapper kept for test substitution is fine, capped at one instance per project, boundary-only, no business logic inside.
- `docker` (1.0.0 → 1.1.0): added the compose environment-variable rule — always `${VAR:?message}`, never a bare `${VAR}`.
- `process-tiers` (1.0.0 → 1.1.0): added — decide and state where shared code lives before splitting work across parallel sub-agents; ambiguity here is a stop-and-ask, not something each sub-agent resolves by writing its own copy.
- Root `SKILL.md`'s skill-index one-liners updated to reflect the above; dispatcher/activation-manifest logic itself untouched.
- Not incorporated: a submitted note that the agent may skip running some skills "at its own discretion" — this directly conflicts with the dispatcher's activation manifest ("all of them, every time relevant, no partial subset") and `process-tiers`' "no unexpected behavior, ever" rule. Flagged to the user instead of silently weakening either rule; see chat.

## 1.0.0 — 2026-09-06
Restructured from a single flat `<!-- vN -->`-versioned package into the skill-scaffolder plugin layout:
- Root `SKILL.md` reduced to a pure dispatcher: activation manifest + skill index + versioning rules, no embedded process rules.
- Extracted four new sub-skills from what used to be inline prose in root `SKILL.md`: `git-workflow`, `security`, `docker`, `process-tiers`. These sit alongside the four pre-existing sub-skills (`code-quality`, `testing`, `logging`, `external-integrations`) as equal modules, not as dispatcher content.
- Added `plugins/manifest.json` — the discovery file listing all 8 sub-skills (path, version, type). Root `SKILL.md` now points at the manifest instead of hardcoding the sub-skill list.
- Moved off the single unified `<!-- vN - date -->` marker shared across every file. Each sub-skill now has its own `version` (frontmatter) and `VERSION` file, bumped independently. The package as a whole still has one `VERSION` (root) and `package_version` (manifest), bumped on any sub-skill change, so "is everything in sync" stays checkable in one place without forcing a lockstep bump on every unrelated file.
- Rewrote `scripts/check_versions.sh`: no longer enforces one version across all files; instead validates each module's frontmatter version against the manifest and reports (not errors on) drift between a sub-skill's version and the last package-version bump.
- Fixed cross-references that pointed at "root AGENTS.md" for rules that no longer live there (secrets → `security`, docker ports → `docker`, decide-vs-ask/tiers/delegation/conflict-resolution → `process-tiers`).
- Restored a "Verification" section in `code-quality` (fresh-command-output rule, baseline comparison, evidence-backed bug fixes) that `testing` referenced but that had been dropped when the old root file was split.

Prior history (pre-1.0.0, package-wide `<!-- v1 -->` through `<!-- v3 -->`) is not reconstructed here — see git history if needed.
