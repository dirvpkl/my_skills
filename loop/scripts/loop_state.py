#!/usr/bin/env python3
"""loop_state.py — mechanical continue/stop decision for a `loop` skill run.

Reads `loop.md` in a workplanx topic folder and prints exactly one verdict:
CONTINUE, or STOP:<reason>. Exit code 0 = keep going or predicate met,
exit code 1 = stop the loop. That verdict is the loop's decision, not the
agent's.

The predicate ("done") is fixed in loop.md. How it is checked:

- `verify:` — shell command, exit 0 means the predicate holds. Re-run here
  every time; the ledger's word is never trusted for this path.
- `criterion:` — a fixed rule judged against recorded evidence (convergence,
  stabilization, exhaustion — things no command can decide). There is nothing
  to re-run, so the recorded `result:` is read. That is exactly why the
  criterion is frozen before the first iteration and every ledger line must
  carry evidence: a `pass` without evidence is a claim, not an observation.

Tests and deploys are examples of command checks, not the definition of
checking. Both check kinds may be present for the same predicate; then the
command decides and the criterion is supplementary.

Usage:
    python3 loop_state.py --dir <topic-dir> [--skip-verify] [--timeout N]

Verdicts, in the order they are checked:
    STOP:condition-met   verify command exited 0, or (criterion-only run)
                         the last ledger line records result: pass
    STOP:iteration-cap   ledger lines >= max_iterations
    STOP:no-progress     no_progress_limit consecutive iterations with no new
                         evidence (a reused or nonexistent commit sha counts
                         as no progress; a repeated evidence token does too)
    STOP:no-ledger       loop.md has a config but no ledger line yet
    STOP:no-contract     loop.md missing, or no predicate / no check / no cap
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

CONFIG_KEYS = ("condition", "verify", "criterion", "max_iterations",
               "no_progress_limit", "unit")
# One ledger line carries three things: iteration number, evidence, result.
# Accepts the current shape (evidence <ref> | result: pass|fail) and the
# legacy shape (commit <sha> | verify: pass|fail) — same fields, older names.
LEDGER_RE = re.compile(
    r"^-\s*iter\s+(\d+)\s*\|\s*"
    r"(?:commit|evidence|artifact)\s+(\S+)\s*\|\s*"
    r"(?:verify|result|verdict)\s*:\s*(pass|fail)\b",
    re.I | re.M,
)
SHA_RE = re.compile(r"[0-9a-f]{4,40}", re.I)
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
    if not SHA_RE.fullmatch(sha or ""):
        return False
    try:
        out = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=cwd, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return out.returncode == 0


def is_sha(token: str) -> bool:
    return bool(SHA_RE.fullmatch(token or ""))


def evidence_is_new(evidence: str, seen: set, cwd: Path) -> bool:
    """True when this evidence was not observed before.

    Commit shas are checked against git (reused or nonexistent = not new),
    so claiming progress is free and buys nothing. Any other token counts
    as new the first time it appears; repeating the same observation with a
    fresh token each pass is gaming, and gaming belongs to
    references/stop-signals.md, not to this script.
    """
    if is_sha(evidence):
        return evidence.lower() not in seen and git_has_commit(cwd, evidence)
    return evidence not in seen


def norm(evidence: str) -> str:
    return evidence.lower() if is_sha(evidence) else evidence


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
                    help="skip running the verify command (criterion checks decide by ledger)")
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

    if "condition" not in config:
        print("STOP:no-contract\n  reason: loop.md has no condition — a loop "
              "without a fixed predicate is not runnable", file=sys.stderr)
        return 1

    has_verify = bool(config.get("verify"))
    has_criterion = bool(config.get("criterion"))
    if not has_verify and not has_criterion:
        print("STOP:no-contract\n  reason: loop.md has neither verify nor criterion — "
              "a loop without a decidable check is not runnable", file=sys.stderr)
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
    last_evidence = entries[-1][1]
    last_result = entries[-1][2].lower()
    head = git_head(topic)

    # Stall = trailing entries that added no new evidence. The first entry is
    # the baseline (it describes work already done) and never counts as one,
    # otherwise every run silently loses one unit of its no-progress budget.
    stalled = 0
    seen = {norm(entries[0][1])}
    for _, evidence, _ in reversed(entries[1:]):
        if evidence_is_new(evidence, seen, topic):
            stalled = 0
            seen.add(norm(evidence))
        else:
            stalled += 1
    made_progress = evidence_is_new(
        last_evidence, {norm(e) for _, e, _ in entries[:-1]}, topic)

    print(f"iterations: {used}/{cap}")
    print(f"last evidence in ledger: {last_evidence}   HEAD: {head or '(not a git repo)'}")
    print(f"new evidence since previous entries: {'yes' if made_progress else 'no'}")
    print(f"consecutive iterations without new evidence: {stalled}/{no_progress_limit}")

    if not args.skip_verify and has_verify:
        ok, detail = run_verify(config["verify"], topic, args.timeout)
        print(f"verify: {'pass' if ok else 'fail'} — {detail}")
        if ok:
            print("STOP:condition-met")
            return 0

    # Criterion path: only when no command decides (none defined, or skipped).
    # The recorded result is read because nothing else can decide it — which
    # is why the criterion is frozen and evidence is mandatory.
    if (not has_verify or args.skip_verify) and has_criterion:
        print(f"criterion: recorded result {last_result} "
              f"({'predicate holds' if last_result == 'pass' else 'predicate unmet'})")
        if last_result == "pass":
            print("STOP:condition-met")
            return 0

    if used >= cap:
        print(f"STOP:iteration-cap\n  reason: {used} iterations, cap is {cap}, "
              "predicate not met — report this as a failure, do not raise the cap")
        return 1

    if stalled >= no_progress_limit:
        print(f"STOP:no-progress\n  reason: {stalled} consecutive iterations with no new "
              "evidence — check references/stop-signals.md before spending more budget")
        return 1

    print("CONTINUE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
