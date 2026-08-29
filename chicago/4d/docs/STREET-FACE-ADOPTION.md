# Street-face adoption — what a business does when the paper names a street and nothing narrower

**Status: policy, in force.** Recorded 2026-08-29 for T-0354, on the owner's ruling of the
same day. A later run applies this without re-deciding it; a run that wants to change it
opens a ticket and asks. The implementation is `tools/adopt_street_faces.py`, the derived
table is `data/research/newspapers/street_face_adoptions.json`, the liberty is **L211**,
and `tools/check.sh` re-derives both on every commit.

## The problem this answers

`data/research/newspapers/register_1835.json` reads 221 businesses out of the *Chicago
Democrat* and the *Chicago American* and finds 172 standing on 1 July 1835. It resolves
**52** of them to a building — 29 `enrich_existing`, where the advertisement's anchor names
a roof this project already holds, and 23 `new_building`, where it names a place precise
enough to raise one. The remaining **120** divide into two piles, and neither is a defect
in the register:

*(T-0354 was written on 2026-08-29 against a register that read 24 placed / 49 `street_only`
/ 78 `unplaceable`. Every count in this file is this branch's own re-derivation later the
same day, after T-0380, T-0383, T-0355 and T-0399 moved businesses between the actions and
merged firms the identity layer had been holding apart. The shape of the problem is
unchanged. **None of these numbers is authored** — `python3 tools/adopt_street_faces.py
--report` reprints all of them, so drift shows rather than rots.)*

| pile | count | what the paper gives |
|---|---|---|
| `street_only` | **45** | a platted street and nothing narrower — "the east end of South Water-street" |
| `unplaceable` | **75** | no street this model holds — Flag Creek, "on the road to Ottawa", or no address printed at all |

Without a policy, the papers yield fifty-odd buildings. With one, they yield most of a
town. That is the whole of what is at stake here.

## The ruling

Asked what a business does when the paper names a platted street and nothing narrower, and
offered the three options T-0354 set out — adopt a standing roof, raise a new frontage
record with a conjectural along-street position, or wait for a corner — **the owner chose
adoption, 2026-08-29:**

> Adopt a reconstructed roof already standing on that street face and attach the business
> to it.

So the 45 join the town on the streets their advertisements name, using roofs the
reconstruction programme has already raised there. Nothing new is built and nothing is
promoted.

## The four limits, and they are the whole of the care

**1. A STREET FACE, NEVER A LOT.** The paper's constraint is the face; the lot is the
reconstruction's. A record that says which lot a street-only business stood on has
asserted something no source carries. Every adoption declares `lot: null` and
`claims_lot: false`, and the gate refuses a record that has grown a lot field of any name.

*The plat may still be read.* `tools/fronting_street.py` asks the Thompson lot grid which
tier a footprint stands in, because that is what says which street a roof faces. **Reading
a lot to learn a frontage is not asserting that a business held that lot.** The distinction
matters and is the reason the gate checks field names rather than trusting the derivation.

**2. THE ROOF STAYS `reconstructed`.** Adopting it does not promote the building. The
business is documented; the building under it is not; the card must be able to say both in
one breath. This is the pattern **T-0264/#518 and L205** already set for a documented head
on a reconstructed dwelling — followed, not reinvented. The gate re-reads the adopted
structure's own phase and fails if its confidence has stopped saying `reconstructed`, so a
later pass that promotes one of these roofs cannot do it silently.

**3. THE ALONG-STREET POSITION IS THE RECONSTRUCTION'S, NOT EVIDENCE.** Which roof on the
face a business is given is an allocation, not a reading. Businesses are ranked by evidence
— most printings, then earliest sighting, then id — and paired with that face's free roofs
in id order. Deterministic, so it re-derives; and a statement about nothing, so it claims
nothing. Every record says so in its own note.

**4. ORDER WITHIN A FACE IS NOT A CLAIM.** If two street-only businesses land on one face,
neither is nearer the corner than the other on any authority. Every record carries
`order_is_a_claim: false`.

## What "already standing on that street face" means — the narrow reading, and why

`tools/fronting_street.py` answers the frontage question three ways, and they are three
different claims:

| reading | what it means | adopted? |
|---|---|---|
| `lot front` | the roof's platted lot faces this street. The plat says it. | **yes** |
| `corner side` | the roof ends its tier and abuts this street on the SIDE; its front is the cross street | no |
| `centreline band` | the roof is off the platted grid, within 25 m of this centreline | no |

**Only `lot front` is adopted.** An advertisement that says "on South Water Street" says
where the door is. A roof whose lot faces Randolph does not have a door on Dearborn because
its gable end reaches it, and a 25 m band is a distance rather than an orientation.

