"""workplanx hook script — logs every owner message into the workplanx sink.

Fired by a UserPromptSubmit hook (registered in ~/.zcode/cli/config.json).
The hook payload arrives on stdin (JSON when the harness sends one, raw
prompt text otherwise). Sinks, in order:
  1. $WORKPLANX_TOPIC/log.md — when the session pins an active topic
  2. <project>/.workplanx/_inbox/<YYYY-MM-DD>.md — the session inbox
Owner words are appended verbatim (capped at 8000 chars). Errors never
break the session: any failure exits 0 silently, diagnostics go to
workplanx/scripts/.hook_errors.log.
"""
import sys, os, json, datetime

MAX_CHARS = 8000

def main():
    try:
        # Windows stdin defaults to a legacy codepage — read BYTES and decode
        # UTF-8 explicitly, never trusting the console encoding.
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    except Exception:
        return 0
    prompt = raw
    try:
        d = json.loads(raw)
        if isinstance(d, dict):
            for k in ("prompt", "user_prompt", "message", "text", "content"):
                if isinstance(d.get(k), str) and d[k].strip():
                    prompt = d[k]
                    break
    except Exception:
        pass
    prompt = (prompt or "").strip()
    if not prompt:
        return 0
    prompt = prompt[:MAX_CHARS]

    proj = (os.environ.get("ZCODE_PROJECT_DIR")
            or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    wp = os.path.join(proj, ".workplanx")
    os.makedirs(wp, exist_ok=True)
    now = datetime.datetime.now()
    stamp = now.strftime("%Y-%m-%d %H:%M:%S")

    topic = os.environ.get("WORKPLANX_TOPIC")
    if topic:
        p = topic if os.path.isabs(topic) else os.path.join(wp, topic)
        log = os.path.join(p, "log.md")
        os.makedirs(os.path.dirname(log), exist_ok=True)
        new = not os.path.exists(log)
        with open(log, "a", encoding="utf-8") as f:
            if new:
                f.write("# log — auto-logged by the workplanx hook\n\n## Owner messages (hook)\n\n")
            f.write(f"- [{stamp}] owner: {prompt}\n")
        return 0

    inbox = os.path.join(wp, "_inbox")
    os.makedirs(inbox, exist_ok=True)
    day = os.path.join(inbox, now.strftime("%Y-%m-%d") + ".md")
    new = not os.path.exists(day)
    with open(day, "a", encoding="utf-8") as f:
        if new:
            f.write("# inbox — " + now.strftime("%Y-%m-%d") + "\n\n"
                    "Every owner message, appended by the workplanx hook. "
                    "Feed to recap/handoff as the session's raw thread.\n\n")
        f.write(f"## [{now.strftime('%H:%M')}] owner\n\n{prompt}\n\n")
    return 0

try:
    sys.exit(main())
except Exception as e:
    try:
        err = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".hook_errors.log")
        with open(err, "a", encoding="utf-8") as f:
            f.write(datetime.datetime.now().isoformat() + " " + repr(e) + "\n")
    except Exception:
        pass
    sys.exit(0)
