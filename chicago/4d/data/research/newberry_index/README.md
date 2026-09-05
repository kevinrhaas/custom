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
| `lead_crosswalk.json` | `tools/rule_newberry_leads.py --write` | every lead in `leads.json` ruled on and anchored to the cards it stands on, over every volume read. Still no merges |
| `acquisition_list.json` | `tools/rule_newberry_leads.py --write` | the Chicago and Cook County cards whose citation the works table could not read — books, not leads |

This is research, not payload. `tools/publish.sh` does not copy `data/research/`, and
`tools/newspaper_corpus.py --check` asserts it stays out of `site/chicago/4d/`.

## How the volumes are read

The four PDFs are ~200 MB each and are **not committed**. Fetch one to a scratch path and
run:

    python3 tools/read_newberry_index.py --extract --volume 3 --pdf /tmp/newberry_v3.pdf
    python3 tools/read_newberry_index.py --parse   --volume 3
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
| 2 (C-H) | 40 | 39 | **0.975** | 20/20 | 19/20 |
| 3 (H-P) | 40 | 37 | **0.925** | 20/20 | 17/20 |
| 4 (P-Z) | 39 | 20 | **0.513** | 8/9 | 12/30 |

Those are the figures **after T-0600**, which struck 443 stanzas that name a locality and
no work. The draw is not re-thrown when a rule strikes cards: the struck rows leave this
sample and are replaced, in the same stratum, from the cards that remain, and every
replacement was adjudicated against the page image the same way the rest were. Before the
rules the four volumes read 0.975, 0.875, 0.900 and 0.475. `precision_sample.json`'s
per-volume `draw.maintained` names exactly which rows were replaced by which.

**The Chicago and Cook stratum held for three volumes and then missed once** — 68 of 69
across four — and all but one bad keep in any draw is in the Illinois-only stratum. That
matters because the Chicago and Cook County cards are the ones `follow_up.json` ranks the
reading order on. Volumes 1-3 are stratified 20/20 and the volumes are not, so weighted by
the population volume 2's estimate is 0.962 and volume 3's is 0.906; the figures in the
table are the ones comparable with each other. **Volume 4's row is not comparable with the
other three and must not be read as if it were**: that volume holds only ten Chicago-or-Cook
cards in all, so its first stratum is a census of them rather than a draw of twenty, and its
second was drawn to thirty. Read its two stratum figures, not its flat one — and read the
section on the volume below before spending anything it produced.

Volume 1's one bad keep used to be `nbi_v01_2226`, whose entire line is `I II.`; the
T-0600 rules struck it, and the row that replaced it is a bad keep of a different shape —
`nbi_v01_2418`, an English card, 'Ferne family. — Eng. (Misc. geneal. gleanings. (Waters,
H. F.) 1901: 2', whose reading opens `i ii. gleanings.` because 'Eng.' broke into three
strokes and a stop at the head of the line. A start-of-line stroke followed by a citation
is the one shape the new rules deliberately leave alone: a wrapped locality looks exactly
like it. Volume 2's five were **two classes, both since struck**:

- **The state banner absorbed as a card body** (four of the five). The index divides one
  family's run of cards by state with a printed rule, `ILLINOIS.`; when that rule falls
  directly under a heading, the extractor reads it as that card's body and keeps the
  stanza, which carries no citation at all. `nbi_v02_1675` is the proof the banner does
  not belong to the heading above it: the heading is 'Kinge or King family.', whose one
  card is an English parish register, and the surname run under the banner is KINGERY.
- **A call number read as a state** (the fifth). `nbi_v02_1106` is 'Holden family. —
  Hapgood fam. (Hapgood, W.) 1898. See index. E. 7. H 21', naming no locality; the
  `, III,` the pattern matched on is the wreck of a Newberry call number.

Volume 3's four were **one old class and three new ones, and every one of them is text
that is not on the card** (the sliver, `nbi_v03_0913`, is the one T-0600 struck):

