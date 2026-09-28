# layout

Referenced by SKILL.md. Full explanation of each piece of the target directory layout and why it exists.

## Progressive disclosure — the reasoning behind splitting files at all
Skills load in three tiers:
1. **Metadata** (`name` + `description` in frontmatter) — always in context, cheap, this is what triggers the skill at all.
2. **SKILL.md body** — loaded into context once the skill is triggered. Ideally under ~500 lines; longer is fine but is a signal to consider pushing detail into `references/`.
3. **Bundled resources** (`references/`, `plugins/`, `scripts/`, `assets/`) — loaded only as needed, on top of tier 2. This tier is effectively unlimited in size because nothing in it costs context until it's actually read.

The practical implication: put anything that's only needed *sometimes* (a specific domain's details, a long channel checklist, historical log data) into tier 3, and keep tier 2 as the connective tissue — trigger conditions, high-level process, and pointers to the right tier-3 file. A SKILL.md that inlines everything defeats the purpose of having tiers at all.

## File-by-file

**SKILL.md** (required, always present)
Frontmatter needs `name` and `description` at minimum; add `version` if the skill will evolve over time (recommended for anything beyond a one-off). The description is the *only* thing that determines whether the skill triggers — write it a little assertively (name concrete trigger phrases/contexts) rather than vaguely, since under-triggering is the more common failure mode than over-triggering.

**VERSION**
A bare semver string (e.g. `1.2.0`), nothing else. Exists so a script or a human can check the current version without parsing YAML frontmatter or a changelog. Keep it identical to the `version` field in SKILL.md's frontmatter — if they drift, something was updated inconsistently.

**CHANGELOG.md**
Human-readable history of changes *to the skill*, one entry per version bump. This is not a place for runtime logs the skill produces while doing its job (research findings, discovered sources, session state) — see `anti-patterns.md` for why conflating these causes confusion.

**references/**
Markdown files with detail the skill needs sometimes, not always. Split along natural seams:
- *Where vs. how* — one file covering *what* to check, another covering *how* to check it once there (this is the shape used in the researcher skill: `sources.md` vs. `patterns.md`).
- *Domain/variant* — when a skill supports several parallel cases that are mostly independent (e.g. `aws.md`, `gcp.md`, `azure.md` for a deploy skill) — the core SKILL.md handles selection/workflow, each reference file handles one variant in full.
- *Log/state files* — if the skill produces or accumulates data across runs (a discovery log, a running todo), that's still a `references/` file (or its own `state/` folder if there'll be several), but it needs an explicit header explaining it's data, not instructions — the model reading it later needs to be able to tell the difference at a glance.

For any reference file over ~300 lines, add a table of contents at the top so a partial read is still useful.

**plugins/**
- `manifest.json` — the discovery file. See `manifest-format.md` for its exact shape. Its purpose is to let SKILL.md say "check the manifest for what's currently active" instead of hardcoding a list of reference files inline — so adding module #4 never means editing module #1-3's descriptions again. It carries two independent keys: `modules` (files inside this skill) and `dependencies` (other skills in the collection that load with it). Both live here for the same reason — a list kept in SKILL.md prose is a list that rots.
- `README.md` — short doc: how to add a module, how to remove/disable one, how to add a dependency, how to run the validator. Copy `assets/templates/plugins-readme-template.md` and adjust wording to the specific skill.

**scripts/**
Executable code, for anything deterministic that shouldn't be re-derived by the model each time — validation, generation/scaffolding, data transforms. Scripts can be referenced and run without loading their contents into context, which is the point: heavy logic lives here instead of as prose instructions in SKILL.md.

**assets/**
Files used *in the skill's output* — templates, boilerplate snippets, icons, starter files the user's finished artifact is built from. Not used for the skill's own reference material (that's `references/`) or its own code (that's `scripts/`).

## When a skill doesn't need all of this
See "Scaling the layout down" in SKILL.md — this file describes the maximal shape, not a mandatory checklist.
