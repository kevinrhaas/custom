# The Newberry genealogical index

*The Genealogical Index of the Newberry Library, Chicago* — four volumes, G. K. Hall &
Co., 1960 — is a photostat of the Newberry's genealogical card index. Each card heads a
family surname and gives, underneath it, a locality and the published genealogy, local
history or periodical that treats that family there, with the author, the date, the
pages and the Newberry call number. The owner put all four volumes on the Internet
Archive on 2026-09-03 as `chicago1835-newberry-genealogical-index`, and that identifier
is the canonical locator for them: the research corpus is moving to the Archive item by
item, and a source record naming the IA identifier survives the move where one naming a
local path does not.

**It is a finding aid, and this whole directory is built around that.** A card never
places a person in Chicago in 1835. It says WHERE A BOOK IS that might. So nothing here
grades a resident, a household or a business; `tools/read_newberry_index.py --check`
FAILS if the source id `newberry_genealogical_index` ever appears in a record under
`data/residents/`, `data/structures/` or `data/reconstruction/`. The whole failure mode
of an index is that a surname in it looks like evidence, and this is the only place that
can be stopped.

## What is here

| file | authored by | what it is |
|---|---|---|
| `text/MANIFEST.json` | `--extract` | the volumes' sizes and sha256s, the crop boxes, the sha256 of every intermediate — what makes the committed text reproducible from PDFs this repo does not carry |
| `text/vol_NN_locality_cards.txt` | `--extract` | the kept cards, verbatim as the text layer gives them, two lines each: the heading, then the body line that named a locality |
| `records/entries_vol_NN.json` | `--parse` | one record per kept card, in the `tools/research_domains.py` records shape |
| `entries.json` | `--parse` | the index of the above: which volumes are parsed, which are not, and the counts. The entries themselves live under `records/`, where the domain gate reads them; a second copy here would drift within a run |
| `leads.json` | `--parse` | surname → the residents, voters, 1840 heads and structures a card COULD bear on, over every volume read so far. Never a match |
| `follow_up.json` | `--parse` | the works the Chicago and Cook County cards point at, over every volume read so far, ranked by how many of this project's people they could bear on. This is the reading order |
| `precision_sample.json` | **hand** | forty cards of EACH volume, drawn at random and adjudicated one at a time against the page image. The only thing here that measures whether the reading is any good. One block per volume: a number drawn on one volume is not a measurement of another |
| `coverage.json` | **hand** | which volumes have been read |
| `crosswalk.json` | **hand** | no merges, and the refusals written out one by one |

This is research, not payload. `tools/publish.sh` does not copy `data/research/`, and
`tools/newspaper_corpus.py --check` asserts it stays out of `site/chicago/4d/`.

## How the volumes are read

The four PDFs are ~200 MB each and are **not committed**. Fetch one to a scratch path and
run:

    python3 tools/read_newberry_index.py --extract --volume 2 --pdf /tmp/newberry_v2.pdf
    python3 tools/read_newberry_index.py --parse   --volume 2
    python3 tools/read_newberry_index.py --check

The volumes carry a text layer, so no OCR pass of our own is needed — but `pdftotext
-layout` alone is useless on them. A page is four columns of card images, and `-layout`
weaves all four into single lines, so a heading and the citation under it end up in
different lines with two other cards' text in between. The repair is to crop before
laying out: `pdftotext -x/-W` over four overlapping 200-point windows returns each column
in card order, heading first. The windows overlap because page widths in volume 1 run
from 689 to 733 points and a column's left edge moves by up to 44 points across the
volume; the duplicate cards the overlap produces are deduplicated on (page, heading,
body).

## What the reading is worth

**The text layer is bad.** These are photostats of typed and hand-corrected cards, and
the OCR of them drops letters, doubles them and puts spaces inside words. 'Andreas'
comes back as 'Andrest', 'Androcs', 'Anurcii', 'Antlrcas' and `A.:.!.;c,`; 'family' as
'foully', 'ramlly' and `f a m i l y`. Nothing here is a clean transcription and it does
not pretend to be one: every record is graded **`transcription_mediated`**, because a
machine's reading of a photostat of a card is a transcription and calling it
`scan_verified` because a machine looked at an image would be exactly the upgrade the
provenance rule forbids.

