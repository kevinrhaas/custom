---
id: T-0173
title: The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part 7 is over it
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The desktop smoke's part 4 and part 5 have under a minute of margin on the ceiling, and part
7 is over it.

**Acceptance:** every part of both viewports fits inside 10 m 00 s on this runner, measured
and recorded in `tools/smoke_renderer.mjs`'s own header the way T-0121 and T-0167 recorded
theirs — with the new cut boundaries chosen at a section boundary that crosses no binding.

**Measured on run 8/23/2026 (T-0142's verification), a full nine-part desktop pass:**

| part | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| desktop | 4 m 33 s | 3 m 25 s | 2 m 11 s | **9 m 35 s** | **9 m 20 s** | 1 m 54 s | **10 m 37 s** | 8 m 20 s | 4 m 09 s |

Mobile is comfortable throughout: 1-2 at 2 m 40 s, 3-4 at 3 m 58 s, 5-6 at 3 m 30 s, 7 at
3 m 50 s, 8 at 3 m 07 s, 9 at 1 m 30 s.

Part 7 PASSED — it was run in the background after the ten-minute foreground command was
killed, and the result was read from the log — so nothing is unverified. But a part that has
to be rescued that way is a part that will be lost the next time a run is less careful, and
the failure mode is the one T-0060 exists to prevent: the page-error assertion is the LAST
line of a viewport's body.

T-0170 already owns part 7 on the grounds that it had 2 m 17 s of margin somewhere else and
was measured over the ceiling on another runner; this is that measurement, on this runner,
plus the two parts beside it. Close T-0170 into this or the other way round — do not cut
part 7 twice.

Roughly S: the cut is arithmetic on measured numbers and the header records it.
