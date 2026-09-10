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
| GARRETT A ET CO | *retired* | refused by hand as a **firm**, and the refusal is now a derivation — see below |

Refusing the firm spelling left `GARRETT AUGUSTUS` standing alone on A. Garrett's card, where
the two spellings had both been written onto it. That second spelling is a reading in its own
name and is NOT ruled on here — it is one of T-0850's twenty-six, which the next section rules on (refused: the town has never read the forename).

## The register sells ground to FIRMS (T-0851)

A purchaser is not always a man. Twice on these 953 rows the register sets a partnership
style after the name — `GARRETT A ET CO`, eighty acres of section 33 in T38N R14E entered on
1 December 1835, and `PRUYNE P AND CO`, block 97 of the school section on 22 October 1833 —
and both of them were being read as people:

* `tools/namesake.py` drops the firm words so it can ask which man of a surname a reading
  points at. That is the right thing for that question and the wrong answer to a different
  one: `GARRETT A ET CO` folded to `A`, `A` named the town's A. Garrett, and a **house's**
  purchase was proposed as a **man's**.
* `PRUYNE P AND CO` was never refused at all. Peter Pruyne's card said the register enters
  *this person* six times, one of them as the firm, and counted the firm's 3.27 acres and
  $310 among his own. It now says five, 167.83 acres and $403.79.
* `normalize_name` read the firm words as forenames and title-cased them, so the deposit's
  own `normalized` field said **`A Et Co Garrett`** — a name of nothing.

**The rule, and it reads the page rather than a list.** `namesake.firm_style()` recognises a
partnership by the conjunction the register prints before its abbreviation for company —
`ET CO`, `AND CO`, `& CO`. The capacity words deliberately are NOT styles: `AS`, `AGENT`,
`TRUSTEE`, `HEIRS`, `OF`. A man buying as an agent or an heir is still a man and the register
names him; `BLANCHARD F G AS`, `VANDERBOGERT JOHN AS` and `WILLIAMS GILES AS` are people.

**Where the ground goes.** Every firm is refused against every person in `refusals[]` — the
count of adjudicated spellings stays whole — and the reading of it is carried in a new
`firm_purchasers[]` block of `resident_crosswalk.json`: what the house bought, when, where,
for how much, the register's Residence column, and the **one partner the page names**, put to
the same forename rule and carried at the same grade it would have earned. That proposal is
about the PARTNER'S NAME and not about a purchase by him. Who else stood in the house is not
on the page and nothing here proposes them.

The identification of `A. Garrett & Co.` with the town's A. Garrett — an auctioneer in four
numbers of the *American* and the *Democrat* — is probably right and is not what is refused.
What is refused is spending a partnership's entry as a person's.

`KNOWN_FIRMS` in `tools/read_land_sales.py` declares the two spellings, and `--check` **fails
on a firm the reading finds that is not declared**: a new deposit carrying one is meant to
stop the build, so somebody reads the rows before a purchaser goes onto no card at all.

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

**A duplicate card found on the way past — and ruled (T-0993).** Fergus 1843's *Francis
Gurtrey* is one man, and the layer held both `blanchard_f_gantry` and `blanchard_gantry`.
T-0993 folded them, under a card-merge rule written for the shape, and named the six
`BLANCHARD GURTREY` rows onto the survivor. The section below is that ruling.

## The ruling the layer could not make: `named` (T-0993)

`upheld` and `refused` can only ADJUDICATE a proposal the mechanical rule made — confirm it,
or take it away. So a reading the rule structurally cannot reach had no way to be ruled on at
all, and `check_rulings` called a ruling on it *"a ruling on nothing"*.

**BLANCHARD GURTREY is that reading.** `namesake.choose` weighs the FIRST forename token, and
the register printed Francis Gurtrey Blanchard's MIDDLE name in the forename's place. Six
school-section rows — ls0076-ls0081, $547.00 of town lots on blocks 2, 3, 21, 82 and 141 —
were refused against every Blanchard the town holds, and no reading of any page could have
changed that.

