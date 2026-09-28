---
name: mission
description: Long-running objective decomposed into a board of cards, worked by subagents, each card verified on its own — the supervisor decomposes and judges, subagents execute. Use when the user gives a goal too big for one pass ("build X", "migrate Y", "research Z thoroughly") and it needs to run for hours across many steps, unattended. Not for a single task, not for retrying one failing thing (that's `loop`).
version: 1.0.0
---

# mission

A mission is a goal that can't be finished in one pass. It gets decomposed into
cards, worked one at a time by a fresh subagent each, and judged at the end by
someone that didn't do the work.

- **references/decompose.md** — how to split a goal into cards that are
  independently verifiable, and when the goal is too vague to split yet.
- **references/board.md** — the board file format, card lifecycle, subagent
  dispatch, and the kanban/whiteboard mechanics.
- **plugins/manifest.json** — active modules, check it.

## Trigger

- A goal that clearly needs more than one working session: "build the whole
  thing", "migrate this service", "research this properly", "clean up the repo".
- The user wants it to run unattended, or to come back to progress rather than
  a single answer.
- Do NOT trigger on: one task that fits in a few iterations (that's `loop`), a
  decision about what to build (`solution-search` + `workplanx`), or research
  that ends in one report (`researcher`).

## Relationship to `loop` and `workplanx`

They're three different scales and they stack:

- **`workplanx`** owns the topic folder and decides whether work may start at
  all (the `build` phase gate). One folder, one decision, per task.
- **`mission`** is above `loop`: it owns *what* the units of work are. Its
  output is a board of cards.
- **`loop`** is the engine for one card: repeat an iteration until that card's
  condition holds.

A card that needs a loop gets one. A card that's a single step doesn't. A
mission that has no cards left is done and goes to `fresh-eyes`.

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
4. **Run a fresh-eyes `conformance` pass on the board before starting work.**
   This is the cheap check that saves the expensive one: a reviewer with clean
   context looking at "does this plan actually cover the goal". Fix the board,
   then start.
5. **Work cards in order, one subagent per card.** The subagent gets the card
   and nothing else — not the mission's history, not the other cards' contents.
   An agent that can see the whole board optimizes for the wrong thing.
6. **After each card: the card's own verification, then the subagent's
   freshness check.** Mark done only on evidence, never on the subagent's word.
7. **When the board is empty:** `fresh-eyes` in `conformance` mode against the
   original goal, and the mission's done-condition. Both. That's the same
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
don't narrate each subagent's session — the board is the record.
