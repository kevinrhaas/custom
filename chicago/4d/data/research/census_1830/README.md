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

**What was read, T-0498 (2026-09-03).** The schedule itself, off the film — NARA M19 reel 24
as the Internet Archive republishes it (`populationsc18300024unit`), leaves n580 and n582, 67
heads of family. The reading is graded `scan_verified` because the item carries no text layer
and no transcriber stands between this project and the enumerator's hand. `search_log.json`
records the four transcription sites tried first and what each of them said.

**The district is not called Chicago.** The heading is `Peoria & Putnam Counties & Territory
attached`, written once on n580 and dittoed. Cook County was five months in the future. The
settlement is a run of households inside a district that also contains the Du Page and Fox River
country, and the schedule does not separate them — so "the 1830 census of Chicago" is a phrase
later indexes added, and this domain does not use it.

**Not finished.** The district runs on past leaf n584 and those leaves are unread. `coverage.json`
says so in `not_declared_and_why`, and T-0605 is the ticket that finishes it.

**Coverage.** Declare the IMAGES or PAGES read, by id or number. A declared image
nothing reaches is a hole. Do not declare an image you have only opened.

**Access, recorded as fact and not as absence.** archive.org's search API and
`/download/<id>/<id>_djvu.txt` work. HathiTrust page views return 403 while its
catalog API works. FamilySearch and Ancestry are login-walled — a source behind a
login is INACCESSIBLE FROM HERE and must be recorded as that, never as "no record
found". The two read very differently to the next run.

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`, and the gate asserts it.
