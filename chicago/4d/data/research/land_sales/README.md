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
H. Pearsons, David P. Frame and Frank Dill — which is 35 matched spellings against 396
refused across the whole domain. Two of them are the interesting ones: **Hiram Pearsons
enters seventeen ring tracts** and **Walter Newberry six**, both while the town's own
lots were being traded. None carries a stated residence, so all nine are `inferred`, and
nothing here mints or regrades a resident.

**Every ruling now names the records it was made from.** `record_ids` on each match and
each refusal in both crosswalks says which sales the ruling was made from — the spend
meter asked for it in as many words, and it is provenance regardless: a refusal a reader
cannot trace back to its rows is a refusal nobody can check. 480 rulings in this domain
anchored to nothing before; none does now, and the domain reads 953 against 511 ruled on.

**Twenty-four people the town already holds meet a purchaser** — Arthur Bronson, David
Carver, Edward W. Casey, Joseph Chandler, Archibald Clybourne, Parker M. Cole, Daniel
Elston, John Hale, Thomas Hartzell, Chester Ingersoll, Paul Kingston, Alexander Lloyd,
Ira Minard, Walter Loomis Newberry, Hiram Pearsons, Jeremiah Price, Peter Pruyne (on
three rows, one of them `PRUYNE P AND CO`), James C Spence, Ashbel Steele, Henry
Vanderbogert, Charles Wessencraft, Henry C. West, Alexander Wolcott, John Ludby — 26
matched purchaser spellings against 234 refused. None carries a stated residence: the
thirty-six COOK rows are other names, and matching them is work this pass did not do.

**Shape: `records`.** A sale is a row on a page, so it takes the records shape — the
purchaser `as_read` exactly as the register spelled him, `normalized` only far enough
to read `DEVINPORT WILLIAM` back as `William Devinport`, one `locator` carrying the
section query, the deposit line, the purchase number and the register's own volume and
page. `data/research/domains.json` states it; `tools/research_domains.py --check` holds
the shape and `tools/read_land_sales.py --check` holds the reading.

**Hand-authored:** this README, and nothing else. Every judgement in the crosswalks was
made by a rule that is written out beside it.

**Generated, and re-derived by the gate:** `entries.json`, one `records/entries_*.json`
per deposit, `coverage.json`, `crosswalk.json` and `resident_crosswalk.json` — all
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
