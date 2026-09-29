# Verification

A proxy change is not done when the variable is set. It is done when a request
from inside the running container is observed leaving through the proxy's exit
IP, and the internal targets are observed still answering directly.

## Order

1. The credential works, from a throwaway container.
2. `docker compose config` passes (an unset required variable fails here, not
   later).
3. The stack starts, no container in a restart loop.
4. The proxy's exit IP, from inside the app container.
5. Each internal target answers directly.
6. The client library under test actually applied the address.

## 1. Verify the credential before wiring it in

```bash
docker run --rm curlimages/curl:latest -sS -o /dev/null -w "%{http_code}\n" \
  --max-time 20 --proxy "http://USER:TOKEN@HOST:PORT" https://www.gstatic.com/generate_204
```

Then record the exit IP, which is how you tell later whether routing changed:

```bash
docker run --rm curlimages/curl:latest -sS --max-time 20 \
  --proxy "http://USER:TOKEN@HOST:PORT" https://api.ipify.org
```

Check SOCKS5 as well if the client needs it - same command with `socks5://`.

Two distinct failures to tell apart: a service that does not know the login
rejects the tunnel (`403`/`407` at CONNECT, i.e. the credential is not
registered), while a transient network blip looks like a timeout. One retry
before concluding anything. Never print the credential in a report.

## 2-3. Config and startup

```bash
docker compose config -q                       # required vars fail here
docker compose ps --format '{{.Name}}  {{.Status}}'
docker inspect <container> --format '{{.RestartCount}} {{.State.OOMKilled}} {{.State.ExitCode}}'
```

A rising restart count with `exit=0` and no OOM is a crash-after-start, not a
config error - read the last lines of the log before theorizing. Some images
have no `curl`/`wget` at all; use the runtime that is present.

## 4. The exit IP, from inside the app container

This is the check that proves the env actually reached the process. Note that
some tools read the variable in different cases - `wget` wants lowercase
`https_proxy`, Go and curl want uppercase `HTTP_PROXY`/`HTTPS_PROXY` - so pass
the case the tool needs and keep the container's real env as the baseline.

```bash
docker exec <container> sh -c 'env | grep -iE "^(http_proxy|no_proxy)="'
```

Then, from inside:

- **Go / curl** - `wget -qO- https://api.ipify.org` (Go honours the env).
- **Python** - `httpx` and `requests` honour the env;
  `aiohttp` does not, so for that library call the code path that resolves the
  proxy and print what it returns, then exercise the real send.

If the container has no HTTP client, run the project's own runtime, and add
the project's source root to the path:

```bash
docker exec -i -w /app <container> .venv/bin/python - <<'PY'
import sys; sys.path.insert(0, "/app")
from your.module import proxy_url, telethon_proxy   # whatever exists
print(proxy_url())
PY
```

## 5. Internal targets stay direct

For each `NO_PROXY` entry, from inside the app container:

```bash
docker exec <container> sh -c 'wget -qO- --timeout=8 http://mongo:27017/ ; echo rc=$?'
```

`rc=0` plus a response means direct. A protocol-level error is still a *good*
sign here - asking a database over HTTP gets disconnected, which proves the
connection was made locally. A timeout or a proxy error means the entry is
missing or the library ignores `NO_PROXY` (aiohttp always does).

## 6. The client applied it

For libraries that take the address as an argument, build the client with
warnings promoted to errors and a throwaway session path:

```python
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("error")   # "proxy argument will be ignored" now raises
    client = TelegramClient(tmp_path, 1, "x" * 32, proxy=telethon_proxy())
```

For a raw-TCP destination, do what the library does - dial the SOCKS5 proxy
yourself, then read a byte from the target. A `400` from a well-known host on
a malformed request proves the tunnel carried the traffic; a `502` from the
proxy proves it did not.

## Failure signatures worth recognizing

| Symptom | Actual cause |
|---|---|
| Restart loop, first log line is a module import | The client needs a proxy package that is not installed (Telethon: `pysocks` sync, `python-socks` async) |
| `502` / `Bad Gateway` on every request to a *local* service | Explicit `proxy=` on an httpx-based client disabled `NO_PROXY`; the local hostname cannot resolve outside |
| `AttributeError: 'str' object has no attribute 'get'` on first request | `curl_cffi` was given a string instead of a per-scheme dict |
| Container `running`, port never opens, no log progress for minutes | A sidecar re-downloading because its cache volume is mounted on a path the image does not write to |
| Exit `137`, no log | Out of memory - often a model-optimization peak, not a large model |
| Exit `3` during startup of an ONNX/embedding service | The chosen execution provider cannot load a quantized node; a CPU provider flag usually fixes it |
| `Connect call failed` / `Connection closed unexpectedly`, then a healthy reconnect | Usually a transient proxy blip, not a config error; check whether it recurs before changing anything |
| `compose up` aborts on `network ... could not be found` | A declared external network is gone; check whether anything still needs it |
| `Bind for 127.0.0.1:PORT failed: already allocated` | Another stack holds the port; a wildcard bind overlaps a loopback bind |

## What not to conclude

A green test suite is a floor, not proof. The bugs this audit exists to find -
a dropped proxy argument, a string where a dict is required, a local service
pushed through the proxy - all pass unit tests that only build objects. The
live check is what catches them.
