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

**Hand-authored:** `claims/`, `text/`, `coverage.json`, `crosswalk.json`.
**Generated:** nothing here yet; `data/research/domains.json` is, and is gated.

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
number is higher. T-0568 reads the Advertising Directory and will correct the
business side from the cards.

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
Advertising Directory (T-0568) and Norris's own General Intelligence Agency card at
the foot of printed page 65. All of it is committed as page text, so those tickets
start from the text rather than from the network.

### What T-0569 spent it on — `data/residents/directory_1844.json`

The crosswalk above is a PROPOSAL and stops at the edge of the residents layer. **T-0587**
(the residents piece of T-0569) is the pass that spends it, and what it produces is a layer
BESIDE the household records rather than a key inside them:
`tools/spend_norris_1844.py` reads the crosswalk and writes
`data/residents/directory_1844.json`, which `renderers/web/js/residents.js` joins on
`person_id` and renders on the person's own card.

**Why beside and not inside.** Most of the people this reaches live in records a mint
regenerates byte for byte — `mint_letter_list_residents.py --check` and its four siblings diff
the whole file — so a block written into them is drift by the next gate that runs. It is also
the argument T-0442 already made for candidate identities, and the shape
`residents/research_pilot.json` already has: an 1844 listing is EVIDENCE ABOUT 1844 offered
beside a person of 1835, not a fact of theirs, and keeping it beside the record is what stops
it reading as one.

**67 people, and all three statuses are shown.** 48 meet exactly one entry no other person in
this town meets, 15 meet several and the project does not choose between them, 4 share their
one entry with another 1835 person so no match is made. A section that showed only the first
would be reporting the crosswalk's successes and hiding its arithmetic. Of the 48, **21** have
no trade in the 1835 layer and a trade printed against their name in 1844, and **39** have no
1835 street and a street printed in 1844 — stated on the card as what the line HOLDS, carried
into no 1835 claim, and moving nobody's grade.

**The 171 refusals reach no card.** A refusal on this rule — the surname is in the book under
no entry carrying the person's initial — is a statement about eleven Smiths rather than about
the person. They stay in the crosswalk, counted in the layer file's `refusals_not_shown`, and
171 cards saying "looked, and the rule says no" would bury the 67 that say something.

**The line is quoted and its parse is not.** The crosswalk splits each printed line into a
trade and an address, and on this volume that split is the weakest thing in the reading:
`Adams, W. H. of W. H. A. & Co. residence iasalle. street` yields the trade `of W`. Those two
fields do not reach the card. The line goes whole, damage and all, with its printed page and
its entry id, and the split survives only as the `carries` statement a reader checks against
the quote.

**One correction to the crosswalk itself.** `could_carry_occupation` reported **0** and the
true number is **21**. The residents layer writes `none_recorded` where a person's trade was
never attested, and the test for "this record has no trade" was a truthiness test, which read
that sentinel as a trade on 23 of the 48. A nil that looked like a finding; it was a bug, and
the crosswalk regenerates with the count corrected.

**Still 1844.** Nothing here regrades, moves, dates or employs anybody in 1835. Under the
ratified ladder an 1844 listing alone never makes an 1835 resident.

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
layers. The remaining unread part of the volume is the Advertising Directory, leaves
89-126 — T-0568.
