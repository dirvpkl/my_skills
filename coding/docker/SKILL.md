---
name: docker
description: Docker networking defaults — never publish container ports to the host without an explicit, same-message ask, internal-only service-to-service networking by default, and required (`${VAR:?...}`) compose environment variables. Use whenever writing or editing docker-compose files or docker run commands.
version: 1.1.0
---

# docker

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-13: added compose env-var rule -- always ${VAR:?message}, never a bare ${VAR}. -->

## Trigger
Writing or editing docker-compose files or `docker run` commands. Bundled by the `coding` dispatcher whenever Docker config is touched — see its activation manifest.

## Networking defaults
- Never add `ports:` mappings (or otherwise publish container ports to the host) in docker-compose files or `docker run` commands unless the user explicitly asks for that port to be exposed in that message.
- Default to internal-only networking: services talk to each other over the compose network by service name; nothing gets published to the host unless asked.
- If a service needs a port for the user to reach it directly (e.g. a web UI), ask first, or wait for explicit instruction — don't assume "it'll be convenient" is enough justification.

## Compose environment variables
- Every variable referenced in a compose file uses the required form `${VAR:?error message}` — never a bare `${VAR}`. An unset value must fail `up`/config validation before containers start, not silently ride into the container as an empty string.

## Editing existing files
- If you find existing `ports:` mappings while editing a compose file for an unrelated reason, leave them as-is — don't add new ones and don't remove existing ones without being asked.
- Existing `ports:` on other services in the same file are not precedent for a new service. Seeing that service X already publishes a port is not a reason to publish a port for new service Y — the same-message explicit-ask rule still applies to Y regardless of what X already does.

## Report
Note any port mappings added, and whether they were explicitly requested in that message.
