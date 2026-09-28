---
name: git-workflow
description: Git conventions for any code task — commit discipline, branch naming and creation, merge gating, dependency-upgrade caution, and .gitignore hygiene. Use whenever a task involves making changes to a git-tracked project, not just when the user explicitly mentions git.
version: 1.0.0
---

# git-workflow

<!-- v1 - 2026-09-06 -->

## Trigger
Any code task in a git-tracked project. Bundled by the `coding` dispatcher on every code write/edit — see its activation manifest, which is the real dispatch logic, not this line in isolation.

## Commits
- Always commit changes after finishing a task. No "leave it for later."
- Conventional Commits: `feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:` — short imperative summary line, body only if genuinely needed.

## Branching
- Any code work happens in a separate branch `<type>/<what>` (e.g. `refactor/...`, `feat/...`, `fix/...`). Ask the user before creating it.
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
