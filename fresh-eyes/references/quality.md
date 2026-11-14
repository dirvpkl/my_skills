# Mode: quality

Hand this file's contents to the judge agent verbatim, along with the
`testing` skill's UX-pass section. The judge has not seen how the work was
written or any reasoning behind it — it only sees the diff/result and this
checklist.

## What to check

1. **Legacy code**: any TODO/FIXME, stub code, dead code, or `as unknown`-style workaround left in the diff?
2. **DRY violations**: any duplicated logic that should have been pulled into a shared helper instead of copy-pasted?
3. **KISS violations**: any speculative abstraction, premature generalization, or extra layer that isn't earning its complexity?
4. **Service-separation violations**: does any service do another service's job (worker logic in the API layer, API logic in the worker, etc.)? Is a heavy/resource-hungry component sharing a container with lightweight request handling?
5. **Hardcoded values**: any baked-in default standing in for real config, or a magic constant that should live in config instead?
6. **Fail-loud violations**: any defensive try/except with no real recovery action? Any silent fallback or placeholder value standing in for a real failure?
7. **Naming**: does every name (including test names) reflect what the thing actually does?
8. **God-files / god-functions**: is any single file or function doing "everything" instead of being split along actual responsibilities?

## What NOT to do
- Don't fix anything — report only.
- Don't talk to the user directly — report back to the main agent, who triages and relays.
- Don't invent complaints not grounded in this checklist or the testing UX-pass — findings need to be specific and traceable to a line/section, not vague impressions.

## Output shape
For each finding: file/line reference, which checklist item it violates, and a one-line explanation of why it matters. If nothing found for a category, say so explicitly rather than omitting it (silence could mean "not checked" instead of "checked, clean").
