# Data — preservation, host, tests

## Don't lose data

Volumes and databases outlive containers. Before migrate/recreate/
upgrade: identify what holds state (named volumes, bind mounts, DB
containers), back it up or snapshot it, then act. `docker compose down`
without `-v` is the default; `-v` needs an explicit yes. If a volume
is already missing (e.g. expected `mongo_data` absent), say so before
creating — an empty DB is data loss shaped like a fresh start.

## Keep the host intact

The host is shared: many projects live on it. Every Python action goes through
`uv`, never the global interpreter: run with `uv run`, add deps with
`uv add`/`uv pip`, and if the folder has no uv environment yet, make one
(`uv venv`, then `uv sync`). Bare global `python`/`pip` is not the tool —
no host-level installs on top of it, no falling back to it when uv is
"missing". Also: no port grabs without checking compose files, no stray
background processes. Published ports (`ports:`) only with an explicit
same-message ask.

## Tests run in docker

New repos, refactors, dependency changes: prove them inside a
container (project compose service or throwaway container with the
repo mounted), never by installing onto the host. A green host run
proves nothing about the deployed artifact. Environment-vs-code
failures are distinguished per `testing` — a broken daemon is a
stop-and-report, not 40 retried iterations.

