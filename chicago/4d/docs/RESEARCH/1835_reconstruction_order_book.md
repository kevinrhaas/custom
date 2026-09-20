# The 1835 reconstruction order book

> DERIVED from `data/reconstruction/1835_reconstruction_order_book.json`. Regenerate with
> `tools/build_order_book_1835.py --build`; `tools/check.sh` re-derives both. Do not hand-edit.

**T-1166.** Known minus model, per bucket, with the ticket that owns filling it. The town converges to **2,536 people** in **643 households**, working **108 enumerated businesses**, under **668 roofs**.

| | target | known | to reconstruct |
|---|---:|---:|---:|
| Persons | 2,536 | 457 | 2,082 |
| Households | 643 | 436 | 209 |
| Businesses (enumerated classes) | 108 | 140 | 8 |
| Roofs | 668 | 384 | 297 |

## The rules this book adds

- **point from range** — Where the town model gives a point the book takes it; where it gives only a range the book takes the MIDPOINT, rounded half up, and carries the range beside it. A quota cannot be a range.
- **unresolved known** — A named person or household the layer cannot place on an axis is subtracted PRO RATA across that axis's cells, so the book never orders a replacement for somebody already standing in the town.
- **presence is the test** — Only a household recorded `present` on the scene date counts as known. An `uncertain` one is the roster's R1 class and is offered to T-1172 — counting it in both places orders one person twice.
- **the fort is read not apportioned** — The garrison and its households carry a null target; T-1176 reads the return and the civilian quota is re-cut at the next --build.
- **rounding** — Largest remainder throughout, ties broken on the bucket key, so two builds on one set of inputs are byte-identical.
- **real names first** — The roster (T-1159) offers every name the corpus printed and withheld. It is a licence on WHICH name a filler uses and never a quota, so it is counted against its ticket rather than smeared across cells that cannot hold it.

## Real names before invented ones

The roster offers 1,811 names the corpus printed and this project withheld. Each class is a licence, not a quota:

| class | offered | ticket |
|---|---:|---|
| `R1_in_window_uncertain` | 805 | T-1172 |
| `R2_in_window_single_source` | 343 | T-1172 |
| `R3_1834_return_or_muster` | 30 | T-1172 |
| `R4_surname_only_census` | 440 | T-1170 |
| `R5_later_only_backprojectable` | 55 | T-1172 |
| `R6_native_metis_black` | 138 | T-1177 |

## Persons

Who the town still has to be given, by sex, age, division, household and trade.

