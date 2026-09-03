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
| `leads.json` | `--parse` | surname → the residents, voters, 1840 heads and structures a card COULD bear on. Never a match |
| `follow_up.json` | `--parse` | the works the Chicago and Cook County cards point at, ranked by how many of this project's people they could bear on. This is the reading order |
| `precision_sample.json` | **hand** | forty cards drawn at random and adjudicated one at a time. The only thing here that measures whether the reading is any good |
| `coverage.json` | **hand** | which volumes have been read |
| `crosswalk.json` | **hand** | no merges, and the refusals written out one by one |
| `lead_crosswalk.json` | `tools/rule_newberry_leads.py --write` | every lead in `leads.json` ruled on and anchored to the cards it stands on. Still no merges |
| `acquisition_list.json` | `tools/rule_newberry_leads.py --write` | the Chicago and Cook County cards whose citation the works table could not read — books, not leads |

This is research, not payload. `tools/publish.sh` does not copy `data/research/`, and
`tools/newspaper_corpus.py --check` asserts it stays out of `site/chicago/4d/`.

## How the volumes are read

The four PDFs are ~200 MB each and are **not committed**. Fetch one to a scratch path and
run:

    python3 tools/read_newberry_index.py --extract --volume 1 --pdf /tmp/newberry_v1.pdf
    python3 tools/read_newberry_index.py --parse   --volume 1
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

**The number, and how it was got.** Forty cards of volume 1 were drawn at random —
twenty from the Chicago/Cook stratum and twenty from the rest, `random.seed(1835)` — and
adjudicated one at a time against what the card line actually says. **39 of 40** carry
the locality this reading assigns them. The one that does not is `nbi_v01_2226`, whose
entire line is `I II.`: three strokes and a stop is the shape of the abbreviation and on
that card it is the only thing there, so nothing demonstrates Illinois. It is left in
the records with its verdict, because a card struck where nobody can see it is a
precision figure nobody can check. `precision_sample.json` carries all forty.

The sample also found one *systematic* false positive and it is now a rule. The index
holds thousands of English cards citing the *Calendarium Inquisitionum post mortem*,
whose entries are filed by regnal year — `Calendarium, Hen. III. and Edw. I` — and
`, III.` is the shape of `, Ill.`. `REGNAL` in the tool refuses them; 35 cards left
volume 1 when it was added, and the sample above was redrawn afterwards.

**Surnames are recovered, not read.** A heading is often clipped by its neighbour, so
`er, E P Adams` is a real reading of an Adams card. The comparison key is the longest
word of three letters or more in the heading, which is `Adams` there and `Aldridge` in
`Aldridge, or Oldridge`. The key is for comparison only; `as_read` always keeps the
heading verbatim.

**Citations are clustered, and more than half of them are not.** The works table in the
tool matches a citation by pattern or by similarity to one canonical spelling. It reaches
1,065 of volume 1's 2,579 cards. The 1,514 it does not reach are overwhelmingly Illinois
COUNTY histories — Chapman, LeBaron, Brink & McDonough, Baldwin, Murray Williamson,
Power — published by houses nobody has written a pattern for, and only **166** of them
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

Volumes 2, 3 and 4 are unread: T-0578, T-0579, T-0580. Each wants its own hand-drawn
precision sample — a number carried over from another volume is not a measurement of it.

## What the 319 leads came to, ruled 2026-09-03 under T-0590

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
the voters layer has been looked at once. So this ticket spends 542, and the domain's
ceiling in `tools/research_spend_baseline.json` comes down from 2,619 to **2,077**.

`acquisition_list.json` is the other half of the finding and is deliberately not a lead
list: 166 Chicago and Cook County cards whose citation matched no work in the table, and
only 39 of them still carry a publication year the photostat left legible. They point at books, and three of the books
already have tickets — T-0581, T-0582, T-0583.
