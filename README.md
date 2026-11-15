# skills — my skills

Personal skill collection: one folder = one skill. This README is the
concepts doc: it carries the phenomena and the rules of how skills work
here — a fresh agent reading only this file should understand the whole
system. It is filled in as the concepts evolve (owner + agent, in
parallel with the discussions).

The collection is harness-agnostic: nothing here names a concrete
harness, machine, or person. Concreteness lives in each skill's
`references/examples.md`; personal phrases live only in `chords/`.

## The one-sentence model

A skill is a folder of abstract method and rules; the harness loads
skills by their folder and frontmatter description; every concrete
pattern lives in that skill's `references/examples.md`.

## Concepts & phenomena

**Skill.** One folder = one skill: `SKILL.md` (frontmatter: name,
description, version — then abstract instructions), `references/` (data
files the skill reads as needed), `scripts/` (executable helpers),
`plugins/manifest.json` (what loads alongside), `VERSION` +
`CHANGELOG.md`. Skills are abstract: no concreteness, no
personalization — the good/bad pairs in `references/examples.md` carry
the concrete patterns and are read beside the SKILL.md as binding
context.

**Trigger.** Two layers: (a) the `description` in SKILL.md frontmatter —
the surface the harness matches against what the user says, deciding
which skill to offer; (b) an optional `## Trigger` section in the body —
the skill's own statement of when it applies. A skill that is always
part of the setup (like base) has no Trigger section: it is never
invoked, it is already running.

**base.** Always loaded, governs every task: delegation carries a log
path, facts resolve at runtime, unclear or risky items become a user
pick, a failed skill load is recovered from disk, everything written is
English, a project's own .md files are read before acting.

**User pick.** One message presenting the situation and the options; the
user's choice is the only thing that proceeds past it. Unclear, risky,
or guessable work is a pick, not a guess — the same protocol as
workplanx's decision gate.

**workplanx topic folder.** Every non-trivial task gets
`<project>/.workplanx/<topic>/` with plan → search → decision → log →
gate. The owner's words land there verbatim, dated; the inbox
(`_inbox/`) is a first-class source for recap and handoff. Chat is the
conversation; the folder is the record.

**Chords.** The shorthand layer, read alongside base from session start:
the user's phrases are shorthand /commands, matched by MEANING —
synonyms and paraphrases count, literal strings are the floor. A
`bundle` is a skill stack fired by one phrase; bundle definitions live
only in chords bindings.

**Dependencies.** `plugins/manifest.json` = `{skill, dependencies,
planned}` — lean by convention: the folder layout is the module list,
versions live in VERSION, there is no dependencies_runtime. An internal
dependency is mandatory (missing = loud failure). An EXTERNAL skill
(harness-side, not in this collection) fails safe: report it and offer a
user pick — search for it, skip it, or another route. External skills
with upstream links: `requirements.md`.

**Runtime values per skill.** Machine facts (ports, hosts, tokens) live
in `<skill>/runtime.toml` — gitignored, never tracked; the tracked
`<skill>/runtime.example.toml` documents the shape. Facts resolve at
runtime: the environment is the truth, a path frozen in a plan is
already stale.

**One validator.** `scripts/validate.py` checks the whole repo: skill
frontmatter, VERSION sync, lean manifest shape, dependency resolution,
runtime.toml parse, wiki-links. There are no per-skill validators.
Helper tools live in root `scripts/` (collection-level, not part of any
skill).

**Versioning.** `VERSION` matches the SKILL.md frontmatter version;
every change lands in the skill's `CHANGELOG.md`; versions move with
`scripts/bump.py`.

**Git everywhere.** Version control is the default for ANY project —
code, notes, brainstorms, docs. The preflight (is this a repo? what is
already dirty?) runs before the first write; details in `git-workflow`.

**Fail loud.** A destructive op done unasked is a failure even when it
worked; a skipped check reported green is a lie; a down dependency stops
the item and asks.

**Depersonalization.** Tracked files are portable: no machine values, no
personal phrases, no harness names, English-only. The allowed-language
zones: `chords/` (the owner's phrases) and `references/examples.md`
(the concrete patterns).

**Graveyard.** Retired skills go to the graveyard with tombstones —
never silently deleted, never resurrected without the owner.

**Delegation.** Work goes to agent sessions; every delegation prompt
names the project's topic log path, and the log is the only progress
signal — silence past the natural cadence means stalled, then ping once
and replace.

**Gates.** `workplanx/scripts/plan_gate.py` checks the topic folder's
shape per phase (plan/search/decision/build). A red gate is a stop and a
question, never a silent workaround.

## Root files

- `AGENTS.md` — how agents work in this repo: the editing rules.
- `instructions_for_harness.md` — the one-line pointer harnesses inject
  into prompts: invoke Skill(base) first; everything is in base.
- `requirements.md` — external skills only (vendored / built-in), with
  upstream links; collection-internal skills are not listed — the folder
  layout is the roster.
- `scripts/` — collection-level tools (validator, trigger checker,
  version bump, scaffold helpers), not part of any skill.

## How skills teach

The collection teaches HOW to think, not rules. Rules govern actions
only (dangerous, destructive, outward-facing); thinking stays free — the
more initiative an agent writes, the more ideas exist, and ideas are the
most valuable output. When in doubt, a skill shows the flow and an
example, never a fence for thought.