- `town_target`: 2,536
- `town_target_basis`: the model's own point within 2,353-3,265
- `town_target_range`: 2353, 3265
- `employed_target`: 506
- `employed_basis`: the midpoint of the model's 424-588, rounded half up
- `lodging_share`: 0.26
- `lodging_share_range`: 0.143, 0.377

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `persons/female/10_19/north/family/none` | 32 | 6 | 26 | 26 | T-1174 |
| `persons/female/10_19/north/lodging/none` | 11 | 2 | 9 | 5 | T-1175 |
| `persons/female/10_19/south/family/none` | 76 | 15 | 61 | 61 | T-1174 |
| `persons/female/10_19/south/lodging/none` | 27 | 5 | 22 | 4 | T-1175 |
| `persons/female/10_19/west/family/none` | 28 | 4 | 24 | 24 | T-1174 |
| `persons/female/10_19/west/lodging/none` | 10 | 2 | 8 | 1 | T-1175 |
| `persons/female/20_29/north/family/trade` | 18 | 3 | 15 | 15 | T-1347 |
| `persons/female/20_29/north/family/none` | 34 | 6 | 28 | 28 | T-1174 |
| `persons/female/20_29/north/lodging/trade` | 6 | 1 | 5 | 2 | T-1175 |
| `persons/female/20_29/north/lodging/none` | 12 | 2 | 10 | 5 | T-1175 |
| `persons/female/20_29/south/family/trade` | 43 | 8 | 35 | 35 | T-1347 |
| `persons/female/20_29/south/family/none` | 81 | 15 | 66 | 66 | T-1174 |
| `persons/female/20_29/south/lodging/trade` | 15 | 3 | 12 | 0 | T-1175 |
| `persons/female/20_29/south/lodging/none` | 29 | 6 | 23 | 4 | T-1175 |
| `persons/female/20_29/west/family/trade` | 16 | 3 | 13 | 13 | T-1347 |
| `persons/female/20_29/west/family/none` | 30 | 5 | 25 | 25 | T-1174 |
| `persons/female/20_29/west/lodging/trade` | 6 | 1 | 5 | 0 | T-1175 |
| `persons/female/20_29/west/lodging/none` | 10 | 1 | 9 | 2 | T-1175 |
| `persons/female/30_39/north/family/trade` | 8 | 2 | 6 | 6 | T-1347 |
| `persons/female/30_39/north/family/none` | 16 | 3 | 13 | 13 | T-1174 |
| `persons/female/30_39/north/lodging/trade` | 3 | 0 | 3 | 1 | T-1175 |
| `persons/female/30_39/north/lodging/none` | 6 | 1 | 5 | 4 | T-1175 |
| `persons/female/30_39/south/family/trade` | 20 | 4 | 16 | 16 | T-1347 |
| `persons/female/30_39/south/family/none` | 38 | 7 | 31 | 31 | T-1174 |
| `persons/female/30_39/south/lodging/trade` | 7 | 1 | 6 | 0 | T-1175 |
| `persons/female/30_39/south/lodging/none` | 13 | 3 | 10 | 2 | T-1175 |
| `persons/female/30_39/west/family/trade` | 7 | 1 | 6 | 6 | T-1347 |
| `persons/female/30_39/west/family/none` | 14 | 2 | 12 | 12 | T-1174 |
| `persons/female/30_39/west/lodging/trade` | 3 | 0 | 3 | 0 | T-1175 |
| `persons/female/30_39/west/lodging/none` | 5 | 1 | 4 | 0 | T-1175 |
| `persons/female/40_49/north/family/trade` | 3 | 0 | 3 | 3 | T-1347 |
| `persons/female/40_49/north/family/none` | 6 | 1 | 5 | 5 | T-1174 |
| `persons/female/40_49/north/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/40_49/north/lodging/none` | 2 | 0 | 2 | 0 | T-1175 |
| `persons/female/40_49/south/family/trade` | 7 | 1 | 6 | 6 | T-1347 |
| `persons/female/40_49/south/family/none` | 14 | 3 | 11 | 11 | T-1174 |
| `persons/female/40_49/south/lodging/trade` | 3 | 0 | 3 | 0 | T-1175 |
| `persons/female/40_49/south/lodging/none` | 5 | 1 | 4 | 0 | T-1175 |
| `persons/female/40_49/west/family/trade` | 3 | 0 | 3 | 3 | T-1347 |
| `persons/female/40_49/west/family/none` | 5 | 1 | 4 | 4 | T-1174 |
| `persons/female/40_49/west/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/40_49/west/lodging/none` | 2 | 0 | 2 | 0 | T-1175 |
| `persons/female/50_plus/north/family/trade` | 2 | 0 | 2 | 2 | T-1347 |
| `persons/female/50_plus/north/family/none` | 4 | 1 | 3 | 3 | T-1174 |
| `persons/female/50_plus/north/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/50_plus/north/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/50_plus/south/family/trade` | 5 | 1 | 4 | 4 | T-1347 |
| `persons/female/50_plus/south/family/none` | 9 | 1 | 8 | 8 | T-1174 |
| `persons/female/50_plus/south/lodging/trade` | 2 | 0 | 2 | 0 | T-1175 |
| `persons/female/50_plus/south/lodging/none` | 3 | 1 | 2 | 0 | T-1175 |
| `persons/female/50_plus/west/family/trade` | 2 | 0 | 2 | 2 | T-1347 |
| `persons/female/50_plus/west/family/none` | 3 | 1 | 2 | 2 | T-1174 |
| `persons/female/50_plus/west/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/50_plus/west/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/under_10/north/family/none` | 55 | 9 | 46 | 46 | T-1174 |
| `persons/female/under_10/north/lodging/none` | 19 | 3 | 16 | 0 | T-1175 |
| `persons/female/under_10/south/family/none` | 132 | 25 | 107 | 107 | T-1174 |
| `persons/female/under_10/south/lodging/none` | 46 | 9 | 37 | 0 | T-1175 |
| `persons/female/under_10/west/family/none` | 49 | 9 | 40 | 40 | T-1174 |
| `persons/female/under_10/west/lodging/none` | 17 | 3 | 14 | 0 | T-1175 |
| `persons/male/10_19/north/family/none` | 37 | 7 | 30 | 30 | T-1174 |
| `persons/male/10_19/north/lodging/none` | 13 | 2 | 11 | 6 | T-1175 |
| `persons/male/10_19/south/family/none` | 88 | 17 | 71 | 71 | T-1174 |
| `persons/male/10_19/south/lodging/none` | 31 | 6 | 25 | 6 | T-1175 |
| `persons/male/10_19/west/family/none` | 32 | 6 | 26 | 26 | T-1174 |
| `persons/male/10_19/west/lodging/none` | 11 | 2 | 9 | 1 | T-1175 |
| `persons/male/20_29/north/family/trade` | 30 | 5 | 25 | 25 | T-1347 |
| `persons/male/20_29/north/family/none` | 58 | 10 | 48 | 0 | T-1171 |
| `persons/male/20_29/north/lodging/trade` | 11 | 2 | 9 | 1 | T-1175 |
| `persons/male/20_29/north/lodging/none` | 20 | 4 | 16 | 8 | T-1175 |
| `persons/male/20_29/south/family/trade` | 73 | 13 | 60 | 60 | T-1347 |
| `persons/male/20_29/south/family/none` | 139 | 26 | 113 | 0 | T-1171 |
| `persons/male/20_29/south/lodging/trade` | 26 | 5 | 21 | 0 | T-1175 |
| `persons/male/20_29/south/lodging/none` | 49 | 10 | 39 | 7 | T-1175 |
| `persons/male/20_29/west/family/trade` | 27 | 4 | 23 | 23 | T-1347 |
| `persons/male/20_29/west/family/none` | 51 | 8 | 43 | 0 | T-1171 |
| `persons/male/20_29/west/lodging/trade` | 10 | 1 | 9 | 1 | T-1175 |
| `persons/male/20_29/west/lodging/none` | 18 | 3 | 15 | 3 | T-1175 |
| `persons/male/30_39/north/family/trade` | 18 | 3 | 15 | 15 | T-1347 |
| `persons/male/30_39/north/family/none` | 34 | 6 | 28 | 0 | T-1171 |
| `persons/male/30_39/north/lodging/trade` | 6 | 1 | 5 | 0 | T-1175 |
| `persons/male/30_39/north/lodging/none` | 12 | 2 | 10 | 5 | T-1175 |
| `persons/male/30_39/south/family/trade` | 43 | 8 | 35 | 35 | T-1347 |
| `persons/male/30_39/south/family/none` | 81 | 15 | 66 | 0 | T-1171 |
| `persons/male/30_39/south/lodging/trade` | 15 | 3 | 12 | 0 | T-1175 |
| `persons/male/30_39/south/lodging/none` | 29 | 6 | 23 | 4 | T-1175 |
| `persons/male/30_39/west/family/trade` | 16 | 3 | 13 | 13 | T-1347 |
| `persons/male/30_39/west/family/none` | 30 | 5 | 25 | 0 | T-1171 |
| `persons/male/30_39/west/lodging/trade` | 5 | 1 | 4 | 0 | T-1175 |
| `persons/male/30_39/west/lodging/none` | 11 | 1 | 10 | 2 | T-1175 |
| `persons/male/40_49/north/family/trade` | 5 | 1 | 4 | 4 | T-1347 |
| `persons/male/40_49/north/family/none` | 10 | 1 | 9 | 0 | T-1171 |
| `persons/male/40_49/north/lodging/trade` | 2 | 0 | 2 | 0 | T-1175 |
| `persons/male/40_49/north/lodging/none` | 3 | 1 | 2 | 0 | T-1175 |
| `persons/male/40_49/south/family/trade` | 12 | 2 | 10 | 10 | T-1347 |
| `persons/male/40_49/south/family/none` | 24 | 5 | 19 | 0 | T-1171 |
| `persons/male/40_49/south/lodging/trade` | 4 | 1 | 3 | 0 | T-1175 |
| `persons/male/40_49/south/lodging/none` | 9 | 1 | 8 | 1 | T-1175 |
| `persons/male/40_49/west/family/trade` | 4 | 1 | 3 | 3 | T-1347 |
| `persons/male/40_49/west/family/none` | 9 | 1 | 8 | 0 | T-1171 |
| `persons/male/40_49/west/lodging/trade` | 2 | 0 | 2 | 0 | T-1175 |
| `persons/male/40_49/west/lodging/none` | 3 | 1 | 2 | 0 | T-1175 |
| `persons/male/50_plus/north/family/trade` | 2 | 0 | 2 | 2 | T-1347 |
| `persons/male/50_plus/north/family/none` | 5 | 1 | 4 | 0 | T-1171 |
| `persons/male/50_plus/north/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/50_plus/north/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/50_plus/south/family/trade` | 6 | 1 | 5 | 5 | T-1347 |
| `persons/male/50_plus/south/family/none` | 11 | 3 | 8 | 0 | T-1171 |
| `persons/male/50_plus/south/lodging/trade` | 2 | 0 | 2 | 0 | T-1175 |
| `persons/male/50_plus/south/lodging/none` | 4 | 1 | 3 | 0 | T-1175 |
| `persons/male/50_plus/west/family/trade` | 2 | 0 | 2 | 2 | T-1347 |
| `persons/male/50_plus/west/family/none` | 4 | 1 | 3 | 0 | T-1171 |
| `persons/male/50_plus/west/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/50_plus/west/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/under_10/north/family/none` | 61 | 10 | 51 | 51 | T-1174 |
| `persons/male/under_10/north/lodging/none` | 22 | 4 | 18 | 0 | T-1175 |
| `persons/male/under_10/south/family/none` | 148 | 28 | 120 | 120 | T-1174 |
| `persons/male/under_10/south/lodging/none` | 52 | 10 | 42 | 0 | T-1175 |
| `persons/male/under_10/west/family/none` | 55 | 9 | 46 | 46 | T-1174 |
| `persons/male/under_10/west/lodging/none` | 19 | 3 | 16 | 0 | T-1175 |
| `persons/garrison/fort` | — | 2 | — | 0 | T-1176 |
| `persons/transient/town` | — | 0 | — | 0 | T-1178 |

