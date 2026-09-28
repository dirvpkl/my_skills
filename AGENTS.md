# AGENTS.md — working in this repo

This repo (`my_skills`) holds versioned agent skills. Every file in it is
**English only** — skills, docs, commit messages, comments. No exceptions.

## Layout

- `<skill>/SKILL.md` — trigger, process, output format. Points outward to
  `references/` and `plugins/`, never duplicates their contents.
- `<skill>/references/` — docs loaded on demand, not upfront.
- `<skill>/plugins/manifest.json` — the only registry of modules and
  cross-skill `dependencies`. If manifest and prose disagree, the manifest wins.
- `<skill>/scripts/` — deterministic checks for that skill.
- `<skill>/VERSION` + `<skill>/CHANGELOG.md` — per-skill versioning.
- `scripts/` (repo root) — repo tooling: `validate.py`, `deploy.py`,
  `new_skill.py`, `bump.py`.
- `coding/` is a package: dispatcher `SKILL.md` + 8 sub-skills, each versioned
  independently, plus one package version at `coding/VERSION`.

## Ground rules

1. **Manifest first.** Before reading or editing a skill, read its
   `plugins/manifest.json` (when present) — it lists what is active and what
   this skill depends on. Never hand-maintain module/dependency lists in prose.
2. **Three separate places.** Instructions (`SKILL.md`) vs history
   (`CHANGELOG.md`) vs runtime logs (named file with a what-belongs-here
   header). Never mix them.
3. **Version everything you change.** Bump per `bump.py` (frontmatter +
   `VERSION` + manifest `package_version` + `CHANGELOG` entry, one message).
   If a `coding/*` sub-skill's meaning changes, the `coding` package version
   bumps too — `bump.py` does this unless passed `--no-package`.
4. **Validate before commit.** Run `python scripts/validate.py` from the repo
   root. Non-zero exit = fix before committing.
5. **Commits.** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`,
   `refactor:`), one logical change per commit, English messages.
6. **Deploy, don't hand-copy.** Install skills into a live agent with
   `python scripts/deploy.py [--target DIR] [--skills a,b]`. `--dry-run` first
   when unsure. Repo tooling (`README.md`, `AGENTS.md`, `scripts/`) is never
   deployed — only skill folders.
7. **New skills** go through `python scripts/new_skill.py <name>` (full layout)
   or `--minimal` for single-purpose ones, then get filled in, validated, and
   committed. See `skill-scaffolder` for the full method.

## Do not

- Write non-English text into any repo file.
- Duplicate manifest contents (module lists, dependency names, versions) in
  `SKILL.md` prose or `README.md` tables — point at the manifest instead.
- Commit `.workplanx/` topic folders, `*.zip`/`*.skill` bundles, editor
  clutter, or secrets (see `.gitignore`).
- Change a skill's rules and its version in separate commits — one change, one
  version, one commit.
- Edit `my_skills` content directly in a live skills dir
  (`~/.agents/skills/`); change it here, validate, commit, then `deploy.py`.
