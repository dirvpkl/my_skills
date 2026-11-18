# Changelog

## [2.3.0] - 2026-11-18
- The creative machinery moved IN (owner ruling: «все в майндшторм» — no
  separate serendipity skill): references/thought-work.md holds wild-shots
  (moved from spine, no caps), gems (the judgment criteria; storage stays
  workplanx's), associations and the how-to-look procedure. The wild-shot
  example scenes moved here from spine's examples.

## [2.2.0] - 2026-11-18
- NO CAPS (owner ruling: «не нравятся мне ограничения», «агент сам будет
  предлагать, сколько показать. либо все»): the 2-3 candidate cap removed
  from method.md + SKILL.md step 5 (a list turning unwieldy is a
  verb-coarseness symptom, not a trimming job); the fog volley "up to
  three" removed.
- Instructional lines moved OUT of the method (owner: instructions live in
  examples — the method explains how to think): the faces-suggest-verbs and
  candidate-vs-analogy checks became worked demonstration scenes in
  examples.md. The spine one-wild-shot cap removal is queued for spine's
  walkthrough turn.

## [2.1.0] - 2026-11-18
- The association now threads ALL steps (owner: «кубик должен быть во время
  майндшторма как раз, все вообще должно быть»): the analogy's faces suggest
  the verb split (step 1), it anchors the abstraction climb (step 2, since
  1.18.0), and every candidate is checked against it in the proposal
  (step 5) — a candidate fighting the analogy fights the task.

## [2.0.0] - 2026-11-18
- RENAMED: solution-search -> mindstorm (owner pick 2026-11-18, a
  brainstorming-adjacent name; "brainstorming" itself was ruled избитое).
  Folder, frontmatter name and the title moved; the "aka brainstorm"
  alias dropped — mindstorm IS the brainstorming skill now. All cross-
  references across the collection updated in the same pass.

## [1.19.0] - 2026-11-18
- Evidence rule widened (owner ruling): evidence = what the next agent can
  RE-CHECK — a URL for the web, a file path (+ line) for anything local, a
  command's output for anything runnable; never memory. "No URLs" reworded
  to "no evidence" across method.md, SKILL.md and the serendipity block.

## [1.18.1] - 2026-11-18
- verb-radar.md: the summon-phrase list removed (the summon register lives
  in chords, not in reference files); the pre-verdict ALWAYS rule kept,
  section renamed off the retired word.

## [1.18.0] - 2026-11-18
- method.md, the abstraction step: hold an association while climbing — an
  analogy whose structure maps onto the task anchors the abstract<->concrete
  hops in both directions (the owner's associations directive landed; the
  workplanx plan.md contract carries the same association line).

## [1.17.1] - 2026-11-17
- examples.md: every case now carries >=2 Good/Bad pairs (the collection convention) — one teaching couplet added per single-pair section.

## [1.17.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- `## Trigger` section removed; its live modes (fog, summon register) are
  already in Process and the description.
- New "Sibling borderline" section: what routes to researcher first and what
  is this skill from the first line.

## [1.16.3] - 2026-11-15
- Description: dropped the reference to the deleted `thinking` dispatcher;
  the no-double-invoke note now points at the think-first chord.

## [1.16.2] - 2026-11-12
- validate_manifest.py: missing-runtime.toml diagnostic and non-table [skills] guard


## [1.16.1] - 2026-11-12
- validate_manifest.py: dependencies_runtime resolution and module type check


## [1.16.0] - 2026-11-11
- Trigger contract sweep: description rewritten as a use-when / not-for / sibling contract with literal user phrases; rules and body unchanged.

## [1.15.0] - 2026-11-08
- fog volleys must differ in essence, not three variants of one shot


## [1.14.0] - 2026-11-08
- fog mode (shot-in-the-dark): up to 3 labeled wild-shot volleys for inarticulate ideas, spine cap waived by explicit request


## [1.13.0] - 2026-11-08
- directive description: imperative trigger + negative constraint (trigger reliability sweep)


## [1.12.0] - 2026-10-31
- `spine` (new sibling skill, 1.0.0) added to dependencies: ideation turns now bundle the own-take quota, labeled wild-shots, and no reflexive agreement. No rule in this skill changed — the link lives only in the manifest, replacing prose.

## [1.11.0] - 2026-10-31
- `method` (1.4.0 -> 1.5.0): class-and-role clarity for user examples — an example illustrates a class and smuggles a role (source of material vs sales channel vs tool); name both separately before querying, one line in the topic folder. Session-learned: anchoring on the user's nouns produced candidates for the wrong role entirely.
- `brainstorm` (1.0.0 -> 1.1.0): concept-chain maps from the topic folder seed the diverge step (every top node is a route candidate); a node earns no standing without a cost and a checkable condition — the map widens where to look, never substitutes for evidence.
## [1.10.0] - 2026-10-21
- Brainstorm mode added: the stuck case (what could we do about this) gets its own mechanics - inventory the spendable assets, diverge into routes with measurable costs, keep rejected routes and say whether the reason still holds, close dead ends with their evidence, converge on a pick. New module references/brainstorm.md; the default find-the-technique mode is unchanged.


## 1.9.0 — 2026-09-26
- `dependencies: ["workplanx"]` declared in the manifest. This skill's output only exists as files in a workplanx topic folder — that was already true, but the link was prose in SKILL.md, which is the list-that-rots pattern.
- The ladder rank names in this file are now the collection's single vocabulary; `coding/external-integrations` deleted its own copy (1.6.0) rather than keeping a second list that could drift.

## 1.8.0 — 2026-09-26
De-coded: the skill claimed any domain while its method was software-only.
- `method` (1.3.0 → 1.4.0): ladder is now domain-neutral — `<oss-project>` → `<open-project>`, `<library>` → `<component>`, `<own-code>` → `<own-make>`; "hand-rolled I/O"/"maintained code" tradeoffs → "doing it from scratch"/"what you carry afterwards"; "wiring belongs to the implementation skill" → "doing belongs to whatever acts on the decision". Registry/lift-implementation anti-pattern generalized (the registry itself moved to the executing side in 1.7.0).
- SKILL.md: description and Trigger no longer mention code, migrations or configs; the `external-integrations` route-out is gone (that skill no longer receives anything from here). Duplicated "decompose into verbs" step collapsed into one.
- New section "Where 'nothing gets made yet' is actually enforced" — points at the `workplanx` build gate and the `coding` dispatcher, since a prose rule inside this file is not a gate.
- `scripts/validate_manifest.py` added — `plugins/README.md` referenced a script the skill did not ship.

## 1.7.0 — 2026-09-23
- Brainstorm generalized: works for any domain (code, video, anything) — trigger covers "how to / what to use / find technique".
- Moved out to coding/external-integrations: default-stack, known-services, holes, scan-protocol (concrete portrait knowledge lives on the implementation side). This skill keeps method only.

## 1.6.1 — 2026-09-22
- Alias: brainstorm. Description + header now name it so triggering by "brainstorm" works; researcher links here.

## 1.6.0 — 2026-09-22
- `default-stack` (1.3.0 → 1.4.0): libs section — tenacity (retry), cachetools (TTL/LRU), dataclasses/pydantic (typed models at medium+, pydantic under API server), dynaconf-class (layered config, optional), SQLAlchemy (relational access). Hand-rolled loops/dicts/env-parsing/raw-SQL are replace-candidates.

## 1.5.0 — 2026-09-22
- `known-services` (1.0.0 → 1.1.0): portability purge — all machine-local rows removed; registry is a shell with regen note, patterns live in default-stack. Skills must work on any machine.

## 1.4.0 — 2026-09-22
- `default-stack` (1.2.0 → 1.3.0): inference section (CPU-only always, infinity-class embedding sidecar); holes moved to `references/holes.md`.
- `method` (1.2.0 → 1.3.0): zero-candidate escape hatch (queries + no candidates = legitimate own-code decision); SKILL output now names topic-folder files; disk-lifting ban.
- New modules: `holes` + `scan-protocol` (split out of default-stack/known-services per fresh-eyes).

## 1.3.0 — 2026-09-22
- `default-stack` (1.1.0 → 1.2.0): de-concretized — all project names removed, entries describe pattern shape + why; blessed product names kept (they are the answers). Hard rule: never open inventoried repos on disk to copy implementation.
- `method` (1.1.0 → 1.2.0): disk-lifting ban added to anti-patterns.

## 1.2.0 — 2026-09-22
- `method` (1.0.0 → 1.1.0): serendipity capture — up to 3 off-track finds with URLs in `search.md`, never promoted into the decision unasked.
- `default-stack` (1.0.0 → 1.1.0): store split into db rule (joins → postgres, docs → mongo) + files ladder (mount → S3 → telegram-drive cold); infra-verify rule (infra rots fastest, confirm docs per session); Alertmanager only with metrics, TG send until then.

All notable changes to this skill are logged here. This tracks changes to the *skill itself* — not runtime data the skill produces or logs while doing its job.

## 1.1.0 — 2026-09-22
- Added `references/default-stack.md`: blessed portrait defaults per need (serve/tasks/schedule/NATS-default stream/logging/health/alerter/store/post) + known holes. Step 1 now checks defaults first — matching verb = reuse, not search.

## 1.0.0 — 2026-09-22
- Initial version: pre-code search split out of external-integrations. Placeholders-only core, concrete inventory in references/known-services.md.
