---
id: T-1448
title: Mint the staffing shortfall to the model's typical band: the 105 reconstructed hands 96 houses are still short, written as a stage of the resident reconstruction programme into cards of their own, each carrying its house, its role and where it slept, and nothing already committed written to
state: blocked-owner
epic: META
requested_by: owner
seen: true
effort: S
legacy_id: null
parent: T-1434
opened: 2026-09-20
closed: null
pr: null
claimed_by: run 9/20/2026, 7:46:36 AM CT
blocked_on: The shops are short 129 hands and the order book has 109 places left, all 129 wanted are men where 40 of the 109 are women's, and 24 of the hands are boys of 12-18 in a band the book has drawn out. Minting to the typical band means one of three things and all three change what the town is: re-cut the book (T-1166), come down toward the model's own count_low of 65, or let the houses stand short and have the business card say so. Numbers for all three are in data/reconstruction/1835_staffing_mint_order.json.
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/35511233651
---

Mint the staffing shortfall to the model's typical band: the 105 reconstructed hands 96 houses are still short, written as a stage of the resident reconstruction programme into cards of their own, each carrying its house, its role and where it slept, and nothing already committed written to.

Piece 1 of 2 of **T-1434 — Mint the staffing shortfall to the model's typical band and close the join: new reconstructed staff where a business is still short, every working-age person a workplace or an explicit not_employed reason, the order book's employment buckets filled and the business card printing its people**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

1. The hands the staffing model's TYPICAL band wants and no house has are derived per
   house and per role row, from committed files only, with `count_low` and `count_high`
   carried beside every row so the other answers can be priced.
2. A class that names the same role twice — the journeyman printer and the printer's
   boy — has the hands standing in the house allotted across both rows before either
   is called short. A hand is never counted against two rows.
3. What the reconstruction order book can pay for is read from the book's own
   outstanding `.../trade` buckets, and a slot pays for a hand only where the two
   vocabularies OVERLAP in years and the role's sex rule allows that sex.
4. Nothing is minted, no bucket's `filled` moves, no `fills` row is added and no card
   or business record is written to.
5. `--check` re-derives the order byte for byte and is in `tools/check.sh`;
   `--self-test` fires seven assertions.

**What it demonstrated — and why the mint did not run.** The shops want **129 hands**
over **88 houses**. The order book — the only quota this project holds, and the one
whose `no_bucket_overfilled` invariant refuses a stage that draws past it — has **109
outstanding `.../trade` slots**. They do not meet, and they miss in three separate ways:

- **On the count.** 129 wanted against 109 outstanding: 20 short before any axis is
  looked at.
- **On the sex.** Every one of the 129 is a man or a role the model calls
  predominantly male. 40 of the book's 109 slots are women's and cannot be spent here
  at all.
- **On the age.** 24 of the hands are boys of twelve to eighteen. The book's 10–19
  trade buckets are drawn out; there is no slot a shop boy could be minted into.

Spend the book greedily in the stated order and it pays for **55** of the 129. The
other **74** have nowhere to come from. Every outstanding slot is a `lodging/trade`
bucket owned by **T-1175**, so even the 55 would be spent out of another stage's quota.

Minting to the typical band therefore means one of three things, and all three change
what the town IS: re-cut the book (T-1166), come down off the typical band toward the
model's own `count_low` of 65, or let the houses stand short and have the business card
say so. `data/reconstruction/1835_staffing_mint_order.json` carries the numbers for all
three. **Blocked on the owner.**

**Findings handed on.**
- T-1449 ("close the join and print it") cannot finish either: there are no minted
  hands to put on `staff[]`. Its other clause — every working-age person a workplace or
  an explicit `not_employed` reason — does not depend on the mint.
- T-1433's 62 unseatable domestics are NOT in this order. Their taverns are full to the
  model's HIGH band, so they are a town owed more lodging houses, not a house short of
  hands.
