# The six criteria

Weights: four criteria score 0–2 each and sum to /8; verifiability is a
multiplier (×0 or ×1); the stock test is a GATE, not a weight — fail it and
everything below never runs.

| # | Criterion | Kind | Range |
|---|-----------|------|-------|
| 1 | stock-test | GATE | pass / STOCK |
| 2 | lens-test | weight | 0–2 |
| 3 | staleness / half-life | weight | 0–2 |
| 4 | actionability | weight | 0–2 |
| 5 | production cost (inverted) | weight | 0–2 |
| 6 | verifiability | multiplier | ×0 / ×1 |

## 1. stock-test — GATE, not weight

Ask a COLD model (different provider/session than the producing one, no
conversation history) the same prompt that produced the finding. If the cold
model's output contains the same finding (fuzzy-diff ≥ threshold, default
0.6) → the finding is stock → final score 0, nothing else runs. Owner ruling
2026-11-12: a stock answer — the kind any LLM would give — does not qualify.

Control arms, in order of availability: a cold-model API call
(`scripts/stock_test.py`), a fresh subagent with no shared context, or a
self-reflection pass — the mechanism is not hard-restricted, the model does
the thinking either way (owner ruling 2026-11-14). Always run the control on
the finding's ORIGINAL formulation: a prompt re-written to lead the control
toward the finding proves nothing. With `scripts/stock_test.py` (see
`output-format.md` for exit codes). Fails the gate = verdict `STOCK`, done.

## 2. lens-test (0–2)

Trace the finding to a prism step: which personality bias, skill method, or
own-pipeline hop produced it (e.g. "soul-bias #3 — cannot scroll past a
marketplace").

- 0 — no traceable step; the prism could have been anyone.
- 1 — traceable but generic (a step many prisms share).
- 2 — traceable and the step is uniquely ours (our bias, our rail, our graph).

At production time, attach an optional `prism:` annotation (souls log bias
ids; skills log method steps) — the scorer accepts it; otherwise reconstruct
from context.

## 3. staleness / half-life (0–2)

Estimate decay of the finding's value.

- 2 — venue lists, prices, fee schedules: rot in weeks, AND/OR only we can
  cheaply re-produce it when it rots (the moat is the fresh machine
  inventory).
- 1 — methods and maps: rot in months-years.
- 0 — math/history/evergreen: never rot, which is worth LESS to sell (an
  evergreen fact is also in every static training set).

## 4. actionability (0–2)

- 2 — the buyer can act in <10 minutes with what is in the finding: exact
  URL, rail, price, form.
- 1 — category-level pointer ("check marketplace X for Y").
- 0 — vibes.

## 5. production cost (0–2, inverted)

Effort to RE-produce — this is the "effort" half of roi:

- 2 — would need our exact stack (souls, graphs, crawl years).
- 1 — hours + special access.
- 0 — one query, minutes.

## 6. verifiability — weight multiplier (×0 if absent)

Every factual claim carries a URL or probe result. Probe each URL (HEAD or
fetch). One unverifiable claim → ×0 regardless of the rest → verdict
`UNVERIFIABLE`.

## Formula

```
if stock-test fails:          verdict = STOCK (score 0)
score = (lens + staleness + actionability + cost) / 8 * verifiability
verdict:  0.75+ HIGH   0.4–0.75 MED   0–0.4 LOW   ×0 UNVERIFIABLE
```

## Run algorithm

1. Input: list of findings (text + evidence URLs each).
2. For each: run the stock test — one cold-model call, provider OTHER than
   the producing one; fuzzy-diff (token overlap or cosine ≥ 0.6 on the core
   claim).
3. Gate fail → `STOCK` verdict, skip steps 4–6.
4. Lens-trace: accept a `prism:` annotation attached at production time;
   else reconstruct from context.
5. Half-life / actionability / cost: LLM-judged against the rubric above —
   the producing model is fine here (they are judgments, not controls; the
   control arm is where a different model is mandatory).
6. Verifiability: probe every URL (HEAD/fetch).
7. Emit blocks (`output-format.md`); aggregate pass summary (n HIGH / MED /
   LOW / STOCK).

## Config

Config lives in the collection's `runtime.toml` (`[omniroute]` section) —
base rule: machine facts resolve there, never from the owner's memory
(owner ruling 2026-11-14). Resolve at run time, in order:

1. `runtime.toml` `[omniroute]` — `url` (OpenAI-compatible router root)
   and `api_key` are already recorded there; the control model is ANY
   omniroute chat model DIFFERENT from the producer's (probe `/v1/models`
   at run time; do not reuse the producer's id or the `skill` alias if
   that is what produced the finding).
2. Env overrides when present: `ROI_CONTROL_MODEL`,
   `ROI_CONTROL_BASE_URL`, `ROI_CONTROL_API_KEY`,
   `ROI_CONTROL_TIMEOUT` (seconds, default 120).
3. `ROI_PRODUCER_MODEL` — optional; if it equals the control model the
   gate refuses (same-model control is invalid).
4. Anything still missing → loud `UNVERIFIED`, never a fake pass; keys
   never logged, never printed.

Known limitation: a producer prompt that leans on conversation context
("про то, что мы обсуждали") travels badly to a cold model — the diff then
measures a degraded prompt, note that in the verdict rather than re-running
with a rewritten prompt.
