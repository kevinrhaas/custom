---
id: T-0167
title: Size the desktop parts from a measured desktop profile, and re-cut whatever still overruns
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-0121
opened: 2026-08-23
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Size the desktop parts from a measured desktop profile, and re-cut whatever still overruns.

Piece 2 of 2 of **T-0121 — The desktop smoke's fourth stage has outgrown the ten-minute command ceiling**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** every part of `SMOKE_STAGE` completes inside 600 s **at 1280x800** on a
standard runner, each one measured and the whole profile written where T-0060's fit was
(docs/ROADMAP.md § THE RUN BUDGET) — re-cutting whatever still overruns, never dropping
a check.

**Why this is its own run, measured rather than argued.** T-0166 cut the four stages
into eight and measured the mobile fit: the mobile body is **13 m 30 s** across the
eight parts, and every one of them fits comfortably. The desktop body does not scale
from it. On this runner, against the published mirror:

| | mobile | desktop |
|---|---|---|
| part 6 (facade tones → the K24 aid) | 0 m 44 s | 1 m 53 s |
| part 7 (the flora census → the street names) | 3 m 48 s | **killed at 10 m 00 s** |

So the desktop cost of a part is not a fixed multiple of its mobile cost — the
camera-heavy parts scale several times harder than the DOM-heavy ones, which is exactly
why an eight-way cut sized on the mobile profile leaves parts over the ceiling. **The
profile has to be measured at 1280x800 and the cut sized from it**, and that measurement
is the whole run: the desktop body is roughly 50 minutes and every part costs another
~1 m 45 s boot, so a full desktop pass is 55-70 minutes of foreground commands. It does
not fit beside a re-cut, and the re-cut is what it exists to size.

**Do it in this order**, so nothing is spent twice: run the eight parts at desktop, one
foreground command each, and record the wall clock each prints (a part that is killed
records ">10 m" and nothing else — the reading it did not give is the reason to cut it
first). Split the parts that overrun at a section boundary re-verified for crossing
bindings — `git log` for T-0121's scope-aware scan — and give each new second half the
idempotent prologue its first line needs (T-0166 needed `enterTown()` for parts 6 and 8,
a panel-open guard for part 8, and a re-frame for part 4). Then measure again.
