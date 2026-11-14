---
name: davinci-editing
description: Rules for driving DaVinci Resolve Studio via davinci-resolve-mcp from ZCode — preflight, duplicates as rollback points, proposal→apply→readback, destructive operations only with explicit confirmation, artifact versioning. ALWAYS load for any Resolve task (editing/timelines, markers, grading, media pool, rendering, Fusion, Fairlight). NOT for tasks outside Resolve.
version: 0.2.0
---

# DaVinci Editing — agent rules inside Resolve

Source of truth: the vbcdag repo (`skills/davinci-editing/SKILL.md`); the copy
in `~/.agents/skills/` is a deploy. Patterns taken from competitive research
(vbcdxl/nodes.md §5: readback verification from AdobePremiereProMCP,
duplicate-sequence recovery boundary, proposal+atomic apply from OpenChatCut).

## Preflight (before any operation)

1. `resolve_control runtime_mode` — is Resolve running? (answers without a
   connection).
2. `resolve_control get_version` — the build. The server launches Resolve
   itself if it is closed (first call up to 60s); never a second instance.
3. A connection error mentioning external scripting → tell the owner:
   `Preferences → System → General → External scripting using = Local`. Don't
   hack around it, don't blind-retry.
4. `project_manager get_current` — which project is open? An unfamiliar or
   someone else's project: ask the owner, mutate nothing.
5. Before creative or destructive operations, read the guidance:
   `knowledge topics/get/search` — it carries measured traps of this specific
   build.

## Recovery boundary (iron)

- Any timeline mutation happens on a **duplicate**: `timeline duplicate`. The
  original is not touched.
- `project_manager save` before a series of mutations and after.
- Mutating tools archive the timeline themselves (archive bin,
  `timeline_versioning`) — use `begin_run`/`end_run` so a series of edits
  produces ONE archive and a cumulative delta report, not N.

## Proposal → Apply → Readback

1. **Proposal**: show the edit plan as a list (what, where, which tool, what
   should be visible afterwards). Short edits (one or two mutations) may skip
   the formal plan.
2. **Apply**: after the owner says go, in atomic series; use dry runs where
   they exist (`dry_run=true`, `plan_*` edit-engine actions).
3. **Readback**: after every mutation read the state back (`get_items`,
   `get_transform`, marker `get_all`, `get_current_timecode`, …) and compare
   with the plan. A mismatch is a loud report. Something counts as applied
   only by readback, never by a `True` in the response.
4. Visual changes are verified with a frame: `timeline_frame capture` (or a
   gallery still) — metadata lies more often than a rendered frame.

## Destructive — only with an explicit "yes" from the owner

- `delete_clips` (ripple=True doubly so), `delete_track`, `delete_timelines`,
  `lift_range`, `overwrite_range`, `relink`/`unlink`, `replace_clips`,
  `reset_all_grades`, `delete_version`, bulk marker deletion.
- Confirmation format: a list of victims (names + timecodes/tracks) +
  "apply?".
- Rendering into a non-empty folder: check the previous job first
  (`verify_output`, ls); overwriting happens only with the owner's consent.

## Conventions

- Versions: `<name>_v{N}` for timelines and exports. Never overwrite someone
  else's output.
- Markers: meaningful color/name/note; a marker is a fact from the task, not
  litter. Bulk markers go onto a duplicate first.
- Artifact names the tools produce (still files, drx, exports) are not renamed
  silently.
- Parameters go through tool `params`/`settings`, not through editing configs
  on disk.

## Failure style

- Loud: what we did, what we expected, what readback returned, what the
  error's remediation field says.
- A tool returned False/empty — that is a refusal, not "applied silently".
  Re-verify and report.
- Never roll back on your own initiative; a rollback (rollback/version
  restore) is also a mutation — agree first.

## Tool map (cheat sheet)

- **Read**: `project_manager` (snapshot/settings), `timeline
  probe_timeline_structure`, `timeline_item get_*`, `timeline_markers get_all`,
  `media_pool probe_media_pool`, `timeline_frame capture`.
- **Mutate**: `timeline_item` (transform/composite/fades/audio), `timeline`
  (delete_clips, ripple_insert, duplicate), `timeline_item_markers add`,
  `graph`/`timeline_item_color` (grading), `fusion_comp` (Fusion),
  `edit_engine` (selects/tighten/swap — plan/confirm/execute).
- **Render**: `render prepare_render_job` → `start` → `verify_output`
  (mandatory).
- **Safety**: `resolve_control inspect_operation` — a risk pre-flight by
  action name; `timeline_versioning` (archive/rollback/history).

## Measured traps (live, 2026-11-10, Resolve Studio 21.2.0.6)

- **Generator items are second-class**: a fresh "Solid Color" generator has
  **no node graph** — `safe_set_cdl` refuses loudly (validation passes,
  node preflight fails, nothing half-applies). `set_clip_color` on a
  generator returns `True` but **silently drops the color** — the MCP catches
  it via readback (`CLIP_COLOR_NOT_PERSISTED`). Color/grade work belongs on
  media-backed items; a timeline marker at the clip's start reads back
  reliably if a generator must be marked.
- **`timeline duplicate`** silently moves the project's current-timeline
  pointer to the duplicate; the MCP compensates and reports which timeline is
  current — but any hand-rolled scripting around duplication must
  capture/restore the pointer itself.
- **First mutation on a timeline auto-archives** the pre-mutation state as
  `<name>_archived_v01` into the same project — expected, do not treat it as
  an accident or delete it as litter.
- **`timeline_frame capture` is truthful**: a black frame from a default
  Solid Color generator is the item's real color, not a capture failure (the
  capture returned the exact requested frame with no restore warnings).
- Versioning runs work end to end: `begin_run` → mutations → `end_run`
  aggregated 5 edits / 1 archive version cleanly.
