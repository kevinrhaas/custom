# Books and reminiscences — prose, read the way the newspapers are read

**What lives here.** Fergus' Historical Series Nos. 26-29 (read in its first half
by T-0499 - see the contents table below), Gurdon Hubbard's
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

## What has been read (T-0650, 2026-09-05)

**Illinois Catholic Historical Review, vol. 4 (1921-22), pages 256-259** — Joseph J.
Thompson's *The Illinois Part of the Diocese of Vincennes*, read for one sentence and the
four pages around it. Eight claims at `claims/ichr_v4_thompson_vincennes.json`, out of the
Internet Archive's own OCR of the whole volume committed at `text/ichr_v4_1921_22.txt`.
Source record: `data/sources/ichr_v4_thompson_illinois_vincennes.json`, tier 4.

**THE TICKET'S PREMISE WAS WRONG TWICE AND THAT IS THE FINDING.** T-0650 was opened on the
belief that the first Catholic church is not in the scene, and that this passage is the only
located statement of the building the project holds. Neither is true.
`data/structures/st_marys_church.json` has stood on the south-west quadrant of Lake and State
since 2026-08-11, and it was placed off `chicagology_prefire216`, whose Andreas transcription
has St. Cyr selecting *a canal lot near the southwest corner of Lake and State streets*. So
this reading is a CORROBORATION of a placement already made, and it is written down as one.
A run reaching for "the ICHR passage that puts the church on the map" is reaching for a second
witness, not a first.

**What the passage fixes.** Four things, and only the last two are new to the project.

1. *The quadrant, said again by a second author.* "near the southwest corner of what is now
   State and Lake Streets", and a second time sixty lines later as "the State-Lake location".
   Same quadrant as the record already carries, same hedge word — **near** — so it does not
   narrow the lot and the unbounded westward error `st_marys_church.json` states is untouched.
2. *Whose ground it was.* "upon ground controlled by the Canal Commissioners". On the scene
   date the congregation stood on a canal lot it did not own. That is a fact about the parcel,
   and the project had the word *canal lot* but not the ownership.
3. *A price.* The commissioners' valuation was "fixed at $10,000", the Catholics could not
   raise it, and "the lot was purchased by a private party". The project held the shape of
   this story from Andreas and not the figure.
4. *A terminus post quem for the removal, which is what this article is worth to a scene dated
   1835-07-01.* "When he came he found the little church … standing" is O'Meara's arrival, and
   the same article dates that to "the early or middle part of June, 1837". **The church had
   not moved 23 months after the scene date.**

**What it does not fix.** The lot — "near" is still *near*. Any dimension, material, plan or
orientation; the article says "the little church" and no more. The date of the removal: it
names the auction as the cause and dates neither. Anything about 1835 in particular — it looks
back from 1837 at a building of 1833 and is silent on the years between. And it is not an
independent voice: the run read here footnotes Garraghan on six of its pages, this project does
not hold Garraghan, and **the sentence about State and Lake carries no footnote at all**, so
which of those words are Thompson's cannot be said.

**One sentence is a NEGATIVE constraint on the scene and is the second most useful thing here.**
The rear addition, the small belfry, the three-pound bell and the cross all come *after* the
removal. The building standing at Lake and State on 1835-07-01 therefore had no belfry, no bell
and no rear addition, and was one length rather than two. `st_marys_church.json` already refuses
a tower and calls the belfry "the tower trap on this record"; this dates the trap. It also says
something about the town — until at least 1837 no church bell had ever rung in Chicago.

**Nothing here is payload, and one reading is deliberately left unspent.** No structure, asset,
resident or household record was changed. The June 1837 terminus sits against a phase end of
1836-12-31 on `st_marys_church.json`, which that record took as the conservative of two
readings; the scene is not wrong either way — the record's own note says so — but the end bound
is, and **T-0717** carries that question rather than this ticket. Jean Baptiste Beaubien's
claim on the whole Fort Dearborn reservation, which the removal passage states in passing, is
recorded in `bk_ichr4_003` and written into no resident record.

**The volume is committed and four pages of it are read.** 290,298 bytes of OCR for four pages
of reading, because a quote is checked against a committed file and cutting the middle out of an
OCR run would break the byte-identity the corpus asserts. There is no deposit PDF and no page
index: the page boundaries were read off the volume's own running heads, which this OCR prints,
so no alignment was needed. `data/sources/st_cyr_register_ichr_v4.json` reads the SAME volume
through a Genealogy Trails transcription of two of its register pages — two source records of
one volume, by two different routes, and neither was re-read against the other.

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

---

## Fergus' Historical Series, Nos. 26-29 — what the volume actually holds

