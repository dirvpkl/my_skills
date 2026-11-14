#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""radar_search.py - the search wrapper for the radar skill.

Runs one verb-tool query through the omniroute search REST endpoint with a
provider fallback chain (exa-search -> tavily-search -> searxng-search),
then applies HEURISTIC kind hints to each hit. The heuristic is a triage
aid only: the agent does the final classification per references/radar-method.md.

Usage:
    python -I radar_search.py --query "dataset publish automation tool"
    python -I radar_search.py --topic "sell datasets" --verb publish
    python -I radar_search.py --selftest        # offline, no network, no env

Config (environment variables):
    RADAR_OMNI_BASE_URL  OpenAI-compatible root; falls back to OMNI_BASE_URL
    RADAR_OMNI_API_KEY   bearer key (never logged, never echoed)
    RADAR_COUNT          hits per provider (default 5)
    RADAR_TIMEOUT        seconds (default 40)

Exit codes:
    0  hits returned
    1  no hits from any provider in the chain
    2  config missing (no base URL) - loud, never a silent direct fallback
    3  bad arguments

Heuristic kind hints:
    github.com/gist|gitlab            -> oss-repo
    /advertise, /sell, /pricing path  -> monetization-evidence (hosted-service likely)
    "list of", "best ", "top " title  -> directory-of-tools likely
    everything else                   -> venue-or-noise (agent decides)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

PROVIDER_CHAIN = ("exa-search", "tavily-search", "searxng-search")


def _config() -> tuple[str, str, int, int]:
    base = (
        os.getenv("RADAR_OMNI_BASE_URL")
        or os.getenv("OMNI_BASE_URL")
        or ""
    ).rstrip("/")
    key = os.getenv("RADAR_OMNI_API_KEY") or os.getenv("OMNI_API_KEY") or ""
    if not base:
        print(
            "radar_search: no RADAR_OMNI_BASE_URL / OMNI_BASE_URL in env - "
            "resolve from the machine's runtime context, never hardcode",
            file=sys.stderr,
        )
        raise SystemExit(2)
    try:
        count = int(os.getenv("RADAR_COUNT", "5"))
        timeout = int(os.getenv("RADAR_TIMEOUT", "40"))
    except ValueError as exc:
        print(f"radar_search: bad RADAR_COUNT/RADAR_TIMEOUT: {exc}", file=sys.stderr)
        raise SystemExit(3)
    return base, key, count, timeout


def _search(base: str, key: str, query: str, provider: str, count: int, timeout: int):
    body = json.dumps({"query": query, "provider": provider, "count": count}).encode()
    req = urllib.request.Request(
        f"{base}/v1/search",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.load(resp)
    return payload.get("results") or []


def _kind_hint(url: str, title: str) -> str:
    u = (url or "").lower()
    t = (title or "").lower()
    if "github.com" in u or "gitlab" in u or u.rstrip("/").endswith(".git"):
        return "oss-repo"
    if any(mark in u for mark in ("/advertise", "/sell", "/pricing", "/sponsor")):
        return "monetization-evidence"
    if t.startswith(("list of", "best ", "top ")) or "alternatives" in t:
        return "directory-of-tools"
    return "venue-or-noise"


def _selftest() -> int:
    # Offline checks: heuristic hints + query-shape guard. No network, no env.
    assert _kind_hint("https://github.com/x/y", "repo") == "oss-repo"
    assert _kind_hint("https://x.example/advertise/", "Advertise") == "monetization-evidence"
    assert _kind_hint("https://x.example/", "Best 12 widget stores") == "directory-of-tools"
    assert _kind_hint("https://x.example/a", "something") == "venue-or-noise"
    bad = ["x marketplace best", "where to buy"]
    for q in bad:
        assert not _is_tool_class_query(q), q
    assert _is_tool_class_query("widget publish automation tool")
    print("radar_search selftest: OK (offline)")
    return 0


def _is_tool_class_query(query: str) -> bool:
    """Guard: object-words must be absent for a query to be a radar query."""
    q = query.lower()
    return not any(w in q for w in ("marketplace", "where to", "best ", "top "))


def main() -> int:
    ap = argparse.ArgumentParser(description="radar verb-tool search wrapper")
    ap.add_argument("--query", help="full tool-class query")
    ap.add_argument("--topic", help="noun/topic; compose with --verb")
    ap.add_argument("--verb", help="verb to compose the query from")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    if args.query:
        query = args.query
    elif args.topic and args.verb:
        query = f"{args.topic} {args.verb} automation tool"
    else:
        ap.error("need --query or --topic+--verb")
        return 3

    if not _is_tool_class_query(query):
        print(
            f"radar_search: '{query}' looks like an object-query (marketplace/"
            "where-to words) - radar queries must be tool-class",
            file=sys.stderr,
        )
        return 3

    base, key, count, timeout = _config()
    seen: dict[str, dict] = {}
    for provider in PROVIDER_CHAIN:
        try:
            for hit in _search(base, key, query, provider, count, timeout):
                url = hit.get("url") or ""
                if not url or url in seen:
                    continue
                seen[url] = hit
                print(
                    f"- [{_kind_hint(url, hit.get('title') or '')}] "
                    f"{(hit.get('title') or '?')[:80]} | {url[:90]}"
                )
            if seen:
                print(f"provider: {provider} (chain stops on first hits)")
                return 0
        except (urllib.error.URLError, OSError, ValueError) as exc:
            print(f"radar_search: {provider} failed: {exc}", file=sys.stderr)
    print("radar_search: no hits from any provider in the chain", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
