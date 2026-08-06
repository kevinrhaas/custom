# The reference — what this piece has to be

The target is a single product photograph: a faceted olive-green chess knight
on a light grey seamless backdrop, 1232 × 1232, soft key light from above, a
soft contact shadow falling to the lower right. This document is that
photograph written down, because the generator and the design critic both need
to argue against the same description.

Machine-readable numbers live in `reference.py`. This file is the prose.

## Camera

Roughly 45° of yaw and 5° of elevation, long lens (near-orthographic). The
horse faces left. We see its left flank, the top plane of the muzzle, the
outward faces of the mane, and the front-left facets of the plinth. The piece
fills about 84% of the frame height.

## The overall read

An upright horse's head and neck on a stepped round plinth — a chess knight,
not a dragon and not a bird. It is **faceted, not smoothed**: every surface is
a flat plane and every transition is a hard edge. The facets are large and few;
this is a deliberate low-poly sculpt, not a tessellated smooth model. Matte
finish, no gloss, no texture.

Proportions, as fractions of the total height:
- plinth: bottom 26%
- neck: the middle ~46%
- head: the top ~28%
- widest point: the plinth, 0.57 × the height across
- the muzzle tip reaches about 1.12 plinth-radii from the axis — it overhangs
  the plinth on the left by a small but visible margin

## The head

- A **long wedge muzzle** thrown forward and very slightly down. Its top is one
  long, nearly straight plane running from the nose back and up to the brow,
  broken once by a shallow **nostril** facet about a third of the way back.
- The **nose is raked**: the front facet leans back as it rises, so the lower
  lip / chin is the most forward point of the whole piece, not the top of the
  nose.
- A **lip line** runs the length of the muzzle as a thin crease — a hairline
  step separating the upper muzzle from the lower jaw. It is a crease, not a
  slot; it must not read as an open mouth.
- The muzzle is **triangular in section**: broad across the top, narrowing to a
  narrow underside. It is not a flat bill.
- A small **triangular eye** is sunk into the flank high on the head, tucked
  directly under a hard brow ridge, just behind where the muzzle meets the
  skull.
- Behind the crown the outline drops to a small **ear** and then a notch,
  before the mane starts.
- The head is visibly **narrower than the neck**; the change happens at a hard
  step that reads as the jowl.

## The mane

**Five teeth** falling down the back from just behind the ear to the shoulder,
evenly pitched (about one tooth every 6.5% of the height). Each tooth is a
wedge: a broad top face sloping up and back to a point, then a shorter
underside dropping forward into the notch below it. The notches are crisp Vs,
about 1.5–2 mm deep on the real object — pronounced enough to catch light and
read from across a board, not a decorative ripple. The teeth get slightly
larger and reach slightly further back as they descend.

## The neck and chest

The chest leans forward out of the plinth, reaches its most forward point low
down, then draws back in a long, nearly straight run to the throat. At the
throat there is a **hard concave notch** where the jaw is thrown forward — the
underside of the muzzle starts there and runs out over open air.

The near flank of the neck is one large flat plane. An **angular panel crease**
runs down the chest, echoing the jowl step above it.

## The plinth

Sixteen-sided. Four bands, each stepping in as it rises:

1. a tall vertical **flange** at the very bottom, the widest part of the piece
2. a drum, stepping in at a hard shoulder
3. a second drum, stepping in again
4. a **collar** the figure springs from, narrower than the drums

Every step faces upward. The bottom edge is very slightly lifted so the first
printed layer cannot flare.

## What would make it wrong

- any smoothed or rounded surface
- a muzzle that reads as a beak, a bill, or a snout rather than a horse's
- the mane reduced to a ripple, a fin, or fewer than five teeth
- the head as wide as the neck (no jowl step)
- a plinth that is a plain cylinder or cone rather than stepped bands
- the mouth as an open slot
- a mushroom-shaped head wider at the crown than at the jaw
- proportions outside 2.5% of the height on the outline table in `reference.py`
