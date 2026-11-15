---
name: handoff
description: Structured context handover between agents — writes a self-sufficient handoff file so a FRESH agent (new session, zero chat history) can continue the work without the conversation. ALWAYS invoke when the owner says "handoff", or in any phrasing for handing a task to another session (export for another agent, a summary or spec for another agent). Complements /compact (which summarizes for the SAME session) — a handoff serves a DIFFERENT agent. NOT a project recap for the owner (recap) and NOT a value score (roi).
version: 1.1.0
---

# handoff — context handover between agents

The next agent does not inherit this conversation. A handoff is the
bridge: one file that carries everything the fresh agent needs to continue
without asking the owner to re-explain.

## Hard rule — self-sufficiency

A handoff the fresh agent cannot start from alone is a failed handoff.
Before delivering, reread the file AS the zero-context agent: every
reference resolvable, every term defined, every path absolute, no "as we
discussed". Fix gaps before handing over.

## Process

1. **Collect.** Four sources, in order: the owner-message inbox
   (`<project>/.workplanx/_inbox/<date>.md` — the owner's words verbatim,
   the rawest record of what was said), the topic folder
   (`<project>/.workplanx/*/log.md`, `decision.md`), git log (commits,
   artifact paths), and the current session (what is in flight that no
   file records yet).
2. **Write** the handoff file — the fixed form in
   `references/handoff-form.md` — to the topic folder, or to the path the
   owner names. Absolute paths only; owner words quoted verbatim, not
   paraphrased.
3. **Verify.** Reread as the zero-context agent (the self-sufficiency
   rule). Name in the last line which agent/session the handoff targets,
   if the owner said.

## Receiving a handoff

When the owner points at an existing handoff ("check the handoff",
"continue from the handoff"), the flow is read-first: read the file
whole, absorb it as the working context, and run the verification
checklist against it. A gap found on the receiving side — a dead path,
an unresolvable reference, a missing decision — is reported to the owner,
not silently patched. Then continue the work the handoff describes. The
file stays the record: what happens next lands in the topic folder, never
back into the handoff file itself.

## Rules

- The handoff carries facts and decisions, not the writing agent's
  opinions — a take travels only if labeled (`#wildshot`).
- Never fill a `#slot` in a handoff; slots travel as slots.
- Chat stays for the conversation — the file is the record.

## References

- `references/handoff-form.md` — the fixed form and the verification
  checklist.
