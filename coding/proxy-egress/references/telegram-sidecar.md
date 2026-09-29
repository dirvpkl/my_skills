# Telegram: client and self-hosted Bot API server

Two independent halves, with different requirements. The client half is a
normal HTTP/MTProto consumer (`client-matrix.md` covers the library behavior).
The server half is a container that has to carry a proxy, and the image choice
is not free.

## The Bot API server image

To proxy the server's own MTProto connection to Telegram, the image must accept
TDLib's proxy flags. The common `aiogram/telegram-bot-api` image does **not** -
it exposes `--proxy`, which covers only outgoing webhook requests, and has no
way to set the TDLib proxy at all. `ghcr.io/avbor/docker-telegram-bot-api`
does, and is the one to use.

```
image: ghcr.io/avbor/docker-telegram-bot-api:latest
```

Verify the image has the flags before relying on it - this is a build-host
reachability question, not a guess:

```bash
docker run --rm --entrypoint telegram-bot-api \
  ghcr.io/avbor/docker-telegram-bot-api:latest --help
```

Concretely, the useful check is that its help output lists
`--tdlib-proxy-type`, `--proxy-server`, `--proxy-port`, `--proxy-login`,
`--proxy-password`.

### The binary takes five flags, not a URL

There is no `PROXY_URL` flag. Mount a small entrypoint that splits the one
`PROXY_URL` from the deployment env, so the credentials are not duplicated
across five variables in `.env` and cannot drift:

```sh
#!/bin/sh
set -eu

api_id=${TELEGRAM_API_ID:?TELEGRAM_API_ID is required}
api_hash=${TELEGRAM_API_HASH:?TELEGRAM_API_HASH is required}
proxy=${PROXY_URL:?PROXY_URL is required}
authority=$(printf '%s' "$proxy" | sed -e 's|^[a-z0-9]*://||' -e 's|.*@||')
credentials=$(printf '%s' "$proxy" | sed -e 's|^[a-z0-9]*://||' -e 's|@.*||')
host=${authority%:*}
port=${authority##*:}
login=${credentials%%:*}
password=${credentials#*:}

exec telegram-bot-api \
  --api-id="$api_id" \
  --api-hash="$api_hash" \
  --local \
  --http-port=8081 \
  --http-stat-port=8082 \
  --dir=/var/lib/telegram-bot-api \
  --temp-dir=/var/lib/telegram-bot-api/temp \
  --tdlib-proxy-type=socks5 \
  --proxy-server="$host" \
  --proxy-port="$port" \
  --proxy-login="$login" \
  --proxy-password="$password"
```

`--tdlib-proxy-type=socks5` is fixed regardless of the scheme in `PROXY_URL`:
MTProto is raw TCP, which HTTP CONNECT cannot carry. The proxy service must
listen for SOCKS5 on that port.

### Replacing the entrypoint drops the env-to-flag translation

This is the trap. The stock image turns `TELEGRAM_API_ID` / `TELEGRAM_API_HASH`
into command-line flags in its own entrypoint. Supply your own entrypoint and
that translation is gone - the binary prints its usage and exits, which looks
like a broken image rather than a missing flag. Hence the explicit
`--api-id` / `--api-hash` above.

Watch for this class of bug in a *copy* of the script that was written before
the fix, or before the project ever deployed - a latent copy fails the first
time someone runs it.

### Volume ownership

That image runs as its own uid/gid (uid 100, gid 101 in the current build). A
named volume populated by a previous image is owned by that image's uid, and
the new one cannot write:

```
Can't create files in the directory "/var/lib/telegram-bot-api/". Use --dir option
```

Check what the image expects, then fix the volume once:

```bash
docker run --rm --entrypoint sh ghcr.io/avbor/docker-telegram-bot-api:latest -c 'id telegram-bot-api'
docker run --rm -v <project>_<volume>:/d --user 0 alpine sh -c 'chown -R 100:101 /d'
```

A throwaway `fix-perms` service in compose is the durable alternative; a
one-shot `docker run` chown is enough when the volume is not recreated often.

### Healthcheck

The image has no `curl`; `nc` is present. The server listens on IPv4 only, and
in some setups `localhost` resolves to `::1` first, so use the literal address:

```yaml
healthcheck:
  test: ["CMD-SHELL", "nc -z 127.0.0.1 8081"]
  start_period: 15s
```

### Registry reachability

`ghcr.io` is often unreachable from a build host. Pull through a mirror and
retag to the canonical name, so the compose file keeps the real image name and
no mirror URL is committed:

```bash
docker pull ghcr.m.<mirror>/<owner>/<image>:<tag>
docker tag  ghcr.m.<mirror>/<owner>/<image>:<tag> ghcr.io/<owner>/<image>:<tag>
```

Pin the tag. `:latest` plus an unreachable registry means the build fails at
the `FROM` line with a TLS error that reads like a broken image, not a
network problem.

## Pointing the client at the local server

With a local Bot API sidecar, the client uses the local base URL and the
sidecar carries the proxy. The client must therefore reach the sidecar
**directly**:

- add the sidecar's service name to `NO_PROXY`;
- do **not** pass an explicit `proxy=` to the client's HTTP layer - in
  httpx-based clients that overrides `NO_PROXY` and pushes the local address
  out through the external proxy, where the container name cannot resolve. The
  failure is a `502` on every request.

Verify both halves separately: from the app container, the local health
endpoint answers directly; and the sidecar's own log shows it established the
MTProto connection through the proxy.

## Ordering when several services share a Bot API

If a service calls another's API over a proxy-mandatory endpoint, deploy the
caller first. A caller that does not send the proxy will be rejected by a
server that requires it, so deploying the server first breaks the caller.
