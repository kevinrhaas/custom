---
id: T-0987
title: The directories' ties and refusals, adjudicated one stretch per run — the 196 ties surname-plus-initial cannot decide, the 1,100 initial-absent refusals a page image can overturn, and every trade and 1839-44 address that lands spent onto the card and the street face; the run that closes this files the next stretch before it closes
state: open
epic: PAPERS
requested_by: owner
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-09
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
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

## Stretch 2, 2026-09-11 — the advertiser ties: 14 ruled, 3 released, 8 held, 3 re-described

**The stretch, named and bounded:** every tie in
`norris_1844_advertiser_crosswalk_1835.json` — 3 ambiguous and 11 contested, 14 units,
the smallest of the four tie pools and the one whose units carry the most (a card prints
its trade and its address as their own lines, so this file's parse is trusted where
Norris's alphabetical volume's is not). **Yield stated in advance:** up to 14 people
gaining an 1844 trade and place of business. Landed: 3.

**What the ties were.** Not one of the fourteen needed a page image. The pool was
mostly an artefact of how the contest was keyed:

```
  before                          after
  matched_one_card        17      20      +3
  ambiguous                3       3      re-described, carrying nothing
  contested               11       8      -3
```

**The defect.** A display card is bought by a FIRM and prints its PARTNERS.
`crosswalk_norris_1844_advertiser.py` keyed rivalry on the CARD — `claimed[card_id]` —
so two residents who met two *different* printed names on one advertisement were filed
as rivals for it and neither was matched, on the file's own reasoning that "at most one
of them is the man who paid for it". That is true of a printed name and false of a card:
"Loyd, Blakesley & Co." prints A. Loyd, H. A. Blakesley and Henry Norton; the
North-Western Land Agency prints William B. Ogden beside William E. Jones. Rivalry is
now keyed on the `(card, proprietor)` pair, which is the only place the old reasoning
holds, and the docstring rule says so in the same words.

**Released, and spent in the same run** — `tools/spend_directories.py` re-run, three
household cards rewritten, each card's note moving from "contested, so nothing crossed"
to "a single entry":

| person | card | what it now holds |
|---|---|---|
| `loyd_alexander` | n1844_ad0046 | Loyd, Blakesley & Co., wholesale and retail groceries, nails, glass, shoes and leather — 101 Lake street |
| `blakesley_harvey_a` | n1844_ad0046 | the same firm, as its other named partner |
| `ogden_w_b` | n1844_ad0116 | North-Western Land Agency, general land agents — office on Kinzie street, east of Dearborn |

No graded value on any of the three MOVED: `graded()` takes the earliest trusted volume
and all three already carried a Fergus 1839 or 1843 trade and street. What a visitor
gains is the 1844 appearance itself — `residents.js` renders `match_status` and the
`holds` chips — and what the measure gains is three rulings that now reach their card
as matches rather than as silences.

**Held, with the clause named.** The 8 that remain contested meet ONE printed name each
and are real ties: `E. Smith` (smith_e_kirby / smith_elded), `J. Coe Clark`
(clark_john_a / clark_john_k), `Chas. Taylor` (taylor_charles / taylor_c),
`William E. Jones` (jones_willard / jones_william). T-0696's discriminator is read on
this file for the first time — `tools/tiebreak.py` imported, not restated, with
`discriminator_rule` and `refused_discriminators` now in the file — and it **names
nobody**: `ties_narrowed_by_a_trade: 0`. Each side carries the block saying why (Taylor:
"two trades that do not agree" — carpenter in 1835 against a fashionable tailor of 1844;
the other three pairs: no trade recorded on either side). A premises and a year stay
refused discriminators for the reasons T-0696 wrote.

**Re-described, and this is a ruling too.** All 3 ambiguous rows meet cards that print
the *identical* proprietor name — `G. S. Hubbard` on forwarding and on the Aetna fire
agency, `George Smith` twice for George Smith & Co., `A. Garrett` on three agencies. The
ambiguity is over WHICH ADVERTISEMENT, not which man, and the file now says which of the
two it is (`ambiguity_is_over`, `proprietor_names_printed`). They are still not matched
and still carry nothing: which card a trade should be read off is exactly what stays
unsettled, and T-0696 forbids resolving a tie into a match.

**Acceptance, measured** (`tools/measure_research_spend.py`, whole town):

| | before | after |
|---|---|---|
| directories, reached | 932 | **938** |
| directories, on a card | 932 of 932 | **938 of 938** |
| directories, **unwritten** | **0** | **0** |
| town total, unwritten | 0 | **0** |

Clause 3 holds: the stretch landed and the column is still 0.

**The pools after this stretch** — the ties are ~196 − 14 = **~182**, of which 8 of this
file's are now ruled-and-held rather than unruled: `fergus_1839` 44+29, `fergus_1843`
40+15, `norris_1844` 19+14, `norris_1844_advertiser` 3+8. **Stretch 3 takes
`norris_1844`'s 33** — the same shape, a volume whose trade line is printed, and the
next-smallest pool. No successor ticket is filed: the succession is on the run that
CLOSES the programme, and the owner's filing rule of 2026-09-10 asks for fewer tickets.
This ticket stays open and is its own cursor.
