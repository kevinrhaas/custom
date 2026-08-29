---
id: T-0390
title: Three of the nine desktop smoke stages no longer fit the ten-minute run ceiling
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

`tools/smoke_renderer.mjs`'s own docstring records the erosion and predicts it is
monotonic: T-0060 cut the body in four, T-0121 re-cut it in eight when three desktop
quarters ran past the ten-minute ceiling, and T-0167 halved part 8 as the thinnest
margin on the desktop profile. Measured again on 2026-08-29, from a steward run:

    desktop stage 1   4 m 08 s   PASS
    desktop stage 2   3 m 54 s   PASS
    desktop stage 3   2 m 10 s   PASS
    desktop stage 4   > 10 m     killed by the ceiling
    desktop stage 5   8 m 48 s   PASS
    desktop stage 6   1 m 54 s   PASS
    desktop stage 7   > 10 m     killed by the ceiling
    desktop stage 8   > 10 m     killed by the ceiling
    desktop stage 9   4 m 07 s   PASS
    mobile 1-2 4 m 36 s · 3-4 6 m 41 s · 5-6 6 m 44 s · 7-9 8 m 39 s — all PASS

Stage 4 was confirmed to blow the ceiling on an UNMODIFIED `origin/dev` worktree as
well — 46 checks taken in nine minutes, the only failure being the suite's own "the
suite body ran to completion" line, which is the clock and not an assertion. So this
is the erosion the docstring predicted arriving again, not any one branch's doing.

The consequence is what makes it worth a ticket rather than a note: a steward run
cannot take the desktop half of its own gate any more, so every branch merges on a
complete mobile pass plus six of the nine desktop parts and an argument about the
other three. Stage 5 at 8 m 48 s is the next one over.

`.github/workflows/chicago-4d-smoke.yml` has no ceiling and takes the unfiltered pass,
so the gate itself is intact — it is the AGENT-side gate that has gone partial.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- Every desktop part fits inside the ten-minute ceiling, measured and printed, with
  the margin on the worst part stated.
- The parts still sum to an unfiltered pass — the section counts add up and the
  always-on count is identical in every invocation, which the summary already asserts.
- `tools/smoke_renderer.mjs`'s docstring carries the new recipe and the new readings,
  and docs/ROADMAP.md § THE RUN BUDGET is updated with them.
