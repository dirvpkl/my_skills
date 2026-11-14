---
name: recap
description: Project recap collector — when the owner asks «перескажи проект», «что я откладывал», «что мы обсуждали», «перескажи с момента X» (X = a date, topic, or phase), or "recap", rebuild the project's story from its records, not from chat memory — an rg hashtag pass over <project>\.workplanx\*\ (log.md, decision.md, afterword.md) plus git log plus the agent's memory index, reported in the fixed form from references/recap-form.md. Read-only — it summarizes, never edits, never fills gaps itself. Use this skill first on any recap request; do not answer from chat memory alone, and never present a guess as a fact. Owner phrasings also trigger — «пересказать все-все», «сделай общий саммари», «напомни весь диалог», «что я просил напомнить», «что мы тут делали», «что мы тут с тобой обсуждали».
---

# recap

The project's memory is on disk, not in chat. A recap is a rebuild from
records — the answer is only as good as the collection pass.

## Trigger

Owner asks to retell the project: «перескажи проект», «что я откладывал»,
«что мы обсуждали», «перескажи с момента X», "recap". «С момента X» scopes
the pass: only topics and records dated after X. Not for live status of
one active task — that is the topic's own log.md.
Also fires: «что мы тут делали», «что мы тут с тобой обсуждали» — same
retell-the-record request.

## Process

1. **Collect.** Four sources, in order:
   - Full topic pass — read EVERY file of `<project>/.workplanx/*/`
     (log.md, decision.md, plan.md, search.md, afterword.md): the recap
     retells the whole project and the whole workplanx, not a highlight
     reel. «С момента X» filters by the dates in the files.
   - Hashtag layer — `rg -n "#gem|#wildshot|#slot|#harvest|#open|#decision"`
     over the same folders: hashtags are only the explicitly-must-not-forget
     markers, surfaced on top of the full pass (meanings: workplanx
     `references/layout.md`).
   - `git log` — dates, commits, artifact paths the folder files miss.
   - The agent's memory index — stances and takes from past sessions the
     files don't carry.
   - The live chat thread — everything this session said that no file
     carries yet; include it, flagged as unrecorded (as the recap runs,
     that state lands in the topic folder).
   No topic folders → say so and fall back to git log + memory index +
   the chat thread; a recap from files alone misses what the session just
   decided.
2. **Assemble.** Fill the fixed form — `references/recap-form.md` —
   section by section, each line traceable to a source (file + date, or
   commit). Verbatim means verbatim: verdicts and parked asks quote the
   owner's words, not the agent's summary of them.
3. **Report.** Anything the record does not show stays out — a gap is
   reported as a gap (the section names it or reads "none found"), never
   filled by inference.

## Rules

- Read-only: a recap never edits project files and never relabels a
  `#wildshot` into a recommendation.
- Every line carries its source. A recap line without a trace is a guess,
  and guesses don't ship.
- Empty sections are data: "Asked-not-done — none found" is an answer,
  not an omission.
