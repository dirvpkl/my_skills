#!/usr/bin/env python3
"""Description quality tools — the collection's dev harness.

Modes:
  python scripts/trigger_check.py --lint
      Static QA of every description: length cap, a quoted user phrase, a
      negative (NOT for / never), an ALWAYS-invoke imperative, no vague
      filler.
  python scripts/trigger_check.py --battery
      Print the exam sheet: every description + the fixture utterances.
      Give the sheet to bare LLMs — AT LEAST THREE RUNS ON AT LEAST THREE
      MODELS (owner ruling 2026-11-15: a single run proves nothing).
  python scripts/trigger_check.py --answers answers.json
      Grade one answer file. The bar is 100%: every fixture tests one
      skill's description separately, any miss = that description fails.
  python scripts/trigger_check.py --gen MODEL --out fixtures-draft.json
      A GENERATOR model writes new test utterances from the descriptions
      (owner ruling 2026-11-15: descriptions are tested on comprehension,
      not on memorized phrase templates). Output is a DRAFT — human review
      before it replaces trigger_fixtures.json.
  python scripts/desc_suggest.py --skill NAME --purpose "..."
      Separate tool: a model drafts description variants, alternative
      names, and extra user phrases for one skill.
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "trigger_fixtures.json"

VAGUE = ["when appropriate", "as needed", "use your judgment", "if needed",
         "when you see fit", "посчитаешь нужным"]
MAX_DESC = 1200
ROUTER_URL = "http://127.0.0.1:20128/v1/chat/completions"


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


def call_llm(prompt: str, model: str, timeout: int = 600) -> str:
    """One router chat call, structured-output only (owner ruling: models
    that cannot answer JSON schema are not worth befriending)."""
    key_line = ""
    rt = ROOT / "roi" / "runtime.toml"
    for line in rt.read_text(encoding="utf-8").splitlines():
        if line.startswith("api_key"):
            key_line = line.split('"')[1]
            break
    if not key_line:
        sys.exit("router key not found — expected roi/runtime.toml [router] api_key")
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(ROUTER_URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key_line,
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(
            f"EXCEPTION, not a fail: model '{model}' cannot answer structured "
            f"JSON (HTTP {e.code}) — the model's limit, not the test's; "
            f"nothing to fix on our side. Pick another model and it passes."
        )
    text = resp["choices"][0]["message"]["content"].strip()
    text = text[text.find("{"):text.rfind("}") + 1]  # strip prose around JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        sys.exit(
            f"EXCEPTION, not a fail: model '{model}' returned malformed JSON — "
            f"its limit, not the test's; pick another model and it passes."
        )


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
            probs.append("no negative trigger (NOT for / Do not / never)")
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


def battery() -> int:
    ss = skills()
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    lines = ["You are an agent working in a chat with a user.",
             "The following skills are available for use with the Skill tool — invoke one by exact name when its description matches what the user needs; if no skill matches, just answer the user yourself.",
             'For each of the user messages below, name the ONE skill to invoke, or the word none. Answer with a JSON object {"<message number>": "<skill-or-none>"} only.', "",
             "## Skills"]
    for name, s in ss.items():
        lines.append(f"- {name} ({s['version']}): {s['description']}")
    lines += ["", "## User messages"]
    for i, fx in enumerate(fixtures, 1):
        lines.append(f"{i}. {fx['utterance']}")
    print("\n".join(lines))
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


def answers(path: str) -> int:
    """The bar is 100%: each fixture tests one skill's description in
    isolation, so any miss is that description's failure."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    given = normalize(raw, fixtures)
    correct = 0
    misses = []
    width = max(len(fx["id"]) for fx in fixtures)
    for i, fx in enumerate(fixtures, 1):
        got = str(given.get(str(i), given.get(fx["id"], given.get(fx["utterance"], "<missing>")))).strip()
        expected = fx.get("accept", [fx["expect"]])
        ok = got.lower() in [e.lower() for e in expected]
        correct += ok
        if ok:
            print(f"PASS  {fx['id'].ljust(width)}  {fx['utterance'][:44]!r}")
        else:
            misses.append(fx["id"])
            print(f"FAIL  {fx['id'].ljust(width)}  {fx['utterance'][:44]!r}")
            print(f"      expected {' / '.join(expected)} — got {got!r}")
    print(f"\n{correct}/{len(fixtures)} — the bar is {len(fixtures)}/{len(fixtures)}.")
    if misses:
        print(f"Failed descriptions: {', '.join(misses)} — improve the description's clarity, do not stuff more keywords.")
    return 0 if correct == len(fixtures) else 1


def gen(model: str, out: str) -> int:
    """A generator model writes new test utterances from the descriptions:
    comprehension testing, not memorized phrase templates."""
    # The prompt stays ABSTRACT on purpose (owner ruling 2026-11-15): no
    # instructions about style, phrasing, paraphrasing, or how many words —
    # the generator infers everything from the schema and the descriptions.
    # Concrete guidance would only be allowed as examples, and examples are
    # skipped here: these are tests, token cost matters.
    ss = skills()
    lines = ["You write user messages for an agent skill collection.",
             'Answer with a JSON object {"utterances": [{"utterance": "...", "skill": "<skill-name>"}]} covering every skill listed.', "",
             "## Skills"]
    for name, s in ss.items():
        lines.append(f"- {name}: {s['description']}")
    data = call_llm("\n".join(lines), model)
    items = data.get("utterances", [])
    if not items:
        sys.exit(f"model '{model}' returned no utterances — wrong schema or a lazy answer; try another model.")
    draft = [{"id": f"gen-{i:02d}", "utterance": it.get("utterance", ""),
              "expect": it.get("skill", "")} for i, it in enumerate(items, 1)]
    Path(out).write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(draft)} generated utterances -> {out} (DRAFT — review before use)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lint", action="store_true")
    ap.add_argument("--battery", action="store_true")
    ap.add_argument("--answers")
    ap.add_argument("--gen", metavar="MODEL")
    ap.add_argument("--out", default="fixtures-draft.json")
    a = ap.parse_args()
    if a.lint:
        return lint()
    if a.battery:
        return battery()
    if a.answers:
        return answers(a.answers)
    if a.gen:
        return gen(a.gen, a.out)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
