---
id: T-0987
title: The directories' ties and refusals, adjudicated one stretch per run — the 196 ties surname-plus-initial cannot decide, the 1,100 initial-absent refusals a page image can overturn, and every trade and 1839-44 address that lands spent onto the card and the street face; the run that closes this files the next stretch before it closes
state: claimed
epic: PAPERS
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-09
closed: null
pr: null
claimed_by: run 9/12/2026, 2:05:46 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34712943596
---

**OWNER, 2026-09-10: "Directories as a succession ticket at the end of band 1."** This is the
open-ended-programme shape `tickets/README.md` describes: one unit, worked one stretch per run,
and **the run that closes a stretch files the next one's ticket before it closes** (T-0028 is
the worked example). It never closes on "there was nothing left" — it closes when the pools
below are empty, and says so with the counts.

## What the directories are, measured, so the work is the right work

Fergus 1839, Fergus 1843 and Norris 1844 are **transcribed in full** — 8,258 claims across
eleven files, every page declared in `data/research/directories/coverage.json`. Nobody has to
read a page to start. `measure_research_spend.py` reads them as 8,258 read, 1,029 spent, 7,229
unspent, and the unspent seven thousand are not a backlog: they are entries whose surname has
no 1835 counterpart — people who arrived after the scene date — and the crosswalk cannot reach
them by construction. **Do not file a ticket to "read" them.**

What still has yield is three smaller pools the three crosswalks already name, and every unit
in them is a person of 1835 who may gain a trade, an 1839-44 address, or both:

| pool | where | count |
|---|---|---|
| **ties** the surname-plus-initial rule cannot decide (ambiguous + contested) | `fergus_1839_crosswalk_1835.json` residents 46+32 · `fergus_1843_crosswalk_1835.json` 41+17 · `norris_1844_crosswalk_1835.json` 23+16 · `norris_1844_advertiser_crosswalk_1835.json` 8+13 | **~196** |
| **initial-absent refusals** — surname present in 1835, the printed initial not | 276 · 349 · 335 · 140 in the same four files | **~1,100** |
| **forename-disagreed refusals** | 94 · 48 | **~142** |
| **could-carry** trades and addresses on matched entries | 1839: 98 trades, 96 streets · 1843: 83 addresses (trades read 0 until **T-0867** fixes `none_recorded`) · 1844: 63 trades, 73 addresses | **~410** |

T-0696 (landed) is the rule for the ties: **a trade may narrow a tie, a premises may not**, and
a narrowed tie is filed `discriminated`, never promoted to a match. T-0900 (band 1, above) is
one initial-absent refusal being overturned off the page image — that is the shape of the second
pool's work. `tools/back_project_addresses.py` (T-0633) and `tools/back_project_residences.py`
(T-0669) are how an address that lands becomes a **street face** — never a lot, never a roof —
and their refusals are readings, kept in full.

## A stretch

One run takes ONE bounded stretch and finishes it: a letter range of one directory's ties, or
one refusal class on one directory, or the could-carry pool of one directory once T-0867 lands.
Name the stretch in the claim commit. A stretch is done when every unit in it carries a ruling —
match, `discriminated`, or a refusal that names its clause — and everything that landed is
spent: the trade onto the card under the 1835/`later_occupation` rule T-0837 gated, the address
through the back-projection as a face.

**Order the stretches by yield, and say the yield.** The ties first (a tie is one page-read
from a match); then the initial-absent refusals of the directory whose scan is best; then
could-carry once its normaliser is fixed. The forename-disagreed pool is last — T-0670's
refusal is usually right.

## Acceptance — per stretch, one demonstration

1. The stretch is named, bounded, and every unit in it is ruled — nothing in it is left silent.
2. Every match or `discriminated` outcome cites the printed line (`quote`) and the 1835 card,
   and every refusal names its clause. A page-image read that overturns a refusal is
   `scan_verified` and says which leaf.
3. **Every trade and address that landed is spent in the same run** — the card carries it, the
   face is placed or the back-projection's refusal is recorded — and
   `measure_research_spend.py` shows the directories' `unwritten` column at 0 afterwards.
4. The three crosswalk `counts` blocks are re-derived and the PR body quotes the pool sizes
   before and after, so the programme's remaining size is always the last PR's number.
5. Gates green; the changelog entry says what a visitor can now see — a trade on a card, a
   business on a face — or states plainly that this stretch placed nothing and why.
6. **Before closing, file the next stretch with `ticket.mjs new "…" --after T-0987`**, naming
   its pool and its count from step 4. If every pool above reads 0, close this ticket instead
   and write the final counts into it. Do not file more than the next stretch; this ticket is
   the programme and the next stretch is its cursor.

## What this is not

Not a reading of the 7,229 post-1835 entries (no 1835 person to reach). Not a change to the
matching rule (T-0670, T-0696 stand). Not lots or roofs (L218, L223: a face). Not the Newberry
index, which is its own epic at the foot at a measured 0.0% match.

## Added by T-0989, 2026-09-10 — the 255 acceptance clause 3 is now measuring

Clause 3 above asks for `measure_research_spend.py`'s directories `unwritten` column at 0
after a stretch lands. Until this date that column read 0 for a reason that had nothing to do
with this programme: the second hop judged a ruling stating no source of its own against the
ONE source id at the top of its file, and counted the card as having learned it if the card
cited that id **anywhere, for any reason**. Every ruling in a generated crosswalk shares that
id, so one citation left by another pass passed all of them at once.

T-0989 closed that. A fallback ruling must now also NAME what it adjudicated — the read unit
it cites, or the sheet a sheet-and-line ruling sits on — and directories fell from **914 of
914 written to 659, with 255 unwritten**. That 255 is recorded in the write ceiling with its
reason; it is this programme's debt, and clause 3 is the thing that pays it down. Where it
sits, by file:

```
  159  fergus_1839_crosswalk_1835.json            all 159 — no entry named on the card
   49  fergus_1843_crosswalk_1835.json            of 120
   31  norris_1844_crosswalk_1835.json            of 99
   16  norris_1844_advertiser_crosswalk_1835.json all 16
```

The four sister files — the 1839 election, lots and register crosswalks, and the 394 rulings
in `spend_crosswalk_1835.json` that state their own sources — already reach their cards and
are unmoved. The instance checked by hand: `hh_garrett_a` cites `fergus_chicago_directory_1839`
because a later resident-research pass wrote a generic `directories` block on the card, while
Fergus 1839's ruling for Garrett — entry `f1839_e0527`, "Garrett, Augustus, auctioneer, real
estate, bds. Sauganash Hotel", printed page 15 — has never been written onto it. Nothing was
lost by the change; what was lost had already been lost, and was being reported as green.

A stretch that lands under clause 3 should quote the 255 before and after, the same way
clause 4 quotes the pool sizes.

## Stretch 1, 2026-09-11 — the write debt, paid in full: 263 → 0

**The stretch:** not a pool of ties but clause 3 itself. The 255 T-0989 exposed had grown
to **263** by the time this run measured it, and every other stretch's acceptance runs
through that number: clause 3 asks for the directories' `unwritten` column at 0 *after*
the stretch lands, and no stretch of ties could have reached 0 while 263 rulings that had
nothing to do with it sat unwritten. So the debt was taken first, as one unit.

**What the 263 were.** All of them, in all four files, were the same defect and none of
them was a reading:

```
  158  fergus_1839_crosswalk_1835.json             matches   card lacks the subject
   49  fergus_1843_crosswalk_1835.json             matches   card lacks the subject
   39  norris_1844_crosswalk_1835.json             matches   card lacks the subject
   17  norris_1844_advertiser_crosswalk_1835.json  matches   card lacks the subject
```

`tools/spend_directories.py` wrote the volume into the card's `directories.sources` and
the printed line into a note — but never the ENTRY ID. `card_block` is documented as
"deliberately thinner than the layer" and dropped the `claim_id` that `graded()` had
already computed; and for the 92 people the pass rules on and carries nothing for
(ambiguous or contested: no graded value, so no note at all) the card said only that
some volume had met somebody of the name. So the citation was doing the work of a
reading, exactly as T-0989 described for `hh_garrett_a`.

**The fix, in one place.** The block's own `note` now ends by naming, per person and per
volume, the printed entries this pass ruled onto that household and the status it ruled
them at. `hh_garrett_a` now reads:

> … garrett_a, Fergus's Chicago directory of 1839 — f1839_e0527 (a single entry);
> garrett_a, Fergus's Chicago directory of 1843 — f1843_e0109, f1843_e0110, f1843_e1051
> (ambiguous, so nothing crossed); garrett_a, Norris's Chicago directory of 1844 —
> n1844_e0679 (a single entry); garrett_a, the advertising cards in Norris's directory of
> 1844 — n1844_ad0110, n1844_ad0111, n1844_ad0112 (ambiguous, so nothing crossed).

It went into the NOTE rather than a new leaf on purpose: the note is already rendered
whole by `residents.js` and already declared `shown` in `measure_layer_reads.py`, so the
entry a reader would go back to arrives in front of that reader instead of into a field
nothing opens — and it is the only place that can speak for the 92 silent rows.

**Measured, before and after** (`tools/measure_research_spend.py`, whole town):

| | before | after |
|---|---|---|
| directories, on a card | 669 of 932 | **932 of 932** |
| directories, unwritten | **263** | **0** |
| town total, unwritten | 263 | **0** |
| on the file's word (the softer door) | 266 | 529 |

