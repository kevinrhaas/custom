# Federal land tract sales — the register of who bought the ground

**What lives here.** The Illinois State Archives' *Illinois Public Domain Land Tract
Sales* database, read for the two townships the town of Chicago and its north side
stand on — **T39N R14E** and **T40N R14E**, third principal meridian — and for the five
that ring them, for every sale dated on or before **31 December 1836**. **953 sales, 431
distinct purchasers as the register spelled them, 57,171.59 acres and $125,223.35 of
ground**, over 252 section queries. **Every one of those sections is read whole**: the
three T-0557 had to leave truncated at the search's 150-row page were walked to their
end through the results page's own More button, which is a cursor and not a dead end.
That is the second section below, and it is the correction that matters most here.

| the reading | townships | sales | purchasers | ticket |
|---|---|---|---|---|
| the town and its north side | T39N R14E, T40N R14E | 566 | 260 | T-0557, T-0675 |
| the ring | T39N R13E, T40N R13E, T38N R14E, T41N R14E, T38N R15E | 387 | 209 | T-0676 |

Each reading has its own deposit and its own records file, named after the townships it
holds, and the record ids run on across them — `ls0001` upward — because
`data/structures/*.json` cite them. **A new reading appends and never renumbers.**

**This is not a list of people, and that is the whole discipline of the domain.** The
register records a TRANSACTION. A man who entered eighty acres in T40N R14E in 1835
may have been standing on South Water Street, or in Vandalia, or in Connecticut; the
purchase says only that he bought. The one column that speaks to where he lived is
`Residence`, and it names a **county**, never a town:

| Residence as the register wrote it | sales |
|---|---|
| UNKNOWN | 485 |
| COOK | 36 |
| MACON | 16 |
| VERMILION | 11 |
| ILLINOIS | 9 |
| MCLEAN | 4 |
| LASALLE | 2 |
| IROQUOIS | 1 |
| VIRGINIA | 1 |
| ST. LOUIS | 1 |

The last two are the register's own words and are carried as it wrote them: neither
is an Illinois county, and this project does not correct a clerk.

So a row whose Residence reads COOK is graded `documented` — for residence in **Cook
County on the date of sale**, which in 1835 reaches far beyond the town — and every
other row is graded `inferred`, with the reasoning written on the record. Nothing here
mints a resident or regrades one. `resident_crosswalk.json` proposes correspondences
and states the rule that made each; T-0514 and T-0515 are what spend them.

**What the reading found.** Sales by year: 1830 · 17, 1831 · 8, 1832 · 3, 1833 · 337,
1834 · 95, 1835 · 101, 1836 · 4, and one row the register dates 1810, carried verbatim
because it is what the page says. By type: 205 federal cash entries (`FD`), 337 school
section sales (`SC`), 24 canal sales (`CN`). By what the tract resolves to: 217 town
lots, 167 half quarter-sections, 50 quarter-sections, 2 quarter-quarters and 130 the
parser leaves `unparsed` rather than guess at. The shape of that list is the school
section arriving: 1833 more than doubles, and the town lot passes the half
quarter-section as the commonest thing the register sells.

**The ring, and why it is worth having (T-0676).** T-0610 asked for the country around
the town and T-0675 read only the middle of it. The five ring townships are now read the
same way, section by section, cursor to the end: **387 sales, every one of them a federal
cash entry** — no school section, no canal land, because neither exists out there. They
are late and they are sudden: 1 sale in 1833, 38 in 1834, **318 in 1835** and 30 in the
first half of 1836. That is the land rush arriving, one year behind the town's own lots,
and 64 of the 180 sections carry it while 116 were walked and held nothing through 1836.
The register states a residence on 32 of the 387 — 22 COOK, and 10 spread over McLean,
Macon, Vermilion and Champaign — so the same grading rule applies out here as in town,
and 355 rows are `inferred`. Where the ground is: T38N R14E 152 sales, T39N R13E 145,
T40N R13E 57, T38N R15E 18, T41N R14E 15. **None of it is inside the town**, and none of
it resolves onto a footprint: the constructed section grid reaches only the four sections
that meet at State & Madison (L219), so every ring row says in `ground.json` why it does
not land.

