# harness capabilities — the harness this collection currently runs under

This file describes what the current harness exposes (ZCode as of
2026-11-18). Update it when the harness changes; skills never hardcode
these — they resolve here before relying on a capability.

## Execution
- Background execs: a command can run in the background while the agent
  keeps working; the result is collected on demand — and the agent does
  not consume a step until the cmd's answer is back (owner framing:
  «агент не работает, пока не выдан ответ cmd»).
- Foreground commands block until done; timeout caps apply.

## Agents
- Parallel agent limit: 3 configured (owner-stated 2026-11-18). Observed
  empirically: parallel background agents have failed one-on-one — verify
  a second agent actually started before planning around it.
- Agent types: general-purpose, Explore (read-only search), per-type
  visual judges.

## Sessions
- Full session API: create, send, fork, wait, interrupt, rename, archive
  — mission card sessions ride this layer.

## Scheduling
- Cron tasks (recurring, per-timezone) and idle-time queued tasks — the
  watchdog ticks ride the cron layer.

## Hooks
- Event hooks (tool calls, messages) are configurable in harness config —
  the enforcement layer; the metawatcher design lives in the parked list.

## The rule

Skills never assume a capability exists — resolve it here first. A
missing capability is a loud report and a stop, never a silent workaround.
