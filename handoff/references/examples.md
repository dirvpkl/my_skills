# handoff — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Self-sufficiency reread before delivery

**Good:** rereading the file as the zero-context agent and fixing every unresolvable reference and relative path before handing over.
**Bad:** shipping the handoff with "fix the thing we talked about yesterday" and a `..\src` path.
Rationale: a handoff the fresh agent cannot start from alone is a failed handoff — no chat history comes with it, so every reference must resolve on its own.

## Owner words verbatim

**Good:** the decisions section quotes "keep the bot on the old token until the migration lands" word for word.
**Bad:** "the owner said to keep the token, roughly, for now."
Rationale: paraphrase turns an owner verdict into the writing agent's interpretation — the fresh agent then continues on a guess instead of the owner's actual words.

## Facts carry; takes only if labeled

**Good:** "wildshot: the scheduler is probably the bottleneck — unverified" rides along, clearly labeled.
**Bad:** "the scheduler is the bottleneck" stated as established fact.
Rationale: the handoff carries facts and decisions, not the writing agent's opinions — an unlabeled take becomes the next agent's ground truth.

## Slots travel as slots

**Good:** the `#slot` left empty with its open question intact for the next agent to see.
**Bad:** filling the slot with a plausible value "so the handoff looks complete."
Rationale: filling a slot hides the open decision behind fake completeness — the next agent must see that it is open, not inherit a guessed answer.

## Collect from records, not chat memory

**Good:** the Collect pass reads the owner-message inbox and the topic's decision.md first, then git log — owner picks are quoted from those files.
**Bad:** the handoff assembled from what the writing agent remembers of the chat — two rulings paraphrased from memory, one forgotten entirely.
Rationale: the inbox and topic files are the durable record; chat memory is the lossiest source and the only one that dies with the session.

## Receiving side verifies before continuing

**Good:** the fresh agent reads the handoff, runs the checklist, reports "the roster in Commands & paths is dead" and continues on what still holds.
**Bad:** the fresh agent skims the file and starts executing, discovering mid-work that the trusted model roster was retired the day before.
Rationale: self-sufficiency is checked by the receiver too — a gap caught before work starts is a one-line report; caught after, it is rework on a wrong foundation.