**What names him.** Fergus 1843 prints *"Blanchard, Francis Gurtrey, capitalist, res 45
Wells"*, so GURTREY is his middle name and the card carries it as *Gantry* from the poll of
1834. And the register proves its own habit at ONE sale: the same school section — sec 16
T39N R14E, type SC, 22 and 24 October 1833 — is entered *BLANCHARD F G* in volume 818 page
010 (0376893-0376895) and *BLANCHARD GURTREY* in volume 817 page 027 (0367525-0367530). That
is the HUNTER E E / HUNTER EDWARD E habit above, one column further along the name.

**The kind, and its guards.** `ruling: "named"` GIVES a match instead of taking one away, and
`read_land_sales.py` holds it to the mirror of the same rules: only where the surname gathered
rivals and the forename failed to choose among them; only onto one of those rivals; never onto
a surname-only purchaser, which this domain refuses however well the tract agrees; and the
same reasoning, ticket and `checked_against` every other ruling owes. A `named_by_ruling`
match carries the refusal it overturned in `was_refused_as`, and it is the one match kept out
of the `namesake.collide` group — that rule asks whether several readings the MECHANICAL rule
named onto one person are one man, with the same forename test a `named` ruling exists because
it failed, and letting it run would have taken the three upheld F G rows down with the sixth.
Four assertions in `--self-test` hold all of it.

**What moved:** matched spellings 123 → **124**, ruled 49 → **50** (33 upheld, 1 named, 16
refused), and $547.00 of town ground reached the card it belongs on — $373.00 → **$920.00**
across ten rows.

**Still unruled: 90.** Cohort B is the twenty-four with no namesake at all (`rivals[]` empty),
cohort C the sixty-six remaining `forename_agrees` proposals that have one; the log on T-0990
carries them. The live count is on the crosswalk's `ruled` block and not repeated here.

## Cohort B: the twenty-four with no namesake at all (T-0990)

The mechanical rule fired on a surname the residents layer holds EXACTLY ONCE, which is
T-0700's and T-0850's original shape — `rivals[]` empty, no namesake for a forename to choose
among. That makes the proposals look safer than they are: holding one bearer of a surname is a
fact about how thin the layer is, and the register itself sells to a second Hurd and to three
Robertses while the town holds one of each.

**Twelve upheld, twelve refused** — the cohort splits exactly in half, and it splits along one
line. What moved: matched spellings 123 → **111**, ruled 49 → **71**, unruled 90 → **66**;
twelve cards retracted, and with them sixteen register rows — **1,549.24 acres and $2,084.04**
of ground taken back off them. Nothing was written on: upholding a proposal confirms what the
spend pass had already put there.

**THE LINE IS WHETHER THE TOWN HOLDS THE MAN MORE THAN ONCE.** Every one of the twelve upholds
has a second document on the town's side, and eleven of the twelve refusals have exactly one
name-only reading and nothing else. Cohort A's discriminator held again — nine of the twelve
upholds are decided by a directory printing the forename whole where the card carries an
initial:

| the register | the town's own printing | ruling |
|---|---|---|
| BOTSFORD JABEZ K | Fergus 1839: *Botsford, Jabez K., Botsford & Beers* | upheld |
| BOYER JOHN K | Fergus 1839: *Boyer, John K., coroner* | upheld |
| GOODHUE JOSIAH C | Fergus 1839: *Goodhue, Dr. Josiah C.* | upheld |
| KIMBALL WALTER | Fergus 1839: *Kimball, Walter, probate judge* | upheld |
| KNICKERBACKER ABRM V | Norris 1844: *Knickerbacker, A. V., grocery and provisions* | upheld |
| PECK P F W | Fergus 1843: *Peck, Philip Ferdinand Wheeler* | upheld |
| SHRIGLEY JOHN | Fergus 1839: *Shrigley, John, tavern keeper* | upheld |
| MARSH SYLVESTER | Fergus 1843: *Marsh, Sylvester, packing-house* | upheld |
| DOLE GEORGE W | Fergus 1843: *Dole, George Washington* | upheld |
| STANLEY JOSEPH | *nothing* — one line of the 1833 tax list | **refused** |
| BLAISDELL BENJAMIN | *nothing* — one line of the poll of 1835 | **refused** |
| SHEPHERD ALBERT · SACKETT JOSHUA · CHIPMAN ANSEL · ALLISON THOMAS · OSTRANDER CATHRINE · ROWLEY HEMAN A | *nothing* — one uncalled-for letter apiece | **refused** |