- **A volume number in roman** — `nbi_v03_1443`, 'Pierce family. — John Dwight. (Dwight,
  B. W.) 1874. See Index III.' *See index III.* is a standing formula on these cards and
  points at the third volume of that genealogy's index; `, III.` is exactly the shape of
  `, Ill.`. It is the regnal problem in a second dress and it is commoner — two of the
  four cards in that one rendered window carry the formula.
- **The neighbouring column's sliver** — `nbi_v03_0913`, 'Murphy family. — Murray, T.H.
  Some voices from ye olden time. 1904', a card that names no place at all. The `Illinoi`
  that made it a keep is the first word of column 3's *Murphy family. — Illinois.* card,
  caught in the 200-point window over column 2. The same bleed put the wrong surname on
  `nbi_v03_1154`, an Onion card filed under the neighbour's *Onslow* — a good keep with a
  key that can never join a lead. Deduplication on (page, heading, body) cannot catch
  either, because a hybrid of two columns is not a duplicate of anything.
- **A stray mark at the start of a line** — `nbi_v03_1870` is a NEW ENGLAND card,
  'Richards family. — New England, First Settlers of. (Farmer, J.) 1829.', whose reading
  opens `lil.`. That is on no card; the `illinois_abbreviated` pattern anchors on
  start-of-line as well as on a comma, and the rule above the card satisfies it. Volume
  2's banner class and this are the same failure at two different sources.
- **The regnal class, through the rule written to stop it** — `nbi_v03_0653`,
  'Messendene family. — England. (Roberts, C., Ed. Calendarium, Hen. III. and Edw. I.
  1865.)', read by the photostat as `Calendafium, Han, iii. and i n .`. `REGNAL` wants
  the regnal name and a capitalised numeral; here neither survived. Volume 1 struck 35
  cards with that rule and volume 3 shows what it still lets through.

One more thing volume 3 shows that is not a precision error: on the widest pages the
printed column 3 begins left of the 519-point crop, and its headings lose their opening
letters — `nbi_v03_0849` is filed under `rtenoan` for a Mortensen card whose Cook County
citation is read correctly. The crop comment already records that page widths run 689 to
733 points; that is what the widest of them cost.

**T-0600 wrote the rules and re-read all four volumes under them** (2026-09-05). Two
refusals sit beside `REGNAL` in `tools/read_newberry_index.py`, both testing what a
stanza is MISSING rather than how a locality is spelled: `names_only_the_place` refuses a
body that carries the locality and no work at all — no word, no date — which is the state
banner and the wreck of a call-number column, and `call_number_slot` refuses a
start-of-line stroke with the next card's family heading behind it, which is
`nbi_v02_1106`. 443 stanzas left the four volumes: 154, 101, 127 and 61, of which 46 named
Chicago or Cook County. The rows they took out of this sample were replaced from the same
stratum and adjudicated fresh, and the classes the rules do NOT catch are named above —
they are what the four volumes' remaining bad keeps are made of. The same draw found a third thing that is not a precision error: a column
sliver is kept as a second, truncated copy of a card the neighbouring pass read in full
(`nbi_v02_1775` is `nbi_v02_1779` again), because the passes deduplicate on (page,
heading, body) and a truncated sliver never matches its full sibling. **T-0601** measures
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
2,830 of the 7,005 cards read so far. The 4,175 it does not reach are overwhelmingly Illinois
COUNTY histories — Chapman, LeBaron, Brink & McDonough, Baldwin, Murray Williamson,
Power — published by houses nobody has written a pattern for, and only **375** of them
name Chicago or Cook County. That residue is the weakest part of this reading and it is
counted rather than hidden: `follow_up.json` reports it in
`chicago_or_cook_cards_matching_no_known_work`.

## Volume 1 (A-C), read 2026-09-03 under T-0570

987 pages cropped and walked · **58,488 cards** assembled · **2,425 kept** for naming
Chicago, Cook County or Illinois · of those **562 name Chicago or Cook County** ·
1,615 distinct surname keys · **399 leads** across four layers (residents 196, census
1840 123, voters 62, structures 18) · **0 merges**. (Kept and Chicago/Cook are the
post-T-0600 figures — 2,579 and 581 before the rules. The lead count rose because the
re-parse ran against the project's people layers as they now stand, not because of the
rules.)

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

