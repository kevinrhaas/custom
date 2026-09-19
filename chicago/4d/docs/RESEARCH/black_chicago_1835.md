# Free Black Chicago, 1 July 1835

**T-1377, of T-1177. Written beside `tools/reconstruct_black_chicago_1835.py`, which mints
the cohort, and `data/reconstruction/1835_black_chicago.json`, which is its ledger.**

Until this ticket the reconstruction held not one free Black resident. It held one sentence
about them, in a white lawyer's card, and a count printed five years after the scene. This
page is everything this corpus says, what was minted out of it, and what was refused.

---

## 1. Every attested trace, in full

### 1.1 The certificates of freedom, August 1833 — the floor

`data/residents/households/hh_caton_john_dean.json` carries this, of John Dean Caton, in the
town's first law office:

> In August 1833 he defended six or seven free coloured men before the Court of County
> Commissioners and obtained certificates of freedom for them, his fee a dollar from each.

That is a dated proceeding of a court of record, two years before the scene date. What it
carries: **six or seven free Black men were living at Chicago in August 1833**, and each of
them had to prove his freedom to a court to stay. What it does not carry: a name, a
household, a trade, a street, or a word about what became of them. It is a count, and the
count is this cohort's floor. This project takes the lower of a source's own pair, so the
floor is **six**.

### 1.2 The Black-headed households of 1840 — the composition stock, and the name pool's seed

Sixty-three sheets of the 1840 Cook County enumeration are read into
`data/research/census_1840/pages/`. Seven of their households carry a mark in the free
coloured columns — twenty-one persons in all — and the reading is this:

| printed page | line | head as read | free coloured | free white | reads as |
|---|---|---|---|---|---|
| 210 | 10 | [?]. S. Sherman | 1 | 9 | one person in a white-headed household |
| 215 | 5 | Geo. Seyman[?] | 1 | 9 | one person in a white-headed household |
| 215 | 29 | John Johnson | 6 | 0 | **a Black-headed household** |
| 216 | 8 | Eliza As[?]ie | 4 | 0 | **a Black-headed household, headed by a woman** |
| 219 | 25 | Oliver Henson | 2 | 0 | **a Black-headed household** |
| 221 | 12 | George White | 6 | 0 | **a Black-headed household** |
| 239 | 15 | Sherman W. Parr | 1 | 4 | one person in a white-headed household |

Four Black-headed households, eighteen people; three people living in white households.
Two of the four are headed by a woman. Their band vectors are the only measured structure of
a Black household in this place that this corpus holds, and they are used here as **shape and
nothing else** — no name, no individual's age, no industry mark and no identity crosses from
1840 into 1835. These people lived five years after the scene; a source that names a person
may never be spent on somebody drawn.

### 1.3 The industry column, printed page 219 — the one occupational fact

The continuation sheet `33S7-9YYJ-24` is paired to printed page 219 by T-0642, on two
independent keys, and it marks **line 25 — the Henson household — in MANUFACTURES AND
TRADES**. Not in agriculture, not in commerce, and not in the learned professions: a
mechanic's or a craftsman's household.

It is reachable for exactly **one of the four**; the other three sit on left sheets whose
continuations are unpaired. One residual is recorded and not resolved here: the left sheet's
own cells sum to 2 persons on that line against the continuation's TOTAL column of 3, one of
nine such disagreements on a sheet where twenty-two of thirty-one lines agree exactly. The
page file carries the residual.

Nothing of this is carried into a drawn household. It is used for one thing: **it is why the
trade deal below may not be all-service.** The single occupational fact this corpus holds
about a Black-headed Chicago household puts it in a trade, and a reconstruction that dealt
this cohort nothing but domestic work would be contradicting the only evidence it has.

### 1.4 The count of 1840 — the ceiling's numerator

`data/research/census_1840/composition_1840.json`, derived from the full-count extract:
**53 free coloured persons at Chicago on 1 June 1840**, in 964 households, in the twelve
bands the file prints — 34 male, 19 female, sixteen of the men in the 24-to-36 band.

