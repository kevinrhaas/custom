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

## What has NOT been read yet, and where it is

The age-band, free-coloured and industry cells are a column-by-column reading that has to
be checked against the **printed column totals at the foot of each sheet** before it can
be committed — 26 narrow columns of single strokes, where a mark one column off is a
person of the wrong age. Committing a half-checked row would be worse than leaving it
unread, so a page's `records[].cells` stays `null` with `cells_state: "not_read"` until that
check is done. Five pages have had it: printed 230 and 232 (T-0530 — 62 households, every
age band and free coloured column read line by line, 73 of 76 footings reconciled exactly,
the three that do not named on the page files) and printed 221, 222 and 226 (T-0532 — the
balance stated per column in the section above, 221 committed on 36 of 38 columns, 222 and
226 committing nothing until their footers are re-read). On every other page here the cells
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