`unwritten_ceiling.directories` is tightened 264 → 0 in the same commit, so it cannot
regrow. **Every domain in the town now reads 0 unwritten**, and clause 3 is a gate a
stretch can actually pass rather than a debt it inherits.

**The pools are untouched and are what stretch 2 takes** — the ~196 ties first, as this
ticket orders them. No successor ticket is filed: `tickets/README.md` puts the succession
on the run that CLOSES the programme, and the owner's filing rule of 2026-09-10 asks for
fewer tickets, not one per stretch. This ticket stays open and is its own cursor.

## Stretch 2, 2026-09-11 (PR #1128) — the advertiser's ties: 14 ruled, 3 released, and the 64 silent refusals

**The stretch:** the ties of `norris_1844_advertiser_crosswalk_1835.json`, the smallest of the
four pools and the one stretch 1's claim had named before it took the write debt instead. Every
tie in it now carries a ruling; nothing in the stretch is silent.

**What was in it, and what a tie turned out to be.** The pool measured 3 ambiguous + 11
contested = 14. Three of the eleven contests were not contests. The generator keyed the contest
on the CARD:

```python
claimed[m["cards_1844"][0]["claim"]].append(m)     # the card, not the name on it
```

An advertising card is a FIRM's, and a firm's card names its partners. `n1844_ad0046` prints
"A. Loyd" and "H. A. Blakesley" over one grocery at 101 Lake street; `n1844_ad0116` prints
"William B. Ogden" and "William E. Jones" over the North-Western Land Agency. Keying on the card
made rivals of the partners — of men the card itself says stood in business together — and
withheld three matches the surname-plus-initial rule had already made. The key is now
`(claim, proprietor_as_printed)`, which is the only pair two readings can actually contest.

| | before | after |
|---|---|---|
| matched one card | 17 | **20** |
| contested | 11 | **8** |
| ambiguous | 3 | 3 |
| refusals (surname present, initial absent) | 130 | 130 |

Released: **Alexander Loyd** and **Harvey A. Blakesley** (Loyd, Blakesley & Co., grocers, 101
Lake street) and **William B. Ogden** (North-Western Land Agency, Kinzie street east of
Dearborn). The eight that remain are all one printed name read two ways — two Smiths on
"E. Smith", two Clarks on "J. Coe Clark", two Taylors on "Chas. Taylor", and the two Joneses on
the "William E. Jones" that stood under Ogden, who was never their rival.

**Every tie was offered the discriminator, and the offer is recorded.** The advertiser crosswalk
was the one of the four that never imported `tiebreak` — T-0696's ruling had no reach here at
all. It does now, on both shapes of tie, and it fired on none of the eleven:

```
ties_offered_the_trade_discriminator  11
ties_narrowed_by_a_trade               0
```

Nine of the eleven sides carry `none_recorded` in 1835, and a trade that names no side leaves
the tie standing (T-0696 term 2). The two that do carry one do not agree with what was printed:
Charles Taylor is a **carpenter** in 1835 against a "fashionable tailor" card, and Gurdon
Hubbard a **packer** against a forwarding merchant's and an insurance agency's. Neither is a
narrowing and neither was made into one. **This stretch placed nothing on the ground** (clause 5)
— an 1844 advertisement is evidence about 1844, and all three released men already carry an
earlier trade and address from Fergus 1839, which keeps them under the precedence rule.

**The 64 silent refusals, which clause 2 found.** `spend_directories.py`'s ledger says of itself
that "a refusal is declared as explicitly as a carry — the absence of one reads like a pair
nobody has looked at yet", and then wrote `why_refused: null` on **64 of its 161 refusals**,
including all three of this stretch's new matches. Only the untrusted-parse refusal had ever had
a reason. Each refused field now names its clause and the volume that beat it — the
earliest-volume precedence rule, stated at the head of `VOLUMES` and never carried onto a
ruling until now — and a `--self-test` invariant holds it:

| | before | after |
|---|---|---|
| rulings refusing something | 161 | 161 |
| …naming no clause | **64** | **0** |

**Measured** (`tools/measure_research_spend.py`): directories on a card 932 → **938 of 938**,
`unwritten` **0 → 0**. Clause 3 holds. No 1835 grade moved (`grades_1835_changed: 0`), and all
four crosswalks re-derive.

**The pools after this stretch**, for the next one to take:

**re-derived from the four files today, not copied from this ticket's 2026-09-09 table, which
had drifted** — ambiguous + contested, residents only:

| pool | before | after |
|---|---|---|
| ties, Norris 1844 advertiser | 14 | **11, every one ruled** |
| ties, Norris 1844 proper | 33 | 33 |
| ties, Fergus 1843 | 55 | 55 |
| ties, Fergus 1839 (`residents` block: 44 ambiguous + 29 contested) | 73 | 73 |
| **total ties left in the programme** | 175 | **172** |
| initial-absent refusals, four files | 276 · 349 · 335 · 130 = 1,090 | unchanged |

No successor ticket is filed, for the reason stretch 1 gave: `tickets/README.md` puts the
succession on the run that CLOSES the programme, and the owner's filing rule of 2026-09-10 asks
for fewer tickets. **Stretch 3 is the Fergus 1839 ties — 73, the largest pool and the volume
nearest the scene** — and it should check first whether that crosswalk, like this one, has never
been offered the discriminator at all: `tools/crosswalk_fergus_1839.py` does not import
`tiebreak` either, so T-0696's ruling still has no reach over the biggest pool of the four.

## Stretch 3, 2026-09-11 — Fergus 1839's ties, and the rule that had never been run on them

**The stretch:** the ties of `fergus_1839_crosswalk_1835.json` — 44 ambiguous and 29
contested, 73 of the 172 the stretch above re-counted, and the largest of the four pools.
This is the stretch the run above nominated, down to the reason it gave: "it should check
first whether that crosswalk, like this one, has never been offered the discriminator at
all." It had not. Bounded to one directory's resident ties; nothing was read off a page
image. Worked in parallel with that run, which is why the Norris advertiser pool it took is
untouched here.

**What was actually wrong, found before anything was ruled.** T-0696's discriminator and
T-0670's forename rule are both landed, both gated in `check.sh`, and both imported rather
than restated — and NEITHER had ever been wired into `tools/crosswalk_fergus_1839.py`.
`crosswalk_fergus_1843.py` and `crosswalk_norris_1844.py` import them; the 1839 file
imported only `trade_recorded`. So the largest tie pool in the programme had never met
either ruling.

Running the discriminator FIRST, before the forename rule, is what showed why the order
matters. It narrowed 8 of the 73 ties, and two of the eight were wrong in the same way:

> `Taylor, Augustin Deodat, carpenter and builder, 74 Lake st` was named for **both**
> Anson H. Taylor and Augustine Deodat Taylor, each an attested 1835 carpenter. One
> printed line, two people of 1835 — which is the CONTESTED shape the matching rule
> refuses by construction, manufactured by a discriminator weighing a line whose own
> forename contradicts one of the two names.

`Madore Benjamin Beaubien` was the other: narrowed onto `Beaubien, Medard B., merchant` on
a trade agreement, across a forename disagreement T-0670 refuses outright. Medard Beaubien
is a third card this town holds (T-1026).

**So the guard landed first, and the ruling second.**

1. `name_agreement.py` (T-0670) is applied to the residents pool: **75 refusals filed**,
   0 against a garbled reading, 39 residents left with no 1839 entry at all by it. The
   refusals are in `residents.forename_refusals`, each naming its clause and both
   forenames. Scope is the residents pool only — `forename_rule_scope` on the file says
   why: the three list pools mint nobody here and belong to T-0513/T-0514/T-0515.
2. `tiebreak.py` (T-0696) then reads what is left: **4 ties narrowed by a trade**, 30 left
   standing with `discriminator` stating on the record why the trade named two sides or
   none. Every one of the 34 surviving ties carries a ruling; nothing is silent.
3. A third gate is added because the invariant is worth keeping after its cause is gone:
   a narrowing may not name one printed line for two people of 1835. It reads 0 now that
   T-0670 runs first, and `narrowings_withdrawn_as_a_collision` is where it would show.

**Measured, before and after:**

| | before | after |
|---|---|---|
| resident ties (ambiguous + contested) | 44 + 29 = **73** | 22 + 12 = **34** |
| resident matches | 158 | **158** — 22 withdrawn, 22 arrived |
| forename refusals filed | 0 (rule not run) | **75** |
| ties narrowed by a trade | 0 (rule not run) | **4** |
| business street faces (L218) | 15 | **18** |
| residence street faces (L223) | 8 | **6** |
| directories `unwritten` (clause 3) | 0 | **0** |

**What a reader can see.** Three businesses of 1835 reach a street they had no position
on: **Mark Beaubien** on Lake Street, **James Kinzie** on Canal Street, and **Richard J.
Hamilton**, clerk of the circuit court, on the Clark and Randolph corner Fergus prints —
all carried four years, the narrowest gap in L218's set, and all three had been sitting in
the tie pool. Going the other way, **Charles L. Bristol**'s card loses the 1839 trade
`canal contractor`, which was read off `Bristol, Calvin, canal contractor` — the exact
instance T-0670's own docstring names as the defect it was written for — and
**`jones_es_high`** loses a Randolph Street house that stood on `Jones, Hiram`. The rule
gives where the printed name is the man's and takes where it is not, and both directions
are the same measurement.