---

## 2. The bracket

| | persons | what it is |
|---|---|---|
| **Floor** | 6 | Caton's six, certificated free before the county court in August 1833. Attested as a count, unnamed as people. |
| **Ceiling** | 28 | The 53 of 1840, scaled back to the scene by the town model's population point for 1 July 1835 (2,536), at the lower of the two available 1840 denominators. |

The two scalings, both printed in the ledger:

- against the extract's 4,834 enumerated persons — 1.10% — **27.8 persons in 1835**
- against the census's own city population of 4,470 — 1.19% — **30.1 persons in 1835**

The ceiling takes the lower and rounds: **28**. The scaling is this ticket's one invented
step, and it is named as one. A town that grew from about 2,500 to about 4,500 in five years
did not grow uniformly across its communities, and nothing in this corpus says how the free
Black share moved. The ceiling is a ceiling.

---

## 3. What was minted

**Six households, twenty-eight people, one firm** — and 28 is the ceiling exactly. That is
not a figure chosen to fill the bracket. The deal takes one household for each of the floor's
six men, deals the four composition vectors to them in the sheets' own printed order, cycled,
and stops the moment the ceiling would be passed; 6 + 4 + 2 + 6 + 6 + 4 comes to 28 by
coincidence of the stock. It is worth stating plainly what a mint on its own ceiling means:
**the model has no room left for a free Black Chicagoan this cohort has not counted**, so a
reading that finds a real one retires a drawn household rather than joining it.

| household | persons | head's trade | vector from |
|---|---|---|---|
| `hh_fb_whitman_chauncey` | 6 | boarding house keeper | p215 l29 |
| `hh_fb_haines_susan` | 4 | laundress | p216 l8 |
| `hh_fb_mccloud_lydia` | 2 | laundress | p219 l25 |
| `hh_fb_magie_samuel` | 6 | labourer | p221 l12 |
| `hh_fb_brand_luther` | 6 | labourer | p215 l29 |
| `hh_fb_mchale_hannah` | 4 | laundress | p216 l8 |

The dealt composition seats **six adult men**, which is exactly what the certificates
counted: the floor is met by the draw rather than forced onto it. Three of the six
households are headed by a woman, which the 1840 stock is where it comes from.

Every person is graded `reconstructed`, carries `community: free_black`, carries
`review_required` with the review named, and carries the seed that redraws them and the
reading that retires them. The households are `unplaced`: nothing in this corpus says where
Chicago's free Black residents lived in 1835, and T-1199 seats them when the placement policy
is written.

### 3.1 The names

**Heads are named; nobody else is.**

The pool's seed is section 1.2: four Black-headed households of 1840 bearing ordinary
Anglo-American names — White, Henson, Johnson; George, Oliver, John, Eliza. That is the whole
of what this corpus attests about how free Black Chicagoans were named, and it says they were
named as their white neighbours were. So **no separate "Black" name list is invented here and
none is cited**, because inventing one would be a claim about this community's naming that no
source makes and the seed says the opposite.

- **Surnames** come from the 1840 Cook County sheets themselves — the naming of this place in
  this decade, written by its own enumerator — less every reading the page files mark
  `name_confidence: low`, less every surname the 1835 resident layer already carries, and
  less the four Black-headed households' own. That leaves a stock of 136.
- **Forenames** come from the ordinary Anglo-American given names of
  `data/reconstruction/1835_invented_name_pools.json`, by sex.
- No drawn full name may equal a name anywhere in the layer, and no two heads share a
  surname. The subtractions are the point: a drawn head must read as neither the 1840
  family's kin nor a documented white family's.

**Nobody below a head is named.** The 1840 schedule names the head and *counts* everybody
else, so a name for a woman or a child here would invent the person and their relation to the
head in one stroke. They carry a designation, a sex and a band, and the ticket that would name
them.

### 3.2 The trades

