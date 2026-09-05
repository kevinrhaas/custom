# What the residents and households look like — September 2026

**Ticket:** T-0517 · **Data:** `data/residents/`, `data/town_census.json`,
`data/research/residents/identity_master.json` ·
**Dossier:** `docs/RESEARCH/residents_1835.md` (the model; this file is the measurement) ·
**Scene date:** 1835-07-01

**The owner's ask, 2026-09-03, verbatim:** *"then i would like a summary of what the residents
and households look like, since you have good census data now on many you should be able to
improve that."*

---

## How to read this file

**Every figure below carries the command that produced it, and the command is the authority.**
The tool is `tools/residents_summary.py`; it reads only committed records and writes nothing.
Numbers in this file were taken on **2026-09-05** against `dev`. When they disagree with the
tool, the tool is right and this file is stale — re-run it and correct the prose.

```
tools/residents_summary.py --list       the section names
tools/residents_summary.py --all        every section, in the order of this document
```

This project has already lost one document to a pasted snapshot: `residents_1835.md` sat for a
month printing "72 households, 96 person entries" while the layer grew past 1,300. The section
commands are the fix, and they are not decoration.

---

## 1. The size of the layer

```
python3 tools/residents_summary.py --section totals
```

| | count | of persons |
|---|---:|---:|
| **households** (one record file each) | **1,380** | |
| **persons** (entries inside them) | **1,404** | |
| grade `attested` | 509 | 36.3% |
| grade `inferred` | 895 | 63.7% |
| grade `reconstructed` | 0 | 0.0% |
| subtype `projected_resident` | 784 | 55.8% |
| `letter_list_only` | 727 | 51.8% |
| `civic_mint` | 531 | 37.8% |
| `later_census` (1840-linked) | 3 | 0.2% |
| carries a `resident_research` row | 849 | 60.5% |

`index.json`'s denormalised counts agree with the records; the section says `AGREES` or
`DRIFTED` and the validator fails the build on drift, so the manifest is never the thing to
doubt.

**The one number to hold on to: 1,404 named people against a town of 3,265.** That is 43.0% of
the November 1835 town census by name — a genuinely large fraction of a frontier town's
population recovered by name — and it sits beside a placement figure of 1.4% (§4). *This layer
knows who was here far better than it knows where they were.*

## 2. Where they are, and whether they were here on the day

```
python3 tools/residents_summary.py --section division
```

| division | households | |
|---|---:|---:|
| `unplaced` | 1,308 | 94.8% |
| south | 52 | 3.8% |
| north | 11 | 0.8% |
| west | 6 | 0.4% |
| fort | 2 | 0.1% |
| outside_town | 1 | 0.1% |

| present on 1835-07-01 | households | |
|---|---:|---:|
| `uncertain` | 893 | 64.7% |
| `present` | 486 | 35.2% |
| `absent` | 1 | 0.1% |

The presence claim is graded `inferred` on 1,354 households, `attested` on 21 and
`reconstructed` on 5. **That asymmetry is the layer working as designed**: `present` at
`inferred` usually means a letter was still waiting at the post office on or after the scene
date, which puts a correspondent's belief at Chicago and not a body.

| placement | households | |
|---|---:|---:|
| `lives_at` names a structure | 20 | 1.4% |
| `works_at` names a structure | 50 | 3.6% |
| neither | 1,325 | 96.0% |

## 3. Sex

```
python3 tools/residents_summary.py --section sex
```

Recorded on **98 of 1,404** persons (7.0%): 84 male, 14 female. Of those, 91 come from a source
that states it and **7 from a printed letter-list honorific alone** — and that column is only as
good as the compositor. `codding_sally` is set down in the Democrat of 1 July 1835 as
"Codding, Sally Mr" and carries `male` on that "Mr" and nothing else.

A further 13 persons have a `relationship` that implies a sex (8 `wife`, 4 `brother`, 1 `son`).
Recorded sex and implied sex disagree on **none**.

Low coverage is the expected shape of a layer built from lists of NAMED HEADS: a poll book, a
voter roll and a list of uncalled-for letters all print a name and no sex. It rises when the
1840 schedules are read into persons, because those print composition by age band and sex.

## 4. Occupation — what the town does for a living

```
python3 tools/residents_summary.py --section occupation
```

| | persons | |
|---|---:|---:|
| carries a named trade | **135** | 9.6% |
| `occupation: none_recorded` | 1,269 | 90.4% |
| no occupation block at all | 0 | 0.0% |

Of the 135, **127 are graded `attested`** and 8 `inferred`. **61 distinct trades** are named.
The commonest: attorney 11, tavern_keeper 8, merchant 7, schoolteacher 6, carpenter 5,
blacksmith 5, physician 5, hotel_keeper 4, forwarding_and_commission 4, dry_goods_merchant 4.

Which source stands behind a trade (a trade may cite more than one):

| source | trades | |
|---|---:|---:|
| `andreas_1884_v1` | 76 | 56.3% |
| `chicago_democrat_1833_1835` | 43 | 31.9% |
| `chicago_democrat_1833_11_26` | 15 | 11.1% |
| `chicago_american_1835` | 5 | 3.7% |
| `drloih_hotels` | 4 | 3.0% |
| 13 further sources | 1–2 each | |

