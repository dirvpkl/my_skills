# Changelog

## [1.1.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- Per-skill review round: examples brought to two pairs per case;
  description unchanged (already passes the lint contract).

## [1.0.0] - 2026-11-14
- First release, built from the handoff spec
  (`Desktop/ampm/.workplanx/11-12-crosslist-analogs/roi-skill-spec.md`,
  owner idea 2026-11-12, criteria resolved by the ampm-session agent 2026-11-14).
- Stock gate as a HARD rule: the same producer prompt goes verbatim to a cold
  control model (`ROI_CONTROL_MODEL`, different provider); fuzzy-diff
  (token overlap / cosine) ≥ 0.6 on the core claim → verdict STOCK, score 0.
  Unset/failed control is a loud UNVERIFIED, never a fake pass.
- `scripts/stock_test.py` — the gate: stdlib only, runs with `python -I`,
  1 control call per finding, `--selftest` offline assertions, JSON mode,
  exit-code contract in references/output-format.md.
- `references/criteria.md` — six criteria with weights and rubric
  (lens / staleness / actionability / cost / verifiability ×0), run
  algorithm, config.
- `references/output-format.md` — verdict block per finding + aggregate
  pass summary.
- Personal until the first real scoring run; then OSS-ify the method only —
  no session cases, no personal prism examples.

## 1.0.1 - 2026-11-14
- Stock-gate softened per owner ruling: control arm is not hard-wired to an
  external API — cold-model call, fresh subagent, or self-reflection pass all
  qualify; control always runs on the finding's ORIGINAL formulation (never a
  leading rewrite). `thinking` added to dependencies (roi closes out the think-first pass
  and forced-serendipity sessions).
