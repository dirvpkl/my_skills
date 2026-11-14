# Sensitive data memo — agent checklist, relayed 2026-11-14

> Source: a memo handed to the owner by another agent; preserved as the
> seed for the `boundaries` skill (see plan.md split proposal). Translated
> to English and sanitized: project-specific names and values replaced
> with generic placeholders; every rule and checklist item kept.

## Checklist: sensitive data in logs and chat

### 0. Golden rule
Anything that lands in chat or a transcript must be treated as compromised. Not "private, but careful" — compromised. A dialogue can be logged, stored, indexed. Hence the only question before every output: "if a stranger sees this — what can they do with it?"

### 1. What counts as sensitive

| Category | Examples from our project |
|---|---|
| Bot tokens | bot token leaked via a verbose HTTP client log (case #1) |
| Session tokens | session access tokens from an internal test panel |
| One-time codes | short-lived door-access codes (live ~60 seconds) |
| Personal identifiers | card number, phone, customer full name |
| Infrastructure secrets | passwords, keys, client_id+secret pairs |

The line: length, presence, shape, error code — not a secret. The value — a secret. `card_len: 10` — fine. `card: 7B7D...` — not fine.

### 2. Logs in code: three levels of protection

**Level 1 — silence chatty libraries** (our case: an HTTP client printing the full URL = token in the URL):

```python
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)      # python-telegram-bot
logging.getLogger("http.client").setLevel(logging.WARNING) # urllib in some versions
logging.getLogger("urllib3").setLevel(logging.WARNING)     # requests
```

**Level 2 — never interpolate a secret into a message:**

```python
# ❌ leaks
log.info(f"minted token: {token}")
log.info(f"request to {url}")            # url may contain ?token=...

# ✅ safe
log.info("minted fresh token (len=%d)", len(token))
log.info("request done: %s", url.split("?")[0])   # path without query
```

**Level 3 — a masking helper for every case:**

```python
def mask(value: str, keep: int = 4) -> str:
    if not value:
        return "(empty)"
    return value[:keep] + "…" + f"({len(value)} chars)"
```

### 3. Curl probes: filter BEFORE pasting into chat
Never paste raw curl output into a non-private chat. Pipe straight into a filter:

```bash
curl -s ... | python3 -c "import json,sys; d=json.load(sys.stdin); \
print('result:', d.get('result'), '| code:', d.get('code'), '| errors:', d.get('errors'))"
```

Print only the shape: result / code / errors / presence of fields / lengths. Field values that contain identifiers — do not print.

Entering secrets into a command — via `read -s` into an env variable, the value lives only in the shell:

```bash
read -s PHONE && curl -s ... -d "{\"phone\": \"$PHONE\"}" ...
```

And a check that it was picked up (without the value!): `echo "len: ${#PHONE}"`.

### 4. Files with secrets
- Do not cat token files "to check what's there". The check — by script, the output — boolean/length:

```python
env = open(r"path/.env").read()
print("token set:", bool(re.search(r"^BOT_TOKEN=\S+", env, re.M)))
```

- Filling in secrets — the user themselves (notepad/editor); the agent never sees them.
- `.env` in `.gitignore` always, before the first commit.

### 5. Docker specifics
- `env_file: .env` in compose — fine: the mechanism injects values into the container, nobody reads the file by eye.
- `docker logs` — a leak vector: any URLs, headers, bodies the library logged will spill out on the first inspection. Logs are a publication too.
- `docker compose restart` — safe: re-reads .env without printing anything. After changing a secret in .env — restart, not rebuild.
- After a token incident: rebuild does not help — the secret lived in the old container's stdout. Only revocation.

### 6. Leak protocol (order of actions)
1. Revoke immediately — for chat-platform bots: the platform's revoke flow (e.g. @BotFather → /revoke). A dead token in logs is just garbage.
2. Issue a new one, write it into the file (not the chat), restart the container.
3. Determine the blast radius: what else lived in that same output (phone? card? another token?).
4. Only then dig into how it leaked and set the filter — in the reverse order you will forget to revoke.

### 7. Checklist before every "show the output in chat"
- [ ] Is there a token/key/password in the output? (URLs too: `?token=`, Bearer headers)
- [ ] Is there personal data (phone, card number, full name, address)?
- [ ] Is there a value that can be used as me? (even one-time)
- [ ] Ran it through a filter that prints the shape, not the values?
- [ ] If it leaked anyway — is it revocable? (token — yes, card number — no!)