Six of the twelve refusals are cards the residents layer itself marks `letter_list_only`, which
turns out to be the SPENCER WILLIAM G test written as a field: the household around such a
person was minted to claim nothing, and an uncalled-for letter plus a tract entry is two
name-only readings.

**A MIDDLE INITIAL DISCRIMINATES; IT DOES NOT CORROBORATE — and this cohort is where that had
to be said.** Three proposals agree on a middle initial the register repeats, which the ruling
rule names as its first limb, and they do not all go the same way. **JAMISON LOUIS T** is
upheld: the town prints *L. T. Jamison* twice and independently, in the Democrat of 4 June 1834
and on the poll of 1835, so the initial pair decides among readings the town already holds.
**ROWLEY HEMAN A** and **HURD NIRAM F** are refused: there the initial pair IS the town's whole
record — one uncalled-for letter, one press line — and a fuller reading of one name beside a
shorter reading of the same name is still one name on each side. That is the NEWBERRY WALTER L
check of T-0700 read carefully: the L decided there because the American of 1835 and both Fergus
directories had already put the man in the town.

**The Residence column was weighed twice and carried neither.** CHIPMAN ANSEL and ALLISON
THOMAS both have **COOK** on the register's side, the strongest thing this source ever offers
and what upheld DILL FRANK and LUDBY JOHN. In those two the town's side was a poll list and a
newspaper naming the man in the town between his entries; here it is a letter nobody called
for. A COOK row and an uncalled-for letter agree about a county, not about a man.

**Two refusals turn on a token the register adds and the town cannot answer.** WILCOX DE LA
FAYETTE reduces as distinctive a forename as the cohort contains to the initial D — the town's
whole record is *Capt. D. Wilcox*, one press line, and the register's social-status column is
blank, so the captaincy checks against nothing. And **CHURCH THOS JR**: the JR is the page
saying there was another Thomas Church of the same county. The town holds one, its card is
written — in its own words — almost entirely to keep a building from being anonymous, and its
`present_on_scene_date` says nothing places him in the town on any particular date. That the
identification is probably right is not what is refused.

**A duplicate card found on the way past, and the reason the crosswalk could not see it.**
KIMBERLEY EDMUND S is upheld against `kimberley_ed` — the card's own press reading is *E. S.
Kimberley*, the Democrat of 1 July 1835, and the 1840 census reads *Ed. Kimberley*, so the S is
on the town's side and two documents bracket the scene date. But the layer ALSO holds
`kimberly_edmund_s`, **Dr Edmund Stoughton Kimberly**, printed *Kimberly, Dr. Edmund S.* in
Fergus 1839 — the same forename and the same middle initial, spelled with one letter fewer.
`tools/namesake.py` folds surnames exactly, so it never gathered him: **`rivals[] empty` means
no namesake OF THAT SPELLING, and this cohort is defined by that field.** Filed as **T-1001**.

**Still unruled after cohort B: 66** — cohort C, the `forename_agrees` proposals that have a
namesake, taken in three runs by surname block. The log on T-0990 carries them.

## Cohort C1: the seventeen with a namesake, surnames A-C (T-0990)

Cohort C is the other half of what T-0697 added: the mechanical rule fired on a surname the
layer holds SEVERAL of, and a forename agreeing in full chose among them. C1 is its first
block, surnames A to C, ruled by eye as well as by `namesake.py`.

