# Changelog

## [1.3.1] - 2026-11-17
- examples.md: every case now carries >=2 Good/Bad pairs (the collection convention) — one teaching couplet added per single-pair section.

## [1.3.0] - 2026-11-17
- Descriptions trimmed to ~400 chars across the collection (the listing cost: 12k -> ~8k chars).
- `## Trigger` section removed; the trivial-edit exemption moved into "What
  the judge is for".
- Judge input now names the parent's loaded skills + read access to the
  workplanx topic folder (owner directive).
- references/examples.md added (the skill had none).

## [1.2.2] - 2026-11-12
- validate_manifest.py: missing-runtime.toml diagnostic and non-table [skills] guard


## [1.2.1] - 2026-11-12
- validate_manifest.py: dependencies_runtime resolution and module type check


## [1.2.0] - 2026-11-11
- Trigger contract sweep: description rewritten as a use-when / not-for / sibling contract with literal user phrases; rules and body unchanged.

## [1.1.0] - 2026-11-08
- directive description: imperative trigger + negative constraint (trigger reliability sweep)


## [1.0.1] - 2026-10-19
- Judge dispatch wording: prefer agents over subagents


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
