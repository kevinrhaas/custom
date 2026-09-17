---
id: T-1220
title: Gate mint_documented_residents.py --check once the resident name-splitting tickets land
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-17
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

Gate mint_documented_residents.py --check once the resident name-splitting tickets land.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

`tools/mint_documented_residents.py --check` reports 10 file(s) differing on `dev`
(measured 2026-09-17; `data/research/check_gate_baseline.json` had said 42 since before
T-0662 re-measured it). The pass is ungated because the drift cannot be committed as it
stands, and T-0662 read it rather than writing it:

- **Real register growth, and welcome.** Aaron Russell's arrival bound moves from
  1834-11-12 to 1834-10-29 because the corpus now holds a second printing
  (`Aapon Ruseell,` — Democrat, 29 October 1834, column 6). Seven files are of this kind.
- **A name the splitter mangles.** The pass re-mints `hh_grant_james` as `hh_grant_j`
  with the person's name written “J. Jr. Grant”. That is the same family-name splitting
  fault T-1155, T-1217 and T-1218 are open on. Committing it would rename a household
  and publish a mangled name.
- **A retirement that wants a reading.** `hh_montgomery_l_w` — a documented shoemaker —
  is refused now as *"a surname, a trade, and nothing else"*, and the trade the register
  reads has changed to auctioneer. Retiring a documented resident is a finding, not a
  by-product; it needs saying what changed under it and why.

**Acceptance:** the three name-splitting tickets have landed; `--check` is re-measured
against that tree; each remaining difference is read and either committed with what
changed and why stated (the retirement named explicitly, in the changelog) or refused as
a fault; `tools/mint_documented_residents.py --check` is then a step in `tools/check.sh`
and the tool leaves `check_gate_baseline.json`'s ungated list in the same commit
(`audit_check_gates.py --write`).
