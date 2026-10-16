# my_skills

Custom skill collection for opencode-style agents. Each skill is a self-contained
module: `SKILL.md` (trigger, process, output format) + `references/` (docs loaded
on demand, not upfront) + `plugins/manifest.json` (module registry and
cross-skill dependencies) + `scripts/` (deterministic checks) + `VERSION` +
`CHANGELOG.md`.

The collection is built around one idea: **structure verifies, prose does not.**
Agents log to files, gates check file shape, judges review diffs — nobody is
trusted on their word.

---

## How the pieces fit

Standard task pipeline (each step writes to the same topic folder):

```
workplanx → solution-search → coding → testing → fresh-eyes
(plan+gate)  (pick approach)   (build)  (prove)    (judge)
```

Scale ladder (which driver owns the work):

```
mission  — goal too big for one pass → board of verifiable cards, one subagent per card
loop     — one card / one condition → repeat iterations until a verify command passes
workplanx — single task → topic folder + phase gate; no implementation before user pick
```

Feeding the pipeline:

```
researcher → solution-search   (surfaces findings, hands off pre-decision choices)
coding ──→ fresh-eyes          (both modes when the task came from a plan)
```

`skill-scaffolder` stands apart: it makes new skills in this same layout.

---

## Skill catalog

### workplanx (v1.4.0) — plan-and-log router

Owns the topic folder. Every non-trivial task gets
`<project>/.workplanx/<topic-slug>/` with files written strictly in order:
`plan.md` → `search.md` → `decision.md` → `log.md` → `gate.log`.

- **Trigger:** any non-trivial task (feature, integration, replacement,
  multi-step fix). Never trivial edits. Declared in the `dependencies` of every
  other skill — skipping the folder breaks the dependency, not just ceremony.
- **Mechanics:** nothing gets built before `decision.md` carries a transcribed
  `user-pick:` — enforced by `scripts/plan_gate.py --phase build`, not by agent
  memory. Red gate = stop and message the user. Every acting skill appends one
  entry per skill to `log.md` (what it did, found, left out).
- **Output:** topic folder with five files, each passing its phase gate.
- **Not its job:** judging finished work — that is `fresh-eyes`.

### solution-search (v1.9.0, aka brainstorm) — pre-decision approach search

Finds the way to do a thing before anyone does it. Any domain, digital or
physical. Pure method, zero domain knowledge — concrete stacks/registries live
on the executing side, never here.

- **Trigger:** "how to do X / what to use for X / is there a better way than
  our own X" — before anything is designed or built. Never for executing an
  already-chosen approach.
- **Mechanics:** decompose the task into verbs (one verb = one search unit,
  never search the whole task as one query); generalize each verb up
  (task → task class → who else solves it); walk the less-make ladder top-down
  per verb (`hosted` > `open-project` > `component` > `template` > `own-make`),
  stopping at the first fitting level — `own-make` needs a written reason.
  Every candidate needs URL evidence; no URLs = no result (a logged zero-result
  search is itself a legitimate outcome).
- **Output:** `search.md` per verb + `decision.md` with max 2–3 candidates,
  tradeoffs, one recommendation, and a verbatim-transcribed `user-pick:`.
  Produces a decision, never the thing — no artifacts, no scaffolding.
- **Enforcement:** the binding check lives in `workplanx`'s build gate, not in
  this file's prose. Skip the search and the gate still blocks.

### coding (v1.13.0) — dispatcher for the code package

A router, not a rulebook. Contains no quality/security rules itself — given a
task, it decides which sub-skills load together as one combined obligation
(never a partial subset), and owns package versioning (root `VERSION` +
`package_version` in manifest, every bump logged in `CHANGELOG.md`,
`scripts/check_versions.sh` keeps frontmatter/manifest in sync).

