# Holes (fix list, not defaults)

> Separation note: blessed rules live in `default-stack.md`. This file is the
> repair backlog — items graduate out of here when fixed, never by editing
> them into defaults.

- Uptime monitors as-code: monitor containers exist, monitor definitions
  don't — define them or the push URLs rot.
- Shared alerter lib: extract from the best notifier, kill the copies.
- Shared factory adoption: services still on raw framework constructors.
- Dead config knobs: defined, never read — wire or delete on sight.
- One-shot harvest scripts on file queues: pipeline only if they become
  recurring; until then, no stack applies.
