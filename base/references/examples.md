# base — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.
Two pairs minimum per rule (owner convention 2026-11-15).

## Resolve paths at runtime

**Good:** the skill catalog is wherever THIS environment exposes it at startup (fallback `%USERPROFILE%/.agents/skills`); a port or host needed → read the skill's `runtime.toml`, never memory.
**Bad:** a path or port pasted from an earlier session and acted on without a check — the environment moved, the fact did not survive.
Rationale: a fact frozen in the plan is already stale; runtime truth is wherever the environment says it is today.

**Good:** the needed runtime key is missing → ask the user for that one key, everything else proceeds.
**Bad:** guessing a port from "typical defaults" or inventing a catalog path.
Rationale: runtime resolution means looking facts up, not interrogating the user — the ask fires only when the key is absent.

## Ask first, pick later — the pick signs

**Good:** an item is unclear, risky, or guessable — the agent catches an internal "hmm", "let me think", "what does the user mean" → user pick: one message with the situation and the options, the user chooses.
**Bad:** building on the guessed interpretation, or blocking the whole task on one unclear item.
Rationale: a guess compounds; a pick costs one message — the signs above are the trigger to stop.

**Good:** delegation vs hands-on is a toss-up → user pick with the tradeoff named.
**Bad:** a fixed policy — always delegating, or never delegating.
Rationale: situational calls are the user's when the agent cannot own them.

## A failed skill load is recovered

**Good:** Skill invocation fails → resolve the catalog at runtime, Read the SKILL.md from disk, follow it as loaded content; ask only if it exists nowhere.
**Bad:** "skill unavailable" and the task quietly dies.
Rationale: execution outranks the broken loader — a manual load counts as loaded.

**Good:** the missing skill is EXTERNAL (harness-side, not in the collection) → report it, user pick: search for it, skip it, or another route.
**Bad:** silently routing around the missing external skill, or hunting the whole disk unasked.
Rationale: internal dependencies are mandatory; external ones fail safe — visibility plus a choice, never a silent gap.

## Write English, always

**Good:** mid-Russian chat, the fix lands — code, comments, commit message, docs all English; the reply mirrors the user's language.
**Bad:** a Russian sentence slips into a tracked file outside the allowed zones.
Rationale: everything the agent touches is public-facing and portable; the chat's language stops at chat.

**Good:** a ticket/issue/README written for a project — English, even though the user discussed it in Russian.
**Bad:** mirroring the conversation language into artifacts.
Rationale: artifacts outlive the conversation; the user chat is the only exception.

## Run the bundle

**Good:** the task matches a bundle → the whole bundle loads this turn; the definitions live in chords bindings, read alongside base.
**Bad:** cherry-picking one skill out of a bundle because "that's enough".
Rationale: a bundle is one combined obligation — partial loading breaks the stack's internal checks.

**Good:** no bundle matches → normal skill routing; no bundle invented on the fly.
**Bad:** composing a new bundle mid-task without the owner's row in chords.
Rationale: bundles are owner-edited data, not agent improvisation.
