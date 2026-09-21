# The ground the 26 moving roof ids stand on — July 1835

DERIVED — regenerate with `tools/measure_roof_id_migration.py --build`. T-1483.

T-1445 returned 32 refamily verdicts; T-1451 carried out the 6 whose record id does not encode its family. These are the other 26. Each becomes a new id the moment its family moves, and the id is named across the tree. NOTHING IS MOVED HERE: this is the measurement the three carry-out tickets (T-1481 south, T-1482 the platted blocks, T-1484 north) each stand on.

- roofs whose id moves: **15**
- files that name one: **58**
- of those, **1** hold a reference a rename would falsify, **15** rename, **38** are re-derived by their own tool, **4** are frozen records of a past run

## The rows that cost judgement

A reference is not always a pointer. These assert what the roof IS, and the verdict moves it out of that — so a carry-out has to resolve them, not rename them. This is the list a scripted rename would have passed over.

| file | where | roof | group | becomes | why it is not a rename |
| --- | --- | --- | --- | --- | --- |
| `data/reconstruction/1835_inferred_household_programme.json` | `.households[33].works_at` | `recon_1835_north_w2_005` | workshops | ordinary_dwellings | `works_at` needs a workplace and ordinary_dwellings is not one |
| `data/reconstruction/1835_inferred_household_programme.json` | `.households[58].works_at` | `recon_1835_north_c1_020` | stores_mixed_use | ordinary_dwellings | `works_at` needs a workplace and ordinary_dwellings is not one |
| `data/reconstruction/1835_inferred_household_programme.json` | `.households[59].works_at` | `recon_1835_north_c2_027` | stores_mixed_use | ordinary_dwellings | `works_at` needs a workplace and ordinary_dwellings is not one |
| `data/reconstruction/1835_inferred_household_programme.json` | `.households[61].works_at` | `recon_1835_north_c1_047` | stores_mixed_use | barns_stables | `works_at` needs a workplace and barns_stables is not one |
| `data/reconstruction/1835_inferred_household_programme.json` | `.households[62].works_at` | `recon_1835_north_w1_018` | workshops | ordinary_dwellings | `works_at` needs a workplace and ordinary_dwellings is not one |

**5** reference(s), across 1 file(s).

## Every moving roof, and what names it

| roof | becomes | renamed | re-derived | frozen | adjudicated |
| --- | --- | ---: | ---: | ---: | ---: |
| `recon_1835_blk_randolph_market_a1_07` | `recon_1835_blk_randolph_market_d4_07` | 2 | 7 | 2 | 0 |
| `recon_1835_blk_randolph_market_a1_12` | `recon_1835_blk_randolph_market_d4_12` | 0 | 7 | 2 | 0 |
| `recon_1835_blk_randolph_market_a3_05` | `recon_1835_blk_randolph_market_d2_05` | 0 | 7 | 2 | 0 |
| `recon_1835_blk_randolph_market_a4_06` | `recon_1835_blk_randolph_market_d2_06` | 0 | 7 | 2 | 0 |
| `recon_1835_blk_south_water_lasalle_a1_06` | `recon_1835_blk_south_water_lasalle_d3_06` | 1 | 8 | 2 | 0 |
| `recon_1835_blk_south_water_wells_a1_07` | `recon_1835_blk_south_water_wells_d1_07` | 0 | 7 | 2 | 0 |
| `recon_1835_north_c1_020` | `recon_1835_north_d3_020` | 2 | 8 | 4 | 1 |
| `recon_1835_north_c1_047` | `recon_1835_north_a1_047` | 0 | 7 | 4 | 1 |
| `recon_1835_north_c2_027` | `recon_1835_north_d6_027` | 0 | 9 | 4 | 1 |
| `recon_1835_north_f1_022` | `recon_1835_north_h2_022` | 2 | 8 | 4 | 1 |
| `recon_1835_north_h3_045` | `recon_1835_north_h2_045` | 4 | 14 | 4 | 1 |
| `recon_1835_north_i2_015` | `recon_1835_north_d4_015` | 5 | 10 | 4 | 0 |
| `recon_1835_north_t1_028` | `recon_1835_north_h2_028` | 2 | 13 | 4 | 1 |
| `recon_1835_north_w1_018` | `recon_1835_north_d4_018` | 0 | 10 | 4 | 1 |
| `recon_1835_north_w2_005` | `recon_1835_north_d4_005` | 0 | 9 | 4 | 1 |

## Renamed — 15 file(s)

A plain pointer at the record. The migration rewrites the string and nothing else is owed.

