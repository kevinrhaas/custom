# Thompson's block numbers, and the one address in the corpus that needed them

**Investigated:** 2026-08-29 · **Re-read block by block:** 2026-09-06 ·
**Tickets:** T-0358, then T-0788 (owner ask) ·
**Record:** none — this is a memo about a *reading* and the count made from it ·
**Data:** `data/traces/thompson_block_numbering.json` (authored),
`data/traces/vectors/thompson_lots.json` (`plat_block_number`, `plat_lot_number`) ·
**Source:** `wright_1834`, through the georeferenced BPL scan
(IIIF `commonwealth:js957744g`); previously through
`data/sources/assets/prefire_views_kevin_2026_08/wright1834_clark_reach_crop.jpeg` ·
**Gate:** `tools/generate_plat_lots.py --check`, in `tools/check.sh`

---

## 0. Superseded in the best way: the numerals were there all along

**2026-09-06, T-0788.** Everything below §§ 1–3 stands as the record of how six blocks got
their numbers from two numerals. **The counting is over.** Twenty-two numerals are now READ off
the sheet, one crop per block, and the four numbers this memo counted — 21, 20, 17, 16 — are
among them. **All four counted values were right.** Nothing moves; what changes is that the
numbers are evidence instead of arithmetic.

**What made it possible was not a better scan — it was asking the georeference for the crop.**
This project is fitted to the BPL copy (`data/traces/gcp/wright_1834_gcps.json`, affine from
eight ground control points, RMS 17.5 m). So for any block the grid holds, the four bounding
street centrelines of `data/streets/1835.json` give a box in local ENU, `tools/wright_px.py`
maps it into the scan's pixel space, and IIIF returns that box at 6×. The block fills the frame.
**Which block carries a numeral stops being a thing the reader decides.** Every entry in
`data/traces/thompson_block_numbering.json` cites the region it was read on, so any reader may
re-open the same rectangle and disagree.

**The run reverses tier by tier, and § 4's refusal was right to refuse it.**

| tier | west → east | direction |
|---|---|---|
| South Water – Lake | 21 20 19 18 **17 16** | falls eastward |
| Lake – Randolph | *28 29* · river · 31 32 33 34 35 36 | **rises** eastward |
| Randolph – Washington | *45 44 43* 42 41 40 · **Public Square** · 38 37 | falls eastward |

*(italic = West Division, west of the South Branch)*

A count carried straight down from the South Water tier would have numbered the Lake tier
backwards. § 4 refused to carry it and said, in terms, that a boustrophedon was one of the
possibilities it could not choose between. It was the one the sheet draws.

**The Public Square carries no numeral.** Wright washes the block pink, rules it into eight lots
like its neighbours, and letters *Public Square* across it where the number would go. So **39 is
the one number in the file that is still counted** — and it is counted across a single block
bracketed by numerals read on both sides: 40 immediately west, 38 immediately east, in a tier
falling by one. One number fits between them. `numeral_on_sheet: false` says so on the record,
and the same reasoning is written onto
`data/reconstruction/1835_reserved_ground.json`, which is where this block's identity is argued.

**Block 16's numeral is on the sheet.** G. Spring's *"LOT No. 7, in block No. 16 … on Lake
street"* no longer rests on a count three blocks long (§ 6). It rests on a numeral in the block's
own frame, on the notice's own "on Lake street", and on the Botsford/Andreas placement of
Haddock's Tavern. The three-way agreement of § 6 is unchanged and is now a check on a reading
rather than a check on arithmetic.

**The lot scheme is read on four blocks, not one.** Blocks 20, 18, 16 and 40 each print
**4 3 2 1** across the north row west to east and **5 6 7 8** across the south row west to east.
Block 40 is in a different tier, whose BLOCK numbering runs the other way — so the lot run is a
property of the block, not of the tier. § 5's grade does not move: the scheme is read, the LINES
it numbers are still the module's, and a number on a conjectural line is conjectural. What the
three extra readings buy is that the scheme is no longer a one-block reading.

**Not every block carries eight lots.** The West Division block west of block 28 prints
`1 4 5 8 9` down its side — ten lots, two rows of five, numerals written across a horizontal
alley. No West Division block is emitted by the generator today, so nothing is mis-numbered;
it is recorded in `lot_numbering.ten_lot_blocks` so that the day one is, this is found first.

**What is still refused, and why it is the same refusal.** Twenty-four of fifty-eight blocks are
held. The Washington–Madison tier, the North Division and the West Division beyond Clinton are
refused because the method is *cut the crop from committed street lines*, and the committed
street grid does not reach them. A numeral found by eye instead, on paper that stretches 3.7%
anisotropically, is a numeral placed by the reader — the mistake this file was rebuilt to stop
making. Block **30** is refused separately: the Lake tier reads 29 on the west bank and 31 on the
first block east of the branch, and the ground between them is water, so 30 is somewhere not yet
read and nothing here says where.