**The deposit's filename says 26-29 and until T-0499 nothing said what that meant.**
It is four separately printed pamphlets bound as one, each with its own title page and
its own folio run starting at 1 — which is why a page number in this volume is not
unique and why every claim cites its LEAF. The table is read off the four title pages
inside; the front matter names no contents at all.

| No. | Title | Author | Printed | Leaves |
|---|---|---|---|---|
| — | Library plate, digitisation note, half-title "FERGUS' HISTORICAL SERIES No. 26 - 29", Fergus Printing Company advertisements | — | — | 1–14 |
| 26 | *A Discourse on the Aborigines of the Ohio Valley*, with the Fort Wayne Indian speeches of 2 October 1811 appended and footnoted | William Henry Harrison (the discourse, 1838); Hiram W. Beckwith (the footnotes) | 1883 | 15–206 |
| 27 | *The Illinois and Indiana Indians* | Hiram W. Beckwith | 1884 | 207–398 |
| 28 | *Directory of the City of Chicago, Illinois, for 1843* | compiled by Robert Fergus | **1896** | 399–656 |
| 29 | *Biographical Sketch of Joseph Duncan, Fifth Governor of Illinois* | Julia Duncan Kirby | 1888 | 657–858 |

The leaf ranges include each number's own advertisement and cover leaves, which is why
they meet with no gap. Blank and plate leaves are inside them: 624 of the 858 leaves
carry text.

## What has been read (T-0499, 2026-09-03) — the first half by page index

**Leaves 1–429**, declared as four `list` items in `coverage.json` with no hole. That is
the front matter, No. 26 entire, No. 27 entire, and No. 28 down to the port statistics,
stopping where the 1843 business directory begins at leaf 430. **T-0500 takes leaves
430–858.** Forty-one claims at `claims/fergus_26_29_first_half.json`; twenty of them are
town findings. The target was stated before the reading began and is in the ticket: at
least forty claims and at least eighteen town findings.

**THE ASK WAS FOR SETTLERS' REMINISCENCES AND THIS HALF IS NOT THAT.** The Fergus numbers
in general are where the settlers of the 1830s told their own stories thirty and forty
years on. Numbers 26 to 29 are a discourse on the mound-builders, a tribal history, a
directory and a governor's life. **No. 26 is a sweep that came back all but empty, and
that is evidence**: four claims out of 192 leaves, every one of them from the 1811
speeches appended to the discourse rather than from the discourse itself, which never
reaches the Illinois lakeshore.

**The two numbers that do touch Chicago miss the scene year from both sides.** No. 27
reaches it fourteen years early and No. 28 eight years late, and every claim's
`describes_date` says so.

**No. 27 — Beckwith, and it is the better of the two.** Where he compiles he is tier 3;
where he quotes Henry R. Schoolcraft on the Chicago treaty of August 1821 he is
transmitting an eyewitness journal, and that is where the landscape comes from: **a belt
of forest skirting the south branch, and beyond it the extensive level plain stretching
to the lake shore** — the first independent corroboration in this domain of the shape the
project's heightfield and timber belt already assume. With it: **a scattered Potawatomi
village on both branches of the river** (the site was inhabited, and not at a point);
the stream's name read as *a skunk* primarily and *a wild onion* secondarily, in that
order; the Des Plaines named for a maple growing along its banks; **a seated bower on the
green along the north bank, near the old John Kinzie house and directly under the guns of
the fort**, which bounds how built that bank can have been; and between two and three
thousand people assembled there, the largest crowd figure this project holds for this
ground.

**No. 28 — a directory *for 1843* that was compiled in 1896**, by a man who did not reach
Chicago until July 1839, out of a canvass of 1843 of which he himself writes that
"sailors were made tailors, and tailors sailors, names were spelled at and locations
guessed". That sentence is a claim in this file (`bk_fer_043`) and it is the most useful
thing in the pamphlet, because **it bears directly on T-0506**: the "1839 Chicago
directory" this project cites is, on the same compiler's account, an 1876 publication —
the same retrospective act, thirty-seven years after its year. What the pamphlet still
gives the town is **the mail across the scene date** (horseback weekly in 1832 under
Jonathan Nash Bailey; a semi-weekly four-horse stage from 1834; **tri-weekly in 1835**),
**the Chicago Lyceum instituted 2 December 1834**, seven churches placed to the block
face as an upper bound on 1835, a Masonic lodge in a third storey at Clark and South
Water, and the earliest customs figures for the port — 1836, exports $1,000.64 against
imports $325,203.90, with the custom house's own warning that both understate.

**One reading was refused outright.** The 1843 census table's ward columns are woven by
the OCR into lines of loose digits. The totals appear to read 7,580 against 4,853, and
"appear to read" is not a transcription: `bk_fer_057` records the refusal instead of the
number, and says what a run would have to do to get it.

