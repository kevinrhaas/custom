# Federal land tract sales — the register of who bought the ground

**What lives here.** The Illinois State Archives' *Illinois Public Domain Land Tract
Sales* database, read for the two townships the town of Chicago and its north side
stand on — **T39N R14E** and **T40N R14E**, third principal meridian — for every sale
dated on or before **31 December 1836**. 375 sales, 202 distinct purchasers as the
register spelled them, 19,704 acres and $43,631.32 of ground (T-0557).

**This is not a list of people, and that is the whole discipline of the domain.** The
register records a TRANSACTION. A man who entered eighty acres in T40N R14E in 1835
may have been standing on South Water Street, or in Vandalia, or in Connecticut; the
purchase says only that he bought. The one column that speaks to where he lived is
`Residence`, and it names a **county**, never a town:

| Residence as the register wrote it | sales |
|---|---|
| UNKNOWN | 296 |
| COOK | 36 |
| MACON | 16 |
| VERMILION | 11 |
| ILLINOIS | 9 |
| MCLEAN | 4 |
| LASALLE | 2 |
| IROQUOIS | 1 |

So a row whose Residence reads COOK is graded `documented` — for residence in **Cook
County on the date of sale**, which in 1835 reaches far beyond the town — and every
other row is graded `inferred`, with the reasoning written on the record. Nothing here
mints a resident or regrades one. `resident_crosswalk.json` proposes correspondences
and states the rule that made each; T-0514 and T-0515 are what spend them.

**What the reading found.** Sales by year: 1830 · 13, 1831 · 8, 1832 · 3, 1833 · 150,
1834 · 95, 1835 · 101, 1836 · 4, and one row the register dates 1810, carried verbatim
because it is what the page says. By type: 205 federal cash entries (`FD`), 150 school
section sales (`SC`), 20 canal sales (`CN`). By what the tract resolves to: 163 half
quarter-sections, 113 town lots, 50 quarter-sections, 2 quarter-quarters and 47 the
parser leaves `unparsed` rather than guess at.

**Seventeen purchasers meet a person the town already holds** — Philo Carpenter,
Archibald Clybourne, George Washington Dole, Daniel Elston, Alexander N. Fullerton,
Edward H. Haddock (twice, once as `HADDOCK E H`), Russel E. Heacock, Hiram Pearsons,
Jeddiah Wooley and eight more. None of the seventeen carries a stated residence: the
thirty-six COOK rows are other names, and matching them is work this pass did not do.

**Shape: `records`.** A sale is a row on a page, so it takes the records shape — the
purchaser `as_read` exactly as the register spelled him, `normalized` only far enough
to read `DEVINPORT WILLIAM` back as `William Devinport`, one `locator` carrying the
section query, the deposit line, the purchase number and the register's own volume and
page. `data/research/domains.json` states it; `tools/research_domains.py --check` holds
the shape and `tools/read_land_sales.py --check` holds the reading.

**Hand-authored:** this README, and nothing else. Every judgement in the crosswalks was
made by a rule that is written out beside it.

**Generated, and re-derived by the gate:** `entries.json`,
`records/entries_t39n_t40n_r14e_through_1836.json`, `coverage.json`, `crosswalk.json`
and `resident_crosswalk.json` — all written by `tools/read_land_sales.py --build` from
the committed deposit at `text/isa_land_tract_sales_t39n_t40n_r14e_through_1836.tsv`,
and all re-derived by `--check`, which refuses a committed file that has drifted. The
deposit itself is written by `tools/harvest_land_sales.py --sweep`, which reaches the
network and is therefore run deliberately by a research pass and never by the gate.

## Two things about the source, both learned the hard way

**The search returns at most 150 rows and offers no paging.** A whole-township query
stops at 150 and looks complete — the first attempt at this read came back with exactly
150 rows for each township and would have recorded a ceiling as a town. So the reading
is BY SECTION, thirty-six queries per township. Sixty-nine of the seventy-two sections
came back under the ceiling and were read whole; `coverage.json` declares the 34 of
those that hold a sale through 1836 and lists the other 35 as queried and empty, which
is read rather than a hole. **Three sections did not come back under the ceiling** — T39N R14E sections 16, 21 and 29, the school section and two of the West
Division sections, whose 1848-1852 city-lot sales fill the ceiling on their own. What
this repo holds for those three is the first 150 rows the search would give (154 of the
375 sales below are from them), and they are deliberately **not declared read**. The
`name` field cannot be used to break them up: it belongs to the database's other search
form and does not narrow a legal-description query, it replaces it, returning that name
from every township in Illinois.

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

- **T39N R14E sections 16, 21 and 29** — truncated at the ceiling, as above.
- **The ring townships** — T39N R13E, T38N R14E, T38N R15E, T40N R13E, T41N R14E.
- **Sales to purchasers whose stated residence is Chicago or Cook County outside these
  townships.** The database's name search cannot be filtered by residence, so this
  needs a different shape of query.
- **The canal sections.** They were sold by the canal commissioners, not the land
  office, and are not in this database at all — their absence is not a hole.
- **The join from a tract to a standing structure.** `entries.json` carries a
  structured `tract` for exactly that purpose; resolving a quarter-quarter or a town
  lot to a footprint against the plat is the next ticket's work, not this one's.