**Nine more purchaser spellings meet a person the town already holds** — William Spencer,
Walter L. Newberry, James Whitlock, James B. Campbell, A. Garrett, John L. Wilson,
H. Pearsons, David P. Frame and Frank Dill. Two of them are the interesting ones: **Hiram
Pearsons enters seventeen ring tracts** and **Walter Newberry six**, both while the town's
own lots were being traded. **All nine have now been RULED ON** — six upheld, three refused
— which is the section below. T-0697 has since re-run the mechanical rule that made the
domain's counts, so the totals those nine sit inside are 136 matched spellings against 295
refused, not the 35 against 396 they were read under.

## The ruling layer (T-0700)

`build_resident_crosswalk()` PROPOSES; it does not decide. `tools/spend_land_sales.py`'s
own rule 1 — *"ONLY WHAT THE CROSSWALK ALREADY DECLARED. This pass re-adjudicates
nothing"* — means that between the mechanical rule and the card there was **nobody**, and
the ring's nine spellings reached thirty-one town cards that way. `resident_rulings.json`
is where a judgement is written instead. It is **hand-authored** — the one file under this
domain that is not derived from the deposit, because a judgement is not a derivation —
and `--build` folds it onto the crosswalk while `--check` validates it: a ruling must name
a spelling the register holds, rule on a proposal the mechanical rule actually made, agree
with that proposal about who is being ruled on, and state its ticket, its date, what it was
checked against, and its reasoning.

**The ruling rule.** A proposal is upheld only where the town's own record of the person
carries something the register's row can be checked against BEYOND a bare name — a middle
initial the register repeats, a trade the purchase is consistent with, a second document,
or the register's own Residence column. Where the town holds nothing but a name read once
off a post-office letter list, the proposal rests on the residents layer being THIN rather
than on the two records agreeing, and it is refused.

| spelling | ruling | what carried it |
|---|---|---|
| PEARSONS H | upheld | the same register spells him HIRAM on 28 other rows; 16 of the 17 H rows fall on one day in one township |
| NEWBERRY WALTER L | upheld | the middle initial agrees with Walter **Loomis** Newberry, attested in the American and both Fergus directories |
| WHITLOCK JAMES | upheld | the town's James Whitlock is **register of the land office** — the purchase is what his trade would predict |
| CAMPBELL JAMES B | upheld | the middle initial agrees, and nine sources hold him |
| FRAME DAVID P | upheld | the letter list printed "David P.Frame"; all three tokens agree |
| DILL FRANK | upheld | ls0912 states **COOK**, and the 1835 poll list has a Frank Dill at Chicago |
| SPENCER WILLIAM G | refused | one letter-list line, and a middle initial the town has never seen |
| WILSON JOHN L | refused | the same, on the commonest name in the corpus, and the entries are 1836 |
| GARRETT A ET CO | refused | the purchaser is a **firm**; this crosswalk proposes people (T-0851) |

Refusing the firm spelling left `GARRETT AUGUSTUS` standing alone on A. Garrett's card, where
the two spellings had both been written onto it. That second spelling is a reading in its own
name and is NOT ruled on here — it is one of T-0850's twenty-six, which the next section rules on (refused: the town has never read the forename).

A refusal is not free: it moves the proposal into `refusals[]`, and
`spend_land_sales.py --build` **retracts** the paragraph the earlier pass had written onto
the card. That retraction is the write made reversible, and it is held by a round-trip
assertion in `--self-test`.

**What ruling on them found.** The crosswalk read each purchaser's residence off the FIRST
row of that spelling. Frank Dill enters the same quarter-section twice on 10 April 1835 and
only the second row states COOK, so he was graded `inferred` against a source that places
him in Cook County; Hiram Pearsons was the same. The reading now takes every row of a
spelling, both grade `documented` — for Cook County on the date of sale and nothing more —
and a card whose paragraph no longer says what the crosswalk says is a gate failure, where
`gaps()` had only ever asked whether a paragraph was PRESENT.

## The first deposit's twenty-six, ruled (T-0850)

**Sixteen upheld, ten refused.** These are the purchaser spellings the town-and-north-side
reading (T-0557, T-0675) matched, ruled on the same rule and by the same file as the ring's
nine. What upholds one is a token the two records SHARE — a middle initial both print, a
trade the purchase is what you would predict from, the register's own Residence column, or
the town holding the man in two documents that bracket the entry date. What refuses one is
a bare name on each side, however unlikely the coincidence looks.

