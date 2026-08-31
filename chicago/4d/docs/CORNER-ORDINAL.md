# The ordinal off a corner — what a business does when the paper counts doors

**Status: policy, in force.** Recorded 2026-08-30 for T-0384, on the owner's ruling of the
same day. A later run applies this without re-deciding it; a run that wants to change it
opens a ticket and asks. The implementation is the `corner_ordinal` anchor kind in
`tools/compile_register.py`, the transparency clause is `no_lot_claim_ids` in
`tools/plat_occupancy.py`, the liberty is **L215**, and `tools/check.sh` re-derives the
register and runs `tools/measure_corner_ordinals.py` on every commit.

## The question, and it was one line

> **Does *"one door from Dearborn street"* place a store, or is it a street and nothing
> narrower?**

It mattered because the two answers put John Holbrook's clothing store in two different
places, and one of them was nowhere. Read as a street, the address is a `street_only`
business and falls to `docs/STREET-FACE-ADOPTION.md`: it adopts a reconstructed roof
already standing on that face, nothing is built, and **South Water Street has no free roof
to adopt** — nineteen front it, five are a named household's dwelling, five are yard
buildings and nine are already adopted by better-evidenced businesses. Holbrook would have
waited on T-0375 indefinitely. Read as an ordinal, the phrase counts doors from a crossing
the plat fixes, which is a position along the face, and the store can be stood at it.

## The ruling

> **Read it as an ordinal off the corner.**

So *"one door from Dearborn"* is a NARROWER claim than *"on South Water Street"*. It counts
doors from a named corner, which is a position along a face and not merely the face.

**The blast radius was measured before the ruling, not after.** Nothing else in the corpus
turns on it: zero register businesses anchor on any of the five documented buildings holding
a business-front lot. The ruling corrects one anchor and does not cascade.

## The one limit, and it is the whole of the care

**AN ORDINAL IS NOT A LOT.** "One door from the corner" fixes a position in a sequence
along a face; it does not name a platted lot and may not claim one. This is the same limit
the street-face ruling carries, arrived at from the other direction — there the paper gives
a face and no position, here it gives a position and no lot — and it is enforced the same
way, in fields rather than in prose:

- the structure record carries a `lot_claim` block: `claims_lot: false`, `lot: null`,
  `placement_rule: "corner_ordinal"`, and a note saying why. The schema permits no other
  value for either of the first two.
- `tools/plat_occupancy.no_lot_claim_ids` reads that block, and such a record is **not a
  holder of the lot** for the business-front clause of 2026-08-27. It neither entitles the
  lot it physically stands on nor exhausts it; the roof schedule and the block generator
  see the lot exactly as they would if the record named a different street.
- `occupied_lots` still counts it. The building stands where it stands, is a roof of its
  block, and is subtracted from that block's headroom like any other. Only the entitlement
  question reads the declaration.
- **nothing physical is relaxed.** The footprint still may not overlap another, still
  clears every neighbour by the separation gate's three metres, still stands inside the
  block's own lot lines by `LOT_MARGIN_M`, and still may not lap a platted corridor.

The transparency runs ONE WAY on purpose. A lot held only by no-lot-claim records has no
documented store entitling it, so it reads as taken and the run is not dealt it — the
cautious answer, costing nothing today because no such lot exists. Freeing it would be a
second ruling, about ground rather than about evidence, and this policy does not make it.

## THE COUNT IS EVIDENCE AND THE METRES ARE NOT

The owner's ruling says it in terms, and it is the sentence a later run is most likely to
forget. How far one door is from the corner is a **reconstruction**. The rule that produced
the number is **L215's door-gap rule**: a front placed one door along from a named
neighbour is set **3.048 m (10 ft) clear of that neighbour's wall**, measured along the
face — because "one door from" describes a neighbouring front and not a party wall, so the
gap may not be zero, and because ten feet is the smallest gap that still reads as two
buildings rather than one at walking distance. It is a convention with two reasons and no
source, it is declared at L215, and a second ordinal placement anywhere in the corpus turns
it from a convention used once into a rule that has to be argued.

