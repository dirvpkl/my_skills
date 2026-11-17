---
name: chords
description: Personal shortcut bindings — the owner's shorthand phrases map straight to skills, bundles or actions; a binding is a key chord, one phrase and the whole stack sounds. ALWAYS invoke when a bound phrase appears, or when asked to see, add, change or remove bindings. NOT a music skill — actual chord or music questions are answered directly.
version: 1.4.0
---

# chords

One binding = one phrase that loads a skill, a bundle, or runs a described
action — like a key chord: press once, the stack sounds. A single skill is a
single note; this skill exists so the user's own shorthand works even when no
skill description would catch it, and so personal routing is editable data
instead of remembered context.

- **references/bindings.md** — the binding table. The actual data: read it
  before resolving any phrase; it is user-edited state, not prose.
- **plugins/manifest.json** — dependencies. No modules: targets are sibling
  skills, referenced by name only.

## Process

1. Read `references/bindings.md`.
2. Match the user's phrase by MEANING — the phrase column is the floor,
   not a regex: synonyms and paraphrases that clearly mean the binding
   count. Literal matching is the minimum, comprehension is the rule;
   a doubtful match is "not bound" plus an offer, never a silent pick.
3. Resolve by `kind`:
   - `skill` → invoke the one sibling skill, as if the user had typed /name;
   - `bundle` → invoke every skill in the row, one combined obligation, same
     turn;
   - `action` → do the described step; no skill loads.
4. No match → one line: "not bound", offer to add it — but only when the
   phrase reads as a shortcut attempt; an ordinary free-form request that
   no row matches is normal routing (base's rules), not a forced binding.
   Never guess a target.
5. After resolving, step out of the way: the target skill's own process
   governs from there. chords is a keypress, not a supervisor.

## Editing bindings

Adding, changing, or removing a row is data, not skill semantics: edit the
table, no version bump, no gate. Bind only what the user asked for or
confirmed — confirm the exact phrase and target before writing a row. A
bound phrase that collides with an existing /command or skill name loses
to the explicit form — note the collision in the row instead of removing
the explicit path.
