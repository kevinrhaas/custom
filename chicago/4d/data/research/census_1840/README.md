# `census_1840` — the 1840 federal census of Chicago, read off the page images

**This is LATER EVIDENCE.** Nothing in this directory mints an 1835 resident. The
project's ratified ladder is explicit: *1839/1840 alone is never a 1835 resident.*
What is read here is a named 1840 household head with a line position; the bridge to
1835 is a separate, adjudicated step (T-0505), and the minting is a separate one again
(T-0514, T-0515).

## What the deposit holds

`chicago/reference/census1840/` holds 75 distinct FamilySearch page images (76 files —
`33S7-9YYJ-9WF (1).jpg` is a byte-identical copy of `33S7-9YYJ-9WF.jpg`). The deposit is
**read only**: no image, crop or render is ever committed. Only derived text is.

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
| `crosswalk_670.json` | the line-by-line comparison against the 210 rows PR #670 recovered from the owner's lost v4 workbook. |

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
new reading must reproduce before it extends. **Two of the seven pages they cover are in
this group (printed 230 and 232), and read off the sheets they do not reproduce.**

Of 62 lines compared, **10 agree on both given name and surname** and **33 agree on
neither**. Some of the disagreements are large: line 17 of page 232 reads *Gurdon S.
Hubbard* on the sheet against *Saml. J. McCord?* in #670, and line 25 reads *John H.
Kinzie* against *John W. Rogers?* — two of the most consequential names in the town.
Page 230's tail shows a different shape again: several #670 rows match the scan one line
LATER, which is what a row drift looks like rather than a bad reading.

`crosswalk_670.json` carries every line of it. **Nothing in #670 was overwritten** — both
readings stand, with the reason the scan is treated as senior stated on each line. What
this means for T-0504 and T-0505 is that the 210 rows cannot be used as ground truth for
a serial fingerprint or an identity bridge until they have been re-read against the
images; that is the whole point of reading the calibration pages first.

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

## What has NOT been read yet, and where it is

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