## Households

The households the model wants, by kind and division.

- `households_target`: 643
- `households_target_basis`: the midpoint of the model's 469-816, rounded half up
- `households_target_range`: 469, 816
- `known_present`: 436
- `known_uncertain_offered_to_T-1172`: 820

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `households/boarding_house/north` | 11 | 8 | 3 | 0 | T-1175 |
| `households/boarding_house/south` | 40 | 28 | 12 | 0 | T-1175 |
| `households/boarding_house/west` | 9 | 6 | 3 | 0 | T-1175 |
| `households/family_dwelling/north` | 121 | 80 | 41 | 26 | T-1171 |
| `households/family_dwelling/south` | 253 | 176 | 77 | 65 | T-1171 |
| `households/family_dwelling/west` | 108 | 69 | 39 | 33 | T-1171 |
| `households/inn_tavern/north` | 3 | 2 | 1 | 0 | T-1175 |
| `households/inn_tavern/south` | 7 | 5 | 2 | 0 | T-1175 |
| `households/inn_tavern/west` | 4 | 2 | 2 | 0 | T-1175 |
| `households/institutional/north` | 4 | 2 | 2 | 0 | T-1411 |
| `households/institutional/south` | 7 | 5 | 2 | 0 | T-1411 |
| `households/institutional/west` | 1 | 1 | 0 | 0 | T-1411 |
| `households/store_residence/north` | 6 | 4 | 2 | 0 | T-1171 |
| `households/store_residence/south` | 60 | 41 | 19 | 0 | T-1171 |
| `households/store_residence/west` | 9 | 5 | 4 | 0 | T-1171 |
| `households/garrison/fort` | — | 2 | — | 0 | T-1176 |

