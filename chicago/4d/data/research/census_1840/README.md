# `census_1840` — the 1840 federal census of Chicago, read off the page images

**This is LATER EVIDENCE.** Nothing in this directory mints an 1835 resident. The
project's ratified ladder is explicit: *1839/1840 alone is never a 1835 resident.*
What is read here is a named 1840 household head with a line position; the bridge to
1835 is a separate, adjudicated step (T-0505), and the minting is a separate one again
(T-0514, T-0515).

## What the deposit holds

`chicago/reference/census1840/` holds **74 distinct** FamilySearch page images in 75 files —
`33S7-9YYJ-9WF (1).jpg` is a byte-identical copy of `33S7-9YYJ-9WF.jpg`. (The tickets, the source
record and this file all said 75 distinct in 76 files; `ls *.jpg | wc -l` is 75 and `md5sum *.jpg |
awk '{print $1}' | sort -u | wc -l` is 74, so the count was one too many and the third image group is
51-74, not 51-75.) The deposit is **read only**: no image, crop or render is ever committed. Only
derived text is.

The sheets come in two kinds and both are numbered in the same run of printed pages:

| kind | what it carries |
|---|---|
| **left sheet** | `NAMES OF HEADS OF FAMILIES`, then 13 free-white male and 13 free-white female age bands, then free coloured males and females |
| **right sheet** | the continuation: slaves, the family TOTAL, the six industry columns, pensioners, deaf/dumb/blind, and schools & illiteracy |

A household is one ruled line spanning both, so a name and its own household figures
live on two different images.

## What is in here

| file | what it is |
|---|---|
| `coverage.json` | exactly which images have been looked at, what each one is, and what has and has not been read from it. A hole is meant to FAIL rather than pass quietly. |
| `pages/<familysearch_id>.json` | one file per page read: the printed page number, the sheet side, and one record per ruled line — `line`, `as_read`, `normalized`, `name_confidence`, `reading`. |
| `crosswalk_670.json` | the line-by-line comparison against the 210 rows PR #670 recovered from the owner's lost v4 workbook, page by page, with a row-offset test on each. |
| `claims.json` | what the sheets say ABOUT the enumeration and about the town, as opposed to who they name. Hand-authored, each with its verbatim quote and locator. |

## The reading rules

- **`as_read` is a POSITION-PRESERVING reading.** An unread letter is `[?]` — a position,
  not an absence (T-0397). `normalized` is the modern spelling this project would use;
  where the surname itself is unread, `normalized` keeps the `[?]` rather than inventing a
  name that scans well.
- **`name_confidence` is `high | medium | low`** and is about the LETTERS, not about who
  the person was. A name can be read with confidence and still belong to nobody this
  project can identify.
- **`reading: scan_verified`** means it was read off the deposited page image. It is the
  senior reading: where a transcription and the sheet disagree, the sheet wins and both
  are kept.
- **Enumeration order is data.** The line sequence is the only spatial signal the 1840
  census carries — households were visited in walking order — so lines are never
  reordered and a blank or illegible line is recorded, never skipped.
- **No IPUMS serial is attached here.** The serial mapping is by age-band fingerprint and
  is T-0504's job, over all three image groups at once.

## The finding this pass exists to record

PR #670 recovered 210 named household heads from the owner's v4 workbook, which he has
since ruled lost — "They are lost; rebuild". Those 210 rows are the calibration set any
new reading must reproduce before it extends. **Five of the seven pages they cover have
now been read off the sheets, and they do not reproduce.**

| printed page | image | scan lines | #670 rows | agree on both names |
|---|---|---|---|---|
| 229 | `33S7-9YYJ-9M5` | 30 | 31 | 2 |
| 230 | `33S7-9YYJ-NY` | 31 | 31 | see `crosswalk_670.json` |
| 231 | `33S7-9YYJ-38` | 31 | 31 | 0 |
| 232 | `33S7-9YYJ-W6` | 31 | 31 | see `crosswalk_670.json` |
| 234 | `33S7-9YYJ-99F` | 31 | 31 | 4 |

Some of the disagreements are large: page 232 line 17 reads *Gurdon S. Hubbard* on the
sheet against *Saml. J. McCord?* in #670, and line 25 reads *John H. Kinzie* against
*John W. Rogers?* — two of the most consequential names in the town.

**Two different faults are present, and they want telling apart.** `crosswalk_670.json`
runs a `row_offset_test` on every page: how many of that page's scan lines find any
name-part agreement with the #670 row one or two places away. Page 234 peaks at offset 0
(16 partial hits against 3 at −1): the rows are aligned and the READINGS differ. Page 231
peaks at offset −1 (11 hits against 5 at 0): #670's rows are DRIFTED one place down that
page, so *Patteson Nickalls* at #670 row 12 is the sheet's line 11, and *John Leonard* at
row 27 is line 26. Page 230's tail shows the same drift shape. Page 229 is a third case
again: the sheet carries **30** ruled entries and #670 carries **31 rows** for it, so at
least one #670 row on that page has no line to sit on.

