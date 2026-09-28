# anti-patterns

Referenced by SKILL.md. Concrete mistakes worth avoiding when scaffolding or restructuring a skill, drawn from real cleanup work rather than theory.

## 1. Ambiguous "mention it somewhere" instructions
**The mistake**: a single line in SKILL.md like *"if you find something good, mention it at the end of the report"* — without specifying which of several different things it means. In one real case this line was meant to cover *newly discovered research channels* (a skill-maintenance concern), but its placement right next to report-formatting instructions made it read as if it meant *findings to show the user* (a per-session output concern) — genuinely ambiguous even to the person who wrote it, let alone a model reading it cold.

**The fix**: identify every distinct "thing that gets recorded" a skill produces, and give each one an unambiguous, separately named home:
- Output shown to the user this session → stays only in the response, not written to any file.
- Changes to the skill's own instructions/structure over time → `CHANGELOG.md`.
- Data the skill discovers or accumulates while doing its job, meant to inform *future* runs → its own named file in `references/` (e.g. `source-log.md`, `session-state.md`), with a one-paragraph header at the top of that file spelling out what does and doesn't belong there.

If a skill produces more than one kind of record, each kind gets its own file — don't let one file or one line quietly serve two purposes.

## 2. Hardcoding a module list inside SKILL.md
**The mistake**: SKILL.md contains a bullet list like "see `notes-a.md` for X and `notes-b.md` for Y" typed directly into the instructions. Every time a file is added, removed, or renamed, this list needs a manual, easy-to-forget edit.
**The fix**: point at `plugins/manifest.json` instead of an inline list (see `manifest-format.md`). SKILL.md then only needs one stable sentence — "check the manifest for currently active modules" — regardless of how many modules exist.

## 3. Reserved/future ideas mixed into active instructions
**The mistake**: a paragraph in SKILL.md describing a feature that doesn't exist yet ("could add a memory file for X later") sitting inline among instructions for what the skill actually does right now — a reader can't tell built from aspirational without reading closely.
**The fix**: put not-yet-built ideas in the manifest's `planned` array with `"status": "not built"` (see `manifest-format.md`), not in prose inside SKILL.md. This keeps "what this skill does" and "what this skill might do later" visibly, structurally separate.

## 4. Premature or excessive splitting
**The mistake**: creating `references/`, `plugins/`, and `scripts/` folders for a skill that's genuinely a single short, coherent set of instructions with no sub-topics and nothing that will grow modules over time. This adds ceremony without benefit and makes the skill harder to read, not easier.
**The fix**: see "Scaling the layout down" in SKILL.md. Default to the minimum structure that fits the content today; add folders when a real second reference file, module, or script actually shows up — not preemptively.

## 5. Vague or under-assertive trigger descriptions
**The mistake**: a `description` field that's technically accurate but soft enough that the skill doesn't fire when it should — the most common failure mode for skills generally (under-triggering, not over-triggering).
**The fix**: name concrete trigger phrases and contexts explicitly in the description, not just an abstract category. Compare "helps with dashboards" against "use whenever the user mentions dashboards, data visualization, or wants to display any kind of data, even if they don't say the word 'dashboard'" — the second is far more likely to fire when it should. This is `skill-creator`'s territory in depth (trigger-accuracy evals); scaffolding just needs to avoid writing an obviously weak description in the first place.

## 6. Delivering a `.skill` file where the client won't render it
**The mistake**: assuming every client/interface treats the `.skill` extension as a recognizable, openable file type. In practice this has failed silently in some mobile clients — the file arrives but nothing opens it.
**The fix**: default to packaging as a plain `.zip` unless the target environment is confirmed to handle `.skill` directly (see "Packaging" in SKILL.md).