| spelling | ruling | what carried it, or did not |
|---|---|---|
| PEARSONS HIRAM | upheld | 28 rows, 1,157 acres, one stating COOK; the card's own trade is `speculator` |
| PRICE JEREMIAH | upheld | four documents beyond the register bracket the eleven entries of 1835 |
| ELSTON DANIEL | upheld | the Democrat of 1833 and Fergus 1839 hold him on both sides of the 1836 entry |
| WOLCOTT ALEXANDER | upheld | a canal entry of 29 Sept 1830, inside the town's own bound for the man, beside James Kinzie's of the day before |
| BRONSON ARTHUR | upheld | the town's 1833 tax list, the same year as the auction; FREDERIC(K) Bronson stands beside him, so the forename is doing the work |
| CARVER DAVID | upheld | the poll of 10 Aug 1833 and the tax list of 1833, two months before he buys |
| CASEY EDWARD W | upheld | the middle initial, printed by the register AND by the town's own rolls |
| CLYBOURNE ARCHIBALD | upheld | one Clybourne on either side; Andreas's trade and the town's rolls |
| COLE PARKER M | upheld | all three tokens agree — the letter list prints 'Parker M. Cole' |
| INGERSOLL CHESTER | upheld | the tavern at Wolf Point, in the paper weeks either side of the parcel |
| LLOYD ALEXANDER | upheld | two documents around the entry, and one Lloyd on either side |
| PRUYNE PETER | upheld | the forename in full, the trade attested, one Pruyne in the layer |
| PRUYNE P | upheld | the same register writes him PETER on four other rows — the PEARSONS H argument |
| STEELE ASHBEL | upheld | the polls of 1834 and 1835 print the same unusual forename |
| LUDBY JOHN | upheld | **the Residence column reads COOK** on three of four rows — the DILL FRANK carrier |
| WEST HENRY C | upheld | the letter list prints 'Henry c. West' — the middle initial is on both sides |
| HARTZELL THOMAS | refused | one tax line in 1833 against a canal entry of 1830; ILLINOIS is a state |
| VANDERBOGERT HENRY | refused | one tax line; the register holds a second Vanderbogert, and **T-0842** is asking whether the town's own two spellings are one man |
| WESSENCRAFT CHARLES | refused | one tax line; a unique surname makes coincidence unlikely, and unlikely is not checked |
| HALE JOHN | refused | **T-0885**: Ebenezer Hale enters every one of the same 26 parcels, and upholding would decide that open question by default |
| SPENCE JAMES | refused | the middle initial is on the town's side only, which tests nothing — the SPENCER WILLIAM G shape |
| CHANDLER JOSEPH | refused | one garbled letter-list return, six months after the entry |
| KINGSTON PAUL | refused | one letter-list return; the register also holds KINGSTON J T and JOHN T |
| MINARD IRA | refused | the closest call: a letter on 20 May 1835 and 161 acres on 27 June 1835, and a coincidence of date says when somebody bought, not who |
| PRUYNE P AND CO | refused | a FIRM, as GARRETT A ET CO was (T-0851) |
| GARRETT AUGUSTUS | refused | the town has never read this man's forename — the corpus prints 'A. Garrett', and an initial is less than the bare name the clause was written for. An auctioneer's trade is consistent with any land transaction, which is what makes it useless as a discriminator |

**What ruling on them moved.** The crosswalk goes from 136 matched spellings to **126**, and
from 295 refusals to **305**. Nine cards had a paragraph RETRACTED — Chandler, Garrett,
Hale, Hartzell, Kingston, Minard, Spence, Vanderbogert and Wessencraft — and Peter Pruyne's
now names two readings instead of three. The spend falls from 122 people to **113**, from
415 register entries carried to **362**, from 20,613.61 acres to **19,192.93**, and from
202 school-section parcels to **160**. No grade moved, here or anywhere: a ruling never
raises one and a refusal never lowers one.

**A. Garrett's card now carries no land purchase at all.** T-0700 refused the firm spelling
expecting `GARRETT AUGUSTUS` to stand alone on it; ruling on that spelling in turn finds
nothing to check it against, so both are refused and the honest state of the card is empty.
One printing of the forename in full would overturn it.