`crosswalk_670.json` carries every line of it. **Nothing in #670 was overwritten** — both
readings stand, with the reason the scan is treated as senior stated on each line. What
this means for T-0504 and T-0505 is that the 210 rows cannot be used as ground truth for
a serial fingerprint or an identity bridge until they have been re-read against the
images, and that a bridge built on #670's row NUMBERS is unsafe on at least page 231.

## Two pages in this deposit are not household pages

`33S7-9YYJ-95F`, printed page **206**, is a printed left sheet used as the enumeration's
**certificate and recapitulation**: no household lines, and a manuscript note that names
Assistant Marshal **S. W. Sherman** as the man who took Cook County, is certified by a
signature reading *Mary Prittyman*, and records the book's two recapitulations —
population 3850, **4470 — City of Chicago**, 8320. The addition is internally consistent,
and 4,470 is the published 1840 figure for the city. It is transcribed in full in
`pages/33S7-9YYJ-95F.json` and its town findings are claims in `claims.json`. It is still
LATER EVIDENCE: it fixes the size of the town five years after the scene and may not be
extrapolated back to 1835.

`33S7-9YYJ-C8`, printed page **238**, is printed, numbered and wholly unfilled. A
swept-and-empty page is evidence, which is why coverage declares it rather than omitting
it.

## The cells, and what the sheet's own footings say about them

Both calibration pages are now read to the cell. Every one of the 62 lines carries all 38
columns of its left sheet — 13 free white male age bands, 13 free white female, 6 free
coloured male and 6 free coloured female — as integers in the sheet's own order, under
`records[].cells`. A blank cell on the schedule IS a zero and is recorded as one; no line
was skipped and none is `illegible`.

**How the columns were fixed, because it is the whole risk.** These are 38 narrow columns
of single strokes and a mark read one column off is a person of the wrong age. The rules
were located per line from the image's own darkness profile rather than from a fixed grid,
which matters: the ruling on `33S7-9YYJ-NY` leans about 36 px between line 1 and line 31,
so a grid measured in the middle of the sheet puts the top and bottom lines a quarter of a
column out. Every column carrying a mark was then read a second time as a montage of its
own 31 cells; that second pass is what caught four counting slips in the first.

**The check is the enumerator's own arithmetic.** Each sheet foots its columns at the
bottom, and `column_totals` states, per column, what the marks come to and what the footing
says. On these two pages **73 of the 76 columns reconcile exactly**, and the three that do
not are named rather than smoothed:

| page | column | marks | the sheet's footing |
|---|---|---|---|
| 230 | free white females, 5 and under 10 | 15 | 13 |
| 230 | free white females, 15 and under 20 | 3 | 5 |
| 232 | free white males, 20 and under 30 | 33 | 35 |

The two on page 230 **cancel**: 15 + 3 = 13 + 5, and the page's free white female total is
70 whichever reading is taken, so the page's free population is 151 both ways. That is what
a footing written into the wrong column looks like — but nothing on the sheet says so, and
neither reading is preferred here. Page 232 has no such cancellation: its free population is
193 by the marks and 195 by the footings.

Page 230's free coloured section is empty in all 12 columns with no figure in any footing.
Page 232 has four free coloured people, three of them on line 31 under a head this reading
gives as `Emanuel M[o]nd[?]`, and its footings — 1, 2, 1 and 1 — reconcile exactly.

## The continuation sheets, and what closing one costs

A continuation (right) sheet carries no name. It carries the other half of every household
line: the twelve slave columns, the family TOTAL, the seven industry columns, the pensioners,
the ten deaf/dumb/blind/insane columns and the seven schools columns — and, at the foot, the
enumerator's own printed totals for the columns he used. **Those footer totals are the gate.**
A continuation reading is committed only when the per-line values sum, column by column, to
what the man who took the census wrote at the bottom of his own sheet; where a column does not
close, the residual is recorded with it and no line is altered to make the total come out.

Three of group 1's eleven continuation sheets have been read on that rule (T-0540):

| image | lines | closes | page population | what it says |
|---|---|---|---|---|
| `33S7-9YYJ-24` | 31 | **all five columns** | 201 | agriculture 2, commerce 9, manufactures 27, learned professions 2 |
| `33S7-9YYJ-5D` | 31 | 4 of 6 | 125 | manufactures 25, canals 2, learned 1, and 1 school with 26 scholars; totals read 128 against 125 and commerce 2 against 3 |
| `33S7-9YYJ-5S` | 29 | **no — not committed** | 189 | 1 school with 42 scholars; the attempted reading is on the page file as an attempt, `cells` is null on every line |

