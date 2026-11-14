# Telegram forum topics — canonical example

Copy this, don't re-derive from memory. Thread routing breaks when the agent
freestyles `message_thread_id` / `parse_mode` params.

## Setup (once, by hand)

1. Create a supergroup, enable **Topics** (forum mode).
2. Create three topics: `critical`, `info`, `service`. Copy their thread IDs
   (the number after `?thread=` in a copied message link, or via `getForumTopic`).
3. Put IDs in config, never in code:

```env
TG_BOT_TOKEN=...
TG_ALERT_CHAT_ID=-1001234567890
TG_TOPIC_CRITICAL=1
TG_TOPIC_INFO=2
TG_TOPIC_SERVICE=3
UPTIME_KUMA_PUSH_URL=https://kuma.example.com/api/push/xxxx?status=up&msg=ok&ping=
```

## Sending (python-telegram-bot v21+, async)

```python
from telegram import Bot
from telegram.constants import ParseMode

async def _send(bot: Bot, chat_id: int, thread_id: int, text: str) -> None:
    await bot.send_message(
        chat_id=chat_id,
        message_thread_id=thread_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        disable_web_page_preview=True,
    )

# critical — needs human now, short + loud
# Escape per MarkdownV2 rules before calling.
async def alert_critical(bot: Bot, cfg, text_md_escaped: str) -> None:
    await _send(bot, cfg.tg_alert_chat_id, cfg.tg_topic_critical, text_md_escaped)

# info — mandatory operational events (started / finished / posted N items)
async def alert_info(bot: Bot, cfg, text_md_escaped: str) -> None:
    await _send(bot, cfg.tg_alert_chat_id, cfg.tg_topic_info, text_md_escaped)

# service — parser stats, polling noise, retries kicked in
async def alert_service(bot: Bot, cfg, text_md_escaped: str) -> None:
    await _send(bot, cfg.tg_alert_chat_id, cfg.tg_topic_service, text_md_escaped)
```

## Level rules

- `critical`: crashes, security, kuma-down, config missing. Always + log ERROR.
- `info` (mandatory, spammy by default): service started/finished, posted batch,
  scheduler tick summary. Always + log INFO. Stays on unless the user explicitly
  asked to remove it — never throttle on the agent's own initiative.
- `service` (spammy by default): per-item parser lines, retry warnings, transient
  noise. Aggregate per N minutes to keep threads readable, but keep it on unless
  the user opted out. Still + log WARNING on retry.

## Anti-patterns

- One chat with no threads — `critical` drowns in noise. Banned.
- Hand-rolled `requests.post("https://api.telegram.org/...")` — use the bot lib,
  it owns retry/backoff. Banned.
- Hardcoded chat/thread IDs in code — config only. Banned.
- `parse_mode="Markdown"` (legacy) mixed with V2 escaping — pick
  `MARKDOWN_V2` and escape, or `HTML`. Don't mix.
