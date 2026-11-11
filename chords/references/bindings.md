# bindings — the chord table

User-edited data. One row per binding; phrase matching is case-insensitive
substring. `target` kinds: `skill` (one sibling), `bundle` (several, loaded
together in the same turn), `action` (no skill loads; the described step runs).
Add new rows at the bottom, newest last; never delete a row without the
user's word. What belongs here: phrases the user actually types and their
resolved targets. What does NOT belong here: skill routing rules (those live
in each skill's trigger), session logs, one-off jokes the user did not confirm
as bindings.

| phrase (RU / EN aliases) | target | kind | note |
|---|---|---|---|
| "думалки", "побрейнштормим", "давай подумаем", "подумай", "можешь поискать" | thinking | skill | owner-canonical trigger family: "подумай / поискай / надо чтобы ты…"; substring match covers "можешь поискать чето/скиллы/..." |
| "перепроверь себя", "перепроверь", "чекни потом", "double-check it" | fresh-eyes | skill | finished work only |
| "пока не зелёное", "until green", "крутись" | loop | skill | iterate until the condition holds |
| "разложи на карточки", "это большая цель" | mission | skill | multi-session decomposition |
| "покопай что нового", "find what's new" | researcher | skill | explicit research request only |
| "что сделано?", "отчитайся", "recap" | Recap the session in base's Report shape: what was done, what was refused/asked, next human action — no skill loads | action | the user asks this between work bursts |
| "гит ворктри", "worktree", "ворктри" | coding | skill | routes to the git-workflow sub-skill; automatic since base 1.7.0 (repo pre-flight + worktree preference) |
| "надо написать", "что-то написать", "напиши доку", "напиши мд", "write it up" | coding | skill | ANY writing task — even plain .md — routes to coding (owner rule 2026-11-12) |
