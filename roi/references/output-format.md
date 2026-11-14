# Verdict block format

One block per finding. Fields in this order; the example is illustrative —
compute, do not copy.

```
roi: HIGH 0.81
  stock: gate-pass (cold-model diff 0.31 < 0.6)
  lens: 2 — soul-bias #3 (obsession: venue structures), our crawl rail
  rot:  ~2 weeks (venue fees change), re-produce: 1 query — our moat
  act:  2 — Agensi seller URL + 70% split + Stripe rail
  cost: 2 — needs souls+browser stack
  verify: 4/4 URLs live
```

Field meanings:

- `roi:` verdict + numeric score (0.00–1.00). Verdicts: `HIGH` ≥ 0.75,
  `MED` 0.4–0.75, `LOW` 0–0.4, `UNVERIFIABLE` (×0), `STOCK` (gate fail).
- `stock:` `gate-pass (cold-model diff <d> < <t>)` — or `STOCK (cold-model
  diff <d> ≥ <t>)` when the gate fails.
- `lens:` 0–2 + the traced prism step (from a `prism:` annotation or
  reconstructed).
- `rot:` half-life + what rots; re-produce cost note.
- `act:` 0–2 + what exactly the buyer can do.
- `cost:` 0–2 + what stack re-production needs.
- `verify:` n/n URLs live, or `×0` with which claim is unverifiable.

Aggregate pass summary after all findings:

```
roi pass: N findings — n HIGH / n MED / n LOW / n STOCK / n UNVERIFIABLE
```

UNVERIFIED (gate could not run — never a pass):

```
roi: UNVERIFIED (stock gate did not run: <reason>)
  stock: UNVERIFIED — no cold-model control was recorded
  NO PASS. The finding stays unscored until a control run succeeds.
```

## stock_test.py exit-code contract

| Exit | Meaning |
|------|---------|
| 0 | Gate ran; finding is NOT stock (diff < threshold) — continue scoring. |
| 2 | Gate ran; finding IS stock — verdict `STOCK`, score 0, stop scoring. |
| 3 | UNVERIFIED — control config missing/invalid (no `ROI_CONTROL_MODEL`, endpoint or key missing, control == producer model, no producer prompt). |
| 4 | UNVERIFIED — control call failed or returned nothing usable. |
| 5 | Self-test failed (`--selftest` only). |
| 1 | Usage error. |

Every non-zero exit prints an all-caps `UNVERIFIED` (or `STOCK`) verdict
line plus the reason — a missing or failed control is loud by design and is
NEVER reported as a pass.
