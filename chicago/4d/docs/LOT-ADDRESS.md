# The lot-and-block address

*Policy. Written for T-0423, 2026-09-03. The tool is `tools/lot_addresses.py`, the ledger
is `data/research/newspapers/lot_addresses.json`, the liberty is **L216**, and the gate is
two steps in `tools/check.sh`.*

## The three ways a newspaper places a building, and this is the third

A Chicago paper of 1834 places a building in one of three grammars, and this project now
answers each of them differently because they are not the same claim.

| the paper says | what it constrains | the policy |
|---|---|---|
| a platted street and nothing narrower | a **face** | `docs/STREET-FACE-ADOPTION.md`, L212 |
| a count of doors off a named corner | a **position along a face**, and no lot | `docs/CORNER-ORDINAL.md`, L215 |
| a lot and a block | the **plat's own unit** | this document, L216 |

The third is the strongest statement the corpus makes and it is also the rarest: there is
**one** of it. G. Spring's For-Sale notice ran in the *Chicago Democrat* six times between
1834-06-18 and 1834-11-19 —

> For Sale, **LOT No. 7, in block No. 16, one lot east of Haddock's Tavern, on Lake
> street**, in the town of Chicago. There is on said lot a large **Dwelling-House and fine
> well**.

— and four of those printings carry the words legibly. T-0358 committed the Thompson
plat's block numbering so that this sentence could resolve to ground. It resolved to a
**polygon** and stopped there: the roof standing on that polygon went on carding as *"A
vacant one-room frame cottage"*, which is a claim about absence made over the top of a
source saying a house was there. This policy is the other half of T-0358.

## Authored, derived, and where the line falls

The **address** is authored. `data/research/newspapers/lot_addresses.json` carries the
printed words, the printings they are read from, what the notice says stood on the lot, and
who the advertiser was. It names no structure and no coordinate.

Everything from there is **derived**, by `tools/lot_addresses.py`:

1. **block number → block.** Through `data/traces/thompson_block_numbering.json`. The
   ledger states the block it believes it resolves to and the tool refuses a ledger that
   disagrees with the committed numbering — a stale copy of a reading that moved is not a
   second opinion.
2. **lot number → polygon.** Through `data/traces/vectors/thompson_lots.json`, whose lots
   carry `plat_lot_number` from that same committed numbering.
3. **polygon → roof.** The roof whose footprint **centroid** falls inside the lot.
   **Exactly one, or the address is refused.** An address landing on two roofs has placed
   neither; one landing on none has nothing to name. (Centroid, not the record's position:
   a record's origin is a corner of its own footprint frame, and on a 26 m lot the
   difference between a corner and a centre answers the question wrong at a lot line.)

## The grade does not rise, and the chain is why

The words are **read**. The block number is **`inferred`** — three blocks counted east of
the single numeral the Wright sheet shows. The lot number is **`conjectural`** twice over:
four lots to a block face is a reading of one block, the lot lines it numbers are the plat
module's and are drawn from no sheet, and the counter-clockwise scheme itself was read off
block 18.

A chain is as strong as its weakest link, so **the seating is graded at the bottom tier** —
exactly where the roof already stood. `confidence` is `const: "reconstructed"` in the
schema, the tool refuses any other value, and `--check` re-reads the structure's own phase
and fails if a documented address has quietly promoted a reconstructed roof.

## What a seating writes, and what it may not

It writes **one block** — `lot_address` on the structure record — and nothing else. It
touches no coordinate, no footprint, no form value, and **not even the record's
`function`**. That last restraint is not fussiness: `function.value` is what the dooryard,
fence, planting and signboard generators read to decide what stands in a yard, so a
documented address rewriting it would have moved fabric all over the lot in order to say a
name.

Four refusals, each an assertion in `--self-test` rather than a promise:

- **It may not move, resize or re-form the roof.** The house the notice calls LARGE is not
  made large. The fabric under the address is the 665-roof programme's D3 count-unit, a
  5.36 × 6.38 m one-room cottage, and the ledger says so in as many words. Whether a
  documented "large dwelling-house" should be re-dealt a larger family is a second
  demonstration and has its own ticket.
- **It may not promote the roof.**
- **It may not seat a person.** The advertiser is the man to apply to for terms and nothing
  else, and the ledger's `is_the_occupant` and `is_the_owner` are `false` and refused if
  they are not. This house is *not* "G. Spring's": the same G. Spring is the attorney the
  papers put second door west of Franklin and South Water, and T-0412 is the same trap read
  from the other side — a building offered FOR SALE must not mint a placement on its vendor.
- **It may not seat two addresses on one roof, or one address on two roofs.**

## What it does not draw

The notice's second structure is **a fine well**, documented as plainly as the house. It is
not drawn, and the record says why: the town has no well — no archetype, no committed
structure, no yard record — so drawing this one would raise a new kind of object for the
whole scene rather than place a known one, and it would be the only well in Chicago. That
is filed as its own ticket. **A documented feature that is absent is stated, not omitted.**

## What a visitor sees

`tools/compile_scene.py` carries the address into the sidecar as an attribute row, so it
renders with the same confidence chip, sources and reasoning as every other thing the card
says, and `renderers/web/js/display-name.js` titles the building from it. A documented
address outranks a composed vacancy and ranks below a household — a house the town knew by
the family in it is known by the family in it. The production identity is not deleted:
`Reconstructed D3 one-room frame cottage #03` still prints under the title as the reference
line, and search takes both.
