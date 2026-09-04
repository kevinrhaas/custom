# Federal land tract sales — the register of who bought the ground

**What lives here.** The Illinois State Archives' *Illinois Public Domain Land Tract
Sales* database, read for **seven townships** of the third principal meridian for every
sale dated on or before **31 December 1836**: the two the town of Chicago and its north
side stand on — **T39N R14E** and **T40N R14E** — and the five that ring them,
**T39N R13E**, **T38N R14E**, **T38N R15E**, **T40N R13E** and **T41N R14E**.
**762 sales, 381 distinct purchasers as the register spelled them, 56,642 acres and
$98,368.92 of ground**, over 252 section queries. The two central townships are T-0557
(375 sales); the ring is T-0677 (387).

**This is not a list of people, and that is the whole discipline of the domain.** The
register records a TRANSACTION. A man who entered eighty acres in T40N R14E in 1835
may have been standing on South Water Street, or in Vandalia, or in Connecticut; the
purchase says only that he bought. The one column that speaks to where he lived is
`Residence`, and it names a **county**, never a town:

| Residence as the register wrote it | sales | of which the ring |
|---|---|---|
| UNKNOWN | 651 | 355 |
| COOK | 58 | 22 |
| MACON | 18 | 2 |
| VERMILION | 13 | 2 |
| ILLINOIS | 9 | — |
| MCLEAN | 8 | 4 |
| CHAMPAIGN | 2 | 2 |
| LASALLE | 2 | — |
| IROQUOIS | 1 | — |

So a row whose Residence reads COOK is graded `documented` — for residence in **Cook
County on the date of sale**, which in 1835 reaches far beyond the town — and every
other row is graded `inferred`, with the reasoning written on the record. Nothing here
mints a resident or regrades one. `resident_crosswalk.json` proposes correspondences
and states the rule that made each; T-0514 and T-0515 are what spend them.

**What the reading found.** Sales by year: 1830 · 13, 1831 · 8, 1832 · 3, 1833 · 151,
1834 · 133, 1835 · 419, 1836 · 34, and one row the register dates 1810, carried verbatim
because it is what the page says. By type: 592 federal cash entries (`FD`), 150 school
section sales (`SC`), 20 canal sales (`CN`). By what the tract resolves to: 423 half
quarter-sections, 162 quarter-sections, 113 town lots, 2 quarter-quarters and 62 the
parser leaves `unparsed` rather than guess at.

**And what the ring adds, which is a different shape of thing entirely.** All 387 ring
sales are federal cash entries — no school section, no canal land — and **318 of them
fall in 1835 alone**, against 101 in the two central townships that year. 260 are half
quarter-sections and 112 are whole quarter-sections: 36,937 acres for $54,738, at the
$1.25 minimum almost throughout. That is not the town buying its own lots. It is the
country around the town going under the hammer in the year the canal was surveyed, in
eighty- and hundred-and-sixty-acre bites, and this domain now holds both halves of that
picture rather than the town half alone. T38N R14E (152 sales) and T39N R13E (145) carry
most of it; T41N R14E, twelve miles north, carries fifteen.

**Twenty-seven purchasers meet a person the town already holds**, thirteen of whom
appear only in the ring — Walter Loomis Newberry, Peter Pruyne, Chester Ingersoll,
Frank Dill, James B Campbell, John Wilson, Henry C. West and six more. Nineteen ring
purchasers carry a stated residence of COOK, among them Joseph Kettlestrings (who gave
his name to Oak Park), both Bickerdikes, Elijah Wentworth Sen and Zebiah W Wentworth;
matching those to people is work T-0514 and T-0515 spend, not work this pass did. The
match set is DERIVED against the residents layer as it stands today — the rule needs
exactly one person of the surname in the town — so it moves when the town does, and it
has: names T-0557 matched are refused now that the layer holds more than one of their
surname, which is the rule working and not a regression.

**Shape: `records`.** A sale is a row on a page, so it takes the records shape — the
purchaser `as_read` exactly as the register spelled him, `normalized` only far enough
to read `DEVINPORT WILLIAM` back as `William Devinport`, one `locator` carrying the
section query, the deposit line, the purchase number and the register's own volume and
page. `data/research/domains.json` states it; `tools/research_domains.py --check` holds
the shape and `tools/read_land_sales.py --check` holds the reading.

**Hand-authored:** this README, and nothing else. Every judgement in the crosswalks was
made by a rule that is written out beside it.

**Generated, and re-derived by the gate:** `entries.json`, one
`records/entries_<township>_through_1836.json` per deposit, `coverage.json`,
`crosswalk.json` and `resident_crosswalk.json` — all written by
`tools/read_land_sales.py --build` from the committed deposits under `text/`, and all
re-derived by `--check`, which refuses a committed file that has drifted. The deposits
themselves are written by `tools/harvest_land_sales.py --sweep --township N --range R`,
which reaches the network and is therefore run deliberately by a research pass and never
by the gate.