**The pools after this stretch**, for the next one to order itself by:

```
  ties                        34 (1839, was 73) · 58 (1843) · 39 (1844) · 21 (1844 ad)  = 152
  initial-absent refusals    277 · 349 · 335 · 140                                     = 1,101
  forename-disagreed          75 (1839, NEW — the rule ran) · 94 · 48                  = 217
```

**Stretch 4 is the 1839 volume's could-carry pool, 92 trades and 96 streets on matched
entries** — the third of this ticket's four pools, now that the matched set it is drawn from
has been corrected rather than merely counted, and `trade_recorded.absent` (T-0867) is the
predicate that says which of them the 1835 layer has room for. The ties that remain are 34
here, 58 in Fergus 1843, 39 in Norris 1844 and 11 in its advertiser cards: 142, each one
carrying a written reason. No successor ticket is filed — `tickets/README.md` puts the
succession on the run that CLOSES the programme, and the owner's filing rule of 2026-09-10
asks for fewer tickets. This ticket stays open and is its own cursor.

## Stretch 4, 2026-09-11 — the 1839 could-carry pool, and the split that fed it

**The stretch:** the could-carry pool of `fergus_1839_crosswalk_1835.json` — 92 trades and
96 streets on matched entries, the third of this ticket's four pools and the one stretch 3
nominated. Bounded to one directory; nothing was read off a page image.

**What the pool turned out to be.** Both halves were already SPENT — the trades on the
cards as `occupation_later`, the addresses through both back-projections, with clause 3's
`unwritten` at 0. What was wrong was not the spending but the READING the pool is drawn
from. `tools/read_fergus_1839.py` splits one printed line into name / trade / address, and
the rule for where the name ends was "keep taking capitalised words, up to three":

```
Beaubien, John B., Michigan ave., bet. Lake and So. Water sts
  name 'Beaubien, John B., Michigan' · trade 'ave., bet. Lake and' · address 'So. Water sts'
```

The comma the compositor set was not a boundary to it. So the head street was eaten into
the name, the address became the tail of its own qualifier — **the wrong street** — and the
fragment between them was carried onto the card as a TRADE. `hh_beaubien_john_s` asserted
an occupation of `ave., bet. Lake and`; `hh_hunter_david` one of `street, near Rush`.

**Four defects, all in the reading, fixed at their one place:**

1. **The printed comma closes the name**, unless the token is a title or a suffix — the
   volume sets `Bates, jr., John` and `Baumgarten, jr., Morris`, whose comma is their own.
2. **A street's head word is a proper noun.** `STREET` was compiled `re.I`, so `[A-Z]`
   matched a lower-case letter and the volume's joining words became street names:
   `cor. Clark and Randolph sts` → "and Randolph sts", `bet Dearborn and State sts` →
   "and State sts", `clerk Steamer Geo. W. Dole, for St. Joseph` → **"for St"**. The name
   is now case-sensitive, the street WORD stays case-blind, and a joiner in front of a
   real head is dropped rather than kept.
3. **The compositor's end-of-line break rejoins**, `¬` as well as `-`, and takes the turned
   line's indent with it: `La¬ / Salle st` was read as a street called Salle, and
   `apothe¬ / caries` as two words.
4. **A host named with an initial is a person, tested BEFORE the street table.** Not a
   defect of the split but one it uncovered: with Wolcott's 1839 line no longer a false
   address, his 1843 `bds H. Wolcott` surfaced, and `back_project_residences.py` placed him
   on **Wolcott Street**. `BARE_PERSON` is only reached when no street name is found, so a
   host whose surname is also a street could never reach it. `INITIALLED_PERSON` is ordered
   in front of `street_words`, and excludes the compass initials or `res N. Water` reads as
   a man called Water. Both directions are self-tested.

**Measured, before and after:**

| | before | after |
|---|---|---|
| 1839 entries whose split changes | — | **192 of 1,655** |
| cards whose later trade or address changes | — | **16** |
| phantom streets read off a non-street phrase | 5 | **0** |
| `residents_could_carry_occupation` | 92 | **90** — two were the garbage above |
| `residents_could_carry_street` | 96 | 96 |
| business addresses adjudicated / placed | 150 / 18 | **151 / 18** |
| residence addresses adjudicated / placed | 44 / 6 | **45 / 6** |
| false placements (Wolcott Street) | 1 would have landed | **0** |
| directories on a card / `unwritten` (clause 3) | 938 / 0 | **938 / 0** |

The five streets that vanish are all refusals earned: `for St` and `schooner St` and
`mate steamer St` are vessels and destinations, `ake st` and `born st` are OCR damage that
the 1835 table refused anyway. No 1835 grade moved; `qualify_later_trades.py` re-derived
13 records.

**What a reader can see.** Sixteen cards. John B. Beaubien's directory line now reads as
the printer set it, from Michigan Avenue; David Hunter's trade of `street, near Rush`
becomes the address it was cut from; Tuthill King keeps the New York Clothing Store, and
Funk, Parsons, Hyde, Tucker and Austin each recover the first name of their own firm.
**No face was added and none was lost** — 18 business and 6 residence, as before.

**The pools after this stretch:**

```
  ties                        34 (1839) · 58 (1843) · 39 (1844) · 11 (1844 ad)  = 142
  initial-absent refusals    277 · 349 · 335 · 140                              = 1,101
  forename-disagreed          75 · 94 · 48                                      = 217
  could-carry, 1839           90 trades · 96 streets, all spent, the reading now correct
```

