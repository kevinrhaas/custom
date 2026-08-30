---
id: T-0435
title: The budget page says the 30-minute cap is not this machine's, and the same leg measures 4 m 40 s there against 4 m 44 s here
state: done
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-30
closed: 2026-08-30
pr: 589
claimed_by: run 8/30/2026, 12:06:07 AM CT
blocked_on: null
needs_bake: false
---

The budget page says the 30-minute cap is not this machine's, and the same leg measures 4 m 40 s there against 4 m 44 s here.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

1. `docs/SMOKE-BUDGET.md` no longer asserts that the 30-minute cap "is not this machine's",
   and what replaces it is MEASURED — the same leg, the same bytes, on both runners — not
   argued from specs.
2. The three caps a run lives under are separated on that page and each is named with the
   file that sets it, so the whole/part confusion cannot be made again.
3. T-0170, T-0173 and T-0181 are restored as sound: the page says their figures do describe
   the machine the gate runs on. Their ticket files are not edited (three parallel slices
   hold them this hour).
4. The correction reaches `docs/ROADMAP.md` § THE RUN BUDGET, which is what a run reads when
   sizing a parcel.

## How this ticket came to exist

T-0235 was worked twice on 2026-08-30. Two slices of the same eight-way lane claimed it three
minutes apart — 11:10:00 PM CT and 11:13:48 PM CT — and `ticket.mjs inflight` could not see
the first, because a claim is only visible once its branch is pushed and neither had pushed
yet. The first merged as PR #588 and shipped `tools/smoke_budget.mjs` and
`docs/SMOKE-BUDGET.md`, which are the better artifact and are kept. This ticket is the second
run's one non-duplicative finding, refiled at the QUEUE bottom where new work belongs rather
than smuggled into a closed ticket. **T-0238 is the ticket for the race itself.**

## The two errors, and the measurement

**1. The 55 minutes and the 30 minutes are not the same quantity.** 30 minutes caps ONE LEG
of the nightly gate — one viewport, one range of parts, eight legs in parallel
(`chicago-4d-bake.yml` § `smoke`, `timeout-minutes`). 55 m 10 s is all eight legs' work in a
single process on `chicago-4d-smoke.yml`, which has no leg cap and a 90-minute job timeout.
Neither bounds the other. "Nearly twice the figure those three margins are taken against"
compares a whole to a part.

**2. It is the same machine.** `steward-improve.yml`, `chicago-4d-bake.yml` § `smoke` and
`chicago-4d-smoke.yml` are all `runs-on: ubuntu-latest` — 4 × AMD EPYC 7763, 15 GiB, no GPU,
SwiftShader in all three. On `dev` at `415909cf`, mobile `SMOKE_STAGE=1-2 --published`:

| | |
|---|---|
| bake runner, run 33290607360, `Smoke the published mirror` step | **4 m 40 s** |
| improve runner, this ticket | **4 m 44 s** |

1.4 per cent apart, and the control is real: that bake produced no changes (`open-pr`
skipped), so the mirror it smoked out of its own artifact is `dev`'s committed mirror byte
for byte.

**3. What actually moves a reading is LOAD.** Part 10 ran its 28 staged desktop checks in
**2 m 53 s** here against T-0167's **6 m 10 s** for the same 28 on 2026-08-24 — a factor of
two on the same part on the same machine class. `dev-smoke-state.json` already stamps cpu
count and load average for this reason, and `smoke_budget.mjs` already reports a median. The
page now says a part must never be re-cut off one reading.

## The legs, which had no gaps to fill

`smoke_budget.mjs` names six desktop PARTS with no reading. The four LEGS have none missing,
because every one runs every night. From run 33290607360, the smoke step alone:

| leg | mobile | desktop |
|---|---|---|
| `1-2` | 4 m 40 s | 8 m 36 s |
| `3-6` | 7 m 02 s | 12 m 23 s |
| `7-8` | 6 m 39 s | 12 m 04 s |
| `9-11` | 9 m 14 s | 17 m 28 s |
| total | 27 m 35 s | 50 m 31 s |

The whole mobile half is four commands that each fit the 600 s ceiling. Three of the four
desktop legs are over it. The staged gate is 78 m 06 s against the unfiltered 55 — eight boots
against two — and the worst leg has 12 m 32 s of margin under the 30-minute leg cap.

## What shipped

- `docs/SMOKE-BUDGET.md` — the false premise replaced by the three-cap table, the two-runner
  A/B, the load finding and the measured leg costs. Everything else on that page is #588's
  and is untouched, including `tools/smoke_budget.mjs`, which is not edited at all.
- `docs/ROADMAP.md` § THE RUN BUDGET — the same correction, beside the figures it corrects.

## Not done, and why

- **T-0170, T-0173 and T-0181 are not edited.** They are three parallel slices' rows this
  hour and their figures need no change — the finding is that they were right. The budget page
  says so on their behalf.
- **`tools/smoke_budget.mjs` is not edited.** Its per-part medians are read from the standing
  record and this ticket adds no per-part readings the tool could use; the leg figures come
  from a CI job's step timings, which are not smoke logs and cannot be `record`ed. Teaching
  the tool to read leg timings out of the Actions API is a run of its own, and not this one.
