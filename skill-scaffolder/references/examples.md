# skill-scaffolder — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Structure follows content

**Good:** a short single-purpose skill ships as one `SKILL.md` — no empty
`references/`, `plugins/` or `scripts/` folders created "for completeness."
**Bad:** every new skill gets the maximal layout, so half the folders are empty
and the manifest lists no modules.
Rationale: the layout is a claim about how the skill grows; empty scaffolding is
a claim that turns out to be false at the first read.

**Good:** a skill with two genuinely different flows (where to look / how to
look) splits them into `references/` files and SKILL.md points at them.
**Bad:** a 600-line SKILL.md that inlines both flows because splitting "can
happen later."
Rationale: the split is cheap at birth and expensive after the file is loaded
into every session.

## Extend, don't rebuild

**Good:** adding a module to an existing skill reads its `plugins/manifest.json`
first, creates the file, registers it, bumps the version and logs the change.
**Bad:** re-scaffolding the whole skill folder and silently dropping the
reference files that were not re-created.
Rationale: extension is an edit to a live contract — the manifest and VERSION
are what make the addition discoverable and reversible.

**Good:** the new capability is a file in `references/`, registered in the
manifest; SKILL.md gains one pointer line, not a second hand-written module
list.
**Bad:** the module is described in SKILL.md only, so the manifest no longer
says what is loaded and the two lists drift.
Rationale: one registry is checkable; two lists are a future inconsistency.