**One cell is two blocks.** The grid's `blk_randolph_canal` runs Canal Street to Market Street,
243 m, and spans **44** on the west bank and **43** on the east with the river between them. It
therefore takes NO number — one number on a cell that is two blocks is a claim the sheet does not
make — and both readings are parked in `blocks_not_in_the_grid`, waiting for the day the grid has
an id for them.

---

## 1. What was missing

G. Spring's For-Sale notice ran in the *Chicago Democrat* six times between 1834-06-18 and
1834-11-19 and is **the only lot-and-block address in the whole newspaper corpus**:

> For Sale, **LOT No. 7, in block No. 16, one lot east of Haddock's Tavern, on Lake street**, in
> the town of Chicago. There is on said lot a large Dwelling-House and fine well. For terms
> enquire of G. SPRING.

Three readings had recorded that this was the most placeable statement the corpus makes and
that placing it was somebody else's job. It was nobody's, because nothing committed carried
Thompson's block NUMBERING: `data/traces/vectors/thompson_lots.json` keys its nineteen blocks
on their bounding streets, and no record in `data/sources/` numbered one. "Block No. 16"
resolved to nothing, and so did "Lot No. 7" inside it.

## 2. The evidence is two numerals, and it used to be quoted as three

The project owner's crop of Wright's 1834 sheet at the Clark reach carries block numbers. Both
memos that cite it — `clark_reach_bulge_1834.md` § 8 and `thompson_plat_grid.md` § 4 — said it
reads "block numbers 19, 18 and 17".