| file | roofs | why |
| --- | ---: | --- |
| `data/businesses/authored/rcb_cavanagh_boarding_house.json` | 1 | a plain pointer at the record |
| `data/residents/lodgers/hh_lodging_recon_1835_north_h3_045.json` | 1 | a plain pointer at the record |
| `data/residents/lodgers/hh_lodging_recon_1835_north_t1_028.json` | 1 | a plain pointer at the record |
| `docs/RESEARCH/business-naming-1835.md` | 1 | a plain pointer at the record |
| `docs/RESEARCH/civic_public_buildings_1835.md` | 1 | a plain pointer at the record |
| `docs/STATUS.md` | 2 | a plain pointer at the record |
| `docs/STREET-FACE-ADOPTION.md` | 1 | a plain pointer at the record |
| `tools/compile_register.py` | 1 | a plain pointer at the record |
| `tools/execute_roof_redeal.py` | 1 | a plain pointer at the record |
| `tools/measure_group_district_rows.py` | 1 | a plain pointer at the record |
| `tools/measure_institutional_claims.py` | 1 | a plain pointer at the record |
| `tools/measure_ridge_reach.py` | 1 | a plain pointer at the record |
| `tools/measure_roof_id_migration.py` | 2 | a plain pointer at the record |
| `tools/smoke_renderer.mjs` | 1 | a plain pointer at the record |
| `tools/step_isolation.json` | 2 | a plain pointer at the record |

## Re-derived — 38 file(s)

Written by a tool, which `check.sh` re-runs. The migration must NOT hand-edit these; it re-runs the tool and commits what comes out.

| file | roofs | why |
| --- | ---: | --- |
| `data/businesses/index.json` | 1 | DERIVED, NEVER AUTHORED |
| `data/enclosures/town_lot_line_boards.json` | 1 | generated_by tools/generate_lot_line_fences.py |
| `data/enclosures/town_lot_line_pickets.json` | 2 | generated_by tools/generate_lot_line_fences.py |
| `data/enclosures/town_lot_line_rails.json` | 4 | generated_by tools/generate_lot_line_fences.py |
| `data/liberties.json` | 9 | compiled from docs/LIBERTIES.md by tools/compile_liberties.py |
| `data/reconstruction/1835_building_inventory.json` | 1 | Authored reconstruction programme |
| `data/reconstruction/1835_business_reconstruction.json` | 2 | DERIVED from the reconstruction order book and the resident band's trade heads by tools/reconstruct_businesses_1835 |
| `data/reconstruction/1835_hay_limits.json` | 1 | Derived |
| `data/reconstruction/1835_lodgers_seated.json` | 2 | DERIVED |
| `data/reconstruction/1835_lodging_model.json` | 2 | DERIVED |
| `data/reconstruction/1835_roof_redeal.json` | 15 | DERIVED — regenerate with tools/redeal_anonymous_roofs |
| `data/research/land_sales/ground.json` | 15 | generated_by tools/resolve_land_tracts.py --build |
| `data/research/newberry_index/lead_crosswalk.json` | 3 | GENERATED |
| `data/research/newberry_index/leads.json` | 3 | GENERATED |
| `data/residents/employment_coverage.json` | 2 | DERIVED — regenerate with tools/employment_coverage_1835 |
| `data/residents/reconstructed_seating.json` | 2 | DERIVED — regenerate with tools/seat_reconstructed_trades_1835 |
| `data/sidecars/1835/index.json` | 15 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/people.json` | 2 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_blk_randolph_market_a1_07.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_blk_randolph_market_a1_12.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_blk_randolph_market_a3_05.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_blk_randolph_market_a4_06.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_blk_south_water_lasalle_a1_06.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_blk_south_water_wells_a1_07.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_c1_020.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_c1_047.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_c2_027.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_f1_022.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_h3_045.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_i2_015.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_t1_028.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_w1_018.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/sidecars/1835/recon_1835_north_w2_005.json` | 1 | compiled from the structure records by tools/compile_scene.py --all |
| `data/signage/town_business_signboards.json` | 2 | The town's business signs |
| `data/yard/town_trade_goods.json` | 1 | Goods standing on the town's own ground — barrels and cases on the footway at the taverns and the stores, the bench against the Green Tree's front wall, the open-sided wagon shed a |
| `docs/RESEARCH/1835_anonymous_roof_redeal.md` | 15 | DERIVED — regenerate with `tools/redeal_anonymous_roofs |
| `docs/RESEARCH/1835_roof_redeal_execution.md` | 15 | DERIVED — regenerate with `tools/execute_roof_redeal |
| `tools/north_bank_frontage_baseline.json` | 1 | T-0947 |

## Frozen — 4 file(s)

A record of something that already happened. The id it names was the id at the time; rewriting it would make a receipt claim to have seen a building that did not exist under that name.

| file | roofs | why |
| --- | ---: | --- |
| `data/research/residents/synthesis_full_gate_after_fixes.log` | 9 | a log of a gate run on a dated tree — it recorded what it saw |
| `docs/LIBERTIES.md` | 9 | append-only by its own rule; a liberty already taken is not rewritten, and the migration appends a new entry instead |
| `docs/unreal/prototype/import_report.json.txt` | 15 | an import report from a dated Unreal prototype run |
| `renderers/unreal/receipts/mac-253f02657.json` | 15 | per-machine import receipts — each records one dated run on one tree |

## Adjudicated — 1 file(s)

Listed above with the reference that has to be resolved.

| file | roofs | why |
| --- | ---: | --- |
| `data/reconstruction/1835_inferred_household_programme.json` | 8 | a reference here asserts what the roof is, and the verdict moves it out of that |

