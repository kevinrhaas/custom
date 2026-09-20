# How a Chicago house of trade signed itself in 1835

**T-1184.** The style guide every reconstructed business in this project is named by,
written from the **196 firm styles the newspaper register prints** — the whole of what the
*Chicago American* and the *Chicago Democrat* put in front of readers between 1833 and
August 1835. It is a reading of that corpus and nothing else: no form appears below that the
register does not carry, and the attested house that carries it is named beside it so the
form can be checked against a printing.

`tools/reconstruct_businesses_1835.py` is the executable half. Its `STYLES` table holds the
forms and goods lines this page argues for, each with the printing it comes from, and the
build refuses a style the register already prints (§ *What an invention may not do*).

## The six forms the register prints

**1 · The sole trader, initials and surname.** The commonest signature in the corpus, and
the one a reconstructed sole trader takes: an initial or two, a surname, a comma, and the
trade or the goods.

> *B. Jones, grocery and provision store* · *J. C. Goodhue, land agent* ·
> *L. W. Montgomery, boot and shoe maker* · *S. B. Cobb, saddle, harness and trunk
> manufactory* · *R. Stewart, attorney* · *J. Bates jr., Auction Store*

The initials are the point. Of the eighty-odd single-keeper houses the register holds, far
more print `J. Curtiss` than `John Curtiss`, and a great many print nothing but the
initials and the surname — *A. Garrett*, *S. Foot*, *S. Dewey*, *W. Reed*, *P. F. Peck*,
*A. O. T. Breed*. The forename in full is the minority form and is also attested:
*Frederick Thomas, drugs and paints*, *William F. Lyon, Wholesale Grocery Store*,
*Philo Carpenter*, *Russell E. Heacock*, *Hiram Pearsons*.

**2 · The partnership, two surnames and an ampersand.** Two names, `&` between them, and
nothing else. Twenty-two of the thirty-six distinct firm styles the register carries are of
this shape.

> *Newberry & Dole* · *Jones & King* · *Pierce & French* · *Kinzie & Forsyth* ·
> *Goss & Cobb* · *Russell & Clift* · *Briggs & Humphrey* · *Magie & Wilkinson* ·
> *Dally & Youngs* · *Kercheval & Hamilton* · *Taylor & Handy* · *Tuttle & Brown*

Two brothers or a father and son sign with shared surname and split initials —
*C. & I. Harmon*, *G. W. & W. Laird*. A house that spells out **and** rather than `&` is
attested once — *Cooley and Halsman* — and is the rarer form.

**3 · The house with a silent partner: `& Co.`** A named principal, or two, with the rest
of the firm behind an abbreviation.

> *P. Pruyne & Co.* · *Hubbard & Co.* · *H. Doty & Co.* · *J. L. Wilson & Co.* ·
> *Wm. Hogue & Co.* · *Thos. Emerson & Co.* · *Matthias Mason & Co.* ·
> *Clark, Filer & Co.* · *Harmon, Loomis & Co.* · *Jones, King & Co.* ·
> *Cromelien, Brothers & Co.*

Three names take commas and the ampersand falls before the last: *Clark, Filer & Co.*
This is also where the register's abbreviated forenames live — *Wm.*, *Thos.*, *Jno.*,
*Geo.* — and `Jno. L. Wilson & Co.` and `J. L. Wilson & Co.` are the same house in two
printings.

**4 · The named house.** A sign rather than a surname: a bird, a city, a virtue, or the
town itself.

> *Eagle Tavern* · *Eagle Hotel* · *New York Clothing Store* · *The Boston Market* ·
> *Chicago Bakery* · *The Chicago Brewery* · *the Chicago Academy* · *the Traveller's
> Home* · *the Man Trap* · *W. Kimball's New Store* · *the Livery Stable at the Point*

**5 · The keeper's possessive.** The house named by whoever keeps it, with the trade after.

> *A. Clybourn's market on the market square* · *E. Wentworth's tavern on Flag Creek* ·
> *Stuart's confectionary and perfumery* · *Ingersoll's tavern stand* ·
> *Miss Bayne's Boarding and Day School* · *Peter Cohen's store*

**6 · The professional's full title.** The learned trades print the office rather than the
goods, at length, and capitalised.

> *Henry Moore, Attorney & Counsellor at Law* · *J. D. Caton, attorney and counsellor at
> law* · *Wm. H. Kennicott, Surgeon Dentist* · *L. G. Curtiss, Deputy Surveyor of Cook
> County* · *Charles Hunt, High School for Young Ladies* · *Dr. J. H. Barnard*

## The goods line

A trade line in this corpus is the advertiser's own idiom and it is a LIST, in the order
the house wanted them read:

