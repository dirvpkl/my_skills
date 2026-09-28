---
name: code-quality
description: Architecture, coding principles, and error-handling rules for any code write or edit — new features, refactors, and cleanup requests. Covers service separation (no god-files, no bundling worker logic into API services), no-hardcoding, DRY/KISS, fail-loud error handling, import/typing discipline, honest async signatures, single-source contracts, lint/format/type-check order, and proactive security flagging. Use this whenever code is being written or changed, not only when explicitly asked to "clean up" or "refactor."
version: 1.5.0
---

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-13: added constant-vs-function, no-pointless-alias, no-single-condition-wrapper, single-source shared contracts, no sync/async adapters, no-recatch-to-rethrow, no re-wrapping others' errors (except mute-error/root-boundary), loud NotImplementedError for unwired stubs, validate-once-at-boundary, hidden-config default args, one-place config values, all-imports-at-top with cost comments, no handwritten isinstance type checks (mypy/schema only), concrete typing with justified Any. -->
<!-- v1.2 - 2026-09-15: added no-trivial-delegating-wrapper, no-unused-parameters (protocol-required _-prefix + shared TypeAlias). -->
<!-- v1.3 - 2026-09-15: added no-single-use-helpers, typed domain payloads, expanded single-source contracts to Exceptions/BaseModels, no exception-to-bool adapters, no duplicated SERVICE_NAME literals. -->
<!-- v1.5 - 2026-09-26: decoupling — fresh-eyes review section removed (moved to the `fresh-eyes` skill, checklist file deleted, security rule kept here as the only owner), tier rules removed from Working order (`process-tiers` owns them). Rules themselves unchanged. -->
<!-- Continues prior content that lived under a package-wide v3 marker before the coding package moved to per-skill versioning; see coding/CHANGELOG.md. -->

# code-quality

## Trigger
Any code work — new feature, edit to existing code — or an explicit request to "clean up / refactor / de-stink" something. Bundled per the `coding` dispatcher's activation manifest (full set, not a subset) — see that manifest for the dispatch logic, not this Trigger line in isolation.

## Base dependency: logging
Anything built or changed under this skill assumes the `logging` skill is already wired in — that's not a separate follow-up task, it's part of doing the work correctly the first time.

## Project context
- We work with Docker. Services run as local Docker containers.
- No public APIs — everything goes through an internal Docker router/network. Never have code reach out to a public API directly; route through the internal service.
- Write all code, comments, commit messages, and docs in English, always — no exceptions for this project.

## Service separation (architecture)
- Basic worker/server concepts apply: a heavy or resource-hungry component (an LLM, a GPU-bound inference engine, anything CUDA-dependent) gets its own container, separate from lightweight request-handling code.
- Inference/engine code and the API layer serving it are not the same process. A FastAPI (or similar) app and a Celery worker (or similar task queue) run as separate services, not bundled into one process just because it's convenient.
- Services respect each other's boundaries. No worker logic running inside the FastAPI service, no FastAPI-side code doing a worker's job — each service does its own job, not another service's, except in specific cases discussed with the user first.
- No god-methods and no god-files: if a function/module is doing "everything," split it along its actual responsibilities — this connects directly to KISS and single-responsibility below.
- Don't be shy about adding lightweight infra (e.g. Redis) as its own container/Dockerfile when the task genuinely calls for it — propose it, don't route around the need with a hack instead.
- Be more conservative specifically about I/O-heavy state (databases): don't reach for a new DB/persistent store casually — that's a bigger commitment than a cache or broker, flag it and discuss before adding one.
- Naming convention for services/containers: `<project>-<service>-<role>` (e.g. `<proj>-api-web`, `<proj>-ml-worker`) — not generic names like `app`, `main`, `web1`. Keep it consistent across a project once picked.