The DIRECTION is the same kind of thing where the paper omits it. Holbrook's card gives a
count and no side of Dearborn; east is read from three of this face's own printed addresses
agreeing when read eastward and closing on nothing when read westward. That is a reading of
sources against each other, which is why the position is graded `inferred`; the fork is
recorded on the record and at L215 rather than resolved silently.

## How a reading pass gets this for free

**The vocabulary is derived, not hand-tagged, and that is the point.** A reading pass writes
what it always wrote — `class: relative`, an `anchor` naming the cross street, and an
`offset_normalized` carrying the phrase — and `tools/compile_register.resolve_anchor` reads
the ordinal out of it. Nobody decides anything twice, and a claim written before this policy
existed is read under it the moment the register recompiles.

`ordinal_off_a_corner` runs **after** the landmark resolutions and **before** the `street`
fallback, which is the whole of its precedence, and three things must hold:

1. the offset counts DOORS, in a word this project translates to a number. *"a few doors
   below Messrs. Newberry & Dole"* names no count and is refused — `few` is not a number,
   and a placement that cannot say how many doors is a reach of the street.
2. its reference resolves to exactly ONE platted street, suffix required — the same test
   the `street` kind uses, so a phrase that could not have been read as a street cannot be
   read as an ordinal off one either.
3. the business's OWN street is platted and is a different street. *"two doors north of Lake
   street"* said by a house on Lake Street names no crossing.

An ordinal off a BUILDING — *"first door west of Messrs. Jones, King & Co."* — is untouched:
it resolves earlier, as a landmark hop, and was always placed by the building it names.

The anchor that comes back names the crossing in `streets`, as `corner` does, and the reading
itself in `ordinal` — `{count, direction, along, from_street, phrase}` — so a gate reads the
count without parsing prose. The action is `new_building`, the same action a corner gets.

## What it reaches today — swept by the gate, not estimated

`tools/measure_corner_ordinals.py` sweeps every extraction file for the `n doors` forms
this corpus prints and reports what the reading does with each, so the numbers below move
when a reading pass adds one rather than going stale. As of 2026-08-30, over 86 extraction
files:

| | |
|---|---|
| claims carrying an *n doors* phrase | **28** |
| — whose phrase also names a corner of two streets, which resolves first | **5** |
| — a landmark hop, or naming no platted street | **20** |
| — readable as an ordinal off a corner | **3** |
| register businesses reading `corner_ordinal` at the scene date | **1** |

Three readable claims, two businesses, and only one of them reaches the register:

- **John Holbrook**, Democrat 1835-06-10 c010, *"one door from Dearborn street"* — the
  store this ruling was made for. Its other printing, American 1835-06-13 c012, is NOT
  readable: the transcription cuts the cross street to *"De[arborn]"* and a bracketed
  supply is not a street name, so the phrase resolves to no platted street. The Democrat's
  printing is what carries the placement, and it also corroborates the street word the
  American's column cut away.
- **Clark, Filer & Co.**, Democrat 1834-06-18 c009 and 1834-07-02 c014, *"their ware house
  on South water St. five [doors east] of the corner [of Randolph st.]"* — readable at
  claim level and **invisible to the register**, because the gazetteer's LIVE placement for
  that house is `class: none` with a null street while three of its printings carry the
  anchor. That is a gazetteer fault and not a fault of this policy; **T-0440** carries it.

So the honest count of what the ruling moves today is **one store**, which is what the
measurement taken before the ruling said it would be — and one more waits on a fix
somewhere else.

**Related:** `docs/STREET-FACE-ADOPTION.md` (the policy for the other half of the problem) ·
**L215** (the metres, the side of Dearborn, and the invented building) · T-0384 (the ruling) ·
T-0306 (the American's six storefronts) · T-0375 (the South Water roofs an adoption wanted).
