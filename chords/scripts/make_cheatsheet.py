"""Render the chords bindings table into a one-page cheatsheet on the Desktop.

Reads chords.md (the data file bound to the skill), groups rows by kind (bundle / action / skill),
emits a compact card. Run after every table edit (the table header says
so). Usage: python -I make_cheatsheet.py [output_path]
"""
import os, re, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
BINDINGS = os.path.normpath(os.path.join(HERE, "..", "chords.md"))
DEFAULT_OUT = os.path.join(os.path.expanduser("~"), "Desktop", "chords.md")

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT
    t = open(BINDINGS, encoding="utf-8").read()
    rows = re.findall(r"^\| (\".+) \|", t, re.M)
    bundles, actions, skills = [], [], []
    for r in rows:
        cells = [c.strip() for c in r.split("|")]
        if len(cells) < 3:
            continue
        phrase, target = cells[0], cells[1]
        kind = cells[2] if len(cells) > 2 else ""
        if kind == "bundle":
            bundles.append((phrase, target))
        elif kind == "action":
            actions.append((phrase, target))
        else:
            skills.append((phrase, target))
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# чорды — шпаргалка",
        "",
        f"updated: {now} · source: chords.md · полный смысл — в таблице",
        "",
    ]
    if bundles:
        lines += ["## Комбо (бандлы)", ""]
        for p, tgt in bundles:
            lines.append(f"- {p} → {tgt}")
        lines.append("")
    if actions:
        lines += ["## Действия", ""]
        for p, tgt in actions:
            lines.append(f"- {p} → {tgt[:120]}")
        lines.append("")
    if skills:
        lines += ["## Скиллы", ""]
        for p, tgt in skills:
            lines.append(f"- {p} → {tgt}")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"cheatsheet written: {out} ({len(bundles)} bundles, {len(actions)} actions, {len(skills)} skills)")

if __name__ == "__main__":
    main()