**The occupation layer is Andreas plus the newspapers, and almost nothing else**: 128 of the
135 people with a trade (94.8%) get it from one of those four sources. That is the sharpest
single finding in this file, because the directories — Fergus 1839 and 1843, Norris 1844 —
print a trade beside nearly every name they carry, and between them they stand behind **187
persons' identity** while standing behind **one** person's trade (`legg_gregory_e`). The
trades are in the corpus already, read, crosswalked and adjudicated, and unspent.

## 5. Household size

```
python3 tools/residents_summary.py --section size
```

| persons in the record | households | |
|---|---:|---:|
| 1 | 1,360 | 98.6% |
| 2 | 17 | 1.2% |
| 3 | 2 | 0.1% |
| 4 | 1 | 0.1% |

Mean 1.02. The largest are `hh_temple_john_t` (4), `hh_beaubien_jean_baptiste` (3),
`hh_robinson_alexander` (3).

**A household of one is not a man living alone.** It is a household whose head is the only
person a source names. The town counted 3,265 people in 398 dwellings — 8.2 to a dwelling — so
this distribution measures the reading, not the town, and it is the cleanest illustration in the
project of what "the sources print heads" costs a reconstruction.

## 6. Evidence coverage, by domain

```
python3 tools/residents_summary.py --section evidence
```

The section holds its own domain table against the layer before printing: it discovers every
`*_evidence` key present on a person and **refuses to run** if the table names one that is
absent or misses one that is there.

| domain | key | persons reached | |
|---|---|---:|---:|
| newspaper | `person.press_evidence` | 413 | 29.4% |
| directory | `household.directories` | 330 | 23.5% |
| civic | `person.civic_evidence` | 215 | 15.3% |
| book | `person.book_evidence` | 144 | 10.3% |
| church | `person.church_evidence` | 38 | 2.7% |
| census_1840 | `person.census_evidence` | 26 | 1.9% |
| biographical | `person.biographical_evidence` | 2 | 0.1% |
| **census_1830** | **no key exists** | **0** | **0.0%** |

**The 1830 domain has reached no card at all.** Chicago was enumerated in Peoria County in 1830
and the named schedule is read in `data/research/census_1830/`; not one ruling from it has been
carried to a person, and no person cites
`census_1830_peoria_county_chicago_precinct`. The section proves the absence rather than
printing a tidy zero — if that source ever appears on a card, it says so and asks for a key.

| domains behind one person | persons | |
|---|---:|---:|
| 0 | 674 | 48.0% |
| 1 | 467 | 33.3% |
| 2 | 123 | 8.8% |
| 3 | 107 | 7.6% |
| 4 | 31 | 2.2% |
| 5 | 2 | 0.1% |

The largest overlaps: newspaper ∩ directory 151, book ∩ directory 120, newspaper ∩ book 108,
civic ∩ directory 82, newspaper ∩ civic 58, civic ∩ book 54.

**Every one of the six largest overlaps involves the newspaper or the directories.** Those are
the two domains that print a trade and an address beside a name, which is why §4's finding and
§2's placement figure are the same finding seen twice.

Source ids on `persons[].sources` — 46 distinct, the top of the tail:

| source | persons | |
|---|---:|---:|
| `chicago_democrat_1833_1835` | 1,035 | 73.7% |
| `chicago_voter_lists_1833_1835_irad` | 255 | 18.2% |
| `fergus_chicago_directory_1843` | 102 | 7.3% |
| `chicago_american_1835` | 102 | 7.3% |
| `fergus_chicago_directory_1839` | 99 | 7.1% |
| `andreas_1884_v1` | 91 | 6.5% |
| `norris_directory_1844` | 85 | 6.1% |

**1,063 persons (75.7%) rest on one source id**, 338 on two or more, 3 on none.

## 7. The layer beside the town it reconstructs

```
python3 tools/residents_summary.py --section town
```

`data/town_census.json` is DERIVED (`tools/town_census.py`, re-derived by `check.sh`):

| | |
|---|---:|
| the town of November 1835, as Andreas prints it | 3,265 people in 398 dwellings |
| persons this layer HOUSES in a standing building | 29 |
| households housed | 20 |
| households with no dwelling | 1,360 |
| buildings standing in the scene | 359 of 662 |

**Named: 43.0% of the town. Housed: 0.9%.** Those two numbers are the state of the programme in
one line.

`data/research/residents/identity_master.json`, the ledger behind them: 6,707 identities,
10,399 appearances, **1,395 identities on a card**, 1,589 identities in two or more domains,
304 declared merges, 1,578 declared refusals, 1,881 derived refusals.

**1,589 identities are corroborated across two or more domains and 1,395 are on a card.** The
ledger is not far ahead of the layer on *identity*; it is far ahead of it on *attributes*, which
is what §4 measures.

## 8. What changed since PR #668 (2026-09-02)

```
python3 tools/residents_summary.py --section baseline
```

