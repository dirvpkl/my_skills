#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""stock_test.py - the stock gate for the roi skill.

Sends the prompt that produced a finding VERBATIM to a COLD control model
(a different model/provider than the producing one, no conversation
history) and fuzzy-diffs the finding against the control's answer. A high
match means the finding is stock: any cold LLM would have said the same
thing.

Usage:
    python -I stock_test.py finding.txt --prompt producer-prompt.txt
    cat finding.txt | python -I stock_test.py - --prompt prompt.txt
    python -I stock_test.py --selftest        # offline, no network, no env

Config (environment variables):
    ROI_CONTROL_MODEL      required to run; any omniroute ":free" id works
    ROI_PRODUCER_MODEL     optional guard; control must differ from producer
    ROI_CONTROL_BASE_URL   OpenAI-compatible root; falls back to OPENAI_BASE_URL
    ROI_CONTROL_API_KEY    bearer key for the control endpoint (never logged)
    ROI_CONTROL_TIMEOUT    seconds (default 120)
    ROI_CONTROL_MAX_TOKENS (default 1024)

Exit codes (see references/output-format.md):
    0  gate ran; finding is NOT stock (diff < threshold) - continue scoring
    2  gate ran; finding IS stock - verdict STOCK, score 0
    3  UNVERIFIED - control config missing or invalid
    4  UNVERIFIED - control call failed or returned nothing usable
    5  self-test failed (--selftest only)
    1  usage error

A missing or failed control is UNVERIFIED and is NEVER reported as a pass.
One control call per finding - hard cap.
"""

import argparse
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_STOCK = 2
EXIT_UNVERIFIED_CONFIG = 3
EXIT_UNVERIFIED_CALL = 4
EXIT_SELFTEST_FAIL = 5

DEFAULT_THRESHOLD = 0.6
DEFAULT_TIMEOUT = 120
DEFAULT_MAX_TOKENS = 1024
EXCERPT_CHARS = 240
MIN_ANSWER_CHARS = 20

# Small bilingual stopword set: function words carry no claim content.
STOPWORDS = frozenset("""
a an the and or but if of to in on for with at by from as is are was were
be been being it its this that these those you your we our i me my he she
they them their will would can could should may might do does did done have
has had not no so than then there here what which who whom when where why
how all any both each few more most other some such only own same too very
just about into over under up down out off via per etc
и в во не что он на я с со как а то все она так его но да ты к у же вы за
бы по только ее мне было вот от меня еще нет о из ему даже ну ли если уже
или ни быть был до там себя ей они для мы их чем была без этот один при об
это эту этот была были будет потому чтобы над через нас про очень какой
""".split())


def read_text(path_or_dash):
    """Read a UTF-8 text file, or stdin when the path is '-'. Loud on failure."""
    if path_or_dash == "-":
        try:
            if hasattr(sys.stdin, "reconfigure"):
                sys.stdin.reconfigure(encoding="utf-8", errors="replace")
            data = sys.stdin.read()
        except Exception as exc:  # pragma: no cover - environment dependent
            sys.stderr.write("ERROR: cannot read stdin: %s\n" % exc)
            sys.exit(EXIT_USAGE)
        if not data.strip():
            sys.stderr.write("ERROR: stdin produced no text.\n")
            sys.exit(EXIT_USAGE)
        return data
    try:
        with open(path_or_dash, "r", encoding="utf-8", errors="replace") as fh:
            data = fh.read()
    except OSError as exc:
        sys.stderr.write("ERROR: cannot read %r: %s\n" % (path_or_dash, exc))
        sys.exit(EXIT_USAGE)
    if not data.strip():
        sys.stderr.write("ERROR: file %r is empty.\n" % path_or_dash)
        sys.exit(EXIT_USAGE)
    return data


def tokenize(text):
    """Lowercased word tokens (unicode), stopwords dropped, numbers kept."""
    tokens = re.findall(r"\w+", text.lower(), re.UNICODE)
    return [t for t in tokens if t not in STOPWORDS and len(t) >= 2]


def cosine(tokens_a, tokens_b):
    """Cosine similarity of bag-of-words TF vectors; 0.0 when empty."""
    counts_a, counts_b = {}, {}
    for t in tokens_a:
        counts_a[t] = counts_a.get(t, 0) + 1
    for t in tokens_b:
        counts_b[t] = counts_b.get(t, 0) + 1
    dot = sum(v * counts_b.get(k, 0) for k, v in counts_a.items())
    norm_a = math.sqrt(sum(v * v for v in counts_a.values()))
    norm_b = math.sqrt(sum(v * v for v in counts_b.values()))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def token_overlap(finding_tokens, response_tokens):
    """Fraction of the finding's distinct tokens present in the response."""
    distinct = set(finding_tokens)
    if not distinct:
        return 0.0
    response_set = set(response_tokens)
    hits = sum(1 for t in distinct if t in response_set)
    return hits / len(distinct)