**Stretch 5 is the could-carry pool of Fergus 1843 and Norris 1844** — the same third pool
in the two volumes this one's defect does not reach, and it should check FIRST whether
their own splitters carry the same comma rule: `read_fergus_1843.py` and
`read_norris_1844.py` are separate files and this one's four defects were all local to the
1839 reader. **Two findings this stretch declined to take, recorded here rather than
filed as tickets** (owner's rule of 2026-09-10): the volume's shared street word
(`Clark and Randolph sts` names TWO streets and only the last is read — Eli B. Williams
loses Clark that way), and the 64 clause-1 refusals that are business-shaped addresses
against people the 1835 corpus gives no trade, which get one ruling on the business
question and none on any other. No successor ticket is filed; this ticket stays open and
is its own cursor.

## Stretch 5, 2026-09-11 — the could-carry pool of Fergus 1843 and Norris 1844, and the three characters their splitters cut at wrongly

**The stretch:** the could-carry pool of `fergus_1843_crosswalk_1835.json` (71 trades,
83 addresses) and `norris_1844_crosswalk_1835.json` (65 trades, 80 addresses) — the
third of this ticket's four pools in the two volumes stretch 4's defect did not reach.
Bounded to those two directories; nothing was read off a page image. It is the stretch
stretch 4 nominated, down to the question it told this run to ask FIRST: "whether their
own splitters carry the same comma rule". Both did, and two more besides.

**Both halves of the pool were already SPENT, as in stretch 4** — clause 3's `unwritten`
at 0 before and after — so what was wrong was again the READING the pool is drawn from.
`read_fergus_1843.py` and `read_norris_1844.py` are separate files from the 1839 reader
and from each other, and **151 of their 4,768 entries were split at a character the
compositor did not set a boundary at**.

**Four defects, in the two readers, each fixed at its one place:**

1. **The printed comma closes the name** — stretch 4's rule, never carried here. The
   test was a capital and a count of three (1844) or four (1843), so the run walked
   past the comma set after the forenames:
   `Baumgarteu, Morris, Illinois street, b Dearborn and Wolcott` read a forename of
   "Morris, Illinois" and lost Illinois Street, the only street in the line;
   `Hanson, Abraham, Methodist clergymen` and `Harrington, Joseph, Unitarian clergyman`
   lost the trade the comma opened; `Barker, Peleg A., Farmers Exchange, 35 Lake` lost
   the Exchange.
2. **A suffix or an initial standing on the far side of that comma is not the end of
   the name.** `still_the_name` states the three shapes the name runs THROUGH — a
   suffix's own comma (`Bates, jr., John`), a suffix standing after (`Bumpstead,
   Thomas, jr.`), and a comma the compositor set between two initials (`Hamlin, E. H.,
   Baptist clergyman`). Without it the rule in (1) took eleven of Fergus's `jr.`
   entries apart.
3. **A comma set with NO SPACE after it is the same comma**, and it sits inside a
   whitespace token where (1) could never see it: `Cleaver, T. B.,soap and oil factory`
   and `Wilson, Maihew,ship carpenter` were read as forenames "T. B.,soap" and
   "Maihew,ship". Keeping the comma on the kept half leaves the offset `rest` is sliced
   at unchanged, so the trade comes back whole.
4. **Norris's abbreviations are lower case and a man's initial is not** — the largest of
   the four, 106 entries. `h`, `r` and `b` are his own shorthand for house, residence
   and between, printed in his preface; the pattern that finds where the address begins
   was compiled `re.I`, so it stopped at the first CAPITAL initial in any name.
   `Adams, R. E. W, physician, corner of Clark and Lake streets` was left with no trade
   at all and an address of "E. W, physician, corner of Clark and Lake streets";
   `Beer, Adam, shoemaker, at J. B. Mitchell's` read a trade of "shoemaker, at J";
   `Bigelow, A. clerk at H. O. Stone's, house State street` read a trade of "clerk at"
   and filed his employer's shop as where he lived. The abbreviation WORDS stay
   case-blind; the three single letters do not.
5. **A hyphen is not a word boundary that rule may cut at** (7 entries, Fergus 1843).
   `\b` holds on the far side of one, so `light-house`, `boarding-house`, `packing-house`
   and `poor-house` each read as a trade ending in a hyphen and an address beginning
   "house …". Mark Beaubien keeps a light-house in 1843 and lives at River Street, not
   at "house keeper, res River street".

**Measured, before and after:**

| | before | after |
|---|---|---|
| Fergus 1843 entries whose split changes | — | **45 of 2,695** |
| Norris 1844 entries whose split changes | — | **106 of 2,073** |
| Norris trades cut at a capital initial | 106 | **0** |
| forenames carrying an unspaced comma | 3 | **0** |
| trades ending in a hyphen, 1843 | 7 | **0** |
| 1844 addresses that were the tail of a name (`could_carry_address`) | 80 | **79** |
| directories, on a card / `unwritten` (clause 3) | 927 of 927 / **0** | 927 of 927 / **0** |
| directories claims read / spent / unspent | 8,258 / 1,007 / 7,251 | unchanged |
| 1835 grades moved by the spend | 0 | **0** |
| business street faces (L218) / residence faces (L223) | 18 / 6 | **18 / 6** |

**What a reader can see — and the part that was not expected.** The cross-domain identity
index (`consolidate_resident_evidence.py`) keys an identity on the surname and forename the
reading gives it, so **51 identities were keyed on a forename with a street, a trade or a
denomination stuck to the end of it** — `id_anderson_john_washington_hall_n`,
`id_barker_peleg_a_farmers_exchange`, `id_wilson_maihewship`, `id_beaubien_mark_u_s`,
`id_hanson_abraham_methodist`. Such a key can never meet the man it belongs to. All 51 come
back to their own names, and **five men the index was carrying twice are one man again**:
Charles Billings Smith, David Lewis Roberts, William Rowlatt, James L. Howe and John P.
Bowes. Identities 6,851 → **6,846**; derived refusals 1,837 → **1,833** (four were refusing a
name nobody had); the directories domain's identities 2,897 → **2,892**; rungs R3 124 → 121
and R4 77 → 76. That file is gated (`--check`) and is where the fault would otherwise have
kept sitting.

**Six household cards correct the LINE they cite.** `mint_civic_residents.py` carries the
directory locator onto the card, and six were pointing a reader at a fragment that began in
the middle of a man's own firm: `hh_bowen_erastus_selden` cited "B. & Cole, house Michigan
avenue" and now cites "house Michigan avenue"; `hh_smith_e_kirby` cited "H. & E. Smith, h
Ohio jst. b Dear and Wolcott" and now cites "h Ohio jst. b Dear and Wolcott";
`hh_bradley_joseph`, `hh_goodrich_john`, `hh_jones_william` and `hh_sherman_rebecca` the
same. `ladder_spend.json` re-derives with them.

One card gives something up and it is the honest direction:
`hh_bradley_joseph`'s Norris 1844 line, "Bradley, Joseph, clerk, at W. H. Adams & Co.'s",
stops declaring that it HOLDS an address — the address it held was the second half of his
employer's name. **This stretch placed nothing on the ground** (clause 5): the four
volumes' precedence rule is untouched, every person whose reading changed already carries
an earlier volume's trade or an 1835 one, and the crosswalk counts are unmoved but for the
one false address above. What changed is that 151 printed lines now read as the printer
set them. `read_norris_1844.py --self-test` holds all three comma-and-capital rules on
seven named lines and sweeps the whole reading for either failure; the assertions fire
when broken.

**The 1839 reader was NOT changed.** The same three shapes exist there — `Morrison,
Ephriam, jr., teamster` reads a trade of "jr., teamster", `O'Meara, Timothy, Rev.,
Catholic priest` one of "Rev., Catholic priest", and `Dickey, Hugh, T. , attorney` loses
the T. — but that volume's `TITLES` includes `judge`, `hon` and `prof`, which are trades
there as often as titles, and the exception written for 1843 and 1844 walks straight into
them: it turned `Pearson, Hon. John, judge Circuit Court` into a forename of "Hon. John,
judge". Seven entries, three of them wrong today and four of them made wrong by the
naive fix. It needs the 1839 volume's own list, not this one's, and it is recorded here
rather than filed (owner's rule of 2026-09-10).

**The pools after this stretch:**

**re-derived from the four files today, not copied from stretch 4's table, which had
drifted** — ambiguous + contested, residents only:

```
  ties                        34 (1839) · 54 (1843) · 33 (1844) · 11 (1844 ad)  = 132
  initial-absent refusals    277 · 349 · 343 · 130                              = 1,099
  forename-disagreed          75 · 91 · 51                                      = 217
  could-carry, 1839           89 trades · 95 streets, spent, the reading correct (stretch 4)
  could-carry, 1843           71 trades · 83 addresses, all spent or refused with a clause
  could-carry, 1844           65 trades · 79 addresses, ALL 144 refused — see below
  could-carry, 1844 ad        12 trades · 15 places of business
```

Stretch 4's line read "34 · 58 · 39 · 11 = 142" and "277 · 349 · 335 · 140 = 1,101";
three of those eight numbers were carried forward rather than re-read, which is the
drift stretch 2 caught the first time and named. Every figure above comes from the
`counts` block of the file beside it, re-derived in this run.

**Stretch 6 is the 1844 half of that last line, and this stretch is what unblocks it.**
`spend_directories.py` carries a volume-level flag, `parse_trusted: False`, on Norris 1844
alone, and every one of that volume's 144 could-carry units is refused by it under one
clause — T-0569's `UNTRUSTED_SPLIT`, which says the split "yields a value containing no
trade at all rather than a trade with something extra on it" and cites `of Loyd`,
`of Horace Norton & Co` and twice simply `of`. Measured against the corrected reading:
**13 of the volume's 65 matched trades are that shape** (a partnership named where the
trade would go) and **52 are plain legible trades** — carpenter, baker, tailor, physician,
watchmaker, "grocery and provisions, South Water st". A great many of the rest of that
refusal's reputation was defect 4 above, now gone. A blanket refusal is not a ruling about
a line, and clause 1 of this ticket asks for one per unit: stretch 6 replaces the volume
flag with a per-entry, per-FIELD predicate (the partnership shape refuses a TRADE and says
nothing about the address beside it), and spends what survives. No successor ticket is
filed — `tickets/README.md` puts the succession on the run that CLOSES the programme, and
the owner's filing rule of 2026-09-10 asks for fewer tickets. This ticket stays open and
is its own cursor.

## Stretch 6, 2026-09-11 — Norris 1844's blanket refusal, replaced per entry and per field

**The stretch:** the could-carry pool of `norris_1844_crosswalk_1835.json` — 65 trades and
79 addresses, all 144 of them refused by one clause — and the volume flag that refused
them. It is the stretch stretch 5 nominated, in the words it nominated it: "replaces the
volume flag with a per-entry, per-FIELD predicate (the partnership shape refuses a TRADE
and says nothing about the address beside it), and spends what survives."

**What the flag was.** `spend_directories.py` carried `parse_trusted: False` on Norris
1844 alone, and `graded()` skipped every row of a volume that had it. The refusal's
GROUND, T-0569's, is sound and is unchanged here: the volume sets a partnership where the
trade would go — `of Loyd`, `of Horace Norton & Co`, twice simply `of` — so the split
yields "a value containing no trade at all rather than a trade with something extra on
it". What was wrong was the SCOPE: a sentence about three lines refusing a hundred and
forty-four, which is not a ruling about a line, and clause 1 of this ticket asks for one
per unit.

**The predicate.** `split_refusal(field, value)` returns the clause key this entry's
split is refused under for this field, or nothing — and `SPLIT_CLAUSES` holds the three
clauses, written into the layer so the sentence on the record and the sentence in the
ledger are the same sentence. Three shapes:

| clause | shape | refuses |
|---|---|---|
| `firm_where_a_trade_is` | the value BEGINS `of` — the volume's "Surname, initials, of <firm>" | the trade |
| `premises_where_a_trade_is` | the value BEGINS `at` — `at United States Hotel`, `at clerk's office` | the trade |
| `address_is_a_backreference` | a locative and then only a ditto — `res same`, `house same`, `res "` | the address |

Both trade patterns anchor at the START, which is what separates them from a trade with
something extra on it: `clerk, at T. King's` and `book-keeper at G. S. Hubbard's` are
trades and cross. No trade in the English of 1844 begins with either word.

**The shapes are a compositor's construction, not one volume's habit, so all four volumes
are asked** — and two of the three the flag TRUSTED print them and had been carrying them.
That is the finding the boolean could not make: under it nobody ever looked.

**Measured, before and after** (`spend_directories.py --report`, whole town):

| | before | after |
|---|---|---|
| people carrying a later trade | 126 | **138** |
| people carrying a later address | 149 | **165** |
| ledger rulings that carried something | 202 | **220** |
| `line_held_but_parse_refused` — held a line, got nothing | 17 | **0** |
| trades refused, by clause | 65 (one clause, one volume) | **16** (2 clauses, 2 volumes) |
| addresses refused, by clause | 79 (one clause, one volume) | **8** (1 clause, 2 volumes) |
| directories, on a card / `unwritten` (clause 3) | 927 of 927 / **0** | 927 of 927 / **0** |
| 1835 grades moved | 0 | **0** |
| business street faces (L218) | 18 | **18** |
| residence faces (L223) | 6 | **14** |

**What the retractions were.** `hubbard_henry_g` carried `at G. S. Hubbard & Co.’s
warehouse` as his 1839 trade — a door, not an occupation; Fergus 1843's `clerk, Circuit
Court` now wins the field, a real trade four years nearer the scene, so the clause
promoted a reading rather than costing one. `rue_john_c` carried `res same` and now
carries Norris's `h Clark, b Madison and Monroe`. `burton_edward` carried `res same` and
no other volume names him, so his card gives the address up: the honest direction.

**Two older faults the released lines walked into, both fixed here because leaving either
would have shipped a placement the policy documents forbid in writing.**

1. **`RESIDENCE_PREFIX` knew only Fergus's words.** `docs/ADDRESS-BACK-PROJECTION.md`
   clause 2 refuses an address the volume prints as a residence, and the pattern that
   reads it listed `res`, `bds`, `boards` — never `house`, `h` or `r`, which are Norris's
   own shorthand, declared in his preface. It had never been exercised on them because
   his parse never reached the clause. The first that did was `house N Water st (See
   card` — Silvester Marsh's HOME — and the business pass PLACED it as a shop face on
   North Water Street, the one street in the town no other rule can seat a building on.
   The pattern is shared by both passes, so adding the four words moves him to the
   residence pass, where he places as a home. Business faces end where they started, 18.
2. **A mis-set space defeated both personal-name tests.** `residence Hum phrey Clark's`
   is Humphrey Clark's house; `street_words` read `Clark` as Clark Street and placed
   Erastus Clark on it. `INITIALLED_PERSON` and `BARE_PERSON` both stand in front of the
   street table for exactly this collision and both key on the SHAPE of a name, which
   `Hum phrey` is not. `POSSESSIVE_HOST` does not: none of these four volumes ever prints
   a street possessively, so a body ending `'s` is refused as a householder before the
   street table is consulted. Four of the addresses this pass adjudicates are that shape.

**What a reader can see.** Fourteen households stand on a street face where six did this
morning, and three streets — Dearborn, Randolph and Wells — are reached by a house for the
first time; Norris prints a man's home far oftener than his shop, which is why this pass
and not the business half is the one his volume feeds. **L223 is restated 6 → 14** with
both faults above written into it; **L218 is unmoved at 18**. Nothing is drawn (L2).
`residents.js` names WHICH field's split does not cross instead of saying it of the whole
line, and the panel's summary sentence reports the two per-field counts in place of a
figure that is now always zero.

**The gates.** `check.sh` 308 steps green. Both back-projection passes gained self-test
rows for Norris's words, the possessive and the ditto, and the business pass gained two
holding that `Randolph st` and `Lake st` are still streets and not `r` and `h`.
`spend_directories.py --self-test` replaces its one-volume rule-3 assertion with two that
run over every volume: nothing a clause refused reached a card, and nothing that reached
one has a shape a clause names — the assertion the flag could never make.

**The pools after this stretch**, re-derived from the four `counts` blocks today:

```
  ties                        34 (1839) · 54 (1843) · 33 (1844) · 11 (1844 ad)  = 132
  initial-absent refusals    277 · 349 · 343 · 130                              = 1,099
  forename-disagreed          75 · 91 · 51                                      = 217
  could-carry, 1839           89 trades · 95 streets, spent (stretch 4)
  could-carry, 1843           71 trades · 83 addresses, spent or refused (stretch 5)
  could-carry, 1844           65 trades · 79 addresses — 50 and 75 SPENT, 15 and 4
                              refused per entry, per field, each naming its clause
  could-carry, 1844 ad        12 trades · 15 places of business, spent (stretch 2)
```

**The could-carry pool is now closed in all four volumes.** Stretch 7 takes the **ties**,
132 of them, as this ticket's own ordering asks — a tie is one page-read from a match and
they are the pool that stood first in the table before the write debt and the readers
took precedence. No successor ticket is filed: `tickets/README.md` puts the succession on
the run that CLOSES the programme, and the owner's filing rule of 2026-09-10 asks for
fewer tickets. This ticket stays open and is its own cursor.

## Stretch 7, 2026-09-12 — Fergus 1843's ties, and the man the volume prints twice

**The stretch:** the ties of `fergus_1843_crosswalk_1835.json` — 39 ambiguous and 15
contested, 54 of the 132 ties stretch 6's table counted, and the largest single-volume tie
pool. It is the stretch stretch 6 nominated ("stretch 7 takes the **ties**, 132 of them, as
this ticket's own ordering asks — a tie is one page-read from a match"). Nothing was read
off a page image: the answer was already in the transcription, in a field nobody had asked
about.

**What the ties were.** Fergus 1843 is TWO directories bound as one, and only this volume
of the four is: a `business directory` of 174 subscribers' notices set under trade headings,
each headed by the subscriber's name in capitals, and an `alphabetical directory` of 2,521
lines, one to a person. **A tradesman who paid for a notice also stands in the roll, so the
volume prints him twice** — and the crosswalk's ambiguity test counted PRINTINGS. Silas B.
Cobb's own advertisement arrived as a rival candidate for Silas B. Cobb, and the tie could
only ever be narrowed. Eighteen of the printings standing in the tie pool were a notice of
that kind. The `section` field that says which is which has been in the claims file all
along; no crosswalk had ever read it.

**The rule, and it is a new module so that it is one rule and not four.**
`tools/printed_twice.py` (self-test, 17 cases) folds a notice onto the roll entry it can
only be, in four clauses: the folded surnames agree; the printed names are CONSISTENT —
`name_agreement`'s first-forename rule plus every FURTHER initial both printings set; the
notice prints a surname and TWO OR MORE initials, or the two printings name a thing in
common (a street number, or a word of five letters or more that both set, one a prefix of
the other, street names and the compositor's furniture struck out); and EXACTLY ONE roll
entry in the whole volume satisfies the first three. **78 of the 106 notices fold. The
other 28 stand as their own candidate exactly as before**, and the clause that was silent
is written against each — all 106 notes are filed in the crosswalk's new `printed_twice`
block, because a refusal here is a reading. A folded notice is not discarded either: it is
carried on the roll entry's row as `also_printed`, quotable.

One thing the rule had to do that the imported one cannot. `name_agreement.agrees`
deliberately does not compare FIRST initials — the crosswalks get that from the bucket they
look a resident up in — so `G. S. HUBBARD` read as consistent with `Hubbard, Ahira` and
clause 4 refused every Hubbard notice for want of it. A module asking its question of two
PRINTINGS has to ask for the initial itself. With that, `Morris, Mrs` stops standing
between B. S. Morris and his own notice, and three more notices fold.

**What landed.** Six men of 1835 gain a listing that was ambiguous: `cobb_silas_b`,
`morris_b_s`, `hubbard_gurdon` (two notices onto one roll line), `harmon_charles_l`,
`bishop_j_e`, `funk_absolom`. 1843's matches 119 → **125**, ambiguous 39 → **31**,
contested 15 → **17** — and the two that became contested are the finding under the
finding: the exchange broker's notice is **Jonas Coe** Clark (`J. COE CLARK`, exchange
broker, Clark St.), not a candidate for either John Clark, so what is left is a true
collision of two residents over one roll line rather than a four-way muddle. Everything
that landed is SPENT in this run: the directories' `unwritten` column is **0** of 939
reached (927 before), and could-carry on this volume goes 71/83/82 → **74/89/86**, each
written.

**The comma that was hiding a house** (clause 3 of this ticket, the half that is a face).
A match carries its address through the two back-projection passes, and the nearer reading
this stretch landed arrives in a shape neither pass could read: the crosswalks split the
printed line on its punctuation, and where the trade's own trailing corner falls into the
address field the field opens with the SHOP and goes on to the HOME — `cor Clark, res
Dearborn, bet Washington and Madison`. Both passes tested the volume's residence word at
the HEAD of the field only, which is the fault stretch 6 fixed one clause earlier (`house N
Water st` placed as a shop face). `split_home()` now cuts the field at that word and each
pass reads its own half; the whole field stays the quote, and the record carries
`address_read_as_the_home` where the two differ.

It pays for itself twice over. **Doctor D. S. Smith's home stands on La Salle Street** — a
face no house had reached — off `office on Clark street … residence La Salle street,
opposite the First Baptist Church`, a residence clause that had been invisible because the
line opened with his office. And **Charles L. Harmon comes off Dearborn Street**, which
looks like a loss and is a repair: he stood there on Norris's `res Dearborn st. b Wash and
Mad sts`, where the abbreviation hid Madison — a street the 1835 layer does not carry — so
the R4 qualifier clause never fired. Fergus spells it out four years nearer the scene, the
clause reads it, and it refuses. **L223 is unmoved at 14** and L218 unmoved at 18; the
residence pass adjudicates 61 → **63**, because two fields it could not see are now read.

**Two findings this stretch declined to take, recorded here rather than filed, since this
ticket owns the question.**

1. **A title read as a forename.** `Doctor D. S. SMITH`, `Doctor Egan`, `Doctor Blaney` —
   14 printings in this volume open with a doctor's title spelled in full, and `doctor` is
   in neither `name_agreement.TITLES` nor the local `initial()` of any of the four
   crosswalks (all of which carry `dr`). So the title is read as the forename: it sets the
   bucket initial to `d`, and it defeats clause 2 of the fold. One ruling depends on it
   today — `smith_d_a`'s tie, where `Doctor D. S.` cannot be shown to be `David Sheppard`
   — and the exposure is larger than that, because a resident printed with the initial D
   can be offered `Doctor Egan`. It is one word in a shared module and it re-derives all
   four volumes, which is why it is stretch 8's and not this one's.
2. **One placement still resting on an unread qualifier.** `sherman_rebecca` stands on
   Clark Street off `h Clark st. b Mad. & Mon` — Madison and Monroe, abbreviated, and
   `NOT_1835` keys on the words spelled out. It is the same clause this stretch just
   applied to Harmon, escaping on a contraction. Filed as a ticket of its own because it
   belongs to the back-projection pass and not to the directories.

**The gates.** `check.sh` 310 steps green. `printed_twice --self-test` 17 cases; both
back-projection self-tests green; the derived layer re-derived with `rederive.mjs --run`
and both back-projections re-written. NOTE for the next run: the chain needed **two**
passes to converge, because `mint_civic_residents` rewrites a card's note from its own
template when the card's source list changes and `spend_land_sales`' prose — which runs
earlier — is re-appended only on the following pass. A card can therefore be one pass short
of its own provenance. Recorded here; it is not this ticket's.

**The pools after this stretch**, re-derived from the four `counts` blocks today:

```
  ties                        34 (1839) · 48 (1843) · 33 (1844) · 11 (1844 ad)  = 126
  initial-absent refusals    277 · 349 · 343 · 130                              = 1,099
  forename-disagreed          75 · 90 · 51                                      = 216
  could-carry                 closed in all four volumes (stretches 2, 4, 5, 6)
```

**Stretch 8 is the title read as a forename, and then Norris 1844's ties.** Finding 1 above
is the first thing to do, because it is cheap, it reaches matches and not only ties, and it
is the only known way a ruling in these four files can be made on a word that is not a
name. Then the 33 ties of `norris_1844_crosswalk_1835.json`, where the same
one-man-two-printings question takes a different shape: his advertising cards are a
SEPARATE crosswalk file, so a man with a card and a roll line is counted once in each, and
whether those two are one printing is the question this volume's fold has to answer. No
successor ticket is filed: `tickets/README.md` puts the succession on the run that CLOSES
the programme, and the owner's filing rule of 2026-09-10 asks for fewer tickets. This
ticket stays open and is its own cursor.

---

**LAPPED ONTO `dev` 2026-09-12, and the lap moved one of this stretch's two placements.**
Stretch 7's PR (#1167) was pushed, gated green and never merged — the run that opened it
ended at the merge — so twelve `dev` merges landed under it before this one picked it up.
The lap is not bookkeeping only, and the difference is recorded here rather than left in a
diff:

- **T-1049 (#1175) withdrew `hh_smith_d_a`.** The card was minted on a press notice printed
  against `Courtland, Alabama`; T-1048's resolved place vocabulary refuses that as a Chicago
  appearance, the ladder then reaches nothing for the identity, and the container goes with
  it. So `Doctor D. S. Smith … residence La Salle street` — the residence clause
  `split_home()` uncovered, and the headline placement of this stretch — has no person of
  1835 left to reach. The clause and the reading stand; the FACE does not. Recorded, not
  claimed.
- **L223 therefore restates 13 → 12**, not 14: `harmon_charles_l` still comes off Dearborn
  Street under the R4 qualifier, and `smith_d_a` cannot replace him. The twelve are six on
  Fergus 1843 and six on Norris 1844; the pass adjudicates 60 with 48 refusals. The
  changelog entry was corrected in the same commit — it had promised a visitor a house on
  La Salle Street that this tree does not place.
- The derived layer was rebuilt with `rederive.mjs --run` and both back-projections
  re-written, twice to convergence, exactly as the note above predicted.

Nothing about the `printed_twice` fold changed on the lap: 78 of 106 notices still fold and
the six 1843 listings still land. The pool table above is re-derived and unchanged.

---

## Stretch 8, 2026-09-12 — the title read as a forename, in all four volumes and on both sides of every comparison

**The stretch:** finding 1 of stretch 7 — "a title read as a forename" — taken across the
four crosswalks, the module they all import, and the reader that feeds one of them. It is
the stretch stretch 7 nominated, in the order it nominated it ("the first thing to do,
because it is cheap, it reaches matches and not only ties"). It is bounded to the
vocabulary and what re-derives from it; the 33 Norris 1844 ties, the second half of that
nomination, are NOT in it and are stretch 9 below. Nothing was read off a page image.

### What was wrong, measured before it was touched

`name_agreement.TITLES` held nine abbreviations. Each of the four crosswalks restated its
own copy — 1839's added `hon` and `esq`, the advertiser's added `doctor`, 1843's and
1844's were inline literals inside `initial()` — and **not one copy carried a rank spelled
out in full**. The corpus prints them on both sides of every comparison:

```
  printed, in the volumes      13   Fergus 1843  DOCTOR BLANEY · DOCTOR EGAN · DOCTOR
                                                 J. BRINKERHOFF · DOCTOR H. H. BRAYTON ·
                                                 DOCTOR JOHN W. ELDRIDGE · DOCTOR BENJAMIN
                                                 F. HALE · DOCTOR D. S. SMITH
                                    Fergus 1839  Campbell, Major James B · Handy, Major ·
                                                 McClure, Judge Samuel · Mulford, Major E. H ·
                                                 Noble, Major · Tew, Prof. Geo. C
                                    Norris 1844  none, in the roll or the advertising cards
  on the 1835 cards            14   Lieut. James Allen · Judge Sidney Breese · Major John
                                    Greene · Major Handy · Judge Silver · Major L Shapley ·
                                    Lieut J L Thompson · and the seven suffix names below
```

Eighteen entries in Fergus 1839 alone were indexed on the initial of a rank or a suffix
rather than of a name (`Archdale, jr` → J, `Campbell, Major James B` → M, `Noble, sen.,
Mark` → S, `Tew, Prof. Geo. C` → P). And the residents layer keys fourteen people the same
way, seven of them on a SUFFIX: `John Bates Jr.` was in the 1839 pool as a man whose
surname was **Jr**, and so were Joshua Hathaway and Elijah Wentworth.

The worst of it is not a miss but a match. `Major Handy` met `Handy, Major` on a shared
initial — the M of Major, on both sides, a rank agreeing with itself. `Lieut J L Thompson`
was matched to `Thompson, Leveret`, admitted to the Second Presbyterian church in **1889**,
on the L of Lieut. `Morgan Shapley` of the 1837 poll reached `Major L Shapley` on the M of
Major, and had written a paragraph onto his card.

### What was done

1. **One vocabulary, written once** (`tools/name_agreement.py`). Every rank now carries its
   abbreviation AND its full spelling, so the pair cannot drift apart again, plus `judge`,
   which these volumes print with no abbreviation at all. `SUFFIXES` gains `esquire`
   beside `esq`. Nothing is in it that the corpus does not print, and no token in it stands
   as a forename anywhere in the residents layer or the four transcribed volumes — measured,
   not assumed.
2. **The four crosswalks import it** rather than restate it. 1839 and the advertiser keep
   their own additions where they are the volume's own (`junr`, `md` — the advertiser's
   tokeniser splits on whitespace alone, so `M.D.` reaches the test as one word there and
   as two everywhere else).
3. **A no-forename refusal, shared** (`na.no_forename_refusal`). `split_name` used to
   return the rank AS the given; with the vocabulary fixed it would have returned nothing
   at all, and a row dropped there is a row no refusal is ever filed for. It now keeps the
   surname, empties the given, and the caller files a refusal that says a rank is standing
   where the given name should be. Four people reach it: Major Handy, Judge Silver, Jun
   Marknoble, Sen Marknoble.
4. **The loose suffix comma** (`tools/read_fergus_1839.py`). Six entries set the suffix's
   comma with a space before it — `Archdale, jr. , John, contractor` — so the comma arrived
   as a token of its own and broke the name loop: the forename was swallowed into the trade
   and `jr` stood as the given name. The waiver the reader already grants a tight `jr.,` now
   covers the loose form. Archdale, Butterfield, Frink, Johnston, King and Ludwig read their
   forenames; six trades lose a name off their head (`John, merchant` → `merchant`).
5. **A withdrawal** (`tools/spend_fergus_1839_later_lists.py`). `strays()` had always
   REFUSED a card carrying this pass's paragraph with no ruling behind it, and nothing could
   ever clear one — the gate could report the state and not leave it. `retract_from_person`
   undoes exactly what the applier does, the paragraph and the citation, and five self-test
   cases hold it. Shapley's card is the first to use it.

### What landed, and what it cost

**Two men gain a land purchase.** `ALLEN JAMES` (ls0954) reaches Lieut. James Allen and
`BREESE SIDNEY` (ls0651) reaches Judge Sidney Breese, both `forename_agrees` — the deed-book
reading had been weighing "James" against "Lieut" and "Sidney" against "Judge" and finding
two different names. Both refusals of rivals are re-derived and stand.

**Four of Fergus 1843's advertising doctors stop being two men each**: `f1843_e0134`
(Brayton), `e0137` (Eldridge), `e0138` (Hale), `e0140` (Smith) fold onto roll entries
`e0422`, `e0900`, `e1179`, `e2289` under stretch 7's clause 1, which the title had been
defeating. Notices folded 78 → 82; standing as their own candidate 28 → 24. The three that
still stand — DOCTOR BLANEY, DOCTOR EGAN, DOCTOR J. BRINKERHOFF — print one initial or none,
and the clause that is silent is written against each.

**Two false matches are withdrawn**, and this is the point of the stretch: Lieut J L
Thompson / Leveret Thompson (1889) and Major L Shapley / Morgan Shapley (1837 poll). The
Shapley paragraph is unwritten and the 1839 citation with it. Major Handy's 1839 listing
goes too, and is now a filed refusal rather than a match on a rank.

**One new match, and its weakness recorded.** Lieut J L Thompson now matches `Thompson,
Joseph, caulker, house Adams st. b Clark and Lasalle` (n1844_e1767) — the only J Thompson
in Norris 1844. It stands by the ratified rule (an initial against a full forename is a
match, T-0670) and no clause refuses it, but the 1835 card prints initials only and the
trades disagree in kind. Recorded here rather than dressed up.

**This stretch placed nothing on the ground** (clause 5). The two back-projections
adjudicate three and one more units than they did — 158 → 161 and 60 → 61 — and every one
of the four is refused: three on clause 1 (no 1835 business) and one on clause 3 (not on
the 1835 grid). **L218 unmoved at 18** and **L223 unmoved at 12**.

**Clause 3, the write ceiling:** `measure_research_spend.py` reads directories **912
reached, 912 judgeable, 912 on a card, 0 unwritten**.

**The pools after this stretch**, re-derived from the four `counts` blocks, and stated with
the formula so they can be compared: ties = `ambiguous` + `contested`; initial-absent =
`refusals`; forename-disagreed = `forename_refusals`. The same formula over `HEAD` gives
the before column, so the two are one measurement and not two.

```
                       1839        1843       1844      1844 ad      total
  ties              34 -> 37    44 -> 45   30 -> 31    11 -> 11   119 -> 124
  initial-absent   257 -> 260  323 -> 323 317 -> 316  124 -> 124 1021 -> 1023
  forename-disagr.  69 -> 68    83 -> 80   47 -> 46     0 ->  0   199 -> 194
  could-carry            closed in all four volumes (stretches 2, 4, 5, 6)
```

The ties RISE, and that is the repair rather than a regression: five collisions the rank's
letter had been hiding come into view. Mark Noble is the clearest — Fergus prints `Noble,
sen., Mark` and `Noble, Mark` and the senior was indexed under S, so the junior stood alone
and matched; both now stand under M and the tie is filed. Lieut. James Allen, refused under
L this morning, is a tie under J between `Allen, Capt. James` and `Allen, James P.`.

**Two entries gained a match off the suffix repair**: `Mulford, Major E. H` → E. H. Mulford,
and John Bates Jr., who had been in the pool under the surname "Jr". `John Lyle King` loses
his, because it had stood on the J of `jr.`; his entry now reads `King, jr., John, merchant`
and the 1839 volume holds a second J King, so it is a tie and not a match.

### The gates

`check.sh` **333 steps, none red**. `name_agreement --self-test` 18 cases. The later-lists
pass's self-test 5 cases longer, all on the withdrawal. `rederive.mjs --run` to convergence
(the derived tree is byte-identical on the following pass; only the audit **.xlsx** differs
run to run, because a zip carries its own timestamps — that is not a data difference and
should not be read as one). The two back-projections re-written, and the five steps the
rederive manifest does NOT cover re-run by hand: `qualify_later_trades`,
`back_project_addresses`, `back_project_residences`, `spend_fergus_1839_later_lists`,
`fergus_1839_street_faces`.

### Three findings this stretch declined to take, recorded here rather than filed

1. **The mints restate the same vocabulary again.** `mint_documented_residents.py`,
   `mint_letter_list_residents.py` and `crosswalk_census_1840_heads.py` each hold their own
   `TITLES` set, and each is missing the full spellings this stretch just added to the
   directories. They are not directory passes and their blast radius is the minting of
   cards, not the reading of a book, so they are outside this programme — but they are the
   same defect and a run that touches the residents layer should take them.
2. **`crosswalk_norris_1844_advertiser.py` DOES re-derive its committed file today.** The
   rederive manifest's `_only_gated_tools` note records that running it once rebuilt
   `norris_1844_advertiser_crosswalk_1835.json` from 443 lines to 195 and took
   `data/residents/directories.json` with it, which is why it is not in the manifest. Run
   against this tree, with the shared vocabulary in place, its output is **byte-identical to
   the committed file**. That is not an argument for adding it to the manifest — the
   manifest's rule is that `check.sh` must gate the tool, and `check.sh` still does not
   invoke it at all — but it is worth knowing that the tool is no longer the hazard the note
   describes.
3. **`Doctor Egan` of Fergus 1843 prints no forename**, and `egan_william_b` is on the cards
   as `Dr William Bradshaw Egan`. The two are almost certainly one man; the surname+initial
   rule cannot say so, because one side has no initial. It is the same shape as `Major
   Handy`, and it is what a page image or a second volume would settle.

**Stretch 9 is the 33 ties of `norris_1844_crosswalk_1835.json`**, the second half of what
stretch 7 nominated and unchanged by this one: 17 ambiguous and 14 contested, where the
one-man-two-printings question of stretch 7 takes a different shape, because this volume's
advertising cards are a SEPARATE crosswalk file — a man with a card and a roll line is
counted once in each, and whether those two are one printing is the question this volume's
fold has to answer. No successor ticket is filed: `tickets/README.md` puts the succession on
the run that CLOSES the programme. This ticket stays open and is its own cursor.

## Stretch 9, 2026-09-12 — Norris 1844's ties, and the middle initial no rule had ever read

**The stretch:** the 31 ties of `norris_1844_crosswalk_1835.json` — 17 ambiguous and 14
contested — which is the stretch stretch 8 nominated. It is answered by a clause, not by a
page image: nothing was read off a scan. The clause is in a shared module and it therefore
re-derives all four volumes and the 1837 poll besides, which is the same shape stretch 8
took and for the same reason.

### What the ties were, and it was not the question stretch 8 expected

Stretch 8 nominated this pool for the one-man-two-printings question — a man with a roll
line and an advertising card is counted once in each of two crosswalk files, so whether
those two are one printing is what this volume's fold has to answer. **It is not what these
ties are.** Measured before anything was touched: of the 31, every candidate on both sides
of every tie is a ROLL entry. Two of them (`Taylor, Charles … (Sec card)`, `Murphy, John,
United States Hotel … (See card.)`) point at a card, and in neither case is the card the
rival. The advertiser file's ties, all 11, fire nothing under this stretch's clause either —
measured, and recorded below. The cross-file fold has no case to answer today, so it was not
built.

What the ties actually are is one defect, and it is upstream of all four volumes.

```
  the rule, as it stood     SURNAME folds the same, AND the FIRST initial of the given
                            name matches. Since T-0670, where BOTH readings print a full
                            FIRST forename and the two disagree, the match is refused.
  what was never compared   every initial after the first
```

`name_agreement.agrees` judges the first forename and stops; the crosswalks take the first
INITIAL from the bucket they look a resident up in. So nothing in the chain had ever weighed
a middle initial both readings print. `H. B. Clarke` stood against `Clarke, H. W. attorney
at law` on the H they share. The module that DOES compare them has existed since stretch 7 —
`printed_twice.consistent`, clause 2 — but it asks its question of two PRINTINGS in one
volume and never of a printing against a person of 1835.

### What was done

1. **The comparison, written once** (`tools/name_agreement.py`). `initials()` is lifted out
   of `printed_twice._initials` and `printed_twice` imports it, so the module that folds two
   printings and the module that refuses a person count a name's initials the same way.
   `further_initials_disagree()` compares only the initials BOTH readings set, position by
   position. `narrow_by_further_initials()` is what a crosswalk calls.
2. **An unread initial refuses nothing**, and this is the half that took the measuring.
   Fergus 1839's H is set as two strokes and comes back as `II`, `I I`, `IT`, `IL`, `Ik`;
   its D comes back as `I)`. A first draft of this clause refused `Chapman, Charles II.`,
   `Beaubien, Charles IT`, `Caton, John I).` and `Taylor, Anson IT` — four men the 1835 layer
   holds under the very initial the artefact hides. Measured over the four transcribed
   volumes: 16 further-name tokens carry a character no compositor set and 22 more are two
   capitals with no name behind them. A further initial is READ when it is a single letter
   with nothing but a printer's point after it, or a middle name of three letters or more
   spelled out; `I` is excluded even so, because it is the shape every one of those artefacts
   collapses to and a middle initial I occurs nowhere else in this corpus. This is T-0695's
   principle one field along — a disagreement against a garbled reading is a transcription
   defect and not two people — and it errs in the safe direction.
3. **Silence is not agreement.** Where the refusal would leave exactly ONE candidate and that
   candidate sets fewer initials than the 1835 reading does, nothing is refused and the tie
   stands. `J. B. Cook`, baker, meets `Cook, Josiah P. baker` and `Cook, John, tailor`: the P
   refuses Josiah and what is left is John, silent. Refusing the rival for speaking and then
   promoting the survivor for its silence would deal the baker's listing to a tailor — and it
   would do it on the weaker of the two readings. Four rows decline on this clause across the
   five files (`J. B. Cook` and `William V Smith` in 1844, `D E Jones` in 1843, `William V
   Smith` in 1839, plus two in the poll), and each carries the declined narrowing in a
   `further_initials_declined` field, because a decision not to act is a reading.
4. **The four generators call it**, each filing into a `middle_initial_refusals` list of its
   own with the count beside it — never into `forename_refusals`, so the pool table below
   still means what it meant. Scope is exactly T-0670's: the pool whose rulings reach a CARD,
   and no other. `crosswalk_fergus_1839_election.py` is added to that scope for the first
   time (its residents pool reaches cards and had no forename rule at all).

### What landed

**Thirty-five printings refused** — 6 in Fergus 1839, 12 in Fergus 1843, 13 in Norris 1844,
4 in the 1837 poll — and **twenty matches withdrawn** with them. Every one names the letter
it turned on: `Edward A. Rogers` against `Rogers, Edward Kendall`, `John N Foster` against
`Foster, Dr. John Herbert`, `S W Reed` against `Reed, Stilman O.`, `John A Mills` against
`Mills, John Rodney`, `W B Clarke` against `Clarke, William Hull`.

**Five readings land, and two are people this town should always have had.**

- **Augustine Deodat Taylor**, the carpenter of the first balloon-frame building, reaches
  `Augustin D. Taylor` in the 1837 poll and `Taylor, A. D. builder, house Michigan ave.` in
  Norris 1844. Both had been CONTESTED by `Anson H. Taylor`, whose H the rule could not see.
- **H. B. Clarke** reaches `Clarke, Henry B., farmer, Michigan ave, n.e. cor 16th Street` in
  1843 and `Clarke, H. B. farmer, lake shore, below Michigan avenue` in 1844 — two volumes
  agreeing — instead of the attorney Henry Wilcox Clarke.
- **Eli B Williams** stops sharing his listing with `Williams, E. S. law student`.

**This stretch moved the ground, once, and it is a withdrawal** (clause 5). H. B. Clarke's
business stood on **Clark Street** on the authority of the attorney's `36 Clark`. That match
is gone and the face with it; the Michigan Avenue reading that replaces it is off the 1835
grid, so it places nothing. **L218 is restated 18 → 17** in `docs/LIBERTIES.md`, with the
prose that reasons from the number. **L223 unmoved at 12.** The address back-projection
adjudicates 161 → 156 and the residence pass 61 → 58, the difference being the withdrawn
matches that no longer carry an address to read.

**Clause 3, the write ceiling.** `measure_research_spend.py` reads directories **883 reached,
883 judgeable, 883 on a card, 0 unwritten**, and the town total 0. It did not get there for
free: the first re-derivation left ONE unwritten, and following it is what put the 1837 poll
in scope. `hh_clarke_w_b`'s card had carried the poll's `W. H. Clarke` only because the 1839
directory pass had put a citation there; withdraw the directory match and the poll line stood
naked on a card that never named it. The poll crosswalk had the same defect and no forename
rule at all, so it was given this clause. Three more poll matches fell out with it, including
`Timothy J Clark` against `Thomas A. Clark`.

### The pools after this stretch

The formula is stretch 8's, so the columns compare: ties = `ambiguous` + `contested`;
initial-absent = `refusals`; forename-disagreed = `forename_refusals`. The new column is this
stretch's clause. The advertiser file is unwired and measures **0** — every one of its 11 ties
and 18 matches was tested against the clause and none fires — so it is not carrying an unpaid
debt; `check.sh` does not invoke that generator at all and the rederive manifest's own rule
forbids running an ungated derivation, which is why the file is left alone rather than rebuilt
to add a zero.

```
                       1839         1843        1844      1844 ad      total
  ties              37 -> 37     45 -> 41    31 -> 24    11 -> 11   124 -> 113
  initial-absent   260 -> 260   323 -> 323  316 -> 316  124 -> 124  1023 -> 1023
  forename-disagr.  68 -> 68     80 -> 80    46 -> 46     0 ->  0    194 -> 194
  further initial    0 ->  6      0 -> 12     0 -> 13     0 ->  0      0 ->  35
  matches          152 -> 146   121 -> 115  102 -> 100   18 -> 18   393 -> 379
  could-carry            closed in all four volumes (stretches 2, 4, 5, 6)
```

The 1837 poll is not in that table because it is not a directory: its residents pool goes
matches 90 → 89, ambiguous 31 → 31, contested 21 → 18, further-initial refusals 4.

### The gates

`check.sh` green. `name_agreement --self-test` 18 cases, six of them new and four of those the
stroke artefacts. `printed_twice --self-test` 17 cases — **and it was RED on `dev` before this
stretch touched it**, which is its own finding: stretch 8 put `doctor` in the title vocabulary
and two of that module's cases had been asserting the DEFECT rather than the rule ever since
(`_initials("Doctor D. S.") == ["d","d","s"]`, and `Doctor D. S.` reading as inconsistent with
`David Sheppard`). Nothing was gating it. Both cases are corrected to the post-stretch-8
answer and **`check.sh` now runs `printed_twice --self-test`** beside `name_agreement`'s, so it
cannot go red unwatched again. `rederive.mjs --run` to convergence, both back-projections
re-written, and the five steps the manifest does not cover re-run by hand.

### Two findings this stretch declined to take, recorded here rather than filed

1. **The 1837 poll's residents pool still has no forename rule.** It got this stretch's clause
   because a ruling of its own went unwritten; T-0670's first-forename rule is still not applied
   there, and `Timothy J Clark` against `Thomas A. Clark` was caught on the J and not on the
   Timothy. Two full forenames that disagree should be refused in that file too. It is a
   different rule in a different pool and it belongs to whoever takes the poll, not to this
   programme.
2. **`could_carry` moved and nothing re-read it.** Norris 1844's `could_carry_occupation` goes
   61 → 57 and `could_carry_address` 79 → 78 with the withdrawn matches, and the same in 1843.
   Those pools were closed by stretches 4-6 and the spend passes re-ran clean, so nothing is
   owed — but a stretch that withdraws matches shrinks a pool that a later stretch's arithmetic
   may quote, and this is the note that says so.

**Stretch 10 is the initial-absent refusals of Norris 1844**, 316 of them and the largest
single pool left after the ties: a surname the volume prints and an initial it does not, which
is what a page image can overturn, and Norris's scan is the cleanest of the three. The ties now
stand at 113 across the three volumes and are no longer the biggest thing on the table. No
successor ticket is filed: `tickets/README.md` puts the succession on the run that CLOSES the
programme. This ticket stays open and is its own cursor.

---

---

## Added on the way past by T-1035 (2026-09-12): the initial rule the FIRM route now states does not reach the PERSON route, and cannot

T-1035 asked how much initial agreement a one-surname join needs when both sides print
more than one initial, and answered it for `date_norris_1844_businesses.py`'s firm route:
CONTAINMENT. One side's printed initials must all be printed by the other. `{W}` against
`{W, H}` is one man printed two ways and is admitted; `{W, H}` against `{R, E, W}` meets
on W, and agreeing on one of three is not agreeing, so it is refused. That is landed.

T-1035 carried a note asking the same rule be tested against the PERSON pair T-1034's
cohort C1 found — `foster_amos`, an Amos Foster off one line of the 1833 poll list,
carrying `Foster, A. H. (Jennings & F.)` from Fergus 1843 and Norris 1844. **The test was
run, and the rule does not refuse it.** The person route's forename test is
`tools/name_agreement.py`'s `agrees()`, and it weighs only the FIRST word of each reading:
`is_full_forename('A. H.')` is false, so the pair returns `(True, "initial")` before any
initial past the first is looked at. Transplanting containment changes nothing — the
1835 side prints the full forename *Amos*, which yields the single initial `A`, and
`{A} ⊆ {A, H}` is exactly the abbreviation case containment is written to ADMIT.

**So the shapes are different and the fix is not the same fix.** The firm pair is two
initial RUNS that each print one the other lacks. The Foster pair is a full forename on
one side against an initial run on the other, where the middle initial is simply never
weighed — and it cannot be weighed by name arithmetic alone, because an Amos H. Foster is
a perfectly possible man. What actually stands against this join is EVIDENCE, not a name
rule: no Amos Foster is printed in Fergus 1839, Fergus 1843, Norris 1844 or the newspaper
run at all, while A. H. Foster boards the American Temperance House in two volumes and is
a partner in Jennings & Foster.

It belongs here because this ticket owns the directories' ties and refusals, and because
`agrees()` is imported by all six crosswalks — a change to it is a stretch of this
ticket's work, not a one-line repair. The stretch that takes it should decide whether an
initial run printed against a full forename may carry a SPEND at all, or only a tie filed
for adjudication. T-1034 cohort C1 has already refused FOSTER AMOS for its own purposes
(25 register rows, $468) after stripping the fold, so nothing is bleeding while this
waits.
