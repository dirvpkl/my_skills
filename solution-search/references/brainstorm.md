# Brainstorm mode

A second shape of the same skill. The default mode (`method.md`) answers
"what exists for this verb" - it looks for technique, service, or component
that already does the job. This mode answers a different question: **"we are
stuck - what could we possibly do about it?"**

Use it when the user asks for options rather than a technique ("run a
brainstorm", "what are our options", "пусти брейншторм себе в голову"), when
the default mode came back empty on a blocker that matters, or when the
blocker is a dead end rather than an unknown.

The output is still a decision, not the thing. This mode changes how the
routes are produced, not what leaves the room.

## 1. Inventory before diverging

Before generating routes, list what already exists and is spendable: data
already collected, tools already deployed, accounts already open, access
already granted, dead ends already measured. The strongest route is usually
the one that spends an asset that is already paid for, and a route that
ignores the inventory re-does work that is already in progress.

The inventory is the part that gets skipped and it is the part that carries
the insight. If the project already holds the missing piece, the problem is
not "how do we get it" but "why aren't we using it".

## 2. Diverge wide, including the rejected

- Generate more routes than will be proposed: four to six internally, two to
  three proposed.
- Routes that were already rejected stay in the pool. Each one states why it
  was rejected and **whether that reason still holds**. A rejection that
  expired - the blocker is gone, the cost dropped, the capability appeared -
  is a finding, and it must be re-raised, not silently dropped.
- Every route names five things: what it does, what it costs, what it risks,
  what it unblocks, and how we would know it worked (a checkable condition).
- A route without a measurable cost is not a route, it is a wish. "Best
  effort" is not a cost; "N requests at M seconds each" is.

## 3. Close the dead ends explicitly

The list of what is **not** being done is part of the output, not a footnote.
Each closed direction keeps its evidence: what was measured, when, and where
the measurement lives. A dead end without evidence is an opinion; with
evidence it is a fact the next pass can trust. Without this section the next
session re-walks the same closed ground, which is the most expensive
waste in a long-running effort.

## 4. Converge to a pick

- Propose 2-3 routes, lead with one recommendation and say why.
- Each proposed route states its ladder level (`<hosted>` / `<open-project>` /
  `<component>` / `<template>` / `<own-make>`); an `<own-make>` route names
  the higher levels that were tried and why each one did not fit.
- Order the routes by what they unblock, not by how cheap they are.
- The pick belongs to the user: transcribe their reply verbatim into the
  `user-pick:` line in `decision.md`. A brainstorm without a pick has not
  finished.
- Name the permissions, accounts, budget or time the recommended route needs
  from the user. A route that waits on a yes says which yes.

## 5. Output shape

`brainstorm.md` in the topic folder (this skill owns that file; `workplanx`
ignores extras by design):

- the inventory - what already exists that a route can spend
- the routes - cost, risk, unblocks, checkable condition, ladder level
- the closed directions - with their evidence
- the recommendation and the ordering
- the open questions for the user

`decision.md`: the recommendation with its tradeoffs and the `user-pick:`
line. Nothing else crosses over.

## Anti-patterns (banned)

- A brainstorm that starts executing: pulling one thread "just to see" turns
  a decision into a half-finished implementation and leaves the pick
  ambiguous.
- Routes that ignore the inventory because they are more interesting to
  describe.
- Presenting a route without a cost.
- Dropping a previously rejected route without saying whether the reason
  still holds.
- Presenting the closed list as a mood ("we looked at a lot of things")
  instead of measurements.
- Ending on the brainstorm itself. The deliverable is a pick.
