---
id: T-0235
title: The unfiltered renderer smoke takes 55 minutes on the steward runner, and three tickets reason against a 30-minute cap
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-27
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The unfiltered renderer smoke takes 55 minutes on the steward runner, and three tickets reason against a 30-minute cap.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

## Measured

2026-08-27, steward run for T-0186, on an unmodified tree plus a changelog entry:

    node tools/smoke_renderer.mjs      851 passed, 0 failed
    55 m 10 s unfiltered

The runner has no GPU — chromium launches with `--enable-unsafe-swiftshader` and
rasterises on the CPU, which is where the time goes.

## Why it matters

T-0170, T-0173 and T-0181 all reason about the desktop legs' margin against a
**30-minute** cap. On this runner the whole gate is nearly twice that, so those
three margin figures do not describe the machine the gate actually runs on.

It also does not fit a steward run's foreground: the ceiling on a single
foreground command is 10 m 00 s, and the smoke's own summary line now says so.
This run had to block on the process across six windows to stay synchronous, and
an earlier attempt was killed at 41 minutes — one minute from the finish, as the
flushed fragment showed afterwards — because the run had no way to see progress:
node block-buffers stdout to a pipe, so the log stayed at **zero bytes for the
whole 41 minutes**. Redirecting to a real file instead made it observable.

## Worth considering

- Whether the per-part timings in T-0170/T-0173/T-0181 should be re-measured on a
  software rasteriser rather than on whatever produced the 30-minute figure.
- `SMOKE_STAGE` already splits the run; a documented steward recipe (which stages
  cover which change) would let a run verify what it touched inside its budget.
- The zero-byte-log problem is worth a line in the runbook on its own: a gate you
  cannot watch is a gate that gets killed.
