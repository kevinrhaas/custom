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

**Second readings.** `second_readings/` holds a volume read INDEPENDENTLY of the reading
committed in `claims/`, kept whole so a disagreement between two readings of one printed book
survives the merge. Nothing downstream reads it; see `second_readings/README.md`.

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

### Read a second time — T-0576

**2,065 of these 2,073 entries have now been checked against a second, independent
transcription** of the same printed book: Kim Torp's, published on genealogytrails.com in 2002
and typed from a different copy. `second_readings/norris_1844_genealogytrails.json` holds the
alignment and `second_readings/README.md` says what it found. **99.61% match; 1,190 of the
matched pairs identical, 808 agreeing, 67 differing, 8 entries in this reading alone and 5 in
hers; the addenda count agrees exactly at 117.** Nothing in `claims/` was deleted, rewritten or
regraded by that pass and neither reading is preferred — both stand, verbatim, wherever they
differ.

**Two defects in the file above are named there and NOT yet repaired.** `n1844_e1332` is two
printed entries in one claim — the scan ran Andrew Nelson's line onto the end of Peter Myers's —
and the Woodbury clerking at T. W. Salisbury's is `Hiram` here and `A. J.` in her transcription,
which is a person this reconstruction would get wrong. Rewriting a generated claims file out of a
second source is a pass of its own, with its own rule to write down, and it has not been done
here for the same reason T-0568 did not regrade the 65 businesses.

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

---

## Robert Fergus's *Directory of the City of Chicago, Illinois, for 1843*

