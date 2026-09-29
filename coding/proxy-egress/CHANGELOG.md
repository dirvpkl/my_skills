# Changelog

## [1.0.1] - 2026-09-29
- Added the silent-fallbacks grep catalog, the failure-signature table, and the ask-where-the-proxy-lives rule.


All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job (that belongs in a dedicated references/ file — see references/anti-patterns.md in skill-scaffolder for why these should stay separate).

## 1.0.0 — 2026-09-29
- Initial version. Distilled from enforcing mandatory proxy egress across a dozen
  real services.
- `references/client-matrix.md` — per-library behavior for httpx, aiohttp,
  requests, urllib3, curl_cffi, Go, Telethon (sync and async), PTB, aiogram,
  yt-dlp, streamlink, ffmpeg, Playwright.
- `references/silent-fallbacks.md` — the fallback catalog with grep patterns,
  plus deployment-shaped traps (required compose form, dependency declared in
  the wrong place, cache volume on the wrong path, port collision, exhausted
  Docker address pools).
- `references/verification.md` — live verification order and a failure-signature
  table.
- Depends on `security` (credentials, never printed), `docker` (required
  compose vars) and `code-quality` (fail-loud as the canonical definition).
- Paths to the user's proxy service are deliberately absent: the skill asks
  where it lives instead of hardcoding it.