**One deposit per sweep, and the list of them is APPEND-ONLY.** A record's `ls####` id is
its position in `DEPOSITS` in `tools/read_land_sales.py`, and those ids are cited from
`ground.json` and from the `land_owner` block on 63 structures — so a new deposit goes on
the END of that list and an existing one never moves. Reordering would silently repoint
every one of those citations at a different sale. A deposit committed under `text/` that
the list does not name is a gate failure, not a warning: it would be committed evidence
that nothing reads.

## Three things about the source, all learned the hard way

**The search returns at most 150 rows and offers no paging.** A whole-township query
stops at 150 and looks complete — the first attempt at this read came back with exactly
150 rows for each township and would have recorded a ceiling as a town. So the reading
is BY SECTION, thirty-six queries per township, 252 in all. Two hundred and forty-eight
sections came back under the ceiling and were read whole; `coverage.json` declares the
ones that hold a sale through 1836 and lists the rest as queried and empty, which is read
rather than a hole. **Four sections did not come back under the ceiling** — T39N R14E
sections 16, 21 and 29 (the town's school section and two West Division sections) and
T39N R13E section 16 (the school section of the township immediately west). What this
repo holds for those four is the first 150 rows the search would give, and they are
deliberately **not declared read**.

**And section is as fine as the search goes.** T-0677 went back over the form to look
for a way past the ceiling and there is not one. `pubdomsrch.jsp` offers exactly three
searches and says so: section/township/range/meridian, township/range/meridian, and
county — and of county, "the name of county cannot be used in combination with any other
search criteria". The result page carries no paging control, no offset and no sort; the
only other inputs on either form are the hidden `srchType=domain` and
`fromPage=pubDomSrch`. The `name` field belongs to the other search form and does not
narrow a legal-description query, it REPLACES it, returning that name from every township
in Illinois — and it hits the same ceiling itself (`name=HALE` returns 150 rows). The
rows come back ordered by purchaser, so the ceiling cuts the alphabet: section 16 returns
BARCKENBILE CHRISTIA through HALE JOHN and stops, and every one of those 150 is October
1833, so the unread remainder is 1833 town lots and not the later city sales. **Reading
past the ceiling therefore needs a different SOURCE — the BLM GLO patents, or the
commissioners' own ledger of the October 1833 sale — and not a cleverer query.** T-0678
holds that, with the two dead ends written out.

**A page the reader proxy drops looks exactly like a section with no sales.** `rows_of`
finds no rows in an error body, and the first ring sweep quietly wrote 51 sections off as
empty that had never been fetched at all — 66 sales missing, and a section 16 whose
truncation nobody would have noticed. The sweep now checks every section page for a body
that is actually the search's own, retries the misses on their own, and REFUSES TO WRITE
A DEPOSIT while one is still missing; the same retry runs on detail pages. Both are worth
knowing about: a research gate that goes red for the network's reasons is bad, but a
sweep that silently records a dropped page as an empty section is much worse, because it
declares coverage over ground nobody looked at. As a check on the older read, every one
of the 252 section pages was re-fetched and the pre-1837 row counts compared section by
section against all six deposits: **they agree exactly, T-0557's included.**

**The site refuses datacentre addresses.** Every user agent tried from this project's
runner gets a bare 403 from the WAF — the session that filed T-0557 hit the same wall
through its proxy. The pages were therefore fetched through the public `r.jina.ai`
reader, which returns the origin's own HTML unchanged; `harvest_land_sales.py --direct`
asks the origin instead, for anyone running it from a machine the site will talk to.
The route is recorded in the source record. It changes nothing about what the page says,
and the reading cross-checks itself: for all 762 sales the summary row and the detail
page agree, field for field, on purchaser, tract, section, township, range, meridian,
county and date.

## What is NOT read, and is not a fault

- **T39N R14E sections 16, 21 and 29, and T39N R13E section 16** — truncated at the
  ceiling, as above. T-0678.
- **Sales to purchasers whose stated residence is Chicago or Cook County outside these
  seven townships.** The database's name search cannot be filtered by residence, so this
  needs a different shape of query.
- **The second ring.** T38N R13E, T39N R15E, T41N R13E and T41N R15E were never on the
  list T-0557 drew and are not read; three of the four are largely lake or prairie
  twelve miles out. Naming them is not a promise to read them.
- **The canal sections.** They were sold by the canal commissioners, not the land
  office, and are not in this database at all — their absence is not a hole.

**Done, 2026-09-04 (T-0677):** the five ring townships T-0557 left unread. 387 more
sales, and `coverage.json` now carries an empty `townships_not_read`.

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
them. And **150 rows, every town-lot and block-only sale in the register, are in section
16, the school section**, sold at the October 1833 auction; that subdivision's plat is
not traced by this project, so a block and lot number in it names ground this repo cannot
point at. That refusal costs the scene exactly one roof, `heacock_house_monroe`, which is
the only committed structure standing in section 16.
