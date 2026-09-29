---
name: proxy-egress
description: Wire a project's outbound internet traffic through an authenticated proxy with no silent direct-connection fallbacks. Use when a task involves a proxy, PROXY_URL/HTTP_PROXY, egress routing, "route everything through the proxy", NO_PROXY, or auditing a codebase for paths that can reach the internet unbound. Covers per-client-library proxy behavior (httpx, aiohttp, requests, curl_cffi, Telethon, PTB, Go), how to hunt down silent fallbacks, and how to prove routing works in a live container.
version: 1.0.2
---

# proxy-egress

Making every outbound call go through an authenticated proxy, with the
guarantee that no code path can quietly connect directly instead. The hard
part is not setting the variable - it is that most HTTP libraries treat a
missing proxy as "connect directly, silently", so a deployment that lost its
proxy config still appears to work while every request leaves the host
unbound.

- **references/client-matrix.md** - per-library proxy behavior. Read this
  before editing any client; the differences between libraries cause more
  bugs than the config does.
- **references/telegram-sidecar.md** - the self-hosted Telegram Bot API server:
  which image can carry a proxy, the entrypoint that splits one `PROXY_URL`
  into TDLib's five flags, volume ownership, healthcheck, and how to point a
  client at the local server without proxying the internal hop.
- **references/silent-fallbacks.md** - the catalog of ways code bypasses a
  proxy, with the grep patterns that find each one.
- **references/verification.md** - proving routing is real, from inside a
  running container.
- **plugins/manifest.json** - the list of active modules for this skill. Check
  this to see what's currently plugged in rather than assuming this file lists
  everything.

## Trigger
Engages when the task is about proxying outbound traffic, enforcing mandatory
egress, or auditing for paths that can reach the internet without a proxy.
Phrases: "through the proxy", "PROXY_URL", "HTTP_PROXY", "NO_PROXY", "egress",
"route everything", "don't go direct", "no direct fallback", "proxy pool".

Does NOT trigger on: a *consumer* of a proxy that already exists and is known
to work (a single `httpx` client already reading `HTTP_PROXY` in a project with
`NO_PROXY` in place - there is nothing to decide); proxy *service* internals
(its own pool logic, routing, credentials storage - that is the user's system,
treat it as a black box unless asked); or a decision about *whether* to proxy
at all (that is `solution-search` via the topic folder).

## Process

### 1. Ask where the proxy lives, never assume

Do not hardcode a host, a port, a credential, or a filesystem path to the
proxy service. Those are the user's environment and they change. Before writing
anything, ask:

- where the proxy service runs (host, port, scheme), and whether it is the
  same port for HTTP and SOCKS5;
- the credential to use for *this* project, and whether each project gets its
  own login or they share one;
- whether the login string selects an exit pool (many services route by
  username), and what the current exit IP actually is.

A login that is not registered yet returns a distinct error from a wrong
password - verify a credential before wiring it in rather than after.

### 2. Establish what the project actually talks to

Inventory every outbound path before changing anything, per client library:
HTTP clients, Telegram/IM clients, downloaders (yt-dlp, streamlink, ffmpeg),
headless browsers, sidecar images that fetch models at boot, and any local Bot
API server. A "network client" is anything holding a socket, not just a file
named `client.py`.

Classify each destination:

| Kind | Treatment |
|---|---|
| External API / CDN | goes through the proxy |
| Local LLM, local search, vector store, database, cache | must stay direct, listed in `NO_PROXY` |
| Raw TCP (IRC, MTProto, custom protocols) | SOCKS5, needs an explicit proxy client library |
| Sidecar fetching a model on first boot | decide separately, see step 6 |

If a project turns out to have no external egress at all, say so and confirm
with the user whether to wire anything anyway - adding a mandatory variable to
a service that never leaves the host is busywork that misleads later readers.

### 3. One address, required form

Put a single `PROXY_URL` in the deployment env and derive everything from it.
Rotation between exits is the proxy service's job, so the repository keeps no
list of addresses unless a single project genuinely needs several credentials
(then a small `proxies.txt` that is gitignored, with the same fail-loud rules).

Required form in compose, so an unset value fails validation before any
container starts rather than surfacing as a direct connection later:

```yaml
HTTP_PROXY: ${PROXY_URL:?set PROXY_URL in .env}
HTTPS_PROXY: ${PROXY_URL:?set PROXY_URL in .env}
NO_PROXY: ${NO_PROXY:?set NO_PROXY in .env}
```

`NO_PROXY` is not optional once `HTTP_PROXY` is set. List every internal
destination by the name the code uses to reach it - the compose service name
for a container, `localhost`/`127.0.0.1` for the host. A wildcard bind
(`0.0.0.0`) overlaps a loopback bind on the same port, so two stacks can
collide without either being wrong.

### 4. Wire each client according to its actual behavior

Read `references/client-matrix.md` and do not assume symmetry. The three
outcomes:

- **reads the environment** (httpx with default `trust_env`, Go's default
  transport, requests when `proxies` is omitted) - env alone covers it;
- **ignores the environment** (aiohttp by default) - pass the address per
  request, or use the library's proxy-aware session;
- **needs a different protocol** (Telethon/MTProto, raw TCP) - build the
  mapping the library expects, forced to SOCKS5, and install the proxy client
  package it silently requires.

A local service reached by an explicit `proxy=` is the specific trap: an
explicit argument overrides `NO_PROXY` in several libraries, so the local Bot
API gets pushed through the external proxy, where its hostname cannot resolve.
Either rely on the environment for those clients, or set `trust_env`/mounts so
the exclusion still applies.

### 5. Hunt the silent fallbacks

This is the part that produces real bugs. Grep for each pattern in
`references/silent-fallbacks.md` and fix what exists. The recurring shapes are
a default that means "no proxy" (`X or None`, `proxies=None`, an empty pool
answering `None`), a file that is optional when it is actually the only source
of addresses, and a cooldown path that gives up and connects directly instead
of failing.

Every one of them must become: raise. A missing proxy is a deployment error,
not a reason to bind the host's own IP.

### 6. Decide per sidecar, do not blanket it

An image that pulls a model or an API on first boot is a separate decision.
Through a shared proxy it can hit provider-side rate limiting keyed on the exit
IP - the container then dies in a way that looks like a hang, not like a
network error. Prefer, in order: load from a cache that persists (check that
the cache path is the one the image actually writes to, not a plausible-looking
default), then a provider mirror the image's HTTP stack can follow, then
`HF_HUB_OFFLINE`-style offline mode once the model is cached. Report the
choice instead of leaving it implicit.

### 7. Fail loud at the entry points

Env-var validation stops the *config* being wrong. A startup assertion in each
process that actually opens sockets stops it being *silently* wrong. A small
helper that reads the variable and raises on missing/blank, called from the
service entry point (and from each client factory when the value is passed
explicitly), is enough. Do not call it per request.

### 8. Prove it in a running container

Static review does not catch the bugs that matter here. Verify from inside the
built container: that external traffic resolves to the proxy's exit IP, that
every `NO_PROXY` target still answers directly, and that the client library
under test actually applied the address rather than warning and continuing.
`references/verification.md` has the commands and the known failure signatures.

## Output format
Report, per project: the inventory of egress paths and how each is wired
(env / explicit / SOCKS5), the fail-loud points, what was verified live and how,
and what remains blocked on a user decision. Name any pre-existing defect found
along the way separately from the change itself, and never print proxy
credentials in the report.
