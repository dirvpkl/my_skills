# Examples — git-workflow

**Good:** task touches README + two source files — one commit per logical
change, `feat:`/`fix:` prefix, checks green before committing. **Bad:** one
"update files" commit mixing docs, a dependency bump, and half-finished
work — history becomes unauditable.

**Good:** first state-changing command runs `git rev-parse --is-inside-work-tree`
+ `git status --porcelain`; another session's dirty files are flagged and
routed around. **Bad:** committing on a dirty tree and sweeping someone
else's work into your commit.

**Good:** risky or parallel work goes to a dedicated worktree
(`git worktree add`). **Bad:** force-pushing shared `master` to "clean up"
history nobody asked to clean.
