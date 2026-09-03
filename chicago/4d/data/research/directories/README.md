# Directories — entry by entry, structured, and crosswalked

**What lives here.** The 1839 Chicago directory, which this project cites today
from a web transcription and has never extracted, and its successors (T-0506).

**Shape: `claims`.** A directory reads like a list and is filed as claims for one
reason: the repository holds it as PROSE — a page of running text this project
commits and quotes from — and the verbatim gate binds any domain whose text is
committed here. A structured entry is then the claim's `normalized` reading, with
the printed line in `quote`, unedited, and `kind: person` or `kind: business`
according to what the entry is.

**A directory entry is three facts at once:** a name, a trade and an address. Keep
all three in `normalized`, keep the printed line whole in `quote`, and let the
crosswalk decide whether the name is a person this project already holds.

**1839 IS FOUR YEARS LATE.** The town in this reconstruction is the town of 1 July
1835. A directory of 1839 is evidence about 1839, and an address in it is not an
1835 address. Where it corroborates a person, say so in the crosswalk with the
rule written out; where it supplies a place, it supplies a 1839 place.

**Not a second-hand citation.** The current citation is to somebody else's
transcription of the directory. A reading made through that is
`transcription_mediated`; a reading made off the page image is `scan_verified` and
outranks it. Say which.

**Hand-authored:** `text/`, `coverage.json`, `crosswalk.json`,
`claims/norris_1844_town_findings.json`, and the READING of a source that is not a
list — `norris_1844_advertiser_index.json`, which says where each advertising card
begins and ends.
**Generated:** `claims/norris_1844_directory_entries.json`,
`claims/norris_1844_advertiser.json`, `norris_1844_crosswalk_1835.json` and
`norris_1844_advertiser_crosswalk_1835.json`, each by the tool named in its own
`generated_by`, each with a `--check`; and `data/research/domains.json`, which is gated.

**Coverage.** Declare the PAGES read. A directory is finite and countable, which
makes an undeclared page an honest "not yet" and a declared empty one a fault.

**This is research, not payload.** Nothing under `data/research/` reaches
`site/chicago/4d/`.

---

## Norris's *General Directory ... of the City of Chicago for the Year 1844*

