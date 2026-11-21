# Changelog

## [1.12.0] - 2026-11-21
- option text v3 per owner design: aliases + kind + intent sentence (I need to launch skill X) + target skills' descriptions pulled from the live catalog — the embedder matches MEANING (descriptions), not surface words; v2 aliases-only lost the semantic jumps (fuzzy layer 1/6 -> 4/6 on the honest set); cache hash covers composed texts (catalog descriptions live outside chords.md)


## [1.11.0] - 2026-11-21
- B+ hybrid decider: literal substring fast-path fires ALL matched rows (multi-binding sentences decompose there), shorter-alias-contained-in-longer loses per the table's collision notes, placeholder aliases dropped; embeddings remain the single-intent fuzzy layer for the no-literal-hit remainder


## [1.10.1] - 2026-11-21
- cache hash includes the embedder model - a model swap must not reuse vectors from another space


## [1.10.0] - 2026-11-21
- decider rewritten: embeddings + cosine via the owner's tei stack (microsoft/harrier-oss-v1-0.6b, MTEB-multilingual #1) instead of the decision-model API; option text = alias list + kind (full-row notes blurred the phrase signal); row vectors cached by chords.md hash; calibrated: noise <=0.49, intent 0.61-0.72, threshold 0.55; hook wall-clock 0.66s incl. interpreter start


## [1.9.0] - 2026-11-21
- chords-decider hook: UserPromptSubmit -> decision model -> binding-match kick; config in runtime.toml [decider] (endpoint/api_key/model/threshold); silent pass without config or on error; meaning-match stays the agent's job


## [1.8.1] - 2026-11-18
- examples.md: one leftover "trigger phrase" wording replaced (the word stays retired).

## [1.8.0] - 2026-11-17
- The Desktop cheatsheet card is GONE (owner ruling: "зачем вообще на раб
  столе что-то? я думал список чордов в папке скилла") — chords/chords.md
  IS the list, no derived render, no second artifact. make_cheatsheet.py
  deleted (its only job was the card); the regen instruction removed from
  the table header and the skill; "mention the change" stays.

## [1.7.0] - 2026-11-17
- Chord watching goes FULL background (owner ruling): no prescribed
  observation procedure — the agent notices what it notices, proposes the
  chord in one line if it does; the prescriptive discipline (cross-session
  rule, one-open-proposal cap, session-end timing) removed — "сам
  разберётся".
- Cheatsheet card renamed: chords-cheatsheet.md -> chords.md (Desktop),
  script + SKILL.md term updated.

## [1.6.0] - 2026-11-17
- "What a chord is" section (owner ruling): the chord DEFINED — a fixed
  personal association, recognized by word work (look at the words,
  translate RU/EN, run associations and hold them against targets, fix the
  meaning, compare) — not string matching. Terms follow after the concept.
- Initiative discipline (owner ruling): watching is free and rides normal
  turns, never a task of its own; the task's attention wins — no proposals
  mid-task; patterns repeat across sessions before proposing; at most one
  open proposal; one decline retires the pattern forever.
- examples.md: word-work case (translate/associate/fix/compare, structure-
  carrying analogies) + proposal-discipline case (rare, timed, retired on
  decline).

## [1.5.0] - 2026-11-17
- SPLIT (owner ruling): the chord DATA moved to chords.md (the data file
  bound to the skill); SKILL.md now carries mechanics + the vocabulary
  (binding, kinds incl. bundle, cheatsheet).
- INITIATIVE section (owner ruling): watch for repeating phrase patterns,
  propose chords in one line (never self-bind, never repeat after a
  decline); added/changed chords are mentioned when they land + cheatsheet
  regenerates same turn.
- Doubtful match REVERSED (owner ruling): a plausible match leans in —
  named and confirmed before loading, never dismissed as "not bound";
  no literal-matching floor, no hard keywords.
- make_cheatsheet.py rewired to chords.md; examples.md doubtful-match
  section rewritten to the reversed rule.
- description: "suggest" added to the ask list (proposals are an ask too).

## [1.4.1] - 2026-11-17
- examples.md: the 'The metaphor name doesn't hijack the domain' section was duplicated whole (header + first pair) by the 1.3.0 append — duplicate removed, both couplets live under one header.

## [1.4.0] - 2026-11-17
- Description trimmed to ~400 chars; the contract is unchanged
  (what it is + ALWAYS invoke + NOT for).

## [1.3.0] - 2026-11-15
- Per-skill review round. `## Trigger` and `## Does NOT trigger on`
  sections folded away (owner ruling: trigger sections are cargo-cult,
  the word is retired from docs) — the confirm-before-write line merged
  into "Editing bindings", the free-form/normal-routing nuance into
  Process step 4.
- Description rewritten intent-only: quoted owner-phrase lists removed
  (descriptions carry intent, not keyword lists). Exam-gated.
- Manifest: superseded `trigger-log` planned entry removed (trigger
  accounting lives in workplanx/references/trigger-log.md since
  2026-11-15).
- bindings.md: "each skill's trigger" reworded to description; the two
  dangling wiki-links to Desktop-record topics made plain text (checker
  stays portable, the reference keeps pointing there for humans).
- examples.md: +1 couplet in the five single-pair sections — every case
  now carries ≥2 pairs (boundaries convention).

## [1.2.0] - 2026-11-15
- Read alongside base at session start (owner ruling): phrases are
  shorthand /commands, matched by meaning — synonyms and paraphrases
  count, literal matching is the floor. Doubtful match = "not bound" +
  an offer.


All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job (that belongs in a dedicated references/ file — see references/anti-patterns.md in skill-scaffolder for why these should stay separate).

## 1.1.0 — 2026-11-11
- Trigger contract sweep alignment: description gains the ALWAYS-invoke imperative (lint requirement); bindings data unchanged.

## 1.0.0 — 2026-11-11
- Initial release: personal shortcut bindings. `references/bindings.md` holds the phrase → target table (kinds: `skill` / `bundle` / `action`); the table is user-edited data — row edits never bump the version and never pass a gate.
- Resolution is same-turn and step-aside: load the mapped target as if the user had typed /name; unknown binding = one-line "not bound", never a guessed target.
- Initial table carries this session's real phrases (thinking, fresh-eyes, loop, mission, researcher, one action row); RU and EN aliases in the same rows.
- Near-miss counterexamples: actual music chord questions are answered directly; explicit /commands and skill names always win over a binding.
- `planned` registers the parked `trigger-log` module (fold observed trigger misses back into bindings/descriptions).