**Eleven upheld, six refused.** What moved: matched spellings 112 → **106**, ruled 71 → **88**,
unruled 66 → **49**; five cards retracted, and with them nine register rows — **1,040.00 acres
and $1,608.00** of ground taken back off them. What stands: 23 rows, 1,125.71 acres and
$2,943.00. Nothing was written on; upholding a proposal confirms what the spend pass had
already put there.

| the register | the town's own record | ruling |
|---|---|---|
| ARCHER WILLIAM B | Chicago American, 4 July 1835, *William B. Archer*, + a Fergus death notice | upheld |
| BEAUBIEN MARK | the election of 1833 held at his house; Fergus 1839 *hotel-keeper, Lake st* | upheld |
| BROWN WILLIAM H | Democrat, 28 May 1834, *W. H. Brown*; Fergus 1839 *cashier, Branch State Bank*; the register's own **ILLINOIS** | upheld |
| CARPENTER PHILO | Fergus 1839 *druggist and apothecary*; by 1843 he has **Carpenter's Addition** | upheld |
| CHAPMAN CHARLES H | three ordinary press printings, 1833-34; Fergus 1839 *real estate dealer* | upheld |
| CLARK JOHN K | Chicago American, 11 July 1835, *John K. Clark*; the register's own **COOK** | upheld |
| COOK JOSIAH P | Norris 1844: *Cook, Josiah P. baker, res Michigan avenue* | upheld |
| COOK THOMAS | *teamster, Desplaines st* in 1839, 1843 AND 1844, + the tax list of 1833 | upheld |
| ANDREWS WILLIAM | Democrat, 25 June 1834, *Wm. Andrews*; Fergus 1839 *tailor, north side* | upheld |
| BOWEN ERASTUS | tax 1833, poll 1834, Calumet Club, Fergus 1839 *city collector* | upheld |
| BENNETT WILLIAM | the poll of 1834, + the register's own **COOK** | upheld |
| BROWN WM | *nothing the fuller spelling does not already carry* — and Fergus 1843 prints three William Browns | **refused** |
| ANDREWS DAVID · ALLEN WILLIAM · BLAKE LEVI · BURDICK PAUL | *nothing* — one uncalled-for letter apiece | **refused** |
| BALLARD THOMAS | *nothing* — one line of the poll of 1835 | **refused** |

**THE HABIT COHORT A FOUND HAS A LIMIT, AND C1 IS WHERE IT SHOWS.** The register does print one
purchaser twice, abbreviated and in full — HADDOCK E H / HADDOCK EDWARD H was cohort A's. But
**BROWN WILLIAM H is upheld and BROWN WM is refused**, on the same day and against the same
card. The fuller spelling carries a middle initial, a bank, two press readings and an ILLINOIS
in the Residence column; the barer one carries a forename so common that Fergus 1843 prints
*Brown, William, grocer*, *Brown, Wm., bds Sauganash* and *Brown, William Hubbard, cashier* as
three men. The layer holding one William Brown is thinness, not a town. **A spelling with no
middle initial is its own proposal and gets its own ruling.**

**THE SIBLING TEST IS THE CHEAPEST ONE IN THE COHORT.** ANDREWS WILLIAM upheld, ANDREWS DAVID
refused, same surname and same afternoon: one has a newspaper printing and a directory trade,
the other has a letter waiting at the post office and a research row whose `evidence_for` is
EMPTY. A `corroborated_enrichment` outcome with nothing written into it corroborates nothing.

**AND `letter_list_only` LIED ONCE.** Four of the six refusals are cards carrying that flag and
they went the way cohort B's six went. CHAPMAN CHARLES H carries it too and is UPHELD, because
three of its four `press_evidence` rows are ordinary printings with their own locators — the
Democrat of 26 November 1833, the American of 24 December 1833, the Democrat of 13 August 1834 —
and only one is a letter list. Read `press_evidence[].list`, not the flag. Seven cards are
flagged that way; filed as **T-1005**.