**`33S7-9YYJ-5S` is the useful failure.** Its attempted reading sums to 183 persons against a
printed 189 AND 12 in agriculture against a printed 10. Two columns out by different amounts is
not two misread glyphs; it is the row indexing itself slipping over part of the sheet, and the
project's rule is that a half-read row is worse than an unread one. So the sheet's footer and
its exact line count — 29, not the 28 the inventory stated to the nearest line — are committed,
and the per-line reading is kept beside them as an ATTEMPT that nothing downstream can consume
as fact. The next run starts from it rather than from nothing.

**The cost is the other finding.** T-0535 asked for all eleven sheets plus the pairing, sized S.
It was split twice as the size was measured — into T-0538/T-0539, then T-0540/T-0541 — because a
sheet that closes takes something like ten passes at magnification, not one: this hand writes
`4` as two strokes that read as `11`, its `7` and `9` differ by a loop, and its two-digit family
totals sit hard against the column rule. Three sheets is a run.

**No continuation sheet here is paired to a left sheet yet.** A right sheet has neither a name
nor a printed page number on its exposure, so the pairing has to be earned: each page's
population (the TOTAL footer, published on each page file as `pairing.page_population_key`) has
to be matched against the printed age-band totals at the foot of each candidate left sheet, and
those have not been read. T-0539 does that for all eleven at once. Until then every one of them
is recorded as `unpaired` — never guessed.

## A line index for a sheet that has no lines (T-0565, `33S7-9YYJ-5V`)

`33S7-9YYJ-5V` is the sheet that stopped two passes. Its industry columns close against the
enumerator's own footings; its TOTAL column would not, and the reason recorded each time was
that **the leaf carries no horizontal ruled lines** — a row-darkness profile through the empty
slaves block finds exactly two rules on the whole leaf, under the heading and above the footer,
and nothing between them stands more than 4 grey levels over its background. With no grid to
count against, every row assignment was an opinion, and the page file would commit no line
number at all.

**The printed form is still ruled at a fixed pitch whether or not the rules survived the
exposure — and that pitch is measurable off columns that have nothing to do with the one in
question.** Twenty-two lines on this leaf are fixed by an entry in the mining, agriculture,
commerce, manufactures or learned-professions column. Fitted to those twenty-two anchors alone,
with the TOTAL column contributing nothing, the grid is

    y(k) = 670.29 + 75.856 k,   k = 0..29

with an rms of 5.8 px — 8 per cent of a line — and a worst residual of 15.5 px. Applied to the
TOTAL cell it puts all 44 of its ink components inside `k = 0..29`, none outside the range and
none unassigned. A 29-consecutive-line model with no empty slot was tested against the same
anchors and is worse by a factor of three; it is rejected. **The leaf carries 30 line slots and
29 of them carry a family.** That supersedes an inventory pass's 28 and the page file's own
"29 to 31, favouring 31" — the 31 was a count of glyph GROUPS, and two of those groups are the
two halves of one number.

Two things fall out of it that are worth carrying to the other ten sheets:

- **The anchor-offset test.** On the 21 lines where an industry entry and a TOTAL number both
  stand, the TOTAL number's y centre sits `+6.0 ± 6.3` px from the industry entry's. That is a
  measurement of two boxes on one line — no grid, no threshold — and it is decisive where the
  grid is not: at `k = 27` it accepts two groups 50 px apart as ONE number (`+1.0 sd`) and
  rejects either of them alone (`-3.5 sd`, `+4.5 sd`).
- **This sheet's `4` is not two strokes.** The section above records, from an earlier reading,
  that "this hand writes `4` as two strokes that read as `11`". On `5V` that is not so, and it
  matters, because three of the column's largest readings are paired slashes. The sheet's own
  `4` — in the commerce column at y834, on a column the footer calibrates at 27 — is a closed
  glyph with a bowl, a crossbar and a descender, and shares nothing with a pair of slashes.
  Each stroke of the paired groups is instead the identical tapered form of the single `1`s at
  `k = 14`, `k = 17` and `k = 21`. The `11`s are `11`. Whether that holds on the other ten
  sheets is a question for whoever reads them; it is stated here per sheet, not per deposit.

## The cells, and the rule that decides whether a column is committed (T-0532)

The age-band cells were read for the first time on printed pages **221, 222 and 226**.
Reading them at all needed a way to say WHICH column a mark is in that does not depend on
counting narrow rules by eye, so each page carries a `grid_note`: the 39 vertical rules are
fitted as a single pitch off the empty right-hand columns of the same image, and the fit is
**checked against the printed heading** — column 1 must read `Under 5`, column 27 `Under 10`
under FREE COLORED MALES — before a single cell is read. Every cell is then cut at that grid
and read as an image, one at a time. Nothing here is an OCR output.

**A column is committed only when it balances.** The lines this pass read must SUM to the
figure the enumerator wrote at the foot of the sheet; where they do not, the column is left
unreconciled with its residual stated, exactly as the ticket required, because a half-checked
column is worse than an unread one. So each page file carries two things per record:

