---
id: T-0181
title: The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin was asserted rather than measured
state: open
epic: META
requested_by: steward
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-24
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

The desktop 7-9 smoke leg has 9m49s of margin against its 30-minute cap, and the margin
was asserted rather than measured.

## What was claimed, and what was measured

T-0171 (PR #348) cut the bake's smoke into eight legs on T-0167's pairing rule and its
merge commit says:

    Measured desktop legs: 6 m 08 s, 8 m 47 s, 8 m 04 s, 17 m 02 s ... Worst leg keeps
    better than ten minutes of margin

Those four numbers were not measured as LEGS. They were summed from T-0167's per-PART
profile, on the reasoning that a pair boots once where the profile paid a boot per part,
so a leg should come in UNDER the sum. Bake run #273 (32690517288) then ran the real
thing:

| leg | predicted | measured | |
|---|---|---|---|
| desktop 1-2 | 6 m 08 s | **5 m 48 s** | under |
| desktop 3-4 | 8 m 47 s | **10 m 16 s** | OVER |
| desktop 5-6 | 8 m 04 s | **10 m 24 s** | OVER |
| desktop 7-9 | 17 m 02 s | **20 m 11 s** | OVER |

Three of four came in over prediction. The worst leg holds **9 m 49 s** against the
`timeout-minutes: 30` on the smoke job — not "better than ten minutes", and the claim in
the commit message is wrong as written.

## Why this is the same defect twice

This programme has now been bitten three times by a cap sized on a number nobody
measured: T-0165 sized the smoke job's 30-minute cap off mobile and killed the desktop
leg of run #269 at 29 m 05 s with 285 checks passed and 0 failed; T-0167 exists because
T-0166's eight-way cut was sized off mobile too. T-0171's margin claim is the third
instance, caught this time before it cost a run — but only because the run was read
line by line afterwards.

T-0167 already wrote down why extrapolation cannot be trusted here: desktop timings
"move by minutes between runs because SwiftShader's cost tracks whatever else the
machine is doing", and part 7 measured 7 m 43 s on one runner having been killed at
10 m 00 s on another three days earlier with an unchanged body. A single measurement of
a leg is therefore also not enough — the spread is the quantity of interest, not one
sample.

## What is actually at risk

Nothing today: run #273 was green end to end, all eight legs SMOKE PASS, and the eight
legs' staged counts sum to 819, matching the unfiltered both-viewport reference from
full-smoke run #10. The risk is a slow runner pushing desktop 7-9 past 30 minutes, which
returns the nightly to exactly the failure mode T-0171 was written to end — a cancelled
leg, `open-pr` never running, and a bake whose content was sound opening nothing.

## The fix, roughly

Two candidates, and the ticket should choose on evidence rather than pick one here:

1. Raise the smoke job's cap to something sized on the measured spread of the worst leg,
   not on one sample. Cheap; does not reduce the leg.
2. Split 7-9 further. T-0167 already had to append part 9 because part 8 carried 107
   staged checks at three times the density of any other part; 7-9 now carries 143 and
   is the tail again.

Whichever is chosen, the number has to come from repeated measurement and the reasoning
has to be written next to it.

## Acceptance

- The worst desktop leg's wall clock is measured on at least three separate runs and the
  spread is recorded in ROADMAP § THE RUN BUDGET beside T-0060's, T-0166's and T-0167's
  fits.
- The cap (or the cut) is set from that spread, and the commit says which measurement it
  used.
- T-0171's merge-commit claim is corrected in the ROADMAP entry, so the record does not
  keep saying "better than ten minutes of margin".

**Re-measured 2026-08-24 by T-0104's run (PR pending), against the published mirror on a
steward runner, one PART per foreground command.** Every part that completed passed with
zero page errors; the wall clocks are the point:

| viewport | parts | wall clock |
|---|---|---|
| mobile | 1-2 · 3-4 · 5-6 · 7-9 | 2 m 46 s · 3 m 58 s · 3 m 29 s · 7 m 54 s — all four fit |
| desktop | 1 · 2 · 3 | 4 m 27 s · 3 m 25 s · 2 m 14 s |
| desktop | 4 | **9 m 38 s** — inside the ten-minute command ceiling by 22 s |
| desktop | 5 | **9 m 15 s** — inside it by 45 s |
| desktop | 6 | 1 m 54 s |
| desktop | 7 | **KILLED at 9 m 45 s (exit 143)** — a single PART now breaches the ceiling |

So the erosion T-0121 tracked across four measurements has reached T-0167's nine-way cut:
part 7 alone no longer fits a steward run's foreground command, and parts 4 and 5 have
under a minute of margin each. Parts 8 and 9 have no reading today because part 7 could
not be got past. That is one more reason this ticket's leg margins have to be measured
per leg rather than summed from parts — three of the nine parts are now at or past the
per-command ceiling the parts were cut to fit.

**THE PART NUMBERS IN THIS TICKET ARE DATED (T-0346, 2026-08-30).** Part 4 was cut into
parts 4, 5 and 6 — the scene-detail ladder was 6 m 17 s of a part the ten-minute ceiling was
killing — and the old parts 5-9 are now 7-11. So read this ticket's numbers through
`old 5→7, 6→8, 7→9, 8→10, 9→11`, and old part 4 as new parts 4+5+6. The mobile legs are
`1-2 3-6 7-8 9-11` and carry exactly what they carried. The readings themselves stand; only
the labels moved.

**AND THE 30-MINUTE CAP THIS TICKET REASONS AGAINST IS NOT THIS MACHINE'S (T-0235,
2026-08-30).** The margins above are taken against a 30-minute figure that was never
measured on the steward runner, which has no GPU and rasterises on the CPU. The whole
gate was measured at 55 m 10 s unfiltered there on 2026-08-27, and the staged total the
committed record now yields is 46 m 35 s — desktop 18 m 02 s over the five parts that
have a reading, mobile 28 m 33 s over all four legs. `node tools/smoke_budget.mjs`
prints that table out of `tools/dev-smoke-state.json` rather than asserting it, names
the parts that still have no reading at all — desktop 4-9 — and `--for <path>…` answers
the question this ticket's margins exist to serve: which parts cover the change in
hand, and do their measured costs fit the 600 s foreground ceiling. See
`docs/SMOKE-BUDGET.md`.

