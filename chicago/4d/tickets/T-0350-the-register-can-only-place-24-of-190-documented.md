---
id: T-0350
title: The register can only place 24 of 190 documented businesses; 49 more reach a street face and 78 reach nothing
state: open
epic: PAPERS
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

The register (T-0262) places 24 of the 190 businesses standing on the scene date.
The other 166 divide into two piles the seeding tickets do not cover, and both need
a POLICY rather than a case-by-case decision:

- **49 `street_only`.** The paper names a platted street and nothing narrower —
  Peter Cohen at "the east end of South Water-street", J. S. C. Hogan on South Water.
  A street face is a real constraint and it is not a lot. What does the town do:
  adopt an anonymous reconstructed roof already standing on that face and attach the
  business to it, raise a new frontage record with a conjectural along-street
  position, or nothing at all until a corner turns up?
- **78 `unplaceable`.** No street the model holds. Some are outside the plat
  altogether (E. Wentworth's public house on Flag Creek, on the road to Ottawa);
  some are advertisements that simply never printed an address.

T-0263 takes the placeable ones onto South Water and Lake. This ticket is what
happens to the rest, and it is the difference between the papers yielding two dozen
buildings and yielding most of a town.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- A written policy for `street_only` and for `unplaceable`, in docs/, that a later
  run can apply without re-deciding.
- The policy states what confidence an adopted or raised record carries and what it
  cites; a business placed to a street face may not claim a lot.
- Counted against the register: how many of the 49 and the 78 the policy moves, and
  where the rest wait.