**The number, and how it was got.** Forty cards of each volume read are drawn at
random — twenty from the Chicago/Cook stratum and twenty from the rest,
`random.seed(1835)` — and adjudicated one at a time against the rendered page image.
`precision_sample.json` carries all of them, one block per volume, because a number
drawn on one volume is not a measurement of another.

| volume | sampled | locality correct | precision | Chicago/Cook stratum | Illinois-only stratum |
|---|---|---|---|---|---|
| 1 (A-C) | 40 | 39 | **0.975** | 20/20 | 19/20 |
| 2 (C-H) | 40 | 35 | **0.875** | 20/20 | 15/20 |

**The Chicago and Cook stratum has not missed yet** — 40 of 40 across both volumes —
and every bad keep in either draw is in the Illinois-only stratum. That matters because
the Chicago and Cook County cards are the ones `follow_up.json` ranks the reading order
on. The draws are stratified 20/20 and the volumes are not, so weighted by the
population volume 2's estimate is 0.813 and the 0.875 above is the figure comparable
with volume 1's.

Volume 1's one bad keep is `nbi_v01_2226`, whose entire line is `I II.`: three strokes
and a stop is the shape of the abbreviation and on that card it is the only thing there.
Volume 2's five are **two classes, and both are new**:

- **The state banner absorbed as a card body** (four of the five). The index divides one
  family's run of cards by state with a printed rule, `ILLINOIS.`; when that rule falls
  directly under a heading, the extractor reads it as that card's body and keeps the
  stanza, which carries no citation at all. `nbi_v02_1675` is the proof the banner does
  not belong to the heading above it: the heading is 'Kinge or King family.', whose one
  card is an English parish register, and the surname run under the banner is KINGERY.
- **A call number read as a state** (the fifth). `nbi_v02_1106` is 'Holden family. —
  Hapgood fam. (Hapgood, W.) 1898. See index. E. 7. H 21', naming no locality; the
  `, III,` the pattern matched on is the wreck of a Newberry call number.

Both are left in the records with their verdicts — a card struck where nobody can see it
is a precision figure nobody can check — and **T-0594** carries the rules that would
refuse them. The same draw found a third thing that is not a precision error: a column
sliver is kept as a second, truncated copy of a card the neighbouring pass read in full
(`nbi_v02_1775` is `nbi_v02_1779` again), because the passes deduplicate on (page,
heading, body) and a truncated sliver never matches its full sibling. **T-0595** measures
how many. And volume 2 showed the sample cannot measure recall: `nbi_v02_0937` is a
Chicago card — 'Henrotin family. — Chicago, Ill. (Andreas, A. T.) 1884-6' — whose body
lost the word 'Chicago', so it is bucketed Illinois-only and is missing from the 501. The
Chicago-and-Cook counts are a floor, not a count.

The samples also found one *systematic* false positive that is now a rule. The index
holds thousands of English cards citing the *Calendarium Inquisitionum post mortem*,
whose entries are filed by regnal year — `Calendarium, Hen. III. and Edw. I` — and
`, III.` is the shape of `, Ill.`. `REGNAL` in the tool refuses them; 35 cards left
volume 1 when it was added, and volume 1's sample was redrawn afterwards.

**Surnames are recovered, not read.** A heading is often clipped by its neighbour, so
`er, E P Adams` is a real reading of an Adams card. The comparison key is the longest
word of three letters or more in the heading, which is `Adams` there and `Aldridge` in
`Aldridge, or Oldridge`. The key is for comparison only; `as_read` always keeps the
heading verbatim.

**Citations are clustered, and more than half of them are not.** The works table in the
tool matches a citation by pattern or by similarity to one canonical spelling. It reaches
1,928 of the 4,566 cards read so far. The 2,638 it does not reach are overwhelmingly Illinois
COUNTY histories — Chapman, LeBaron, Brink & McDonough, Baldwin, Murray Williamson,
Power — published by houses nobody has written a pattern for, and only **274** of them
name Chicago or Cook County. That residue is the weakest part of this reading and it is
counted rather than hidden: `follow_up.json` reports it in
`chicago_or_cook_cards_matching_no_known_work`.

