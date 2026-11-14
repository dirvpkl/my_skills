# Scan protocol (for inventory agents)

Readonly: code search + compose/docker files + `docker ps` / `compose ls`
max. No writes, no restarts, no exec into containers beyond read-only inspect.
NEVER read `.env` (`.env.example` allowed). NEVER read `*.log`.

Per repo report: services found, what need each covers (schedule / stream /
parse / post / observe), deps used, and hand-rolled code duplicating a
covered need (flag as replace-candidate, don't replace).

Update `known-services.md` only with seen evidence (repo path + file/line or
container name). No "probably exists".
