---
id: T-0346
title: Desktop smoke stage 4 no longer fits the ten-minute foreground ceiling, so no steward run can take the whole desktop gate
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-28
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Desktop smoke stage 4 no longer fits the ten-minute foreground ceiling, so no steward run can take the whole desktop gate.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)
Desktop smoke stage 4 no longer fits the ten-minute foreground ceiling, so no steward run can take the whole desktop gate.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`tools/smoke_renderer.mjs` documents a staged recipe that exists precisely because a
steward run's single foreground command is capped at ten minutes, and it asserts that
each command in that recipe fits:

    for s in 1 2 3 4 5 6 7 8 9; do SMOKE_VIEWPORT=desktop SMOKE_STAGE=$s node tools/smoke_renderer.mjs --published; done

**Stage 4 no longer fits.** Measured on this branch (T-0314, a data-only change that
touches no geometry), on the GitHub-hosted runner, 2026-08-29:

| desktop stage | wall clock |
|---|---|
| 1 | 4 m 30 s |
| 2 | 4 m 02 s |
| 3 | 2 m 09 s |
| **4** | **killed at 10 m 00 s — never printed its clock** |
| 5 | 8 m 46 s |

Stage 5 at 8 m 46 s is the next one to go, so this is not a one-stage problem.
T-0167 halved part 8 when it was the thinnest margin; the town has grown since and the
margin has moved to parts 4 and 5.

**What it costs:** a steward run cannot take the whole desktop gate any more, so every
PR from the loop has to argue its desktop coverage from the stages that did fit. The
unfiltered single-process pass still runs in `.github/workflows/chicago-4d-smoke.yml`,
which has no ceiling — so the gate is not lost, only the loop's own foreground copy of
it.

**What would fix it:** cut stage 4 in half the way T-0060, T-0121 and T-0167 cut the
ones before it, at a section boundary measured for zero crossing bindings, and re-size
stage 5 at the same time. `SMOKE_TIMING=1` is the instrument — and note the trap the
script's own comment records: a part that BREACHES the ceiling is killed before it
prints its wall clock, so stage 4 has to be profiled under a raised ceiling (or in the
no-ceiling workflow) to find where to cut it.
