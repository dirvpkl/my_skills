# chords — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Bound phrase loads in the same turn

**Good:** the user says «думалки» → the thinking bundle (solution-search + workplanx + spine) loads this turn, then chords steps out of the way.
**Bad:** "I see that's one of your shortcuts — want me to load it?"
Rationale: the binding is a keypress, not a question — resolve and load in the same turn; the target skill's own process governs from there.

**Good:** the owner drops «на сегодня» mid-evening → the close-out ritual (afterword + fresh-eyes + recap) starts that same turn, not "later when we wrap up."
**Bad:** acknowledging the phrase and deferring the load to whenever the conversation naturally ends.
Rationale: a chord pressed later is a different note — bindings resolve immediately or they rot.

## No match says so, never guesses

**Good:** the phrase isn't in the table → "not bound — want me to add it?"
**Bad:** "that phrase is close enough to «пока не зелёное», I'll run the loop skill."
Rationale: resolving an unbound phrase to a guessed target invents routing the user never set — no match is a one-line answer plus an offer to add the binding.

**Good:** «закрепи это» — never bound → one "not bound" line, then the request is handled as ordinary chat.
**Bad:** silently reading «закрепи» as «пиши» or any other near row because the meanings feel adjacent.
Rationale: adjacency is not binding — near-misses resolved silently compound into a table that means nothing.

## Explicit form wins on collision

**Good:** the user types `/loop` while a chord phrase collides with it → the explicit command runs, the collision is noted in the row's note.
**Bad:** intercepting the explicit /command because a binding "covers the same words."
Rationale: chords never outranks the explicit path — a colliding bound phrase loses to the explicit form, and the table records the collision rather than removing the explicit route.

**Good:** a row's note says the phrase collides with the /loop command → when the user then types /loop, the harness command runs untouched.
**Bad:** "helpfully" resolving the typed /loop through the bindings table first because a row mentions it.
Rationale: the collision note exists to document coexistence, not to redirect the explicit path through the table.

## The metaphor name doesn't hijack the domain

**Good:** "какие аккорды в этой песне?" is answered directly as a music question.
**Bad:** routing the music question through `references/bindings.md` as if it were a trigger phrase.
Rationale: the skill name is a metaphor — chords is not a music skill, and its surface is bound phrases, not the word "chord".

**Good:** "explain chord progressions" → a plain music answer; the chords skill never loads.
**Bad:** loading chords because the word "chord" appeared in the message.
Rationale: the word in the skill's own name is not a binding on the word itself — only user-established phrases fire it.

## The metaphor name doesn't hijack the domain

**Good:** "какие аккорды в этой песне?" is answered directly as a music question.
**Bad:** routing the music question through `references/bindings.md` as if it were a trigger phrase.
Rationale: the skill name is a metaphor — chords is not a music skill, and its surface is bound phrases, not the word "chord".

## Meaning, not regex

**Good:** user says «а отложим это до вечера» → recognized as the «чекни потом» binding by meaning (defer until later), not because the words match.
**Bad:** only the exact string «чекни потом» fires, and «до вечера» passes as ordinary chat.
Rationale: the user paraphrases constantly — a binding that needs the literal string is a binding that never fires.

**Good:** a terse reply "1" to a presented pick → treated as the answer to that pick, not as an unbound phrase.
**Bad:** treating every short message as a chord candidate and interrogating the user.
Rationale: brevity is an answer when a pick is pending; the chord layer reads intent, not length.

## Bundles are defined here

**Good:** the task matches a bundle row → the whole stack loads as one obligation, and the row is the single place the stack is defined.
**Bad:** base (or any skill) carrying its own private copy of a bundle definition.
Rationale: bundles are owner-edited data in chords — a second copy anywhere is a drift bug.

**Good:** the think-bundle row gains a member later → the row is edited once, and every session re-reads the table from disk before resolving.
**Bad:** an agent loading the stack from last week's memory — four skills when the row now lists five.
Rationale: the row is live data, like every skill — re-read from disk, never recited from memory.

## Mode recognition (moved from base 2026-11-15)

**Good:** owner pastes another agent's spec + "чудо" as a queue message → process the queue, load the stack the spec implies, no re-asking what was already answered.
**Bad:** answering the previous reply's open question first, or "what do you want me to do with this?" when the spec already says it.
Rationale: queue messages arrive without reply chains — the newest item supersedes.

**Good:** «побрейнштормим» → think-first stack (solution-search + workplanx + spine), zero code written.
**Bad:** jumping to implementation because the idea sounded concrete.
Rationale: think-first requests route to the think stack; code waits for the user-pick.

**Good:** «на сегодня» → afterword + fresh-eyes + morning extract, all wired, no re-negotiation.
**Bad:** "what should I do before you go?" when the chord defines the close-out.
Rationale: end-of-night rituals are bindings — run them.

**Good:** owner mourns a lost idea («мне так грустно, что из головы вылетело») → presence first, hold the `#slot`.
**Bad:** rebuilding the idea for them or opening a task list mid-comfort.
Rationale: comfort register is not a task register; the slot keeps fragments safe until they re-derive it.

**Good:** «много букв» → skeleton answer in chat, full state sinks to the topic folder the same turn.
**Bad:** shrinking the answer AND the record together.
Rationale: terse ≠ lossy — the folder remembers what the chat drops.
