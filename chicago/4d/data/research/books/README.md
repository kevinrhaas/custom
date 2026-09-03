# Books and reminiscences — prose, read the way the newspapers are read

**What lives here.** Fergus' Historical Series Nos. 26-29 (1.24 MB of raw OCR,
with no text, no register and no claim read out of it), Gurdon Hubbard's
autobiography (a 226-page scan the project has never mentioned), H. H. Porter's
*Short Autobiography* (66 MB, a garbled text layer, and nothing yet saying whether
it carries 1835 Chicago at all), and the memoirs printed beside them (T-0499,
T-0500, T-0501, T-0502).

**Shape: `claims`.** A book is PROSE, so the unit is a claim and not a row —
exactly the newspapers' shape, for exactly the newspapers' reason. A claim carries
a `kind` from the closed vocabulary, a `reading` grade, a **verbatim `quote`**, the
`normalized` reading, the `locator` that finds it again, `describes_date`, the
`entities` it names, and `town_finding`.

**`town_finding` is the field this domain needs and the papers did not.** A
reminiscence is mostly about its author. The paragraph that says the writer's
mother was kind is worth recording and is not worth placing in the town;
`town_finding: false` says so, and keeps a reading from being mistaken for a
finding by whoever consolidates.

**THE VERBATIM GATE BINDS THIS DOMAIN.** `tools/research_domains.py --check`
reassembles every `quote` out of the committed file at `text/`, line by line, and
fails on a one-character difference. A tidied quote is invisible to every other
check in this repository, and the smoothed reading has a field of its own to live
in: `normalized`. Commit the text you quote from; a quote whose text is not
committed cannot be checked and does not pass.

**`describes_date` is not the printing date.** These books were written decades
after 1835. The date a passage DESCRIBES is the one the reconstruction cares
about, and a memoir's own distance from it is a reason to grade carefully, not a
reason to skip the field.

**Hand-authored:** `claims/`, `text/`, `coverage.json`, `crosswalk.json`.
**Generated:** nothing here yet; `data/research/domains.json` is, and is gated.

**Coverage.** Declare the PAGES read. A declared page no claim reaches is a hole —
and in a 226-page scan, a hole is the difference between "read" and "opened".

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`.

---

## What has been read (T-0575, 2026-09-03)

**Hurlbut's *Chicago Antiquities* (1881), pages 28-36** — the chapter on the American
Fur Company and Chicago. Nineteen claims at
`claims/american_fur_company_hurlbut.json`, out of this project's own committed copy
of the transcription at `text/hurlbut_chicago_antiquities_28_36.txt`, which is
byte-identical to the genealogytrails cache it was taken from. Source record:
`data/sources/chicago_antiquities_american_fur_co.json`.

**Three voices, and every claim says which it is.** Hurlbut compiles in 1881 and
judges; Gurdon S. Hubbard remembers inside quotation marks at sixty years' distance;
and an outward-invoice book of the Michilimackinac agency, 1821-22, is a period record
printed verbatim with its orthography kept. The source record's `transcribes[]` grades
the three separately — 4, 2 and 1 — and the record's own tier is 2, which is
Hubbard's rung and not Hurlbut's.

**What the chapter is for.** It is a SIZE ARGUMENT about the town, said twice by two
men who did not copy each other: Hurlbut's "Chicago was the port and point of a very
limited district of distribution", and Hubbard's "this place never had been preeminent
as a trading-post, as this was not the Indian hunting-ground". With the two dates
beside them — Hubbard bought the company's whole Illinois interest in 1828, and Astor
sold the company in 1834 — it settles what this town may say about the American Fur
Company in 1835, which is nothing.

**Nothing here is payload.** No structure, asset, resident or household record was
changed by this reading. The readings that argue for such a change — Hubbard's dated
1818 arrival against a resident record that grades the same year "reconstructed", the
Factory House origin of `jb_beaubien_homestead`, the catalogue of trade goods, and the
James / John H. Kinzie half-brotherhood — are written as proposals in T-0575 and carry
their own tickets. **The chapter's latest Chicago event is 1828**, so it dates and
corroborates and places nobody.

**`coverage.json` declares this chapter as one `list` item and not as nine `page`
items**, because the transcription marks no page breaks. The page RANGE is named in
every locator; a page number would be an invention, and the gate would then be checking
a fiction. The day this project reads the book itself, the declaration can become nine
pages honestly.
