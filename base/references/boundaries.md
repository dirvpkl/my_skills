# Boundaries — scope, secrets, external services

Read before the first state-changing command.

## Assigned scope only

Work inside the projects named in the task. Anything else — sibling
projects, home directories, host apps, other checkouts — is out of
scope until the user explicitly adds it. Read-only inspection of a
sibling to diagnose (e.g. checking whether a proxy router is up) is
allowed; changing it is not.

## External services are black boxes

If the bug lives in an external service (proxy provider, hosted API,
tunnel, VPS side), do not go there unasked. Diagnose up to the
boundary, report the evidence, stop. Rationale: credentials there
may be non-rotatable, and a "fix" can lock the user out.

## Secrets: ask everything

`.env` files, API keys, tokens, cookies, tunnel configs, browser
profiles, `*.pem`/`*.key`, chat histories with creds: never open to
browse, never print, never log. Ask in plain language first; explicit
yes only; no provisional work while waiting. Missing secret = loud
fail, never a silent fallback or a guessed value. An exposed
credential gets an all-caps flag line every time.

## Never-do list (no exceptions without explicit yes)

- `rm -rf`, `docker down -v`, volume prune, `DROP DATABASE`, disk format.
- Host package installs, firewall/network changes, reboot, cron edits.
- Force-push, history rewrites, `git reset --hard` on uncommitted work.
- Committing `.env`, keys, cookies, or chat exports.
- Editing files outside the assigned projects.
