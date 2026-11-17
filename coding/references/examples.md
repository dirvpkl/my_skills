# coding — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## The whole set, not a partial subset

**Good:** a code-writing task loads `git-workflow` + `boundaries` + `process-tiers` + `code-quality` + `logging` + `testing` (+ `docker` when compose is touched) as one combined obligation — weight scales per process-tiers, presence does not.
**Bad:** loading `code-quality` and calling the rest "not relevant to this small change."
Rationale: the set is one obligation, not a menu — every skipped member is a rule that silently stops applying, which is how logging and egress guarantees rot.

**Good:** the wiring task for a decided integration adds `external-integrations` alongside the base set.
**Bad:** reimplementing retry/heartbeat logic inline "since it's just a few lines."
Rationale: the wiring rules (retry, topics, heartbeat) live in one skill on purpose — an inline copy is a drift bug waiting for the first change.

## Route out, don't search in place

**Good:** "how should we build X?" → the pre-decision question routes to `mindstorm` + `workplanx`; this package loads only after the `build` gate passes on a transcribed `user-pick:`.
**Bad:** picking a stack inline and starting to code "since the answer is obvious."
Rationale: searching inside coding is a routing violation — the gate is the single enforcement point for no-implementation-before-the-pick, and it lives outside this package.

**Good:** a goal too big for one pass ("migrate the whole service") routes to `mission` first.
**Bad:** attacking a multi-session goal by loading this package and hoping.
Rationale: this package is what ONE card's implementation loads — decomposition is mission's job, and a card that needs repetition hands off to `loop`.
