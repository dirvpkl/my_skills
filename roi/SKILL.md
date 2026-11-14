---
name: roi
description: Value-scoring for the agent's own findings — is this finding actually valuable, or would any cold LLM have said the same thing (the stock question)? ALWAYS invoke when the owner asks to price a find ("оцени ценность находки", "сколько стоит эта находка", "roi этих находок", bare "roi"), before publishing or selling anything derived from findings ("стоит ли это продавать"), or asks whether a find is stock ("это сток?", "любой бы это нашёл?") — the cold-model stock gate is this skill's hard core and runs before any scoring. Findings are scored and annotated append-only, never deleted or edited. NOT for reviewing finished work (fresh-eyes), NOT for ideation takes and opinions (spine), NOT for finding things (researcher finds; roi prices what was found). Owner phrasings also trigger — «приводи ценность к находкам».
version: 1.0.0
---

# roi — value-scoring for findings

Value = unique to the prism (personality, method, own pipeline) × actionable
× fresh, divided by the cost to re-produce. The question underneath every
score: would a cold model — different provider, no conversation history —
have said the same thing?

## The stock gate (hard rule)

Before ANY scoring, the finding goes through the stock test
(`scripts/stock_test.py`): the same prompt that produced the finding goes
verbatim to a COLD control model — a model DIFFERENT from the producing
one, resolved from the collection's `runtime.toml` `[omniroute]` section
(env overrides win; owner ruling 2026-11-14: the config is already
recorded there, never ask the owner for it). If the control's answer
contains the same finding (fuzzy-diff ≥ 0.6 on the core claim), the
finding is stock → verdict `STOCK`, final score 0, nothing else
runs.

- The control arm is not hard-wired to an external API: a cold-model call,
  a fresh subagent, or a self-reflection pass all qualify — the model does
  the thinking either way (owner ruling 2026-11-14: don't hard-restrict the
  mechanism).
- The owner's own formulation of the stock question: «сток ответ, какой бы
  дал любой ллм» — same test, same gate.
- Run the control on the finding's ORIGINAL formulation — never a re-written
  leading version; a prompt engineered to produce the finding proves nothing.
- No control config, a failed control call, or a missing producer prompt is
  a loud `UNVERIFIED` verdict — never a fake pass, never a guessed result.
- Cap: 1 control call per finding. Control calls cost tokens.
- The gate never deletes findings; it annotates (append-only).

## Formula

```
if stock-test fails:          verdict = STOCK (score 0)
score = (lens + staleness + actionability + cost) / 8 * verifiability
verdict:  0.75+ HIGH   0.4–0.75 MED   0–0.4 LOW   ×0 UNVERIFIABLE
```

## Running it

1. Input: the findings (text + evidence URLs each) and the producer prompt
   that produced them.
2. Per finding: run the stock gate (exit codes in
   `references/output-format.md`), then judge the four 0–2 criteria against
   the rubric in `references/criteria.md`.
3. Verifiability: probe every URL the finding cites; any unverifiable
   factual claim → ×0 regardless of the rest.
4. Emit one verdict block per finding (format: `references/output-format.md`),
   then the aggregate pass summary (n HIGH / MED / LOW / STOCK).

## References

- `references/criteria.md` — the six criteria with weights and rubric, the
  run algorithm, and config (`ROI_CONTROL_MODEL` and friends).
- `references/output-format.md` — the verdict block format, the aggregate
  summary, and `stock_test.py`'s exit-code contract.
- `scripts/stock_test.py` — the stock gate; stdlib only, runs with
  `python -I` (no pip installs).

## Constraints

- Append-only: the skill scores and annotates findings, never deletes or
  edits them.
- Personal until the first real scoring run; then OSS-ify the METHOD only —
  no session cases, no personal prism examples in the shipped skill.
