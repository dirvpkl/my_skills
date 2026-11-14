---
name: chords
description: Personal shortcut bindings — the user's shorthand phrases map straight to skills, bundles, or actions. ALWAYS invoke this skill when the user uses a bound phrase ("думалки", "пока не зелёное", "что сделано?", "разложи на карточки") or asks to see, add, change, or remove bindings ("какие шорткаты", "what are my shortcuts", "add a shortcut", "запомни шорткат", "unbind X"). A binding is a key chord — one phrase, the whole stack sounds. NOT a music skill; actual chord/music questions are answered directly.
version: 1.1.0
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

## Trigger

- The user uses a bound phrase from the table → resolve it and load the
  target in the same turn.
- The user asks about bindings (list, add, change, remove) → operate on the
  table; confirm the exact phrase and target before writing a row.

## Process

1. Read `references/bindings.md`.
2. Match the user's phrase (case-insensitive substring against the phrase
   column; RU and EN aliases live in the same row).
3. Resolve by `kind`:
   - `skill` → invoke the one sibling skill, as if the user had typed /name;
   - `bundle` → invoke every skill in the row, one combined obligation, same
     turn;
   - `action` → do the described step; no skill loads.
4. No match → one line: "not bound", offer to add it. Never guess a target.
5. After resolving, step out of the way: the target skill's own process
   governs from there. chords is a keypress, not a supervisor.

## Editing bindings

Adding, changing, or removing a row is data, not skill semantics: edit the
table, no version bump, no gate. Bind only what the user asked for or
confirmed. A bound phrase that collides with an existing /command or skill
name loses to the explicit form — note the collision in the row instead of
removing the explicit path.

## Does NOT trigger on

- Actual music questions ("какие аккорды в этой песне", "what chords are
  these") → answer directly; the name is a metaphor, not a domain.
- A phrase that is already an explicit /command or skill name → the explicit
  form wins; chords does nothing.
- Free-form requests that no row matches → normal routing (base's rules),
  not a forced binding.
