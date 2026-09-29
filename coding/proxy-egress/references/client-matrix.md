# Client proxy matrix

How each client behaves when you hand it a proxy address. Read the row for the
library in the project before editing it; the libraries are not interchangeable,
and the surprising entries are where the bugs live.

Assumes the proxy service listens for HTTP and SOCKS5 on the same port (verify,
don't assume - some services use separate ports).

## Summary

| Client | Reads env? | Needs explicit? | Gotcha |
|---|---|---|---|
| httpx | yes, `trust_env` defaults true | no | explicit `proxy=` **overrides `NO_PROXY`** |
| aiohttp | no, `trust_env` defaults false | yes, per request | env is silently ignored |
| requests / cloudscraper | yes, but only when `proxies` is omitted | no | `proxies=None` means direct |
| urllib3 / requests `ProxyManager` | no | yes | takes a dict |
| curl_cffi | no | yes | **wants a dict**; a string raises `AttributeError` |
| Go `http.Client` (no Transport) | yes | no | setting a custom `Transport` opts out |
| Go `http.Client` (custom Transport) | no | yes | you own the transport config |
| Telethon (sync) | no | yes, `proxy=` dict | needs `pysocks`, else drops the arg |
| Telethon (async) | no | yes, `proxy=` dict | needs `python-socks`, else drops the arg |
| python-telegram-bot | via `HTTPXRequest` | usually no | `HTTPXRequest(proxy=)` also overrides `NO_PROXY` |
| aiogram (`AiohttpSession`) | no | needs a session that supports it | no `proxy=` parameter exists |
| yt-dlp | env (`http_proxy`) | yes, `--proxy` | accepts both schemes |
| streamlink | env | yes, `--http-proxy` | `--https-proxy` is deprecated, warns |
| ffmpeg | env, lowercase | yes, in the subprocess env | `http_proxy` / `https_proxy` |
| Playwright | no | yes, at context/launch | not an env read |

## httpx

Reads `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY` from the environment by default
(`trust_env=True`). Env alone is usually enough.

The trap: passing `proxy=` explicitly replaces the environment for every
request, so `NO_PROXY` stops applying. A local Bot API or an internal service
then goes out through the external proxy, where its hostname does not resolve -
usually surfacing as `502`/`Bad Gateway` on every call, or `ConnectError` when
the target is a container name. If a client must use an explicit proxy, check
whether the local destinations for that client are reachable some other way, or
use `mounts=` to scope the proxy to specific URL patterns.

## aiohttp

`trust_env` defaults to **false**. The environment is read by nobody. Pass
`proxy=` on each request, or build the session with `trust_env=True` if the
address is in the environment. The safest shape is one shared helper that
resolves the address once, so no call site can forget it:

```python
async with session.post(url, data=payload, proxy=proxy_url()) as response:
    ...
```

## requests / cloudscraper

Honors the environment only when the `proxies` argument is **omitted**. A
caller that passes `proxies=None` explicitly gets a direct connection, and so
does any code path that passes `proxies=` built from a missing value. Convert a
bare URL into a per-scheme mapping in one helper and let the helper raise when
no address is configured.

## urllib3 / requests ProxyManager

Takes a dict (`{"http": ..., "https": ...}`) and does not read the
environment.

## curl_cffi

Takes a **dict** for `proxies`. Handing it the URL string raises
`AttributeError: 'str' object has no attribute 'get'` on the *first request* -
the session object constructs fine, so a unit test that only checks
construction passes and the breakage only shows under real traffic. This exact
split is worth a test that performs a request, not just a build.

## Go

`&http.Client{Timeout: ...}` with no `Transport` uses `http.DefaultTransport`,
which reads `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`. That covers the whole
project at zero code cost. Setting a custom `Transport` (or setting
`Transport: &http.Transport{Proxy: nil}`) silently opts the client out of the
environment - grep for `Transport:` when auditing.

## Telethon

Telegram's MTProto is raw TCP, which HTTP CONNECT cannot carry, so the mapping
must be SOCKS5 regardless of the URL scheme in `PROXY_URL`:

```python
def telethon_proxy() -> dict[str, str]:
    parts = urlsplit(proxy_url())
    out = {"proxy_type": "socks5", "addr": parts.hostname, "port": str(parts.port)}
    if parts.username:
        out["username"] = parts.username
    if parts.password:
        out["password"] = parts.password
    return out
```

The dependency is the part that bites. Telethon dials the proxy through
PySocks, and **drops the `proxy=` argument with a single warning when it is not
installed**, then connects directly. So both are needed, and they are needed at
different layers:

- sync client (`from telethon.sync import TelegramClient`) → `pysocks`
- async client (`import telethon`) → `python-socks[asyncio]`

A unit test that builds a client and asserts on the mapping will pass with
neither installed. Only an actual connect proves it, and the failure surfaces
as a restart loop, not an exception at startup. If the project installs
packages with a hand-written `pip install` list in a Dockerfile rather than
from `pyproject.toml`, the dependency has to be added in both places.

## python-telegram-bot

`HTTPXRequest` is httpx underneath and does not set `trust_env`, so the
environment applies by default and `NO_PROXY` is respected. Passing
`proxy=` to it has the same override problem as plain httpx - do not, unless a
local Bot API is not involved. Note that some versions accept `proxy=` at the
request level for a *local* Bot API; a local server on the compose network
belongs in `NO_PROXY`, not behind the proxy.

## aiogram

`AiohttpSession` has no proxy parameter, and aiohttp ignores the environment.
Either use a session type that accepts a proxy, or route the Telegram API
through a local Bot API sidecar and set `api_base` to it - the sidecar's MTProto
leg then carries the SOCKS5 flags, which is the cleaner arrangement anyway.

## yt-dlp / streamlink / ffmpeg

- yt-dlp: `--proxy` accepts an `http://` or `socks5://` URL. It also reads
  `http_proxy` from the environment, but an explicit flag makes the intent
  visible and lets a retry pick a different address.
- streamlink: `--http-proxy` covers both schemes; `--https-proxy` is deprecated
  and warns on every run.
- ffmpeg: reads **lowercase** `http_proxy` / `https_proxy` in the subprocess
  environment, which is a different variable from the one the rest of the
  project uses.

A downloader that takes its address per attempt is the right shape: each retry
can rotate, and a failed attempt can mark that specific address as cooling.
See `silent-fallbacks.md` for the cooldown path that usually ruins this.

## Playwright

Not an environment read. Pass the proxy at context or launch:

```python
browser = await playwright.chromium.launch(proxy={"server": proxy_url()})
```

## Headless sidecars

An image that downloads a model on first boot is a separate case: it is
usually a Python process with its own HTTP stack, so it obeys the rules above,
but its *provider* may rate-limit by exit IP. The failure mode is a slow
timeout during startup that looks like a hang. Prefer a persistent cache
(verify the image writes to the path that is actually mounted - `HF_HOME` and
`HF_HUGGINGFACE_HUB_CACHE` are the variables that decide, and a
plausible-looking mount path can be the wrong one), then a mirror the image's
HTTP stack can follow, then offline mode.
