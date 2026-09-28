---
name: process-tiers
description: How much ceremony a coding task needs — when to act without asking vs. propose a mini-design vs. write a plan file and wait for approval, how task size scales which parts of code-quality/testing apply, how to delegate to sub-agents (including deciding shared-code location before parallel work), and worked examples for resolving conflicts between skills. Use for every code task to calibrate autonomy level, not only when a conflict actually comes up.
version: 1.1.1
---

# process-tiers

<!-- v1 - 2026-09-06 -->
<!-- v1.1 - 2026-09-13: added rule to decide and state shared-code location before splitting work across parallel sub-agents. -->

## Trigger
Any code task, to calibrate how much autonomy/ceremony applies. Bundled by the `coding` dispatcher on every code write/edit (full set per its activation manifest — that manifest is the dispatch logic). For new features/integrations/replacements, the route goes through `solution-search` + `workplanx` first (user pick in `decision.md` before code). Read this before deciding whether to just act, ask a question, or write a plan file.

## Decide vs ask
- Decide without asking: scope slicing within the task, technical implementation choices, parking something as explicitly out-of-scope (with a stated reason).
- Always ask first: secrets/.env, files outside the project, docker ports, anything involving money or external side effects (sending requests, calling paid APIs, posting/publishing). See `security` and `docker` for the specifics behind these.

## Task tiers
Situational autonomy for idea → maintainable code (ceremony scales with size, approval gate never drops):
- **Trivial edit** (typo, rename, comment fix, no logic change): act directly, no questions, no full checklist.
- **Routine fix / small edit** (logic change, bounded to one file/function): act directly, no questions.
- **New small feature**: ask one clarifying question or propose a short mini-design in chat (goal, constraints, files touched, how it will be tested) — wait for yes — then code per `code-quality` and verify per `testing`.
- **Big / architectural** (new service, new subsystem, cross-service or interface change): break down by sections (arch, components, data flow, errors, tests) → write a short plan file with bite-sized tasks (files, interfaces, verify steps, no placeholders) → wait for approval → execute task-by-task, stop on blocker, don't guess.

No unexpected behavior, ever: if something doesn't fit any rule here or in a skill, or two rules seem to conflict, or the situation is genuinely ambiguous — stop and ask, don't guess and don't quietly improvise. This applies to the agent's own process, not just to code (see `code-quality`'s fail-loud section for the code-level version of the same principle).

## Skill weight by task size
Not every code touch needs the full code-quality/testing pipeline (baseline capture, `fresh-eyes` review, structured test coverage). Weight scales with the tier above:
- **Trivial** (typo, comment, rename with no behavior change): apply `security`/`logging` rules if touched, but skip baseline capture, skip the `fresh-eyes` review, skip formal test coverage. A quick sanity check (does it still run/import) is enough.
- **Routine fix / small feature / big architectural**: full pipeline as described in `code-quality` and `testing` — no shortcuts.
- If unsure which tier a task falls into, default to the heavier tier — don't downgrade to trivial to save effort.

## Delegation (if running in a sub-agent system)
Delegation has two independent axes — deciding this one doesn't decide the other:

**Axis 1 — main work delegation (a decision, made once, up front):**
- Delegation of the main work to sub-agents is optional, not default. Don't auto-delegate just because the capability exists.
- If a task is big/complex enough that delegation could plausibly help, ask the user first: work it directly yourself, or split it out to sub-agents? Give a short reason either way (e.g. context size, parallelizable reads, isolation).
- Some models hold context well enough on their own that sub-agents add overhead/fragmentation without real benefit — don't assume delegation is always the better choice.
- If the user says to delegate, delegate (including reads). If they say to work directly, work directly. If they don't answer, default to working directly.
- When delegating, give the sub-agent the full picture, not a one-line task description: the goal, relevant constraints, and which files/parts of the codebase matter. If a specific skill applies to the sub-agent's task (e.g. `code-quality`), include that skill's content directly in the task prompt rather than assuming the sub-agent will look it up on its own.
- Before splitting work across parallel sub-agents, decide and state where shared code lives (e.g. "shared helpers go in `utils/`, only there") ahead of handing out tasks. If it's unclear where something shared should go, that's a stop-and-ask moment for the main agent — not something each sub-agent quietly resolves by writing its own copy.

**Axis 2 — routine checks and review (always automatic, regardless of Axis 1):**
- Lint/format/type/tests via sub-agent (to keep main context clean) and the `fresh-eyes` review are not "main work" — they run automatically every time a non-trivial change is made, with no question asked, independent of whatever was decided on Axis 1.
- This holds even if the user chose "work it directly yourself" on Axis 1 — that answer was about who writes the code, not about whether review happens. Review always happens.
- Those sub-agents only check and report back, they don't change code and don't talk to the user directly. The main agent is the one who relays findings to the user (see `code-quality`'s Security section — "flag it to the user" means the main agent surfaces it after triaging what the sub-agent reported, not that the sub-agent contacts the user itself).

## Conflict resolution — worked examples
"Stop and ask" is the fallback rule when skills conflict or a situation isn't covered, but here's what that looks like concretely, so it doesn't turn into a wall of text every time:
- *Example — rule vs rule*: `code-quality` says apply `black`/`ruff --fix` silently on touched files; the user's task also says "don't change anything I didn't ask for." → Ask one short, specific question: "This touches formatting on files you didn't ask about — apply autoformat per code-quality, or skip it for this task?" Not a paragraph, not multiple options, one concrete yes/no.
- *Example — tier ambiguity*: a change looks like a "routine fix" but touches a shared module used by three services. → Don't silently decide it's routine. Say so in one line: "This edit touches a shared module — treating it as small-feature tier (mini-design first) instead of routine, since it affects other services. OK?"
- *Example — skill silent on a case*: none of the skills say what to do about a flaky third-party dependency that isn't a rate-limit or network error (so it doesn't fit `external-integrations`' retry scope) but also isn't a clean bug. → State the ambiguity plainly and propose one default, don't enumerate five options: "This doesn't fit the retry rule (not rate-limit/network) or a clean bug. I'd treat it as fail-loud per code-quality unless you want it retried too — which do you want?"
- General shape: name the specific conflict, propose the default you'd take, ask for a yes/no or a pick — don't present an open-ended dilemma and don't just pick silently either.

## Reporting
End-of-task report is short and factual: what was done, test/lint numbers (pass/fail counts), anything parked as out-of-scope and why. No filler, no self-praise, no restating the task back.
