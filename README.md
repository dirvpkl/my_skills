# skills — my skills

Personal skill collection (one folder = one skill: SKILL.md +
plugins/manifest.json). This root also holds **requirements.md**: a
dependency registry in Python-requirements format — what exists, where
it comes from, why, and whether it already replaces something else.
Update it whenever a skill is added or removed; the README is about the
collection's layout, requirements is about the roster and its links.

## Folders

- `<skill>/SKILL.md` — the skill itself; `<skill>/plugins/manifest.json` —
  its modules and dependencies; `<skill>/references/` — the skill's data
  (for example, chords keeps its bindings table in references/bindings.md).
- `runtime.toml` — settings for the collection's runner.

## How skills teach

The collection teaches HOW to think, not rules. Rules govern actions only
(dangerous, destructive, outward-facing); thinking stays free — the more
initiative an agent writes, the more ideas exist, and ideas are the most
valuable output. When in doubt, a skill shows the flow and an example,
never a fence for thought. (Owner principle, 2026-11-14.)

## Built-in, NOT from this collection

Some skills live outside my_skills, built into the host
(`~/.zcode/skills/`), and get wired in through package dependencies.
**What lives there and why — see requirements.md** (section
"Built-in, outside the collection folder"): pony and REA with reasons
and replacement notes, so this file stays lean.
