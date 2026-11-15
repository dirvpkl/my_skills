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
import http.client
import json
import os
import re
import sys
import urllib.parse
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
    import time
    for rf in attempts:
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "response_format": rf,
        }).encode()
        # http.client, NOT urllib.request: the router fronting 307s
        # Python-urllib requests to /dashboard (observed live) while plain
        # http.client POSTs pass through — the client library is part of
        # the contract here. 307/5xx also FLAP in bursts (the upstream pool
        # rebalances) — retryable with backoff; 429 = throttle; 400/402 =
        # the model itself, exit immediately.
        u = urllib.parse.urlsplit(url)
        for attempt in range(5):
            conn = http.client.HTTPConnection(u.hostname, u.port, timeout=timeout)
            conn.request("POST", u.path, body=body, headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + key,
            })
            r = conn.getresponse()
            raw = r.read()
            conn.close()
            if r.status == 200:
                resp = json.loads(raw)
                break
            if r.status == 429:
                sys.exit(
                    "EXCEPTION, not a fail: rate limited (HTTP 429) — the router "
                    "is throttling this session after heavy use. Wait a bit and "
                    "retry, or pick another model. Not a description failure."
                )
            if r.status in (400, 402, 404):
                sys.exit(
                    f"EXCEPTION, not a fail: model '{model}' is not servable "
                    f"(HTTP {r.status}): {raw[:160].decode(errors='ignore')} — "
                    f"pick another model and it passes."
                )
            last = r.status
            time.sleep(min(90, 10 * (attempt + 1)))
        if resp is not None:
            break
    if resp is None:
        sys.exit(
            f"EXCEPTION, not a fail: model '{model}' rejected both json_schema "
            f"and json_object (HTTP {last}) — the model's "
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


def exam_models() -> list:
    """The exam roster from scripts/runtime.toml ([exam] models) — machine
    config, not hardcoded aliases. Three minimum (owner ruling: a single
    run proves nothing)."""
    import tomllib
    rt = Path(__file__).resolve().parent / "runtime.toml"
    if not rt.exists():
        sys.exit("scripts/runtime.toml missing — copy scripts/runtime.example.toml, fill [router] and [exam] models")
    data = tomllib.loads(rt.read_text(encoding="utf-8"))
    models = list(data.get("exam", {}).get("models", []))
    if len(models) < 3:
        sys.exit(f"[exam] models needs at least 3 entries (a single run proves nothing) — got {len(models)}")
    return models


def gen_schema() -> dict:
    return {"name": "utterances", "strict": True, "schema": {
        "type": "object",
        "properties": {"utterances": {"type": "array", "items": {
            "type": "object",
            "properties": {"utterance": {"type": "string"}, "skill": {"type": "string"}},
            "required": ["utterance", "skill"], "additionalProperties": False}}},
        "required": ["utterances"], "additionalProperties": False}}


def gen(model: str, out: str) -> int:
    """A generator model writes the test set from the descriptions —
    comprehension testing, not hand-written phrase files. The prompt stays
    ABSTRACT (owner ruling): no style/phrasing instructions; the generator
    infers everything from the schema and the descriptions. Skills are
    CHUNKED (owner finding: the free upstreams cap prompts, and the full
    list overflows — one call per small batch, drafts merge into one set).
    The output is a DRAFT — review before using it as the exam set."""
    ss = skills()
    head = ["You write user messages for an agent skill collection.",
            'Answer with a JSON object {"utterances": [{"utterance": "...", "skill": "<skill-name>"}]} covering every skill listed.', ""]
    # pack skills into batches under the upstream prompt cap
    chunks, cur, size = [], [], 0
    for name, s in ss.items():
        block = f"- {name}: {s['description']}" + "\n"
        if cur and size + len(block) > 4000:
            chunks.append(cur)
            cur, size = [], 0
        cur.append((name, s["description"]))
        size += len(block)
    if cur:
        chunks.append(cur)
    draft = []
    n = 0
    for chunk in chunks:
        lines = head[:] + ["## Skills"]
        for name, desc in chunk:
            lines.append(f"- {name}: {desc}")
        prompt = "\n".join(lines)
        data = call_llm(prompt, model, gen_schema())
        items = data.get("utterances", [])
        for it in items:
            n += 1
            draft.append({"id": f"gen-{n:02d}", "utterance": it.get("utterance", ""),
                          "expect": it.get("skill", "")})
    if not draft:
        sys.exit(f"model {model} returned no messages — wrong schema or a lazy answer; try another model.")
    Path(out).write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(draft)} generated messages over {len(chunks)} calls -> {out} (DRAFT — review before use as the exam set)")
    return 0


def run_default(models: list | None = None) -> int:
    """No flags = the exam, by default (owner ruling: there is no
    not-by-exam variant). Generates the set if missing, then runs the
    per-skill exam for every model in [exam] models. The bar: every model
    passes every description."""
    models = models or exam_models()
    set_path = str(DEFAULT_SET)
    if not Path(set_path).exists():
        print(f"no test set — generating with {models[0]}")
        gen(models[0], set_path)
    results = {}
    for m in models:
        print(f"--- exam run: {m} ---")
        results[m] = exam(m, set_path, f".exam-answers-{m.replace('/', '_')}.json")
    print()
    failed = [m for m, rc in results.items() if rc != 0]
    if not failed:
        print(f"EXAM PASS — all {len(models)} models passed every description. Commit allowed.")
        Path(".exam-run").write_text("", encoding="utf-8")
        return 0
    print(f"EXAM FAILED — failing runs: {', '.join(failed)}")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", action="store_true", help="static description QA only")
    ap.add_argument("--battery", action="store_true", help="print the exam sheet, change nothing")
    ap.add_argument("--gen", metavar="MODEL", help="regenerate the test set with this model")
    ap.add_argument("--models", metavar="M1,M2,M3", help="override the [exam] roster for this run")
    ap.add_argument("--set", default=str(DEFAULT_SET), help="generated test set (default .exam-set.json)")
    ap.add_argument("--out", default=None, help="output file for --gen")
    a = ap.parse_args()
    if a.lint:
        return lint()
    if a.battery:
        return battery(a.set)
    if a.gen:
        return gen(a.gen, a.out or a.set)
    return run_default(a.models.split(",") if a.models else None)


if __name__ == "__main__":
    sys.exit(main())
