---
name: recap
description: Project recap collector — rebuild the project's story from its records, not from chat memory: a full pass over .workplanx (log, decision, plan, afterword), a hashtag layer, git log and the memory index, in the fixed form. ALWAYS invoke on any recap or retell request, including 'from moment X'. Read-only: summarizes, never edits, never fills gaps. NOT for live status of one task (its own log), NOT for handing work to another agent (handoff).
version: 1.1.0
---

# recap

The project's memory is on disk, not in chat. A recap is a rebuild from
records — the answer is only as good as the collection pass.


## Process

1. **Collect.** Four sources, in order:
   - Full topic pass — read EVERY file of `<project>/.workplanx/*/`
     (log.md, decision.md, plan.md, search.md, afterword.md): the recap
     retells the whole project and the whole workplanx, not a highlight
     reel. "From moment X" filters by the dates in the files.
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

- Not for the live status of one active task — that's the topic's own
  `log.md`. A recap rebuilds the project's story from the records.

- Read-only: a recap never edits project files and never relabels a
  `#wildshot` into a recommendation.
- Every line carries its source. A recap line without a trace is a guess,
  and guesses don't ship.
- Empty sections are data: "Asked-not-done — none found" is an answer,
  not an omission.