This is a real cost and it is reported rather than avoided: it refuses **the whole of
Dearborn Street**, which has eighteen roofs showing it a corner side and not one whose lot
fronts it. `--report` prints both readings side by side, because the reader is owed the
disagreement the decision was made about, and because a later owner ruling that a corner
side is a face has exactly one number to change.

## The five refusals

1. **`not present at the scene date`** — the register already excluded it: contradicted
   before 1 July 1835, or first printed after it.
2. **`the face holds no roof whose lot fronts it`** — Dearborn, La Salle, Canal and North
   Water. These wait for the reading above to widen, or for the reconstruction to raise a
   roof whose lot faces them.
3. **`this face already holds this proprietor`** — the corpus prints one house under more
   than one heading ("Peter Cohen" and "Peter Cohen's store"). One house, one roof per
   face; the better-evidenced heading keeps it. Matched on the **exact** normalised
   proprietor surname set and never on resemblance: whether a firm sharing one partner
   surname with a sole trader is the same house is **T-0338's** open question over
   thirty-one such groups, and a placement pass must not answer it by seating or refusing.
   Variant spellings escape it too, which **T-0405** measures.
4. **`every roof on the face is spoken for`** — the supply ran out. This is a count, not a
   failure, and it is the number this policy exists to produce.
5. **the roof is a named household's dwelling** — a refusal of a ROOF rather than a
   business. A roof `data/residents/` seats a household in is that household's home;
   hanging a documented store on it asserts a relation between two claims nothing supports.
   The documented tradesmen this leaves standing on South Water are **T-0375's**, and this
   policy must not quietly answer that ticket.

## What it moves, measured 2026-08-29

| | |
|---|---|
| `street_only` in the register | **45** |
| adopted a street face | **22** |
| waiting | **23** |
| — no roof whose lot fronts the named street | 16 |
| — this face already holds this proprietor | 6 |
| — every roof on the face is spoken for | 1 |
| `unplaceable`, outside this policy and still open | **75** |

| street face | ads | took | roofs fronting | free | side only | in band |
|---|---|---|---|---|---|---|
| South Water Street | 20 | 14 | 19 | 14 | 0 | 0 |
| Dearborn Street | 11 | 0 | 0 | 0 | 18 | 0 |
| Lake Street | 8 | 7 | 51 | 29 | 0 | 4 |
| La Salle Street | 2 | 0 | 0 | 0 | 8 | 0 |
| North Water Street | 2 | 0 | 0 | 0 | 0 | 1 |
| Canal Street | 1 | 0 | 0 | 0 | 3 | 0 |
| Randolph Street | 1 | 1 | 64 | 50 | 0 | 0 |

**Where the rest wait, named rather than implied:**

- **Dearborn Street (11), La Salle Street (2), Canal Street (1), North Water Street (2).**
  No roof's platted lot faces them. Two remedies, and neither is this policy's to take: a
  ruling that a corner side is a face, or a reconstruction that raises frontage on those
  streets. Two of the eleven — the New York Clothing Store and the Dearborn Street wine
  store — have their own tickets (**T-0385**, **T-0387**) that place them from an anchor
  and do not need this policy at all.
- **South Water Street (6 refused).** Nineteen roofs front it, five are households' homes
  and fourteen are adopted, so six advertisements are short of a roof. Five of those six
  are refused as a second heading of a house already seated; only one is short purely on
  supply. **T-0375** is the ticket that notices South Water's reconstructed roofs are
  all a labourer's, and any roof it adds to that face is a roof this pass will take on its
  next re-derivation, automatically.

## The 75 `unplaceable` are NOT covered, and stay open

The ruling does not reach them and this policy does not extend it. Some are outside the
plat entirely — E. Wentworth's public house on Flag Creek, on the road to Ottawa — and
adopting a roof for them would put a business in a town it never stood in. Some simply
never printed an address. **T-0354's second half is still open**, and the honest answer for
these 75 today is that the corpus records them and the model does not hold them.

## How to spend it

This file and its table are the POLICY and the ALLOCATION. Nothing here writes a card, a
signboard or a frontage — that is **T-0263's** and the seeding tickets'. A pass that spends
an adoption reads `street_face_adoptions.json`, takes `structure_id` and `cites`, and
carries limits 2, 3 and 4 into whatever it writes: the roof stays reconstructed, the
along-street position is not evidence, and the order on a face is not a claim.

**Related:** T-0354 (this) · T-0262 (the register) · T-0263, T-0384–T-0387 (the seeding) ·
T-0375 (South Water's roofs) · T-0338, T-0340, T-0405 (identity) · L205, L211 ·
`docs/PROVENANCE.md` · `docs/LIBERTIES.md`
