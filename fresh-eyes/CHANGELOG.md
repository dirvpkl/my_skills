# Changelog

## 1.0.0 — 2026-09-26
Split out of three places that each described the same procedure.
- New skill with two modes: `quality` (was the work done well) and
  `conformance` (was it done to the plan). The second mode is new — scope drift
  and unverified "done" claims had no owner.
- `references/quality.md` is the eight-point checklist moved verbatim from
  `coding/code-quality/references/fresh-eyes-checklist.md`; that file is deleted
  and `code-quality` points here instead.
- `references/conformance.md` is new: requirement coverage, decision fidelity,
  scope creep, parked work, verification honesty, non-goals.
- Subagent-triage canon moved here from `workplanx` step 5 — the judge reports,
  the main agent accepts/rejects each finding with a one-line reason, only
  accepted findings reach the user.

All notable changes to this skill itself are logged here — not runtime data
(that lives in `workplanx` topic folders).
