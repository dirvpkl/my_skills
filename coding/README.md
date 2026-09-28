# coding skill package

Lives in `~/.agents/skills/coding/` (global, auto-loaded). Root `SKILL.md` is
a pure dispatcher — it contains no process/quality/security rules itself,
only routing logic and versioning bookkeeping. All actual rules live in
8 sibling sub-skills, each a peer module registered in
`plugins/manifest.json`, not a hardcoded list in the dispatcher's prose.

```
coding/
├── SKILL.md                        ← dispatcher: activation manifest + skill index + versioning
├── VERSION                         ← package version (bumped on ANY sub-skill change)
├── CHANGELOG.md                    ← history of changes to the package itself
├── README.md                       ← this file
├── plugins/
│   ├── manifest.json                ← discovery: every sub-skill, its path, version, type
│   └── README.md                    ← how to add/remove a sub-skill
├── scripts/
│   └── check_versions.sh            ← validates each sub-skill's version against the manifest
├── git-workflow/
│   ├── SKILL.md
│   └── VERSION
├── security/
│   ├── SKILL.md
│   └── VERSION
├── docker/
│   ├── SKILL.md
│   └── VERSION
├── process-tiers/
│   ├── SKILL.md
│   └── VERSION
├── code-quality/
│   ├── SKILL.md
│   ├── VERSION
│   └── scripts/
│       └── run_checks.sh           ← format → lint → typecheck → test, fixed order
├── testing/
│   ├── SKILL.md
│   ├── VERSION
│   └── scripts/
│       ├── baseline_diff.sh        ← automates the git-stash regression check
│       └── classify_failure.sh     ← quick environment-vs-code failure triage
├── logging/
│   ├── SKILL.md
│   └── VERSION
└── external-integrations/
    ├── SKILL.md
    └── VERSION
```

## How this is meant to work

- **`SKILL.md`** (root) is the dispatcher. It says which sub-skills load
  together for a given trigger (the "activation manifest"), and how skill
  versions get bumped and kept in sync. It does not contain git/security/
  docker/process rules directly — those are sub-skills like any other.
- **`plugins/manifest.json`** is the discovery file: every sub-skill, its
  path, its version, and whether it's `core` (always bundled) or `plugin`
  (optional). The dispatcher points here instead of hardcoding a sub-skill
  list inline, so adding sub-skill #9 never means editing #1-8's mentions.
- Each sub-**`SKILL.md`** is self-contained enough to read on its own, but
  they cross-reference each other instead of repeating the same rule three
  times (e.g. "fail loud" is defined once in `code-quality`, the others
  just point back to it).
- **`references/`** folders hold longer material a skill points to but
  doesn't inline — e.g. the full fresh-eyes checklist, so its `SKILL.md`
  itself stays short.
- **`scripts/`** folders hold small, boring, deterministic helpers — things
  an agent would otherwise reconstruct by hand every time (the exact check
  order, the stash/pop dance for baseline comparison, a few environment
  sanity pings). They're plain bash/python3, no dependencies beyond common
  CLI tools (`git`, `curl`, `lsof`, `docker`, `python3` if present) —
  missing tools are skipped with a note, not a hard failure.

## Adding a new sub-skill

Same shape as the eight here: a folder, a `SKILL.md` with YAML frontmatter
(`name`, `description`, `version`), a `VERSION` file matching that version,
optional `references/` and `scripts/`. Then register it in
`plugins/manifest.json` (see `plugins/README.md` for the exact steps) and
add it to the root `SKILL.md`'s "Activation manifest" if it should
auto-load with something, and to the "Skill index" either way — a sub-skill
that exists but isn't in the manifest won't reliably load when it should.

## Versioning

Two independent layers, both required:
- **Per-skill version**: each sub-skill has its own `version` (frontmatter)
  and `VERSION` file, bumped independently whenever that skill's rules
  change in meaning (not for typo fixes).
- **Package version**: one `VERSION` at the root and `package_version` in
  `plugins/manifest.json`, bumped whenever *any* sub-skill changes — this
  keeps one place that says "everything here is in sync as of this state,"
  without forcing every unrelated file to bump in lockstep.

Run `scripts/check_versions.sh` after editing any skill file:

```bash
./scripts/check_versions.sh .
```

It checks that every module in the manifest resolves, that each module's
frontmatter version matches the manifest, and that VERSION files match
frontmatter. It also reports (doesn't error on) any sub-skill whose version
has moved ahead of the last package-version bump, as a nudge to bump the
package version too.
