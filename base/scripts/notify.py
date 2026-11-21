#!/usr/bin/env python3
"""Notify the owner through Telegram — base's standing channel.

WHEN
  Every finished unit of harness work gets exactly one summary here: a task
  closed, a card done, a long job ended. Also the way to reach the owner
  mid-work when the session is unattended and a decision is needed.
  Delegated agents do NOT call this script — they stay in the workplanx log;
  the orchestrator sends.

USAGE
  python notify.py "text"                        # info thread (default)
  python notify.py --critical "text"             # critical thread
  python notify.py "text" -m shot.png out.zip    # text + media files
  python notify.py --from "label" "text"         # override the origin stamp

ORIGIN
  Every message is auto-stamped with where it came from:
  "<project> (<topic>)" — project = the caller's cwd basename, topic =
  $WORKPLANX_TOPIC when the session pins one. --from "label" overrides
  the stamp, --from "" removes it. Mandatory by construction — the agent
  never has to remember it. The label rides as a bold header in rich
  sends and as a "<label>: " prefix in plain fallbacks and captions.

FORMATTING
  Text sends go through sendRichMessage as markdown (Bot API 10.1): the
  body renders rich — bullets, backticks, bold, tables — with no escaping
  anywhere. Captions stay plain text. If the endpoint predates Bot API
  10.1 the send falls back to plain text and a note lands on stderr.

MARKER
  After a successful send the script appends a timestamped line to
  .workplanx/_notify.log (when a topic folder exists) — the notify
  stop-hook reads it to tell finished-and-notified from finished-and-silent.

LEVELS
  info     — finished-work summaries, status reports (the default).
  critical — the owner is needed now: crash, blocker, exposed secret.
  Level policy behind the threads:
  coding/external-integrations/references/telegram-topics.md

MEDIA
  -m takes one or more file paths (relative to the caller's cwd). Images
  (jpg/png/webp) go as photos, everything else as documents. One media file
  carries the stamped message as its caption when it fits (<= 1024 chars);
  otherwise the text goes as its own message first and media follow
  without captions.

CONFIG
  ../runtime.toml (gitignored), section [tg]: bot_token, chat_id,
  topic_critical, topic_info. Missing file or keys = exit 2 with a clear
  message. The token is never printed. HTTP(S)_PROXY env vars are honored
  by urllib automatically.

FAIL LOUD
  Any send failure = nonzero exit + reason on stderr. A summary the channel
  lost is reported to the caller, never swallowed.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
import tomllib
import urllib.error
import urllib.request
import uuid
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent / "runtime.toml"
API_URL = "https://api.telegram.org/bot{token}/{method}"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
CAPTION_LIMIT = 1024
TEXT_LIMIT = 4000
TIMEOUT = 30

REQUIRED_KEYS = ("bot_token", "chat_id", "topic_critical", "topic_info")


def fail(message: str, code: int) -> None:
    print(f"notify: {message}", file=sys.stderr)
    sys.exit(code)


def load_config() -> dict:
    try:
        with CONFIG.open("rb") as f:
            cfg = tomllib.load(f)
    except FileNotFoundError:
        fail(f"config not found: {CONFIG} — copy runtime.example.toml beside it and fill [tg]", 2)
    tg = cfg.get("tg") or {}
    missing = [k for k in REQUIRED_KEYS if not tg.get(k)]
    if missing:
        fail(f"config missing [tg] keys: {', '.join(missing)} ({CONFIG})", 2)
    return tg


def _multipart(fields: dict) -> tuple[str, bytes]:
    boundary = "----zcode" + uuid.uuid4().hex
    body = bytearray()
    for name, value in fields.items():
        body += f"--{boundary}\r\n".encode()
        if isinstance(value, tuple):
            filename, data = value
            body += (
                f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'
                "Content-Type: application/octet-stream\r\n\r\n"
            ).encode()
            body += data + b"\r\n"
        else:
            body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
    body += f"--{boundary}--\r\n".encode()
    return boundary, bytes(body)


def api(tg: dict, method: str, soft_404: bool = False, **fields) -> dict | bool:
    """POST one Bot API call. Returns the result JSON on success; returns
    False only when soft_404 is set and the endpoint lacks the method
    (formatting fallbacks). Everything else fails loud."""
    boundary, body = _multipart(fields)
    request = urllib.request.Request(
        API_URL.format(token=tg["bot_token"], method=method),
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        if soft_404 and error.code == 404:
            return False
        detail = error.read().decode("utf-8", "replace")[:300]
        fail(f"{method} -> HTTP {error.code}: {detail}", 1)
    except OSError as error:
        fail(f"{method} -> network error: {error}", 1)
    if not result.get("ok"):
        fail(f"{method} -> telegram rejected the send: {result}", 1)
    return result


def send_text(tg: dict, thread, label: str, body: str) -> None:
    """Text send: markdown via sendRichMessage, plain fallback without it."""
    header = f"**{label}**" if label else ""
    markdown = f"{header}\n\n{body}".strip() if body else header
    plain = f"{label}: {body}".strip() if body else label
    sent_rich = markdown and api(
        tg, "sendRichMessage", chat_id=tg["chat_id"], message_thread_id=str(thread),
        rich_message=json.dumps({"markdown": markdown}), soft_404=True)
    if not sent_rich:
        if markdown != plain:
            print("notify: rich send unavailable here — sent plain text", file=sys.stderr)
        api(tg, "sendMessage", chat_id=tg["chat_id"], message_thread_id=str(thread),
            text=plain, disable_web_page_preview="true")


def send_media(tg: dict, thread, path: Path, caption: str | None) -> None:
    try:
        data = path.read_bytes()
    except OSError as error:
        fail(f"cannot read media file {path}: {error}", 2)
    method = "sendPhoto" if path.suffix.lower() in IMAGE_EXTS else "sendDocument"
    field = "photo" if method == "sendPhoto" else "document"
    fields = {
        "chat_id": tg["chat_id"],
        "message_thread_id": str(thread),
        field: (path.name, data),
    }
    if caption:
        fields["caption"] = caption
    api(tg, method, **fields)


def origin_stamp(from_label: str | None) -> str:
    """Origin label carried by every message: project (topic)."""
    if from_label is not None:
        return from_label
    topic = os.environ.get("WORKPLANX_TOPIC", "").strip()
    if topic:
        return f"{Path.cwd().name} ({topic})"
    return f"{Path.cwd().name}"


def mark_sent(thread) -> None:
    """Append a timestamp marker so the stop-hook can tell notifies happened."""
    marker = Path.cwd() / ".workplanx" / "_notify.log"
    if not marker.parent.is_dir():
        return  # no topic folder here — the notify hook skips markerless projects
    with marker.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} thread={thread}\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("text", nargs="*", help="summary text")
    parser.add_argument("--critical", action="store_true",
                        help="send to the critical thread instead of info")
    parser.add_argument("-m", "--media", nargs="+", type=Path, metavar="FILE",
                        help="media files to attach (images as photos, rest as documents)")
    parser.add_argument("--from", dest="from_label", default=None, metavar="LABEL",
                        help='override the origin stamp (empty string removes it)')
    args = parser.parse_args()

    text = "\n".join(args.text).strip()
    media = args.media or []
    if not text and not media:
        parser.error("nothing to send — pass a text and/or -m FILE ...")
    for path in media:
        if not path.is_file():
            fail(f"media file not found: {path}", 2)

    tg = load_config()
    thread = tg["topic_critical"] if args.critical else tg["topic_info"]

    label = origin_stamp(args.from_label)
    plain = f"{label}: {text}".strip() if text else label
    if plain and len(plain) > TEXT_LIMIT:
        fail(f"message is {len(plain)} chars, limit is {TEXT_LIMIT} — shorten the summary", 2)

    text_sent = False
    if not media or len(media) > 1 or len(plain) > CAPTION_LIMIT:
        if label or text:
            send_text(tg, thread, label, text)
        text_sent = True
    caption = None
    if len(media) == 1 and not text_sent:
        caption = plain
    for index, path in enumerate(media):
        send_media(tg, thread, path, caption if index == 0 else None)
    mark_sent(thread)
    print(f"notify: sent to {'critical' if args.critical else 'info'}"
          f" ({len(media)} media)")


if __name__ == "__main__":
    main()
