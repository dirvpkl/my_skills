#!/usr/bin/env python3
"""UserPromptSubmit decider: matches the incoming prompt against the chords
bindings with a decision model, injects the matched stack as a kick.

Fires on UserPromptSubmit. Reads the prompt from the event JSON on stdin
(defensive key lookup). The decision call is configured in the skill's own
runtime.toml (gitignored; tracked shape in runtime.example.toml):

  [decider]
  endpoint  = "<chat-completions base URL of the decision model>"
  api_key   = "<token>"          # optional; sent as Bearer
  model     = "<model id>"
  protocol  = "openai"           # one-shot classification adapter
  threshold = 0.75               # minimum confidence to inject

Missing config, an unreachable endpoint, or an unparsable answer = silent
pass — a decider never blocks a prompt. A match injects: chords-decider:
'<phrase>' -> load <stack> (p=…) — the agent still verifies against
chords.md; matching by MEANING stays the agent's job, the model only
nominates.
"""

import json
import sys
import tomllib
import urllib.request
from pathlib import Path

TIMEOUT = 6
THRESHOLD_DEFAULT = 0.75


def runtime() -> dict:
    cfg = Path(__file__).resolve().parent.parent / "runtime.toml"
    if not cfg.is_file():
        return {}
    try:
        with cfg.open("rb") as f:
            return (tomllib.load(f) or {}).get("decider") or {}
    except Exception:
        return {}


def prompt_from(payload: dict) -> str:
    for key in ("prompt", "prompt_text", "user_prompt", "text"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def chords_text() -> str:
    p = Path(__file__).resolve().parent.parent / "chords.md"
    return p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""


def decide(cfg: dict, prompt: str, chords: str) -> dict:
    body = json.dumps({
        "model": cfg.get("model", ""),
        "temperature": 0,
        "max_tokens": 120,
        "messages": [
            {"role": "system", "content":
                "You are a phrase-to-binding matcher. Given the user's message and the "
                "binding list, return STRICT JSON only: {\"match\": <phrase or null>, "
                "\"stack\": <skills to load or null>, \"confidence\": <0..1>}. Match by "
                "meaning, not literal words; no match -> match null."},
            {"role": "user", "content": f"Binding list:\n{chords}\n\nMessage:\n{prompt}"},
        ],
    }).encode()
    request = urllib.request.Request(
        cfg["endpoint"].rstrip("/") + "/chat/completions",
        data=body,
        headers={"Content-Type": "application/json",
                 **({"Authorization": f"Bearer {cfg['api_key']}"} if cfg.get("api_key") else {})})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        answer = json.load(response)["choices"][0]["message"]["content"]
    return json.loads(answer[answer.index("{"):answer.rindex("}") + 1])


def main() -> None:
    cfg = runtime()
    if not cfg.get("endpoint"):
        return
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    prompt = prompt_from(payload)
    chords = chords_text()
    if not prompt or not chords:
        return
    try:
        verdict = decide(cfg, prompt, chords)
    except Exception:
        return
    match = verdict.get("match")
    confidence = verdict.get("confidence") or 0
    if not match or float(confidence) < float(cfg.get("threshold", THRESHOLD_DEFAULT)):
        return
    stack = verdict.get("stack") or "the bound skill stack"
    print(json.dumps({"additionalContext":
        f"chords-decider: message matches binding '{match}' (p={confidence}) -> load {stack}. "
        "Verify against chords.md before acting; match by meaning stays yours."}))


if __name__ == "__main__":
    main()
