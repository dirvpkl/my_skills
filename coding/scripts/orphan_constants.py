#!/usr/bin/env python3
"""Orphan-constant checker — the consumer-trace lens in script form.

Finds module-level constants (UPPER_CASE names) that are defined but never
consumed anywhere in the scanned tree: no code reference, no config mention.
An "integrated" constant is wired into something that reads it; a constant
nobody reads is a wish, not configuration ("integrated != wired").

Definition (what counts as a constant):
    Module-level Assign / AnnAssign whose single target is a Name matching
    ^[A-Z][A-Z0-9_]*$ — the classic config-constant shape. Underscore-prefixed
    names are treated as intentionally private and skipped.

Consumption (two tiers, reported per orphan):
    code   — the name appears as an AST Name or as an attribute access
             (MODULE.CONST) in any scanned .py file, other than its own
             defining line;
    config — the name appears as a word in a config-like file
             (yml/yaml/toml/ini/env/sh/Dockerfile/JSON), which covers compose
             env wiring and the like.

A name consumed only by a comment is an orphan: comments do not read values.

Usage:
    python -I coding/scripts/orphan_constants.py [PATH ...] [--strict] [--json]

    PATH defaults to the current directory. --strict exits 1 when orphans
    exist (CI-style); default exit is 0 — this is a report, not a gate.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

CONST_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
SKIP_DIRS = {".git", ".hg", ".svn", "__pycache__", ".venv", "venv",
             "node_modules", ".workplanx", ".idea", ".vscode", ".mypy_cache"}
CONFIG_SUFFIXES = {".yml", ".yaml", ".toml", ".ini", ".env", ".sh",
                   ".json", ".cfg", ".conf", ""}
CONFIG_NAMES = {"Dockerfile", ".env.example", ".env"}
WORD_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")


def iter_files(root: Path):
    for p in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file() and (p.suffix == ".py" or p.name in CONFIG_NAMES
                            or p.suffix in CONFIG_SUFFIXES):
            yield p


def scan(paths: list[Path]) -> tuple[dict, dict]:
    """Returns ({name: [(file, line), ...]}, {name: [(file, line), ...]}) —
    definitions and consumption sites."""
    defs: dict[str, list] = {}
    uses: dict[str, list] = {}
    for f in paths:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if f.suffix == ".py":
            try:
                tree = ast.parse(text, filename=str(f))
            except SyntaxError:
                continue
            lines = text.splitlines()
            for node in tree.body:  # module level only
                targets = []
                if isinstance(node, ast.Assign):
                    targets = node.targets
                elif isinstance(node, ast.AnnAssign):
                    targets = [node.target]
                for t in targets:
                    if isinstance(t, ast.Name) and CONST_RE.match(t.id) \
                            and not t.id.startswith("_"):
                        defs.setdefault(t.id, []).append((f, node.lineno))
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    uses.setdefault(node.id, []).append((f, node.lineno))
                elif isinstance(node, ast.Attribute) \
                        and isinstance(node.value, ast.Name):
                    # MODULE.CONST in another module: the attr name is the
                    # consumption signal (approximation — same-name
                    # attributes of unrelated objects may overcount, which
                    # is the safe direction: fewer false orphans).
                    uses.setdefault(node.attr, []).append((f, node.lineno))
        else:
            for m in WORD_RE.finditer(text):
                uses.setdefault(m.group(0), []).append((f, text[:m.start()].count("\n") + 1))
    return defs, uses


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", default=["."], help="trees to scan")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when orphans exist")
    ap.add_argument("--json", action="store_true", help="JSON report")
    a = ap.parse_args()

    roots = [Path(p).resolve() for p in a.paths]
    files = [f for r in roots for f in iter_files(r)]
    if not files:
        print("no files to scan", file=sys.stderr)
        return 0
    defs, uses = scan(files)

    orphans = []
    for name, sites in sorted(defs.items()):
        ref_sites = uses.get(name, [])
        live = [u for u in ref_sites
                if not any(u[0] == d[0] and u[1] == d[1] for d in sites)]
        if not live:
            orphans.append({
                "name": name,
                "defined": [{"file": str(f), "line": ln} for f, ln in sites],
            })

    if a.json:
        print(json.dumps({"scanned_files": len(files),
                          "constants": len(defs),
                          "orphans": orphans}, indent=2))
    elif orphans:
        print(f"{len(orphans)} orphan constant(s) "
              f"over {len(defs)} constants, {len(files)} files:\n")
        for o in orphans:
            where = ", ".join(f"{d['file']}:{d['line']}"
                              for d in o["defined"])
            print(f"  {o['name']}  (defined at {where})")
        print("\nEach one is either dead config or unwired intent — wire a "
              "consumer, delete the constant, or record why it stays.")
    else:
        print(f"no orphan constants over {len(defs)} constants, "
              f"{len(files)} files")
    return 1 if (a.strict and orphans) else 0


if __name__ == "__main__":
    sys.exit(main())
