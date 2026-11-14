# code-quality — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Catch-and-reraise vs original propagate

**Good:** `JSONDecodeError` from the parser propagates as-is to the caller — it already names the line and the reason.
**Bad:** `try: parse(raw) except JSONDecodeError: raise` — a body that only re-raises the identical exception.
Rationale: catching is justified only by added context or a real recovery action; a re-raise adds a layer to unwrap and zero information — delete the try.

## No silent fallback for missing config

**Good:** `os.environ["BOT_TOKEN"]` at startup, raising when absent — the service refuses to half-start.
**Bad:** `os.environ.get("BOT_TOKEN", "dev-token")` — a default argument standing in for real config.
Rationale: a required value that fails loudly surfaces a real problem; a fallback hides it and quietly ships wrong credentials.

## Security flag surfaced, not fixed unasked

**Good:** "While refactoring I noticed the webhook endpoint has no auth or rate limiting — flagging it; say if you want it fixed."
**Bad:** silently bolting on middleware "since it's obviously needed" — or staying quiet to keep the diff scoped.
Rationale: the rule is flag proactively and let the user decide — neither silence nor an unasked fix; surfacing through fresh-eyes is relayed by the main agent.

## God-file split along real seams

**Good:** a 400-line script becomes `entry.py`, `config.py`, `client.py` — and the FastAPI app and the Celery worker stay separate services.
**Bad:** stuffing the task body into the API handler "since it's just a few lines".
Rationale: service separation and single responsibility are structural, not size-based; convenience bundling is the god-file failure at any scale.