## Project structure
- Real folder structure, always — even for a small standalone script (e.g. a little proxy-rotation script). No dumping everything in one flat file/folder just because the thing is small. A tiny script's structure can be minimal, but it's still structure (e.g. separate the entry point from config/helpers), not one god-file doing config parsing, logic, and I/O all inline.
- This is the same principle as no-god-files/no-god-functions above, applied at the project layout level, not just within a single file.

## Imports
- All imports live at the top of the file, no exceptions — never inside a function, never deferred for "lazy optimization." Whoever imports a module pays its full startup cost up front and can see that cost in the file header, instead of it being hidden until some function happens to run.
- A heavy import (noticeable startup cost) gets a comment next to it stating what it pulls in and roughly what it costs to import, so the cost is visible without profiling.

## Typing
- No handwritten type checks in code. A type is declared via annotation and checked exactly once — statically via mypy, or at the boundary via a schema (e.g. pydantic). A bare `isinstance` → `raise` in business logic is not allowed; that job belongs to mypy and the boundary schema, not runtime code.
- Dependencies are annotated with concrete types imported from the library that defines them. `Any` is a last resort for when the type is genuinely unknowable until runtime — and even then it needs a comment saying why.
- No unused parameters. Every declared parameter must be used in the body. If a framework protocol forces a param you don't need (e.g. a logging processor receives `logger, method_name` but only uses `event_dict`), prefix the unused ones `_logger, _method_name` and type the callable via the project's shared processor TypeAlias (single-source contract) — never leave a bare `logger: Any` that looks alive but is dead code. Unused-argument lint (`ruff` `ARG001`/`ARG002` or equivalent) must stay green.
- No untyped domain payloads. Structured domain data (error details, API responses, lease details) must be a `BaseModel`/`TypedDict`/`dataclass` from the project's shared contracts module, not a bare `dict[str, Any]` built by a helper. A single-use function that builds an untyped dict for one call site violates this — return a typed model or inline the literal at the single raise site.

## No hardcoding
- No hardcoded values anywhere: no baked-in default arguments standing in for real config, no magic constants sitting in a file. If a value can plausibly change between environments/runs, it belongs in config.
- One config, not several: don't split into `config-1`/`config-2` or multiple ad-hoc config files/modules within a project. All non-secret config values live in a single place; secrets live in `.env` as usual (see `security`).
- Exceptions are discussed with the user case by case, not assumed. One clear exception: dataclasses/models describing a request shape (e.g. an API request schema) are not "config" and don't need to be pulled out.
- This rule covers retry parameters too (max attempts, backoff) — see `external-integrations`' centralized-handling section, which is the same no-hardcoding principle applied specifically to retry logic. Don't treat retry config as a special case exempt from this section.
- A default argument that happens to match the real production value is hidden config — it's a config value that just isn't labeled as one. Move the value into config; the function signature only references it from there.
- Every config value lives in exactly one place. The same value repeated in a second file/module is a bug even when the two copies currently agree — they will eventually drift, silently.
- Service identity strings (e.g. `SERVICE_NAME = "<proj>-<role>-svc"`) live once per service in its own logging/config module and are imported — never re-declared as a literal in another module. Duplicate literals across two modules, or scattered string copies of the same name, violate this; import from the owning module instead.

