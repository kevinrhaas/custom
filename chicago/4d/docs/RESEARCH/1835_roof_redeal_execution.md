# The anonymous-roof redeal, carried out — July 1835

DERIVED — regenerate with `tools/execute_roof_redeal.py --apply`. T-1451.

T-1445 adjudicated 285 anonymous roofs and moved none of them. This is the execution: the verdicts carried back into the authored recipes so the generators re-derive the records. It adjudicates nothing — every family below is the `to_family` T-1445 reached.

- refamily verdicts standing: **32**
- carried out here: **6** (the West Division parcel)
- outstanding, and why: **26** — the record id carries the family, so executing them renames a roof other files name (T-1452)
- retired: **0** — the guard stands empty and that is a measurement, not an omission

## Carried out

| roof | was | now | group | footprint ft | why |
| --- | --- | --- | --- | --- | --- |
| `recon_1835_west_008` | W1 | D4 | workshops → ordinary_dwellings | 20x28 | the placement policy refuses this family here — stands 3.81 m off the street line (2.71 m), and mechanics_streets puts it on the line; the slot is wanted and the position stands |
| `recon_1835_west_009` | W2 | D5 | workshops → ordinary_dwellings | 20x30 (was 20x32) | the placement policy refuses this family here — stands on a light street, which mechanics_streets avoids; the slot is wanted and the position stands |
| `recon_1835_west_010` | A1 | D3 | barns_stables → ordinary_dwellings | 16x24 | the placement policy refuses this family here — stands on a principal street, which ancillary_behind_its_own_roof avoids; the slot is wanted and the position stands |
| `recon_1835_west_011` | A3 | D2 | small_outbuildings → ordinary_dwellings | 12x16 (was 5x6) | the placement policy refuses this family here — stands on a principal street, which ancillary_behind_its_own_roof avoids; the slot is wanted and the position stands |
| `recon_1835_west_021` | W3 | D6 | workshops → ordinary_dwellings | 22x33 (was 22x34) | the placement policy refuses this family here — stands 30.47 m off the street line (2.71 m), and mechanics_streets puts it on the line; the slot is wanted and the position stands |
| `recon_1835_west_022` | W4 | A1 | workshops → barns_stables | 18x26 | the placement policy refuses this family here — stands on a light street, which mechanics_streets avoids; the slot is wanted and the position stands |

## Outstanding — the id migration T-1452 owns

Each of these becomes a new id when its family moves, and the id is not private to its record. The files below name it today and would point at a roof that no longer exists. Counted over the committed tree; a record's own `data/structures/<id>.json` is not listed.

| roof | becomes | files that name it |
| --- | --- | ---: |
| `recon_1835_blk_randolph_market_a1_07` | `recon_1835_blk_randolph_market_d4_07` | 4 |
| `recon_1835_blk_randolph_market_a1_12` | `recon_1835_blk_randolph_market_d4_12` | 4 |
| `recon_1835_blk_randolph_market_a3_05` | `recon_1835_blk_randolph_market_d2_05` | 4 |
| `recon_1835_blk_randolph_market_a4_06` | `recon_1835_blk_randolph_market_d2_06` | 4 |
| `recon_1835_blk_south_water_lasalle_a1_06` | `recon_1835_blk_south_water_lasalle_d3_06` | 5 |
| `recon_1835_blk_south_water_wells_a1_07` | `recon_1835_blk_south_water_wells_d1_07` | 4 |
| `recon_1835_north_c1_020` | `recon_1835_north_d3_020` | 5 |
| `recon_1835_north_c1_047` | `recon_1835_north_a1_047` | 5 |
| `recon_1835_north_c2_027` | `recon_1835_north_d6_027` | 7 |
| `recon_1835_north_f1_022` | `recon_1835_north_h2_022` | 6 |
| `recon_1835_north_h3_045` | `recon_1835_north_h2_045` | 13 |
| `recon_1835_north_i2_015` | `recon_1835_north_d4_015` | 7 |
| `recon_1835_north_t1_028` | `recon_1835_north_h2_028` | 11 |
| `recon_1835_north_w1_018` | `recon_1835_north_d4_018` | 8 |
| `recon_1835_north_w2_005` | `recon_1835_north_d4_005` | 7 |
| `recon_1835_south_c1_003` | `recon_1835_south_d1_003` | 8 |
| `recon_1835_south_c1_010` | `recon_1835_south_d1_010` | 5 |
| `recon_1835_south_c1_018` | `recon_1835_south_d1_018` | 5 |
| `recon_1835_south_c2_007` | `recon_1835_south_d5_007` | 9 |
| `recon_1835_south_c2_036` | `recon_1835_south_d6_036` | 10 |
| `recon_1835_south_c3_037` | `recon_1835_south_a2_037` | 6 |
| `recon_1835_south_f2_039` | `recon_1835_south_h2_039` | 6 |
| `recon_1835_south_w1_023` | `recon_1835_south_d5_023` | 10 |
| `recon_1835_south_w2_026` | `recon_1835_south_d4_026` | 10 |
| `recon_1835_south_w3_029` | `recon_1835_south_h1_029` | 8 |
| `recon_1835_south_w4_032` | `recon_1835_south_d1_032` | 10 |

The three platted-block roofs among them carry a second difficulty the West parcel does not: they are `ancillary` slots whose new family is a dwelling, and `generate_block_infill` gates a block's principal/ancillary split against its claimed schedule and refuses a second principal roof on one lot. That is a re-deal of the block, not a field edit.

