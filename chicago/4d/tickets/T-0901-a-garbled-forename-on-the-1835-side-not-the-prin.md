---
id: T-0901
title: A garbled forename on the 1835 side, not the printed one: 'Willınm Bandle' carries a dotless i and refuses its own Fergus 1843 entry
state: open
epic: META
requested_by: loop
seen: false
effort: M
legacy_id: null
parent: null
opened: 2026-09-06
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

A garbled forename on the 1835 side, not the printed one: 'Willınm Bandle' carries a dotless i and refuses its own Fergus 1843 entry.

**Acceptance:** (state it before working — the definition of done, never weakened to pass)

**Found by T-0695's sweep**, which looked at both sides of every forename refusal and not
only the printed one. `tools/name_agreement.garbled()` fires on the 1835 reading here, not
on the directory's:

    resident  Willınm Bandle   (person_id bandle_william)   — a dotless 'ı' where the 'a' belongs
    printed   Bandle, Willis, blacksmith, Stow's Foundry, res North Branch, w.side
              — f1843_e0263, Fergus 1843

`fold()` drops the `ı` outright, so `Willınm` folds to `willnm` and `Willis` to `willis`;
they are neither the same string, a prefix, a printed contraction nor one letter apart, and
the match is refused with `garbled_reading: true` — correctly flagged, and pointing at the
resident record rather than at the volume.

Whether the refusal SURVIVES the repair is the open question and is not assumed here:
`William` against `Willis` is still two full forenames that differ, so the man may well stay
refused. The defect is that a resident record carries a character no hand wrote, and that
the crosswalk is deciding against it.

**Unlike T-0695 this touches the residents layer**, so it is a grade-bearing change and not
a directory repair: the name moves on the record, the identity master and the grading
proposal re-derive, and the card in the walkthrough prints the corrected name.

**Acceptance:** the source of `Willınm` is traced to the pass that wrote it and corrected at
that pass rather than by hand; no grade moves in either direction unless the ticket says why;
`name_agreement.garbled()` finds no resident-side garble left in either directory crosswalk's
refusals; `bash tools/check.sh` green and the mirror published.