Key routes: pre-decision work goes out to `solution-search` (+`workplanx`) and
only re-enters past a green build gate; multi-session goals go to `mission`
first; repeat-until-green goes to `loop`; judging goes to `fresh-eyes`.

Sub-skills (rules live in each sibling folder, read before acting):

| Sub-skill | Ver | Scope |
|---|---|---|
| `code-quality` | 1.5.0 | Architecture (service separation, no god-files, real folder structure even for small scripts), no hardcoding (single config place, no hidden-config defaults), DRY/KISS, no pointless aliases/wrappers/single-use helpers, single-source contracts, typed domain payloads, honest async-only signatures, imports top-only with cost comments, no handwritten `isinstance` checks, fail-loud error handling (canonical definition: catch only with a real recovery action, no recatch-to-rethrow, no re-wrapping except mute-error/root-boundary, loud `NotImplementedError` stubs, validate-once-at-boundary), TDD for new code, baseline capture (`git stash` compare) before refactors, checks in order format → lint → typecheck → tests. Proactively flags security issues spotted mid-work, fixes nothing unasked. |
| `testing` | 1.2.0 | Proof beyond the default suite: green tests are a floor, not verification. Coverage for every change (or an explicit check script + statement of incompleteness), UX pass from the real user entry point through real service boundaries, regression vs baseline via stash-compare, environment-vs-code failure classification (never conflate, never assume "probably the environment"), fair A/B comparisons (one variable at a time, negative result must be possible). The UX pass is the artifact handed to a `fresh-eyes` judge. |
| `logging` | 1.2.1 | Base dependency, not a follow-up task: structured entries (labeled fields, one format across services, `structlog`-style default), one correlation ID generated at the entry point and carried through every service, fail-loud raises must also be *visible* (a raise dying in an unwatched container equals swallowing it), Telegram forum-topics alerts (`critical` / `info` / `service`, spammy-by-default). Never log secrets. |
| `security` | 1.0.0 | Ask-first in plain language for secrets/`.env`, logs, browser profile data, out-of-project files — explicit yes only, no provisional work while waiting, no routing around client permission prompts. No silent fallbacks for secrets (missing key = loud fail). Exposed credentials flagged with an all-caps line, every time. System boundaries: no host apps, no unbounded searches, no out-of-project touches unasked. |
| `process-tiers` | 1.1.1 | Calibrates ceremony: trivial edit → act; routine fix → act; small feature → one clarifying question or mini-design, wait for yes; big/architectural → plan file with bite-sized tasks, wait for approval. Weight of the quality/testing pipeline scales with tier (never downgrade to save effort). Delegation has two axes: main work (optional, ask user first, full context in prompt, shared-code location decided *before* parallel split) vs routine checks + `fresh-eyes` review (always automatic). On conflict or ambiguity: stop and ask one concrete yes/no with a proposed default. |
| `docker` | 1.1.0 | Never publish container ports (`ports:`) without an explicit same-message ask; internal-only networking by service name by default; existing ports are not precedent for new ones. Every compose variable in required form `${VAR:?message}` — unset values fail validation before start, never ride in as empty strings. |
| `git-workflow` | 1.0.0 | Work on `<type>/<what>` branches (ask before creating), Conventional Commits, always commit when done, merge only past checks + explicit approval. Never destructive ops or major dependency upgrades unasked. Every project keeps a current `.gitignore`. |
| `external-integrations` | 1.6.0 | Wiring-only for a *decided* integration (no `user-pick:` = no wiring, route back to search). Centralized retry for a narrow set (rate limits, transient network errors) in one root-level helper with config-driven params — everything else fails loud immediately. Code is the last resort: wired solution must sit at the decided ladder level. Docs-first (Telegram topics always from `references/telegram-topics.md` + current Bot API check, never from memory). Long-running services get an uptime-kuma heartbeat as the mandatory observability floor. One test-seam wrapper per project max, at the client boundary only. |
| `proxy-egress` | 1.0.0 | Mandatory outbound proxy with no silent direct fallbacks. Asks where the proxy service lives rather than hardcoding host/port/credential/path. One `PROXY_URL` in required form; rotation owned by the service; a `proxies.txt` only when a project genuinely needs several credentials. Per-client-library behavior matrix (httpx honors env, aiohttp ignores it, curl_cffi needs a dict, Telethon needs SOCKS5 plus `pysocks`/`python-socks` or it drops the argument with a warning, Go honors env until a custom `Transport` opts out). Fallback hunting with concrete grep patterns, and live verification from inside the container plus a failure-signature table. Treats the proxy service as a black box. |