## Principles
- No legacy: TODOs/FIXMEs, stub code, dead code, `as unknown`-style workarounds — remove, don't preserve. Rewrite unclear logic instead of wrapping it in a patch.
- DRY: duplicated helpers get pulled into shared core code, not copy-pasted.
- KISS: prefer the simplest design that solves the actual problem — no speculative abstraction, no premature generalization, no extra layers "just in case."
- Favor clear composition over deep inheritance; keep classes/functions doing one thing.
- Naming: names must reflect what they actually do. Misleading names get renamed, including in tests.
- A function with no arguments and no logic that always returns the same thing is a constant — write it as a constant, not a function.
- No pointless aliasing: re-exporting or renaming an imported name for no reason (same value, same meaning, now two spellings of one thing) makes the codebase harder to grep and adds nothing. Use the name from its source directly; delete the alias.
- No wrapper function around a single condition. A one-condition check is written inline at the point where the decision is made — it doesn't get its own function until there's actual logic inside that can't be read in a second.
- No trivial delegating wrappers. A function whose body is only `return other_fn(args)` / `return builtin(args)` / `return CONST[key]` / `return len(x)` with no branching, validation, added context or error enrichment must not exist — call the target directly. Encapsulation of private state (e.g. a `ContextVar` accessor wrapping a `.set()` call) is exempt; forwarding between two same-domain public helpers with no added value is not. Two names for one transformation violate `No pointless aliasing` and `KISS` and make grep harder.
- No single-use private helpers. A `def _helper(...)` called in exactly one place and only building a literal/dict must be inlined at the call site or replaced by a typed model. A helper is justified only when it is recursive, shared by ≥2 call sites, encapsulates private state, or is a test seam — single-use dict builders are not.
- Contracts shared between two pieces of code (the shape of a function, what a message contains, what codes exist) are defined in exactly one place in code (a type, schema, or constant), and both sides reference it — never let each side describe the same shape independently in its own words. Independent descriptions drift silently while the code keeps running on the mismatch. This includes domain `Exception` classes, `BaseModel`/`TypedDict` schemas and `Enum`/`TypeAlias` definitions: they belong in the project's shared contracts module, not in service-local files. A service-local module owns only its own wiring, not the domain types it wires.
- No sync/async adapters. Production code is async throughout, and tests are async too (async-pytest is already in place) — no bridging layer that lets a function "accept either." A signature always states honestly what it returns: a coroutine means the caller awaits it, a value means a value. A function designed to "accept whatever, sort it out inside" doesn't get written.