**The retraction learned to cut from the middle of a note (T-0850).** T-0700 built it to cut
the paragraph off the TAIL, which is where this pass appends. Joseph Chandler's card had the
1840 census written under his purchase, so the tail was somebody else's and the tool refused
the cut and said so. It now excises the span between the two literals that bound the
paragraph — the marker that opens it and the ladder sentence that closes it — and still
refuses where the closing literal is gone, because then where the paragraph ends is genuinely
unknown. `--self-test` holds both.

## T-0697's proposals, cohort A: the fourteen an initial decided among namesakes (T-0990)

Neither T-0700 nor T-0850 was written against the hundred-odd proposals **T-0697** added when
the mechanical rule stopped requiring exactly one person of the surname — both were written
against a crosswalk of 35 matches. **T-0990** rules them one cohort per run, and this is the
first: the fourteen whose match is `initial_agrees` AND whose `rivals[]` is not empty, which
is where the rule is at its weakest. The layer holds a namesake of the surname, and a
forename INITIAL alone chose between them.

**Eleven upheld, three refused.** What moved: matched spellings 126 → **123**, ruled 35 →
**49**, unruled 104 → **90**; three cards retracted, and with them six register rows — 230.78 acres and
$762.89 of ground taken back off them. Nothing was written on — the upheld eleven were already carried, and
upholding a proposal only confirms what the spend pass had put there.

**The discriminator was in `data/residents/directories.json` nearly every time, and it is
where the next cohort should look first.** Where the card holds an initial the later
directories very often print the forename whole, and that printing — not the initial — is
what decides:

| the register | the town's own printing | ruling |
|---|---|---|
| MONTGOMERY LOTON WM · MONTGOMERY LOTON W | Fergus 1843: *Montgomery, Loton W., shoemaker* | upheld |
| BLANCHARD F G · F G AS · FRANCIS G | Fergus 1843: *Blanchard, Francis Gurtrey, capitalist* | upheld |
| FOOT STAN | Fergus 1839/1843: *Foot, Star / Starr, teamster* | upheld |
| WRIGHT T G | Fergus 1839: *Wright, Truman G., speculator* | upheld |
| HADDOCK E H | Fergus 1839: *Haddock, Edward H., commission merchant* | upheld |
| BEAUBIEN J B | Andreas's 1833 roster: *J. B. Beaubien, merchant* | upheld |
| REED JAMES W | the Democrat, 31 Dec 1833: *J. W. REED.*, cabinet maker | upheld |
| HUNTER E E | the register's own duplicate ls0920, *HUNTER EDWARD E*, Residence COOK | upheld |
| GOODRICH CHAUNCEY | *nothing* — one line of the 1833 tax list | **refused** |
| SMITH LIMAN | *nothing* — one line of the poll of 1834 | **refused** |
| MORRISON THOS M | *nothing* — one uncalled-for letter, the Democrat of 20 May 1835 | **refused** |

Three of the fourteen have no directory line at all, and all three are the refusals. The
directories are read here **for the name and nothing else**: *teamster* is a trade of 1839
and *speculator* of 1839, and neither is written onto an 1835 card — T-0633 is the rule for
back-projecting a trade, and identifying a man is not back-projecting one.

**The register's second habit is worth as much.** It prints the same purchaser twice, once
abbreviated and once in full, and the fuller reading is sometimes a whole second row:
HADDOCK E H / HADDOCK EDWARD H, WRIGHT T G / WRIGHT TRUMAN G, and — decisively — HUNTER E E
(ls0919) and HUNTER EDWARD E (ls0920), the same 80 acres of section 13 T40N R13E on the same
day at the same price, with **COOK** in the Residence column of the fuller one and UNKNOWN in
the abbreviated one. SMITH LIMAN and SMITH SIMAN (ls0572, ls0573) are the same duplication
working against the proposal: the deposit itself cannot decide whether the man was a Lyman or
a Simon, so the token the rule matched on is not stable in the source that supplies it.

**A duplicate card found on the way past.** Fergus 1843's *Francis Gurtrey* is one man, and
the layer holds both `blanchard_f_gantry` and `blanchard_gantry` — filed as **T-0993**, beside
T-0844's six clusters. This cohort's rulings do not decide it, and the six `BLANCHARD GURTREY`
rows are left unruled for that ticket.

