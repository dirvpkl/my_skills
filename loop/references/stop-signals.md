# Stop signals — the rationality catalogue

`loop_state.py` catches mechanical stagnation. It cannot catch an agent working
hard in the wrong direction, which is the expensive kind of failure: it burns
the full cap, produces commits, and looks productive the whole way.

Read this before starting a long loop, and check it once per few iterations.
A signal here is a reason to **stop and report**, not to adjust and continue.

## Adjusting the goalposts instead of the work

The most common way a loop burns its whole budget. Watch for:

- **The check got edited, not the thing.** A test was relaxed, an assert
  removed, a `skip` added, a threshold loosened, a timeout raised, a fixture
  rewritten to match the wrong output. This is the single most important entry
  in this file: the loop is now "make the failure go away", which is a different
  goal from the one in `condition:`.
- **The verify command changed mid-run.** Same failure mode, one level up.
  Legitimate once, with a stated reason; a pattern means the goal moved.
- **New scope appeared.** A failing unrelated test gets fixed "while we're
  here", and the original failure is untouched. The unit was more than one unit.

## Activity without progress

- **Same failure, different wording.** The error text shifts (new line numbers,
  different ids) but it's the same class of failure two iterations running. Text
  churn is not progress.
- **Volume going up, signal staying flat.** More code, more files, more commits
  — the condition's number doesn't move. Rewriting the same thing harder is the
  failure mode with the best-looking git history.
- **The last few iterations only read.** Reasoning, planning, re-reading files,
  no artifact. A loop that stopped touching anything is a loop that has run out
  of ideas and is now generating text.

## The agent is solving a different problem

- **It can't reproduce the failure.** If the verify command passes when the
  agent runs it by hand but fails in the loop (or the reverse), the loop and the
  environment disagree. Stop — that's an environment problem, and `testing`
  owns that distinction.
- **It's stuck on something only a human can decide.** A missing secret, an
  ambiguous requirement, two valid designs. A loop cannot resolve any of these;
  it will spend the cap producing variants of the same question.
- **It's working around a broken environment.** Retrying against a dead Docker
  daemon, an unreachable host, a missing dependency. Same shape as a retry, but
  the agent rewrites its own instructions each pass, so nothing accumulates.

## What is *not* a stop signal

- The condition isn't met yet — that's the normal case, that's why there's a cap.
- Two iterations with no new commit, if work is genuinely in flight (a long
  build, a slow deploy) — that's what `no_progress_limit` is for, set it above
  the noise floor rather than stopping by hand.
- One bad iteration after several good ones — variance is not a trend.
- The agent asking a clarifying question mid-loop — that's correct behavior.
  Stop, get the answer, resume with the cap reduced by what was already spent.

## When you do stop

Report it as a stop, with the evidence: which signal fired, the iteration it
fired on, what the last failure was. Don't quietly raise the cap, don't narrow
the condition, and don't re-run the loop "one more time to be sure" — a stop
signal is a finding about the work, and re-running it is how the finding gets
lost.