## Error handling — fail loud
This is the canonical definition of "fail loud" — `external-integrations` and `logging` both reference this section rather than redefining it; if either seems to say something different, this section wins.
- No defensive try/except on every line "just in case." Only catch an exception when there's a real, specific recovery action to take.
- If something can't be done correctly (missing config, invalid input, an unexpected state), let it fail loudly — raise/throw, don't swallow it, don't return a silent fallback or a placeholder value.
- This applies in production too, not just dev: a loud failure that surfaces a real problem is strictly better than a quiet fallback that hides one. Don't "fix" this by adding a broad catch-all.
- No silent defaults/fallbacks standing in for missing/invalid data (see `security`'s secrets rule for the .env-specific case — this is the general version of the same principle).
- This is about swallowing errors, not about handling known, expected failure modes of external things (rate limits, transient network errors, etc.) — see the `external-integrations` skill for how those should be handled (centrally, via retry, not scattered try/except). A raised exception also needs to be *seen*, not just raised — see `logging`'s "What fail-loud implies for logging" for that half.
- Never catch an exception just to re-raise the same thing. Catching is only justified when it adds information that wasn't there — extra context in the message, a different exception type the caller actually needs — or when there's a real recovery action. A `try/except` whose body just does `raise` (or raises the identical exception) is noise; delete it and let the original propagate.
- Don't guard against impossible types with a catch. If the type system (or the schema at the boundary) already rules a case out, a defensive `except` for it is dead code pretending to be safety.
- Re-wrapping someone else's error is not allowed except in two cases: the original error is mute (says nothing about what happened — an opaque `ffmpeg` failure, for example) or this is the one designated root boundary for that integration (a single top-level handler beyond which the caller has no visibility, like a request going out through a bot API). Everywhere else, let the original error propagate as-is — `JSONDecodeError` already states the line and the reason; wrapping it just adds another layer to unwrap for no new information.
- An unwired seam (a piece of a feature that isn't connected yet) is a loud `NotImplementedError` naming who owns finishing it, what's missing, and why it can't silently continue. Silent `pass`/`TODO`/`return None` stand-ins are not allowed — every such stub is tied to a real tracked task to wire it up, not left indefinite.
- A value is validated once, at the point it crosses into the system (e.g. reading env/config at startup). Past that point, it's trusted — don't re-validate the same value again deeper in the call chain "just in case."
- No exception-to-bool adapters. Don't wrap a raise-vs-pass contract into a boolean via `try: pred(x) except Exception: return False; return True`. If the hook's contract is "raise means dead", keep it raise-vs-pass and let the caller handle the `try/except` (or use `assert`/explicit result type) — don't hide it behind a predicate helper with a blind `except Exception: return False`. A blind `except Exception: return False` swallows real bugs and violates `fail loud`; narrow the caught type or remove the shim.

## Verification
- Any claim that something works, passes, or is fixed must be backed by fresh command output from this session — never state a result without having just run the command and seen it.
- If in doubt about whether a change caused a regression, compare against baseline: `git stash`, re-run the check, `git stash pop`, compare results.
- If a bug is found along the way (even during an unrelated refactor), fix it and back the fix with evidence — a repro case or a test — not just a claim that it's fixed.

## Baseline (before refactoring)
- Capture the "before" state: typecheck + test + lint/format --check.
- Compare results against this baseline afterward instead of eyeballing it.
- Skip this for trivial-tier edits (see `process-tiers`' "Skill weight by task size") — a rename or comment fix doesn't need a baseline capture.

## Working order
- How much ceremony a task gets is decided by `process-tiers` (tiers, delegation axes) — this file doesn't restate those rules, it says what to do once a tier is chosen. The "did it actually work" half is `testing`.
- Small to large: packages/modules → services → god-files last.
- Don't touch unrelated dirty files along the way — only refactor what's in scope for the task.
- Big-task plan file: bite-sized tasks, each with exact files (create/modify/test), interfaces (consumes/produces — exact names and types), and verify steps with real commands. No placeholders: no TBD/TODO, no "add validation" without code, no "same as Task N", no undefined names.
- For new code (not refactoring existing code): TDD cycle — red test → fix → green test → commit.

## Formatters
- Files touched in this task: apply `black` / `ruff --fix` (or equivalent) immediately, no need to ask — note what was fixed in the report.
- Bulk formatting across unrelated files / whole repo (`prettier --write .`, etc.) — ask first.

## Docker / compose specifics
- Heavy dependencies (e.g. CUDA) go into the Dockerfile's build/cache layers properly, so rebuilds don't re-download/re-install them every time — don't just dump them in without thinking about layer caching.
- Never expose ports to the host in compose files — this is already a hard rule in `docker`; it applies here too when writing or editing service definitions.

## Checks after changes (in order)
Format first, then lint:
1. `uvx black --check`, `uvx ruff format --check` (format checks)
2. `uvx ruff check`, `uvx isort --check-only`, `uvx pyflakes` (lint checks)
3. `uv run mypy`, `uv run pytest` (type-check, then tests)
- Don't skip failing tests — investigate the cause.
- For larger changes, run these checks via a sub-agent so the main context stays clean (routine delegation per `process-tiers` — no need to ask, it only checks and reports).
- `scripts/run_checks.sh` wraps this exact sequence (format → lint → typecheck → test) for Python projects — use it instead of running each command by hand so the order is never accidentally scrambled.
- These are a floor, not the whole picture — see the `testing` skill for the UX-level pass that goes beyond them.

## Fresh-eyes review
- Judging finished work is the `fresh-eyes` skill, and only that skill — how the review runs, which checklist the judge gets, and how findings are triaged all live there. This file owns the rules the judge checks against, not the act of checking.
- Security, though, stays here and here only: if a potential vulnerability is spotted while working (an endpoint or bot command anyone can hit with no auth/rate-limiting, unsanitized input reaching a shell/DB call), flag it to the user proactively, even if it's outside the current task's scope. Don't fix it unasked, don't stay quiet about it either — surface it and let the user decide. When this surfaces through a `fresh-eyes` review, the main agent is the one who relays it.

## Report
Short: what changed, before/after numbers for lint and tests, fresh-eyes findings (if run, after main-agent triage), any security concerns flagged, what was left untouched and why.