| field | what it is |
|---|---|
| `cells` | the committed reading — only the columns whose page total balanced |
| `cells_first_pass` | the whole reading, balanced or not. **Not reconciled data.** It exists so the next reader starts from a reading rather than from the sheet. |

and `cells_column_check` states, per column, the read sum, the printed total, how confidently
that printed figure was read, whether it balanced, and the residual.

**Printed page 221 balances on 36 of its 38 columns** and is committed on those. The two that
do not are column 6 (free white males 30 under 40: read 10, printed 11) and column 15 (free
white females 5 under 10: read 11, printed 13) — one and two marks this pass did not find,
not a disagreement about what the sheet says.

**Printed 222 and 226 commit nothing, and the reason is the TOTALS and not the cells.** Both
sheets' footers are written across the foot rule and neither could be read to better than
`low` — so no column on them can be certified, whatever the cells say. What the page files do
record is that the read sums are *consistent with a plausible reading of the footer* on most
columns (`read_sum_matches_an_alternate_reading`), which is a lead for the next reader and is
explicitly not a balance. Re-read those two footers at higher magnification and most of both
pages should commit without the cells being touched.

## The 30-versus-31 question on printed page 229, settled (T-0534)

The most consequential thing in this directory is now settled, and it was settled by arithmetic
rather than by looking harder at the ruling. **Printed page 229 carries 30 household entries.**
PR #670 carries 31 rows for it. The test is the enumerator's own footings: on a page where the
column totals close, a 31st household has to put its people somewhere, and on 33S7-9YYJ-9M5 there
is nowhere left. **Seventeen of the nineteen columns that carry a mark close EXACTLY on the 30
lines read** — free white males 1-5, 7-10 and free white females 15-22 — against the figures
written at the foot of the sheet. So at least one of #670's 31 rows for that page has no line to
sit on, which is what `crosswalk_670.json`'s `row_offset_test` could only suspect. Nothing here
says which row is the intruder; that is a reading of #670, not of the sheet.

**A second finding sits beside it.** Line 26 of page 229 is a named head — the reading gives
`R. D. Coe` — with **no mark in any of the 38 columns**. A ruled, named line with a household of
nobody. It is not an artefact of the two columns that fail to balance: neither of them carries a
mark on line 26 either. It is recorded as it stands, an empty `cells` object on a named line.

## The cells of printed 229 and 231, and where the footings and the marks part company (T-0534)

Both pages are read to the cell on the T-0532 rule — a column is committed only where the lines
read SUM to the figure the enumerator footed — and **36 of 38 columns commit on each**. The four
that do not are named rather than smoothed:

| page | column | marks | the sheet's footing | what it looks like |
|---|---|---|---|---|
| 229 | free white males, 30 under 40 | 8 | 1 | not a reading dispute. A column montage of all 30 cells shows eight separate single strokes, on lines 2, 3, 4, 8, 15, 18, 20 and 28, and the footing is one stroke. Either the footing was never finished or it was written for a different column. |
| 229 | free white females, Under 5 | 19 | 11, or 19 | the footing is two long diagonals on the worst-degraded paper on the sheet. This hand writes `1` as a long diagonal, so `11` is the literal reading — but the second stroke carries a hook that reads as a `9`, and 19 is exactly what the marks come to. Neither reading is preferred here. |
| 231 | free white females, 20 under 30 | 20 | 21, or 20 | the footing is a `2` followed by a character that is either this hand's `1` or its `0`. A montage of all 31 cells of the column, cut and read one at a time, gives 20 and no twenty-first mark to find. |
| 231 | free white females, 40 under 50 | 3 | 5 | a genuine shortfall. The montage shows marks on lines 11, 24 and 29 only, and the footing is an unambiguous `5`. Two people this pass did not find. |

Everything else closes. **Page 231 is the cleanest sheet read in this deposit so far**: 34 of its
36 non-empty-or-footed columns balance on the first pass, including two-digit footings of 14, 30,
14, 16, 12 and 9. Page 229 is the worst-exposed, and it still closes on 36.

**Neither page has a free coloured person.** All 12 free-coloured columns are blank down both
sheets and blank in both footings, and that is recorded as a balance at zero rather than as
silence.

**The reading's populations**, which are the reading's and not the sheet's: page 229 is 71 free
white males and 81 free white females, 152 in all; page 231 is 83 and 74, 157. Taking every
footing exactly as written instead would give 137 and 160. Both are candidate keys for T-0539's
pairing of the eleven continuation sheets, and both should be treated as ±the residuals above
until a right sheet's TOTAL column confirms one.

