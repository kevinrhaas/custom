# The 668-roof programme, re-derived against the order book

DERIVED. Written by `tools/reprogramme_roofs_1835.py --build`; re-derived by `--check` in `tools/check.sh`. Do not hand-edit.

Ticket T-1196. An adjudication over committed derived files — no page of any source was opened, nobody is named, nothing is built, and no roof moves ground.

## What moved

The specification schedules **668 roofs**; this re-derivation adopts **668** — no group moves.

The inventory's own defensible range is 565–765 roofs; the adopted total is inside it.

| Group | Spec | Model | Compared in | Adopted | Δ |
|---|---:|---:|---|---:|---:|
| `barns_stables` | 73 | — | not modelled | 73 | +0 |
| `fort_principal` | 10 | 10 | roofs against roofs | 10 | +0 |
| `inns_taverns` | 10 | 15 | roofs against printed notices | 10 | +0 |
| `institutional_public` | 9 | 9 | roofs outside the fort against roofs outside the fort | 9 | +0 |
| `larger_boarding_houses` | 42 | 42 | roofs against roofs | 42 | +0 |
| `ordinary_dwellings` | 335 | 335 | roofs against roofs | 335 | +0 |
| `small_outbuildings` | 85 | — | not modelled | 85 | +0 |
| `stores_mixed_use` | 53 | — | roofs against establishments | 53 | +0 |
| `warehouses_freight` | 20 | — | roofs against establishments | 20 | +0 |
| `workshops` | 31 | — | roofs against establishments | 31 | +0 |

## Why each group stands where it does

**`barns_stables`** — Ancillary. The town model carries no figure for yards and outbuildings and the order book orders none; the ratio to principal roofs is T-1212's to deal. The spec stands untouched.

**`fort_principal`** — The fort component of the model's institutional high end, and the same number. The compound is read from its dossiers, not apportioned.

**`inns_taverns`** — The structure layer holds 10 standing public houses and the programme schedules 10: in roofs the two already agree. The model's 15 is the business register's count of RECORDS at the scene date, which the trade-census crosswalk folds none of, and the register counts notices where a roof count counts houses. Folding a notice into a house is an identity ruling; this tool makes none and owes the delta out.

**`institutional_public`** — The model's low end is the 9 roofs OUTSIDE the fort and its high end adds the 10 principal roofs INSIDE it. The programme schedules both — 9 institutional_public plus 10 fort_principal — so the two agree at 19. The order book's delta of ten is that high end read against one of the two groups.

**`larger_boarding_houses`** — The model reads this figure off district_group_matrix, so its agreement with the programme is the programme agreeing with itself. Recorded as circular rather than banked as corroboration; the group stands because nothing independent moves it.

**`ordinary_dwellings`** — The model's own low end IS this schedule. The order book's competing figure is 643 HOUSEHOLDS, which is a different unit: satisfying it with roofs would seat one family per roof, the error the town model exists to refuse. It is met by occupancy instead — see the dwellings reconciliation, where the rate the order book needs falls inside the band the November census brackets.

**`small_outbuildings`** — Ancillary. The town model carries no figure for yards and outbuildings and the order book orders none; the ratio to principal roofs is T-1212's to deal. The spec stands untouched.

**`stores_mixed_use`** — No model figure schedules this group on its own. The nearest comparandum is the 118–137 establishments the occupation model counts in the compared classes, against the 104 commercial, workshop and freight roofs the programme schedules together — more trades than roofs, which is the store-over-office and shop-house town these families already build. Nothing moves a single group off that.

**`warehouses_freight`** — No model figure schedules this group on its own. The nearest comparandum is the 118–137 establishments the occupation model counts in the compared classes, against the 104 commercial, workshop and freight roofs the programme schedules together — more trades than roofs, which is the store-over-office and shop-house town these families already build. Nothing moves a single group off that.

**`workshops`** — No model figure schedules this group on its own. The nearest comparandum is the 118–137 establishments the occupation model counts in the compared classes, against the 104 commercial, workshop and freight roofs the programme schedules together — more trades than roofs, which is the store-over-office and shop-house town these families already build. Nothing moves a single group off that.

## The census's 398 dwellings, reconciled

The order book orders more households than the programme schedules dwellings. How many households to a roof?