**The identity pass is small on purpose.** `crosswalk.json` rules on the five names that
fall in the 1830–1836 window — two merges (Billy Caldwell into Billy Caldwell
(Sauganash); John Stephen Coates Hogan into John S. C. Hogan, which dates the
postmastership the resident record already half-carried) and three refusals (Jonathan
Nash Bailey against Bennet Bailey; John Kinzie against his son John Harris Kinzie;
"Mrs. Kinzie" against Juliette Augusta Magill Kinzie, on the surname-only rule). Every
other name in 429 leaves is outside the window, and the pass says so by name so the next
sweep does not do the work again.

**Nothing here is payload.** No structure, asset, resident or household record was
changed by this reading.

**The page index needed no alignment, and that is new.** Hubbard's leaf boundaries had to
be transferred from a second file by `difflib`. This volume's deposit carries the hOCR
page index emitted with the same OCR pass that made the text, so the 858 leaf boundaries
are exact arithmetic; `tools/build_book_page_index.py` grew a second derivation mode for
it (`derivation: hocr_page_index`) and hard-fails unless the ranges tile the committed
text with no gap and no overlap. **Its folios are read or they are null** — the volume
binds four pamphlets that each restart at 1, so there is no offset to carry and a carried
folio would be an invention. 194 of the 624 non-blank leaves print one the reader could
take.

## What has been read (T-0500, 2026-09-03) — the second half by page index

**Leaves 430–858**, declared as five `list` items in `coverage.json` with no hole, which
completes the volume: T-0499 stopped where the 1843 business directory begins and this
takes it from there. Fifty-eight claims at `claims/fergus_26_29_second_half.json`;
forty-five of them are town findings. The target was stated before the reading began, in
its own commit: fifty claims and twenty town findings.

The five are **No. 28's Business Directory** (430–457) and **Obituary** (606–644) and the
whole of **No. 29** (658–850), read in full; the **publisher's advertisement leaves**
(645–657, 851–858) read for Chicago titles only; and **No. 28's alphabetical name
directory** (458–605) **swept by machine and not read continuously**. That last is stated
as plainly in its declaration as it is here, because it is the one limit that could be
mistaken for coverage: every line was passed against two patterns — every year from 1820
to 1836, and every personal and firm name this project's own 1835 records hold — and only
the thirty-odd lines that answered were read. An absence from this file is therefore **no
evidence** that a name is absent from the directory.

**The directory is 1843 and the claims say so, forty times over.** Not one of its
addresses is carried into the scene year, and the most useful thing in it is a dated
negative: `bk_fer2_043`, Fergus's own note that Bristol & Porter's was the **first
warehouse on the South Side, erected in the fall of 1839**. `bk_fer2_044` is why every
other annotation of his is graded where it is — his own entry gives his arrival as
**1 July 1839**, which is T-0499's finding reached independently from the other end of the
book. What 1843 does give is the distance travelled: a four-storey brick on South Water
second door from Clark, the Sauganash still at Lake and Market, a *later* Tremont House on
Lake Street, and two shops reading their position as an ordinal off a named building —
the same grammar T-0384 and T-0385 read for 1835.

**The Obituary is where the second half touches the scene year at all**, six times:
Thomas J. V. Owen the Indian agent (15 October 1835), the Rev. Jesse Walker twelve miles
west of Chicago (5 October 1835), Hollis Newton hotel-keeper (25 August 1835), a **Dr
Spring** with no given name (10 November 1835), the Rev. Allen B. Freeman (17 December
1834) and Dr Alexander Wolcott (25 October 1830, his the first will probated in Cook
County). The Spring line is **refused** against this project's Giles Spring and the
refusal is the point: a surname with a doctor's title in front of it is not a lawyer, and
T-0423 would otherwise inherit a death inside the scene year on a surname alone.

**No. 29 names Chicago four times in ninety-five pages and places nothing here.** Its one
thread that reaches the town is the Illinois-and-Michigan Canal, and that thread is worth
the reading: Duncan's Washington diary of March 1829 pressing the War Department to get
the route **located**; the legislature of 1834–35 adjourning without acting on it; and the
special session of **December 1835** — the last month of the scene year — where he
reported every attempt at a loan had failed and asked instead for the faith of the State
to be pledged, which that session granted and which is the money the canal was built
with. One passage naming Chicago canal lots is recorded as a **trap** (`bk_fer2_012`): it
sits in a message headed *July 11, 1837*, so its "20th of June last" is 1837, and a sweep
for Chicago plus a canal context would take it for 1835.

**The identity pass rules on eleven claims** — six merges and seven refusals — and lists
all twenty-five people named inside the 1830–1836 window by name with the outcome of
each, because a crosswalk that reports only its merges cannot be audited. Nothing in
`data/residents/`, `data/structures/` or `data/assets/` was edited.
