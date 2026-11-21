#!/usr/bin/env python3
"""PreToolUse guard: hard-enforces the boundaries never-do list for Bash commands.

Fires on PreToolUse for the Bash tool (matcher "Bash"). Reads the command from
the event JSON on stdin (defensive key lookup: tool_input.command /
tool_input.cmd / command). Denies by exit code 2 with the reason on stderr —
the documented block mechanism; anything else passes silently (exit 0, no
output).

Deny set (the never-do list entries a yolo session would otherwise run
without a prompt):
- git push with --force / --force-with-lease / -f — needs the owner's explicit yes
- git reset --hard — destroys uncommitted work
- rm -rf/-fr on /, ~, $HOME, %USERPROFILE%, C:\ or a bare * — host-level destruction
- git branch -D — branch deletion needs explicit owner confirmation

Not a permission-system replacement: narrow, pattern-level, fail-pass — an
unparseable command is allowed, not blocked.
"""

import json
import re
import sys

RULES = [
    (r"\bgit\s+(?:-\S+\s+\S+\s+)*push\b[^&|;]*(--force(-with-lease)?|\s-f(?:\s|$))",
     "force-push needs the owner's explicit yes (boundaries never-do)"),
    (r"\bgit\s+(?:-\S+\s+\S+\s+)*reset\s+--hard\b",
     "git reset --hard destroys uncommitted work (boundaries never-do)"),
    (r"\brm\s+(-\w*r\w*f\b|-\w*f\w*r\b)\s+(\"?(/|~|\$HOME|%USERPROFILE%|C:[/\\])\"?|\*)",
     "rm -rf on a root-ish path is host-level destruction (boundaries never-do)"),
    (r"\bgit\s+(?:-\S+\s+\S+\s+)*branch\s+-D\b",
     "git branch -D needs explicit owner confirmation (boundaries never-do)"),
]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    data = payload.get("tool_input") or payload
    if not isinstance(data, dict):
        return
    command = data.get("command") or data.get("cmd") or ""
    if not isinstance(command, str):
        return
    for pattern, reason in RULES:
        if re.search(pattern, command):
            print(f"pretooluse-guard: {reason} — ask the owner first", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
