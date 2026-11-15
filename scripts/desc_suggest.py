#!/usr/bin/env python3
"""desc_suggest — a model drafts description variants, alternative names,
and extra user phrases for one skill (owner idea 2026-11-15: the tool
family around the exam — generators, suggesters).

Usage:
    python -X utf8 -I scripts/desc_suggest.py --skill NAME --purpose "what the skill does" [--model auto/best-reasoning]

Output: JSON printed pretty — description drafts (each satisfying the lint
contract: quoted user phrase, negative NOT-for, ALWAYS-invoke imperative,
no vague filler), alternative names, extra user phrases. The owner picks;
nothing is applied by the tool itself.
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUTER_URL = "http://127.0.0.1:20128/v1/chat/completions"


SUGGEST_SCHEMA = {"name": "suggestions", "strict": True, "schema": {
    "type": "object",
    "properties": {
        "descriptions": {"type": "array", "items": {"type": "string"}},
        "alt_names": {"type": "array", "items": {"type": "string"}},
        "user_phrases": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["descriptions", "alt_names", "user_phrases"],
    "additionalProperties": False}}


def call_llm(prompt: str, model: str, timeout: int = 600) -> dict:
    key_line = ""
    rt = ROOT / "roi" / "runtime.toml"
    for line in rt.read_text(encoding="utf-8").splitlines():
        if line.startswith("api_key"):
            key_line = line.split('"')[1]
            break
    if not key_line:
        sys.exit("router key not found — expected roi/runtime.toml [router] api_key")
    attempts = [{"type": "json_schema", "json_schema": SUGGEST_SCHEMA},
                {"type": "json_object"}]
    last = None
    for rf in attempts:
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
            "response_format": rf,
        }).encode()
    req = urllib.request.Request(ROUTER_URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key_line,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read())
        break
    except urllib.error.HTTPError as e:
        last = e
        continue
    sys.exit(
        f"EXCEPTION, not a fail: model '{model}' rejected both json_schema and "
        f"json_object (HTTP {last.code}) — pick another model and it passes."
    )
    text = resp["choices"][0]["message"]["content"].strip()
    text = text[text.find("{"):text.rfind("}") + 1]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit(f"EXCEPTION, not a fail: model '{model}' returned malformed JSON — "
            f"pick another model and it passes.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True)
    ap.add_argument("--purpose", required=True, help="what the skill does, one sentence")
    ap.add_argument("--model", default="auto/best-reasoning")
    a = ap.parse_args()

    prompt = (
        "You draft skill descriptions for an agent skill collection.\n"
        "Contract every draft MUST satisfy:\n"
        "- one paragraph, max 1200 chars\n"
        "- contains at least one QUOTED literal user phrase that should invoke it\n"
        "- contains a negative: NOT for / Do not / never (when it must NOT load)\n"
        "- contains an imperative with ALWAYS invoke or ALWAYS load\n"
        "- no vague filler (\"when appropriate\", \"as needed\", \"use your judgment\")\n"
        "- improve CLARITY, do not stuff keyword variants — phrases are unbounded and keyword stuffing fakes the pass\n\n"
        f"Skill name: {a.skill}\n"
        f"What it does: {a.purpose}\n\n"
        'Answer with a JSON object only:\n'
        '{"descriptions": ["<draft1>", "<draft2>", "<draft3>"],\n'
        ' "alt_names": ["<name>", ...],\n'
        ' "user_phrases": ["<phrase>", ...]}\n'
        "descriptions: 3 drafts. alt_names: 5 alternative skill names with one-phrase rationale each (format: 'name — why'). user_phrases: 5 casual RU/EN utterances that should invoke it."
    )
    data = call_llm(prompt, a.model)

    print(f"# desc_suggest — {a.skill} (model: {a.model})\n")
    for i, d in enumerate(data.get("descriptions", []), 1):
        print(f"## description draft {i}\n{d}\n")
    print("## alternative names")
    for n in data.get("alt_names", []):
        print(f"- {n}")
    print("\n## user phrases (candidate fixtures)")
    for ph in data.get("user_phrases", []):
        print(f"- {ph}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
