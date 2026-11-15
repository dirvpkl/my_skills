# git-workflow — worked examples

Good vs bad pairs, each with a one-line rationale. Read beside SKILL.md.

## Repo check before the first write

**Good:** first state-changing command comes only after `git rev-parse --is-inside-work-tree` + `git status --porcelain` — branch, dirty files, and whose work is in flight are known.
**Bad:** straight to `git add -A && git commit` on a checkout holding someone else's uncommitted work.
Rationale: uncommitted foreign work is never mixed into your commit — routing around it is the point of the check.

**Good:** the folder is not a repo → `git init` is proposed (version control is the default for any project), not silently skipped.
**Bad:** doing the whole task in an un-versioned folder because "it's just notes".
Rationale: git covers any project work — notes, brainstorms, docs — not only code; the check doubles as the init detector.
