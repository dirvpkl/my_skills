#!/usr/bin/env python3
"""loop_state.py — mechanical continue/stop decision for a `loop` skill run.

Reads `loop.md` in a workplanx topic folder and prints exactly one verdict:
CONTINUE, or STOP:<reason>. Exit code 0 = keep going, 1 = stop the loop.
That verdict is the loop's decision, not the agent's — the whole point is that
progress is measured by git and by a real command, never by the agent's
assessment of its own work.

Usage:
    python3 loop_state.py --dir <topic-dir> [--skip-verify] [--timeout N]

Verdicts, in the order they are checked:
    STOP:condition-met   verify command exited 0
    STOP:iteration-cap   ledger lines >= max_iterations
    STOP:no-progress     max_iterations consecutive iterations with no new commit
    STOP:no-ledger       loop.md has a config but no ledger line yet
    CONTINUE             none of the above

Deliberately no banned-word or heuristics matching: word-matching a ledger is
gameable and teaches avoidance. Semantic stagnation ("busy but going nowhere")
belongs to references/stop-signals.md, read by the agent.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

CONFIG_KEYS = ("condition", "verify", "max_iterations", "no_progress_limit", "unit")
LEDGER_RE = re.compile(r"^-\s*iter\s+(\d+)\s*\|\s*commit\s+(\S+)\s*\|", re.I | re.M)
DEFAULT_NO_PROGRESS_LIMIT = 3
DEFAULT_VERIFY_TIMEOUT = 1800


def parse_config(text: str) -> dict:
    config = {}
    for key in CONFIG_KEYS:
        m = re.search(rf"^-\s*{key}\s*:\s*(.+)$", text, re.I | re.M)
        if m:
            config[key] = m.group(1).strip()
    return config


def git_head(cwd: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def git_has_commit(cwd: Path, sha: str) -> bool:
    if not re.fullmatch(r"[0-9a-f]{4,40}", sha or "", re.I):
        return False
    try:
        out = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=cwd, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0


def run_verify(command: str, cwd: Path, timeout: int) -> tuple[bool, str]:
    try:
        out = subprocess.run(
            command, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"verify timed out after {timeout}s"
    except OSError as e:
        return False, f"verify could not run: {e}"
    tail = (out.stdout or out.stderr or "").strip().splitlines()[-3:]
    return out.returncode == 0, " / ".join(tail)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="topic folder holding loop.md")
    ap.add_argument("--skip-verify", action="store_true",
                    help="skip running the verify command (condition check only by ledger)")
    ap.add_argument("--timeout", type=int, default=DEFAULT_VERIFY_TIMEOUT,
                    help="verify command timeout in seconds")
    args = ap.parse_args()

    topic = Path(args.dir)
    loop_file = topic / "loop.md"
    if not loop_file.exists():
        print(f"STOP:no-contract\n  reason: {loop_file} not found", file=sys.stderr)
        return 1

    text = loop_file.read_text(encoding="utf-8", errors="ignore")
    config = parse_config(text)
    entries = LEDGER_RE.findall(text)

    if "max_iterations" not in config:
        print("STOP:no-contract\n  reason: loop.md has no max_iterations — a loop "
              "without a cap is not runnable", file=sys.stderr)
        return 1
    try:
        cap = int(config["max_iterations"])
    except ValueError:
        print(f"STOP:no-contract\n  reason: max_iterations '{config['max_iterations']}' "
              "is not an integer", file=sys.stderr)
        return 1

    if not entries:
        print("STOP:no-ledger\n  reason: loop.md has a contract but no ledger line — "
              "run the first iteration, then append its line", file=sys.stderr)
        return 1

    no_progress_limit = DEFAULT_NO_PROGRESS_LIMIT
    if "no_progress_limit" in config:
        try:
            no_progress_limit = int(config["no_progress_limit"])
        except ValueError:
            print(f"STOP:no-contract\n  reason: no_progress_limit "
                  f"'{config['no_progress_limit']}' is not an integer", file=sys.stderr)
            return 1

    used = len(entries)
    last_sha = entries[-1][1]
    head = git_head(topic)

    # Progress is derived, never taken from the ledger's word. A repeated or
    # nonexistent sha is treated as no progress, so claiming progress is free
    # and buys nothing.
    made_progress = bool(head) and last_sha != head

    # Stall = trailing entries that didn't add a commit. The first entry is the
    # baseline (it describes work already committed) and never counts as one,
    # otherwise every run silently loses one unit of its no-progress budget.
    stalled = 0
    seen = {entries[0][1]}
    for _, sha in reversed(entries[1:]):
        if git_has_commit(topic, sha) and sha not in seen:
            stalled = 0
            seen.add(sha)
        else:
            stalled += 1

    print(f"iterations: {used}/{cap}")
    print(f"last commit in ledger: {last_sha}   HEAD: {head or '(not a git repo)'}")
    print(f"new work since last entry: {'yes' if made_progress else 'no'}")
    print(f"consecutive iterations without new progress: {stalled}/{no_progress_limit}")

    if not args.skip_verify and config.get("verify"):
        ok, detail = run_verify(config["verify"], topic, args.timeout)
        print(f"verify: {'pass' if ok else 'fail'} — {detail}")
        if ok:
            print("STOP:condition-met")
            return 0

    if used >= cap:
        print(f"STOP:iteration-cap\n  reason: {used} iterations, cap is {cap}, "
              "condition not met — report this as a failure, do not raise the cap")
        return 1

    if stalled >= no_progress_limit:
        print(f"STOP:no-progress\n  reason: {stalled} consecutive iterations with no new "
              "commit — check references/stop-signals.md before spending more budget")
        return 1

    print("CONTINUE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
