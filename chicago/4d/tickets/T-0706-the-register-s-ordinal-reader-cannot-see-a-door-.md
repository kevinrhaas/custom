---
id: T-0706
title: The register's ordinal reader cannot see a door count whose 'doors' the reading pass reconstructed in brackets, so 'five [doors east] of the corner' falls through to street_only
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-04
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The register's ordinal reader cannot see a door count whose 'doors' the reading pass
reconstructed in brackets, so "five [doors east] of the corner" falls through to
street_only.

Found by T-0440. `tools/compile_register.py`'s `ORDINAL_DOOR` is

    r"\b(%s)\s+doors?\b\s*(north|south|east|west)?\s+(?:from|of|above|below)\s+(.{0,40})"

and it is matched against `offset_normalized` first and `offset_text` second. A normalised
reading puts the reconstructed words in SQUARE BRACKETS, which is the corpus's own
convention and is right — Clark, Filer & Co.'s June printing reads "South water St. five
[doors east] of the corner [of Randolph st.]". `\s+doors?` cannot cross the `[`, so the
phrase does not match, `ordinal_off_a_corner` returns None, and the anchor falls through to
the `street` reading the owner's ruling of 2026-08-30 overturned. Meanwhile
`tools/measure_corner_ordinals.py` DOES report this same phrase as "readable as an ordinal
off a corner" — the sweep and the reader disagree about the same string, which is the part
worth fixing whatever the answer is.

The question the fix has to answer first is whether a bracketed word may be read at all.
Brackets mark what the page does not carry, so reading through them silently would let a
reconstruction place a building; but refusing them means the sweep's own count of readable
ordinals is wrong. One defensible shape: strip brackets for MATCHING but record on the
resolution which words were bracketed, so a placement resting on a reconstruction says so
and a gate can refuse to spend it. That is a proposal, not a decision.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

- The disagreement between `measure_corner_ordinals.py`'s sweep and
  `ordinal_off_a_corner` is closed in one direction or the other, and the direction is
  argued rather than assumed.
- Every ordinal phrase in the corpus is counted both ways before and after, so the change
  is measured and not hoped for.
- If bracketed words become readable, a placement that rests on one is marked as resting
  on one, and `docs/CORNER-ORDINAL.md` says what may be spent from it.
- Clark, Filer & Co. is NOT placed by this ticket regardless: T-0705 holds the bar on its
  door count and this ticket may not lift it.

**Related:** T-0440 · T-0705 · T-0384 · `docs/CORNER-ORDINAL.md`.