**How the grid was fitted here, because it differs from T-0532's.** The 39 vertical rules were
fitted as a single pitch over the whole width of the sheet's own body and then checked against the
printed heading — column 1 must read `Under 5`, column 27 `Under 10` under FREE COLORED MALES,
column 38 `100 and upwards`. That check is what caught the thing a fixed grid would have missed:
**the rules of this book lean, and so do the lines.** The same column grid sits about 10 px left
of the printed rules at the head of a sheet and 10 px right of them at its foot; and on
33S7-9YYJ-9M5 the writing lines drop about 45 px between the left edge of the table and its right,
which is more than half a row — so a flat row grid reads the free-coloured end of a line into the
wrong household. Both leans are carried in the grid. Every column carrying a mark was then read a
second time as a montage of its own 30 or 31 cells; that second pass is what separated three
name-tails intruding from the NAMES column into column 1 of page 229 from the tally marks, and it
is what makes the 8-against-1 above a finding rather than a miscount.

## Two line counts the sheets do not agree with the inventory about (T-0532)

The row grid was fitted the same way as the column grid and checked against the names, and on
two of the three pages it finds fewer entries than the inventory declared:

| printed page | image | inventory said | entries read | blank ruled lines at the foot |
|---|---|---|---|---|
| 221 | `33S7-9YYJ-2T` | 31 | **31** | 0 |
| 222 | `33S7-9YYJ-98M` | 31 | **30** | 1 |
| 226 | `33S7-9YYJ-B3` | 31 | **29** | 2 |

The inventory's figure is `lines_with_an_entry`; the difference is blank ruled lines below the
last household, which the page files **record as lines** rather than skip. Coverage now carries
both numbers per image (`lines_with_an_entry` and `lines_ruled`).

## Printed 234 to the cell, and a second reading of 229 and 231 that does not agree with the first (T-0551, PR #698)

`33S7-9YYJ-99F` (printed **234**, 31 lines) is read to the cell: **37 of 38 columns balance the
enumerator's own footings and are committed**. The one that does not is free white females 5 under
10 — ten marks against a footing of 11 — and line 17 is the candidate, its mark carrying a second
stroke at the foot that this pass read as an inked start to a 1 and that could be the base of a 2.
Line 2 (*Geo. Shelley*) is the deposit's largest household so far — 7 males 20-30, 4 males 30-40,
6 females 20-30 and 4 females 30-40 — and every one of those four columns closes on its footing with
that reading in it. A single line that large is a lodging house rather than a family, and it is the
sort of thing T-0507's composition calibration will need to hold separately. All twelve free
coloured columns are empty and footed empty.

