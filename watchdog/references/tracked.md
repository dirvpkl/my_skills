# tracked.md — WHAT BELONGS HERE

Live registry of supervised worker sessions. Each row: session ID, project
directory, what the session owes (one line), its natural cadence (how long
one unit of work takes). Rows are added when work is dispatched and REMOVED
only after the verdict is delivered — never to hide a stall.

Stalled sessions keep their rows until they deliver or are explicitly retired
by the user. History of past ticks lives in the tick log, not here.

| session | directory | owes | cadence |
|---|---|---|---|
| ses_ee437563cffeq71upLokZJZ34A | C:\Users\orlando\Desktop\fzz | ttm.sh/envs.sh sickness: cause + fix + commit/push/redeploy | ~15 min |
| ses_ee4375496ffd5Xgic0FXg5P0L0 | C:\Users\orlando\Desktop\tppr | dead-pool loop verdict (dead <20% or honest FAIL) | ~15 min |
| ses_ee437562dffemSkrBXjqd1pVYI | C:\Users\orlando\Desktop\ggfr | scheduled n8n fetch 200 (pool-dependent) | ~30 min |
| ses_ee4375484ffeXvrmheRU3xyhXu | C:\Users\orlando\Desktop\DINA_SAS | idle unless tasked | — |
| ses_ee437538bffdfvyisEkLCNVw5C | C:\Users\orlando\Desktop\gws | idle unless tasked | — |
| ses_ee4375496ffePNsl24zTJPJYQ5 | C:\Users\orlando\Desktop\strfk | idle unless tasked | — |
| ses_ee4375485ffe5SmGKPASZFCx8b | C:\Users\orlando\Desktop\mscyaf | idle unless tasked | — |
| ses_ee437538affetLoCP83Vr0tua6 | C:\Users\orlando\Desktop\sdstrs | retired by user 2026-10-11 (push blocked: no remote; frozen) | — |
| ses_ee437538bffeNjbFU2XNNoKKRp | C:\Users\orlando\Desktop\vbcdxl | frozen by user | — |
| ses_ee4375486ffeWnwLrdWt5HjQRj | C:\Users\orlando\Desktop\vbcdpr | frozen by user | — |
| ses_ee4378436ffezwI02P9cVbsoiu | C:\Users\orlando\Desktop\ampm | frozen by user (3 branches await merge) | — |
| ses_ee437536fffejB9lx5gpWE77sc | C:\Users\orlando\Desktop\thewarmertg | done (merged+pushed+redeployed) — retire after verify | — |

Tick log: each tick appends one line per session to the orchestrator's run
log (or `ticks.md` next to this file when running standalone).
