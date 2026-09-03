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

## What has NOT been read yet, and where it is

The age-band, free-coloured and industry cells are a column-by-column reading that has to
be checked against the **printed column totals at the foot of each sheet** before it can
be committed — 26 narrow columns of single strokes, where a mark one column off is a
person of the wrong age. Committing a half-checked row would be worse than leaving it
unread, so every `records[].cells` here is `null` with `cells_state: "not_read"`, and the
cells are their own ticket. The other images of both read groups are inventoried in
`coverage.json` — kind, printed page, line count — and transcribed by the sibling tickets
T-0494 and T-0495 were split into.

One printed page number could not be read at all: `33S7-9YYJ-9MX` is a filled left sheet
whose top-right corner falls outside the exposure. It is recorded as `unknown` rather than
inferred from the ids around it, because the sorted filename order is not the book order —
this group alone runs 221, 231, 228, 206, 222, 234, 225, 219, 229, ?, 210, 215, 226, 238.
