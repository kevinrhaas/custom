# The 1830 federal census — the named schedule, not the county totals

**What lives here.** Chicago was enumerated in **Peoria County** in 1830, and this
project holds only the county aggregates. The object of this domain is the NAMED
schedule: the sheets that carry heads of household by name, and the page images
behind them (T-0498).

**Shape: `records`.** One census line is one record. `as_read` is the enumerator's
hand as the image or the transcription gives it; `normalized` is this project's
spelling. Age-band and composition columns belong in the row's `notes` or in a
structured field beside them — never silently promoted into an 1835 household.

**1830 is FIVE YEARS EARLY.** A name on this schedule is evidence that a person was
in the enumerated district in 1830. It is not evidence that they were in Chicago in
July 1835, and this domain must never be the sole ground of a resident record. The
bridge belongs in `crosswalk.json` and in the consolidation, with its rule written
out.

**Hand-authored:** `text/`, `claims/`, `coverage.json`, `crosswalk.json`, `search_log.json`.
**Generated:** `records/schedule_chicago_1830.json` and `resident_crosswalk.json`, both by
`tools/read_census_1830.py --build` out of the committed reading in `text/`;
`data/research/domains.json`, which is gated.

**What was read, T-0498 (2026-09-03) and T-0605 (2026-09-05).** The schedule itself, off the
film — NARA M19 reel 24 as the Internet Archive republishes it (`populationsc18300024unit`).
T-0498 read leaves n580 and n582, 67 heads of family. T-0605 read n576 (55), n578 (56) and
n584 (22), and the recapitulation leaf n586. **The division is now read complete: 200 heads of
family on five leaves.** The reading is graded `scan_verified` because the item carries no text
layer and no transcriber stands between this project and the enumerator's hand. `search_log.json`
records the four transcription sites tried first and what each of them said.

**Where the district begins and ends, and what proves it.** The division is leaves n576, n578,
n580, n582 and n584 — printed pages 299 to 303 — and n586 (page 304) is its recapitulation,
which carries five page-total rows and not one head of family. Those five rows ARE the totals
rows of the five name leaves: page 1's row repeats the same six struck-and-rewritten cells that
n576's totals row carries, and pages 2, 3 and 5 match n578, n580 and n584 cell for cell. That,
and not the county column, is what binds the leaves together — the heading is written on n580
alone and every other leaf leaves the cell empty. T-0605 was opened on T-0498's belief that the
district ran ON past n584; it runs BACK to n576, and the unread leaves were at the front.

**What does not close.** n586's family column, as read, gives 53 / 56 / 88 / 28 / 22 per page —
which sums to 247, not to the 199 written under it — while the leaves as read carry 55 / 56 / 39
/ 28 / 22 = 200. Pages 1 and 3 are where the recapitulation and the leaves part. Neither figure
is preferred, nothing in this domain is graded on it, and the re-count is a ticket of its own.

**The district is not called Chicago.** The heading is `Peoria & Putnam Counties & Territory
attached`, written once on n580 and dittoed. Cook County was five months in the future. The
settlement is a run of households inside a district that also contains the Du Page and Fox River
country, and the schedule does not separate them — so "the 1830 census of Chicago" is a phrase
later indexes added, and this domain does not use it.

**Still not read.** The per-household age-band cells, on every leaf — twenty-eight columns for
two hundred households is a pass of its own, and half of it would be worse than none. The odd
leaves (n577, n579, n581, n583, n585) are the right-hand continuation halves of the same sheets
and are unread. `coverage.json` carries both, and the recapitulation re-count above.

**Coverage.** Declare the IMAGES or PAGES read, by id or number. A declared image
nothing reaches is a hole. Do not declare an image you have only opened.

**Access, recorded as fact and not as absence.** archive.org's search API and
`/download/<id>/<id>_djvu.txt` work. HathiTrust page views return 403 while its
catalog API works. FamilySearch and Ancestry are login-walled — a source behind a
login is INACCESSIBLE FROM HERE and must be recorded as that, never as "no record
found". The two read very differently to the next run.

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`, and the gate asserts it.
