# AGENTS.md — working in `loop`

English only in every file. No exceptions (repo rule, see `../AGENTS.md`).

- `SKILL.md` is the table of contents: trigger, process, dialog rule, fail-loud.
  Details live in `references/`, never duplicated inline.
- `references/` holds `contract.md`, `stop-signals.md`, `wait.md`. Split along
  natural seams; add a TOC on top once a file passes ~300 lines.
- `plugins/manifest.json` is the only module registry. If manifest and prose
  disagree, the manifest wins.
- `scripts/loop_state.py` is the mechanical verdict. Its output is followed
  without a vote; semantic stagnation belongs to `stop-signals.md`, not to
  the script.
- Dialog rule: no user answer until `STOP`, except destructive or potentially
  harmful next units — then stop and ask first.
- Version every change via `python scripts/bump.py loop --minor|--patch -m "msg"`,
  then run `python scripts/validate.py` from the repo root before committing.
  Conventional Commits, one logical change per commit.
