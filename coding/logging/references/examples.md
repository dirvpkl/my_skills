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

**Good:** debugging an auth failure logs `token_length=47` or a masked form.
**Bad:** logging the full request URL that contains `?token=...` — or printing the Bearer header.
Rationale: a URL with the token in it has already leaked the token; redact to length or mask before any print/log statement.
