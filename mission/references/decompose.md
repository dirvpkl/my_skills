# Decomposing a goal into cards

## The test for a good card

A card is ready to be worked when all four hold:

1. **Its own condition is a command or an observable fact.** Not "understand
   the auth system" — "the auth flow's entry points are listed in
   `docs/auth.md` with a caller for each". If you can't write the condition,
   the card isn't decomposed yet.
2. **It fits in a fresh context.** A card session gets the card and nothing else. If
   the card only makes sense to someone who read the last three cards, either
   the card is too big or the ordering is wrong — probably the latter, and the
   fix is to write the dependency down.
3. **One card = one outcome.** "Add the endpoint and the tests and the docs" is
   three cards, and as one card it's unfinishable (something always gets
   skipped) and unverifiable (which of the three failed?).
4. **It doesn't need a person mid-card.** A card that stalls on a decision
   belongs in an ask, not in a queue. Queue it as a blocker card with a named
   question, so the mission visibly waits instead of quietly guessing.

## Order by dependency, then by risk

- **Dependencies first, hard dependencies only.** "Reads the file the previous
  card writes" is a real one. "Conceptually related" is not — that ordering
  just serializes work for no reason.
- **Then highest-risk-first.** The card most likely to be impossible, or the one
  whose failure invalidates the rest, goes near the front. Discovering on card
  9 that card 1's assumption was wrong costs the whole mission; finding out on
  card 2 costs one card.
- **A spike is a card.** If a part of the goal is genuinely unknown, make
  "find out whether X is possible, written down as yes/no plus evidence" a
  card with that as its condition. Don't smuggle the uncertainty into an
  implementation card — it becomes a rewrite later.

## When the goal is too vague to decompose

Stop and ask. Three questions earn their cost:

1. **What is true when this is done?** Not "what should we build" — what
   observable state means finished.
2. **What is explicitly out of scope?** Non-goals are what stop a mission from
   growing, and they're the hardest part to recover later.
3. **What must not change?** The do-not-touch list (a live service, a public
   API, a data store) belongs on the board before any card session sees it.

If the user answers "you decide", propose a decomposition in chat and get a
yes before building forty cards. Proceeding on an unconfirmed decomposition is
the expensive version of being helpful.

## Cards that are really a different kind of card

- **Research** — needs its own output artifact (a written answer, a file), not
  just "looked into it".
- **Migration** — cut by table/service/tenant, each with a rollback condition.
- **Cleanup** — cut by directory or by rule violation, each with a check that
  proves the rule now holds.
- **The last mile** — integration, docs, rollout. It's the card most often
  dropped, and dropping it is what makes a mission look done when it isn't. If
  the mission isn't allowed to end without it, it gets a card.
- **A loop** — a card whose condition needs many iterations of the same unit is
  a `loop` card: it names the loop's condition, cap, and verify command, and
  hands the engine over. Don't try to do it inside one card session.

## How many

Enough that each card is small enough to finish, few enough that a human can
still hold the list. If the board is forty cards, the goal is at least two
missions. If it's three cards, each is probably too big. Ten to fifteen is the
usual range, and a board that fits on one screen is a board a human can
actually supervise — which is the entire point of putting it on a board.