## Businesses

The December 1835 State census set against the register the town already holds.

- `register_total`: 196
- `at_scene_date`: 223
- `census_enumerated_total`: 118
- `register_businesses_read`: 196
- `division_note`: EVERY BUSINESS BUCKET IS `unassigned` BY DIVISION TODAY, and that is a reading rather than a hole: the register carries a street where the paper printed one and no division at all, and assigning premises to a division is T-1182's audit and T-1198's seating. The key carries the axis so those tickets fill it rather than re-cut the book.
- `staffing_note`: The STAFF each business implies is T-1183's model and is not guessed at here; T-1189 staffs them from it.

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `businesses/bank` | 0 | 0 | 0 | 0 | T-1182 |
| `businesses/book_store` | 2 | 2 | 0 | 0 | T-1184 |
| `businesses/brewery` | 2 | 1 | 1 | 1 | T-1185 |
| `businesses/church` | 5 | 4 | 1 | 0 | T-1411 |
| `businesses/druggist` | 4 | 2 | 2 | 2 | T-1184 |
| `businesses/iron_foundry` | 1 | 2 | 0 | 0 | T-1185 |
| `businesses/lawyer` | 15 | 13 | 2 | 2 | T-1418 |
| `businesses/lottery_office` | 0 | 0 | 0 | 0 | T-1182 |
| `businesses/lyceum_and_reading_room` | 0 | 0 | 0 | 0 | T-1182 |
| `businesses/physician` | 9 | 8 | 1 | 1 | T-1418 |
| `businesses/printing_office` | 2 | 3 | 0 | 0 | T-1411 |
| `businesses/school` | 7 | 7 | 0 | 0 | T-1411 |
| `businesses/silversmith_jeweller` | 2 | 1 | 1 | 1 | T-1185 |
| `businesses/steam_saw_mill` | 1 | 2 | 0 | 0 | T-1187 |
| `businesses/storage_and_forwarding` | 4 | 8 | 0 | 0 | T-1187 |
| `businesses/store` | 44 | 67 | 0 | 0 | T-1184 |
| `businesses/tavern` | 8 | 16 | 0 | 0 | T-1187 |
| `businesses/tin_and_copper_manufactory` | 2 | 4 | 0 | 0 | T-1185 |