### fresh-eyes (v1.0.0) — clean-context judge

A subagent that never saw the work reviews it. Two modes: `quality` (was it
done well — code checklist) vs `conformance` (was it done as decided —
requirement by requirement). Beautiful-but-wrong fails conformance;
right-but-sloppy fails quality.

- **Trigger:** non-trivial change finished and checks passed, before reporting
  done. Both modes when the task came from a plan. Never trivial edits.
- **Mechanics:** judge gets artifacts + verbatim reference file, never the
  author's narration. Reports only — never edits, never talks to the user.
  Main agent triages every finding (accept/reject with reason); only accepted
  findings reach the user.
- **Explicitly not:** a replacement for running checks, an oracle (clean review
  proves nothing except a second pair of eyes found nothing), or the phase gate.

### loop (v1.0.0) — bounded autonomous iteration

One condition, repeated iterations, fresh context each time, state on disk.
Covers iterate-until-green (tests, deploy, inference, build), bounded retry
with a hard cap, no-progress detection.

- **Trigger:** "keep going until X passes/works", "check your own work N
  times", unattended bounded runs. Not "retry this once" (that is an
  integration's centralized retry, not a loop).
- **Mechanics:** condition defined as a command whose exit code means done
  (no command = no loop — a self-judging loop is the failure mode). Verify
  command runs *before* the first iteration; one unit of work per iteration;
  after each unit: verify, append one ledger line to `loop.md`, run
  `scripts/loop_state.py` — `CONTINUE`/`STOP` is the verdict and is followed
  without a vote. Cap hit = reported failure, never resolved by relaxing the
  condition or moving goalposts.
- **Watch for:** editing the check instead of the thing; writing more code each
  pass while the failure stays identical (`references/stop-signals.md`).

### mission (v1.0.0) — goal → board of cards → subagents

