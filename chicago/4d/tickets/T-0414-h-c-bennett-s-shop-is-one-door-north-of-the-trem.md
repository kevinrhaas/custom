---
id: T-0414
title: H. C. Bennett's shop is one door north of the Tremont House
state: open
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: null
opened: 2026-08-29
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
---

H. C. Bennett's shop is one door north of the Tremont House.

Filed by **T-0385**, which taught `tools/compile_register.py` to see the first Tremont
House through the disambiguator this project put in its name. Three businesses were
anchored on that hotel and could not reach it; T-0385 built the New York Clothing Store
and filed the other two rather than bundling them.

`business_h_c_bennett` moved from `street_only` on `dearborn` to `new_building` on
`tremont_house_1` on 2026-08-29. Its anchor reads `si door north from the Tremont` —
an offset AND a direction, which is the same shape as the clothing store's and one door
rather than three. The leading `si` is the transcription's; whether the count is one door
or a cut number is the first question to settle, from the printing itself.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- The count of doors is read off the printing and stated, or the ticket says the
  segmenter has eaten it and records what that costs the placement.
- Bennett's shop stands on the west side of Dearborn Street at the offset the reading
  supports, its residual stated on the record by axis, with a liberty in the shape of
  L214 — the side of the street, the width of a door, and anything that had to move
  for the mid-block alley.
- It shares the block face with `tremont_house_1`, `new_york_clothing_store` and
  `bates_auction_room`: check none of the four overlaps and that the run still reads as
  a row of doors rather than a terrace.
- `./tools/check.sh` green, `./tools/bake.sh --only`, `./tools/publish.sh`, and a
  changelog entry in the same commit.
