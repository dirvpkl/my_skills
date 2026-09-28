---
name: fresh-eyes
description: Clean-context judging of finished work by a subagent that never saw how it was written — two modes: `quality` (was the work done well, against the code checklist) and `conformance` (was it done to the plan, requirement by requirement). Use after code + checks pass, before reporting done, and whenever a claim of "works" / "done" needs independent backing. Reports only — never fixes, never talks to the user.
version: 1.0.0
---

# fresh-eyes

One job: a judge with clean context looks at finished work and reports what it
finds. The judge never saw the reasoning behind the work, so it cannot be
swayed by it — that is the entire point. This skill is the only place that
procedure lives; other skills point here, none of them restate it.

- **references/quality.md** — mode `quality`: the code checklist, verbatim,
  to hand to the judge.
- **references/conformance.md** — mode `conformance`: plan-to-diff checking.
- **plugins/manifest.json** — active modules, check it.

## Trigger

- A non-trivial change is finished and checks passed, before it's reported as
  done. Both modes; see "Pick the mode" below.
- Any time something is about to be claimed as working, complete, or
  plan-conformant and that claim hasn't been checked by something that didn't
  do the work.
- Never on a trivial edit (typo, rename, comment) — there is nothing to judge.

## Pick the mode

| question | mode |
|---|---|
| "was this done *well*?" — quality of the change itself | `quality` |
| "was this done *as asked*?" — did the change match what was decided | `conformance` |

They're different questions and they fail differently. Work that is beautiful
and does the wrong thing fails `conformance`. Work that does exactly the right
thing badly fails `quality`. When the task came from a plan file or a
`decision.md`, run **both** — the second one is the one people skip and the one
that catches scope drift.

## Process

1. Assemble the judge's input: the diff or the result, plus the topic folder
   if there is one (`workplanx`). The judge gets artifacts, never your
   narration of how you did it.
2. Pick the mode (or both) and hand over the matching reference file's
   contents **verbatim** — don't summarize it, don't pre-empt findings.
3. Dispatch a subagent with clean context. It reports back; it does not edit
   files, and it does not talk to the user.
4. **Triage every finding yourself.** A subagent can send back nonsense. Check
   each one against what the user actually asked for and whether the technical
   claim is sound. Mark each `accept` or `reject` with a one-line reason.
5. Only accepted findings reach the user, in the final report. Rejected ones
   are dropped silently — a rejected finding is noise, not a result.

## What the judge is for (and what it's not for)

- It is **not** a replacement for running the checks. `testing` runs them;
  `fresh-eyes` looks at the result of them.
- It is **not** an oracle. A clean review does not prove the work is right —
  it only proves a second pair of eyes found nothing. Say it that way.
- It is **not** the phase gate. Whether the task was allowed to start at all
  is `workplanx`'s `plan_gate.py`. This skill never re-litigates that.

## Report

Accepted findings with their accept/reject reasoning stated plainly. If the
review came back clean, say "clean review" — don't dress silence up as
verification, and don't imply the checks were re-run.