**The same run also read printed 229 and 231 to the cell, and so, one batch earlier, did T-0550
(PR #697).** Two independent readings of the same two sheets now exist, and they do not agree.
T-0550's is the committed reading in `pages/`; this run's is preserved verbatim in
`second_readings/` (its page files exactly as PR #698 first carried them), and the disagreement is
stated here rather than one reading being chosen by whichever landed first:

| printed page | lines | names agree | lines whose cells differ | column checks that differ (second reading / committed) |
|---|---|---|---|---|
| 229 (`33S7-9YYJ-9M5`) | 30 | 30 of 30 | **20** | free white males Under 5: 9 read against 14 footed on the second reading, 10 against 10 on the committed one; free white males 30 under 40: 8 read against 7 footed on the second reading, 8 against 1 on the committed one; free white females Under 5: 19 read against 19 footed on the second reading, 19 against 11 on the committed one |
| 231 (`33S7-9YYJ-38`) | 31 | 31 of 31 | **25** | free white females 5 under 10: 9 read against 9 footed on the second reading, 12 against 12 on the committed one; free white females 20 under 30: 20 read against 20 footed on the second reading, 20 against 21 on the committed one; free white females 40 under 50: 3 read against 3 footed on the second reading, 3 against 5 on the committed one |

The names agree on every line. The cells do not, and the pattern is not scatter: on 229 the strokes
one reading puts in the first column (free white males Under 5) the other puts in column 14 (free
white females Under 5), and on 231 marks sit in column 15 on one reading and column 18 on the other.
The two readings also read the FOOTINGS differently in exactly those columns — which is why each
reading balances, on a different set of columns, and each records a different pair as unreconciled
(second reading: free white males Under 5, free white males 30 under 40 on 229 and free white females 5 under 10 on 231;
committed: free white males 30 under 40, free white females Under 5 and free white females 20 under 30, free white females 40 under 50). Two grids fitted
to the same photograph put the same marks in different columns, and a footing read at the wrong
column agrees with the marks read at the wrong column. **That means a column that balances is
not, on its own, a column read right**, and the committed cells of 229 and 231 are ONE reading
until the two are reconciled against the sheets — which is what the reconciliation ticket filed
with this PR asks for, starting from the columns named above.

Printed 229's line count is settled at 30 by both readings independently, on the same argument
(the footings close on 30 lines and there is no 31st ruled line), so that finding stands whichever
reading of the cells prevails.

## Three more sheets read to the same rule (T-0533)

| image | printed page | entries | blank ruled lines | columns committed | `cells_state` |
|---|---|---|---|---|---|
| `33S7-9YYJ-9HY` | 225 | 23 | 8 | 38 of 38 | `read` |
| `33S7-9YYJ-6J` | 228 | 17 | 14 | 38 of 38 | `read` |
| `33S7-9YYJ-9MX` | unknown | 31 | 0 | 36 of 38 | `read_partly_reconciled` |

**Two of the three balance completely.** On 225 the twenty-three entries sum to the
enumerator's own 10, 5, 5, 9, 14, 12, 4, 2, 0, 1 across the male bands and 13, 6, 4, 2,
17, 6, 4, 0, 1 across the female; on 228 to 6, 2, 3, 2, 8, 8, 1, 1 and 8, 10, 1, 1, 8, 9,
2, 0, 1. Both sheets leave the FREE COLORED PERSONS block wholly unfilled, with no total
written under it, so those twelve columns commit at zero.

On `33S7-9YYJ-9MX` twenty-four of the twenty-six free-white columns close and **two do
not** — free white males Under 5 (sheet 11, thirty-one lines 18) and 5 under 10 (9
against 10). Those two are absent from `cells` and kept in `cells_first_pass`, which is
the same shape T-0532 set: the reading is evidence of what is on the page, and it is not
reconciled data.

Three things the totals rows taught, which the remaining cell tickets will want:

- **This hand's `8` is a reversed S with a closed head** and passes for a `5` until you
  have seen four of them. Four columns on page 228 were first read 5 and are 8.
- **Two-digit totals straddle the printed rule.** The second digit of 14, 17, 29 and 10
  each falls partly into the next cell, so reading a cell in isolation loses it — the
  page-225 female 20-under-30 total read as 13 and is 17.
- **The check catches the reader at least as often as the sheet.** Every apparent failure
  on 225 and 228, and two on `9MX`, was a printed digit misread rather than a mark
  miscounted.

Two more inventory counts are now exact: page 225 stops at line **23** (inventory said
25) and page 228 at line **17** (said 18). The remainder of each sheet is ruled and
blank, and those lines are recorded as lines.

`33S7-9YYJ-9MX` keeps `printed_page: "unknown"`. The corner carrying the number is
outside the exposure; the `(p. 4.)` in the printed heading is the form's plate marker and
is not the book's page; and it is not inferred from the filename order, which is not the
book's order. T-0504's serial fingerprint is the route that can place it.

One household is worth naming before anyone reads these sheets as families: **line 1 of
`33S7-9YYJ-9MX` holds nineteen men** — 11 in their twenties, 8 in their thirties, no
women under forty and no children. That one line is most of why its 30-under-40 column
totals 21.

## What has NOT been read yet, and where it is

The age-band, free-coloured and industry cells are a column-by-column reading that has to
be checked against the **printed column totals at the foot of each sheet** before it can
be committed — 26 narrow columns of single strokes, where a mark one column off is a
person of the wrong age. Committing a half-checked row would be worse than leaving it
unread, so a page's `records[].cells` stays `null` with `cells_state: "not_read"` until that
check is done. Eight pages have had it: printed 230 and 232 (T-0530 — 62 households, every
age band and free coloured column read line by line, 73 of 76 footings reconciled exactly,
the three that do not named on the page files), printed 221, 222 and 226 (T-0532 — the
balance stated per column in the section above, 221 committed on 36 of 38 columns, 222 and
226 committing nothing until their footers are re-read), printed 229 and 231
(T-0550 — 36 of 38 columns committed on each, printed 229's line count settled at 30, and a second
reading of both on PR #698 that does not agree with it, see below) and printed 234 (T-0551 — 37 of 38).
On every other page here the cells
are still `not_read`, and those cells are their own ticket. The other images of both read groups are inventoried in
`coverage.json` — kind, printed page, line count — and transcribed by the sibling tickets
T-0494 and T-0495 were split into.

One printed page number could not be read at all: `33S7-9YYJ-9MX` is a filled left sheet
whose top-right corner falls outside the exposure. It is recorded as `unknown` rather than
inferred from the ids around it, because the sorted filename order is not the book order —
this group alone runs 221, 231, 228, 206, 222, 234, 225, 219, 229, ?, 210, 215, 226, 238.

The **continuation half** of these two households — the family TOTAL, the six industry
columns, pensioners, and the schools and illiteracy columns — is on the paired right sheet,
and which right sheet that is is not settled. It is not in this image group: no continuation
sheet in images 26–50 foots a TOTAL of 193, and the only one footing 151 (`33SQ-GYYJ-9CZ`)
carries a per-line total vector that does not match page 230's. `records[].cells.free_persons`
is the fingerprint that settles it — a household is one ruled line spanning both sheets, so
the right sheet's TOTAL column must equal it line for line. That pairing is T-0528's ticket
and the continuation columns follow it.

The other 23 images of this group are inventoried in `coverage.json` — kind, printed page,
line count — and transcribed by the sibling tickets T-0495 was split into.

## Printed pages 216 and 217, read to the cell (T-0552)

`33S7-9YYJ-DD` (printed **216**) and `33S7-9YYJ-RC` (printed **217**) are the first two left
sheets of image group 26–50 to be read in full: 62 households, every one of the 38 age-band
columns on each line, and the enumerator's own footings transcribed beside them.

**How the columns were fixed.** The leaf bows into the gutter, so a grid taken off the printed
header is about a quarter of a column out in the middle of the page — the first reading of page
216 put two marks a column to the left of where they stand because of it. Both sheets were
therefore gridded from the image's own vertical darkness profile (page 216: free white males
from x=0.1558 of the image width at a pitch of 0.019725, females from 0.4118 at 0.019575,
coloured from 0.6689 at 0.01963; page 217: 0.1529/0.019523, 0.4067/0.0195, 0.6611/0.01955) and
every line re-read from a crop with that grid drawn over it. The row ruling leans about half a
line down page 217, which on a uniform row grid reads as a blank line between Philo Carpenter
and Robert Crawford; it is drift, not a blank line, and the tail was re-read on a grid fitted
to it.

**A line count corrected.** The inventory declared page 217 at 33 lines "to the nearest line".
It carries **31**, counted twice — once down the names column and once on the drawn grid — with
no blank ruled line anywhere between entries. Page 216's declared 31 is restated unchanged.

**What closes and what does not.** Every column of both sheets is checked against the figure the
enumerator wrote at the foot of his own column, and a residual is recorded rather than adjusted
away.

| sheet | block | footings that close | that do not |
|---|---|---|---|
| 216 `33S7-9YYJ-DD` | free white males | 5 of 8 | under 5 (20 read / 21 footed), 10–15 (3/6), 15–20 (6/1) |
| 216 | free white females | 7 of 9 | under 5 (15/14), 5–10 (4/2) |
| 216 | free coloured | 3 of 3 | — |
| 217 `33S7-9YYJ-RC` | free white males | **9 of 9** | — |
| 217 | free white females | 5 of 8 | under 5 (20/16), 20–30 (19/18), 30–40 (15/12) |

Page 217's male block closing exactly on all nine footed columns is what licenses the method:
the same grid, read the same way, reproduces the enumerator's own arithmetic on 86 people. The
residuals that remain are therefore a statement about the sheets, not a confession about the
grid — and two of page 216's are as likely to be a glyph as an error, which the page file says
where it says it (its 10–15 footing is a bottom-looped figure read as 6, and a 3 would close the
column exactly; the reading is flagged, not assumed).

**What this means for pairing.** Neither sheet is paired to its continuation — that is T-0539's
single reading over all eleven. Each publishes its population key: page 216 at 175 by the
footings, 180 by the lines; page 217 at 160 by the footings, 168 by the lines. Try the footing
key first, because the TOTAL column a continuation sheet foots comes out of the same arithmetic.

**Nothing here mints or regrades an 1835 resident.** Philo Carpenter is on page 217 line 29 and
is the one name a modern reader can be sure of; the bridge from a named 1840 head to an 1835
record is T-0505's step, under a ladder that is explicit that 1839/1840 alone is never a 1835
resident.

## Printed 210 and 215, read to the cell (T-0584)

Two more left sheets of image group 1 are now read line by line and column by column,
and both were closed against the figures the enumerator footed on his own sheet.

| printed page | image | lines with an entry | columns balanced | not committed |
|---|---|---|---|---|
| 210 | `33S7-9YYJ-9RG` | 30 (inventory said 31) | 36 of 38 | free white females Under 5 (14) and 5 under 10 (15) |
| 215 | `33S7-9YYJ-9WF` | 31 (inventory's figure stands) | 37 of 38 | free white females 30 under 40 (19) |

**The footings corrected the reading twice, and the reading corrected the footings twice.**
On 210 the columns for free white males 20 under 30 and 30 under 40 were first read off a
1400 px contact view as 25 and 16; the line-by-line sums came to 29 and 19, and zoomed on
the footing itself both figures are plainly 29 and 19. The other way round, on 215 the
first column template — anchored on the strongest 39 rule detections rather than on the
printed heading — started one whole column too far right, which would have aged every
person on the sheet by one band. Rendering the template over the printed heading is what
caught it, and it is why the grid note on every page file states that check.

**What the two sheets are.** They are not alike. Printed 210 is a page of large households:
30 entries carrying 179 free white persons, one of them (line 1) of fourteen. Printed 215
is the opposite — 31 entries, and columns 6 and 7 (free white males 30 under 40 and 40
under 50) carry 49 of its 116 free white persons between them, mostly one man to a
household. Printed 215 also carries the only free coloured persons read from image group 1
so far: six of them in John Johnson's household on line 29, and one on line 5.

**Two residual columns are left standing rather than forced.** On 210, free white females
Under 5 reads 14 against a printed 16 and 5 under 10 reads 18 against a printed 15 — equal
and opposite to within one, which is the shape of marks read into the wrong one of two
adjacent columns; the montage was cut at the leaned rules, re-read, and did not move them.
On 215, free white females 30 under 40 reads 17 against a printed 19. Those columns are
omitted from `cells` and kept in `cells_first_pass`, which is read but unreconciled and is
not data anything downstream may use.

## Every named head has an outcome now (T-0505)

The 498 names read off the 19 left sheets in this repo were in no state at all: three of
them were bridged to an 1835 person and the rest were neither matched nor refused, which
reads exactly like a pile nobody has looked at, so the next sweep would have looked at it
again. `tools/crosswalk_census_1840_heads.py --build` writes
`resident_crosswalk.json`, which gives every one of them an outcome and the rule that
decided it, and it fills this domain's `crosswalk.json` — which held
`passes: [], merges: [], refusals: []` — with 5 merge(s) and 139 refusal(s).

**The counts.** 5 matched, 5 candidate, 488 refused.

| rule | heads |
|---|---|
| `L1 unreadable_name` | 141 |
| `L2 no_surname_in_the_1835_pools` | 230 |
| `L3 given_name_conflict` | 94 |
| `L4 initial_only` | 21 |
| `L5 name_is_not_unique` | 2 |
| `L6 matched` | 5 |
| `L6a low_confidence_caps_at_candidate` | 1 |
| `L7 candidate` | 4 |

**The ladder is deliberately hard to climb.** `matched` needs the full forename and the
surname to agree, the name to be unique BOTH among the 498 heads and among the 1835
persons, the reader's own grade on that name to be `medium` or better, and a discriminator
that is independent of the name — an 1843 Fergus or 1844 Norris directory entry adjudicated
to that person, or an 1840 bridge already adjudicated. An appearance of the SAME NAME on a
poll list or a letter list is NOT a discriminator: it is the same name again, and it cannot
separate two people who share it. Those appearances are recorded on every head as
`same_name_support`, and they never promote a candidate.

**What it found.**

| 1840 head | 1835 person | printed page / line | rule |
|---|---|---|---|
| William H. Stow | William H. Stow | 225 / 20 | L6 |
| William Allen | William Allen | 230 / 26 | L6 |
| Philo Carpenter | Philo Carpenter | 217 / 29 | L6 |
| John Davis | John Davis | 232 / 13 | L6 |
| Gurdon S. Hubbard | Gurdon Saltonstall Hubbard | 232 / 17 | L6 |

and 5 candidate(s):

| 1840 head | 1835 person | printed page / line | rule |
|---|---|---|---|
| John Wilson | John Wilson | 229 / 2 | L7 |
| John H. Kinzie | John Harris Kinzie | 232 / 25 | L7 |
| Byram King | Byram King | 207 / 4 | L7 |
| Samuel C. Jackson | Samuel Jackson | 207 / 5 | L7 |
| Joseph M. Chandler | Joseph Chandler | 207 / 6 | L6a |

**John Murphy is now a refusal, and that is the most useful thing in the pass.** The
adjudicated bridge in `census_1840_identity_bridges.csv` puts him on printed page 233 row
30. This repo has read a `[?]ohn Murphy` on printed page 222 line 27 — a different line, on
a sheet the bridge does not name, and printed 233 has not been read here at all. Two 1840
lines carry the name, so neither identifies the man, and the pair is refused under L5 with
the conflict written down. The bridge is not withdrawn here: this file adjudicates lines
and T-0515 owns the bridge table. Reading printed 233 settles it.

**The 29 heads the 2 September legacy matcher left unmatched are re-adjudicated**, and they
split three ways: 14 sit on printed pages this repo has not read yet and are refused as
unverifiable rather than carried forward (the workbook behind them is lost — the owner's
ruling of 2026-09-03 is "They are lost; rebuild"); 13 sit on pages that HAVE been read here
line by line and no line on them carries the name, so the workbook row is refused in favour
of the page; and 2 are found in this reading and take an ordinary ladder outcome.

**Town finding.** The only spatial signal an 1840 sheet carries is the order the enumerator
walked it in. 2 adjacent pair(s) of matched-or-candidate heads are recorded under
`town_findings` — an 1840 fact about 1840 neighbours, which places nothing on the 1835
ground and may not.

**Nothing here mints or regrades anybody.** Each `matched` head carries a PROPOSED
`later_census` block in the shape PR #670 wrote, with `serial: null` because the
page-to-IPUMS-serial fingerprint is T-0504 and is not landed; T-0515 applies them. The
ratified ladder binds throughout: an 1839 or 1840 appearance alone is never an 1835
resident, and 1840 household composition is never back-projected to the scene.
