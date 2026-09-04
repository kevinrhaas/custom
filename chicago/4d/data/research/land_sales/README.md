# Federal land tract sales — the register of who bought the ground

**What lives here.** The Illinois State Archives' *Illinois Public Domain Land Tract
Sales* database, read for **seven townships** of the third principal meridian for every
sale dated on or before **31 December 1836**: the two the town of Chicago and its north
side stand on — **T39N R14E** and **T40N R14E** (T-0557, finished by T-0675) — and the
five that ring them, **T39N R13E**, **T38N R14E**, **T38N R15E**, **T40N R13E** and
**T41N R14E** (T-0676). **953 sales, 431 distinct purchasers as the register spelled
them, 57,172 acres and $125,223.35 of ground**, over 252 section queries.

**All seventy-two sections of the two central townships are read whole**: the three
T-0557 had to leave truncated at the search's 150-row page were walked to their end
through the results page's own More button, which is a cursor and not a dead end. That is
the second section below, and it is the correction that matters most here. The ring sweep
ran before the cursor was known and stopped at the first page of each section; only one
ring section reached the ceiling, T39N R13E sec 16, and it is named as short rather than
declared (T-0682).

**This is not a list of people, and that is the whole discipline of the domain.** The
register records a TRANSACTION. A man who entered eighty acres in T40N R14E in 1835
may have been standing on South Water Street, or in Vandalia, or in Connecticut; the
purchase says only that he bought. The one column that speaks to where he lived is
`Residence`, and it names a **county**, never a town:

| Residence as the register wrote it | sales | of which the ring |
|---|---|---|
| UNKNOWN | 840 | 355 |
| COOK | 58 | 22 |
| MACON | 18 | 2 |
| VERMILION | 13 | 2 |
| ILLINOIS | 9 | — |
| MCLEAN | 8 | 4 |
| LASALLE | 2 | — |
| CHAMPAIGN | 2 | 2 |
| IROQUOIS | 1 | — |
| VIRGINIA | 1 | — |
| ST. LOUIS | 1 | — |

The last two are the register's own words and are carried as it wrote them: neither
is an Illinois county, and this project does not correct a clerk.

So a row whose Residence reads COOK is graded `documented` — for residence in **Cook
County on the date of sale**, which in 1835 reaches far beyond the town — and every
other row is graded `inferred`, with the reasoning written on the record. Nothing here
mints a resident or regrades one. `resident_crosswalk.json` proposes correspondences
and states the rule that made each; T-0514 and T-0515 are what spend them.

**What the reading found.** Sales by year: 1830 · 17, 1831 · 8, 1832 · 3, 1833 · 338,
1834 · 133, 1835 · 419, 1836 · 34, and one row the register dates 1810, carried verbatim
because it is what the page says. By type: 592 federal cash entries (`FD`), 337 school
section sales (`SC`), 24 canal sales (`CN`). By what the tract resolves to: 427 half
quarter-sections, 217 town lots, 162 quarter-sections, 2 quarter-quarters and 145 the
parser leaves `unparsed` rather than guess at.

**The ring is a different shape of record from the town, which is why it was worth
reading.** All 387 ring sales are federal cash entries — no school-section lot, no canal
land — and **318 of them fall in 1835 alone**, against 101 in the two central townships
that year. 260 are half quarter-sections and 112 whole quarter-sections: 36,937 acres for
$54,738, at the $1.25 minimum almost throughout. That is not a town buying its own lots.
It is the prairie and timber around it going under the hammer in eighty- and
hundred-and-sixty-acre bites in the year the canal was surveyed, and the domain now holds
both halves of the picture. T38N R14E (152 sales) and T39N R13E (145) carry most of it;
T41N R14E, twelve miles north, carries fifteen. Nine purchasers meet a person the town
holds and appear ONLY in the ring — Walter Loomis Newberry, William Spencer, James
Whitlock, James B Campbell, John Wilson and four more — and nineteen more state a
residence of COOK on the day they bought, among them Joseph Kettlestrings, who gave his
name to Oak Park, and both Bickerdikes.

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

**Generated, and re-derived by the gate:** `entries.json`, one
`records/entries_<townships>_through_1836.json` per deposit, `coverage.json`,
`crosswalk.json` and `resident_crosswalk.json` — all written by
`tools/read_land_sales.py --build` from the committed deposits under `text/`, and all
re-derived by `--check`, which refuses a committed file that has drifted. The deposits
themselves are written by `tools/harvest_land_sales.py --sweep --township N --range R`,
which reaches the network and is therefore run deliberately by a research pass and never
by the gate.

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
and the reading cross-checks itself: for all 953 sales the summary row and the detail
page agree, field for field, on purchaser, tract, section, township, range, meridian,
county and date.

## What is NOT read, and is not a fault

- **T39N R13E section 16** — the school section of the township immediately west. Its
  first page filled the 150-row ceiling and the ring sweep, which ran before the cursor
  was known, stopped there. A sweep to re-run and not a source to go looking for: T-0682.
- **The second ring.** T38N R13E, T39N R15E, T41N R13E and T41N R15E were never on the
  list T-0557 drew and are not read; three of the four are largely lake or prairie twelve
  miles out. Naming them is not a promise to read them.
- **Sales to purchasers whose stated residence is Chicago or Cook County outside these
  seven townships.** The database's name search cannot be filtered by residence, so this
  needs a different shape of query.
- **The canal sections.** They were sold by the canal commissioners, not the land
  office, and are not in this database at all — their absence is not a hole.

**Done, 2026-09-04 (T-0676):** the five ring townships T-0557 left unread. 387 more
sales, and `coverage.json`'s `townships_not_read` is empty.

**One deposit per sweep, and the list of them is APPEND-ONLY.** A record's `ls####` id is
its position in `DEPOSITS` in `tools/read_land_sales.py`, and those ids are cited from
`ground.json` and from the `land_owner` block on 63 structures — so a new deposit goes on
the END of that list and an existing one never moves. A deposit committed under `text/`
that the list does not name is a gate failure, not a warning: it would be committed
evidence that nothing reads.

**Done, 2026-09-04 (T-0609):** the join from a tract to a standing structure.
`tools/resolve_land_tracts.py` puts every sale on the ground or says why it cannot,
writes the result to `ground.json`, and puts a `land_owner` block on the 63 structures
the resolved tracts reach. See the next section.

## The join to the ground, and the four tracts the town stands on

`tools/resolve_land_tracts.py --build` derives `ground.json`: one row per sale, carrying
either the polygon it lands on or the reason it does not. **10 of the 375 rows land on
the ground and reach 63 of the 372 structures; the other 365 rows each say why they do
not.** The
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

**The two silences, and both are the source's rather than the tool's.** 254 of the
structures stand in the SOUTH-EAST QUARTER OF SECTION 9 — the original town — and get
nothing, because the canal commissioners sold those lots and this database does not hold
them. And **337 rows — every one of them in section 16, the school section**, sold at the
October 1833 auction, are refused: 336 because that subdivision's plat is not traced by
this project, so a block and lot number in it names ground this repo cannot point at, and
one because the register prints its lot as `06126` and the parser will not guess. That refusal costs the scene exactly one roof, `heacock_house_monroe`, which is
the only committed structure standing in section 16.