For objectives too big for one pass ("build X", "migrate Y", "research Z
thoroughly", hours of unattended work). Supervisor decomposes and judges,
subagents execute.

- **Trigger:** multi-session goals. Not single tasks (that is `loop`), not
  what-to-build decisions (`solution-search` + `workplanx`), not one-shot
  research (`researcher`).
- **Mechanics:** goal must be statable as "true when…"; every card carries its
  own verifiable condition; board (`mission.md`) gets a `fresh-eyes`
  conformance pass *before* work starts; one subagent per card with the card
  only (never whole-board context); done only on evidence. Stacks with the
  scale ladder: `mission` owns *what* the units are, `loop` drives one card,
  `workplanx` gates start, `fresh-eyes` closes.
- **Fail loud:** open cards at stop = stopped run, never "mostly done"; cards
  never shrink their own conditions; systemic card failures mean re-cut the
  decomposition, not re-run.

### researcher (v1.3.0) — open-ended research

Surfaces recent or non-obvious findings on a topic — new releases, niche tools,
buried resources. Searches abstraction chains (topic → topic class → who else
solves it), not literal queries. Never compares pre-defined options and never
picks stacks.

- **Trigger:** explicit user request only ("find what's new on X"). Never
  self-triggers on knowledge gaps mid-task.
- **Mechanics:** three source classes checked at least once (Contentsphere /
  Artifacts-residue / Registries); primary sources over SEO rewrites; per-angle
  stop (2–3 reformulations, same results = exhausted) and overall stop (all
  classes checked, new angles yield nothing); think out loud every step;
  disagreements reported as disagreements; noise actively filtered (fewer good
  findings beat many mediocre ones); quoting limited to short exact phrases.
  Before the final report, asks the user what to exclude — filter once at the
  end, never during search.
- **Output:** flat finding list (what + link + why it matters), unverified gaps
  stated, never guessed. Pre-decision choices handed to `solution-search` as a
  one-line "what to decide + which verbs".
- **Self-improvement:** newly discovered *sources* (not findings) go to
  `references/source-log.md`, folded into `references/sources.md` once proven.

### skill-scaffolder (v1.0.0) — new-skill factory

Builds a new skill (or restructures a loose one) into this same layout:
`SKILL.md` + `references/` + `plugins/manifest.json` + `scripts/` +
`CHANGELOG.md` + `VERSION`. Structure follows content, `SKILL.md` written last
as a table of contents pointing outward (~500 lines = signal to split).

- **Trigger:** create-from-scratch, notes-to-skill, or reorganizing a flat
  skill. Never evals/benchmarks/description-optimization (that is a different
  skill's job).
- **Rules that matter:** split `references/` along natural seams; manifest from
  day one (`modules` = what's inside, `dependencies` = which sibling skills
  load alongside — never merged, never hand-listed in prose); instructions vs
  history (`CHANGELOG.md`) vs runtime logs (named file with a what-belongs-here
  header) live in three separate places; scale the layout down when the skill
  is small; validate the manifest before handoff; deliver as inspectable
  folder/zip (`.zip`, not `.skill`).

---

## Cross-skill contracts

- **Manifests, not prose.** `plugins/manifest.json` in each skill is the only
  place module lists and `dependencies` are written. If manifest and prose
  disagree, the manifest wins.
- **Files, not words.** Gates check folder shape (`plan_gate.py`), loops check
  exit codes (`loop_state.py`), judges check diffs. Claims without artifacts
  verify nothing.
- **Decisions cross one bridge.** `decision.md` + transcribed `user-pick:` is
  the single handoff from search to build. No pick, no code.
- **Reports stay in their lane.** Each skill reports its own verdict; review
  verdicts belong to `fresh-eyes`, never restated elsewhere.
- **Fail loud everywhere.** No swallowed errors, no silent fallbacks, no moved
  goalposts, no dressed-up partial results — at code level, loop level, and
  mission level alike.

---

## Layout

```
my_skills/
├── README.md
├── coding/                  dispatcher + 8 sub-skills + package CHANGELOG/VERSION
│   ├── code-quality/  docker/  external-integrations/  git-workflow/
│   ├── logging/  process-tiers/  security/  testing/
│   └── scripts/             check_versions.sh, run_checks.sh, ...
├── fresh-eyes/              references/{quality,conformance}.md
├── loop/                    references/{contract,stop-signals}.md + loop_state.py
├── mission/                 references/{decompose,board}.md
├── researcher/              references/{sources,patterns,source-log}.md
├── skill-scaffolder/        assets/templates + scripts/scaffold.py
├── solution-search/         references/method.md
└── workplanx/               references/layout.md + scripts/plan_gate.py
```

## Working with this repo

- Versions are per-skill (`VERSION` + frontmatter, independently bumped);
  `coding` additionally carries a package version bumped whenever any
  sub-skill's meaning changes. `plugins/manifest.json` plus `VERSION` are the
  authority; README version labels are descriptive and may lag.
- After editing any skill file, run that skill's validator
  (`validate_manifest.py`, `check_versions.sh`, `plan_gate.py`) and log the
  bump in its `CHANGELOG.md`.
- Prose never duplicates the manifest: add modules/references by editing
  `references/` + registering in `plugins/manifest.json`, not by rewriting
  `SKILL.md` lists.
