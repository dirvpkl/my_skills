#!/usr/bin/env python3
"""Description quality tools — the collection's dev harness.

Everything runs THROUGH LLMs (owner ruling 2026-11-15: no hand-written
phrase files on disk — the fixtures file is gone). The pipeline:

  --gen MODEL [--out SET]      a generator model writes the test set
                               (user messages + the skill each belongs
                               to) — a DRAFT, review before use
  --exam MODEL [--set SET]     send the exam sheet (descriptions + the
                               set's user messages) to a bare model with
                               a forced answer schema; save answers
  --answers FILE [--set SET]   grade: exact-name compare, bar = 100% —
                               every miss is one description's failure
  --battery [--set SET]        print the exam sheet
  --lint                       static description QA

Machine facts resolve at RUNTIME (owner ruling: nothing machine-local is
hardcoded — a hardcoded endpoint breaks the project on any other machine):
env ROUTER_URL / ROUTER_API_KEY first, else scripts/runtime.toml
(gitignored; tracked shape: scripts/runtime.example.toml).
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SET = ROOT / ".exam-set.json"

VAGUE = ["when appropriate", "as needed", "use your judgment", "if needed",
         "when you see fit", "посчитаешь нужным"]
MAX_DESC = 1200


def router_creds() -> tuple:
    """(url, key) from the environment, else scripts/runtime.toml.
    Never hardcoded: the collection must work on any machine."""
    url = os.environ.get("ROUTER_URL")
    key = os.environ.get("ROUTER_API_KEY")
    rt = Path(__file__).resolve().parent / "runtime.toml"
    if (not url or not key) and rt.exists():
        for line in rt.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            m = re.match(r'^url\s*=\s*"([^"]+)"', line)
            if m and not url:
                url = m.group(1)
            m = re.match(r'^api_key\s*=\s*"([^"]+)"', line)
            if m and not key:
                key = m.group(1)
    if not url or not key:
        sys.exit(
            "router endpoint unknown — set ROUTER_URL / ROUTER_API_KEY in "
            "the environment, or fill scripts/runtime.toml (shape: "
            "scripts/runtime.example.toml). Machine values never enter "
            "tracked files."
        )
    if key.startswith("env:"):
        key = os.environ.get(key[4:], "")
        if not key:
            sys.exit("api_key is an env pointer but the variable is empty")
    return url, key


def call_llm(prompt: str, model: str, schema: dict | None = None, timeout: int = 600) -> dict:
    """One chat call with FORCED structured output: a json_schema (strict —
    the shape is guaranteed by constrained decoding) when the model
    supports it, json_object as the fallback. A model that rejects both is
    an exception, not a fail."""
    url, key = router_creds()
    attempts = []
    if schema:
        attempts.append({"type": "json_schema", "json_schema": schema})
    attempts.append({"type": "json_object"})
    last = None
    resp = None
    for rf in attempts:
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "response_format": rf,
        }).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                resp = json.loads(r.read())
            break
        except urllib.error.HTTPError as e:
            last = e
            if last.code == 429:
                sys.exit(
                    f"EXCEPTION, not a fail: rate limited (HTTP 429) — the router "
                    f"is throttling this session after heavy use. Wait a bit and "
                    f"retry, or pick another model. Not a description failure."
                )
            continue
    if resp is None:
        sys.exit(
            f"EXCEPTION, not a fail: model '{model}' rejected both json_schema "
            f"and json_object (HTTP {last.code if last else '?'}) — the model's "
            f"limit, not the test's; nothing to fix on our side. Pick another "
            f"model and it passes."
        )
    text = resp["choices"][0]["message"]["content"].strip()
    text = text[text.find("{"):text.rfind("}") + 1]
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit(
            f"EXCEPTION, not a fail: model '{model}' returned malformed JSON "
            f"({e}) — its limit, not the test's; pick another model and it passes."
        )


def load_set(path: str) -> list:
    p = Path(path)
    if not p.exists():
        sys.exit(
            f"test set not found: {p} — nothing is hand-written anymore. "
            f"Generate it first: python -X utf8 -I scripts/trigger_check.py "
            f"--gen <model> --out {p}"
        )
    return json.loads(p.read_text(encoding="utf-8"))


def skills():
    out = {}
    for d in sorted(ROOT.iterdir()):
        f = d / "SKILL.md"
        if not d.is_dir() or not f.exists() or d.name.startswith("."):
            continue
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not m:
            continue
        fm = m.group(1)
        name = re.search(r"^name: (\S+)", fm, re.M)
        desc = re.search(r"^description: (.*)$", fm, re.M)
        ver = re.search(r"^version: (\S+)", fm, re.M)
        if name and desc:
            out[name.group(1)] = {"description": desc.group(1).strip(),
                                  "version": ver.group(1) if ver else "?"}
    return out


def lint() -> int:
    issues = 0
    for name, s in skills().items():
        d = s["description"]
        low = d.lower()
        probs = []
        if len(d) > MAX_DESC:
            probs.append(f"description too long ({len(d)} > {MAX_DESC})")
        always_loaded = "always loaded" in low
        if not always_loaded and not re.search(r'"[^"]{3,}"', d):
            probs.append("no quoted literal user phrase")
        if not any(k in low for k in ("not for", "do not", "never", "not a ")):
            probs.append("no negative surfacing rule (NOT for / Do not / never)")
        for v in VAGUE:
            if v in low:
                probs.append(f"vague filler: {v!r}")
        if not re.search(r"ALWAYS invoke|ALWAYS load", d) and not always_loaded:
            probs.append("no ALWAYS-invoke imperative")
        if probs:
            issues += len(probs)
            print(f"FAIL {name}:")
            for pr in probs:
                print(f"  - {pr}")
        else:
            print(f"OK   {name} ({s['version']})")
    print(f"\n{issues} issue(s) found." if issues else "\nLint green: every description is a surfacing contract.")
    return 1 if issues else 0


def sheet_lines(fixtures: list) -> list:
    ss = skills()
    lines = ["You are an agent working in a chat with a user.",
             "The following skills are available for use with the Skill tool — invoke one by exact name when its description matches what the user needs; if no skill matches, just answer the user yourself.",
             'For each of the user messages below, name the ONE skill to invoke, or the word none. Answer with a JSON object {"<message number>": "<skill-or-none>"} only.', "",
             "## Skills"]
    for name, s in ss.items():
        lines.append(f"- {name} ({s['version']}): {s['description']}")
    lines += ["", "## User messages"]
    for i, fx in enumerate(fixtures, 1):
        lines.append(f"{i}. {fx['utterance']}")
    return lines


def battery(path: str) -> int:
    print("\n".join(sheet_lines(load_set(path))))
    return 0


def normalize(given, fixtures):
    """Models drift around the requested scheme: they answer with a list,
    wrap the object ({"answers": {...}}), key by utterance text instead of
    the number, or vary the case. Grading tolerates all of it — the scheme
    is the happy path, not a requirement the model must guess right."""
    if isinstance(given, list):
        return {str(i + 1): str(v) for i, v in enumerate(given)}
    if not isinstance(given, dict):
        return {}
    if isinstance(given.get("answers"), (dict, list)):
        return normalize(given["answers"], fixtures)
    by_text = {fx["utterance"]: str(i) for i, fx in enumerate(fixtures, 1)}
    out = {}
    for k, v in given.items():
        out[str(by_text.get(k, k))] = v
    return out


def answers(path: str, set_path: str) -> int:
    """The bar is 100%: each test message checks one skill's description in
    isolation, so any miss is that description's failure."""
    ap = Path(path)
    if not ap.exists():
        sys.exit(f"answers file not found: {path} — run --exam first (it writes the answers file)")
    raw = json.loads(ap.read_text(encoding="utf-8"))
    fixtures = load_set(set_path)
    given = normalize(raw, fixtures)
    correct = 0
    width = max(len(fx.get("id", "?")) for fx in fixtures)
    for i, fx in enumerate(fixtures, 1):
        got = str(given.get(str(i), given.get(fx.get("id", ""), given.get(fx["utterance"], "<missing>")))).strip()
        expected = fx.get("accept", [fx["expect"]])
        ok = got.lower() in [e.lower() for e in expected]
        correct += ok
        mark = "PASS" if ok else "FAIL"
        print(f"{mark}  {fx.get('id', str(i)).ljust(width)}  {fx['utterance'][:44]!r}")
        if not ok:
            print(f"      expected {' / '.join(expected)} — got {got!r}")
    print(f"\n{correct}/{len(fixtures)} — the bar is {len(fixtures)}/{len(fixtures)}.")
    return 0 if correct == len(fixtures) else 1