**Re-read at full resolution it carries 19 and 18.** The file is 639 × 719 px and the map region
inside it ends at block 18's east edge; there is no third block on the sheet. The asset's own
README, written when it was supplied, describes exactly two ("a narrow sinuous line dropping
south off the bank between numbered blocks 19 and 18"), so the third arrived somewhere in the
retelling. Both memos are corrected here.

Nothing that was built on the crop moves. Both memos used the numbers to establish the step and
the direction of the run, and two consecutive numerals do that as well as three do. What changes
is the size of the evidence base, which is the thing a later reader needs in order to know how
far it can be pushed — and § 4 pushes it three blocks.

## 3. What the two numerals fix

**The step is one and the direction falls eastward.** 19 stands west of 18.

**The run is along the tier, not down a column.** Two blocks side by side in one row differ by
one. A column-major numbering would separate them by the number of rows.

**Which blocks they are, at ±20 m.** The crop shows a narrow sinuous watercourse drawn down the
street between the two blocks, with the platted **80** written in it. That stream is already
traced and committed: `clark_reach_bulge_1834.md` § 4 measured its mouth at local
**E +462 … +469**, and established — against the reading that it was the river bulge — that the
committed trace runs up the inside of its own ink line there. La Salle Street's committed
centreline is at **E +451.3**, so its corridor spans E +439.1 … +463.5 and the stream is drawn
in the east half of it. The next candidates are Wells at E +329.3, 122 m west, and Clark at
E +574.7, 123 m east.

So the crop's two blocks are the **Wells–La Salle** block (19) and the **La Salle–Clark** block
(18) of the tier fronting South Water Street on the north and Lake Street on the south. That
step is an inference and is graded as one; it is not a close call.

## 4. Counting along the tier

| block | id | number | numeral, 2026-08-29 | numeral, 2026-09-06 |
|---|---|---:|---|---|
| Market–Franklin | `blk_south_water_market` | 21 | counted (2 west) | **read** |
| Franklin–Wells | `blk_south_water_franklin` | 20 | counted (1 west) | **read** |
| Wells–La Salle | `blk_south_water_wells` | **19** | **read** | **read** |
| La Salle–Clark | `blk_south_water_lasalle` | **18** | **read** | **read** |
| Clark–Dearborn | `blk_south_water_clark` | 17 | counted (2 east) | **read** |
| Dearborn–State | `blk_south_water_dearborn` | **16** | counted (3 east) | **read** |

The last column is § 0's re-reading, kept beside the count so the two can be compared. **Every
counted value was right**, which is worth exactly as much as it is worth: four out of four is a
good record for a step of one along a row, and it is not a reason to trust a count over a
reading anywhere else.

`blk_south_water_market` is not in the grid — South Water's committed centreline stops 24 m short
of it (`thompson_plat_grid.md` § 6) — so its number is stamped onto the omission, where the two
facts sit together instead of one contradicting the other's absence.

**Nothing else is numbered, and the refusals are the load-bearing part.** The crop fixes the
direction of the run *inside* a row and says nothing about how it passes from one row to the
next. A boustrophedon that turns back west, a run that restarts at the west end of every tier,
and a run that descends a column all reproduce 19 beside 18 and give the Lake–Randolph and
Randolph–Washington tiers different numbers. The West Division is refused for the same reason
one step larger, and the North Division has no blocks to number. Where the tier's own run begins
and ends is refused too: only offsets from the two read numerals are claimed here.

**No modern plat reprint was consulted**, and the authored record says so in terms. If one
agrees, that is a corroboration somebody may fetch and cite; if it disagrees, it is evidence.
Neither may be quietly substituted for this reading.

## 5. The lot scheme, and why its number is conjectural wherever it lands

Block 18's north row is set **4 3 2** west to east and its south row **5 6 7**, the fourth of
each falling outside the crop. That is a counter-clockwise run from the block's north-east
corner: **1–4 east to west along the north row, 5–8 west to east along the south row.**

The scheme is emitted only inside a numbered block, and it is graded `conjectural` *everywhere*,
including on block 18 itself. Four lots to a face is a reading of this one block
(`thompson_plat_grid.md` § 4); the lot lines in `thompson_lots.json` are the module divided into
a block and carry `conjectural` for that reason. **A number put on a line no sheet drew is
conjectural whatever the number's own provenance.** What the scheme is good for is reading a
documented address onto the grid. It is not evidence of where a lot line ran.

## 6. The check that was not built into the count

Counting east three blocks from 19 puts **block 16 on Dearborn–State**. Three statements made
independently of each other, and of this count, land on the same ground.

- **The notice itself.** "block No. 16 … **on Lake street**". Block 16 as counted is bounded south
  by Lake Street, and under the scheme in § 5 its Lake frontage is the row numbered 5 to 8.
  A count that had landed one block out would have put block 16 on a tier Lake Street does not
  bound, or on the wrong side of it.
- **Its own neighbour clause.** "LOT No. 7 … **one lot east of Haddock's Tavern**". Lot 7 is the
  third lot east of the Dearborn corner, so Haddock's is the second — not the corner lot.
- **A placement argued before this file existed.** Haddock's Tavern is the Mansion House
  (`data/structures/mansion_house.json`, and T-0324 for the succession). Andreas has it "on Lake
  near Dearborn"; T-0324 read J. K. Botsford's two advertisements — "next door to Graves' Tavern"
  and "Corner of Dearborn and Lake-sts." — as one frontage on the corner lot, and concluded the
  tavern stood **on the second lot from Dearborn rather than on the corner**
  (`botsford_graves_1834.md`). That is lot 6, one lot west of lot 7.

Three readings, three sources, one block face. **The arithmetic is still arithmetic** and every
number in § 4 stays `inferred`; what the agreement buys is that nothing independent contradicts
it, on the one block where anything independent could.

The other four counted numbers have no such check. 17, 20 and 21 rest on the step alone, and the
authored record says so on each of them rather than letting block 16's corroboration wash over
the tier.

## 7. What is now measurable, and is deliberately not done here

The Lake Street row of block 16 as this dataset stands today:

| lot | what stands on it | centre |
|---:|---|---|
| 5 | `mansion_house` | E +718.2, N −96.1 |
| 6 | `recon_1835_blk_south_water_dearborn_d2_04` — an anonymous reconstructed roof | E +750.9, N −94.9 |
| 7 | `recon_1835_blk_south_water_dearborn_h1_03` — an anonymous reconstructed roof | E +773.3, N −93.3 |

So the address resolves, and it resolves onto two consequences this ticket does not act on:

1. **The Mansion House stands on lot 5 and the corpus puts it on lot 6.** Its committed position
   was set with its west face on the Dearborn frontage — the corner lot — from Andreas's "on
   Lake near Dearborn". The gap is **24.2 m, one lot, eastward**, and it is *inside the
   uncertainty that record already declares* ("the house may have stood one or two lots further
   east … read the along-street position as good to about plus or minus 20 m on top of the
   georeference"). T-0324 reached the same conclusion from Botsford and deliberately did not
   move the record. Nothing here changes that judgement; what changes is that the discrepancy is
   now a number instead of a sentence.
2. **Lot 7 carried a large dwelling-house and a fine well**, and an anonymous count-unit roof
   stands on it. Standing Spring's documented house there is a visible change and a separate
   piece of work, filed as its own ticket.

Neither is smuggled in here. Moving a committed building on the strength of an inference made in
the same commit that authored the inference is how a reconstruction talks itself into precision
it has not paid for.

## 8. What this is not

- **Not rendered.** The grid is a dataset layer and the walkthrough does not draw it, so nothing
  here adds to `docs/LIBERTIES.md` — a liberty records something invented that a visitor is
  looking at. Nothing was invented in any case: every number here is counted from two numerals
  on a survey sheet, and everything that could not be counted is refused in writing.
- **Not a cadastre.** No lot is owned and no lot is claimed to be the lot a particular building
  stood on. § 7 is a report of where this dataset's own buildings fall, not a title.
- **Not the whole plat.** Twenty-four blocks of fifty-eight — six when this memo was written,
  and the other eighteen read in § 0. The rest are refused there, by name.
