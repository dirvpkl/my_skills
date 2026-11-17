---
name: handoff
description: Structured context handover between agents — one self-sufficient file so a fresh agent with zero chat history can continue. ALWAYS invoke when the owner says handoff or asks to export work for another session or agent. Collects from the inbox, topic folder, git log and the live session; absolute paths, owner words verbatim. NOT a recap for the owner (recap), NOT a value score (roi).
version: 1.4.0
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

## Additional sources beyond the context

The REAL base is the context the agent holds right now — the handoff file
absorbed and the live conversation. Beyond it sit additional sources,
extra info:

- **workplanx** — use it and ALL of its resources (topic folders, the
  owner-message inbox, the hashtag vocabulary — defined in workplanx's own
  docs, never restated here). Compare dates while reading: old records are
  stale, the newest ruling wins. Bind what you take to the current
  context: the records are durable and either agent can read them — their
  value here is what they mean for the task being handed over right now,
  not a copy of what they already say.
- **the harness DB** — the harness may compress sessions on its own; when
  session data matters, ask the harness directly — where its database is,
  what the schema is, what to read from it.

## Rules

- The handoff carries facts and decisions, not the writing agent's
  opinions — a take travels only if labeled (`#wildshot`).
- Never fill a `#slot` in a handoff; slots travel as slots.
- Chat stays for the conversation — the file is the record.

## References

- `references/handoff-form.md` — the fixed form and the verification
  checklist.
