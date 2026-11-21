#!/usr/bin/env python3
"""Stop-hook sweep: fresh #slot / #harvest / #gem / #open lines from the
project's workplanx topics become Planka cards, so the board is the owner's
forgotten-things surface (third-light bridge wild-shot, owner-approved
2026-11-22).

Fires on Stop. Resolves the project dir from $ZCODE_PROJECT_DIR (fallback
cwd), scans .workplanx/*/log.md and */afterword.md for tag lines, and POSTs
one card per not-yet-swept line to the lists configured in the skill's own
runtime.toml (gitignored; tracked shape in runtime.example.toml):

  [planka]
  url             = "http://127.0.0.1:23333"   # pinned by the owner
  api_token       = "<Planka access token>"
  harvest_list_id = "..."   # Собрано (harvest): #harvest, #gem
  queue_list_id   = "..."   # Очередь (queue): #slot, #open

The board/lists are the pass-built «wildshots dispatch» board — ids live in
runtime.toml, no discovery. Swept lines are remembered in
<project>/.workplanx/_planka-swept.json (keyed by a content hash, so edited
lines sweep again). Planka down, credentials missing, or any API error =
silent pass — a sweep never blocks a Stop.
"""

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

TAGS = ("#slot", "#harvest", "#gem", "#open")
TIMEOUT = 8


def runtime() -> dict:
    cfg = Path(__file__).resolve().parent.parent / "runtime.toml"
    try:
        import tomllib
        with cfg.open("rb") as f:
            return (tomllib.load(f) or {}).get("planka") or {}
    except Exception:
        return {}


def project_dir() -> Path:
    return Path(os.environ.get("ZCODE_PROJECT_DIR") or os.getcwd())


def scan_tags(wx: Path) -> dict[str, tuple[str, str, str]]:
    """{line_hash: (tag, source_ref, line)} from topic log/afterword files."""
    found: dict[str, tuple[str, str, str]] = {}
    for topic in sorted(p for p in wx.iterdir() if p.is_dir()):
        for name in ("log.md", "afterword.md"):
            f = topic / name
            if not f.is_file():
                continue
            try:
                lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for line in lines:
                low = line.lower()
                tag = next((t for t in TAGS if t in low), None)
                if not tag or not line.strip():
                    continue
                key = hashlib.sha256(f"{f}|{line}".encode()).hexdigest()[:16]
                ref = f"{topic.name}/{name}"
                found[key] = (tag, ref, f"[{tag}] {line.strip()[:280]} ({ref})")
    return found


def swept_keys(wx: Path) -> set[str]:
    state = wx / "_planka-swept.json"
    if not state.is_file():
        return set()
    try:
        return set(json.loads(state.read_text(encoding="utf-8")))
    except Exception:
        return set()


def mark_swept(wx: Path, keys: list[str]) -> None:
    state = wx / "_planka-swept.json"
    known = swept_keys(wx)
    try:
        state.write_text(json.dumps(sorted(known | set(keys))), encoding="utf-8")
    except OSError:
        pass


def api(url: str, token: str, method: str, path: str, payload: dict | None = None):
    request = urllib.request.Request(
        url.rstrip("/") + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method=method)
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.load(response)


def main() -> None:
    cfg = runtime()
    required = ("url", "api_token", "harvest_list_id", "queue_list_id")
    if not all(cfg.get(k) for k in required):
        return  # not provisioned yet — silent
    url, token = cfg["url"], cfg["api_token"]
    wx = project_dir() / ".workplanx"
    if not wx.is_dir():
        return
    found = scan_tags(wx)
    known = swept_keys(wx)
    fresh = {k: v for k, v in found.items() if k not in known}
    if not fresh:
        return
    list_for = {"#harvest": cfg["harvest_list_id"], "#gem": cfg["harvest_list_id"],
                "#slot": cfg["queue_list_id"], "#open": cfg["queue_list_id"]}
    done = []
    try:
        # 2.x demands an explicit position: append after the last card of each list
        positions = {}
        for lid in set(list_for.values()):
            try:
                cards = api(url, token, "GET", f"/api/lists/{lid}/cards")
                items = cards.get("items", []) if isinstance(cards, dict) else cards
                positions[lid] = max((c.get("position") or 0 for c in items), default=0) + 65536
            except Exception:
                positions[lid] = 65536
        for key, (tag, ref, text) in fresh.items():
            lid = list_for[tag]
            api(url, token, "POST", f"/api/lists/{lid}/cards",
                {"type": "story", "position": positions[lid], "name": text[:120],
                 "description": f"{text}\n\nsource: {ref}"})
            positions[lid] += 65536
            done.append(key)
        mark_swept(wx, done)
    except Exception:
        return  # fail-pass: retry next Stop


if __name__ == "__main__":
    main()