The men's table is **labourer and teamster**; the women's is **laundress and domestic**;
one head keeps the boarding house (§3.3). The deal is even, because no source ranks these
employments for this town, and an even deal is the only apportionment that adds no ranking
the record does not carry.

**Four trades T-1177 names are refused rather than smuggled in under a near term.** This
layer's occupation vocabulary has no word for `barber`, `cook`, `whitewasher` or `drayman`:
`barber_surgeon` is a different trade, `domestic` is a household's servant rather than a cook
by trade, no committed source puts a whitewasher in this town at all, and `teamster` is the
vocabulary's own word for a drayman's work. Inventing a term here would put a trade into the
town's census of trades that nothing ordered. **This is a finding for T-1182 and T-1378**: if
the town wants a Black barber's stand, the vocabulary has to carry `barber` first.

### 3.3 The one firm

`data/businesses/authored/rcb_whitman_boarding_house.json` — a boarding house, `provenance:
reconstructed`, `proprietor_community: black`, `review_required`, unplaceable, undated, kept
by `fb_whitman_chauncey`.

The rule that mints it: **a drawn household carrying more than one adult man is a house where
men lodged**, and the largest such household's head keeps it. One, and no more: T-1187 owns
how many boarding houses the town had against the 42-roof programme, and a cohort may not
order more of them than its own evidence carries.

One inconsistency is recorded here rather than fixed: the business schema's
`proprietor_community` enum carries `black` where the resident layer's community vocabulary
carries `free_black`. The record uses the word its own schema accepts and the keeper's card
carries `free_black`, so the join is exact from either side — **reconciling the two
vocabularies is T-1378's**, which owns the field and the filter.

---

## 4. What was refused

- **A name for anybody but a head**, and **a kin tie of any kind** — the schedule of 1840
  records no relationships, so everybody below the head is `household_member` and this stage
  writes no wife, no son and no daughter. The families of this cohort are owed to T-1170 and
  T-1171 exactly as every other household's are.
- **Any identity, age or industry mark carried from 1840 into 1835.**
- **A second boarding house**, and any business the trades do not imply: a laundress, a
  domestic, a labourer and a teamster are employments and not firms.
- **A residence, a division and an arrival year.** One arrival bound is on the record already
  — six men were at Chicago in August 1833 — and T-1169 is where it is spent.
- **"Former slaves" as a fact about anybody.** T-1177 allows it only as a `reconstructed`
  status with the bracket's basis, and this stage writes none: a certificate of freedom is
  evidence that a court demanded proof, not evidence of where a man was born. The Illinois
  registers of free persons of colour would be the reading that settles it, and this corpus
  does not hold them.

---

## 5. What a reading would retire

- **The Illinois registers of negroes and mulattoes** for Cook County, and the county
  commissioners' own record of the August 1833 certificates: those would NAME the six men,
  and a name retires a drawn head outright.
- **The 1835 Illinois State census returns for Cook County**, if they survive with the
  free coloured column: that would replace the scaled ceiling with a count.
- **Any Chicago newspaper notice naming a free Black resident or a Black-owned firm** — the
  register has none today.
- **The unpaired 1840 continuation sheets** for printed pages 215, 216 and 221, which would
  give the other three Black-headed households their industry class and widen §1.3 from one
  fact to four.

Every one of those retires part of this page. That is what the tiers on the cards are for.

---

## 6. The review this cohort is owed

Every person and the firm carry `review_required` and name it: **a reading by Black Chicago
historians or community organisations before this scene is marked released**, as T-1177 asks
of every under-documented cohort it reconstructs. `review_required` already blocks release —
the gate asserts it — so this is not a promise, it is a lock.

**Related:** `docs/LIBERTIES.md` L250 · T-1177 (the parent) · T-1376 (the Native and Métis
cohort) · T-1378 (`proprietor_community` and the Businesses filter) · T-1170/T-1171 (the
families) · T-1199 (seating) · `docs/RESEARCH/community_shares_1835.md` (T-1375, the
community attribute this cohort is the first to carry from a pool).
