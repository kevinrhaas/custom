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

### The two streets may come from two fields, and this is the limit on that (T-0771)

Test 3 above joins a street the OFFSET names to a street the placement's own `street` field
names, and that pairing is **ruled legitimate**. It has to be said out loud, because a corner
is otherwise something the papers write in one breath — *"corner of Dearborn and Lake"* — and
this reading builds one out of two halves that are never printed together. Clark, Filer & Co.
prints *"their ware house on South water St. five doors east of the corner of Randolph st."*
and the reading pass files it as it always files an address: `anchor: "the corner of Randolph
st."`, `street: "South Water Street"`. One street in the anchor, the other in the placement.

**The limit is that the second street must be the placement's own DECLARED field, and nothing
else.** `street` is what the reading pass wrote down as the street this business stands on,
taken from the same sentence that carries the offset — not a street inferred from a neighbour,
not one carried over from another printing, and not one guessed from where the house is
thought to be. So the crossing is still read entirely out of one claim, and a pairing this
reading makes is a pairing the paper made. Where the placement declares no street, or declares
one the plat does not hold, or declares the same street the offset names, there is no crossing
and the phrase falls through to the `street` fallback exactly as before.

**The population was measured, not assumed** — T-0771, over 86 extraction files: **six** claims
across **four** businesses carry an anchor naming one platted street while the placement's
`street` names a different one AND are not read as a corner first. Three resolve as
`corner_ordinal` today (Holbrook's Democrat printing; Clark, Filer's two intact printings).
Two are refused for want of ink, not for want of a rule — Holbrook's American printing cuts the
street to *"De[arborn]"*, and the Democrat's torn column of 1834-06-11 cuts the count. The
sixth is a landmark hop that carries no *n doors* phrase at all: *"in a building on Randolph
Street, nearly in rear of the Presbyterian Church, between Clark and Dearborn streets"*, where
the two streets are a description of where the CHURCH stands, not a crossing to count from.
So the pairing reaches four claims and invents nothing.

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
| register businesses reading `corner_ordinal` at the scene date | **2** |

Three readable claims and two businesses, and since T-0771 **both** reach the register:

- **John Holbrook**, Democrat 1835-06-10 c010, *"one door from Dearborn street"* — the
  store this ruling was made for. Its other printing, American 1835-06-13 c012, is NOT
  readable: the transcription cuts the cross street to *"De[arborn]"* and a bracketed
  supply is not a street name, so the phrase resolves to no platted street. The Democrat's
  printing is what carries the placement, and it also corroborates the street word the
  American's column cut away.
- **Clark, Filer & Co.**, Democrat 1834-06-18 c009 and 1834-07-02 c014, *"their ware house
  on South water St. five doors east of the corner of Randolph st."* — the register reads
  it as `corner_ordinal` and its action is `new_building`, so the warehouse now waits on a
  seeding run rather than on a fix. It sat readable and unspent for a week, and **the reason
  was not the one the finding named**: the ticket supposed that nothing joined the anchor's
  Randolph Street to the placement's South Water Street, and that pairing has in fact worked
  since the ruling shipped — test 3 above IS it. What the register actually held was a torn
  transcription. Three printings carry this anchor; the gazetteer kept the earliest, and the
  earliest is the Democrat of 1834-06-11, whose column is cut through the address and whose
  reading pass supplied it as *"five [doors east] of the corner [of Randolph st.]"*.
  `ORDINAL_DOOR` cannot count doors across a bracket — for the same reason the American's
  *"De[arborn]"* is not a street name — so the phrase fell through to the `street` fallback
  and the warehouse read as a reach of Randolph Street.

  **The rule this produced is one line and it is not about ordinals at all.** Among printings
  the gazetteer has already declared to be ONE reading — same class, same anchor —
  **a supply gives way to ink**: a transcription carrying an editorial bracket yields to a
  sibling printing that sets the same reading plainly, and the date decides only between
  printings of equal standing. It is `compile_gazetteer.supplied_transcription`, it grades
  three ways rather than two (an *unread* raw column outranks nothing, because it has no
  brackets in it for the reason that nothing has been supplied into it), and it moved twelve
  readings across the corpus — every one of them from a fragment to a fuller reading of the
  same sentence. Exactly one live placement moved: this one. No business's street moved.

So the honest count of what the ruling moves today is **two stores**, one of them placed and
one of them waiting to be built.

**Related:** T-0771 (the pairing ruled, the population measured, and the supply-gives-way-to-ink rule) · `docs/STREET-FACE-ADOPTION.md` (the policy for the other half of the problem) ·
**L215** (the metres, the side of Dearborn, and the invented building) · T-0384 (the ruling) ·
T-0306 (the American's six storefronts) · T-0375 (the South Water roofs an adoption wanted).
