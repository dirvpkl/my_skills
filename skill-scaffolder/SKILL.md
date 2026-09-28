---
name: skill-scaffolder
description: Scaffold a new Claude skill (or restructure an existing loose one) into a consistent, extensible layout — SKILL.md + references/ + plugins/manifest.json + scripts/ + CHANGELOG.md + VERSION. Use when the user wants to create a new skill, turn a workflow/set of notes into a skill, or reorganize existing skill files into proper modular structure. Not for evaluating or optimizing an existing well-formed skill's trigger accuracy — for that, defer to skill-creator if present.
version: 1.0.0
---

# skill-scaffolder

Sets up the *file layout* of a skill so it's modular and extensible from day one — plugin discovery via a manifest instead of hardcoded references, a place for logs/history that doesn't get confused with the skill's core instructions, and a script to sanity-check it all. This is deliberately narrow: it's about structure and scaffolding, not about testing trigger accuracy or running eval loops. If this environment has `skill-creator` available and the user wants evals, benchmarking, or description-optimization, point them there instead — this skill and that one are complementary, not competing.

- **references/layout.md** — the full target directory layout, explained file by file.
- **references/manifest-format.md** — the exact shape of `plugins/manifest.json` and how discovery works.
- **references/anti-patterns.md** — mistakes to avoid, drawn from real cleanup work (ambiguous "mention it somewhere" instructions, hardcoded file lists, mixing logs with instructions).
- **assets/templates/** — blank starting files to copy: `SKILL.md`, `manifest.json`, `CHANGELOG.md`, `validate_manifest.py`.
- **scripts/scaffold.py** — generates the full directory structure with templates filled in, given a skill name.
- **scripts/validate_manifest.py** — copied into every scaffolded skill; also runnable directly here to check a manifest before handing it off.

## Trigger
- User wants to create a new skill from scratch.
- User has a rough idea, a workflow, or a pile of notes and wants it turned into a skill.
- User has an existing skill that's a single flat file, or several loose files with no manifest/discovery, and wants it reorganized.
- Do NOT trigger for: writing evals, running trigger-accuracy tests, optimizing a skill's `description` field for better triggering, or benchmarking skill performance — that's `skill-creator`'s job, not this one's.

## Core layout (what gets created)
```
skill-name/
├── SKILL.md                  — required. Frontmatter (name, description, version) + instructions.
├── VERSION                   — plain semver string, kept in sync with SKILL.md frontmatter.
├── CHANGELOG.md               — history of changes to the skill itself.
├── references/                — docs loaded into context as needed, not upfront.
│   └── (topic-specific .md files)
├── plugins/
│   ├── manifest.json           — discovery: lists every active module, the skills this one
│   │                            depends on, plus planned/reserved ones.
│   └── README.md               — how to add/remove a module or a dependency.
├── scripts/                    — executable code for deterministic tasks (validation, generation, etc.)
└── assets/                     — templates/files used in output, if the skill produces files.
```
Not every skill needs all of these — see "Scaling the layout down" below. But when in doubt, this is the full shape, and it's easier to omit an empty folder than to retrofit one in later.

## Process
1. **Understand what the skill is for.** Ask (or infer from conversation) what the skill should do, when it should trigger, and roughly how it should work — same intent-capture as any skill-writing task. Don't skip straight to file structure before this is clear; structure follows content, not the other way around.
2. **Check for existing material.** If the user already has a draft (a single .md file, a doc, a set of loose notes) — read it fully before scaffolding. Restructuring existing content is the common case, not writing from zero.
3. **Decide the module split.** One SKILL.md always. Beyond that, split into `references/*.md` files along natural seams — e.g. "where to look" vs. "how to look" (see the researcher skill as a worked example), or by domain/variant (aws.md / gcp.md / azure.md style) if the skill covers multiple parallel cases. Don't split prematurely — a skill that's genuinely one coherent flow doesn't need `references/` at all.
4. **Scaffold the files.** Either run `scripts/scaffold.py <skill-name>` to generate the skeleton with templates filled in, or build it by hand using `assets/templates/` as a starting point — either is fine, script is just faster for the boilerplate.
5. **Write SKILL.md last, pointing outward.** The core file should read like a table of contents with process/trigger/format info, not contain everything inline. If SKILL.md is approaching ~500 lines, that's the signal to push more into `references/` — see `references/layout.md` for the progressive-disclosure reasoning behind this.
6. **Set up the manifest, even for a simple skill.** Even a skill with just one or two reference files benefits from `plugins/manifest.json` from day one — it costs almost nothing now and means the *next* addition doesn't require restructuring later. See `references/manifest-format.md` for the exact shape. Two different questions live there and must not be merged: `modules` = what's inside this skill, `dependencies` = which *other* skills load alongside it. If this skill hands off to a sibling skill, that name goes in `dependencies` — never as a hand-written list in this file, which is the failure mode the manifest exists to prevent.
7. **Validate before handing off.** Run `scripts/validate_manifest.py` inside the new skill folder. Fix anything it flags.
8. **Package and present.** If a file-presentation tool is available, zip the skill folder and present it (see "Packaging" below). Skills should be delivered as a folder/zip the user can inspect or install, not just described in chat.

## Separating instructions from history from logs
This is the single most common mess in ad-hoc skills, worth calling out on its own: a skill's core instructions (SKILL.md), its own change history (CHANGELOG.md), and any *runtime data it produces or logs while doing its job* (a findings log, a discovered-sources log, a session tracker) are three different things and belong in three different places. A single ambiguous line like "mention a good find at the end" invites confusion about which of these three it means. When scaffolding, if the skill's job involves producing or accumulating any kind of log, give it its own named file in `references/` (or a dedicated `state/` folder if it's meant to be read back and updated across runs) with a short doc at the top of that file saying explicitly what does and doesn't belong there — see `references/anti-patterns.md` for a concrete before/after.

## Scaling the layout down
Not every skill needs the full shape:
- A short, single-purpose skill with no sub-topics and no reference material → just `SKILL.md`. Don't create empty `references/`, `plugins/`, or `scripts/` folders for their own sake.
- A skill with reference docs but no meaningful "modules" to toggle → `references/` files are fine without a `plugins/manifest.json` at all, if there's no real plan to add/remove modules over time. The manifest earns its place when a skill is expected to grow pluggable pieces (like the researcher skill's planned session-tracker / findings-memory / output-formatter), not by default on every skill.
- A skill that never produces files → no `assets/` folder.
The point of scaffolding isn't maximal structure, it's the *right* structure for what the skill actually needs to stay unambiguous as it grows. Ask if unsure rather than defaulting to the maximal layout every time.

## Packaging
If `present_files` (or an equivalent file-delivery tool) is available: zip the finished skill folder (e.g. `zip -r skill-name.zip skill-name/`) and present the zip, not a bare `.skill` extension — some clients don't render `.skill` as an openable file type, plain `.zip` is the safer default unless the user's environment is confirmed to handle `.skill` directly. Mention the target platform if it matters (mobile file managers reliably open `.zip`; ambiguity about `.skill` support is a real reported failure mode, not hypothetical).