## Volume 1 (A-C), read 2026-09-03 under T-0570

987 pages cropped and walked · **58,488 cards** assembled · **2,579 kept** for naming
Chicago, Cook County or Illinois · of those **581 name Chicago or Cook County** ·
1,671 distinct surname keys · **319 leads** across four layers (residents 156, census
1840 81, voters 64, structures 18) · **0 merges**.

The reading order it produces, ranked on Chicago and Cook County cards standing on a
surname this project already holds:

| work | Chicago/Cook cards | on a lead surname | held? |
|---|---|---|---|
| Andreas, *History of Chicago* (1884-6) | 300 | 68 | yes — `andreas_1884_v1` |
| **Moses and Kirkland, *History of Chicago, Illinois* (1895)** | 76 | 16 | **no** |
| Moses, *Illinois, historical and statistical* (1888-92) | 57 | 11 | no |
| La Salle Book Co., Cook County biographical volumes (1900, 1909) | 19 | 5 | no |
| Fergus, *Chicago directory for 1839* | 12 | 5 | yes |
| Reynolds, *The pioneer history of Illinois* (1887) | 1 | 1 | no |
| Hurlbut, *Chicago antiquities* (1881) | 2 | 0 | no |

**The finding that is worth a ticket:** the index's Chicago cards point at Andreas more
than at everything else together, and this project already has Andreas. The largest
Chicago work it points at that this project does **not** hold is Moses and Kirkland's
*History of Chicago* (1895) — 76 Chicago and Cook County cards in volume 1 alone, 16 of
them under surnames already in the residents, the poll lists or the 1840 census. Both
volumes are on the Internet Archive (`historyofchicago01mose`, `historyofchicagov2mose`).

## Volume 2 (C-H), read 2026-09-03 under T-0578

1,016 pages cropped and walked · **58,589 cards** assembled · **1,987 kept** for naming
Chicago, Cook County or Illinois · of those **501 name Chicago or Cook County** ·
1,302 distinct surname keys · **215 leads** across four layers (residents 109, census
1840 61, voters 38, structures 7) · **0 merges**.

Fewer kept cards than volume 1 (1,987 against 2,579) on more pages, and the reason is the
alphabet, not the reading: C-H carries the great English and New England surname runs —
Clark, Davis, Hall, Hall's compounds — whose cards are overwhelmingly eastern, while A-C
carried Andrews, Bailey, Brown, Burns and Butler, which the Chicago works cite heavily.
The Chicago-and-Cook share is nearly identical: 25.2 per cent of volume 2's kept cards
against 22.5 per cent of volume 1's.

## The reading order, over volumes 1 and 2

Ranked on Chicago and Cook County cards standing on a surname this project already holds:

| work | cards | Chicago/Cook | on a lead surname | held? |
|---|---|---|---|---|
| Andreas, *History of Chicago* (1884-6) | 760 | 579 | 123 | yes — `andreas_1884_v1` |
| **Moses and Kirkland, *History of Chicago, Illinois* (1895)** | 202 | 132 | **35** | **no** |
| Moses, *Illinois, historical and statistical* (1888-92) | 276 | 109 | 27 | no |
| La Salle Book Co., Cook County biographical volumes (1900, 1909) | 125 | 57 | 10 | no |
| Fergus, *Chicago directory for 1839* | 26 | 22 | 7 | yes |
| Reynolds, *The pioneer history of Illinois* (1887) | 30 | 1 | 1 | no |
| Hurlbut, *Chicago antiquities* (1881) | 2 | 2 | 0 | no |

**Volume 2 did not change the finding, it doubled it.** The index's Chicago cards point
at Andreas more than at everything else together, and this project already has Andreas.
The largest Chicago work it points at that this project does **not** hold is still Moses
and Kirkland's *History of Chicago* (1895): 132 Chicago and Cook County cards over the
two volumes, 35 of them under surnames already in the residents, the poll lists or the
1840 census — up from 76 and 16 on volume 1 alone. Both volumes are on the Internet
Archive (`historyofchicago01mose`, `historyofchicagov2mose`).

Volumes 3 and 4 are unread: T-0579, T-0580. Each wants its own hand-drawn precision
sample — a number carried over from another volume is not a measurement of it.
