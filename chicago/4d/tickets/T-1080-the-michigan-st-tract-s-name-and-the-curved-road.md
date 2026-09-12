---
id: T-1080
title: The Michigan St tract's name and the curved road north through it: who platted it, what the sources call it, and the road traced off Wright's sheet
state: claimed
epic: META
requested_by: owner
seen: false
effort: S
legacy_id: null
parent: T-1075
opened: 2026-09-12
closed: null
pr: null
claimed_by: run 9/12/2026, 11:13:30 AM CT
blocked_on: null
needs_bake: false
closed_at: null
claimed_run: https://github.com/kevinrhaas/polecat-platform/actions/runs/34704397060
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

## WIP, 2026-09-12 — the reading is done and the record cannot be merged yet

**Both halves of the ask are answered** and the work is on
`steward/t-1080-michigan-st-name-road` (PR on `hold`):

1. **The name is refused, now twice.** Moses & Kirkland, line 13122, set Wolcott's Addition
   AFTER the canal commissioners' addition of June 1836 — two years past Wright's survey. The
   land was bought in 1830 but buying is not platting. The size argument (7.78 acres against
   eighty) is now the second reason rather than the only one.
   `docs/RESEARCH/michigan_st_tract.md` carries it.
2. **The road is traced, seated and committed** as the track `michigan_st_tract_road`, with
   `tools/read_michigan_st_tract_road.py`, `data/traces/michigan_st_tract_road.json` and
   **L234**. It CORRECTS the parent's premise: the road ENDS at Michigan Street and does not
   run north through the tract. 262 m, from North Water Street to the tract's Michigan Street.
   `tools/check.sh` is green on it (335 steps; the one red, the Chappel shore step, is red on
   clean dev too and is invisible in CI — see below).

**WHY IT IS NOT MERGED — a collision, not a defect in the reading.** The smoke's T-0184 wedge
check fails on this record, at `mobile 7-8`:

> `no bend in the ribbon opens a wedge on the outside of its turn — uncovered:
> michigan_st_tract_road [137.65, 301.66] 9.9 deg …; [146.96, 236.47] 19.8 deg …`

The cause is measured and it is not the mitre. **Seated, this road runs along the LIP OF A
MODELLED SWALE.** Sampling `e1834_harbor_cut`'s heightfield along the committed line: the
centreline stays dry the whole way (worst −0.087 m against the −0.10 m shore line), but the
ribbon's WEST edge is below that line for most of the reach between N 240 and N 320 — down to
−0.25 m at 3 m off the centre, and −0.20 m at 1.5 m off. `isWater` is `sample < −0.10`, so
`dryReach` trims those corners, `refinedPanel` refuses any panel with a wet interior vertex,
and the panels beside those two bends are not drawn. The joints' own vertices are dry, so the
check does not skip them, and it reports the hole the missing panels leave. **It is reporting
the truth.** Thinning the line does not fix it and neither does densifying it — the dense
36-station trace failed the same check at one station.

**THE QUESTION, and it is not this ticket's to decide.** Wright draws a road across ground this
project's terrain models 10 to 25 cm below the summer-1835 water surface. One of the two is
wrong, or neither is and the road ran along a wet verge that a ribbon may not be painted over.
Three ways out, none of them free:
  a. **The terrain moves.** The swale here is modelled relief, not traced; a drawn road across
     it is evidence against it.
  b. **The road moves.** Shifting it 5–10 m east would dry it — and it would be fitting the
     reading to the model, which is the thing this project does not do.
  c. **The road stands and the ribbon breaks.** Honest, and the wedge check refuses it, which
     is the check doing its job rather than a bug.

**ALSO FOUND, and it is a hole in the gate rather than in the data.** `tools/check.sh`'s
Chappel shore step is RED on clean `dev` and green in CI, because
`measure_chappel_shore_lighthouse.py` needs Pillow to re-measure the sheet and CI installs only
`jsonschema pyproj openpyxl pypdf` — so without PIL the step passes without asking anything.
With PIL it fires: `sauganash_range_m moved from 1066.3 to 1001.2 (tolerance 1.0)`, a 65 m drift
between the banked baseline and the committed Sauganash coordinate. Reproduced on a pristine
`--depth 1` clone of `dev`.
