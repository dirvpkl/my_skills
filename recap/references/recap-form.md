# Recap form

Fixed output form for a recap. Exactly these sections, in this order, no
others. Each line traces to a source (topic file + date, or git commit).
An empty section is written out as "none found" — it's an answer, not an
omission.

Sections are collected from the hashtag pass (`rg` over
`<project>/.workplanx/*/log.md|decision.md|afterword.md`), git log, and
the agent's memory index; hashtag vocabulary (`#gem` `#wildshot` `#slot`
`#harvest` `#open` `#decision`) lives in workplanx `references/layout.md`.

## Done
Completed units of work, each with its artifact path (file or folder).
From log.md entries, afterword.md, git log. Pick one ordering (newest
first, or per topic) and keep it consistent through the recap.

## Asked-not-done
Owner asked, agent did not do. Source: owner-voice lines in log.md, `#open`
hits that are requests, memory index. One line each; include why it never
happened if the record says.

## Parked by owner
Owner explicitly deferred ("do it later" and the like). Verbatim quote +
date. Parked is not forgotten — listing it lets the owner revive it.

## Verdicts (verbatim)
Owner rulings that decided something: `#decision` hits and `user-pick:`
lines, quoted verbatim with date and the topic they ruled on. Never
paraphrase a verdict.

## Open questions
`#open` hits plus any question the record shows is still with the owner.
One line each: question, where asked, date.

## Gems
`#gem` hits — unique finds that passed the stock test. One line each with
the topic they came from.

## Wild-shots (labeled)
`#wildshot` hits, kept labeled — intuition, not evidence. One line each:
take, topic, date. The label survives the recap; a wild-shot is never
restated as a recommendation.

## Harvest/rules
`#harvest` hits and afterword `harvest:` blocks — skill patches born in
the passes, each naming the rule and the target skill. Include applied /
awaiting-owner state when the record shows it.

## Slots (unfilled lost fragments)
`#slot` hits — fragments the owner left and hasn't recalled yet. Listed
as-is, unfilled; the agent never fills a slot in — not in the recap, not
after it.

## Unsaid (agent's withheld takes)
Positions the agent held but did not voice at the time — from the memory
index and stance records. Surfaced now, still labeled as takes, one line
each; never silently promoted into advice.

## Artifacts
Everything the owner would want to open after reading: topic folder paths,
key files, commits. One path per line, no commentary.

---

Fixed form: no other sections. An emotional-milestones section was
explicitly excluded (owner decision, 2026-11-14) — do not add it; the
recap is a work record, not a diary.
