---
name: docker
description: Docker networking defaults — never publish container ports to the host without an explicit, same-message ask; published ports always land on a random ephemeral host port (never a fixed default like `8080:8080`); internal-only service-to-service networking by default; required (`${VAR:?...}`) compose environment variables. Use whenever writing or editing docker-compose files or docker run commands.
version: 1.3.0
---

# docker

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-13: added compose env-var rule -- always ${VAR:?message}, never a bare ${VAR}. -->
<!-- v1.3 - 2026-10-27: published host ports are always random ephemeral ports, never fixed defaults like 8080:8080; services inside the network stay unpublished. -->

## Trigger
Writing or editing docker-compose files or `docker run` commands. Bundled by the `coding` dispatcher whenever Docker config is touched — see its activation manifest.

## Networking defaults
- Never add `ports:` mappings (or otherwise publish container ports to the host) in docker-compose files or `docker run` commands unless the user explicitly asks for that port to be exposed in that message.
- Default to internal-only networking: services talk to each other over the compose network by service name; nothing gets published to the host unless asked.
- If a service needs a port for the user to reach it directly (e.g. a web UI), ask first, or wait for explicit instruction — don't assume "it'll be convenient" is enough justification.
- When publishing to the host is explicitly approved, never pin a fixed host port — no `8080:8080`, `8000:8000`, or any other default. Publish with a random ephemeral host port instead: compose `ports: ["<container-port>"]` (container port only, Docker picks the host port) or `docker run --publish-all` / `-p :<port>`. The container-side port stays explicit; the host side is always random.
- Exception — services inside the network: service-to-service traffic stays on the compose network by service name and container port; nothing about those services is published to the host, random or otherwise.

## Compose environment variables
- Every variable referenced in a compose file uses the required form `${VAR:?error message}` — never a bare `${VAR}`. An unset value must fail `up`/config validation before containers start, not silently ride into the container as an empty string.

## Editing existing files
- If you find existing `ports:` mappings while editing a compose file for an unrelated reason, leave them as-is — don't add new ones and don't remove existing ones without being asked.
- Existing `ports:` on other services in the same file are not precedent for a new service. Seeing that service X already publishes a port is not a reason to publish a port for new service Y — the same-message explicit-ask rule still applies to Y regardless of what X already does.

## Report
Note any port mappings added, and whether they were explicitly requested in that message.
