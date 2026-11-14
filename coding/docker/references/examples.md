# docker — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Publishing a port nobody asked for

**Good:** the new service joins the compose network by name, no `ports:` key — the web UI is reachable only through the network until the user asks.
**Bad:** adding `ports: ["8080:8080"]` "so it's convenient to test" in the same edit.
Rationale: publishing a container port to the host without an explicit same-message ask is the core breach — and a fixed default port is a double violation.

## Approved publish still keeps the host side random

**Good:** after the user says "expose the web UI", `ports: ["3000"]` — Docker picks the ephemeral host port, the container side stays explicit.
**Bad:** `ports: ["3000:3000"]` because it mirrors the container port.
Rationale: even with approval the host port is never pinned — a random ephemeral port is the rule, the container-side port is the only one that stays named.

## Compose env vars: required and unprefixed

**Good:** `BOT_TOKEN: ${BOT_TOKEN:?bot token required}` — an unset value fails config validation before containers start.
**Bad:** `PROJECT_BOT_TOKEN: ${PROJECT_BOT_TOKEN:-dev123}` — project-prefixed name plus a silent fallback.
Rationale: `${VAR:?msg}` makes a missing value fail loud; a project prefix and a `${VAR:-fallback}` hide the same failure and bake in wrong values.

## Existing ports are not precedent

**Good:** while editing an unrelated setting for service Y, leaving its networking untouched and noting in the report that service X already publishes a port.
**Bad:** "service X already publishes 8080, so I gave service Y one too for consistency."
Rationale: the same-message explicit-ask rule applies per service — another service's existing mapping never authorizes a new one, and existing mappings are left as-is, not removed or copied.
