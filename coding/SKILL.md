---
name: coding
description: Dispatcher for the coding skill package — routes to the right sub-skills (git-workflow, security, docker, process-tiers, code-quality, testing, logging, external-integrations, proxy-egress) for a given task. Use when writing, editing, or reviewing code.
version: 1.16.0
---

# coding (dispatcher)

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-13: sub-skill content updates only (code-quality, external-integrations, docker, process-tiers); dispatcher logic itself unchanged, see CHANGELOG.md. -->
<!-- v1.2 - 2026-09-15: code-quality 1.1.0->1.2.0 + logging 1.0.0->1.1.0; dispatcher version bump only. -->
<!-- v1.3 - 2026-09-15: code-quality 1.2.0->1.3.0; dispatcher version bump only. -->
<!-- v1.4 - 2026-09-22: testing 1.0.0->1.1.0; dispatcher version bump only. -->
<!-- v1.5 - 2026-09-22: external-integrations 1.1.0->1.2.0; dispatcher version bump only. -->
<!-- v1.5.1 - 2026-09-22: external-integrations 1.2.0->1.2.1 (spam-by-default); dispatcher version bump only. -->
<!-- v1.6 - 2026-09-22: external-integrations 1.2.1->1.3.0 (wiring-only split); routing now sends pre-code search to solution-search + workplanx. -->
<!-- v1.7 - 2026-09-22: fresh-eyes alignment — logging 1.1.0->1.2.0 (forum-topics + spammy-by-default), external 1.3.0->1.3.1 (ladder as verification lens), triggers now point at manifest (testing 1.1.1, code-quality 1.3.1, process-tiers 1.1.1 + solution-search route). -->
<!-- v1.8 - 2026-09-22: portability purge — code-quality 1.3.1->1.4.0 + logging 1.2.0->1.2.1: all project-local paths/names generalized to placeholders; skills carry no machine-local references. -->
<!-- v1.9 - 2026-09-23: external-integrations 1.3.1->1.4.0 (gate.py deleted; verification is workplanx gate + fresh-eyes). -->
<!-- v1.10 - 2026-09-23: external-integrations 1.4.0->1.5.0 (portrait defaults moved in from solution-search); solution-search 1.6.1->1.7.0 (method only, any-domain trigger). -->
<!-- v1.11 - 2026-09-26: pre-decision route made mechanical — the user-pick gate is now workplanx 1.3.0's `build` phase check, not prose in this file or in solution-search; solution-search 1.7.0->1.8.0 (domain-neutral ladder) + workplanx 1.2.0->1.3.0 (phase `code`->`build`, neutral vocabulary). Dispatcher version bump + one manifest bullet; no sub-skill file changed. -->
<!-- v1.12 - 2026-09-26: decoupling — new `dependencies: [workplanx, solution-search, fresh-eyes]` in the manifest makes the cross-skill links a declared fact instead of prose. code-quality 1.4.0->1.5.0 (fresh-eyes section out, tiers out, security flag kept), testing 1.1.1->1.2.0 (UX pass marked as the judge's input), external-integrations 1.5.0->1.6.0 (ladder copy out, Telegram reduced to wiring). -->
<!-- v1.13 - 2026-09-26: new siblings `loop` 1.0.0 (bounded autonomous iteration, mechanical verdict) and `mission` 1.0.0 (goal -> board of cards -> subagents) added to dependencies; activation manifest gains the two entry points that route to them. No sub-skill changed. -->

This file is a router, not a rulebook. It doesn't contain process/quality/security rules itself — those live in the sub-skills listed below, each self-contained. This file's only job is: given a task, which sub-skills load, and how do skill-package versions stay in sync.

## plugins/manifest.json
The authoritative list of every sub-skill in this package — path, current version, and whether it's `core` or `plugin`, plus the `dependencies` this package loads alongside. Check the manifest for what's currently active instead of trusting a hardcoded list here; if this file and the manifest ever disagree on what exists, the manifest wins.

## Activation manifest — what loads together
Skills aren't read one at a time in isolation. When a trigger below fires, the whole listed set activates together, in the same task, not sequentially-if-remembered:
- **New feature / integration / replacement (pre-decision)** → route out to `solution-search` (+ `workplanx` topic folder) first. Searching inside coding is a routing violation. The handoff back in is mechanical, not a judgement call: `solution-search` writes only `search.md` + `decision.md`, and this package loads only after `workplanx/scripts/plan_gate.py --phase build` comes back green on a transcribed `user-pick:`. That gate is the single enforcement point for "no implementation before the user picked" — it lives in `workplanx` (1.3.0), not as prose in either skill, so skipping `solution-search` doesn't skip the check.
- **A goal too big for one pass** ("build the whole thing", "migrate this service") → `mission` first, not this package. `mission` decomposes the goal into cards and drives subagents; a card that needs repetition hands off to `loop`. This package is what a single card's implementation loads. Don't start a multi-session goal by loading this package and hoping.
- **One unit of work repeated until a condition holds** ("until the tests pass", "re-check your work 40 times", run unattended) → `loop`. It owns the iteration cap, the verify command and the stop signals. `process-tiers` still decides how much ceremony the *first* iteration gets; `loop` decides how many there are.
- **Any code write/edit** (new or existing) → `git-workflow` + `security` + `docker` (if Docker config is touched) + `process-tiers` + `code-quality` + `logging` + `testing` + `proxy-egress`. All of them, every time relevant, no partial subset — this is not a set of separate optional reads, it's one combined obligation. (Weight scales per `process-tiers`' "Skill weight by task size".)
- **Task involves outbound proxy/egress routing** (PROXY_URL/HTTP_PROXY, "through the proxy", NO_PROXY, egress audit) → `proxy-egress` drives. If the proxy service connection itself is a decided external integration, `external-integrations` loads alongside it (retry/heartbeat/topics live there, not in `proxy-egress`).
- **Wiring an already-decided external integration** → adds `external-integrations` (wiring-only: retry, docs-first, topics, heartbeat) to the set above, plus `proxy-egress` when the wiring touches outbound routing. It never searches or picks stacks — the pick arrives via the topic folder.
- **Judging finished work** → `fresh-eyes`, both modes when the task came from a plan. Not a sub-skill of this package, and not a thing to re-describe here.
- Don't treat a skill's own "Trigger" line as the only signal to read it — this manifest is the actual dispatch logic; a skill's Trigger section describes its scope once activated, not when to activate it.

