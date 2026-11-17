# researcher — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Constraints filter results, not queries

**Good:** searches "self-hosted vector databases" (the class), then drops paid options while filtering results.
**Bad:** every query carries "free" from the start — self-hosted alternatives that don't market "free" never surface.
Rationale: constraints baked into the query filter out candidates that qualify but don't advertise the constraint.

**Good:** "X qualifies but is paid — excluded per constraint, listed anyway."
**Bad:** excluded options silently vanish from the report.
Rationale: the record shows the shape of the pool, not just the survivors — exclusions are the evidence that the constraint was applied, not asserted.

## Narrate the moves

**Good:** "Trying GitHub topics next — the aggregator channel returned only 2024 listings, nothing current."
**Bad:** silent channel-hopping, then one polished list at the end.
Rationale: the reasoning must be followable step by step, not reconstructed from the final report.

**Good:** a source class turns out empty → the narration says so ("registrar forums: zero hits, moving on").
**Bad:** reporting only the hits, as if the empty class never happened.
Rationale: negative results steer the next move — a reader who can't see them can't tell diligence from luck.

## Untraced claim is flagged, not stated

**Good:** "CLI v2 exists per the changelog; v2 pricing not found on the pricing page — unverified."
**Bad:** "v2 costs $0.40/1M tokens" with no source behind it.
Rationale: if it can't be traced to a source, it isn't a fact — flag it or drop it.

**Good:** the claim is dropped entirely when nothing confirms it and nothing depends on it.
**Bad:** keeping it "as a hunch" inside the findings list, unlabeled.
Rationale: an unlabeled hunch reads as a fact two paragraphs later — a hunch either carries a flag or it isn't in the findings.

## Disagreement reported, not resolved silently

**Good:** "The blog post says GA; the release tag is still v1.9 — sources disagree."
**Bad:** reporting "GA" because the blog post looked more official.
Rationale: picking one side silently manufactures certainty the record doesn't contain.

**Good:** the disagreement triggers one more probe (the registry itself) before reporting, when a cheap arbiter exists.
**Bad:** shipping the conflict as-is when one more source class could settle it.
Rationale: disagreement is a prompt to probe deeper, not a verdict to ship — exhaust the cheap arbitration first.

## Exhausted angle, not exhausted query

**Good:** after 3 reformulations return the same results, switches from the aggregator to the registries class; wraps once every source class has been checked.
**Bad:** tenth rephrase of the same search string on the same site.
Rationale: the stop condition is per angle and per source class — a rephrase that returns the same page has added nothing.

**Good:** the wrap-up names which source classes were checked and which returned nothing.
**Bad:** "I looked everywhere" with no class list.
Rationale: the class list is the stop condition's evidence — without it, "exhausted" is a mood, not a measurement.
