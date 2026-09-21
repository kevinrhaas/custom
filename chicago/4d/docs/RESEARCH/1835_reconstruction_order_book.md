# The 1835 reconstruction order book

> DERIVED from `data/reconstruction/1835_reconstruction_order_book.json`. Regenerate with
> `tools/build_order_book_1835.py --build`; `tools/check.sh` re-derives both. Do not hand-edit.

**T-1166.** Known minus model, per bucket, with the ticket that owns filling it. The town converges to **2,536 people** in **643 households**, working **108 enumerated businesses**, under **668 roofs**.

| | target | known | to reconstruct |
|---|---:|---:|---:|
| Persons | 2,536 | 1,283 | 1,725 |
| Households | 643 | 1,256 | 124 |
| Businesses (enumerated classes) | 108 | 133 | 7 |
| Roofs | 668 | 384 | 297 |

**2,267 people stand in the layer today** and **514** are still owed after the counters, so the town this book converges to is **2,781** — inside the model's 2,353-3,265. `--build` and `--check` both refuse a remainder that lands outside it.

## What the re-cut found

> T-1463 summed T-1386's presence rulings into `known`. These are the three things that made measurable, carried in the book so they cannot go stale in a report.


### t 1171 adjudicated

*T-1171 closed 2026-09-18 (PR #1476) having drawn 124 of 556, and the presence rulings landed 2026-09-19 — the day after. Was its 432 real, or an artifact of a quota cut against a town that did not yet hold the 827 ruled-in people?*

Of the 432, the household leg is DISCHARGED: T-1171's household quota was 182 against 124 drawn and the re-cut takes it to its own drawn figure, so it owes 0. The person leg is PART artifact: 374 before, 227 now. The remainder is owed and is not a counting error, so T-1171 REOPENS for it.

**Verdict:** reopen T-1171 for the persons; the households are discharged

### the remainder said out loud

*What does the town converge to if every remaining order is filled?*

2,267 standing plus 514 still owed is 2,781, inside the model's 2,353-3,265. Before the re-cut the same sum was 2,267 + 843 = 3,110, and the book was ordering a replacement for 826 people already in the layer. It is 245 above the model's 2,536 point, and that surplus is the 590 people drawn into 50 buckets past what the re-cut would now order — named in `recut_refusals`, held rather than clamped, and retired or re-familied by T-1196, T-1197 and T-1179 rather than by this book.

### households are counted in two different units

*The model wants 643 households and the layer now holds 1,391 records. Are those the same thing?*

814 of the 820 records T-1386 ruled present hold exactly ONE person, and 424 of them are a single name off a post-office letter list. A letter-list name evidences a PERSON in the town; whether it evidences a HOUSEHOLD in the model's sense — the model's own average is 3.9 people to a house — is a modelling question, and the persons re-cut does not depend on the answer. The household quota therefore reads 0 owed today. That is arithmetic the ruling forces, not a finding that the town has all the houses it needs.

**Declined:** T-1463 says a run that finds a new modelling decision required is to stop and say so rather than invent it. This is that. Filed for the owner.

## Where the re-cut was refused

50 buckets would have had their order cut below the people already drawn against them. The owner's ruling of 2026-09-20 refuses that by name rather than clamping it: each is held at what was drawn, and the surplus is retired or re-familied by T-1196, T-1197 and T-1179.

| bucket | ticket | quota before the rulings | the re-cut would order | drawn |
|---|---|---:|---:|---:|
| `persons/female/10_19/north/family/none` | T-1174 | 26 | 16 | 26 |
| `persons/female/10_19/south/family/none` | T-1174 | 61 | 36 | 61 |
| `persons/female/10_19/west/family/none` | T-1174 | 24 | 14 | 24 |
| `persons/female/20_29/north/family/trade` | T-1347 | 15 | 9 | 15 |
| `persons/female/20_29/north/family/none` | T-1174 | 28 | 18 | 28 |
| `persons/female/20_29/south/family/trade` | T-1347 | 35 | 21 | 35 |
| `persons/female/20_29/south/family/none` | T-1174 | 66 | 39 | 66 |
| `persons/female/20_29/west/family/trade` | T-1347 | 13 | 8 | 13 |
| `persons/female/20_29/west/family/none` | T-1174 | 25 | 15 | 25 |
| `persons/female/30_39/north/family/trade` | T-1347 | 6 | 4 | 6 |
| `persons/female/30_39/north/family/none` | T-1174 | 13 | 8 | 13 |
| `persons/female/30_39/south/family/trade` | T-1347 | 16 | 10 | 16 |
| `persons/female/30_39/south/family/none` | T-1174 | 31 | 18 | 31 |
| `persons/female/30_39/west/family/trade` | T-1347 | 6 | 3 | 6 |
| `persons/female/30_39/west/family/none` | T-1174 | 12 | 7 | 12 |
| `persons/female/40_49/north/family/trade` | T-1347 | 3 | 2 | 3 |
| `persons/female/40_49/north/family/none` | T-1174 | 5 | 3 | 5 |
| `persons/female/40_49/south/family/trade` | T-1347 | 6 | 3 | 6 |
| `persons/female/40_49/south/family/none` | T-1174 | 11 | 7 | 11 |
| `persons/female/40_49/west/family/trade` | T-1347 | 3 | 1 | 3 |
| `persons/female/40_49/west/family/none` | T-1174 | 4 | 3 | 4 |
| `persons/female/50_plus/north/family/trade` | T-1347 | 2 | 1 | 2 |
| `persons/female/50_plus/north/family/none` | T-1174 | 3 | 2 | 3 |
| `persons/female/50_plus/south/family/trade` | T-1347 | 4 | 2 | 4 |
| `persons/female/50_plus/south/family/none` | T-1174 | 8 | 4 | 8 |
| `persons/female/50_plus/west/family/trade` | T-1347 | 2 | 1 | 2 |
| `persons/female/under_10/north/family/none` | T-1174 | 46 | 28 | 46 |
| `persons/female/under_10/south/family/none` | T-1174 | 107 | 63 | 107 |
| `persons/female/under_10/west/family/none` | T-1174 | 40 | 25 | 40 |
| `persons/male/10_19/north/family/none` | T-1174 | 30 | 19 | 30 |
| `persons/male/10_19/south/family/none` | T-1174 | 71 | 43 | 71 |
| `persons/male/10_19/west/family/none` | T-1174 | 26 | 16 | 26 |
| `persons/male/20_29/north/family/trade` | T-1347 | 25 | 15 | 25 |
| `persons/male/20_29/south/family/trade` | T-1347 | 60 | 35 | 60 |
| `persons/male/20_29/west/family/trade` | T-1347 | 23 | 14 | 23 |
| `persons/male/30_39/north/family/trade` | T-1347 | 15 | 9 | 15 |
| `persons/male/30_39/south/family/trade` | T-1347 | 35 | 21 | 35 |
| `persons/male/30_39/west/family/trade` | T-1347 | 13 | 8 | 13 |
| `persons/male/40_49/north/family/trade` | T-1347 | 4 | 3 | 4 |
| `persons/male/40_49/south/family/trade` | T-1347 | 10 | 6 | 10 |
| `persons/male/40_49/west/family/trade` | T-1347 | 3 | 2 | 3 |
| `persons/male/50_plus/north/family/trade` | T-1347 | 2 | 1 | 2 |
| `persons/male/50_plus/south/family/trade` | T-1347 | 5 | 3 | 5 |
| `persons/male/50_plus/west/family/trade` | T-1347 | 2 | 1 | 2 |
| `persons/male/under_10/north/family/none` | T-1174 | 51 | 30 | 51 |
| `persons/male/under_10/south/family/none` | T-1174 | 120 | 71 | 120 |
| `persons/male/under_10/west/family/none` | T-1174 | 46 | 28 | 46 |
| `households/family_dwelling/north` | T-1171 | 41 | 0 | 26 |
| `households/family_dwelling/south` | T-1171 | 77 | 0 | 65 |
| `households/family_dwelling/west` | T-1171 | 39 | 0 | 33 |

## The rules this book adds

- **point from range** — Where the town model gives a point the book takes it; where it gives only a range the book takes the MIDPOINT, rounded half up, and carries the range beside it. A quota cannot be a range.
- **unresolved known** — A named person or household the layer cannot place on an axis is subtracted PRO RATA across that axis's cells, so the book never orders a replacement for somebody already standing in the town.
- **presence is the test** — A household is known when the index records it `present` on the scene date, or when T-1386's presence rulings rule it present. The 820 `uncertain` households hold 827 people who stand in the layer, so counting them unknown ordered a replacement for each of them (T-1463). The two evidenced absences stay out; the roster stays a licence, not a quota, so counting these once orders nobody twice.
- **the re cut does not reach work already done** — Summing the rulings into `known` shrinks quotas people have already been drawn against. No bucket's order falls below its own `filled`: the re-cut is REFUSED there by name, with both numbers, in `recut_refusals` — never clamped in silence (the owner's ruling of 2026-09-20).
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
| `persons/female/10_19/north/family/none` | 32 | 16 | 26 | 26 | T-1174 |
| `persons/female/10_19/north/lodging/none` | 11 | 5 | 6 | 1 | T-1175 |
| `persons/female/10_19/south/family/none` | 76 | 40 | 61 | 61 | T-1174 |
| `persons/female/10_19/south/lodging/none` | 27 | 14 | 13 | 3 | T-1175 |
| `persons/female/10_19/west/family/none` | 28 | 14 | 24 | 24 | T-1174 |
| `persons/female/10_19/west/lodging/none` | 10 | 5 | 5 | 0 | T-1175 |
| `persons/female/20_29/north/family/trade` | 18 | 9 | 15 | 15 | T-1347 |
| `persons/female/20_29/north/family/none` | 34 | 16 | 28 | 28 | T-1174 |
| `persons/female/20_29/north/lodging/trade` | 6 | 3 | 3 | 1 | T-1175 |
| `persons/female/20_29/north/lodging/none` | 12 | 6 | 6 | 1 | T-1175 |
| `persons/female/20_29/south/family/trade` | 43 | 22 | 35 | 35 | T-1347 |
| `persons/female/20_29/south/family/none` | 81 | 42 | 66 | 66 | T-1174 |
| `persons/female/20_29/south/lodging/trade` | 15 | 8 | 7 | 0 | T-1175 |
| `persons/female/20_29/south/lodging/none` | 29 | 15 | 14 | 4 | T-1175 |
| `persons/female/20_29/west/family/trade` | 16 | 8 | 13 | 13 | T-1347 |
| `persons/female/20_29/west/family/none` | 30 | 15 | 25 | 25 | T-1174 |
| `persons/female/20_29/west/lodging/trade` | 6 | 3 | 3 | 0 | T-1175 |
| `persons/female/20_29/west/lodging/none` | 10 | 4 | 6 | 1 | T-1175 |
| `persons/female/30_39/north/family/trade` | 8 | 4 | 6 | 6 | T-1347 |
| `persons/female/30_39/north/family/none` | 16 | 8 | 13 | 13 | T-1174 |
| `persons/female/30_39/north/lodging/trade` | 3 | 1 | 2 | 2 | T-1175 |
| `persons/female/30_39/north/lodging/none` | 6 | 3 | 3 | 1 | T-1175 |
| `persons/female/30_39/south/family/trade` | 20 | 10 | 16 | 16 | T-1347 |
| `persons/female/30_39/south/family/none` | 38 | 20 | 31 | 31 | T-1174 |
| `persons/female/30_39/south/lodging/trade` | 7 | 4 | 3 | 0 | T-1175 |
| `persons/female/30_39/south/lodging/none` | 13 | 6 | 7 | 2 | T-1175 |
| `persons/female/30_39/west/family/trade` | 7 | 4 | 6 | 6 | T-1347 |
| `persons/female/30_39/west/family/none` | 14 | 7 | 12 | 12 | T-1174 |
| `persons/female/30_39/west/lodging/trade` | 3 | 2 | 1 | 0 | T-1175 |
| `persons/female/30_39/west/lodging/none` | 5 | 2 | 3 | 0 | T-1175 |
| `persons/female/40_49/north/family/trade` | 3 | 1 | 3 | 3 | T-1347 |
| `persons/female/40_49/north/family/none` | 6 | 3 | 5 | 5 | T-1174 |
| `persons/female/40_49/north/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/40_49/north/lodging/none` | 2 | 1 | 1 | 0 | T-1175 |
| `persons/female/40_49/south/family/trade` | 7 | 4 | 6 | 6 | T-1347 |
| `persons/female/40_49/south/family/none` | 14 | 7 | 11 | 11 | T-1174 |
| `persons/female/40_49/south/lodging/trade` | 3 | 2 | 1 | 0 | T-1175 |
| `persons/female/40_49/south/lodging/none` | 5 | 2 | 3 | 0 | T-1175 |
| `persons/female/40_49/west/family/trade` | 3 | 2 | 3 | 3 | T-1347 |
| `persons/female/40_49/west/family/none` | 5 | 2 | 4 | 4 | T-1174 |
| `persons/female/40_49/west/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/40_49/west/lodging/none` | 2 | 1 | 1 | 0 | T-1175 |
| `persons/female/50_plus/north/family/trade` | 2 | 1 | 2 | 2 | T-1347 |
| `persons/female/50_plus/north/family/none` | 4 | 2 | 3 | 3 | T-1174 |
| `persons/female/50_plus/north/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/50_plus/north/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/50_plus/south/family/trade` | 5 | 3 | 4 | 4 | T-1347 |
| `persons/female/50_plus/south/family/none` | 9 | 5 | 8 | 8 | T-1174 |
| `persons/female/50_plus/south/lodging/trade` | 2 | 1 | 1 | 0 | T-1175 |
| `persons/female/50_plus/south/lodging/none` | 3 | 1 | 2 | 0 | T-1175 |
| `persons/female/50_plus/west/family/trade` | 2 | 1 | 2 | 2 | T-1347 |
| `persons/female/50_plus/west/family/none` | 3 | 1 | 2 | 2 | T-1174 |
| `persons/female/50_plus/west/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/50_plus/west/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/female/under_10/north/family/none` | 55 | 27 | 46 | 46 | T-1174 |
| `persons/female/under_10/north/lodging/none` | 19 | 10 | 9 | 0 | T-1175 |
| `persons/female/under_10/south/family/none` | 132 | 69 | 107 | 107 | T-1174 |
| `persons/female/under_10/south/lodging/none` | 46 | 24 | 22 | 0 | T-1175 |
| `persons/female/under_10/west/family/none` | 49 | 24 | 40 | 40 | T-1174 |
| `persons/female/under_10/west/lodging/none` | 17 | 8 | 9 | 0 | T-1175 |
| `persons/male/10_19/north/family/none` | 37 | 18 | 30 | 30 | T-1174 |
| `persons/male/10_19/north/lodging/none` | 13 | 6 | 7 | 2 | T-1175 |
| `persons/male/10_19/south/family/none` | 88 | 45 | 71 | 71 | T-1174 |
| `persons/male/10_19/south/lodging/none` | 31 | 17 | 14 | 4 | T-1175 |
| `persons/male/10_19/west/family/none` | 32 | 16 | 26 | 26 | T-1174 |
| `persons/male/10_19/west/lodging/none` | 11 | 5 | 6 | 1 | T-1175 |
| `persons/male/20_29/north/family/trade` | 30 | 15 | 25 | 25 | T-1347 |
| `persons/male/20_29/north/family/none` | 58 | 28 | 30 | 0 | T-1171 |
| `persons/male/20_29/north/lodging/trade` | 11 | 6 | 5 | 1 | T-1175 |
| `persons/male/20_29/north/lodging/none` | 20 | 10 | 10 | 5 | T-1175 |
| `persons/male/20_29/south/family/trade` | 73 | 38 | 60 | 60 | T-1347 |
| `persons/male/20_29/south/family/none` | 139 | 72 | 67 | 0 | T-1171 |
| `persons/male/20_29/south/lodging/trade` | 26 | 14 | 12 | 0 | T-1175 |
| `persons/male/20_29/south/lodging/none` | 49 | 25 | 24 | 7 | T-1175 |
| `persons/male/20_29/west/family/trade` | 27 | 13 | 23 | 23 | T-1347 |
| `persons/male/20_29/west/family/none` | 51 | 24 | 27 | 0 | T-1171 |
| `persons/male/20_29/west/lodging/trade` | 10 | 5 | 5 | 1 | T-1175 |
| `persons/male/20_29/west/lodging/none` | 18 | 9 | 9 | 2 | T-1175 |
| `persons/male/30_39/north/family/trade` | 18 | 9 | 15 | 15 | T-1347 |
| `persons/male/30_39/north/family/none` | 34 | 16 | 18 | 0 | T-1171 |
| `persons/male/30_39/north/lodging/trade` | 6 | 3 | 3 | 0 | T-1175 |
| `persons/male/30_39/north/lodging/none` | 12 | 5 | 7 | 2 | T-1175 |
| `persons/male/30_39/south/family/trade` | 43 | 22 | 35 | 35 | T-1347 |
| `persons/male/30_39/south/family/none` | 81 | 42 | 39 | 0 | T-1171 |
| `persons/male/30_39/south/lodging/trade` | 15 | 8 | 7 | 0 | T-1175 |
| `persons/male/30_39/south/lodging/none` | 29 | 15 | 14 | 4 | T-1175 |
| `persons/male/30_39/west/family/trade` | 16 | 8 | 13 | 13 | T-1347 |
| `persons/male/30_39/west/family/none` | 30 | 15 | 15 | 0 | T-1171 |
| `persons/male/30_39/west/lodging/trade` | 5 | 2 | 3 | 0 | T-1175 |
| `persons/male/30_39/west/lodging/none` | 11 | 5 | 6 | 0 | T-1175 |
| `persons/male/40_49/north/family/trade` | 5 | 2 | 4 | 4 | T-1347 |
| `persons/male/40_49/north/family/none` | 10 | 5 | 5 | 0 | T-1171 |
| `persons/male/40_49/north/lodging/trade` | 2 | 1 | 1 | 0 | T-1175 |
| `persons/male/40_49/north/lodging/none` | 3 | 1 | 2 | 1 | T-1175 |
| `persons/male/40_49/south/family/trade` | 12 | 6 | 10 | 10 | T-1347 |
| `persons/male/40_49/south/family/none` | 24 | 13 | 11 | 0 | T-1171 |
| `persons/male/40_49/south/lodging/trade` | 4 | 2 | 2 | 0 | T-1175 |
| `persons/male/40_49/south/lodging/none` | 9 | 5 | 4 | 1 | T-1175 |
| `persons/male/40_49/west/family/trade` | 4 | 2 | 3 | 3 | T-1347 |
| `persons/male/40_49/west/family/none` | 9 | 4 | 5 | 0 | T-1171 |
| `persons/male/40_49/west/lodging/trade` | 2 | 1 | 1 | 0 | T-1175 |
| `persons/male/40_49/west/lodging/none` | 3 | 1 | 2 | 0 | T-1175 |
| `persons/male/50_plus/north/family/trade` | 2 | 1 | 2 | 2 | T-1347 |
| `persons/male/50_plus/north/family/none` | 5 | 2 | 3 | 0 | T-1171 |
| `persons/male/50_plus/north/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/50_plus/north/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/50_plus/south/family/trade` | 6 | 3 | 5 | 5 | T-1347 |
| `persons/male/50_plus/south/family/none` | 11 | 6 | 5 | 0 | T-1171 |
| `persons/male/50_plus/south/lodging/trade` | 2 | 1 | 1 | 0 | T-1175 |
| `persons/male/50_plus/south/lodging/none` | 4 | 2 | 2 | 0 | T-1175 |
| `persons/male/50_plus/west/family/trade` | 2 | 1 | 2 | 2 | T-1347 |
| `persons/male/50_plus/west/family/none` | 4 | 2 | 2 | 0 | T-1171 |
| `persons/male/50_plus/west/lodging/trade` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/50_plus/west/lodging/none` | 1 | 0 | 1 | 0 | T-1175 |
| `persons/male/under_10/north/family/none` | 61 | 31 | 51 | 51 | T-1174 |
| `persons/male/under_10/north/lodging/none` | 22 | 11 | 11 | 0 | T-1175 |
| `persons/male/under_10/south/family/none` | 148 | 77 | 120 | 120 | T-1174 |
| `persons/male/under_10/south/lodging/none` | 52 | 27 | 25 | 0 | T-1175 |
| `persons/male/under_10/west/family/none` | 55 | 27 | 46 | 46 | T-1174 |
| `persons/male/under_10/west/lodging/none` | 19 | 9 | 10 | 0 | T-1175 |
| `persons/garrison/fort` | — | 2 | — | 0 | T-1176 |
| `persons/transient/town` | — | 0 | — | 0 | T-1178 |

## Households

The households the model wants, by kind and division.

- `households_target`: 643
- `households_target_basis`: the midpoint of the model's 469-816, rounded half up
- `households_target_range`: 469, 816
- `known_present`: 1,256
- `known_uncertain_in_the_index_ruled_in_by_T-1386`: 820

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `households/boarding_house/north` | 11 | 12 | 0 | 0 | T-1175 |
| `households/boarding_house/south` | 40 | 46 | 0 | 0 | T-1175 |
| `households/boarding_house/west` | 9 | 10 | 0 | 0 | T-1175 |
| `households/family_dwelling/north` | 121 | 129 | 26 | 26 | T-1171 |
| `households/family_dwelling/south` | 253 | 289 | 65 | 65 | T-1171 |
| `households/family_dwelling/west` | 108 | 113 | 33 | 33 | T-1171 |
| `households/inn_tavern/north` | 3 | 3 | 0 | 0 | T-1175 |
| `households/inn_tavern/south` | 7 | 8 | 0 | 0 | T-1175 |
| `households/inn_tavern/west` | 4 | 4 | 0 | 0 | T-1175 |
| `households/institutional/north` | 4 | 4 | 0 | 0 | T-1189 |
| `households/institutional/south` | 7 | 8 | 0 | 0 | T-1189 |
| `households/institutional/west` | 1 | 1 | 0 | 0 | T-1189 |
| `households/store_residence/north` | 6 | 7 | 0 | 0 | T-1171 |
| `households/store_residence/south` | 60 | 68 | 0 | 0 | T-1171 |
| `households/store_residence/west` | 9 | 9 | 0 | 0 | T-1171 |
| `households/garrison/fort` | — | 2 | — | 0 | T-1176 |

## Businesses

The December 1835 State census set against the register the town already holds.

- `register_total`: 196
- `at_scene_date`: 216
- `census_enumerated_total`: 118
- `register_businesses_read`: 196
- `division_note`: EVERY BUSINESS BUCKET IS `unassigned` BY DIVISION TODAY, and that is a reading rather than a hole: the register carries a street where the paper printed one and no division at all, and assigning premises to a division is T-1182's audit and T-1198's seating. The key carries the axis so those tickets fill it rather than re-cut the book.
- `staffing_note`: The STAFF each business implies is T-1183's model and is not guessed at here; T-1189 staffs them from it.

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `businesses/bank` | 0 | 0 | 0 | 0 | T-1182 |
| `businesses/book_store` | 2 | 2 | 0 | 0 | T-1184 |
| `businesses/brewery` | 2 | 1 | 1 | 1 | T-1185 |
| `businesses/church` | 5 | 4 | 0 | 0 | T-1215 |
| `businesses/druggist` | 4 | 2 | 2 | 2 | T-1184 |
| `businesses/iron_foundry` | 1 | 2 | 0 | 0 | T-1185 |
| `businesses/lawyer` | 15 | 13 | 2 | 2 | T-1418 |
| `businesses/lottery_office` | 0 | 0 | 0 | 0 | T-1182 |
| `businesses/lyceum_and_reading_room` | 0 | 0 | 0 | 0 | T-1182 |
| `businesses/physician` | 9 | 8 | 1 | 1 | T-1418 |
| `businesses/printing_office` | 2 | 2 | 0 | 0 | T-1215 |
| `businesses/school` | 7 | 5 | 0 | 0 | T-1215 |
| `businesses/silversmith_jeweller` | 2 | 1 | 1 | 1 | T-1185 |
| `businesses/steam_saw_mill` | 1 | 2 | 0 | 0 | T-1187 |
| `businesses/storage_and_forwarding` | 4 | 7 | 0 | 0 | T-1187 |
| `businesses/store` | 44 | 65 | 0 | 0 | T-1184 |
| `businesses/tavern` | 8 | 15 | 0 | 0 | T-1187 |
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
| `structures/ordinary_dwellings/west` | 75 | 26 | 49 | 0 | T-1208 |
| `structures/ordinary_dwellings/north` | 84 | 42 | 42 | 0 | T-1206 |
| `structures/small_outbuildings/south` | 48 | 25 | 23 | 0 | T-1212 |
| `structures/small_outbuildings/west` | 14 | 2 | 12 | 0 | T-1212 |
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
| `structures/workshops/west` | 8 | 4 | 4 | 0 | T-1207 |
| `structures/workshops/north` | 7 | 7 | 0 | 0 | T-1205 |
| `structures/workshops/fort` | 1 | 1 | 0 | 0 | T-1204 |

## Ground first

The streets, terrain and lots a structure bucket waits on.

- `roofs_on_committed_ground`: 12
- `roofs_gated_on_coverage`: 285
- `statement`: 12 of the 297 remaining roofs stand on ground this project has already surveyed, platted and modelled. The other 285 have nowhere to go until street control, terrain and hydrology reach them. The binding constraint on the 668-roof programme is coverage, not recipes.

| bucket | target | known | to do | filled | ticket |
|---|---:|---:|---:|---:|---|
| `ground/blk_west_fulton_des_plaines` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_fulton_jefferson` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_fulton_clinton` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_lake_des_plaines` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_lake_jefferson` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_lake_canal` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_randolph_des_plaines` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_randolph_jefferson` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_west_randolph_canal` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_michigan_st_tract_west_north` | 0 | — | — | 0 | T-1191, T-1193, T-1194 |
| `ground/blk_michigan_st_tract_west_south` | 0 | — | — | 0 | T-1191, T-1193, T-1194 |
| `ground/blk_michigan_st_tract_east_north` | 0 | — | — | 0 | T-1191, T-1193, T-1194 |
| `ground/blk_michigan_st_tract_east_south` | 0 | — | — | 0 | T-1191, T-1193, T-1194 |
| `ground/blk_wabansia_b_t1` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_c_t1` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_b_t2` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_c_t2` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_b_t3` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_c_t3` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_b_t4` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_b_t5` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_c_t5` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_b_t6` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_c_t6` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_b_t7` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
| `ground/blk_wabansia_c_t7` | 0 | — | — | 0 | T-1192, T-1193, T-1194 |
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
| **inns_and_taverns** — The model reads 15-15 inns and taverns; the programme schedules 10. | 15 | 10 | +5 |
| **institutional_and_public** — The model reads 9-19 institutional and public roofs; the programme schedules 9. | 19 | 9 | +10 |
| **people_per_roof** — 2,536 people under 668 roofs is the ratio the completed town must meet; the census's own reading for November 1835 is 8.204 people per dwelling over 398 dwellings. | 2,536 | 668 | +0 |

## The invariants the convergence tickets assert

- **every_person_housed** (T-1215) — Every person in the layer — attested, inferred or reconstructed — is a member of a household or a lodging place that is seated on a roof. *Now:* 20 of 1256 present households name a lives_at.
- **every_working_person_has_a_workplace** (T-1189) — Every person carrying a trade, profession or employment has a workplace, or a stated `no fixed workplace`. *Now:* 49 of 1256 present households name a works_at.
- **every_business_has_staff** (T-1189) — Every business — attested, inferred or reconstructed — carries the staff T-1183's model implies for its kind. *Now:* not yet measurable: the authored business layer is T-1180.
- **every_structure_occupied_or_its_use_stated** (T-1197) — Every standing roof carries an occupant or a stated use. *Now:* 260 of 384 standing records carry no occupants block.
- **dwellings_ratio_within_its_bracket** (T-1215) — The town census's people-per-dwelling ratio is met within the model's bracket. *Now:* the book orders 2,536 people into 643 households.
- **an_uncompared_class_orders_nothing** (T-1442) — A trade-census class the crosswalk rules `compared: false` carries its figures but orders no reconstruction: the difference between a census line and the register is only a shortfall where the crosswalk has ruled the two comparable. *Now:* carried uncompared: 1 of 18 enumerated business classes, each ordering nought.
- **no_bucket_overfilled** (T-1166) — No bucket's `filled` exceeds its `to_reconstruct`; a filler that bypasses the book is red in check.sh. *Now:* enforced by --check on every gate run.
