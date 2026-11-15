---
name: boundaries
description: Rules for secrets, credentials, logs, chat/transcript hygiene, browser profiles, data preservation, and any access outside the project directory — when to ask before touching something, how to handle an exposed credential, and how to keep sensitive data out of chat output. ALWAYS invoke this skill before a task could touch a secret, a credential, log output, chat output, browser session data, a volume or database, or a file outside the project — notes, research, infrastructure and plain conversation count, not only code. NOT for pure in-project work that touches no secrets, logs, or anything outside the project.
version: 1.3.0
---

# boundaries

<!-- v1 - 2026-11-14: promoted out of the coding bundle (was coding/security 1.0.0) and extended with the owner's sensitive-data memo — kept verbatim in references/sensitive-data-memo.md, golden rule promoted to a hard rule here. -->

## General permission rule
If a task requires a secret, credential, or a file outside the project directory, ask the user directly, in plain language, before touching it. Don't infer implicit permission from context/task description — only an explicit "yes" from the user in this conversation counts as permission. Once granted, that permission applies to what was asked about; if scope expands (a different secret, a different external path), ask again.

## Secrets / .env files
- Never read, print, or pass the contents of `.env` or similar secrets files without asking the user directly first and getting an explicit yes.
- This includes indirect reads too (e.g. cat-ing it inside a script, echoing it, dumping it into a log) — same rule applies.
- Never log secrets in code — redact sensitive values before any print/log statement.
- No silent fallback defaults for secrets (`.env.get("key", "fallback")`, `${KEY:-KEY_DEFAULT}`). If a key is missing, fail loudly instead of quietly substituting a placeholder (see `code-quality`'s fail-loud section, the canonical definition).

## Logs
- Never read log files/output without asking first, even for debugging. Ask, wait for permission, then read.

## Browser data
- Browser sessions/cookies/profile dirs (Chrome profile, cookie stores, session tokens, etc.): never read without explicit request from the user in that message.

## Out-of-scope access protocol
Applies whenever a rule above requires user permission (out-of-project files, secrets/.env, logs, browser profile dirs, etc.):
- Ask the user directly and wait for their answer before doing anything — don't proceed "provisionally" while waiting.
- Use the normal tool call (cd / read / terminal) as-is once permission is granted — do NOT route around client-side permission prompts (e.g. reading via a different tool, symlinks, wrapper scripts, subprocess cat). Let the client's own permission dialog handle confirmation too, where applicable.
- If the client denies or the user rejects the prompt, stop and report access was denied — don't retry with a different method.

## Exposed credentials
If a secret/credential gets exposed anywhere during the session (seen in command output, a file, a log, pasted by the user, etc.), flag it: end that response with a short, all-caps line naming which credential was exposed. Do this every time it happens, not just once.

## Data preservation and host integrity
Live in `references/data.md` — read it before touching volumes, databases, hosts, or running tests.

## Chat & transcript hygiene
The memo's golden rule is a hard rule: **anything already in the chat or transcript is compromised.** Not "private, but careful" — compromised. Dialogue can be logged, stored, indexed, so the only question before every output is: "if a stranger reads this, what can they do with it?" The memo lives verbatim in `references/sensitive-data-memo.md`.

- Before showing any command output in chat, print the FORM, not the values — result / code / errors / field presence / lengths, never field values carrying identifiers or tokens. Pipe raw output through a filter first (the memo's curl example). A URL with `?token=...` is a leaked token; Bearer headers count too.
- Never interpolate a secret into a log message or chat text: print a length or a masked form (the memo's `mask()` helper), never the value. Silencing chatty libraries (httpx, http.client, urllib3) is level 1 — a full URL in an httpx log has already leaked a bot token once.
- Files with secrets are checked by script with boolean/length output, never read "to see what's there". The user fills in secret values themselves; the agent never needs to see them. `.env` goes into `.gitignore` before the first commit.
- Docker: `env_file:` in compose is fine (values are substituted, nobody reads the file); `docker logs` is a leak vector — anything a library logged spills out on the first view; after a secret change, restart (re-reads .env silently) rather than rebuild; after a leak, rebuild doesn't help — the secret lived in the old container's stdout. Revoke.
- Leak protocol, in this order: revoke immediately (a dead token in logs is just garbage), issue the new value into the file — not the chat — and restart, figure out what else lived in that same output (another token? card? phone?), only then investigate how it leaked and add a filter. Reversing the order means you forget to revoke.
- Before every "show the output in chat" moment, run the memo's checklist (section 7): token/key/password present? personal data present (phone, card number, name, address)? anything usable even once? filter applied (form, not values)? if it leaks anyway — is it revocable? (a token is, a card number is not).

## Assigned scope only

Work inside the projects named in the task. Anything else — sibling
projects, home directories, host apps, other checkouts — is out of scope
until the user explicitly adds it. Read-only inspection of a sibling to
diagnose (e.g. checking whether a proxy router is up) is allowed;
changing it is not.

## External services are black boxes

If the bug lives in an external service (proxy provider, hosted API,
tunnel, VPS side), do not go there unasked. Diagnose up to the boundary,
report the evidence, stop. Rationale: credentials there may be
non-rotatable, and a "fix" can lock the user out.

## Never-do list (no exceptions without explicit yes)

- `rm -rf`, `docker down -v`, volume prune, `DROP DATABASE`, disk format.
- Host package installs, firewall/network changes, reboot, cron edits.
- Force-push, history rewrites, `git reset --hard` on uncommitted work.
- Committing `.env`, keys, cookies, or chat exports.
- Editing files outside the assigned projects.

## System boundaries
- Don't touch host-machine apps (VLC, Chrome, singbox, etc.). Docker/Python/Node/dev tooling is fine.
- Don't run unbounded searches over huge directories — always scope depth/pattern to avoid flooding the terminal.

## Report
Note any secret/credential exposure flagged during the session, and any out-of-scope access that was requested and whether it was granted or denied.