- Dwelling roofs on the scene date: **377** (335 ordinary dwellings, 42 larger houses and boarding houses).
- Households the order book orders: **643**.
- Households to a dwelling, adopted: **1.706**.
- The band the census brackets: **1.636–2.051** — 8.204 people per dwelling in the town census of November 1835, over the 1840 city's household size of 4.0–5.015 (median to mean).
- Inside the bracket: **yes**.

The census counted 398 dwellings in November 1835, four months after the scene, in the fastest-growing months the town had. A July programme of 377 dwelling roofs stands 5.3% below it, which is growth across that gap and not a hole in the schedule. The same date caution governs every class the trade-census crosswalk compares.

Source for the November figures: `andreas_1884_v1`.

## The crosswalk's count fields

Re-derived from `1835_building_inventory.json`'s `family_targets` and the crosswalk's own `priority_rule`. Authored content — archetypes, geometry bands, evidence and assumption notes — is untouched.

Target 668 roofs · 48 instantiated in phase 1 · 620 remaining.

| Rank | Family | Target | Phase 1 | Remaining | Band |
|---:|---|---:|---:|---:|---|
| 1 | `D4` | 75 | 7 | 68 | P0 |
| 2 | `D3` | 65 | 6 | 59 | P0 |
| 3 | `D5` | 58 | 5 | 53 | P0 |
| 4 | `D1` | 52 | 2 | 50 | P0 |
| 5 | `A1` | 42 | 1 | 41 | P1 |
| 6 | `A3` | 40 | 3 | 37 | P1 |
| 7 | `D2` | 38 | 2 | 36 | P1 |
| 8 | `A2` | 31 | 1 | 30 | P1 |
| 9 | `A4` | 28 | 2 | 26 | P1 |
| 10 | `D6` | 29 | 3 | 26 | P1 |
| 11 | `H1` | 18 | 0 | 18 | P2 |
| 12 | `D7` | 18 | 1 | 17 | P2 |
| 13 | `A5` | 17 | 1 | 16 | P2 |
| 14 | `C1` | 18 | 3 | 15 | P2 |
| 15 | `C3` | 17 | 3 | 14 | P2 |
| 16 | `H2` | 14 | 0 | 14 | P2 |
| 17 | `C2` | 13 | 2 | 11 | P2 |
| 18 | `H3` | 10 | 0 | 10 | P2 |
| 19 | `M1` | 10 | 0 | 10 | P2 |
| 20 | `F1` | 8 | 1 | 7 | P3 |
| 21 | `W2` | 8 | 1 | 7 | P3 |
| 22 | `F2` | 7 | 1 | 6 | P3 |
| 23 | `T1` | 6 | 0 | 6 | P3 |
| 24 | `W4` | 7 | 1 | 6 | P3 |
| 25 | `C4` | 5 | 0 | 5 | P3 |
| 26 | `W1` | 6 | 1 | 5 | P3 |
| 27 | `W3` | 6 | 1 | 5 | P3 |
| 28 | `I1` | 4 | 0 | 4 | P4 |
| 29 | `W5` | 4 | 0 | 4 | P4 |
| 30 | `F3` | 3 | 0 | 3 | P4 |
| 31 | `I3` | 3 | 0 | 3 | P4 |
| 32 | `T2` | 3 | 0 | 3 | P4 |
| 33 | `F4` | 2 | 0 | 2 | P4 |
| 34 | `I2` | 2 | 0 | 2 | P4 |
| 35 | `T3` | 1 | 0 | 1 | P4 |

## Deltas this re-derivation does not act on

**`inns_and_taverns`** → T-1190. The business register holds 15 tavern records at the scene date and folds none of them, against 10 scheduled roofs and the same number standing. Whether those records are that many HOUSES is an identity question the business layer's convergence owns; if it folds them the roof programme needs no change, and if it does not, this group re-cuts against the folded count.

**`institutional_and_public`** → the order book's own comparison. build_order_book_1835.programme_deltas reads the town model's institutional HIGH end — which includes the fort's ten principal roofs — against district_group_matrix.institutional_public alone, and reports a delta of ten where the two files agree. The comparison needs the fort group added to its programme side, or the model's low end taken.

**`boarding_houses`** → the town model's own derivation. model_town_1835.build_lodging takes larger_boarding_houses straight off district_group_matrix, so that figure can never disagree with the programme and the order book's delta of zero is a tautology. A figure that cannot fail is not a check on 42 roofs.
