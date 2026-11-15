# AGENTS.md — working in this repo

You are modifying the skill collection itself. `instructions_for_harness.md`
is the one-line pointer harnesses inject into prompts; this file is the
working guide for agents editing here. Skill(base) is invoked at session
start and governs everything below.

## Non-negotiables

- **Personal data stays out of tracked files.** Owner phrases live only in
  `chords/`; machine-local values (ports, hosts, tokens) only in a skill's
  own `runtime.toml` (gitignored). Tracked files are portable.
- **Skills are abstract.** A skill carries method and rules only — no
  concreteness, no personalization; every concrete pattern lives in the
  skill's `references/examples.md`.
- **Skill changes go through `skill-scaffolder`.** New or restructured
  skills get the modular shape (SKILL.md + plugins/manifest.json +
  references/ + VERSION + CHANGELOG); versions move with `scripts/bump.py`.
- **Ask rules.** Destructive, secret, out-of-scope, mass, public-facing:
  stop and ask. Derivable calls: decide, do, report — don't ask.

## Layout

- `<skill>/` — one skill per folder: SKILL.md, plugins/manifest.json,
  references/, scripts/, VERSION, CHANGELOG.md.
- `instructions_for_harness.md` — minimal harness-injected pointer (base
  first); `requirements.md` — external skills only, with upstream links.
- `<skill>/runtime.toml` — that skill's machine values (gitignored);
  `<skill>/runtime.example.toml` — its tracked shape.
