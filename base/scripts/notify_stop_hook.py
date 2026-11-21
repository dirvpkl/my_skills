#!/usr/bin/env python3
"""Stop-hook guard: the owner gets a TG notify for finished work (base Process item 9).

Fires on the harness Stop event. Resolves the project dir from
$ZCODE_PROJECT_DIR (fallback cwd). If a workplanx topic log was written
recently (< 15 min — a unit of work just wrapped) and no notify marker
(.workplanx/_notify.log, written by notify.py after each send) is newer
than that log write, injects a kick: send the owner a summary before
wrapping up. Work that continues ignores the kick; a sent notify silences
it until the next log write. Stale logs (> 45 min) are the metawatcher's
lane, not this hook's. Never blocks: empty output = pass.
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

FRESH_WINDOW = 900  # a log write newer than this counts as just-finished work


def project_dir() -> Path:
    return Path(os.environ.get("ZCODE_PROJECT_DIR") or os.getcwd())


def newest_log(wx: Path):
    logs = list(wx.glob("*/log.md"))
    if not logs:
        return None
    return max(logs, key=lambda p: p.stat().st_mtime)


def last_notify(wx: Path) -> float:
    marker = wx / "_notify.log"
    if not marker.is_file():
        return 0.0
    newest = 0.0
    for line in marker.read_text(encoding="utf-8", errors="ignore").splitlines():
        token = line.strip().split()
        if not token:
            continue
        try:
            newest = max(newest, datetime.fromisoformat(token[0]).timestamp())
        except ValueError:
            continue
    return newest


def main() -> None:
    wx = project_dir() / ".workplanx"
    if not wx.is_dir():
        return
    log = newest_log(wx)
    if log is None:
        return
    age = time.time() - log.stat().st_mtime
    if age > FRESH_WINDOW:
        return
    if last_notify(wx) >= log.stat().st_mtime:
        return
    minutes = max(1, int(age) // 60)
    kick = (
        f"notify-hook: topic '{log.parent.name}' logged work {minutes} min ago with no "
        "telegram notify after it. If this unit of work is complete, send the owner a "
        "summary via base scripts/notify.py before wrapping up; if work continues, "
        "ignore this kick."
    )
    print(json.dumps({"additionalContext": kick}))


if __name__ == "__main__":
    main()
