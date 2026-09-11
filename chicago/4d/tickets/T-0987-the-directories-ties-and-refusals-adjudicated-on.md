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
claimed_by: run 9/11/2026, 4:07:07 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34647482664
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
