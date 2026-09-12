---
id: T-1049
title: With the place vocabulary resolved, refuse an out-of-town newspaper person as a Chicago appearance in read_newspapers(), record the refusal in its own class, and re-derive every card that loses a press reading
state: claimed
epic: META
requested_by: loop
seen: false
effort: S
legacy_id: null
parent: T-1047
opened: 2026-09-11
closed: null
pr: null
claimed_by: run 9/11/2026, 11:47:52 PM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34673822849
---

With the place vocabulary resolved, refuse an out-of-town newspaper person as a Chicago appearance.

Piece 2 of 2 of **T-1047**, itself piece 2 of **T-1040**. BLOCKED ON T-1048 — do not start this one first; a guard built on the unresolved vocabulary refuses Fort Dearborn.

## THE FINDING

`tools/consolidate_resident_evidence.py`'s `read_newspapers()` hands EVERY gazetteer person to the resident identity pool with evidence class `newspaper_1833_1835`, reading only the name and the first mention. It never looks at `associated_places`. So a man the papers place at Michigan City is offered to the clustering as a Chicago appearance, and merge rule M1 — identical normalised name — puts him on whatever Chicago card shares his name.

`hh_miller_samuel` is the worked example T-1040 was filed on. After T-1046 that card cites one press reading, `person_col_samuel_miller`, whose gazetteer record correctly reads `occupations: [agent]`, `associated_places: [Michigan City]` — David Carver's agent at Michigan City, Indiana. The card's note still says "A CONTEMPORARY CHICAGO PAPER OF 1833-1835 PRINTS THIS PERSON BY NAME IN THE TOWN" and its rung G1b is spent partly on that reading. The sentence is false of it. Strip it and the card is the 1832 muster and the 1833 tax list, which is what it should have rested on.

**Acceptance:** (state it before working — one demonstration, never weakened to pass)

- a newspaper person the resolved vocabulary places OUTSIDE the town, and nowhere inside it, is not offered to the pool as a Chicago appearance;
- the refusal is RECORDED in its own evidence class and not dropped — named, counted, and visible in the master the way the letter-list class already is, because a suppressed refusal is invisible and a named one can be argued with;
- `hh_miller_samuel` no longer cites the Michigan City reading, and its note no longer claims a Chicago paper printed the man in the town;
- every card that loses a press reading is re-derived in the same pass, and every rung that MOVES is stated with its count. This reached 132 households at filing; if the resolved vocabulary makes it fewer, say the new number;
- `bash tools/check.sh` is green.
