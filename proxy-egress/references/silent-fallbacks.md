# Silent fallbacks

Every pattern here is a way code reaches the internet without a proxy while
appearing to be configured for one. Each one has been found in a real codebase
by grepping, not by reading. Run the greps; do not rely on remembering.

## The core defect: a default that means "direct"

Most libraries and most hand-written pools express "no proxy" as falsy. Once
that value reaches the client, the client connects directly and reports success.

Grep for the shapes:

```bash
grep -rnE "proxy\s*=\s*None|proxies\s*=\s*None|proxies=\{\}" --include=*.py
grep -rnE "proxies?\s*or\s+None|proxy_url\s*or\s+[\"'][\"']" --include=*.py
grep -rnE "getenv\([^)]*PROXY[^)]*,\s*[\"'][\"']\)|environ\.get\([^)]*PROXY[^)]*,\s*[\"'][\"']\)" --include=*.py
grep -rnE "\bor None\b|\bor \"\"\s*$" --include=*.py | grep -i proxy
```

The fix is always the same: the value must come from a helper that raises when
it is missing or blank, and the "no proxy" default disappears from the type.
A parameter typed `str | None` where `None` reaches a client is the smell.

Precision note for `requests`: a bare `proxies=None` is smell, not proof -
`Session.request` normalizes it to `{}` and the environment still applies.
Direct happens on a per-scheme `None` (`proxies={"http": None}`) or
`trust_env=False`. So a `proxies=None` grep hit means "read the surrounding
lines", while a per-scheme `None` or a disabled `trust_env` means "found it".

## Optional file that is the only source of addresses

A pool file treated as optional means an unmounted or typo'd path yields an
empty pool, which yields "direct" for every request.

```bash
grep -rnE "is_file\(\)|FileNotFoundError|except OSError" --include=*.py | grep -iE "proxy|pool"
grep -rn "load_proxies\|load_proxy_pool\|read_text" --include=*.py | grep -i proxy
```

A missing file, an unreadable file, and a file with no usable URL are all
deployment errors. Raise on each. Lines without a scheme can still be skipped
with a warning - one bad line should not kill the worker, and that is a
different failure from "no addresses at all", which is the one that must raise.

## Cooldown that gives up and goes direct

Round-robin pools cool a failed address down and pick another. The common
version, when every address is cooling, returns `None` "so the attempt still
happens" - and the attempt happens directly.

```bash
grep -rnE "cooldown|cooling|cool_down|note_failure|mark_bad" --include=*.py
```

With a single address (the common case - rotation is the proxy service's job),
one failure therefore means *every* subsequent request goes direct. Fail the
attempt instead. A dead proxy should stop the work, not silently change its
meaning.

## The caller that bypasses the shared helper

The shared request helper takes an optional per-call proxy so one call can
override it. The moment that argument defaults to `None`, every call site that
omits it decides for itself whether to use the pool.

```bash
grep -rnE "def .*\(.*proxy.*=.*None" --include=*.py
grep -rnE "def .*\(.*proxies.*=.*None" --include=*.py
```

Resolve the address inside the helper when the argument is absent, so the
fallback is the proxy rather than a direct connection.

## `NO_PROXY` that does not cover the internal service

The proxy is set, `NO_PROXY` is set, and internal traffic still breaks -
because the internal hostname is not in the list, or the list is set but the
client library ignores it (aiohttp always does).

```bash
grep -rn "NO_PROXY\|no_proxy" --include=*.yml --include=*.yaml --include=*.env*
```

The list must contain the names the code actually uses: the compose service
name for a container (`mongo`, `qdrant`, `whisper`), `localhost` and
`127.0.0.1` for host-bound services, and the host gateway name when a local
service is published on the host (`host.docker.internal`). A sidecar that is
internal *and* reached by service name cannot be proxied at all - the proxy has
no way to resolve it - so a wrong list produces a hard failure rather than a
slow one.

## Library defaults worth re-checking

- Explicit `proxy=` on an httpx-based client disables `NO_PROXY` for that
  client.
- Go clients that set a custom `Transport` stop reading the environment.
- A Telethon/MTProto client with no proxy package installed warns and connects
  directly.
- `curl_cffi` with a string `proxies` raises on the first request, so a
  construction-only test passes.
- ffmpeg reads lowercase `http_proxy`, a different variable from the rest.

See `client-matrix.md` for the full table.

## Deployment-shaped traps

These are not code fallbacks but they produce the same outcome - traffic leaves
from the wrong address - so they belong in the same audit:

- **Compose required form.** `${PROXY_URL}` without `:?` lets the stack start
  with an empty value, and an empty value is a direct connection. Use
  `${PROXY_URL:?message}`.
- **A variable set in the wrong place.** Declared in `pyproject.toml` but the
  image installs from a hand-written list in the Dockerfile, so the container
  lacks it. Check how the image is actually built.
- **A cache volume on the wrong path.** The image exports `HF_HOME=/app/...` and
  the volume is mounted at `/root/...`; nothing persists, so every restart
  re-fetches, which reads as a hang.
- **A port collision.** Stack A binds `127.0.0.1:8080`, stack B wants
  `0.0.0.0:8080`; the wildcard overlaps the loopback bind, and one stack's
  container starts without a network attachment, which looks like a networking
  bug in the proxy config.
- **Exhausted Docker address pools.** `all predefined address pools have been
  fully subnetted` - new networks cannot be created, so `compose up` aborts.
  Give the stack an explicit subnet outside the default pools.

## A test that is not worth writing

A test asserting the address was *read* proves little. What catches these bugs:

- a test that performs a request through the fake client and asserts the proxy
  argument is present (catches the `proxies=None` and string-vs-dict shapes);
- a test that deletes the variable and asserts the entry point raises (catches
  the missing-config shape);
- for protocol-requiring clients, a test that builds the client with warnings
  promoted to errors (catches the silently-dropped argument), plus a live
  connect in the deployed container, because construction alone is not proof.

And one that keeps the suite green once fail-loud checks exist: tests that
construct clients with external-looking fixture URLs would trip the startup
assertion, since the test process has no proxy configured. Mirror production
in the test setup instead - a `conftest.py` that defaults a dummy
`HTTP_PROXY`/`HTTPS_PROXY` (and a production-like `NO_PROXY`) the same way
compose does. The dummy is never dialled (transports are mocked); it only
satisfies the assertion that production satisfies via the real variable. Never
put real credentials there.