## Skill versioning
- Every sub-skill has its own `version` in its frontmatter and its own `VERSION` file, bumped independently as that skill's rules change.
- This package also has one `VERSION` at the root (and `package_version` in `plugins/manifest.json`) — bump it whenever *any* sub-skill's meaning changes (not for typo fixes), so the whole package has one place that says "everything here is in sync as of this state." Log every bump in `CHANGELOG.md`.
- When editing a sub-skill file, state in the report which sub-skill version was set, and whether the package version was bumped too, with a one-line reason.
- If a skill file is loaded mid-task and its content looks stale relative to what the codebase is actually doing (e.g. the skill still describes a pattern the project moved away from), flag the mismatch to the user instead of silently following the stale rule or silently ignoring it.
- `scripts/check_versions.sh` checks that every registered skill has a version marker, that its frontmatter version matches what `plugins/manifest.json` says, and reports (not errors on) any skill whose version is newer than the last package-version bump — run it after editing any skill file, not just when asked.

## Skill index
The actual rules live in sibling skill folders — read the relevant `SKILL.md` before acting, not just when something explicitly asks for it by name (see the activation manifest above, which is the real dispatch logic):
- `git-workflow/SKILL.md` — commit discipline, branching, merge gating, .gitignore hygiene, dependency-upgrade caution.
- `security/SKILL.md` — secrets/.env, logs, browser profile data, out-of-project access, exposed-credential handling.
- `docker/SKILL.md` — port-publishing defaults, internal-only networking, and required (`${VAR:?...}`) compose env vars for compose/docker run.
- `process-tiers/SKILL.md` — decide-vs-ask, task-size tiers, sub-agent delegation (incl. shared-code location decided before parallel work), conflict-resolution worked examples, reporting shape. The only place tier rules and the two delegation axes are stated.
- `code-quality/SKILL.md` — architecture (service separation, no god-files, no hardcoding), coding principles (DRY/KISS/naming, no pointless aliases, no trivial delegating wrappers, no single-use helpers, typed domain payloads, single-source contracts incl. Exceptions/BaseModels, no duplicated SERVICE_NAME), fail-loud error handling (no recatch-to-rethrow, no error re-wrapping except mute-error/root-boundary, no exception-to-bool adapters, loud NotImplementedError for stubs, validate-once-at-boundary), import discipline (top-only, cost-commented), typing (no handwritten isinstance checks, concrete types over Any, no unused parameters with _-prefix + shared TypeAlias), lint/format/type-check order, proactive security flagging. Applies to any code work (new or edit) or refactor. The code checklist lives in `fresh-eyes`, not here.
- `testing/SKILL.md` — verifying a feature actually works beyond the default test suite: coverage gaps, UX-level pass from the real entry point, environment-vs-code failure distinction, fair comparisons. Applies after implementing/changing a feature. Its UX pass is the artifact a `fresh-eyes` quality-mode judge receives.
- `external-integrations/SKILL.md` — wiring-only for a decided integration (centralized retry, docs-first, Telegram topics wiring, uptime-kuma heartbeat, portrait defaults). Never searches or picks stacks — the pick arrives via the `workplanx` topic folder from `solution-search`. Applies when connecting code to something external.
- `proxy-egress/SKILL.md` — mandatory outbound proxy with no silent direct fallbacks: per-client-library behavior, fallback hunting with grep patterns, live verification from inside a container. Asks where the proxy lives, never hardcodes it. Loads by default with the set above; drives proxy/egress tasks (see the activation manifest).
- `logging/SKILL.md` — structured logging, one Processor TypeAlias and one request ID across services, no private-helper + public-wrapper forwarding processors, no dangling processor params, Telegram forum-topics levels and spam policy (spammy-by-default; wiring canonical in external-integrations). This isn't optional/standalone: `code-quality`, `external-integrations`, and `testing` all assume logging is wired in per this skill whenever something is built or changed — treat it as a base dependency, not a separate task to remember later.
