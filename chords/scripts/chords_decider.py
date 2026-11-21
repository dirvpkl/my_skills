#!/usr/bin/env python3
"""UserPromptSubmit decider (B+ hybrid): literal phrase fast-path first,
then cosine matching against the chords binding rows via the embeddings
endpoint; injects the matched stack as a kick.

Fires on UserPromptSubmit. Reads the prompt from the event JSON on stdin
(defensive key lookup). The embedding service is configured in the skill's
own runtime.toml (gitignored; tracked shape in runtime.example.toml):

  [decider]
  endpoint  = "http://127.0.0.1:30188/v1/embeddings"  # openai-compatible embeddings API
  model     = "microsoft/harrier-oss-v1-0.6b"         # hint; tei ignores or routes it
  threshold = 0.55                                    # cosine gate for the kick

Why embeddings for the fuzzy layer, not a generative classifier: zero-shot
by construction (the option set is whatever chords.md says right now — no
training, no fine-tuning), one embedding pass per message, and the row
vectors are cached keyed by a hash of chords.md (invalidated when the table
changes).

Flow (B+ hybrid, brainstorm.md): LITERAL fast-path first — case-insensitive
substring scan of every alias phrase (chords.md's own documented mechanic);
ALL rows hit this way kick at once (one message may carry several bindings),
and a shorter alias contained in a longer matched one loses («пиши» ⊂
«напиши» — the specific row wins, per the table's collision notes). No
literal hit -> the fuzzy layer: embed the prompt (row vectors from cache)
-> cosine per row -> best row above threshold -> kick {phrase, aliases,
score}. The fuzzy layer stays single-intent: a whole-sentence embedding is
one-directional (owner's point) — multi-thought sentences are decomposed
only at the literal layer; if multi-thought-FUZZY proves common, the
F-route (table injection, agent matches) is the designed escalation. Below
threshold, an unreachable endpoint, or an unparsable answer = silent pass —
a decider never blocks a prompt. Every kick is a nomination: meaning-match
stays the agent's job, verified against chords.md.
"""

import hashlib
import json
import math
import re
import sys
import tomllib
import urllib.request
from pathlib import Path

TIMEOUT = 6
THRESHOLD_DEFAULT = 0.55
CACHE = Path(__file__).resolve().parent / ".emb-cache.json"


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


def binding_rows() -> list[tuple[str, list[str], str]] | None:
    """(key, aliases, option_text) rows from the chords table; None when
    empty. Option text v3 = aliases + kind + an intent sentence + the
    TARGET SKILLS' descriptions from the live catalog — the embedder matches
    by meaning, and the meaning of a binding lives in what the skill does,
    not in the alias words (owner ruling; v1 full-row notes and v2 bare
    aliases both blurred it). Placeholder aliases («чекай <skill-name>»)
    are dropped from the literal layer."""
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


def embed(cfg: dict, texts: list[str]) -> list[list[float]] | None:
    body = json.dumps({"model": cfg.get("model", ""), "input": texts}).encode()
    request = urllib.request.Request(
        cfg["endpoint"], data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            data = json.load(response)["data"]
        return [item["embedding"] for item in sorted(data, key=lambda x: x.get("index", 0))]
    except Exception:
        return None


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def row_vectors(cfg: dict, rows: list[tuple[str, list[str], str]]) -> list[list[float]] | None:
    """Cached embeddings for the binding rows; invalidated by a hash over the
    composed option texts + the embedder model (descriptions come from the
    live catalog, OUTSIDE chords.md — a table-only hash would go stale when a
    skill description changes)."""
    texts = [text for _, _, text in rows]
    table_hash = hashlib.sha256(
        (Path(__file__).resolve().parent.parent / "chords.md").read_bytes()
        + json.dumps(texts, ensure_ascii=False).encode()
        + b"|v3-desc|" + cfg.get("model", "").encode()).hexdigest()
    if CACHE.is_file():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
            if cache.get("hash") == table_hash and len(cache.get("rows", [])) == len(rows):
                return cache["rows"]
        except Exception:
            pass
    vectors = embed(cfg, texts)
    if vectors is None:
        return None
    try:
        CACHE.write_text(json.dumps({"hash": table_hash, "rows": vectors}), encoding="utf-8")
    except OSError:
        pass
    return vectors


def main() -> None:
    cfg = runtime()
    if not cfg.get("endpoint"):
        return
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    prompt = prompt_from(payload)
    rows = binding_rows()
    if not prompt or not rows:
        return
    hits = literal_hits(prompt, rows)
    if hits:
        lines = [f"literal hit '{key}' -> {option_text}" for _, key, option_text in hits]
        print(json.dumps({"additionalContext":
            "chords-decider: literal phrase hit(s):\n" + "\n".join(lines) +
            "\nVerify against chords.md before acting."}))
        return
    vectors = row_vectors(cfg, rows)
    if vectors is None:
        return
    query = embed(cfg, [prompt])
    if query is None:
        return
    best_index, best_score = max(
        ((i, cosine(query[0], v)) for i, v in enumerate(vectors)),
        key=lambda pair: pair[1])
    if best_score < float(cfg.get("threshold", THRESHOLD_DEFAULT)):
        return
    phrase, aliases, option_text = rows[best_index]
    print(json.dumps({"additionalContext":
        f"chords-decider: message matches binding '{phrase}' (cosine {best_score:.2f}) -> {option_text}. "
        "Verify against chords.md before acting; match by meaning stays yours."}))


if __name__ == "__main__":
    main()
