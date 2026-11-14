---
name: handoff
description: Structured context handover between agents — writes a self-sufficient handoff file so a FRESH agent (new session, zero chat history) can continue the work without the conversation. ALWAYS invoke when the owner says «хендофф», «выгрузка для другого агента», «сводка для агента», «передай другому агенту», "handoff", or when handing a task to another session. Complements /compact (which summarizes for the SAME session) — a handoff serves a DIFFERENT agent. NOT a project recap for the owner (recap) and NOT a value score (roi). Owner phrasings also trigger — «хэндоф», «выжимка для передачи другому агенту», «записка для другого агента», «briefing для следующего агента», «я другому агенту пихну», «я создам с новым агентом чат», «спека для другого агента».
version: 1.0.0
---

# handoff — context handover between agents

The next agent does not inherit this conversation. A handoff is the
bridge: one file that carries everything the fresh agent needs to continue
without asking the owner to re-explain.

Owner phrasings that summon this file: «я другому агенту пихну», «я создам с
новым агентом чат», «запиши все-все-все» — all three mean this handoff file.

## Hard rule — self-sufficiency

A handoff the fresh agent cannot start from alone is a failed handoff.
Before delivering, reread the file AS the zero-context agent: every
reference resolvable, every term defined, every path absolute, no "as we
discussed". Fix gaps before handing over.

## Process

1. **Collect.** Three sources, in order: the topic folder
   (`<project>/.workplanx/*/log.md`, `decision.md` — decisions and owner
   verdicts verbatim), git log (commits, artifact paths), and the current
   session (what is in flight that no file records yet).
2. **Write** the handoff file — the fixed form in
   `references/handoff-form.md` — to the topic folder, or to the path the
   owner names. Absolute paths only; owner words quoted verbatim, not
   paraphrased.
3. **Verify.** Reread as the zero-context agent (the self-sufficiency
   rule). Name in the last line which agent/session the handoff targets,
   if the owner said.

## Rules

- The handoff carries facts and decisions, not the writing agent's
  opinions — a take travels only if labeled (`#wildshot`).
- Never fill a `#slot` in a handoff; slots travel as slots.
- Chat stays for the conversation — the file is the record.

## References

- `references/handoff-form.md` — the fixed form and the verification
  checklist.