def gen_schema() -> dict:
    return {"name": "utterances", "strict": True, "schema": {
        "type": "object",
        "properties": {"utterances": {"type": "array", "items": {
            "type": "object",
            "properties": {"utterance": {"type": "string"}, "skill": {"type": "string"}},
            "required": ["utterance", "skill"], "additionalProperties": False}}},
        "required": ["utterances"], "additionalProperties": False}}


def gen(model: str, out: str) -> int:
    """A generator model writes the test set from the descriptions:
    comprehension testing, not hand-written phrase files. The prompt stays
    ABSTRACT (owner ruling): no style/phrasing instructions — the
    generator infers everything from the schema and the descriptions.
    Concrete guidance would only be allowed as examples, and examples are
    skipped here: these are tests, token cost matters. The output is a
    DRAFT — review before using it as the exam set."""
    ss = skills()
    lines = ["You write user messages for an agent skill collection.",
             'Answer with a JSON object {"utterances": [{"utterance": "...", "skill": "<skill-name>"}]} covering every skill listed.', "",
             "## Skills"]
    for name, s in ss.items():
        lines.append(f"- {name}: {s['description']}")
    data = call_llm("\n".join(lines), model, gen_schema())
    items = data.get("utterances", [])
    if not items:
        sys.exit(f"model '{model}' returned no messages — wrong schema or a lazy answer; try another model.")
    draft = [{"id": f"gen-{i:02d}", "utterance": it.get("utterance", ""),
              "expect": it.get("skill", "")} for i, it in enumerate(items, 1)]
    Path(out).write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(draft)} generated messages -> {out} (DRAFT — review before use as the exam set)")
    return 0