def diff_score(finding_tokens, response_tokens):
    """Fuzzy-diff score: max(token overlap, cosine) - spec allows either."""
    return {
        "cosine": round(cosine(finding_tokens, response_tokens), 4),
        "token_overlap": round(token_overlap(finding_tokens, response_tokens), 4),
        "score": round(max(cosine(finding_tokens, response_tokens),
                           token_overlap(finding_tokens, response_tokens)), 4),
    }


def excerpt(text, limit=EXCERPT_CHARS):
    flat = " ".join(text.split())
    return flat[:limit] + ("..." if len(flat) > limit else "")


def unverified(reason, exit_code, as_json=False):
    """Loud UNVERIFIED verdict - the gate did not run; never a fake pass."""
    if as_json:
        print(json.dumps({"verdict": "UNVERIFIED", "reason": reason,
                          "gate_ran": False}, ensure_ascii=False))
    else:
        print("STOCK-GATE verdict: UNVERIFIED - gate did not run (%s)" % reason)
        print("  stock: UNVERIFIED - no cold-model control was recorded")
        print("  NO PASS. The finding stays unscored until a control run succeeds.")
    sys.exit(exit_code)


def check_config(as_json):
    """Validate the control configuration; returns (model, base_url, key)."""
    model = os.environ.get("ROI_CONTROL_MODEL", "").strip()
    if not model:
        unverified("ROI_CONTROL_MODEL is not set", EXIT_UNVERIFIED_CONFIG, as_json)
    producer = os.environ.get("ROI_PRODUCER_MODEL", "").strip()
    if producer and producer == model:
        unverified("ROI_CONTROL_MODEL equals ROI_PRODUCER_MODEL - a control "
                   "arm must be a different model", EXIT_UNVERIFIED_CONFIG, as_json)
    base_url = os.environ.get("ROI_CONTROL_BASE_URL",
                              os.environ.get("OPENAI_BASE_URL", "")).strip()
    if not base_url:
        unverified("no ROI_CONTROL_BASE_URL (or OPENAI_BASE_URL) for the "
                   "control endpoint", EXIT_UNVERIFIED_CONFIG, as_json)
    key = os.environ.get("ROI_CONTROL_API_KEY", "").strip()
    if not key:
        unverified("ROI_CONTROL_API_KEY is not set - missing secret fails "
                   "loud, never a guessed value", EXIT_UNVERIFIED_CONFIG, as_json)
    return model, base_url.rstrip("/"), key


def call_control(model, base_url, key, prompt, timeout, max_tokens):
    """One OpenAI-compatible chat completion to the cold control model."""
    url = base_url + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            pass
        unverified("control endpoint returned HTTP %s %s" % (exc.code, detail),
                   EXIT_UNVERIFIED_CALL)
    except (urllib.error.URLError, OSError, ValueError) as exc:
        unverified("control call failed: %s" % exc, EXIT_UNVERIFIED_CALL)
    try:
        data = json.loads(body)
        answer = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        unverified("control answer not parseable (%s)" % exc, EXIT_UNVERIFIED_CALL)
    if not isinstance(answer, str) or len(answer.strip()) < MIN_ANSWER_CHARS:
        unverified("control returned nothing usable", EXIT_UNVERIFIED_CALL)
    return answer


def report(finding_text, prompt_text, claim_text, answer, model, base_url,
           threshold, as_json):
    """Print the verdict and exit 0 (non-stock) or 2 (stock)."""
    diffed = diff_score(tokenize(claim_text), tokenize(answer))
    full_diff = diff_score(tokenize(finding_text), tokenize(answer))
    score = diffed["score"]
    is_stock = score >= threshold
    if as_json:
        print(json.dumps({
            "verdict": "STOCK" if is_stock else "NON-STOCK",
            "gate_ran": True,
            "control_model": model,
            "control_base_url": base_url,
            "diff": diffed,
            "full_finding_diff": full_diff,
            "threshold": threshold,
            "finding_chars": len(finding_text),
            "prompt_chars": len(prompt_text),
        }, ensure_ascii=False))
    else:
        print("STOCK-GATE verdict: %s" % ("STOCK" if is_stock else "NON-STOCK (gate-pass)"))
        print("  control: %s @ %s" % (model, base_url))
        print("  diff vs core claim: cosine %s | token overlap %s | score %s %s threshold %s"
              % (diffed["cosine"], diffed["token_overlap"], diffed["score"],
                 ">=" if is_stock else "<", threshold))
        print("  diff vs full finding: score %s" % full_diff["score"])
        print("  cold answer excerpt: %s" % excerpt(answer))
    sys.exit(EXIT_STOCK if is_stock else EXIT_OK)