**A second card found on the way past.** Fergus 1843 prints two Erastus Bowens — the city
collector of *B. & Cole*, and *Erastus Selden Bowen [veterinary surgeon] [died Oct. 19, 1888,
a. 69]*, who was born about 1819 and was sixteen on the scene date. The layer's single card is
keyed `bowen_erastus_selden` and appears to hold the elder man's documents under the younger
man's name. The ruling is against the elder and says so; the conflation is **T-1004**.

**Still unruled: 49** — cohort C2 (surnames D-J, 21 spellings) and C3 (K-Z, 28). The log on
T-0990 carries them, and C3 holds KIMBERLY EDMUND S, which is T-1001's man.

## Forty rulings were reverted, and restored (#1073, T-1000)

**For part of 10 September 2026 this file's rulings block held eight entries and its own
prose described forty-eight.** The merge lap pushed onto #1055 — T-0851, the firm rule —
and `resident_rulings.json` conflicted there. It is hand-authored, and the lap's regex
resolution took the branch's whole block for the second conflict; that branch had been
cut before T-0850 and T-0990 cohort A ruled, so all twenty-six of T-0850's rulings and
all fourteen of cohort A's left the file on one line. #1055's own prose survived, and
went on describing the cohort A rulings the same commit had removed. **A file that
describes forty judgements it does not contain** is what the next run noticed, reading
T-0990's cohort log for the remaining count and finding the crosswalk disagreed with it.

| | before | reverted | restored |
|---|---|---|---|
| entries in `resident_rulings.json` | 49 | 8 + 1 retired | **47** + 2 retired |
| crosswalk `ruled.upheld` | 33 | 6 | **33** |
| crosswalk `ruled.refused` | 16 | 2 | **14** |
| crosswalk `ruled.unruled` | 90 | 129 | **90** |
| matched spellings | 123 | 135 | **123** |

**The loss was not inert, which is the thing to take from this.** A refusal RETRACTS the
paragraph `spend_land_sales.py` wrote, so refusals going missing put the purchases back
onto the cards that had adjudicated them away — Thomas Hartzell, Henry Vanderbogert,
Charles Wessencraft, John Hale, James Spence, Joseph Chandler, Paul Kingston, Ira Minard,
Augustus Garrett, Chauncey Goodrich, Liman Smith and Thos M. Morrison — twelve cards,
each carrying a federal land entry and an `isa_public_domain_land_tract_sales` source
line it had been ruled it could not have. Restoring the rulings and re-running the spend
takes them back off: **twelve records retracted, nothing written on**, and matched
spellings back down 135 → 123, a refusal being what removes a match.

**Every entry is restored as its own ticket wrote it** — the same `ruled_on`, `ticket`,
`checked_against` and reasoning — because a judgement re-argued is a different judgement.
**One is retired rather than kept.** `PRUYNE P AND CO` was T-0850's, refused for being a
partnership; T-0851 then made that a DERIVATION — `namesake.py`'s `firm_style()` refuses
every firm against every person before a surname is gathered — so the crosswalk proposes
nothing for the spelling and `--check` rightly calls a hand ruling on it a ruling on
nothing. #1055 retired its twin `GARRETT A ET CO` in exactly this way, and that
retirement note **names this spelling** as the second firm the rule caught; it could not
retire the entry because its base did not hold it. So the retirement is finished under
T-0851's date and ticket, with the argument kept rather than deleted: it is half of what
the rule was written from.

**Nothing in the gate could see it, and that is still true.** `read_land_sales.py
--check` asserts a ruling is WELL FORMED — that it names a spelling the register holds
and a person the proposal named. It has no opinion about a ruling that is simply GONE,
because a smaller rulings file is a legal rulings file, and the eight-ruling file
re-derived perfectly into a crosswalk perfectly consistent with it. `check.sh` was green
on #1055 and on every commit after it. The count is the only thing that can be watched
here and nothing watches it; T-0999 is that gate.

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