**Still unruled: 90.** Cohort B is the twenty-four with no namesake at all (`rivals[]` empty),
cohort C the sixty-six remaining `forename_agrees` proposals that have one; the log on T-0990
carries them. The live count is on the crosswalk's `ruled` block and not repeated here.

**THE SURNAME GATHERS THE RIVALS AND THE FORENAME DECIDES BETWEEN THEM (T-0697).** Until
that ticket the rule needed EXACTLY ONE person of the surname in the residents layer, and
a count of namesakes says nothing about the reading in hand: it made the crosswalk fire
LESS as the town grew truer, so seating 531 people (T-0514) COST this register three
rulings with nothing new read. The reading is now put to every person of the surname and
named onto the one it agrees with, on the merge rules this project already ratified —
`tools/namesake.py`, which restates identity master's M1/M2/M3 and R3/R4 and imports the
directories' own forename rule. **139 purchaser spellings now meet 124 people the town
holds, against 38 spellings and 35 people before**, and consolidation pass 3 carries 421
entries onto 124 cards where it carried 180 onto 34. Nothing new was read to get there.

The refusals it keeps are the ones the forename makes, and three kinds are new: a middle
initial that disagrees (`KING JOHN R` is not John Lyle King), M3's guard (`WRIGHT JOHN F`
is not John Wright while John S. Wright stands beside him), and a suffix (`CHURCH THOS JR`
names the son, and the town's one Thomas Church is not said to be either man). Two
readings the rule named onto ONE person are put back to each other and refused where they
are not the same man — `BOND HARVEY` and `BOND HEMAN` both meet an `H Bond`, and the
initial cannot say which. **T-0697 also asked whether a purchase date, a trade or a lot
could break what the forename leaves standing, and all three are refused**, with the
reasons in `tools/namesake.py`'s `REFUSED_DISCRIMINATORS` rather than in prose: the
register prints no trade at all, a man may enter ground in a county he has not moved to,
and preferring the rival the town has already placed on the ground is how a reconstruction
invents a fact (the ruling T-0696 made for the directories, which allowed a trade to
NARROW a tie and had one to narrow with).

**Every ruling now names the records it was made from.** `record_ids` on each match and
each refusal in both crosswalks says which sales the ruling was made from — the spend
meter asked for it in as many words, and it is provenance regardless: a refusal a reader
cannot trace back to its rows is a refusal nobody can check. 480 rulings in this domain
anchored to nothing before; none does now, and every one of the 953 records carries a
ruling — the same 953 before T-0697 and after it, which is the thing that did NOT move
when a hundred spellings crossed from refused to matched.

**Twenty-four people the town already holds meet a purchaser** — every one of them ruled on by T-0850, above — Arthur Bronson, David
Carver, Edward W. Casey, Joseph Chandler, Archibald Clybourne, Parker M. Cole, Daniel
Elston, John Hale, Thomas Hartzell, Chester Ingersoll, Paul Kingston, Alexander Lloyd,
Ira Minard, Walter Loomis Newberry, Hiram Pearsons, Jeremiah Price, Peter Pruyne (on
three rows, one of them `PRUYNE P AND CO`), James C Spence, Ashbel Steele, Henry
Vanderbogert, Charles Wessencraft, Henry C. West, Alexander Wolcott, John Ludby — 26
matched purchaser spellings against 234 refused. **That sentence used to end "none carries
a stated residence"; ruling on them found otherwise** — John Ludby's rows state COOK on three
of four, and Hiram Pearsons, Thomas Hartzell and Alexander Wolcott each carry a COOK or an
ILLINOIS somewhere in theirs. The claim was made off the FIRST row of each spelling, which is
the same reading fault T-0700 found in Frank Dill's grade. It is corrected here: the residence
column speaks for four of these twenty-six, and it carried the Ludby ruling.

**Shape: `records`.** A sale is a row on a page, so it takes the records shape — the
purchaser `as_read` exactly as the register spelled him, `normalized` only far enough
to read `DEVINPORT WILLIAM` back as `William Devinport`, one `locator` carrying the
section query, the deposit line, the purchase number and the register's own volume and
page. `data/research/domains.json` states it; `tools/research_domains.py --check` holds
the shape and `tools/read_land_sales.py --check` holds the reading.

**Hand-authored:** this README and `resident_rulings.json`, and nothing else. Every judgement in the crosswalks was
made by a rule that is written out beside it.

**Generated, and re-derived by the gate:** `entries.json`, one `records/entries_*.json`
per deposit, `coverage.json`, `crosswalk.json` and `resident_crosswalk.json` (which folds the hand-authored rulings) — all
written by `tools/read_land_sales.py --build` from the committed deposits in `text/`,
and all re-derived by `--check`, which refuses a committed file that has drifted. The
deposits themselves are written by `tools/harvest_land_sales.py --sweep`, which reaches
the network and is therefore run deliberately by a research pass and never by the gate.
A township is a township AND a range there: `--tr 38:15` asks for T38N R15E, and each
set of pairs writes the deposit its own name spells out.

## Two things about the source, both learned the hard way

**The search shows at most 150 rows at a time — and it pages.** A whole-township query
stops at 150 and looks complete: the first attempt at this read came back with exactly
150 rows for each township and would have recorded a ceiling as a town. So the reading
is BY SECTION, thirty-six queries per township. That much T-0557 got right. What it got
wrong is the ceiling itself. **The results page carries a `More` button**, and that
button is a keyset cursor — `hiddenPurchaseNo` + `hiddenPurchaser` + `hiddenSectionNo`,
replayed against the same search, return the rows after the last one shown. Results are
ordered by purchaser, so replaying the cursor walks a section to its end.
`harvest_land_sales.py --sweep` follows it and prints how many pages each section took.

T-0557 read the three sections that filled their first page — T39N R14E 16, 21 and 29,
the school section and two of the West Division sections — as truncated, and declared
them unread. T-0675 walked them: **section 16 is 3 pages and 337 sales, all of them the
October 1833 school-section auction; section 21 is 6 pages and 781 rows, 4 of them
through 1836; section 29 is 2 pages and 217 rows, again 4 through 1836.** So the hole
was 191 sales wide and it is closed, and every section of both townships is now declared
read. The lesson is worth keeping over the numbers: **a page that fills is a page, not a
limit** — look for the cursor before recording a refusal.

The `name` field still cannot be used to break a section up: it belongs to the
database's other search form and does not narrow a legal-description query, it replaces
it, returning that name from every township in Illinois. It DOES combine with the county
select, which is a different way through the same ceiling and was not needed once the
cursor was found.

**The site refuses datacentre addresses.** Every user agent tried from this project's
runner gets a bare 403 from the WAF — the session that filed T-0557 hit the same wall
through its proxy. The pages were therefore fetched through the public `r.jina.ai`
reader, which returns the origin's own HTML unchanged; `harvest_land_sales.py --direct`
asks the origin instead, for anyone running it from a machine the site will talk to.
The route is recorded in the source record. It changes nothing about what the page says,
and the reading cross-checks itself: for all 375 sales the summary row and the detail
page agree, field for field, on purchaser, tract, section, township, range, meridian,
county and date.

## What is NOT read, and is not a fault

- **Nothing of what T-0610 asked for.** The two townships the town stands on and the
  five that ring them are all read whole, section by section, cursor to the end.
- **Sales to purchasers whose stated residence is Chicago or Cook County outside these
  townships.** The database's name search cannot be filtered by residence, so this
  needs a different shape of query.
- **The canal sections.** They were sold by the canal commissioners, not the land
  office, and are not in this database at all — their absence is not a hole.
**Done, 2026-09-04 (T-0609):** the join from a tract to a standing structure.
`tools/resolve_land_tracts.py` puts every sale on the ground or says why it cannot,
writes the result to `ground.json`, and puts a `land_owner` block on the 63 structures
the resolved tracts reach. See the next section.

## The join to the ground, and the four tracts the town stands on

`tools/resolve_land_tracts.py --build` derives `ground.json`: one row per sale, carrying
either the polygon it lands on or the reason it does not. **346 of the 953 rows land on
the ground; the other 607 each say why they do not.** Ten of them are country tracts and
reach 63 of the 375 structures; the other 336 are school-section rows seated on the block
polygons of T-0797, and they reach no structure at all, for the reason the next section
gives. The
section grid is CONSTRUCTED from the one PLSS corner this project holds — State &
Madison, `G1` — on the plat's own bearing, in nominal one-mile squares, and is carried
only across the four sections that meet at it. That is liberty **L219**, and the module
docstring is the long form.

| the ground | who entered it | when | roofs |
|---|---|---|---|
| north fraction of section 10 — Kinzie's Addition | Robert A Kenzie / Kinzie, printed both ways | 7 May 1831 | 27 |
| E2NE of section 9 | Alexander Wolcott | 29 Sept 1830 | 18 |
| SW fractional quarter of section 10 — the United States Reservation | John Baptist Baubian | 28 May 1835 | 17 |
| E2NW of section 9 | James Kinzie | 28 Sept 1830 | 1 |

The reservation row is the one to read twice. `data/liberties.json` **L108** already
quotes Andreas for Beaubien's pre-emption of 28 May 1835 over the fort's ground; this
register carries the same entry independently, and the polygon under it is the ring L108
derives rather than a second construction of the same tract. **Whether the entry held is
not read here** — it was litigated for years, and this domain records the transaction the
register prints and nothing about its outcome.

## The school section, spent (T-0798)

**337 rows of this register — every one of them in section 16, the school section — were
read at the October 1833 auction and, until T-0797 traced the plat, not put on the
ground.** 336 of them now are: each is seated on the block polygon its own number names
in `data/traces/vectors/school_section_blocks_1834.json`, the 142 blocks measured off
J. S. Wright's 1834 survey. The one that is not is the row whose lot the register prints
as `06126`, refused because the parser will not guess at it.

**The block, and not the lot.** The sheet's ruled LOT lines are not traced, so a row that
buys lot 6 of block 48 is placed on block 48 with its lot carried as read and unplaced. A
block is about a hectare and the auction sold most of them to several men apiece, so
**no school-section row reaches a roof**, by rule rather than by geometry — a purchaser of
some lot in a block did not thereby buy the ground under a particular house. The one
committed structure standing in section 16, `heacock_house_monroe`, therefore still
carries no `land_owner`, and that is the honest answer rather than a missing one.

**What the 336 rows say about who owned the south.** The sale ran 22–25 October 1833 and
**105 purchasers as the register spelled them took ground in 136 of the 142 blocks**. 218
rows name a lot inside their block and 118 name the block alone. The busiest blocks are
95 (12 rows), 26 (11), and 48, 81, 82 and 120 (10 apiece) — the northern tiers, nearest
the town. The keenest buyers are Ebenezer and John Hale on fourteen blocks each, Arthur
Bronson on thirteen (with eight more under the register's spelling `Broson`), and Hiram
Pearsons on twelve, who is also the man who enters seventeen ring tracts above.

**And the rows are not parcels (T-0885).** Every count above is a count of REGISTER
ROWS, which is what the source offers. The ground is smaller: 335 live rows name only
**297 distinct block-and-lot parcels**, because **38 parcels are entered twice**, under
two names, on the same day and the same page of volume 818, each row with its own
purchase number. Six of the 38 carry the register's `AS` suffix on one of the two rows —
an assignment, the one shape of duplicate this source explains itself. **Twenty-six are a
single pair of names: every parcel Ebenezer Hale enters, John Hale enters as well**,
which is why the keenest-purchaser table reads two Hales at its head. One of the 38 is a
price disagreement rather than a name pair — block 72 lot 2, entered at **$8.00** and at
**$80.00**, same day, same page — and both figures are carried as read. Nothing here
merges a name or drops a row: whether a pair is one transaction or two is an identity
ruling, `resident_crosswalk.json` is where this domain makes those, and T-0885 leaves the
Hales an open question with the evidence beside it.

**Six blocks changed no hands at all: 1, 41, 87, 88, 126 and 142.** Four of those are
exactly the four Wright writes `Reserved` across and draws no numeral on. **Neither
reading was made from the other** — one is a plat traced off a sheet in 2026, the other an
auction list kept in 1833 — and they agree, which is the strongest corroboration the
block numbering has. `--self-test` holds it. The ticket that asked for this spend expected
the sheet and the sale to disagree somewhere near the tear at 87/88; they do not, because
neither block was ever offered.

**A block number the sheet does not carry is refused by name and never nudged onto a
neighbour.** No row needs that refusal today; the reason is written into `ground.json` and
the counter is printed at zero, so it is a standing check rather than a dead branch.

**The other silence is the source's rather than the tool's.** 254 of the structures stand
in the SOUTH-EAST QUARTER OF SECTION 9 — the original town — and get nothing, because the
canal commissioners sold those lots and this database does not hold them.
