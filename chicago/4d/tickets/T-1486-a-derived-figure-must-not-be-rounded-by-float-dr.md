---
id: T-1486
title: A derived figure must not be rounded by float drift: sweep the 31 remaining round(sum(...)) sites
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-20
closed: null
pr: null
claimed_by: run 9/20/2026, 4:30:26 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35538771732
---

Two gated writers flapped their committed output between machines this week, and both for
the same reason. `sum()` accumulates left to right and drifts a few parts in 10^15. That
is nothing on a height or an easting — until the true value sits exactly on the rounding
boundary, at which point the drift, and not the measurement, decides the last digit
printed.

**Where it bit.** Found working PR #1585 (T-1477), whose gate was red on two steps that
had nothing to do with its diff:

* `generate_plat_lots.ground_reading` — the School Section's blocks 95, 118 and 119 are
  each perfectly flat at 0.885 m. `min` and `max` rounded that up to 0.89; the mean of
  418 identical samples accumulated to 0.8849999999999949 and rounded DOWN to 0.88. The
  committed record printed **a mean outside its own min and max**, which rounding being
  monotonic says is impossible, and no assertion caught it.
* `derive_hay_limits.programme_blocks` — Kinzie's Addition is platted in feet, so a
  quarter of four corners lands on an exact half-centimetre; **twenty** of these
  centroids sit precisely on the 2 dp boundary. Four of them read one value on the
  loop's machine and the other on CI's, so the committed file was re-derived back and
  forth between two "correct" versions, each red on the other machine. One branch
  committed a re-derivation of it believing it was clearing a stale fossil from dev; it
  was not stale, it was flapping.

Both were fixed in that PR with `math.fsum`, which is correctly rounded and
order-independent, plus a refusal in `ground_reading` for a mean outside its own
min-max. Neither fix moved a committed byte — the arithmetic was wrong, not the data.

**What is left.** 31 further `round(sum(...))` sites in `tools/*.py` carry the same
pattern (`grep -rn "round(sum(" tools/*.py`). Most will never land on a boundary. The
point is not to guess which: the two that bit were both found by a red gate rather than
by reading, and a figure whose last digit is decided by accumulation order is not a
measurement.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

1. Every `round(sum(...))` site in `tools/*.py` that divides by a count is either
   converted to `math.fsum` or carries a one-line note saying why the boundary cannot be
   reached there. The count in this ticket's title is checked at the start, not assumed.
2. A gate step that measures how close each converted figure runs to its rounding
   boundary, so the next one is found by measurement and not by a red CI run on someone
   else's branch. A figure landing within one part in 10^12 of a boundary is reported.
3. Any site that also publishes a min and a max alongside the mean asserts the three
   against each other, as `ground_reading` now does — and the assertion is
   mutation-tested by restoring `sum()` and watching it fire.
4. No committed derived file changes value. If one does, that is a finding to be
   explained on the PR, not a re-derivation to be waved through: the last digit moving
   means the old one was decided by drift.
5. `./tools/check.sh` green, and `tools/writer_inventory.json` untouched by this work —
   this is an arithmetic fix, not a placement pass.

**Not this ticket.** The tie-breaking *rule* itself. A true half like 888.695 has no exact
binary form, so which way `round()` breaks the tie is decided by which double is nearest.
`fsum` makes that decision reproducible everywhere, which is what a gate needs; whether
the project would rather round half away from zero on the exact decimal is a separate
question and nothing currently turns on it.