The baseline is a literal table inside the tool — the only place those numbers are written down,
so drift is measured rather than remembered.

| | #668 | now | change |
|---|---:|---:|---:|
| households | 824 | 1,380 | **+556** |
| persons | 848 | 1,404 | **+556** |
| grade `attested` | 117 | 509 | **+392** |
| grade `inferred` | 731 | 895 | +164 |
| `projected_resident` | 706 | 784 | +78 |

**Read it as two independent movements, not one net figure.** `attested` rising by 392 against
556 new persons is the civic sweep MINTING corroborated people, not regrading the ones already
there. `projected_resident` is the letter-list floor; it falls only when a second source reaches
a name, and it rose because the letter lists kept being read.

## 9. What remains unresearched or unresolved

```
python3 tools/residents_summary.py --section gaps
```

| persons | count | |
|---|---:|---:|
| rests on ONE source id | 1,063 | 75.7% |
| no trade | 1,269 | 90.4% |
| no sex recorded | 1,306 | 93.0% |
| no 1840 linkage | 1,401 | 99.8% |
| rests on the letter lists alone | 727 | 51.8% |
| no `resident_research` row | 555 | 39.5% |
| no source id at all | **3** | 0.2% |

| households | count | |
|---|---:|---:|
| division `unplaced` | 1,308 | 94.8% |
| no `lives_at` | 1,360 | 98.6% |
| no `works_at` | 1,330 | 96.4% |
| no `origin` | 1,363 | 98.8% |
| no `reason_for_coming` | 1,355 | 98.2% |
| no `party_size_on_arrival` | 1,368 | 99.1% |
| `review_required` | 8 | 0.6% |
| `touches_removal` | 8 | 0.6% |

Arrival precision: `not_later_than` 1,318 (95.5%), year 45, month 6, day 6, season 5. The layer
can say *by when* almost every household was here and *when* almost none of them came — the
direct consequence of the commonest evidence being an act performed at Chicago on a date.

**The three persons with no source id of their own are the only outright contract gap in the
list**; everything else above is honestly-recorded absence, which is what this project asks for.

---

## 10. The report — five paragraphs for the owner

**The town has its people.** 1,380 households and 1,404 named persons, against a town census of
3,265 — 43% of Chicago in the summer of 1835 recovered by name, from a corpus that in phase one
yielded 96. 509 of those people are `attested`: corroborated well enough that the project will
stand behind them as real named residents. Nothing in the layer is graded `reconstructed`; the
vocabulary keeps the word and the data does not use it, which is the state we wanted.

**What it does not have is where they lived.** Twenty households — 1.4% — name a building they
live in. Fifty name a premises they work at. 1,308 of 1,380 sit in division `unplaced`. The
layer houses 29 people in a standing structure out of 3,265; the walkable town is still a town
of roofs with almost nobody assigned to them. **This, and not more reading, is the gap between
the dataset and the scene.**

**The trades tell the same story, and they tell it about work already done.** 135 people carry
an occupation and 1,269 do not; 128 of those 135 get it from Andreas or a newspaper. Meanwhile
Fergus 1839, Fergus 1843 and Norris 1844 stand behind **187 people's identity** — read,
crosswalked and adjudicated — and behind **exactly one** person's trade. Those directories
print a trade and very often a street beside each name. **The most valuable material
in the project right now is not on a shelf; it is in `data/research/directories/`, ruled on and
unspent.**

**The evidence is thin under most people and thick under a few.** 1,063 persons (76%) rest on a
single source id, 727 on the post-office letter lists alone, and 674 have no domain evidence
block at all. At the other end, 140 persons are corroborated across three or more domains. The
identity ledger holds 1,589 identities corroborated in two or more domains against 1,395 on a
card — so the ledger is roughly level with the layer on *who*, and far ahead of it on *what is
known about them*. Reading a new volume moves the first number. Spending what is adjudicated
moves the second, and the second is where the town is short.

**The recommendation is the placement sweep, and it should run before any new source is
opened.** Take the directories' printed addresses — the `res`/`bds` forms for homes, the shop
addresses for premises — position the household or the business against the plat under
`inferred` with the later date stated in the note, and let the 1840 schedules supply composition
where a bridge is validated rather than provisional (3 persons today, out of 26 with 1840
evidence). Every one of those moves takes a number in §2 or §4 off its floor without reading a
page. The measurements to watch afterwards are the two in §7: **named 43.0%, housed 0.9%.** The
first is the achievement. The second is the work.

---

## Notes on scope

- **`docs/RESEARCH/residents_1835_inferred.md` is stale in the same way this file's companion
  was** — it documents an earlier state of the inferred layer. T-0517 deliberately does not
  rewrite it; it is named here so the next run finds it.
- **`docs/RESEARCH/resident-household-synthesis-2026-09-02.md`** is the receipt for one day's
  sweep and remains accurate as a receipt. It is not a description of the model.
- The final audit that brackets this programme is
  `chicago/reference/resident-research/final/audit/` (T-0512), regenerated in the same PR as
  this file; `tools/export_resident_audit.py --report` prints its metrics.
