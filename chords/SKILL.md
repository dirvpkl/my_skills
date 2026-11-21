---
name: chords
description: Personal shortcut bindings — the owner's shorthand phrases map straight to skills, bundles or actions; a binding is a key chord, one phrase and the whole stack sounds. ALWAYS invoke when a bound phrase appears, or when asked to see, add, change, suggest or remove bindings. NOT a music skill — actual chord or music questions are answered directly.
version: 1.10.0
---

# chords

One binding = one phrase that loads a skill, a bundle, or runs a described
action — like a key chord: press once, the stack sounds. A single skill is a
single note; this skill exists so the user's own shorthand works even when no
skill description would catch it, and so personal routing is editable data
instead of remembered context.

- **chords.md** — the chord table, the data file bound to this skill. Read
  it before resolving any phrase; it is user-edited state, not prose.
- **plugins/manifest.json** — dependencies. No modules: targets are sibling
  skills, referenced by name only.

## What a chord is

A chord is a fixed personal association: a phrase pattern the owner uses →
an action that must happen when it appears. Press once, the whole stack
sounds.

Recognizing one is word work, not string matching. When a phrase arrives:

1. Look at the words, not the sentence — what does each one carry.
2. Translate both ways (RU ↔ EN) — a chord often rhymes across languages.
3. Run the associations the phrase evokes and hold them against the
   table's targets — an analogy carries structure (faces, throws, chances),
   not vibes.
4. Fix what the phrase is asking for — the meaning with the wording
   stripped.
5. Compare with the table: a plausible match → lean in and confirm
   (Process step 2); nothing plausible → "not bound" (step 4).

The terms used below:

- **binding** — one row in `chords.md`: the owner's phrase(s) → a target.
  Bound only on the owner's ask or confirmed word.
- **kinds**: `skill` — one sibling, loads as if the user typed /name;
  `bundle` — several skills that load together in the same turn as ONE
  combined obligation (the row is the single place the stack is defined);
  `action` — no skill loads, the described step just runs.

## Process

1. Read `chords.md`.
2. Match the user's phrase by MEANING — the phrase column illustrates the
   intent each binding serves, not exact strings: no hard keywords;
   synonyms, paraphrases and rough meanings count. There is no
   literal-matching floor. A doubtful match leans IN: name the binding it
   probably is and confirm before loading — a plausible match is never
   dismissed as "not bound". Loading a doubtful match without confirming
   is a guess.
3. Resolve by `kind`:
   - `skill` → invoke the one sibling skill, as if the user had typed /name;
   - `bundle` → invoke every skill in the row, one combined obligation, same
     turn;
   - `action` → do the described step; no skill loads.
4. No match → one line: "not bound", offer to add it — but only when the
   phrase reads as a shortcut attempt; an ordinary free-form request that
   no row matches is normal routing (base's rules), not a forced binding.
5. After resolving, step out of the way: the target skill's own process
   governs from there. chords is a keypress, not a supervisor.

## Initiative — notice, propose, mention

Chord watching runs entirely in the background — as it comes to mind, no
prescribed procedure; the agent notices what it notices. When it notices a
shorthand forming, it proposes the chord in one line. A decline retires
the pattern. When a chord IS added or changed, say so plainly — the
phrase, the target, the kind — and mention it in the same turn. The table is the owner's: the skill proposes, the
owner binds.

## Editing bindings

Adding, changing, or removing a row is data, not skill semantics: edit the
table, no version bump, no gate. Bind only what the user asked for or
confirmed — confirm the exact phrase and target before writing a row, and
mention the change when it lands. A bound phrase that collides with an
existing /command or skill name loses to the explicit form — note the
collision in the row instead of removing the explicit path.
