# boundaries — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Chat hygiene: show the FORM, not the values

**Good:** after a curl, the chat shows `status: 200, token: present (len 47), user_id: 3` — the raw response filtered before display.
**Bad:** pasting the raw response body into chat, token and personal data included.
Rationale: anything already in chat is compromised (the memo's golden rule) — print the form (lengths, presence, codes), never the values, and a URL with `?token=...` is a leaked token.

## Secrets file checked by script, not read

**Good:** the .env check script prints booleans and lengths — `KEY1 present: true, len 24`.
**Bad:** `cat .env` to "see what's in there" before wiring a service.
Rationale: the user fills in secret values themselves; the agent never needs to see them, and indirect reads (echoing, logging, scripting the cat) count as reads.

## Denied access stays denied

**Good:** the user rejects the permission prompt for a log file → "access was denied — reporting what's blocked and stopping."
**Bad:** retrying the same read via a wrapper script or symlink "since it's just a log."
Rationale: routing around a denial with a different method is the breach itself — no provisional work while waiting, no alternate-route retries after a no.

## Every exposure flagged, every time

**Good:** a token appears in command output → the response ends with the all-caps line naming it: EXPOSED CREDENTIAL: TGBOT_TOKEN in curl output.
**Bad:** mentioning the exposure casually once and moving on with the task.
Rationale: the all-caps flag fires every time an exposure happens, not just the first — the repetition exists so nothing scrolls by unnoticed, and revoke comes first in the leak protocol.
