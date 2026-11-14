# Default stack (portrait defaults)

Blessed building blocks. Reuse without re-search — but still record the pick
per verb in `decision.md` (reuse is a decision too). If a verb genuinely
doesn't fit anything below, fall back to full search.

Hard rule: never open the inventoried repos on disk to copy implementation.
Reuse means the same technology + the same pattern, wired fresh from current
docs — not code lifted from a sibling project. Per-repo paths live in
`known-services.md` (a map of what exists); this file is rules. No project
names appear below on purpose.

## serve — HTTP API

- Default: FastAPI behind one shared app factory that gives `/health` for free.
- Pattern: custom lifespan (DB pings, index ensure) passed into the factory;
  never a hand-rolled app per service.

## tasks — background queue

- Default: Celery + Redis via the shared factory (queue per service,
  started-state tracking, result polling, cancel/revoke).
- No beat process in the default stack — scheduled fires live in `schedule`.

## schedule — cron/triggers

- Default: APScheduler (interval/cron, single-instance + coalesce for serial
  ticks). Lightest thing that fires reliably.
- Prefect (server + UI + versioned flows) only iff ≥2 of: more than one
  schedule with distinct params, non-dev operators need UI/audit, fan-out
  above ~10 parallel tasks, long steps needing heartbeats. Below that it's a
  container, a volume, and a port for nothing.
- Custom tick-loop allowed only with injected `sleep`/`rng`/tick-limit and a
  serial-tick guarantee by construction (overlap impossible, not tuned away):
  pure decision core + thin loop, wall-clock never leaks into the core.

## stream — transport (default: NATS)

- Default: NATS JetStream — one light binary covering streams + KV + dedup +
  DLQ. For inter-service contracts and lease-aware flows in new stacks.
- Redis Streams when Redis is already in the stack for cache, sessions, or
  locks — one container covering four needs beats two containers.
- RabbitMQ: keep where it already runs (task results + vhosts), never the
  default for new stacks — heaviest ops of the three.

## logging — one shape everywhere

- structlog JSON + one correlation ID propagated across services + service
  name, from a single shared factory.
- No per-service logger copies, no bare `print()` in recurring code.

## health — two layers, both mandatory for long-running

- `/health` on every service (free via factory; a 3-line manual route if no
  factory). A service nobody can probe is a service nobody can supervise.
- Heartbeat push per long-running service (uptime-kuma class monitor, push URL
  from config, tick on the healthy loop). Missing tick = dead, no log reading.
- Prometheus / log centers / webhook hubs: opt-in by load, not default.

## alerter — Telegram forum topics

- One forum supergroup, three threads by severity: `critical` (needs a human
  now), `info` (mandatory and spammy by default: started/finished/posted),
  `service` (stats, retries, noise — aggregated, still on unless opted out).
- Pattern: rate-limited per key, never-raises sender (alerting must not crash
  the worker), thread IDs from config, never hardcoded.
- Canonical wiring lives in `external-integrations/references/telegram-topics.md`
  — yes, the TG-topics example is added there; copy the call shape, not any
  IDs or texts.
- Hole: no shared alerter lib yet — scattered notify-copies and hand-rolled
  Bot-API POSTs are the replace-candidates for it.

## store — db rule + files ladder

- Joins/constraints/leases → postgres (relations the queries actually join).
  Schemaless docs/vault/dedupe → mongo. Rule of thumb: if the query joins,
  it's postgres; if it stores, it's mongo.
- Files, hot → cold: shared volume mount for hot; S3-compatible storage
  (minio class) for warm blobs; telegram-drive class (`tgdrive`/`teldrive`)
  for cold archives nobody reads — cheap, slow, perfect. Never
  container-local paths without a mount (data dies with the container).

## queue/cache — infra rots fastest, always re-verify

- Defaults above are a starting point, not truth: infra versions and compose
  patterns rot faster than any other layer. For every infra verb the agent
  must confirm current docs (official repo/compose examples) in this session —
  memory of versions, flags, and image tags is not evidence.
- Cache/locks/sessions: one Redis-family container (redis/dragonfly) covering
  cache + locks + leadership + streams. Don't add a second cache system.
- Alertmanager/Prometheus: only when numeric metrics + thresholds exist to
  route. Until then logging + TG send covers everything (events already
  emitted). Rule: no metrics → no router; metrics → add it, keep TG as the
  last-mile sender.

## post — delivery

- Socials: Postiz (multi-network hub, not per-network hand code).
- Telegram: a bot lib per case (`aiogram` / `python-telegram-bot` /
  `telethon` for user-session actions) — never hand-rolled HTTP to the Bot API.
- Media render: `ffmpeg` via a wrapper lib, not raw subprocess string parsing
  duplicated per service.

## inference — CPU-only, always

- Every model runs on CPU. No GPU images, no CUDA layers, no device requests —
  ever. If a model can't run on CPU, it's the wrong model, not a reason to
  touch a GPU.
- Pattern: small/quantized builds first (tiny variants cover speech/music/
  silence-class tasks outright), ONNX/CPU-native runtimes over PyTorch stacks
  where the accuracy gap doesn't justify the weight, batch calls over
  one-by-one prediction loops.
- Embeddings: a dedicated embedding server (infinity-class: OpenAI-compatible
  API, CPU-first, batching built in) as a sidecar — never inline model loads
  per worker, never one text per request when the server batches.

## libs — standard utilities, never hand-rolled

- Retry/backoff: tenacity (async-ready, stop/wait/retry predicates). Any hand
  `for attempt in range(N)` + `sleep` loop is a replace-candidate on sight.
- Caching: cachetools (TTL/LRU) instead of hand dicts with timestamps.
- Structures: dataclasses for internal shapes; pydantic at boundaries (API
  request/response models, config validation). Medium+ project rule:
  cross-module data travels as typed models (passable as arguments, storable
  as structures), never bare dicts. Pydantic sits naturally under an API
  server.
- Config: dynaconf-class layered settings (defaults → files → env) instead of
  hand env parsing. Optional until config outgrows one flat file.
- Relational access: SQLAlchemy (async where the stack is async) for the
  relational DB — migrations + typed queries instead of raw SQL strings
  scattered per module.

## Known holes (not defaults — fix list)

Moved to `references/holes.md` — this file holds blessed rules only.
