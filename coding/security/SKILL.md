---
name: security
description: Rules for secrets, credentials, logs, browser profiles, and any access outside the project directory — when to ask before touching something, and how to handle an exposed credential. Use whenever a task could touch a secret, a file outside the project, log output, or browser session data, not only when the user explicitly says "security."
version: 1.0.0
---

# security

<!-- v1 - 2026-09-06 -->

## Trigger
Any code task that could touch secrets, credentials, logs, browser profile data, or files outside the project directory. Bundled by the `coding` dispatcher on every code write/edit — see its activation manifest.

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

## System boundaries
- Don't touch host-machine apps (VLC, Chrome, singbox, etc.). Docker/Python/Node/dev tooling is fine.
- Don't run unbounded searches over huge directories — always scope depth/pattern to avoid flooding the terminal.
- Don't touch files outside the project directory unless the user explicitly asks in that message.

## Report
Note any secret/credential exposure flagged during the session, and any out-of-scope access that was requested and whether it was granted or denied.
