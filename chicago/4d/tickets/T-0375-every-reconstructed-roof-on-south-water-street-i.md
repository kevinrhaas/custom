---
id: T-0375
title: Every reconstructed roof on South Water Street is a labourer's, so five documented tradesmen the papers put there have nowhere to stand
state: claimed
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: run 8/29/2026, 2:32:19 PM CT
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

---

## THE ANSWER, 2026-08-29 — REFUTED, and the refusal it rests on now tells the truth

**It cannot, and the ticket's premise has been overtaken by a merge that landed the
same day it was filed.** Both halves are measured below on an unmodified `dev`; nothing
here is asserted.

### 1. Four of the six men are standing on the street the papers name — as storefronts

`docs/STREET-FACE-ADOPTION.md` is the owner's ruling of 2026-08-29 (T-0354, #551/#553):
a business the paper puts on a street and nothing narrower adopts a reconstructed roof
whose platted lot fronts that street. `python3 tools/adopt_street_faces.py --report`
prints the result, and four of this ticket's six tradesmen are in it:

| the man | stands on South Water Street as | roof |
|---|---|---|
| D. Graves, baker | `D. Graves` | `recon_1835_blk_south_water_dearborn_c3_01` |
| A. Filer, joiner | `A. Filer & Co.` | `recon_1835_blk_south_water_wells_a3_08` |
| L. W. Montgomery, shoemaker | `L. W. Montgomery, boot and shoe maker` | `recon_1835_blk_south_water_dearborn_a3_06` |
| John Holbrook, shoemaker | `John Holbrook` | `recon_1835_blk_south_water_lasalle_d5_01` |

So "have nowhere to stand" was never quite what refusal 8 meant, and after 2026-08-29 it
is plainly false. What these men are short of in `tools/replace_invented_residents.py` is
a DWELLING of their trade on that street, which is a narrower and true statement. The two
who are short of anything at all are **Rockwell** (joiner, South Water — the corpus
carries no business under that surname for the adoption pass to seat) and **J. B. Tuttle**
(grocer, Dearborn Street — where no roof's platted lot fronts the street at all, which is
STREET-FACE-ADOPTION.md's own reported cost).

### 2. And the household route is now barred rather than merely empty

Seven reconstructed dwellings front South Water Street with no household in them, and two
are of the shoemakers' own family band (`recon_1835_blk_south_water_franklin_d4_02` and
`recon_1835_blk_south_water_lasalle_d4_02`, both D4, both south division — so all three of
the adoption tests in the inferred-household programme's method rule 6 pass, and the
per-division counts would not move). That is the change this ticket asked about, and it
was simulated rather than argued: `adopt_street_faces.derive()` re-run with those two roofs
marked as households' homes.

| | before | after |
|---|---:|---:|
| street-face adoptions, whole town | 24 | **22** |
| adopted on South Water Street | 14 | **12** |
| free roofs fronting South Water | 14 | **12** |
| refused `every roof on the face is spoken for` | 3 | **5** |

The cost is exactly one-for-one, because the face is already exhausted — 19 roofs front
South Water, five are households' homes and the pass has taken all fourteen it was
allowed. The two documented businesses evicted are **`A. Garrett`** and **`the New Store at
the corner of Water and Clark streets`**. Worse than the arithmetic: the men the seats
would go to are L. W. Montgomery and John Holbrook, who would then stand on South Water
Street TWICE — once as a storefront and once as a household head. Trading two documented
businesses for two duplicate seatings is not a demonstration; it is a regression.

### 3. The remaining trade is a claim about means, and no source carries it

The only way to put a tradesman's household on South Water without taking a roof from the
business pool is to trade one of the five D1 log cabins the labourers hold there for a
shoemaker's D4 two-room cottage. **The family band IS the claim** — D1 is the roughest
dwelling in the schedule and D4 a two-room frame cottage — so a shoemaker in the cabin and
a labourer in the cottage are two statements about those men's means that nothing in the
corpus supports, and the acceptance above forbids reaching the result that way. Refused.

### What changed in this PR

No record, roof, coordinate or confidence moves. `tools/replace_invented_residents.py`
reads `data/research/newspapers/street_face_adoptions.json` before it speaks: refusal 8
now names the adoption when there is one, so it can never again be read as saying the man
is absent from the town. The module docstring, which asserted in prose that these men
"have nowhere on it to go", says what is true instead.

**The six refusals stand, and three of the five that reach refusal 8 now say where the man
actually is** (D. Graves is refused earlier, under rule 5, and never reaches it).
