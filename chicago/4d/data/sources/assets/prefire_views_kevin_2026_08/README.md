# Retrospective views of pre-fire Chicago — reference set, supplied 2026-08-11

Twelve images extracted from the project owner's brief of 2026-08-11, most of them
the 19th-century retrospective lithographs collected at chicagology.com (see the
existing `chicagology_prefire275` source record and its siblings). Supplied as the
**accuracy bar for building-improvement loops**: render the model's building, put it
beside the view, and close the gap.

**These are TIER 5 PICTORIAL sources.** They are retrospective reconstructions drawn
decades after 1835, and this project's standing rule applies in full: they may drive
**massing, roof form, fenestration rhythm, materials and setting** as `inferred`, and
they may never drive a coordinate or a footprint outline. They are comps, not surveys.

Known subjects (identify precisely before using — several carry printed plate numbers):

- **Fort Dearborn from across the river** (two views, one coloured): the fort on its
  RISING GROUND with the whitewashed palisade, outbuildings on the slope, the low
  wooded far bank, bark canoes. The bank height and its GRADATION down to the water is
  exactly what the owner wants the terrain to learn from (ROADMAP P8).
- **The Green Tree Tavern** (plate "11"): two full storeys of pale clapboard, end
  chimneys at both gables, 6-over-6 sash in even bays, a hanging SIGNBOARD on the
  street corner, the rear ell with its own gable. The best single facade reference in
  the set.
- **The Kinzie mansion group** (plate "12", `p6_1.png`): the long low house with its
  PIAZZA/porch front, the row of Lombardy poplars, the picket-fenced garden plots,
  outbuildings up the rise behind. NOTE: the house itself is EXCLUDED from the 1835 scene
  (gone before 1835; the cottonwoods stay) — this view is reference for FENCES, GARDENS,
  POPLARS and PORCH TREATMENT generally, not for rebuilding the house.
  **IDENTIFIED 2026-09-13 (T-0055): `kurz_allison_1893`, panel 12.** See the table below.
- **The courthouse with the Doric portico** (plate "6"): **THIS IS THE 1837 (or later)
  BUILDING — A DOCUMENTED TRAP.** The 1835 courthouse is a small wooden building about
  which nearly nothing is known (see the `cook_county_courthouse_1835` record and the
  `illinoiscourthistory` source's guards). Do NOT make the 1835 model look like this
  plate. It is in the set as a NEGATIVE reference.

The remaining images include the owner's screenshots of the current render for
comparison. Anything used in a critique loop should be identified against
chicagology's plate numbering first and cited to the matching `chicagology_*` source
record.

## Identifications

**The numbered plates in this set are not chicagology's numbering — they are the
panel numbers of one sheet.** T-0055 chased plate "12" and found it: the numerals
printed in the corners of these crops are the vignette numbers of **Kurz & Allison,
*Chicago In Early Days, 1779-1857*** (Chicago, 1893), a chromolithograph of fifteen
numbered panels with a printed key, held here since long before this directory
existed as `data/sources/kurz_allison_1893.json` (tier 5, **public_domain**), with the
whole sheet committed at `chicago/reference/photos/IMG_5382.png`. So the instruction
above is right in spirit and wrong in its destination: the citation these crops owe is
a `kurz_allison_1893` panel, not a `chicagology_*` record.

| file | numeral | the sheet's own key | source record |
|---|---|---|---|
| `p6_1.png` | "12." | "No. 12.  The Old Kinzie Mansion, built 1832.  Population 310." | `kurz_allison_1893`, panel 12 — **confirmed** |
| `p6_0.png` | "11." | "No. 11.  The Green Tree Hotel, cor. West Lake and Canal St.  Built in 1833." | `kurz_allison_1893`, panel 11 — **confirmed** |
| `p4_0.png` | plate "1" per this README | "No. 1.  Old Fort Dearborn.  Erected 1803." | `kurz_allison_1893`, panel 1 — *unconfirmed, not measured by T-0055* |
| `p3_1.png` | plate "5" per this README | "No. 5.  Fort Dearborn, as re[built] … 1835.  Population 3,265." | `kurz_allison_1893`, panel 5 — *unconfirmed, not measured by T-0055* |
| `p7_*`, `p8_*`, `p9_0`, `p3_0`, `p4_1`, `p5_0`, `p6_*` others | — | — | unidentified |

**How plate "12" was proved, so that the next one can be done the same way.** Three
independent agreements, of which any one alone would be an eyeball: (a) the numeral —
"12." in the crop's upper-left corner and in the upper-left corner of the sheet's
lower-left vignette; (b) the sheet's printed key, transcribed off the committed copy,
whose No. 12 line names the Kinzie Mansion and whose No. 11 line names the Green Tree —
matching the two crops that carry those two numerals; (c) a normalised cross-correlation
of `p6_1.png` against the sheet, which peaks at **0.797** at 0.88× scale on sheet pixels
(94,1164)-(438,1416) — that vignette — against a best of **0.341** anywhere in the
bird's-eye panel used as a control.

**The two fort rows are marked unconfirmed on purpose.** They are strongly implied by
the same numbering and by `kurz_allison_1893`'s own locator, but T-0055's scope was the
Kinzie plate and nothing else was measured. `data/enclosures/fort_dearborn_apron.json`
still cites those two by committed path and still records its `sources` as empty; making
that join, with the same three checks, is filed as its own ticket. Do not fill it in from
this table.

**What identification does and does not buy.** Panel 12 is still tier 5, still published
fifty-eight years after the scene date, and still may never drive a coordinate. What
changes is the citation: a source_id with a date, a publisher, a holding institution and
an expired copyright ("Copyrighted 1893 by Kurz & Allison, 76 & 78 Wabash Avenue,
Chicago, Ills.", printed at the foot of the sheet) in place of a path to a 391-pixel crop
of unstated rights.

## `wright1834_clark_reach_crop.jpeg` — supplied 2026-08-13

A detail crop of **Wright 1834** at the Clark Street reach, supplied by the project owner
against ROADMAP **K6** (the river "bulge"). Unlike everything else in this directory it is
NOT a retrospective lithograph — it is a piece of the master survey sheet, so the ordinary
Wright rules apply: it may drive geometry, at the ±20 m working uncertainty.

What it shows: the river's south bank running east, and a **narrow sinuous line dropping
south off the bank between numbered blocks 19 and 18** (lots 4/3/2 along 18's north edge,
5/6/7 along its south). The line is in the same thin ink as the river banks and runs BETWEEN
the blocks — the platting respects it, which is itself evidence that the surveyor was working
around a real watercourse.

**The owner's reading, which reframes K6:** the bulge in the render may be that STREAM,
mis-traced — most likely the water polygon closed ACROSS its mouth instead of running up it,
which turns the ground between the stream and the river into an enclosed peninsula. The
inverse (the stream traced too wide, drowning the land beside it) is also possible. The
distinction matters and should be determined from the geometry, not assumed.

Cross-reference: ROADMAP § S2e designates **Conley/Stelzer 1833** as the primary guide for
"the streams coming in, and where each one terminates", with Wright as the check. If a
documented watercourse belongs here and the trace never carried it, K6 is a MISSING FEATURE
rather than a bad curve.

The crop also shows block and lot numbers legibly, which is a georeferenced check on the
plat module for **K7**.
