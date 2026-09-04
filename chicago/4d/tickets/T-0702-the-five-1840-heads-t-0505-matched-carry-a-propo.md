---
id: T-0702
title: The five 1840 heads T-0505 matched carry a proposed later_census block and no IPUMS serial, and the bridge CSV refuses a row without one
state: open
epic: TOWN
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-0515
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The five 1840 heads T-0505 matched carry a proposed later_census block and no IPUMS serial, and the bridge CSV refuses a row without one.

Piece 2 of 2 of **T-0515 — 727 projected residents rest on a letter list alone: regrade every one a second source corroborates and attach its evidence**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

**The finding, measured on dev at the split.** `tools/crosswalk_census_1840_heads.py` (T-0505) adjudicated
498 named 1840 heads against the 1835 name pools and matched five: `stow_william_h` (printed page 225
line 20), `allen_william` (230/26), `carpenter_philo` (217/29), `davis_john` (232/13) and
`hubbard_gurdon` (232/17). Each carries a `proposed_later_census` block whose own note says
"PROPOSED ONLY — T-0515 applies bridges". None of the five is in
`data/research/residents/census_1840_identity_bridges.csv`, which holds three rows recovered from the
v4 workbook.

**Why they cannot simply be appended.** `apply_census_1840_bridges.py`'s `bridge_rows()` requires a
non-blank, unique integer `serial` on every row, and `census_lookup()` joins that serial into the
210-row v4 recovery, which covers printed pages 229-235 only. All five proposals carry `serial: null`
— the page-to-serial fingerprint is T-0504 and is not landed — and three of the five sit on pages 217,
225 and 207, outside the recovered range entirely. So the CSV's join key does not exist for them.

**The ask.** Decide, and implement, how a bridge located by image + printed page + line rather than by
IPUMS serial is carried: either land the serial mapping the block asks for, or give the CSV and
`apply_census_1840_bridges.py` a second, serial-less locator with its own gate. Then apply the five,
report `census_1840_linked` before and after, and keep the standing rule — a bridge needs an
adjudicated discriminator and 1840 composition is never back-projected.

**Links:** T-0505 · T-0504 · T-0515 · T-0698 · #669.