1,016 pages cropped and walked · **58,589 cards** assembled · **1,886 kept** for naming
Chicago, Cook County or Illinois · of those **492 name Chicago or Cook County** ·
1,258 distinct surname keys · **241 leads** across four layers (residents 129, census
1840 68, voters 37, structures 7) · **0 merges**. (1,987 and 501 before T-0600.)

Fewer kept cards than volume 1 (1,886 against 2,425) on more pages, and the reason is the
alphabet, not the reading: C-H carries the great English and New England surname runs —
Clark, Davis, Hall, Hall's compounds — whose cards are overwhelmingly eastern, while A-C
carried Andrews, Bailey, Brown, Burns and Butler, which the Chicago works cite heavily.
The Chicago-and-Cook share is nearly identical: 26.1 per cent of volume 2's kept cards
against 23.2 per cent of volume 1's.

## Volume 3 (H-P), read 2026-09-03 under T-0579

1,003 pages cropped and walked · **68,552 cards** assembled · **2,004 kept** for naming
Chicago, Cook County or Illinois · of those **503 name Chicago or Cook County** ·
1,411 distinct surname keys · **238 leads** across four layers (residents 115, census
1840 72, voters 43, structures 8) · **0 merges**. (2,131 and 520 before T-0600.)

The most cards assembled of any volume so far (68,552 against 58,488 and 58,589) on
1,003 pages, and the fewest kept per card: H-P is the densest stretch of the alphabet
and it is also the least Illinois one. The Chicago-and-Cook share, **25.1 per cent** of
the kept cards, sits between volume 1's 23.2 and volume 2's 26.1 — three volumes now
agree that about a quarter of what this index files under Illinois is filed under
Chicago or Cook County.

Volume 3's own contribution to the reading order is Andreas again, and one card that is
not: `nbi_v03_1030`, 'Nicholson family. — Chicago, Ill., Directory, 1839. (Fergus hist.
ser. 1876. no. 2.)', which turned up in the forty-card draw and points at the work
T-0506 is extracting.

## Volume 4 (P-Z), read 2026-09-03 under T-0580

