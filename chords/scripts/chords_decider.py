#!/usr/bin/env python3
"""UserPromptSubmit decider (keyword-only): scans the incoming prompt for the
chords binding phrases and injects the matched stacks as a kick. Zero external
infrastructure — no embedding service, no model, no config; the matcher is a
case-insensitive substring scan over the chords.md table (the table's own
documented mechanic), reading the target skills' descriptions from the live
catalog for the kick text.

Fires on UserPromptSubmit. Reads the prompt from the event JSON on stdin
(defensive key lookup).

Flow: parse the chords.md table (aliases + kind + target description) ->
ALL rows whose alias appears verbatim in the prompt kick at once (one message
may carry several bindings) — a shorter alias contained inside a longer
matched one loses («пиши» ⊂ «напиши» — the specific row wins, per the
table's collision notes); placeholder aliases («чекай <skill-name>») carry
no verbatim surface and are dropped. No hit = silent pass — a decider never
blocks a prompt. Every kick is a nomination: meaning-match stays the agent's
job, verified against chords.md. Paraphrases with zero lexical overlap are
NOT this hook's job — the always-loaded chords/base duty covers them; a
semantic tier (decision model) was designed and parked (brainstorm.md).

Option text v3 (owner design): aliases + kind + an intent sentence + the
TARGET SKILLS' descriptions pulled from the live catalog per run — the kick
carries meaning, not just surface words. Full SKILL.md is deliberately not
embedded.
"""

import json
import re
import sys
from pathlib import Path


def binding_rows() -> list[tuple[str, list[str], str]] | None:
    """(key, aliases, option_text) rows from the chords table; None when
    empty. Option text = aliases + kind + an intent sentence + the target
    skills' descriptions from the live catalog. Placeholder aliases
    («чекай <skill-name>») are dropped from the literal layer."""
    table = Path(__file__).resolve().parent.parent / "chords.md"
    try:
        lines = table.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return None
    kinds = {"skill", "bundle", "action"}
    rows = []
    for line in lines:
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0].startswith("phrase") or set(cells[0]) <= set("-: "):
            continue
        key_match = re.search(r'"([^"]+)"', cells[0])
        if not key_match:
            continue
        aliases = [a.strip().strip('"').strip() for a in cells[0].split(",")]
        aliases = [a for a in aliases if a and "<" not in a]
        kind_pos = next((i for i, c in enumerate(cells[1:4], start=1) if c in kinds), None)
        kind = cells[kind_pos] if kind_pos else "?"
        if kind in ("skill", "bundle"):
            body = cells[1]  # the target cell is always column 2 for skill/bundle rows
        else:  # action rows carry the description in whichever cell it fits
            body = max((c for c in cells[1:4] if c != kind), key=len, default="")
        if kind in ("skill", "bundle"):
            targets = [t.strip() for t in re.split(r"[+,]| {2,}", body) if t.strip()]
            descs = [f"{t}: {read_description(t)}" for t in targets if read_description(t)]
            intent = f"I need to launch {kind} {body}" + (": " + " | ".join(descs) if descs else "")
        else:
            intent = f"I need to perform this action: {body[:500]}"
        rows.append((key_match.group(1), aliases,
                     f"{cells[0].replace(chr(34), chr(39))} [{kind}] — {intent[:700]}"))
    return rows or None


def read_description(skill: str) -> str:
    """Frontmatter description of a sibling skill from the live catalog."""
    f = Path(__file__).resolve().parent.parent.parent / skill / "SKILL.md"
    try:
        lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return ""
    inside, grab, desc = False, False, []
    for line in lines:
        s = line.strip()
        if s == "---":
            if inside:
                break
            inside = True
            continue
        if inside and s.startswith("description:"):
            grab = True
            rest = s[len("description:"):].strip()
            if rest and rest not in (">", ">-", "|", "|-"):
                desc.append(rest)
            continue
        if grab:
            if s == "---" or re.match(r"^[A-Za-z_-]+:", s):
                break
            desc.append(s)
    return " ".join(part for part in desc if part).strip()[:240]


def literal_hits(prompt: str,
                 rows: list[tuple[str, list[str], str]]) -> list[tuple[str, str, str]]:
    """All rows whose alias appears verbatim in the prompt
    (case-insensitive). A shorter alias contained inside an already-matched
    longer one loses — the specific row wins («пиши» ⊂ «напиши»), per the
    table's collision notes."""
    low = prompt.lower()
    hits: list[tuple[str, str, str]] = []  # (matched_alias, key, option_text)
    for key, aliases, option_text in rows:
        for alias in aliases:
            if alias.lower() in low:
                hits.append((alias.lower(), key, option_text))
                break
    matched = [h[0] for h in hits]
    return [h for h in hits
            if not any(h[0] in other and h[0] != other for other in matched)]


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    data = payload if isinstance(payload, dict) else {}
    prompt = ""
    for key in ("prompt", "prompt_text", "user_prompt", "text"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            prompt = value
            break
    rows = binding_rows()
    if not prompt or not rows:
        return
    hits = literal_hits(prompt, rows)
    if not hits:
        return
    lines = [f"literal hit '{key}' -> {option_text}" for _, key, option_text in hits]
    print(json.dumps({"additionalContext":
        "chords-decider: LITERAL phrase hit(s) — verbatim, certain:\n" + "\n".join(lines) +
        "\nVerify against chords.md before acting. When this task completes, notify "
        "the owner via base scripts/notify.py."}))


if __name__ == "__main__":
    main()
