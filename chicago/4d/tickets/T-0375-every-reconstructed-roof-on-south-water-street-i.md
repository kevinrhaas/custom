---
id: T-0375
title: Every reconstructed roof on South Water Street is a labourer's, so five documented tradesmen the papers put there have nowhere to stand
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

Every reconstructed roof on South Water Street is a labourer's, so five documented tradesmen the papers put there have nowhere to stand.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

Found while landing T-0367, which gave the deal a way to ask which street a
reconstructed roof fronts. Six documented tradesmen now reach that test and all
six are turned back by the same fact.

**Five roofs in this town front South Water Street and every one of them is a
labourer's.** So D. Graves the baker, A. Filer and Rockwell the joiners, and
L. W. Montgomery and John Holbrook the shoemakers — all placed on South Water by
their own advertisements — have no roof of their trade on the street the paper
names. J. B. Tuttle wants Dearborn, where the grocers have none either, and
J. H. Barnard wants Lake, where the town's one physician's roof is not.

`python3 tools/replace_invented_residents.py --report` prints the six with the
street each wanted and what his trade's roofs front instead;
`python3 tools/fronting_street.py` prints the frontage of every reconstructed
dwelling.

This is a fact about where the occupation census put the trades, not about the
evidence. The census is calibrated on counts per division and never asked which
street a roof would stand on, so the business streets drew labourers and the
tradesmen drew the inside of blocks.

**Acceptance:** (one demonstration, never weakened to pass)

- Either the trade a reconstructed roof carries can be argued against the street
  it fronts — a shoemaker's roof on South Water rather than a labourer's — with
  the argument recorded and the occupation census's per-division counts unchanged;
  or the answer is that it cannot, stated with the reason, and this ticket closes
  as refuted with the six refusals standing.
- If roofs do change trade, the before → after runs through
  `tools/replace_invented_residents.py --check` and names every documented man it
  seats.
- No confidence is upgraded and no roof moves to reach the result.

Related: **T-0367** (the frontage derivation), **T-0366**/**T-0264** (the deal),
**T-0263** and **T-0306** (which place the BUSINESSES on these same streets).