def selftest():
    """Offline assertions of the diff logic - no network, no env needed."""
    checks = []

    identical = tokenize("Agensi seller URL, 70 percent split, Stripe rail")
    checks.append(("identical text scores 1.0",
                   diff_score(identical, list(identical))["score"] == 1.0))

    disjoint_a = tokenize("quantum flanges melted yesterday")
    disjoint_b = tokenize("old brick houses cost money")
    checks.append(("disjoint text scores 0.0", diff_score(disjoint_a, disjoint_b)["score"] == 0.0))

    claim = tokenize("agensi marketplace takes 30 percent commission "
                     "sellers keep 70 percent payouts via stripe rail "
                     "https example com sell")
    stock_answer = tokenize("on agensi marketplace the platform takes a 30 "
                            "percent commission and sellers keep 70 percent, "
                            "payouts run through a stripe rail")
    checks.append(("stock-like answer clears threshold",
                   diff_score(claim, stock_answer)["score"] >= DEFAULT_THRESHOLD))

    unrelated_answer = tokenize("try affiliate networks instead, they pay "
                                "monthly via bank transfer")
    checks.append(("unrelated answer stays below threshold",
                   diff_score(claim, unrelated_answer)["score"] < DEFAULT_THRESHOLD))

    checks.append(("cosine is symmetric",
                   abs(cosine(tokenize("alpha beta gamma"),
                              tokenize("beta gamma delta"))
                       - cosine(tokenize("beta gamma delta"),
                                tokenize("alpha beta gamma"))) < 1e-12))

    failures = [name for name, ok in checks if not ok]
    if failures:
        for name in failures:
            print("SELFTEST FAIL: %s" % name)
        sys.exit(EXIT_SELFTEST_FAIL)
    print("SELFTEST PASS: %d/%d checks green" % (len(checks), len(checks)))
    sys.exit(EXIT_OK)


def main():
    parser = argparse.ArgumentParser(
        description="roi stock gate: diff a finding against a cold control model")
    parser.add_argument("finding", nargs="?",
                        help="finding text file, or '-' for stdin")
    parser.add_argument("--prompt", default=None,
                        help="the producer prompt that produced the finding "
                             "(file or '-'); required for a real run")
    parser.add_argument("--claim", default=None,
                        help="optional file with the core claim only; diff "
                             "runs on it (falls back to the full finding)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help="stock threshold (default %.1f)" % DEFAULT_THRESHOLD)
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--selftest", action="store_true",
                        help="run offline diff-logic assertions and exit")
    args = parser.parse_args()

    if args.selftest:
        selftest()

    if not args.finding:
        parser.error("a finding (file path or '-') is required")
    if args.prompt == "-" and args.finding == "-":
        parser.error("finding and --prompt cannot both read stdin")

    finding_text = read_text(args.finding)

    if not args.prompt:
        # The method requires the SAME prompt that produced the finding.
        # A reconstructed prompt could manufacture a fake pass - refuse loud.
        unverified("no producer prompt (--prompt) - the stock test needs the "
                   "same prompt that produced the finding",
                   EXIT_UNVERIFIED_CONFIG, args.json)
    prompt_text = read_text(args.prompt)

    claim_text = read_text(args.claim) if args.claim else finding_text

    model, base_url, key = check_config(args.json)
    try:
        timeout = float(os.environ.get("ROI_CONTROL_TIMEOUT", DEFAULT_TIMEOUT))
        max_tokens = int(os.environ.get("ROI_CONTROL_MAX_TOKENS", DEFAULT_MAX_TOKENS))
    except ValueError:
        timeout, max_tokens = DEFAULT_TIMEOUT, DEFAULT_MAX_TOKENS

    answer = call_control(model, base_url, key, prompt_text, timeout, max_tokens)
    report(finding_text, prompt_text, claim_text, answer, model, base_url,
           args.threshold, args.json)


if __name__ == "__main__":
    main()
