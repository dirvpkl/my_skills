---
name: mission
description: Long-running objective decomposed into a board of cards, worked one card per fresh session, each card verified on its own — the orchestrator drives the board and logs results; cards execute. ALWAYS invoke when the user gives a goal too big for one pass that needs hours across many steps, unattended. Do not attack such a goal in one session or improvise the decomposition. NOT for a single task, NOT for retrying one failing thing (loop).
version: 1.7.0
---

# mission

A mission is a goal that can't be finished in one pass. It gets decomposed into
cards, worked one at a time in a fresh session each, and judged at the end by
a context that didn't do the work.

Mission's MAIN task is the board plus the result log: drive the kanban
(dispatch cards, verify, move) and log every outcome. Mission does not
build — card sessions build (with `coding`). The board's state is the
source of truth; when the attachments exist, execution follows the kanban
service and the record surfaces in the obsidian graph. The stack is PICKED
(owner 2026-11-19): the board = **Planka** (self-hosted docker, Trello-like
UI for the owner, REST for the agents), the graph = **Obsidian** over the
`.workplanx/` folder. Wiring goes per `external-integrations` (REST,
centralized retry) when deployed — until then the `.md` board in the topic
folder is the working truth (owner ruling: «основная задача - канбан +
логирование результатов. не кодинг и не что-то еще»).

- **references/decompose.md** — how to split a goal into cards that are
  independently verifiable, and when the goal is too vague to split yet.
- **references/board.md** — the board file format, card lifecycle, session
  dispatch, and the kanban/whiteboard mechanics.
- **plugins/manifest.json** — active modules, check it.


## Relationship to `loop` and `workplanx`

They're three different scales and they stack:

- **`workplanx`** owns the topic folder and decides whether work may start at
  all (the `build` phase gate). One folder, one decision, per task.
- **`mission`** is above `loop`: it owns *what* the units of work are. Its
  output is a board of cards.
- **`loop`** is the engine for one card: repeat an iteration until that card's
  condition holds.

A card that needs a loop gets one. A card that's a single step doesn't. A
mission that has no cards left is done and goes to a final conformance review
against the goal.

## Process

1. **Get the goal into a checkable shape.** A goal you can't state as "this is
   true when…" is a wish, not a mission. If the user gave one sentence, the
   first act is decomposing it — and if decomposition needs answers only the
   user has, stop and ask (see `references/decompose.md`). Don't guess a scope
   and then build forty cards on it.
2. **Decompose into cards** (`references/decompose.md`). Every card carries its
   own condition — a command or an observable fact. A card you can't verify
   isn't a card, it's a wish that will absorb the whole mission's budget.
3. **Write `mission.md`** into the `workplanx` topic folder: the goal, the
   done-condition for the whole thing, and the board (`references/board.md`).
4. **Run a conformance pass on the board before starting work.** The
   orchestrator or an independent session with clean context checks one
   question: does this plan actually cover the goal. This is the cheap check
   that saves the expensive one. Fix the board, then start.
5. **Work cards in order, one full session per card.** Create the card session
   with `session.create`, drive it with `session.send`, collect the result
   with `session.messages`. The card session gets the card and nothing
   else — not the mission's history, not the other cards' contents. An
   executor that can see the whole board optimizes for the wrong thing. Do
   not use subagents for cards — they lock the orchestration cycle; the
   orchestrator session dispatches and collects, card sessions execute.
6. **After each card: the card's own verification, then the session's
   freshness check — and the result LOGGED on the board.** Mark done only on
   evidence, never on the card session's word; the outcome line goes to the
   board and the topic log the same step.
7. **When the board is empty:** a conformance review against the
   original goal, and the mission's done-condition, by the orchestrator or an
   independent session with clean context. Both. That's the same
   discipline `loop` applies per card, applied to the whole.
8. **Report** per `references/board.md`.

## Fail loud

- **A mission that stops with cards open is not a partial success, it's a
  stopped run.** Say which cards are open and why they stopped. Do not present
  7 of 10 as "mostly done".
- **Never let a card shrink its own condition.** A card that was "auth works
  end-to-end" does not become "auth module exists" because that's what got
  built. That's `loop`'s goalpost rule and it applies one level up: a mission
  whose done-condition quietly narrows is the most expensive failure mode here,
  because everything below it still looks green.
- **Cards that keep failing get re-cut, not re-run.** Three cards failing the
  same way means the decomposition is wrong, not the cards. Stop decomposing
  deeper and go back to `references/decompose.md`.
- **Don't decompose into "research X" + "implement X" as separate cards** unless
  the research card has its own verifiable output. Otherwise the implement card
  inherits every ambiguity the research card left unresolved, at a much higher
  price.

## Report

Goal and its done-condition. Cards: done / open / dropped, each with its
condition and the evidence behind the status. What the last failure was, what
the next human action is. Never dress a stopped mission as a finished one, and
don't narrate each card session — the board is the record.
