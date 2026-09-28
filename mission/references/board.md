# The board, the cards, and the subagents

## `mission.md` — one file in the topic folder

Same rule as `loop`: the topic folder is the state, and a second folder would be
a second source of truth. Config at the top, board below, append-only card
history at the bottom.

```
# Mission: <one-line name>

- goal: <the objective in the user's words>
- done_condition: <command or observable fact that means the whole mission is finished>
- do_not_touch: <paths/services that must not change, comma-separated; "-" if none>
- cards_max: <optional sanity cap on how many cards this mission may have>

## Board
- [ ] c1 | <what it delivers> | condition: <command/fact> | depends: -
- [ ] c2 | <...> | condition: <...> | depends: c1

## Done
- c1 | condition: <...> | evidence: <command + its result> | at: <iteration/date>

## Dropped
- c7 | <why it was dropped, by whom>
```

The board is the kanban. `pending` = `[ ]`, `in progress` = `[>]` (exactly one
at a time — two means two agents are improvising), `done` = a line in `## Done`
with evidence, `dropped` = a line in `## Dropped` with a reason. Moving a card
off the board *into* a section is the mechanic: the board is the queue, the
sections are the history, and a card can't be both.

**Done without evidence is not done.** The `evidence:` field is a command and
its result, not a description. "Tests pass" is a description; `pytest tests/api
-q` → `12 passed` is evidence.

## Dispatching a card

- **Fresh subagent per card.** It gets: the card line, the mission's
  `do_not_touch`, the project conventions, and the current state of the repo.
  It does **not** get the mission's reasoning, the previous card's session, or
  the text of the other cards. An agent that can see the whole board starts
  optimizing for the board instead of the card.
- **Include the mission's done-condition for context only**, clearly marked as
  context — a subagent that knows the goal makes better local choices, but must
  not redefine it.
- **One card at a time by default.** Parallel cards are allowed when
  `depends:` says they're independent *and* they don't touch the same files.
  When in doubt, serial: two agents editing one file produce a merge problem
  that costs more than the parallelism saved.
- **The subagent reports; the supervisor verifies.** Run the card's condition
  yourself after the subagent finishes. Never mark a card done on the
  subagent's report — that's the same trust mistake as a loop judging itself,
  one level up.

## Cards that are loops

A card whose condition needs repetition names the loop and stops being a card
the supervisor drives turn by turn:

```
- [ ] c4 | migrate the users table | condition: pytest tests/migrate -q exits 0
        | loop: verify=pytest tests/migrate -q, max_iterations=12, unit=one table
```

The loop engine runs the card; the supervisor comes back when the loop returns
`STOP:*`. A `STOP:no-progress` or `STOP:iteration-cap` on that card means the
card is a **stopped card**, not a done card — report it, don't re-queue it.

## The whiteboard moment

This is the mechanic worth naming, because it's the whole design: the goal
becomes a visible board, the board is the only queue, and cards get moved
across it as they finish. Whoever supervises — human or agent — sees the same
state, and the state is on disk rather than in anyone's head. The card a person
would have moved with a finger is the card a subagent claims with a tool call,
and the reasons section is where a human writes "drop this, wrong assumption".

## Reporting

Goal, done-condition, and the board's state. Per card: condition + evidence (or
why it's open). Cards dropped, with reasons. Which cards needed a loop and how
they ended. What the next human action is. Don't narrate subagent sessions — the
board already says what happened, and a session log is not a result.
