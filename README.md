# skills — my skills

Personal skill collection: one folder = one skill (SKILL.md +
plugins/manifest.json + references/ + VERSION + CHANGELOG.md).

## Root files

- `AGENTS.md` — how agents work in this repo: the editing rules.
- `instructions_for_harness.md` — the one-line pointer harnesses inject
  into prompts: invoke Skill(base) first; everything is in base.
- `requirements.md` — external skills only (vendored / built-in), with
  upstream links; collection-internal skills are not listed — the folder
  layout is the roster.
- Runtime values are per-skill: `<skill>/runtime.toml` (gitignored), shape
  documented by `<skill>/runtime.example.toml` (tracked).

## How skills teach

The collection teaches HOW to think, not rules. Rules govern actions only
(dangerous, destructive, outward-facing); thinking stays free — the more
initiative an agent writes, the more ideas exist, and ideas are the most
valuable output. When in doubt, a skill shows the flow and an example,
never a fence for thought. (Owner principle, 2026-11-14.)

## Built-in, NOT from this collection

Some skills live outside my_skills, built into the host
(`~/.zcode/skills/`), and get wired in through package dependencies.
**What lives there and why — see requirements.md**: ponytail,
frontend-design, REA with sources and replacement notes, so this file
stays lean.