**AND AGAIN, THE SAME DAY (T-0173, 2026-08-30).** Part 7 was halved — the three road-legibility
stations were 7 m 04 s of a part killed at 9 m 25 s — so old part 7 is now parts 7 + 8 and old
parts 8-11 are 9-12. Read this ticket's post-T-0346 numbers through `old 8→9, 9→10, 10→11,
11→12`, and old part 7 as new parts 7+8. The mobile legs are `1-2 3-6 7-9 10-12` and carry
exactly what they carried. The readings themselves stand; only the labels moved.

**RE-READ 2026-09-03 AGAINST THE CORRECTED BUDGET PAGE (T-0450), AND THE OBJECTION ABOVE
IS WITHDRAWN.** The paragraph headed *"AND THE 30-MINUTE CAP THIS TICKET REASONS AGAINST
IS NOT THIS MACHINE'S"* is wrong and is retracted here rather than deleted. Two quantities
were compared that do not bound each other: **30 minutes caps ONE LEG** of the nightly
gate (`chicago-4d-bake.yml` § `smoke`, `timeout-minutes`, eight legs in parallel), while
the **55 m 10 s** offered as its refutation is the whole body in one process on
`chicago-4d-smoke.yml`, which carries no per-leg cap at all and a 90-minute job timeout.
The runners are also the same machine — both `ubuntu-latest`, both `playwright@1.56.1`
and chromium alone, and `smoke_renderer.mjs` passes `--enable-unsafe-swiftshader`
wherever it runs. **So this ticket was reasoning about the right cap all along**, and
`docs/SMOKE-BUDGET.md` § THREE CAPS now says so.

**AND THE LEG THIS TICKET IS ABOUT IS NOW CALLED `10-13`.** Its subject is the desktop
leg measured at 20 m 11 s on bake run #273, when the legs were `1-2 3-4 5-6 7-9` over
nine parts. Pushed through the three cuts of 2026-08-30 — T-0346, T-0173, T-0170 — old
`7+8+9` is today's `10+11+12+13`, which is the fourth leg of the current matrix and still
the tail. `node tools/smoke_budget.mjs --legs` prices it from the standing record at
**17 m 51 s, a margin of 12 m 09 s**, and names it the worst fully measured margin of the
eight legs. Against run #273's 9 m 49 s that is a wider margin, not a narrower one.

**THIS DOES NOT CLOSE THE TICKET, AND THE REASON IS THE TICKET'S OWN.** That 17 m 51 s is
SUMMED from three per-part readings taken one part per foreground command, so it pays a
boot per command where a leg boots once — it is a prediction of a leg from parts, which is
exactly the move this ticket was opened to object to when T-0171 made it. It is an upper
bound and a useful one; it is not a measurement of the leg. **The acceptance stands
unchanged**: the worst desktop leg's wall clock measured on at least three separate runs,
the spread recorded, and the cap or the cut set from the spread. What T-0450 removes is
only the claim that the cap those measurements would be taken against is the wrong one.
