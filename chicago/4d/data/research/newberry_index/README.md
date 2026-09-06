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
| `text/vol_NN_locality_cards.txt` | `--extract` | the kept cards, verbatim as the reading gives them, two lines each: the heading, then the body line that named a locality. Volumes 1-3 are read from the text layer; volume 4 from the page images (`--ocr`) |
| `text/ocr/vol_04/pages_*.json.gz` | `--extract --ocr --pages A-B` | the OCR reading of volume 4, one shard per page range, committed because the volume they were read from is not. `--check` holds them to MANIFEST's sha256 in both directions |
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

Volumes 1-3 carry a usable text layer, so no OCR pass of our own is needed on them —
volume 4's does not, and its section below is the whole story of that — but `pdftotext
-layout` alone is useless even on the good ones. A page is four columns of card images, and `-layout`
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
| 4 (P-Z) | 40 | 39 | **0.975** | 20/20 | 19/20 |

Volumes 1-3 are the figures **after T-0600**, which struck 443 stanzas that name a locality
and no work. The draw is not re-thrown when a rule strikes cards: the struck rows leave this
sample and are replaced, in the same stratum, from the cards that remain, and every
replacement was adjudicated against the page image the same way the rest were. Before the
rules those three volumes read 0.975, 0.875 and 0.900. `precision_sample.json`'s per-volume
`draw.maintained` names exactly which rows were replaced by which.

**Volume 4's row is a different reading, not a maintained draw.** Its text-layer reading
scored 0.475, and 0.513 after T-0600 struck eight of its forty. T-0775 re-assembled the
volume out of the OCR shards, which rewrote every card in it, so no verdict could be
carried across: the forty above are a fresh draw over the re-read volume, adjudicated the
same way. The old figures are kept under `volumes.4.supersedes` in `precision_sample.json`,
where they measure the reader they belong to and enter no total.

**The Chicago and Cook stratum has not missed once** — 80 of 80 across the four volumes,
and every bad keep in every draw is in the Illinois-only stratum. That matters because the
Chicago and Cook County cards are the ones `follow_up.json` ranks the reading order on. All
four draws are stratified 20/20 while the volumes themselves are not, so weighted by the
population volume 2's estimate is 0.962 and volume 3's is 0.906; the figures in the table
are the ones comparable with each other.

**The warning that volume 4's row was not comparable with the other three is WITHDRAWN.**
It stood because the text-layer reading of that volume held only ten Chicago-or-Cook cards
in all, so its first stratum was a census of them rather than a draw of twenty and its
second was drawn to thirty. The re-read volume holds 207 Chicago-or-Cook cards and 206
others, it is stratified 20/20 like the rest, and its flat figure may now be read beside
theirs.

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
sliver is kept as a second, truncated copy of a card the neighbouring pass read in full,
because the passes deduplicate on (page, heading, body) and a truncated sliver never
matches its full sibling. **T-0601 measured how many: nine, over all four volumes**, and
the section below carries the figure and the rule. And volume 2 showed the sample cannot measure recall: `nbi_v02_0937` is a
Chicago card — 'Henrotin family. — Chicago, Ill. (Andreas, A. T.) 1884-6' — whose body
lost the word 'Chicago', so it is bucketed Illinois-only and is missing from the 501. The
Chicago-and-Cook counts are a floor, not a count.

**T-0765 added the third refusal: a page number standing where the state stands**
(2026-09-06). A card's citation ends in the pages the surname is on, printed as a
comma-separated list — `1897: 130,111,183,186,371` — and `illinois_abbreviated` is
anchored to a comma, so the list supplies its own anchor and every citation that reaches
page 111 was kept as an Illinois card. So was the illustration note: `(Delano, J. A.)
1899: 203,ill.` is page 203, illustrated. T-0600 measured the class in passing and would
not ship the obvious rule, because refusing on *any* preceding digit takes real Chicago
cards with it — this OCR reads a trailing `o` as `0`, and `««g0, III.` and
`> — Chiear.0, 111.,` are both *Chicago, Ill.*

`page_number_slot` tests the narrower shape T-0600 proposed and never measured: a run of
**two or more** digits ending at the anchor with no letter immediately in front of it. A
page list always presents that shape; a fallen letter presents one digit. Over the
committed text it strikes **32 cards — 11, 9, 9 and 3** across the four volumes, and
every one was read against its body: all 32 are page lists or illustration notes, none is
a locality. It cannot reach a Chicago or Cook County card by construction, because it
disables one bucket and a card with any other locality bucket keeps it — and the counts
bear that out, `chicago_or_cook_cards` holding at 562, 491, 502 and 207 across the strike.
The stratum genuinely at risk is the wrecked `Chicago` that reaches the file only through
the abbreviation, and the two the ticket names are the two the digit-run test spares; both
are self-test cases now.

**What it deliberately leaves.** 21 further cards precede the anchor with a digit and are
not struck — mostly page lists whose last run this OCR ran into the word in front of it,
`1899il09,lll,113.`. Dropping the letter guard to reach them takes exactly **two** more
cards across all four volumes, measured rather than guessed, and spends the one test that
tells a fallen letter from a number to do it. The trade was refused. None of the 32 was in
the 160-card precision sample, so no verdict was re-made and no precision figure moved;
152 of the 160 rows were re-anchored, because the record id is positional and striking a
card renumbers every card behind it.

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
3,068 of the 6,688 cards read so far. The 3,620 it does not reach are overwhelmingly Illinois
COUNTY histories — Chapman, LeBaron, Brink & McDonough, Baldwin, Murray Williamson,
Power — published by houses nobody has written a pattern for, and only **365** of them
name Chicago or Cook County. That residue is the weakest part of this reading and it is
counted rather than hidden: `follow_up.json` reports it in
`chicago_or_cook_cards_matching_no_known_work`.

## The column sliver, measured and marked — T-0601

The four crop windows are **200 points wide on a 173-point pitch**, so every window
carries the leftmost **27 points of the next column**. A card sitting on that boundary is
therefore read twice: in full by the pass over its own column, and as a short truncated
fragment by the pass over the column to its left. `assemble()` deduplicates on
`(page, heading, body)`, and a truncation is equal to nothing, so the fragment survives as
a second card of the same locality and the domain counts one card twice.

**The measurement came before the rule, and it decided the rule's shape.**

| test | pairs found | at column delta +1 | at any other delta |
|---|---|---|---|
| body a prefix of another body under `alpha()`, any column | 17 | 10 | 7 |
| the same, byte-exact under `collapse()`, any column | 9 | **9** | **0** |

The second row is the rule. Two things fall out of it and both are load-bearing:

- **The match has to be byte-exact, not `alpha()`-folded.** A sliver is the *same ink read
  twice by the same engine*, so the reader's own errors come through verbatim — `Pike Ce,
  III.`, `Füa Co., III.`, `Chicago, in.`. `alpha()` drops the digits and the stops, and
  once it does, two genuinely different cards citing one county history collapse into a
  match: `Sangamon Co, III. (Power, J. C.) 1878.` and `Sangamon Co, III, (Power, J. C.)
  I876.` are one string under `alpha()` and are two readings on the leaf. Seven of the
  seventeen loose matches are that mistake.
- **Column adjacency is measured, not assumed.** Under the byte-exact test every one of
  the nine pairs stands at delta **+1** and not one stands at +2, +3 or 0 — which is
  exactly what the 27-point overlap predicts, and is why the clause is in the rule.

Nine pairs over the 6,533 kept rows those readings now stand at (T-0601 measured them over
6,562, before T-0765 struck 32): three in volume 1, one in volume 2, four in volume 3 and
one in volume 4's text-layer reading.

**A sliver is marked, never dropped**, and there are three reasons:

1. The record id is positional (`nbi_v01_0708`), so striking one renumbers every card
   after it and orphans `precision_sample.json`'s hand-adjudications and
   `lead_crosswalk.json`'s 1,248 rulings.
2. The ink is real and was really read. `check()` rebuilds every `as_read` out of the
   committed text, which still carries the sliver at its own line numbers; deleting the
   record would leave the reading and the records disagreeing about what is on the leaf.
3. A wrong call stays visible and reversible instead of silently removing a card.

So the record keeps its place and gains `normalized.sliver_of`, naming the card it
truncates, and it is withheld from the volume's counts, from the leads and from the
reading order. `counts` now carries all three figures — `records` (rows in the file),
`slivers` (marked), `cards` (what the volume read) — so nothing is hidden behind one
number.

The gate runs **both ways**, and the second half is the one that earns its keep: a record
that calls itself a sliver has to be one on the committed text, **and every sliver the
committed text carries has to be marked**. Without that second clause a records file
parsed before this rule existed goes on counting one card twice and nothing says so.
Three cases in `--self-test` cover it: a sliver unmarked, a card marked a sliver of one it
does not truncate, and a volume counting its slivers as cards.

**Not one of the 160 adjudicated precision rows is a sliver**, so no row leaves the sample
and every precision figure in this file is unchanged. That is the sense in which this is a
count defect and not a reading defect.

**What this rule does NOT catch, and a caution about a claim it disproves.**
`coverage.json` said volume 2's one remaining bad keep was "a column sliver of the shape
T-0601 carries". It is not. `nbi_v02_0610` — `Hallam | , 111.19 Hallam faaily.` — opens
with `, 111.19`, which is the **tail** of the card in the column to its *left*
(`Hall | -±~2.' la letk» te,'», 111.19`). That is the mirror artefact: a window catching
the right edge of the previous column on a page wide enough to push it past the boundary,
and it contaminates a body rather than duplicating a card. A first pass found **117**
candidates at a byte-exact run of six characters, an upper bound and not a measurement.
It is measured in the section below.

### The bled-in prefix, measured and withheld (T-0769)

**The artefact.** A crop window is 200 points wide on a 173-point pitch, and page widths
in a volume run from 689 to 733 points. On a wide page the PREVIOUS column's text is
pushed past the boundary and the window catches its right edge — not as a card of its
own, which is T-0601's sliver, but glued to the FRONT of a real card's body. The locality
patterns then match on ink that is not on that card.

**The test, and why length alone will not do it.** T-0601's argument run the other way:
the fragment is the SAME INK READ TWICE BY THE SAME ENGINE, so the run must be
byte-exact — not alpha-folded, because the damage is the evidence — and long enough that
two independent cards could not both reach it. Six byte-exact characters finds 113
candidates and most are a common formula: `Chicago,` opens **519** bodies in this domain,
`Illinois` 285, `Cook Co.` 274, `Pike Co., Ill.` 34. So the run must also be **unique** —
the prefix of no other body in the four volumes — and that clause, not the length, is
what makes it this ink rather than that formula.

**The figure, with the delta profile beside it.** **47 cards** over the four volumes —
26, 14, 7 and 0 — and **every one of them at column delta +1**: the contaminated card
sits one column to the RIGHT of the body its prefix closes, which is the crop geometry's
own prediction. **None at any other delta.** The same test without the uniqueness clause
finds 113, of which 3 sit at delta 0, where a column cannot bleed into itself and the
artefact is impossible. That control channel is empty under the rule and populated
without it, which is the sense in which the rule has found the artefact and not a word.
Asked per volume instead of over the domain the rule finds 53, and the six it adds are
the formula class exactly (`Carroll Co., Ill,`, `Pika Co., III.`, `hicago, III`); marking
a sound card is worse than missing a contaminated one, so the corpus is the domain.

**43 of the 47 have no locality of their own.** Strip the fragment and nothing on the
card names Chicago, Cook County or Illinois — `nbi_v01_0845` is `y.dwn, Co., III.` from
the card to its left followed by ` (Murray, Williamson & Phelps, Publ.) 1870:`, and the
locality it was kept for was never on it. Those 43 are withheld from the volume's counts,
from the leads and from the reading order, exactly as a sliver is. The other four name
their locality on their own text as well, so the contamination cost them nothing and they
keep their place.

**Marked, not trimmed, and the choice is forced.** Trimming the body would edit a
reading, and `MANIFEST.text_sha256` and `check()` would both refuse it — rightly, because
a reading this project has tidied is a reading nobody can check. So the record keeps its
place and gains `normalized.bled_in_from`, `bled_in_run` and `locality_is_borrowed`, for
the same three reasons a sliver is marked rather than dropped: the id is positional, the
ink is real, and a wrong call must stay visible. The gate runs **both ways** here too,
and six cases in `--self-test` cover the geometry — the fragment one column right, a
shared formula in the column alongside, the card it would have been read off, a page
boundary, the locality really being on the fragment, and a run that repeats in the
corpus.

**Only one of the 160 adjudicated precision rows is affected** — `nbi_v02_0610`, volume
2's one remaining bad keep, which is now withheld — so no other row leaves the sample and
no other precision figure in this file moves.

| | before T-0769 | after |
|---|---|---|
| cards, all four volumes | 6,688 | **6,645** |
| distinct surname keys | 4,576 | **4,548** |
| leads | 974 | **971** |

The lead count does not move: a surname the withheld cards carried is carried by a sound
card too, so what leaves is 28 surname keys that stood on nothing else and the cards the
surviving leads are anchored on. `lead_crosswalk.json` and `acquisition_list.json`
re-derive byte-identically.

## Volume 1 (A-C), read 2026-09-03 under T-0570

987 pages cropped and walked · **58,488 cards** assembled · **2,414 kept** for naming
Chicago, Cook County or Illinois, of which 3 are column slivers, so **2,411 cards** ·
of those **562 name Chicago or Cook County** ·
1,605 distinct surname keys · **398 leads** across four layers (residents 196, census
1840 123, voters 62, structures 17) · **0 merges**. (Kept and Chicago/Cook are the
post-T-0600 figures — 2,579 and 581 before the rules. T-0601's re-parse moved the lead
counts again, and almost none of that is T-0601: run against today's people layers the
four volumes reach 401, 246, 242 and 53 leads WITH their slivers and 400, 246, 242 and 53
without, so the rise from the committed 399, 241, 238 and 51 is the residents, voters and
1840 heads having grown since each volume was last parsed, and striking the slivers costs
exactly one lead, in volume 1. The lead count rose because the
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

1,016 pages cropped and walked · **58,589 cards** assembled · **1,877 kept** for naming
Chicago, Cook County or Illinois, of which 1 is a column sliver, so **1,876 cards** ·
of those **491 name Chicago or Cook County** ·
1,252 distinct surname keys · **243 leads** across four layers (residents 126, census
1840 72, voters 37, structures 8) · **0 merges**. (1,987 and 501 before T-0600.)

Fewer kept cards than volume 1 (1,877 against 2,414) on more pages, and the reason is the
alphabet, not the reading: C-H carries the great English and New England surname runs —
Clark, Davis, Hall, Hall's compounds — whose cards are overwhelmingly eastern, while A-C
carried Andrews, Bailey, Brown, Burns and Butler, which the Chicago works cite heavily.
The Chicago-and-Cook share is nearly identical: 26.2 per cent of volume 2's kept cards
against 23.3 per cent of volume 1's.

## Volume 3 (H-P), read 2026-09-03 under T-0579

1,003 pages cropped and walked · **68,552 cards** assembled · **1,995 kept** for naming
Chicago, Cook County or Illinois, of which 4 are column slivers, so **1,991 cards** ·
of those **502 name Chicago or Cook County** ·
1,402 distinct surname keys · **238 leads** across four layers (residents 113, census
1840 75, voters 42, structures 8) · **0 merges**. (2,131 and 520 before T-0600.)

The most cards assembled of any volume so far (68,552 against 58,488 and 58,589) on
1,003 pages, and the fewest kept per card: H-P is the densest stretch of the alphabet
and it is also the least Illinois one. The Chicago-and-Cook share, **25.2 per cent** of
the kept cards, sits between volume 1's 23.3 and volume 2's 26.2 — three volumes now
agree that about a quarter of what this index files under Illinois is filed under
Chicago or Cook County.

Volume 3's own contribution to the reading order is Andreas again, and one card that is
not: `nbi_v03_1030`, 'Nicholson family. — Chicago, Ill., Directory, 1839. (Fergus hist.
ser. 1876. no. 2.)', which turned up in the forty-card draw and points at the work
T-0506 is extracting.

## Volume 4 (P-Z), read 2026-09-03 under T-0580, RE-READ BY OCR 2026-09-05 under T-0775

918 pages rendered and read by tesseract · **33,357 cards** assembled · **410 kept** for
naming Chicago, Cook County or Illinois · of those **207 name Chicago or Cook County** ·
342 distinct surname keys · **106 leads** across four layers (residents 50, census 1840
39, voters 14, structures 3) · **0 merges** · precision **0.975** on a fresh forty.

The section that follows is kept in two halves on purpose. The first is what the volume's
own text layer was worth, measured rather than asserted, and it is the reason the OCR
reader was built at all. The second is what the re-read did to those numbers. Neither is
deleted: a project that only records its final figure cannot show that it earned it.

| volume | pages | cards assembled | per page | kept | column slivers | borrowed locality | cards | Chicago/Cook | precision |
|---|---|---|---|---|---|---|---|---|---|
| 1 (A-C) | 987 | 58,488 | 59 | 2,414 | 3 | 24 | 2,387 | 561 | 0.975 |
| 2 (C-H) | 1,016 | 58,589 | 58 | 1,877 | 1 | 12 | 1,864 | 489 | 0.975 |
| 3 (H-P) | 1,003 | 68,552 | 68 | 1,995 | 4 | 7 | 1,984 | 502 | 0.925 |
| 4 (P-Z), text layer | 918 | 6,548 | 7 | 247 | 1 | not checked | 246 | 9 | 0.513 |
| **4 (P-Z), OCR** | **918** | **33,357** | **36** | **410** | **not checked** | **0** | **410** | **207** | **0.975** |

`kept` is the rows in the committed text; `cards` is what the volume actually read, which
is `kept` less the column slivers T-0601 marked and the cards T-0769 found borrowing their
only locality from the column to their left. The precision figures are unchanged: not one
of the 160 adjudicated rows is a sliver, and the one that is a bled-in prefix
(`nbi_v02_0610`) was already adjudicated `not_demonstrated`, so no row leaves the sample
and no number in it moves.

The OCR re-read of volume 4 (T-0775) carries **no sliver count**, and the blank is
deliberate rather than a zero. T-0601's pass ran over the text-layer reading; the re-read
rewrote every card in the volume, so that pass does not describe it and nothing has yet
looked for slivers in the 33,357 cards it assembled. Its `cards` column therefore repeats
`kept` because none have been deducted, not because none exist.


**Volume 4's row is the OCR one.** It is what `records/entries_vol_04.json` holds, what
`leads.json` and `follow_up.json` are parsed from, and what the table in the precision
section above reports. The text-layer row is history.

### What the text layer was worth (T-0580)

A rendered page of this volume carries about a hundred cards, so volumes 1-3 assembled
roughly 60 per cent of what is printed and volume 4's text layer assembled seven. **The
cause was the deposited file, not this project's reading**, and both halves of that were
tested rather than asserted:

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

The forty-card draw said the same thing from the other end. Chicago-and-Cook scored
**0.900** — one bad keep in ten, the column sliver, which was volume 2's and volume 3's
number — and Illinois-only scored **0.333**. Six classes of bad keep, five of them already
named in this file (the column sliver, `See Index III.`, the state banner, a bare body of
mush, and a call number or stray mark read as the abbreviation) and one new: **a page
number**. `nbi_v04_0183` is 'Woodruff fam. (Woodruff, F.E.) 1902:117' and the `117` came
back as `111,`; the anchor the pattern carries does not catch it, because the OCR supplies
the comma in front of the strokes.

And the ten Chicago cards were themselves a floor. Three of the ten good keeps in the
Illinois-only stratum are Chicago cards the `chicago` pattern missed — `Chicngo`, `Gkgo`,
`Chh:|go` — none of which it will take, because it wants i, l or 1 in the second and third
places. Three in thirty sampled, over 298 Illinois-only cards, put the true figure nearer
thirty than ten. The pattern was not widened to chase them: at that text quality a wider
one would have taken page numbers with them. (The re-read below settles the question the
other way: the figure is 207, and the estimate was short because it could only be made
over the cards that reading had already found.)

**T-0613 carried the repair, and it was demonstrated rather than hoped for.** `tesseract` on
a 300 dpi render of page 300 returns `Stoddard family.` card after card where the text layer
returns mush. It costs about 8.5 s a page to render and 6.3 s a page to read — some 3.8
hours for 918 pages — which is more than one run's foreground budget, and is why T-0580
read the volume as deposited and measured what that was worth instead of quietly shipping
a thin reading as a whole one.

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
shards one at a time. Volume 4's committed reading stayed the 308-card text-layer one
until all three were in — a partial OCR read would have been a third state of the volume
and worse than either.

### What the re-read did (T-0775)

Twelve shards cover pages 1-918 — T-0619 read 1-306, T-0620 read 307-612, T-0769 read
613-918 — and `--extract --ocr --volume 4` with no range stitched them, assembled the
volume out of them and replaced `text/vol_04_locality_cards.txt`. The whole stitch takes
eight seconds: the eighty-four minutes were spent in the three runs that made the shards,
which is exactly what committing them was for.

| | text layer | OCR | |
|---|---|---|---|
| cards assembled | 6,548 | **33,357** | 5.1× |
| cards a page | 7 | **36** | against 59, 58, 68 in volumes 1-3 |
| locality cards kept | 247 | **410** | 1.7× |
| naming Chicago or Cook County | 9 | **207** | 23× |
| distinct surname keys | 212 | **342** | |
| leads offered | 51 | **106** | |
| precision, forty cards | 0.513 | **0.975** | a fresh draw, no verdict carried |

**Half of this volume's kept cards name Chicago or Cook County** — 207 of 410, 50.5 per
cent, where volumes 1, 2 and 3 run 23.3, 26.2 and 25.2. That is not a rule change; it is
what P-Z looks like once the reader can resolve the word. `Chicago` and `Cook` are short,
common and distinctive, and a text layer that scattered word boxes across the page lost
them at the same rate it lost everything else — but the Illinois abbreviation survived
mangling far better, because `Ill.` needs only three strokes to look right. The text-layer
reading was therefore not merely thin, it was thin in a *biased* way, and the bias ran
against the exact cards this project wants.

Volume 4 still assembles 36 cards a page against volumes 1-3's 59-68, so the OCR reading
is not the equal of a good text layer and this file does not claim it is. What the
forty-card draw says is narrower and firmer: of the cards it does keep, 39 in 40 really do
name the locality they were kept for, which is the best figure any volume in this domain
has been measured at.

**Volumes 1-3 were not re-read here, and the probe does not say they should be.**
`vol_04_probe.json` measured this volume, whose text layer emits five times the characters
and finds eight times fewer cards — the signature of boxes in the wrong places. Volumes
1-3 show no such signature: their text layers assemble 59, 58 and 68 cards a page and
measure 0.975, 0.975 and 0.925. Re-reading them would cost about four hours of compute
each to test a hypothesis nothing supports. If anyone wants it tested rather than argued,
`--probe --volume N --pdf <path>` is the command, and it is eight pages, not a volume.

## The reading order, over all four volumes

Ranked on Chicago and Cook County cards standing on a surname this project already holds:

| work | cards | Chicago/Cook | on a lead surname | held? |
|---|---|---|---|---|
| A. T. Andreas, *History of Chicago, from the earliest period to the present time* (1884-1886) | 1231 | 1010 | 261 | yes — `andreas_1884_v1` |
| **John Moses and Joseph Kirkland, *History of Chicago, Illinois* (1895)** | 337 | **228** | 86 | **no** |
| John Moses, *Illinois, historical and statistical* (1888-92) | 460 | 202 | 119 | no |
| La Salle Book Co., *The biographical and portrait volumes of Cook County* (1900, 1909) | 188 | 91 | 41 | no |
| Robert Fergus, *Chicago directory for 1839* (Fergus' Historical Series, 1876) | 33 | 29 | 15 | yes — `fergus_chicago_directory_1839` |
| D. W. Wood, *Chicago and its distinguished citizens* (1881) | 10 | 6 | 3 | no |
| Henry H. Hurlbut, *Chicago antiquities* (1881) | 4 | 4 | 1 | no |
| H. F. Kett & Co., *County histories published by H. F. Kett & Co. and its successors* (1877-1880) | 773 | 4 | 147 | no |
| John Reynolds, *The pioneer history of Illinois* (1887) | 47 | 1 | 18 | no |
| Illinois Society, S.A.R., *Sons of the American Revolution year book* (1896) | 155 | 0 | 33 | no |
| Century Publishing and Engraving Co., *Encyclopedia of biography of Illinois* (1892-1902) | 61 | 0 | 16 | no |

**Four volumes have not changed the finding.** The index's Chicago cards point at Andreas
more than at everything else together — 1,010 of the 1,764 Chicago and Cook County cards
read so far — and this project already has Andreas. The largest Chicago work it points at
that this project does **not** hold is still Moses and Kirkland's *History of Chicago,
Illinois* (1895): 228 Chicago and Cook County cards, up from 193 before volume 4 was
re-read, 192 on three volumes, 132 on two and 76 on one. Both volumes are on the Internet
Archive (`historyofchicago01mose`, `historyofchicagov2mose`).

**Volume 4 used to move these numbers by single digits; re-read, it moves them by
hundreds.** Andreas gains 112 Chicago-or-Cook cards, Moses and Kirkland 35, Moses alone
33. The ranking is unchanged in its ORDER — which is the honest thing to report, because
a quarter of the alphabet arriving late and confirming the standing answer is worth more
than one that reshuffled it — but it is no longer a ranking over three volumes and a
fragment. All four now speak.

Of the 6,688 cards read, **3,620** cite a work no pattern in the table reaches, and
**365** of those name Chicago or Cook County. `acquisition_list.json` carries them.

## Every lead is ruled on, over four volumes

T-0590 built the ladder and ruled volume 1's 319 leads; T-0578 read volume 2 and ruled the 227 it adds;
T-0579 read volume 3 and ruled the 191 it adds; T-0580 read volume 4 and ruled the 51 it adds; T-0775
re-read volume 4 and ruled the 62 more it then offered — each
under the same ladder and in the same PR as its
read, because T-0590's gate fails the moment a volume offers a lead nobody has answered.
`tools/rule_newberry_leads.py` reads every `entries_vol_*.json` now rather than volume 1's alone.

| outcome | vol 1 (T-0590) | vols 1-2 (T-0578) | vols 1-3 (T-0579) | vols 1-4 (T-0580) | now (T-0775) |
|---|---:|---:|---:|---:|---:|
| leads ruled | 319 | 546 | 737 | 788 | **981** |
| cards anchored | 542 | 947 | 1,250 | 1,294 | **1,391** |
| candidate — `testable_in_a_held_work` | 79 | 146 | 188 | 190 | **257** |
| refused — `ocr_variant_only` | 129 | 208 | 279 | 292 | 341 |
| refused — `locality_absent` | 90 | 144 | 206 | 242 | 288 |
| refused — `surname_only_chicago` | 21 | 48 | 64 | 64 | 95 |
| **matched** | **0** | **0** | **0** | **0** | **0** |
| discriminators found | 0 | 0 | 0 | 0 | 0 |

**The last column is not volume 4's re-read alone**, and saying so is cheaper than letting
someone difference the two columns and get the wrong number. T-0600's rule strike moved
these counts and was never given a column of its own; the T-0580 column is the state on
the day volume 4 was first read. Volume 4's re-read on its own took the ladder from 919
leads on 1,333 cards to **981 on 1,391** — 62 leads and 58 anchored cards, against the 51
leads its text-layer reading offered in total.

`matched` stays reachable and unreached: the test is run over all 1,391 cards, not assumed — every
forename this project holds for a candidate is searched for in the card text, and four volumes have
turned up none. The acquisition list grew from 166 Chicago and Cook cards whose citation matched no
work, to 274 on two volumes, to 369 on three, to 375 on four; T-0600's strike then cut it to 324,
and volume 4's re-read brings it to **365** — 88 of them still carrying a year the photostat left
legible. All 41 of those new cards are volume 4's, whose residue goes from 5 Chicago-or-Cook
cards to **46**: the re-read finds Chicago cards faster than the works table can place them, which
is the honest shape of the gain rather than an unqualified win.

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

All four volumes are read, and all four readings now measure between 0.925 and 0.975.
Volume 4's text layer was poor and the poverty was the source's rather than the method's;
**T-0613**'s re-OCR, finished under T-0775, recovered the cards it lost — 33,357 assembled
against 6,548, and 207 Chicago-or-Cook cards against 9. Its section above keeps both
readings, because the second one is only worth what the first one measured.
