#!/usr/bin/env python3
"""SessionStart bootstrapper: injects the project's workplanx state so a fresh
agent starts FROM the playground, not from zero.

Fires on SessionStart (startup/resume/clear/compact — compaction included, so
the state comes back after a context reset). Resolves the project dir from
$ZCODE_PROJECT_DIR (fallback cwd), reads .workplanx: topic count, newest topic
with its last-activity age, inbox file count. Injects one compact state line
via additionalContext. Errors stay silent — a bootstrapper never blocks a
session start.
"""

import json
import os
import time
from pathlib import Path


def project_dir() -> Path:
    return Path(os.environ.get("ZCODE_PROJECT_DIR") or os.getcwd())


def main() -> None:
    wx = project_dir() / ".workplanx"
    if not wx.is_dir():
        return
    name = project_dir().name
    topics = [p for p in wx.iterdir() if p.is_dir() and (p / "log.md").exists()]
    parts = [f"project {name}"]
    if topics:
        newest = max(topics, key=lambda p: (p / "log.md").stat().st_mtime)
        age = int((time.time() - (newest / "log.md").stat().st_mtime) // 60)
        when = "just now" if age < 1 else f"{age} min ago"
        parts.append(
            f"workplanx: {len(topics)} topic(s), newest '{newest.name}' (activity {when})"
            " — work FROM the topic folder and INTO it")
    else:
        parts.append("workplanx: no topics yet — open one before project-scale work")
    inbox = wx / "_inbox"
    if inbox.is_dir():
        entries = sorted(inbox.glob("*.md"))
        if entries:
            parts.append(f"inbox: {len(entries)} owner-message file(s), latest {entries[-1].name}")
    print(json.dumps({"additionalContext": "bootstrapper: " + "; ".join(parts) + "."}))


if __name__ == "__main__":
    main()
