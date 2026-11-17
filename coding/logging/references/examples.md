# logging — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## A raise nobody sees is a swallow

**Good:** retries exhausted → the helper raises AND the root boundary logs an ERROR with the request ID, service name, and the integration that failed.
**Bad:** a raise that dies silently in a container nobody watches — or `except Exception: pass` in the worker loop.
Rationale: fail loud means raised AND seen; pairing the raise with a log a human will notice is what makes it loud instead of merely fatal.

## One correlation ID, minted once

**Good:** the entry point generates `request_id`, and the bot, API, and worker logs all carry that same ID.
**Bad:** each service invents its own request ID at its first log line.
Rationale: the shared ID is what ties logs from different services about the same request together — per-service IDs structurally un-tie them.

## Structured fields, not prose

**Good:** `logger.info("message_sent", request_id=rid, chat_id=cid, svc="bot")` in the same shape as every other service.
**Bad:** `print(f"sent message to chat {cid}!")` — a free-text line one service emits while another logs JSON.
Rationale: labeled fields make logs greppable and filterable; a prose line can only be read one at a time and breaks the one-format rule.

## Secrets never reach a log

**Good:** debugging an auth failure logs the request line with the query stripped — `GET api.example.com/v1/users status=401` — and `token_length=47`.
**Bad:** logging the full request URL that contains `?token=...`, or printing the Bearer header.
Rationale: log everything that matters (method, host, path, status, duration) — and redact only the credential-bearing parts; a URL with the token in it has already leaked the token.

**Good:** a body field named `password`/`token`/`secret` is masked in the log record; the rest of the payload stays readable.
**Bad:** dumping the request body "for debugging" with the password field intact.
Rationale: the body is log material, the credential inside it is not — mask the field, keep the shape.

## Library request loggers are log writers

**Good:** httpx/httpcore loggers are pinned to `WARNING` (or routed through a redaction filter) — since httpx 0.24.0 the `INFO` line prints the full URL including `?api_key=...` (the `Authorization` header itself is not printed at INFO).
**Bad:** leaving library loggers at `DEBUG`/`INFO` because "it's just request logging" — the query string is the credential.
Rationale: libraries log the request line with its query; the redaction has to cover them, or they must be silenced.

**Good:** `http.client` debug output is kept off — `HTTPConnection.debuglevel = 1` writes to stdout and bypasses logging filters entirely; when a lower-level trace is needed, it goes through the same redaction path.
**Bad:** enabling `debuglevel` "just for one run" and getting headers and bodies in plain stdout.
Rationale: a filter on the handler cannot see output that never passes through logging; the lowest-level switch needs its own control.

## One masking helper, applied at the boundary

**Good:** one `mask(value) -> first 4 chars + length` helper sits in the logging setup and every record passes through it — the call sites log normally.
**Bad:** each call site formats its own "safe" version, so one forgotten `f"{token}"` reopens the leak.
Rationale: redaction is a property of the log sink, not of the author's memory — one boundary covers every writer, including the library loggers.