## Structures

The roofs the 668-roof programme still owes, by archetype group and division.

- `roof_target`: 668
- `standing_records`: 384
- `standing_with_an_occupant`: 124
- `standing_without_an_occupant`: 260
- `to_build_total`: 297
- `redeal_note`: A roof standing where the order book has nobody to put in it is a SUBSTITUTION for T-1197, never a demolition: 260 of the 384 standing records carry no occupants block today, and T-1197 re-audits them against this book.

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `structures/barns_stables/south` | 35 | 19 | 16 | 0 | T-1212 |
| `structures/barns_stables/west` | 20 | 8 | 12 | 0 | T-1212 |
| `structures/barns_stables/north` | 17 | 7 | 10 | 0 | T-1212 |
| `structures/barns_stables/fort` | 1 | 1 | 0 | 0 | T-1204 |
| `structures/fort_principal/fort` | 10 | 10 | 0 | 0 | T-1204 |
| `structures/inns_taverns/south` | 5 | 5 | 0 | 0 | T-1201 |
| `structures/inns_taverns/west` | 3 | 3 | 0 | 0 | T-1207 |
| `structures/inns_taverns/north` | 2 | 2 | 0 | 0 | T-1205 |
| `structures/institutional_public/south` | 5 | 5 | 0 | 0 | T-1202 |
| `structures/institutional_public/west` | 1 | 1 | 0 | 0 | T-1208 |
| `structures/institutional_public/north` | 3 | 3 | 0 | 0 | T-1205 |
| `structures/larger_boarding_houses/south` | 28 | 7 | 21 | 0 | T-1209 |
| `structures/larger_boarding_houses/west` | 6 | 1 | 5 | 0 | T-1209 |
| `structures/larger_boarding_houses/north` | 8 | 4 | 4 | 0 | T-1209 |
| `structures/ordinary_dwellings/south` | 176 | 110 | 66 | 0 | T-1203 |
| `structures/ordinary_dwellings/west` | 75 | 21 | 54 | 0 | T-1208 |
| `structures/ordinary_dwellings/north` | 84 | 42 | 42 | 0 | T-1206 |
| `structures/small_outbuildings/south` | 48 | 25 | 23 | 0 | T-1212 |
| `structures/small_outbuildings/west` | 14 | 3 | 11 | 0 | T-1212 |
| `structures/small_outbuildings/north` | 20 | 9 | 11 | 0 | T-1212 |
| `structures/small_outbuildings/fort` | 3 | 3 | 0 | 0 | T-1204 |
| `structures/stores_mixed_use/south` | 42 | 32 | 10 | 0 | T-1201 |
| `structures/stores_mixed_use/west` | 6 | 3 | 3 | 0 | T-1207 |
| `structures/stores_mixed_use/north` | 4 | 4 | 0 | 0 | T-1205 |
| `structures/stores_mixed_use/fort` | 1 | 1 | 0 | 0 | T-1204 |
| `structures/warehouses_freight/south` | 11 | 5 | 6 | 0 | T-1200 |
| `structures/warehouses_freight/west` | 2 | 0 | 2 | 0 | T-1207 |
| `structures/warehouses_freight/north` | 7 | 7 | 0 | 0 | T-1205 |
| `structures/workshops/south` | 15 | 14 | 1 | 0 | T-1201 |
| `structures/workshops/west` | 8 | 8 | 0 | 0 | T-1207 |
| `structures/workshops/north` | 7 | 7 | 0 | 0 | T-1205 |
| `structures/workshops/fort` | 1 | 1 | 0 | 0 | T-1204 |

