# proxy-egress — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Ask where the proxy lives, never assume

**Good:** before writing config, ask for the host, port, scheme, credential and
whether the login selects an exit pool — then verify the credential with one
call before wiring it in.
**Bad:** hardcoding `http://10.0.0.5:8080` from a previous project's compose
file because "it's probably the same proxy."
Rationale: the proxy is the owner's environment, not the project's; a guessed
address fails as a timeout or, worse, silently connects direct.

**Good:** the login is not registered yet and returns its distinct error → say
so and stop, instead of retrying with variations.
**Bad:** "the proxy is probably fine" and wiring it anyway.
Rationale: a missing proxy is a deployment error; discovering it after the code
is written costs a second pass over every client.

## No silent fallback

**Good:** a missing `PROXY_URL` raises at startup with the variable name and
where it is read, before any container starts.
**Bad:** `PROXY_URL or None` passed to the client, which treats `None` as
"connect directly" — the deployment looks healthy and leaks the host IP.
Rationale: the failure mode this skill exists for is a fallback that works, so
the only acceptable missing-proxy behavior is a loud stop.

**Good:** the retry path that gives up and would have connected direct now
raises instead.
**Bad:** a cooldown branch that "degrades gracefully" to a direct connection.
Rationale: graceful degradation is the bug; every path either proxies or fails.

## Prove it in the running container

**Good:** from inside the built container, external traffic resolves to the
proxy's exit IP and every `NO_PROXY` target still answers directly.
**Bad:** the compose file says `HTTP_PROXY` and the service starts — declared,
therefore assumed working.
Rationale: static review cannot see a library ignoring the environment; only
the exit IP proves routing.