> *drugs, paints, chemicals, perfumery and dye stuffs* (Frederick Thomas) ·
> *drugs and medicines* (Philo Carpenter) · *wholesale and retail store — groceries,
> hardware, crockery and drugs* (P. Pruyne & Co.) · *Boot, Shoe & Leather Store*
> (Wm. H. Taylor) · *Tin, Sheet Iron and Copper Factory* (J. K. Botsford) ·
> *storage, forwarding and commission merchant* (Wm. Sabine)

Capitalisation is inconsistent in the papers themselves and is not regularised here. Where
a reconstruction needs a goods line it takes one the register prints for that class,
never one composed for it.

## What an invention may not do

- **It may not reuse an attested style.** A reconstructed house may not trade under a name
  or a firm style the register already prints, and may not carry the name of a real
  proprietor. `reconstruct_businesses_1835.py --check` refuses each, over the whole
  register, and `--self-test` fires both.
- **It may not use an anachronism.** No *Inc.*, no *Ltd.*, no *Company* spelled out, no
  brand word, no trademark, no ampersand-free corporate style. The register has none, and
  the general incorporation acts that would license them are decades away.
- **It may not invent a surname.** Surnames come from
  `data/reconstruction/1835_invented_name_pools.json` by the proprietor's community, and in
  practice a reconstructed house does not draw one at all: it **adopts** a reconstructed
  trade head the resident band already drew, so the surname on the sign is the surname on a
  card that was checked against every real name in the town when it was written.
- **It may not be more specific than its evidence.** The house's name is a reconstruction
  and the record says so on every field; nothing about a style is ever graded above
  `reconstructed`, and no reconstructed house cites a source.

## Worked: the two druggists of 1835

The December 1835 State census prints **four druggists**; the register holds **two** at the
scene date — Philo Carpenter and Frederick Thomas. The order book therefore orders two, and
the resident band had already drawn exactly two reconstructed heads at the trade. They sign
by form 1, on goods lines both attested druggists advertise:

| | reconstructed house | adopted keeper | face |
|---|---|---|---|
| south | *B. Crandall, drugs, medicines and dye stuffs* | `rc_crandall_benjamin` | Dearborn Street |
| north | *Nathaniel Metcalf, drugs, medicines and dye stuffs* | `rc_metcalf_nathaniel` | Kinzie Street |

Both forms of the sole trader's signature are in the table, and the seed decides which each
house takes — which is why one prints an initial and one a forename. The face is a
`street_only` limit, not a premises: no lot, no roof, no coordinate. See
**docs/LIBERTIES.md § L254**.

## Worked: the four boarding houses of 1835, and the honorific that is not dealt

A boarding house signs by **form 5, the keeper's possessive**, and by nothing else. It is
the form this town's own lodging houses take — *Miss Bayne's Boarding and Day School* in
the register, *Rufus Brown's Boarding House* on the one boarding house the structure layer
names — and the seed deals between the possessive in full and the possessive with the
forename cut, exactly as *Ingersoll's tavern stand* and *Stuart's confectionary and
perfumery* print it.

| | reconstructed house | adopted keeper | seat |
|---|---|---|---|
| north | *Bardwell's boarding house* | `rc_bardwell_esther` | `recon_1835_north_h1_007` |
| north | *Newell's boarding house* | `rc_newell_lydia` | `recon_1835_north_h2_030` |
| north | *Ellen Cavanagh's boarding house* | `rc_cavanagh_ellen` | `recon_1835_north_h3_045` |
| west | *Martin Fitzgerald's boarding house* | `rc_fitzgerald_martin` | `recon_1835_west_006` |

Two things are different here from the druggists above, and both follow from the same fact:
**the building came first**. The seat is a `premises` and not a street face, because the
roof is what bought the house — the census enumerates taverns and never boarding houses, so
no shortfall of this class can be counted and there is no order-book row to spend. And the
keeper is adopted from the **lodgers** stage rather than from the trade heads: T-1371 drew
these four as the keepers of roofs it was putting people into, and their cards already read
`boarding_house_keeper`.

**No honorific is dealt, ever.** Three of the four keepers are women, and the register
prints both *Mrs. H. Sherman* and *Miss Bayne's* — so the form is available and attested.
It is refused anyway, because both forms assert a marital status and these cards carry
none: the stage minted them as solitary keepers and nothing in the layer says whether they
were married, widowed or single. A sign reading *Mrs. Bardwell's* would be inventing a
husband to make a shopfront read well. The possessive stands on the name alone, which
asserts only what the card holds. See **docs/LIBERTIES.md § L257**.

---

Related: the order book **docs/RESEARCH/1835_reconstruction_order_book.md**, the trade heads
**docs/RESEARCH/1835_trade_households.md**, the lodging model
**data/reconstruction/1835_lodging_model.json**, the business layer
**docs/RESEARCH/business-layer.md**, tickets **T-1184**, **T-1408**, **T-1173**, **T-1166**.
