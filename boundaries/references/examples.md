# boundaries — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.
Two pairs minimum per case (owner convention 2026-11-15).

## Chat hygiene: show the FORM, not the values

**Good:** after a curl, the chat shows `status: 200, token: present (len 47), user_id: 3` — the raw response filtered before display.
**Bad:** pasting the raw response body into chat, token and personal data included.
Rationale: anything already in chat is compromised (the memo's golden rule) — print the form (lengths, presence, codes), never the values, and a URL with `?token=...` is a leaked token.

**Good:** chatty libraries are silenced at level 1 (httpx/http.client/urllib3) — a full URL in an httpx log has already leaked a bot token once.
**Bad:** "the library logs the request line, that's fine, it's just debug output."
Rationale: the request line carries the query string, and the query string carries tokens — a log is chat output the moment anyone opens it.

## Secrets: ask, never browse

**Good:** the task needs a DB password → one plain-language ask ("I need the postgres password to run the migration — where is it?"), explicit yes, then read.
**Bad:** `cat .env | grep POSTGRES` "just to see what's there" — browsing secrets without an ask is the breach itself.
Rationale: the ask IS the rule; browsing first turns every read into a possible leak.

**Good:** the .env check script prints booleans and lengths — `KEY1 present: true, len 24`.
**Bad:** echoing the key inside a helper script "to verify it loaded" — an indirect read counts as a read.
Rationale: the user fills in secret values themselves; the agent never needs to see them, and indirect reads (echoing, logging, scripting the cat) count as reads.

**Good:** the key is missing at runtime → fail loudly naming the key.
**Bad:** `os.environ.get("API_KEY", "fallback-dev-key")` — a silent placeholder that "works" until it silently works against production.
Rationale: a guessed secret value is worse than a missing one — fail loud, never substitute.

## Denied access stays denied

**Good:** the user rejects the permission prompt for a log file → "access was denied — reporting what's blocked and stopping."
**Bad:** retrying the same read via a wrapper script or symlink "since it's just a log."
Rationale: routing around a denial with a different method is the breach itself — no provisional work while waiting, no alternate-route retries after a no.

**Good:** while waiting for the user's answer on the log file, the rest of the task proceeds — everything that doesn't touch the denied item.
**Bad:** doing the whole task provisionally "assuming the permission will land."
Rationale: the ask is per item, not a task-wide freeze — but the denied item itself never moves until the yes.

## Every exposure flagged, every time

**Good:** a token appears in command output → the response ends with the all-caps line naming it: EXPOSED CREDENTIAL: TGBOT_TOKEN in curl output.
**Bad:** mentioning the exposure casually once and moving on with the task.
Rationale: the all-caps flag fires every time an exposure happens, not just the first — the repetition exists so nothing scrolls by unnoticed.

**Good:** leak protocol in order: revoke immediately, issue the new value into the file — not the chat — restart, then investigate what else lived in that output.
**Bad:** investigating the leak first and revoking last.
Rationale: reversing the order means you forget to revoke — a dead token in logs is just garbage, a live one is an open door.

## Data preservation: snapshot before migrate

**Good:** before `docker compose down` on a stack with named volumes → identify the state holders, back them up or snapshot, then act; `-v` only with an explicit yes.
**Bad:** `docker compose down -v` on a stack "to start clean" — an empty DB is data loss shaped like a fresh start.
Rationale: volumes and databases outlive containers; the migrate is only done when the old state was provably carried over.

**Good:** a volume is already missing (expected `mongo_data` absent) → say so before creating anything.
**Bad:** silently creating a fresh volume and reporting success.
Rationale: "success" on a missing volume means the old data was lost before you arrived — that is the report, not a starting point.

## Host integrity: uv venv, never global pip

**Good:** a script needs `requests` → `uv venv && uv sync` (or the project's env) and run via `uv run`.
**Bad:** `pip install requests` into the global interpreter because "it's just one package".
Rationale: the host is shared by many projects; global installs are the slow leak that breaks everything else.

**Good:** tests for a new repo run in a container (compose service or throwaway with the repo mounted).
**Bad:** proving the repo by installing its deps onto the host and running there.
Rationale: a green host run proves nothing about the deployed artifact — the container is the proof.

## Out-of-scope: one ask, one boundary

**Good:** the bug looks like the tunnel → diagnose up to the boundary, report the evidence, stop; the user decides whether anyone touches the VPS.
**Bad:** ssh into the VPS "just to check the config" — unasked.
Rationale: external credentials may be non-rotatable; a "fix" can lock the user out — the boundary is where the agent's reach stops.

**Good:** permission granted for `.env` → read exactly that; the task then needs the sibling `.env.production` → ask again.
**Bad:** treating the first yes as a pass to the whole directory.
Rationale: permission applies to what was asked; scope expansion is a new ask, not an implied one.