**Read for T-0571** (piece 1 of 6 of the owner's T-0556). The earliest complete
Chicago directory this project can reach, and the largest list of named
Chicagoans it holds: **2,695 entries** — 174 classified business cards off page
1, and 2,521 alphabetical entries off pages 2, 3 and 4.

**Which copy, and it is not the printed one.** Fergus set this volume in 1896 out
of the canvass J. W. Norris made between August and December 1843 — the same
canvass that produced the 1844 directory T-0566 read. What this project has seen
is K. Torp's 2007 transcription of it on Genealogy Trails, cached here on
2026-09-03 and copied into `text/` byte for byte, so a line number means the same
thing in `data/research/genealogytrails/text/1843directory_N.txt` and in
`text/fergus_1843_page_00N.txt`. Every reading is `transcription_mediated`, and
the source record says so rather than only this file.

**Two shapes on four pages, because the printer set them differently.**

*Page 1, the business directory.* Fergus groups 174 cards under 26 all-caps trade
headings — ATTORNEYS, DRY GOODS GROCERIES ETC, FORWARDING AND COMMISSION,
LOOKING-GLASSES — and shouts each card's subject at its head. The heading is
carried onto the claim as `trade_heading`: it is the printer's own classification
of the business, and it is worth more than anything a parser could infer from the
prose beneath it. Every card is `kind: business`, including the ones headed by a
man's name, because the card advertises a business and not a household; where the
subject IS a named man his `surname` and `given` are in `normalized` anyway, which
is how the crosswalk reaches him.

*Pages 2-4, the alphabetical directory.* One sequence, broken by letter sections.
The transcription wraps the long entries and does NOT indent the turn, so the
indent that gives Norris its entry boundaries is unavailable here. **The rule is
the directory's own organising principle instead: an entry begins where a line
begins with a surname in the current letter section.** A turned line that opens
with a capital opens with a place or a date — `Ill., Nov. 25,1893, a. 80. ]` under
A, `Feb. 22,1862` under B — and its initial is not the section's. Where the
capital IS the section's letter and the head carries no comma, alphabetical order
decides: `Cass` arriving after `Clarke & Co.` is the tail of that firm's address,
not a new name. Seven times on page 2 the transcription runs a new entry onto the
tail of the line above; those are cut mid-line and located with `spans`.

**What this directory carries that Norris's does not is a date of death.** Fergus,
writing fifty-three years later, set each man's death in brackets after his entry —
`[died June 6, 1882, aged 67.]` — and an age at death is a year of birth. Those
brackets are kept whole in `normalized.bracket_notes` and carried onto every
crosswalk match as `death_note_1843`. **They are not spent here.** T-0574 is the
ticket that reads them.

**1843 IS EIGHT YEARS LATE, and doubly late.** The town in this reconstruction is
the town of 1 July 1835; the canvass is of 1843 and the deaths and corrections are
of 1896. Nothing here is an 1835 fact, every claim carries `describes_date:
"1843"`, and no resident record changed state in this ticket.

**What is generated here.** `claims/fergus_1843_directory_entries.json` by
`tools/read_fergus_1843.py --build`, and `fergus_1843_crosswalk_1835.json` by
`tools/crosswalk_fergus_1843.py`. Both have a `--check` that rebuilds and
compares, so a hand-edit is caught; the reader's `--check` also holds the per-page
entry counts to what `coverage.json` declares, because a declared page that
quietly loses forty entries is exactly the hole coverage exists to catch. The page
text under `text/` is committed and is what the verbatim gate reads.

**`normalized` is best effort and the quote is not.** The transcriber's damage is
left in every quote on purpose — `accidentially`, `John S.Wright`, `aged - .` —
because a tidied quote cannot be found again. The split of a printed line into
name / occupation / address is a heuristic over punctuation that is not a grammar:
the address begins at the first of Fergus's own abbreviations, which he prints in
his REMARKS (`bet` for between, `res` for residence, `bds` for boards, and `cor`
and `op.` beside them). 937 entries yield no address on that rule and 170 no
occupation, and that is the reading being honest rather than guessing. What the
split is FOR is the crosswalk, which needs a surname and an initial and nothing
else to be safe.

**The crosswalk: 68 matches, 33 ambiguous, 8 contested, 174 refusals** out of the
847 people in the 1835 layer, on surname-fold plus first initial. 46 of the 68
could carry a 1843 address the 1835 person lacks and 43 could carry a death
notice. None of it has been spent — T-0569 is the pass that spends the matches
and T-0574 the one that spends the notices.

**Page 1's civic account is NOT read here.** Lines 37-750 — the officers and
courts, twenty-odd churches and societies with their ministers and memberships,
the newspapers, the fire and military companies, the schools, the 1843 ward
population count and the port's exports and imports for 1842-3 — are a different
reading with a different kind vocabulary. `coverage.json` names them as not read
and names **T-0589**, which owns them.

---

## Do any of these firms reach the town of 1 July 1835? — `norris_1844_businesses_1835.json`

**Read for T-0588** (piece 2 of the owner's T-0569). The owner's ask on the 1844
volume was to "include the businesses with date appropriate", and the ticket set the
test: a firm reaches this scene only if some printing DATES its founding at or before
1835 — the Historical Sketch, the firm's own advertising card, or Fergus's 1843
directory. `tools/date_norris_1844_businesses.py` walks all three over every firm the
volume prints, and this file is the result.

**The answer is no, and it is no 207 times.** 222 firm printings — 65 in the directory
proper, 157 on the advertising cards — resolve to **207 distinct firms**, and not one
of them is dated at or before 1835 by any of the three routes:

- **The sketch.** 25 of its 65 town findings are dated at or before the scene, and
  they name **no** 1844 firm. Norris's early paragraphs are about the fort, the
  harbour, the mails, the lyceum, the two newspapers and five or six houses; the
  businesses in them — the Fur Company's traffic, R. A. Kinzie's store at Wolf Point,
  Mark Beaubien's Eagle — are places this town already holds, not firms his directory
  lists nine years later.
- **The cards.** Seven of the 158 carry a date at all, and every one of the seven is
  December 1843 or 1844. That is T-0568's finding re-derived rather than trusted.
- **Fergus 1843.** **153 of the 207 firms are already in it** — the single most
  telling number here, because it says the 1844 volume is a portrait of the town of
  1843-4, and being in print in 1843 is not being in business in 1835. Exactly one
  entry in the whole of Fergus prints a founding year, and it prints **1839**
  (Bristol & Porter's "first warehouse on the South Side, erected 1839").

**So this pass writes nothing to the businesses layer, and the writing-nothing is the
result.** The ticket said as much before the work began: a pass that stretches an 1844
listing back nine years to have something to show fails it, and one that writes nothing
and says why closes it. `written.why` in the file carries the reason, so it survives
where a pull-request body will not.

**What it did confirm.** The 206 businesses the 1835 papers give the town were walked
against the same 207 firms on a firm-style rule — the standing surname-and-initial
discipline adapted from people to partnerships. **Two survive into the first
directory** under the same style: **Newberry & Dole**, and **G. S. Hubbard** against
the papers' Hubbard & Co. One is ambiguous (B. Jones & Co. meets two Jones businesses
of 1835) and seven are refused on a surname alone under the eleven-Smiths rule, each
named in the file with the 1835 business it nearly met. A continuity match is worth
less than a date and the file says so: it adds no business, dates no founding, and
moves no grade.

**No page was read for this ticket**, so `coverage.json` is untouched — the four
inputs (`claims/norris_1844_directory_entries.json`,
`claims/norris_1844_advertiser.json`, `claims/norris_1844_town_findings.json`,
`claims/fergus_1843_directory_entries.json`) and the town's own
`data/research/newspapers/gazetteer.json` were all already committed. What is new is
the question asked of them.

**A negative result is the easiest artefact here to corrupt** — nobody re-reads it,
and one hand-edit promoting a firm to "dated 1834" would put a business in the town on
nobody's authority. So `tools/check.sh` rebuilds the whole file and diffs it, and runs
the tool's own twelve assertions: that the sketch route reads the printed quote and the
reader's entity index but never this project's gloss (the gloss says "Norris's summary
of the beginning", which would otherwise date the author's own 1844 firm to 1832), that
a one-surname firm needs an agreeing initial on both sides, and that a founding year
has to be carried by founding language rather than by a street number.
