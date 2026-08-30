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

**Part 4 has now CROSSED the ceiling — measured 2026-08-28 on the steward runner (T-0028's
verification), twice on the same tree:**

| run | wall clock | outcome |
|---|---|---|
| `SMOKE_PORT=4291 SMOKE_VIEWPORT=desktop SMOKE_STAGE=4` | killed at 9 m 30 s | 42 checks taken, body incomplete |
| `SMOKE_PORT=4293 SMOKE_VIEWPORT=desktop SMOKE_STAGE=4` | killed at 9 m 48 s | 43 checks taken, body incomplete |

Against dev's own record for that part — 46 passed, 2 failed — both runs stop about four
checks short, at the confidence-mode checkbox (`#cm-reconstructed`). So the part no longer
fits a foreground command on this runner and the reading above (9 m 35 s on 2026-08-23) is
the last one that did. `the suite body ran to completion` is what reports it, and it reports
it as a FAIL that looks like a product red and is not one.

What is NOT lost, and it is worth saying because it changes how urgent this is: `zero page
errors` is taken in EVERY invocation rather than only at the end of the body, so the
assertion T-0060 exists to protect was green in both runs above. What is lost is the tail of
the part.

Mobile is still comfortable — `SMOKE_VIEWPORT=mobile SMOKE_STAGE=3-4` ran 7 m 20 s green
(116 passed, 0 failed) on the same tree and the same runner, in the same session.

**RENUMBERED BY T-0346, 2026-08-30, and half of it is done.** "Part 4" here was the part T-0346 cut into parts 4, 5 and 6 — measured after that cut at 1 m 03 s, 6 m 12 s and 2 m 58 s at desktop under eight-way load, so the part-4 half of this ticket is closed by that work. **"Part 5" is now part 7, and it is what is left here**: measured **8 m 48 s** at desktop on the same loaded runner, a margin of **1 m 12 s**, which is T-0167's own definition of not-a-margin. "Part 7" here is now part 9. See ROADMAP § THE RUN BUDGET.
