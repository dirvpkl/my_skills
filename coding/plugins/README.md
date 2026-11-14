# plugins/

`manifest.json` is the discovery file for the `coding` package. It lists every sub-skill (git-workflow, security, docker, process-tiers, code-quality, testing, logging, external-integrations) — not `references/` files, since this package's "modules" are whole skills, each with its own `SKILL.md`. The root `SKILL.md` dispatcher points here instead of hardcoding the list inline.

## Adding a sub-skill
1. Create the folder and its `SKILL.md` (with `name`, `description`, `version` in frontmatter), plus `VERSION`, and any `references/`/`scripts/` it needs.
2. Add an entry to `manifest.json`'s `modules` array: `id`, `name`, `path` (relative to the `coding/` root), `type` (`core` for something always bundled, `plugin` for optional add-ons), `version`, one-line `description`.
3. Add it to the root `SKILL.md`'s "Activation manifest" if it should auto-load alongside other skills for some trigger, and to the "Skill index" either way.
4. Bump `package_version` in `manifest.json` and the root `VERSION` file — any new sub-skill changes overall package behavior. Log it in `CHANGELOG.md`.
5. Run `scripts/check_versions.sh` to confirm the new module's frontmatter version matches the manifest and its path resolves.

## Removing or disabling a sub-skill
Delete its `modules` entry (or move it to a `disabled` array using the same shape if the history should stay documented). Remove it from the root `SKILL.md`'s activation manifest and skill index too — an orphaned reference there is exactly the anti-pattern this manifest exists to avoid. Leave the underlying folder in place unless it's genuinely obsolete.

## Validating
`scripts/check_versions.sh` (run from the `coding/` root) checks: every module's `path` resolves, every module's frontmatter `version` matches what `manifest.json` says, and reports (doesn't error on) any module whose version has moved ahead of the last `package_version` bump — a signal to bump the package version, not necessarily a mistake.