## Ground first

The streets, terrain and lots a structure bucket waits on.

- `roofs_on_committed_ground`: 12
- `roofs_gated_on_coverage`: 285
- `statement`: 12 of the 297 remaining roofs stand on ground this project has already surveyed, platted and modelled. The other 285 have nowhere to go until street control, terrain and hydrology reach them. The binding constraint on the 668-roof programme is coverage, not recipes.

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `ground/blk_south_water_market` | 27 | — | — | 0 | T-1194 |
| `ground/west_wolf_point_outer` | 35 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/south_plat_beyond_committed_control` | 104 | — | — | 0 | T-1194 |
| `ground/west_division_beyond_committed_control` | 52 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/north_division_beyond_modelled_ground` | 67 | — | — | 0 | T-1191, T-1193, T-1194 |

## Where the model and the roof programme disagree

The book carries THE MODEL. Every difference is listed here for T-1196, which re-cuts the 668-roof schedule against it.

| | model | programme | delta |
|---|---:|---:|---:|
| **households_against_dwellings** — The household model wants 643 households and the programme schedules 335 ordinary dwellings (335-377 in the model's own reading). More than one household to a roof is the resolution the census's own 8.204 people per dwelling implies; T-1196 re-cuts the schedule to say how many. | 643 | 335 | +308 |
| **boarding_houses** — The lodging model and the programme agree on the larger boarding houses. | 42 | 42 | +0 |
| **inns_and_taverns** — The model reads 16-16 inns and taverns; the programme schedules 10. | 16 | 10 | +6 |
| **institutional_and_public** — The model reads 9-19 institutional and public roofs; the programme schedules 9. | 19 | 9 | +10 |
| **people_per_roof** — 2,536 people under 668 roofs is the ratio the completed town must meet; the census's own reading for November 1835 is 8.204 people per dwelling over 398 dwellings. | 2,536 | 668 | +0 |

## The invariants the convergence tickets assert

- **every_person_housed** (T-1215) — Every person in the layer — attested, inferred or reconstructed — is a member of a household or a lodging place that is seated on a roof. *Now:* 16 of 436 present households name a lives_at.
- **every_working_person_has_a_workplace** (T-1189) — Every person carrying a trade, profession or employment has a workplace, or a stated `no fixed workplace`. *Now:* 36 of 436 present households name a works_at.
- **every_business_has_staff** (T-1189) — Every business — attested, inferred or reconstructed — carries the staff T-1183's model implies for its kind. *Now:* not yet measurable: the authored business layer is T-1180.
- **every_structure_occupied_or_its_use_stated** (T-1197) — Every standing roof carries an occupant or a stated use. *Now:* 260 of 384 standing records carry no occupants block.
- **dwellings_ratio_within_its_bracket** (T-1215) — The town census's people-per-dwelling ratio is met within the model's bracket. *Now:* the book orders 2,536 people into 643 households.
- **no_bucket_overfilled** (T-1166) — No bucket's `filled` exceeds its `to_reconstruct`; a filler that bypasses the book is red in check.sh. *Now:* enforced by --check on every gate run.
