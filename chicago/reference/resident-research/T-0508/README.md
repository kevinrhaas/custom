# T-0508 resident-research handoff — cohort 13

Thirteenth cohort. Frozen manifest: `chicago/4d/data/research/residents/pass_13_76_cohort.json`
(76 people: 26 established profiles, 25 letter-list present, 25 letter-list uncertain).

Reviewed **2026-09-05**: **76 of 76 complete, 0 pending** —
**10 corroborated · 18 corroborated enrichments · 7 candidate identities retained unasserted ·
41 documented no-corroboration results**.

## Artifacts

- `T-0508_resident_research.csv` — the machine-readable export the synthesis reads.
- `T-0508_search_log.csv` — one row per person searched: 76 rows for 76 people.
- `T-0508_resident_research_working.xlsx` — the same, with a `Search_Log` and a `Counts` sheet.
- `chicago/4d/data/research/residents/pass_13_findings.json` — the authoritative outcome ledger.

## What was searched

Every committed research and source file in the repository — **794 files, 42.8 MB** under
`data/research/` (excluding the derived `residents/` ledgers and `newberry_index/`) and
`data/sources/` — for each of the 76 names, in four forms: `Given Surname` and `Surname, Given`
within thirty characters, and the two initial forms `G. Surname` and `Surname, G.`. A separate
surname-only pass ran first as a file census, to know where to look; a surname-only agreement is
never a match.

Then **one external source, fetched whole**: Andreas, *History of Chicago*, vol. 1 (1884),
archive.org item `historyofchicago01andr`, `_djvu.txt`, 5,214,426 bytes,
sha256 `e842bdadb9385be2e3e673b7191520ddcd20fb035b7229cf829eb516c9a95687`, read 2026-09-05.
The OCR was fetched and searched locally rather than through archive.org's full-text index
because that index is lossy on this item by its own source record's statement — and because the
public `advancedsearch` endpoint proved to search metadata only, returning zero for names that
stand in the same item's OCR. The text is not committed; the hash of what was read is.

Login-walled (FamilySearch, Ancestry) and 403-ing (HathiTrust page views) sources are recorded as
**inaccessible, never as absent**.

## The rules this pass held to

1. A surname-only agreement is a refusal, however good it looks.
2. The post-office letter lists are the **seed**. They never corroborate themselves.
3. Evidence printed in 1839, 1840, 1843, 1844 or 1892 is evidence **about those years**. It can
   corroborate an identity; it can never make a 1835 residence, trade or address. Every such row
   here says so in `evidence_against`.
4. Candidate identities are retained **unasserted**, with their conflicts written down.
5. A negative search is a result, and all 41 of them are on the record.
6. **Nothing here changes a grade.** T-0513 consolidates and T-0514/T-0515 apply.

## What this cohort actually bought

The cohort was chosen by the freeze, not by promise, and it happened to contain twenty-six of the
town's most documented citizens — and Andreas's roll of *"the denizens of the town in the fall of
1833"* names thirteen of them in one passage, most with a **trade and an arrival year**, all inside
or before the scene window:

| person | what the passage gives, and for what year |
|---|---|
| Tyler K. Blodgett | came spring 1833; started **the first brickyard**, North Side, between Dearborn and Clark, near the river bank — and a second Andreas passage repeats it independently |
| **Beckford** | **printer, in John Calhoun's employ, 1833** — the only naming of this person anywhere |
| John Calhoun | printer and editor of the first newspaper; arrived November 1833 |
| Philo Carpenter | druggist; came July 1832 |
| David Carver | seaman and lumber merchant; came 1833 |
| John Bates Jr. | auctioneer; came 1832 |
| Lemuel Brown | blacksmith; came 1833 |
| Archibald Clybourne | butcher; came 1823; living north of the town limits |
| Mrs Rufus Brown | kept one of the first-class boarding houses, 1833 |
| Mark Beaubien | the Sauganash, "still kept by the original proprietor" |
| Madore B. Beaubien | merchant |
| J. B. Beaubien | merchant |
| W. H. Adams | named, no trade |

Beside them: Edward W. Casey among the lawyers who *"had put out their signs in 1833"*; John Dean
Caton appointed Corporate Attorney 4 December 1833; Silas B. Cobb *"a minor, came June 1, 1833"*;
Josette Beaubien and her children named in the 1833 treaty annuity schedule.

**Beckford is the find.** Before this sweep the record read `Beckford`, occupation none, and
returned **zero hits in 42.8 MB of committed corpus**. Andreas names him once — a printer working
for John Calhoun — and the emptiest card in the cohort is the one the external fetch paid for.

## Unresolved, and written down so the next pass does not re-find them

- **Andreas reprints the letter list of 1 January 1834 in full.** It corroborates nobody (it is the
  seed), but it is a **further printing** of the list whose length and lost names are the open
  question in T-0318, T-0424, T-0425 and T-0428 — and it is not among the printings those tickets
  enumerate.
- **Three pairs inside this one cohort are one person read twice**: Aaron Parcel / Aron Parcell,
  Alonzo Murray / Alonzo Murry, Alanson B. Vaughan / Alison B. Vaughn. Merging is T-0513's job;
  naming them is this pass's.
- **Ira Couch is corroborated as an identity and NOT as a 1835 resident.** Every record that names
  him — the 1840 census, the 1842 church roll, Andreas's juries — is after the scene date, and the
  ledger says so rather than letting a famous name imply a presence.
- **Joseph Bailly** is probably the Lake Michigan fur trader who died at Baillytown, Indiana, on
  21 December 1835. That makes the postal return **mail held at Chicago for a man who lived in
  Indiana** — a caution about what a letter-list return is worth as residence evidence, and the
  books crosswalk had already refused the merge on the same ground.
- **Charles Avery** carries three different middle initials across three sources (none, K, E). Not
  one man until something says which.

Cumulative reviewed total after T-0508: **912**.
