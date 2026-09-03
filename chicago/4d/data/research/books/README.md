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

**Hand-authored:** `claims/`, `text/`, `coverage.json`, `crosswalk.json`, `corpus.json`.
**Generated:** `page_index/` (`tools/build_book_page_index.py --build`, gated by its own
`--check` in `tools/check.sh`); `data/research/domains.json`.

**`corpus.json` is the register.** One entry per book whose text this project commits: what
the book is, which source record grades it, the deposit copy and its sha256, the derived text
and its sha256, HOW that text was produced, and what has been read out of it. A quote is
checked against a committed file, so the file has to be traceable back to the artifact or the
check is circular.

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

---

## What has been read (T-0501, 2026-09-03)

**Gurdon S. Hubbard's *Autobiography* (Lakeside Classics, 1911)** — a 226-leaf scan that had
sat in the deposit unmentioned: no text, no source record, and zero hits for "swift walker"
anywhere in `docs/`, `data/sources/` or `tickets/`. Ninety-two claims at
`claims/hubbard_autobiography_1911.json`, out of the Internet Archive's own OCR committed at
`text/hubbard_autobiography_1911.txt`. Source record:
`data/sources/hubbard_autobiography_1911.json`, tier 3.

**THE BOOK IS TWO BOOKS AND EVERY CLAIM SAYS WHICH.** Hubbard's own narrative is a
participant's recollection of 1818–1830 at rung 2, and it **stops dead in November 1830** —
the closing editorial note says so in as many words. Caroline M. McIlvaine's Introduction is
1911 compilation at rung 4, and it is the *only* place in the volume where the town of
1834–1836 appears at all: the brick building at La Salle and South Water, the five or six
hundred inhabitants, the brig *Illinois* of 25 May 1835, the Green Tree Tavern, the fire
engine, the Russell & Mather purchase, the canal commissioners. **A run reaching for "Hubbard
on 1835" is reaching for McIlvaine.** One period document is printed between them — Hubbard's
letter to his sister, headed *Chicago, July 25, 1827* — and it alone reads at rung 1.

**What the book is actually worth here** is 1818, and it is worth a great deal: a full
elevation of Fort Dearborn and its enclosure (fourteen-foot oak pickets, block house
south-west, bastion north-west, whitewashed throughout, officers' quarters *outside* the
pickets with a piazza at second-storey level, a brick magazine, a four-acre garden, one road,
a fence line closed from river to river, a well by the south gate, wash-houses on the beach);
the Factor House and the American Fur Company's round-log storehouse that passed from John
Craft to Jean Baptiste Beaubien; John Kinzie's long log cabin with its rude piazza facing the
fort across the river; and a **complete building count for the whole of Cook County** — the
fort's group, those two, Hardscrabble, Ouilmette's cabin and Kinzie's house, and nothing else.
Seventeen years before the scene.

**Two contradictions are recorded and neither is resolved.** Page 36 puts the officers'
quarters outside the pickets and built of hewn logs; page 167 puts the commanding officers'
former quarters in a *brick* building just within the north stockade. And page 167 dates the
Pottawatomie payment and the fort fire to "September of the year 1828" while the section
heading, the narrative around it and Hubbard's own dated letter all say July 1827. Both are
written down as disagreements. Neither is smoothed.

**The scan is out of order, and finding that out is part of the reading.** Pages xv and xvi
were photographed at the *front* of the Internet Archive item, as leaves 11 and 12, ahead of
the title page — leaf 26 ends "Quoting Mr. Gale's characteristic manner of narration:", leaf
11 opens the Gale quotation, leaf 12 ends "his engine was soon put to", leaf 27 opens "use as
'Fire King Engine No. I,'". Six folios read off the page fix the runs above and below the
displacement, and `tools/build_book_page_index.py` now carries all three runs and **hard-fails
if a folio printed on a page ever contradicts them** — which is the check that would have
caught it without the text.

**`page_index/` exists because the committed text has no pages.** The djvu output carries not
one form feed. The leaf boundaries are transferred onto it, mechanically and reproducibly,
from the deposited PDF's own text layer, which has all 226; 207 of the 208 non-blank leaves
aligned, and the one that did not — the Contents at leaf 19 — is declared, and the leaf that
swallows its lines says so with `runs_into`. No claim cites those lines.

**Nothing here is payload.** No structure, asset, resident or household record was changed by
this reading. Seven identities are merged and fifteen refused in `crosswalk.json`, all inside
the research layer; the sharpest refusal is the "John Kinzie" of the 1834 trustee list, which
*looks* like an easy merge and is not — the elder John Kinzie died in 1828 and this project
holds three separate Kinzies, so a 1911 writer's shortened form is not enough to put a dated
civic office on any one of them.
