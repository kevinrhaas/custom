---
id: T-1080
title: The Michigan St tract's name and the curved road north through it: who platted it, what the sources call it, and the road traced off Wright's sheet
state: open
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-1075
opened: 2026-09-12
closed: null
pr: null
claimed_by: null
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: null
---

The Michigan St tract's name and the curved road north through it: who platted it, what the sources call it, and the road traced off Wright's sheet.

Piece 2 of 2 of **T-1075 — The Michigan St tract named and seated: who platted it and what the sources call it, and its street, alley, parcels and the curved road north into the town's data**, split because the parent needed more than one run's demonstration to be done. The parent keeps the full ask and its links; this ticket owns one slice of it.

**Acceptance**, stated before working and not weakened to pass:

1. The tract's name is settled from a source that gives a BOUNDARY, or the refusal is
   recorded as a refusal. `docs/RESEARCH/michigan_st_tract.md` already carries the one
   candidate the corpus raises — Wolcott's Addition, canal-commissioner land west of State
   Street, which is the right section and the right side of the river — and the arithmetic
   that refuses it: Wolcott's was eighty acres and this tract is 7.78, with nothing platted
   beside it on Wright's sheet to make up the rest. Start there, not from scratch.
2. The curved road that leaves the Kinzie/North Water corner and runs north through the
   tract is traced off the sheet and committed as a TRACK of the same kind as `fort_road`,
   not as a platted corridor — or the trace is refused with the reason on the record.
3. Whatever is found is graded, and a name without a boundary grades no higher than
   conjectural.

---

## FOUND BY T-0795, 2026-09-13 — the road is the slough, and that is why the ribbon is wet

T-0795 walked the whole 600 dpi NA/HUP sheet for watercourses. It draws exactly one that is
not the river, and **it is this ticket's curved double line.**

**The project has held it as water since before this ticket existed.** `north_side_slough`,
in `data/terrain/epochs/e1834_harbor_cut/hydrology.geojson`, is a 45-vertex centreline
described as *"a narrow winding watercourse running north out of the main stem, across Kinzie
Street, ending at Michigan Street"* — the same two ends, the same reach, `wright_1834` cited
for **existence and course**. Re-measured against the NA sheet, 41 of its 45 stations find the
pair of strokes that bracket them and the centre of the pair departs from it by **1.78 m
median, 8.03 m at worst**. `michigan_st_tract_road` and `north_side_slough` are not neighbours.
They are one feature, read twice, four hundred commits apart.

**This dissolves the blocker exactly.** The WIP note above measures the road's ribbon standing
10–25 cm below the summer-1835 water surface and offers three ways out — move the terrain, move
the road, or break the ribbon. There is a fourth, and it is the one the evidence points at: the
ground under the road is wet **because the project already carves a watercourse along it**. The
swale is not modelled relief that happens to be in the way; it is this line, in the terrain.

**What the sheet says about which reading is right** — stated, not decided, because it is this
ticket's to decide:

1. **It is drawn as a confluence.** At NA px (2033, 2270) the west stroke *becomes* the river's
   north bank running south-west and the east stroke *becomes* the same bank running east: two
   banks continuous with the main stem's, on either side of an opening. A road drawn to a river
   either stops at the bank or crosses it. This does neither.
2. **Thompson's 1830 plat draws this feature as water**, across North Division block 6 — the
   same block the line crosses (T-0452, `docs/RESEARCH/thompson_plat_sloughs.md`). A second
   surveyor, four years earlier, on the same ground.
3. **The road argument cuts both ways.** "It curves, and it cuts diagonally across platted
   blocks and lot lines" is at least as true of a stream: a plat ruled over a watercourse is
   the ordinary case, a road ruled across finished blocks is not.
4. **The corridor widths agree, which is the tell.** This ticket measured 12.22 m between
   stroke centres; T-0795 measured 13.02 m on the same strokes by a different method. Same ink.

**What this ticket now owes**, and none of it is new reading: either withdraw
`michigan_st_tract_road` as a duplicate of `north_side_slough` and say so on L234, or show why
Wright drew a road down the middle of a watercourse he drew joining his own river. Whichever
way it goes, the two records must not both stand.

Audit: `docs/RESEARCH/wright_1834_watercourses.md`,
`data/traces/wright_1834_watercourse_audit.json`.