def answers_schema(count: int) -> dict:
    """strict: true with every message number declared — the model cannot
    add a "reason" field, skip a number, or change a key type. Built per
    set size, since strict requires all keys declared."""
    props = {str(i): {"type": "string"} for i in range(1, count + 1)}
    return {"name": "routing", "strict": True, "schema": {
        "type": "object", "properties": props,
        "required": list(props.keys()), "additionalProperties": False}}


def exam(model: str, set_path: str, out: str) -> int:
    """Send the sheet to one bare model with a forced answer schema and
    save its answers for --answers grading. Three models minimum (owner
    ruling); a single run proves nothing."""
    fixtures = load_set(set_path)
    data = call_llm("\n".join(sheet_lines(fixtures)), model, answers_schema(len(fixtures)))
    Path(out).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"answers ({model}) -> {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", action="store_true")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--answers", metavar="FILE")
    ap.add_argument("--gen", metavar="MODEL")
    ap.add_argument("--exam", metavar="MODEL")
    ap.add_argument("--set", default=str(DEFAULT_SET), help="generated test set (default .exam-set.json)")
    ap.add_argument("--out", default=None, help="output file for --gen / --exam")
    a = ap.parse_args()
    if a.lint:
        return lint()
    if a.battery:
        return battery(a.set)
    if a.answers:
        return answers(a.answers, a.set)
    if a.gen:
        return gen(a.gen, a.out or str(DEFAULT_SET))
    if a.exam:
        return exam(a.exam, a.set, a.out or "answers.json")
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