**Read for T-0566** (piece 1 of the owner's T-0555). The first Chicago directory,
and the largest single list of named Chicagoans this project has touched: **2,073
entries** off printed pages 21-65, of which 117 are the ADDENDA Norris set at the
back for "names accidentally omitted above."

**Which copy, and why not the owner's.** He named HathiTrust `chi.56111136`. That
copy sits behind a Cloudflare challenge no runner here can pass — the plain-text
view, the `ssd` reader and `imgsrv` all answer 403 with a challenge page. The
volume was read instead from the University of Illinois scan of the T. F. Bohan
republication of 1903, Internet Archive `generaldirectory19norr`, which is the
same 1844 text and is full-view public domain. That substitution is in the source
record, not only here.

**The structure is the indent.** Norris sets every entry flush left and turns the
long ones in about half an inch. `text/norris_1844_leaf_NNN.txt` keeps that: a
turned line carries two leading spaces, computed from the word coordinates of the
scan (`_djvu.xml`), and a line is judged turned when it starts more than 45/400 of
an inch right of the page's own margin — the MODE of that page's line starts, not
the minimum, because a speck in the gutter is one line and the body is fifty. On
leaves 40, 46 and 61 the speck is far enough left that a minimum would have made
the whole page look turned. Entry boundaries therefore survive the trip from image
to text and can be checked by eye against the page.

**What is generated here.** `claims/norris_1844_directory_entries.json` by
`tools/read_norris_1844.py --build`, and `norris_1844_crosswalk_1835.json` by
`tools/crosswalk_norris_1844.py`. Both have a `--check` that rebuilds and compares,
so a hand-edit is caught. The page text under `text/` is committed, hand-authored
in the sense that nothing regenerates it here, and is what the verbatim gate reads.

**The reading is `transcription_mediated`, all 2,073 of them.** This is
archive.org's OCR, machine-read and not checked against the image by eye. The
damage is left in every quote on purpose — `Win.` for `Wm.`, `ISickalls` for
`Nickalls`, `wi<jmaker` for `wigmaker` — because a tidied quote cannot be found
again. The repair, where one is safe, is in `normalized`, and `normalized` is best
effort: the split of one printed line into name / occupation / address is a
heuristic over inconsistent nineteenth-century punctuation, `as_printed` carries
the whole line, and the quote carries it unedited. Firm detection is the weakest
part of it — `Frink, Walker, & Co.` reads as a person because the comma falls
before the ampersand — and 65 entries are graded `kind: business` where the true
number is higher. T-0568 has now read the Advertising Directory, below; it did NOT
regrade those 65, because the advertiser is a separate 158-card file that stands
beside the directory proper rather than editing it, and regrading a generated file
from a second source is a pass of its own.

**1844 IS NINE YEARS LATE, and this is the whole discipline of the file.** Every
claim carries `describes_date: "1844"`. Nothing here is an 1835 fact. The one place
a name in this volume touches a person standing in the scene of 1 July 1835 is
`norris_1844_crosswalk_1835.json`, and it touches them as corroboration and as a
CANDIDATE enrichment: **48** of the 847 people in the residents layer meet exactly
one 1844 entry on the rule, **15** meet more than one and are left ambiguous, **4**
are contested — two 1835 people meeting the same 1844 line, at most one of whom is
the man printed — and **171** have their surname in the book under a different
initial and are refused outright, because a surname-only agreement is always a
refusal and Norris lists eleven Smiths. That file **changes no resident record**:
under the ratified ladder an 1844 listing alone never makes an 1835 resident, and
T-0569 is the ticket that spends the reading on the layers.

**What was not read** is named in `coverage.json`: the 1903 front matter, the
Description and Historical Sketch (T-0567), the Statistical Account (T-0567), the
Advertising Directory (T-0568, read — see below) and Norris's own General
Intelligence Agency card at the foot of printed page 65 (T-0568, read). All of it is
committed as page text, so those tickets started from the text rather than from the
network.

---

## …and its Description, Historical Sketch and Statistical Account

**Read for T-0567** (piece 2 of the owner's T-0555). T-0566 read the volume's list of
names and deliberately left the two parts of it that are PROSE AND TABLES: the
**Description and Historical Sketch**, printed pages 5-20 (leaves 15-30), and the
**Statistical Account**, printed pages 66-78 (leaves 76-88). Those 29 leaves are now read,
as **65 town findings** in `claims/norris_1844_town_findings.json`.

**Why they are `claims` and not `records`.** A directory entry is a row in a list; a
sentence in Norris's sketch is an assertion about the town, made nine years after the fact
by a man selling the town to its own inhabitants. It has an author, a purpose and a date,
and the shape that carries all three is a claim with `town_finding: true`. Every quote is
lifted unedited out of the committed page text and `tools/research_domains.py --check`
rebuilds it character-for-character — that check is this file's gate, and a hand-edit to
one word of one quote fails it.

**`describes_date` IS THE FIELD THAT MATTERS.** It is the year the STATEMENT describes,
never the year the book was printed. Of the 65 findings only 21 are about 1844; the rest
run from 1673 to 1843, and **four are about 1835** — the scene year of this
reconstruction. Sorting the file by that field is the whole point of having read it:

| `describes_date` | what is there |
| --- | --- |
| **1835** (4) | Norris's population of the scene year — "said to amount to 5,500 … could not have been much less than 3000"; the autumn prairie fires running over the third and fourth wards "so late as '35 or '6"; speculation raging "with great violence during '35-6"; and the eastern mail arriving TRI-WEEKLY by four-horse stage in 1835 |
| 1832 (6) | the pre-boom town, named building by building — see below |
| 1833-1834 (5) | the harbour work begun, the light-house re-erected, the school section sold, the Democrat founded, the first brick buildings |
| 1836-1837 (10) | the year after the scene and the crash: canal work begun 1836, Hydraulic Company 1836, six churches by 1836, city charter 1837, fort evacuated 1837 |
| 1673-1829 (10) | Marquette, Greenville 1795, the 1804 fort and Fur Company post, the 1812 evacuation, the 1816 rebuild as Fort Dearborn, the canal board of 1829 that laid the plat out |
| 1840-1844 (30) | the town of the directory — its wards, officers, churches, presses, fire companies, trade and 1843 census |

**The passage this ticket was worth a run for** is on printed page 12 (leaf 22), where
Norris inventories what stood at Chicago in 1832 and names it: the Fur Company house that
Col. Beaubien later occupied; Colonel Owings's house 80 rods south of it, since washed
away by the lake; "Cobweb Castle" on block No. 1, Dr Alexander Wolcott's; John Kinzie's
dwelling east of the Lake House; a log building at Dearborn and South Water; Mark
Beaubien's tavern on the site of the Sauganash, "generally known as the Eagle"; a building
on block 14; and Robinson's cabin at Wolf Point. Eight buildings, most with a street, a
block or a landmark. **They are 1832 buildings.** What they fix is the floor the scene was
built up from, not the scene — and whether any of them still stood on 1 July 1835 is a
question this file does not answer.

**What it does NOT settle for 1835, said plainly.** Norris has no 1835 census — none was
taken — and his figure for the year is a recollection with a 2,500-person spread in it. He
gives no 1835 street list, no 1835 building count and no 1835 officers. The famous "five
or six houses" sentence on leaf 21 is about 1832, not 1835, and the claim that quotes it
says so at length, because a later run reading that line out of context would put a
hamlet where the reconstruction has a town. The three OCR slips that change a date —
`1932` for 1832, `1617` for 1816, `1342` for 1842 — are repaired in `normalized` only and
named in the notes of the claims that carry them.

**What was declared unread, and why**, is in `coverage.json`: the 1843 census table on
printed page 76 beyond its three unambiguous totals (the OCR wove its columns into one
stream of bare numbers and the nativity counts cannot be attached to a heading without the
page image), and the ordering assumption behind the trade tables on page 77.

**Nothing here is payload, and nothing here was written onto a record.** No resident,
household, business or structure was created, graded or regraded by this pass. Under the
ratified ladder of 2026-09-03 a source printed nine years after the scene never on its own
makes an 1835 fact; T-0569 is the ticket that spends this reading and T-0566's on the
layers. The Advertising Directory, leaves 89-126, has since been read by T-0568 and is
the section below; the only part of the volume still unread is the 1903 republisher's
front matter, leaves 1-14, which no ticket owns.

---

## Norris's 1844 ADVERTISING DIRECTORY — the cards

**Read for T-0568** (piece 3 of the owner's T-0555). **158 advertising cards** off
printed pages 79-116, plus Norris's own General Intelligence Agency card at the foot
of printed page 65, which T-0566's coverage sent here. They name **204 proprietors**
between them and **156** carry a firm name.

**A card is not a line, so the boundaries are read by eye.** The directory proper is
a list and a line-by-line reader can see its entries. The advertiser is 38 pages of
display cards — a firm's name, its trade, its partners and its address, set in
whatever type the subscriber paid for, over anything from three lines to
twenty-four. Where each card begins and ends is therefore READ, and the reading is
committed in `norris_1844_advertiser_index.json`: leaf, line range, and what the card
says. `tools/read_norris_1844_advertiser.py --build` turns that into
`claims/norris_1844_advertiser.json`, **slicing every quote out of the committed page
text at the card's own line range**, so a quote cannot drift from the page it claims
to come from; `--check` rebuilds and compares, and the domain gate rebuilds the quote
a second time from the same text. Nothing here is typed into a quote.

**What no card reaches is counted, not hidden.** 65 advertiser lines fall outside
every card, and all 65 are listed with their text under `uncovered` in the claims
file. They are the running heads and page numbers, the ornamental section headings
(`Stnrtioneera` for Auctioneers, `HJookbtn&trg*` for Bookbinders, `l)otcls` for
Hotels — this is what OCR does to a decorated capital), the signature marks, and two
fragments the scan tore off the cards they belonged to: `  paid` on printed page 89
and `Office and House opposite the City Hotel.` on printed page 80. The second sits
between two law cards and is left out of both rather than given to one it may not
belong to.

**Two cards lost their headings to the scan** and are filed with `firm: null` rather
than a guess: the attorneys' card opening printed page 79, whose surviving lines name
A. O. Beaumont and Mark Skinner, and a banking card on printed page 82 that opens at
its address, 127 Lake street. Guessing either name would be inventing a citation.

**Display type is what OCR reads worst**, so the damage in this section is heavier
than in the directory proper and it is left in every quote: `SMITH & BALUNGALL` and
`P. BALLINOALL` are the same name twice on one card, `BOTSFORD & BEEKS` heads a card
whose partner signs `C. BEERS`, `ERT REYNOLDS` is Robert Reynolds with three letters
gone, and `Chicago, Jan. 1st, 1344` is 1844. The repair, where one is safe, is in
`normalized`, and the reading grade is `transcription_mediated` for all 158.

**THE FOUNDING DATES ARE NOT THERE, and that is the finding.** T-0555 asked for
"often 'established 18xx'" and the answer is that Norris's advertiser almost never
prints one. **Seven** cards carry a date at all, and every one of them is 1843 or
1844: the Pittsburg Iron Store's `CHICAGO, ILL. 1844`, Osterhoudt's `Jauunry, 1844`
at the Sauganash, John Murphy's `Chicago, Jan. 1st, 1844` at the United States Hotel,
Perkins & Fenton's `Chicago, Jan. 1st, 1844`, and the three Garrett cards of December
1843 — of which Garrett & Seaman is the only true founding statement in the section,
a partnership announced before it exists, "to commence on the 1st of May, 1844". **No
card in the advertiser dates a business to 1835 or earlier.** What some cards do
carry is an undated claim of age — Joseph E. Ware "still continues", Chas. Taylor
asks "a continuance of the liberal patronage hitherto extended to him", Washington
Hall is a "well known Hotel" that "has recently undergone extensive additions", the
Chicago Bookbindery is "LATE BOWMAN & ROSS", the Lake Street House is the "Late
Farmers' Exchange", and Dr. Tew has been at it "for the last five years". Those are
recorded in each card's `notes` as what they are: a firm asserting it is older than
this book, with no year attached. **Not one of them reaches 1835 on its own**, and
none has been written to a business record.

**The crosswalk.** `norris_1844_advertiser_crosswalk_1835.json`, by
`tools/crosswalk_norris_1844_advertiser.py`, runs the same rule the directory-proper
crosswalk runs, so the two files can be read side by side: surname folded, first
initials must agree, a surname-only agreement is always a refusal. Of the 204 printed
proprietor names, **157** carry a given name or an initial and can be matched at all;
**47** are printed as a bare surname — `Skinner & Smith`, `Clybourn & Hovey`,
`Spring & Goodrich` — and are unmatchable by construction. Against the 847 people in
the residents layer: **14** meet exactly one card, **2** meet more than one and are
left ambiguous (A. Garrett, who signs three cards, and G. S. Hubbard, who signs two —
both are almost certainly one man twice over, and the rule does not get to say so),
**0** are contested, and **52** have their surname on a card under a different
initial and are refused outright. That file **changes no resident record and writes
no business**; T-0569 is the ticket that spends it.

**What the advertiser does not settle.** T-0566 left a note saying this ticket would
"correct the business side from the cards" — the 65 entries the directory-proper
reader graded `kind: business` where the true number is higher. It has not: the 158
cards are a separate file, and rewriting a generated claims file out of a second
source is a pass of its own with its own rule to write down. The cards are here for
whoever takes it.

**AN ADVERTISING CARD IS A SUBSCRIPTION.** The page says so itself — "CONTAINING THE
CARDS OF SUBSCRIBERS". These 158 firms are not the trades of Chicago in 1844; they
are the part of them that had money for display type and chose to spend it. A trade
absent from this section is not a trade absent from the town.