918 pages cropped and walked · **6,548 cards** assembled · **247 kept** for naming
Chicago, Cook County or Illinois · of those **9 name Chicago or Cook County** ·
212 distinct surname keys · **51 leads** across four layers (residents 27, census
1840 10, voters 11, structures 3) · **0 merges**. (308 and 10 before T-0600, which took
this volume's tenth Chicago card with the rest: `nbi_v04_0094` really is 'Steen family. —
Chicago, Ill. (Andreas, A. T.) 1884-6', and its READING is `*5 ._.ChicAgo, m.
<.-...«..-.5.` — a locality and no work. A recall loss, named here because the sample
could see it.)

**Read those numbers against the other three volumes before using anything in them.**

| volume | pages | cards assembled | per page | kept | Chicago/Cook | precision |
|---|---|---|---|---|---|---|
| 1 (A-C) | 987 | 58,488 | 59 | 2,425 | 562 | 0.975 |
| 2 (C-H) | 1,016 | 58,589 | 58 | 1,886 | 492 | 0.975 |
| 3 (H-P) | 1,003 | 68,552 | 68 | 2,004 | 503 | 0.925 |
| **4 (P-Z)** | **918** | **6,548** | **7** | **247** | **9** | **0.513** |

A rendered page of this volume carries about a hundred cards, so volumes 1-3 assemble
roughly 60 per cent of what is printed and volume 4 assembles seven. **The cause is the
deposited file, not this project's reading**, and both halves of that were tested rather
than asserted:

- **The text layer is a different and much worse scan.** The card that prints `Stoddard
  family.` comes back as `s:'o'ddnrdmany.`, `Btoddaxd family.`, `seoddu-d luuy.` and
  `'I "odd."`; the heading rule needs the family word as a token of its own and gets it
  perhaps one time in six. Volume 4 is also the one file in the Internet Archive item
  without the Newberry's scan id — `130151_04.pdf` beside `FL2091539_CP-130151_01.pdf`
  and its two fellows — so a different digitisation is the likely reason.
- **The crop geometry was measured and ruled out.** Every word box on sixty pages puts
  this volume's gutters at 192, 348 and 508 points, and the shared 200-point windows on a
  173-point pitch contain each column whole. Boxes cut to the measured gutters moved
  heading detection from 576 to 616 over the same 61 pages — 7 per cent, against an
  eight-fold shortfall. The shared boxes were therefore **kept**, and this volume is read
  by exactly the method volumes 1-3 were, which is what makes the table above mean
  anything.

The forty-card draw says the same thing from the other end. Chicago-and-Cook scores
**0.900** — one bad keep in ten, the column sliver, which is volume 2's and volume 3's
number — and Illinois-only scores **0.333**. Six classes of bad keep, five of them already
named in this file (the column sliver, `See Index III.`, the state banner, a bare body of
mush, and a call number or stray mark read as the abbreviation) and one new: **a page
number**. `nbi_v04_0183` is 'Woodruff fam. (Woodruff, F.E.) 1902:117' and the `117` came
back as `111,`; the anchor the pattern carries does not catch it, because the OCR supplies
the comma in front of the strokes.

And the ten Chicago cards are themselves a floor. Three of the ten good keeps in the
Illinois-only stratum are Chicago cards the `chicago` pattern missed — `Chicngo`, `Gkgo`,
`Chh:|go` — none of which it will take, because it wants i, l or 1 in the second and third
places. Three in thirty sampled, over 298 Illinois-only cards, puts the true figure nearer
thirty than ten. The pattern is not widened to chase them: at this text quality a wider one
would take page numbers with them.

**T-0613 carries the repair, and it is demonstrated rather than hoped for.** `tesseract` on
a 300 dpi render of page 300 returns `Stoddard family.` card after card where the text layer
returns mush. It costs about 8.5 s a page to render and 6.3 s a page to read — some 3.8
hours for 918 pages — which is more than one run's foreground budget, and is why this
ticket read the volume as deposited and measured what that is worth instead of quietly
shipping a thin reading as a whole one. Until T-0613 lands, **volume 4's cards are not worth
what volumes 1-3's are**, and `coverage.json` says so on its declaration.

### The reader that repair needs, built and measured under T-0618

T-0613 has been split, and its first piece is done: the reader exists, and what it
recovers is now a measured number rather than a demonstration on one page.
`text/vol_04_probe.json` is that measurement, written by
`--probe --volume 4 --pdf <path>` so it can be re-run and disagreed with. Eight pages
spread through the volume — 100, 200, … 800 — read BOTH ways:

| | text layer | OCR |
|---|---|---|
| cards assembled | 36 | **278** (7.7×) |
| locality cards kept | 0 | **4** |
| characters emitted | ~59,000 a page | ~12,000 a page |

The character counts are the telling part and they confirm what the section above
diagnosed from the other end. The text layer is not short of characters; it has five
times as many and finds eight times fewer cards. They are in the wrong places.

    python3 tools/read_newberry_index.py --extract --ocr --volume 4 --pdf <path> --pages 1-110
    …one command per range, until every page is covered…
    python3 tools/read_newberry_index.py --extract --ocr --volume 4 --pdf <path>
    python3 tools/read_newberry_index.py --parse   --volume 4

Each page is rendered by `pdftoppm` and cropped into the **same four column windows** the
pdftotext path uses — the boxes the section above measured and kept — each strip is read
by tesseract at `--psm 6`, and the four column texts go to the same card assembly. The
two readers differ only in where the characters come from, and the grade does not move:
`transcription_mediated` was already the right grade for a machine reading a photostat,
and a second machine reading it does not make it stronger.

**It is resumable because it has to be.** `--pages A-B` reads a range and commits a shard
under `text/ocr/vol_04/`; `--extract --ocr` with no range stitches every committed shard
in page order and assembles. A shard records the engine, dpi, psm and crop boxes it was
made with, and stitching **refuses** a set that disagrees, or a set with a gap — two
ranges read at different settings are two readings of one volume, and a volume assembled
over a gap is a partial read wearing a finished volume's file name. `--check` then holds
the shards to the sha256 MANIFEST recorded for them, in both directions: named and
missing, committed and unnamed.

**The 3.8 hours the section above quotes is not what it costs.** That figure is 300 dpi,
one page at a time. Two changes bring it to about **84 minutes**: 200 dpi, which loses
nothing at this card size, and `OMP_THREAD_LIMIT=1`. The second is not a detail —
tesseract parallelises a single image across the cores by itself, so four page workers on
a four-core runner oversubscribe it three times over and the machine thrashes. Measured
here: four workers at tesseract's default threading did not finish eight pages in ten
minutes, and the same four workers with the limit set did four pages in 21.7 s. 5.5 s a
page against 17.5 s sequential. Page-level parallelism only pays when the engine
underneath it is single-threaded.

Eighty-four minutes is still more than one run's foreground, which is why T-0613's
remaining pieces cut the volume into three page bands (T-0619, T-0620, T-0621) that commit
shards one at a time. **Volume 4's committed reading stays the 308-card text-layer one
until all three are in** — a partial OCR read would be a third state of the volume and
worse than either.

## The reading order, over all four volumes

Ranked on Chicago and Cook County cards standing on a surname this project already holds:

| work | cards | Chicago/Cook | on a lead surname | held? |
|---|---|---|---|---|
| A. T. Andreas, *History of Chicago, from the earliest period to the present time* (1884-1886) | 1127 | 898 | 210 | yes — `andreas_1884_v1` |
| **John Moses and Joseph Kirkland, *History of Chicago, Illinois* (1895)** | 299 | **193** | 68 | **no** |
| John Moses, *Illinois, historical and statistical* (1888-92) | 418 | 169 | 97 | no |
| La Salle Book Co., *The biographical and portrait volumes of Cook County* (1900, 1909) | 179 | 91 | 34 | no |
| Robert Fergus, *Chicago directory for 1839* (Fergus' Historical Series, 1876) | 31 | 27 | 13 | yes — `fergus_chicago_directory_1839` |
| John Reynolds, *The pioneer history of Illinois* (1887) | 47 | 1 | 16 | no |
| H. F. Kett & Co., *County histories published by H. F. Kett & Co. and its successors* (1877-1880) | 711 | 2 | 117 | no |
| Henry H. Hurlbut, *Chicago antiquities* (1881) | 2 | 2 | 0 | no |
| Illinois Society, S.A.R., *Sons of the American Revolution year book* (1896) | 156 | 0 | 32 | no |
| Century Publishing and Engraving Co., *Encyclopedia of biography of Illinois* (1892-1902) | 57 | 0 | 11 | no |

**Four volumes have not changed the finding.** The index's Chicago cards point at Andreas
more than at everything else together — 898 of the 1,612 Chicago and Cook County cards read
so far — and this project already has Andreas. The largest Chicago work it points at that
this project does **not** hold is still Moses and Kirkland's *History of Chicago, Illinois*
(1895): 193 Chicago and Cook County cards, up from 192 on three volumes, 132 on two and 76
on one. Both volumes are on the Internet Archive (`historyofchicago01mose`,
`historyofchicagov2mose`).

Volume 4 moved every one of those numbers by single digits, and that is the point rather
than an anticlimax: P-Z is a quarter of the alphabet and it contributed ten Chicago-or-Cook
cards where H-P contributed 520. The ranking above is, for now, a ranking over three
volumes and a fragment; **T-0613**'s re-read is what will let the fourth speak.

Of the 7,005 cards read, **4,175** cite a work no pattern in the table reaches, and only
**375** of those name Chicago or Cook County. `acquisition_list.json` carries them.

## Every lead is ruled on, over four volumes

T-0590 built the ladder and ruled volume 1's 319 leads; T-0578 read volume 2 and ruled the 227 it adds;
T-0579 read volume 3 and ruled the 191 it adds; T-0580 read volume 4 and ruled the 51 it adds — each
under the same ladder and in the same PR as its
read, because T-0590's gate fails the moment a volume offers a lead nobody has answered.
`tools/rule_newberry_leads.py` reads every `entries_vol_*.json` now rather than volume 1's alone.

| outcome | vol 1 (T-0590) | vols 1-2 (T-0578) | vols 1-3 (T-0579) | vols 1-4 (T-0580) |
|---|---:|---:|---:|---:|
| leads ruled | 319 | 546 | 737 | **788** |
| cards anchored | 542 | 947 | 1,250 | **1,294** |
| candidate — `testable_in_a_held_work` | 79 | 146 | 188 | **190** |
| refused — `ocr_variant_only` | 129 | 208 | 279 | 292 |
| refused — `locality_absent` | 90 | 144 | 206 | 242 |
| refused — `surname_only_chicago` | 21 | 48 | 64 | 64 |
| **matched** | **0** | **0** | **0** | **0** |
| discriminators found | 0 | 0 | 0 | 0 |

`matched` stays reachable and unreached: the test is run over all 1,294 cards, not assumed — every
forename this project holds for a candidate is searched for in the card text, and four volumes have
turned up none. The acquisition list grows from 166 Chicago and Cook cards whose citation matched no
work, to 274 on two volumes, to 369 on three, to **375** on four, 81 of them still carrying a year the
photostat left legible. Volume 4 adds 51 leads and 6 acquisition-list cards against volume 3's 191 and
95 — the shortfall this file's volume 4 section measures, showing up on the other side of the ledger.

The lead ids keep the form `lead_v01_*` … `lead_v04_*`, numbered by the FIRST volume the
surname appears in, because `lead_crosswalk.json` anchors its rulings to them and a surname filed in more
than one volume must keep the id its ruling was anchored to. A merged row's `entries` carry every
volume's cards.

### Volume 1's half of it, ruled 2026-09-03 under T-0590

A lead offered and never answered reads exactly like a lead nobody has looked at, and
that is what `tools/measure_research_spend.py` found: 2,619 units read here, **0 ruled
on** — the project's largest unspent read. `lead_crosswalk.json` closes it. Every one of
the 319 leads carries a verdict, and every verdict is anchored to a card and, where the
heading picks out exactly one of them, to the person in the town it reaches.

| outcome | leads | why |
|---|---:|---|
| refused — `ocr_variant_only` | 129 | no candidate reaches the heading by an exact surname key; the heading is not certainly that surname at all |
| refused — `locality_absent` | 90 | every card under the heading names Illinois and neither Chicago nor Cook County |
| refused — `surname_only_chicago` | 21 | a Chicago card on an exact surname, waiting on a work nobody here holds |
| candidate — `testable_in_a_held_work` | 79 | a Chicago card on an exact surname citing Andreas or the 1839 directory — answerable without acquiring anything |
| **matched** | **0** | — |

**`matched` is reachable and volume 1 does not reach it.** The one thing that could lift a
lead off a bare surname is a forename on the card, so the tool looks for one rather than
asserting there is none: every forename this project holds for a candidate is searched for
in the card text, with the surname's own OCR variants and the locality words filtered out
because 'Cook' on a Cook County card and 'Cary' under a Carey heading are not forenames.
`counts.discriminators_found` is **0** across all 542 cards. A later volume that does yield
one raises it for a hand ruling; it never merges on it.

The 319 leads stand on **542 distinct cards**, and the spend measure counts cards rather
than leads because it dedupes on the anchor — a card standing under both the residents and
the voters layer has been looked at once. So that ticket spent 542 and brought the domain's
ceiling in `tools/research_spend_baseline.json` down from 2,619 to 2,077, which PR #727's
recount restated as 1,753 on 866 units; volume 2's read and ruling together take the
ceiling to **3,148** on 1,498 spent.

`acquisition_list.json` is the other half of the finding and is deliberately not a lead
list: over both volumes, 274 Chicago and Cook County cards whose citation matched no work in
the table (166 of them volume 1's), and only 60 of them still carry a publication year the
photostat left legible. They point at books, and three of the books
already have tickets — T-0581, T-0582, T-0583.

All four volumes are read. Volume 4 is read and its reading is poor, and the poverty is the
source's rather than the method's — see its section above and **T-0613**, which carries the
re-OCR that recovers the cards its text layer loses.
