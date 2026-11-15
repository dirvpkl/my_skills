---
name: git-workflow
description: Version-control conventions for ANY project work — code, notes, brainstorms, reverse-engineering, montage, scripts, whatever lives in a repo (git is version control, and version control is not only about code). Commit discipline, branch naming and creation, merge gating, dependency-upgrade caution, and .gitignore hygiene. Use whenever a task involves making changes to a git-tracked project, not just when the user explicitly mentions git.
version: 1.3.0
---

# git-workflow

<!-- v1 - 2026-09-06 -->
<!-- v1.1.0 - 2026-11-14: promoted out of the coding bundle to a top-level skill; Trigger/description made project-agnostic per the owner — version control covers any project work, not only code. Owner approval phrasings carried over unchanged. -->

## Trigger
ANY task in a git-tracked project, whatever the work is — code, notes, brainstorms, reverse-engineering, montage, scripts, whatever lives in a repo. Git is version control, and version control is not only about code. The `coding` dispatcher also keeps it loaded as a mandatory sibling dependency on every code write/edit — see coding's activation manifest, which is the real dispatch logic, not this line in isolation.

## Git everywhere

Version control is the default for ANY project — a project without a
repo gets `git init` proposed before work starts, and notes, brainstorms,
docs count as project work exactly like code.

## Repo preflight

Before the first state-changing command in any project folder: check
the folder is a repo and what is already dirty (`git rev-parse
--is-inside-work-tree` + `git status --porcelain`) — know the branch,
the dirty files, and whose work is in flight. Another session's
uncommitted changes are never mixed into your commits — flag them and
route around them. Parallel or risky work on one repo happens in a
dedicated worktree (`git worktree add`), not the shared checkout.

## Commits
- Always commit changes after finishing a task. No "leave it for later."
- Conventional Commits: `feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:` — short imperative summary line, body only if genuinely needed.
- Owner approval phrasings — "go ahead and commit", "commit it", "push it", "merge it" — are the explicit user approval the merge/push gates need.

## Branching
- Any project work happens in a separate branch `<type>/<what>` (e.g. `refactor/...`, `feat/...`, `fix/...`). Ask the user before creating it.
- Merge only after checks pass (see `code-quality` and `testing`) and explicit user approval.
- Use a worktree only if the working tree is dirty and must not be stashed, or the user asks for isolation. Otherwise work in the current tree.

## Destructive operations
- Never delete branches/files (`git branch -D`, `rm -rf`) without explicit user confirmation.
- Never upgrade major dependency versions without asking — no silent breaking changes.

## .gitignore
- Every project has one, and it's kept current — anything not part of the project (venvs, caches, local env files, build artifacts, IDE clutter, model weights/checkpoints, etc.) goes in it, not into a commit.

## Version bumps (project code, not this skill package)
- When a change to the *project's own code* is significant (not a one-line fix), bump its version and write a clear, specific description of what changed and why — not just "update" or "fix stuff."
- This is about the project being worked on. For versioning this skill package itself, see the `coding` dispatcher's "Skill versioning" section.

## Report
Note which branch was used, whether it was newly created, and the final commit(s) made.
