# Fort Dearborn on 1835-07-01

Research memo for the `fort_dearborn_*` records and `chicago_lighthouse_1832`.
Written 2026-08-11. Where sources disagree the disagreement is set out and the reading
is chosen with reasoning, per `AGENTS.md`.

---

## 1. The question this memo had to answer first

`docs/ROADMAP.md` § S5a set two gates before any geometry:

1. **Find a plan source.** Wright 1834 labels the reservation and draws no fort, so the
   palisade, blockhouses, barracks, magazine and parade had to come from somewhere else.
2. **Settle what the fort WAS on the scene date**, because an occupied fort and an empty
   one are different scenes.

Both are answered below. The first is answered better than expected — a plan exists and
it is a U.S. engineer's survey. The second is answered completely.

---

## 2. What the fort was on 1835-07-01

**Occupied, garrisoned, and maintained.** The chain, from Andreas vol. 1 p. 84 unless
noted:

| | |
|---|---|
| garrison withdrawn | 1823 |
| re-garrisoned | October 1828 |
| troops removed to Green Bay | May 1831 |
| **re-garrisoned, Black Hawk War** | **June 1832** — "In June the fort was once more garrisoned. Major William Whistler being assigned to the command" |
| held continuously | to **29 December 1836**, when the troops were permanently withdrawn under a printed order |

So the common belief that the fort stood empty in the mid-1830s is wrong, and this
project's brief carried a version of it. **On 1835-07-01 the post is held.**

**Who commanded.** Andreas brackets rather than states: DeLafayette Wilcox "commanded
until December 18, 1833, and again from September 16, 1835", with "Major John Bender,
Major John Greene and Captain and Brevet-Major Joseph Plympton … in command at various
times" in between. The drloihjournal chronology fills the bracket with **Maj. John
Greene, 5th Infantry, 18 December 1833 – 16 September 1835**, which lands exactly inside
Andreas's two dates. That is the reading the records carry, graded `inferred`, with both
sources cited and the unfootnoted one named as such.

**How many men is not attested.** Andreas gives two companies of U.S. infantry in 1833
and nothing later. No strength figure for mid-1835 was found, so none is recorded. The
often-quoted "about fifty in number, many of whom were invalids" is the **first** fort —
see § 6.

**Condition.** No source reports dilapidation before the late 1830s. "In decay" language
belongs to the years after the army left. The fort is modelled serviceable, with its
gates shut, because a shut gate is a claim about a garrison being present and an open one
is a claim about the hour of the day.

**One live event, five weeks old on the scene date.** Jean Baptiste Beaubien bought the
entire Fort Dearborn Reservation at the land office on **28 May 1835** for $94.61,
recorded 26 June. The purchase was voided years later by *Wilcox v. Jackson*. It changes
nothing about the buildings and everything about the mood of the place; it is context,
not geometry.

---

## 3. The plan source, and what it is worth

**Found.** *Map of the Mouth of Chicago River, drawn by F. Harrison Jr., Ass't U.S. Civil
Engineer, for the Purpose of showing the proposed Harbor Improvements … The original
received and approved by William Howard, U.S. Civil Engineer, February 24, 1830*,
reproduced in **Andreas, History of Chicago, vol. 1, p. 113** — listed in that volume's
own table of maps as "Fort Dearborn in 1830-32". Recorded as
`data/sources/harrison_1830_river_mouth.json`; the page image is Internet Archive leaf
`n242` of `historyofchicago01andr`.

It draws the fort **in plan**: a quadrangular picket enclosure, a work at three of its
four angles, four ranges of buildings set against the walls, two small buildings flanking
a break in the south wall, and a heavier block outside the south-west angle. It also names
the ground around it — *Garden for the Garrison*, *Cultivated Field belonging to The
Fort*, *Big Barn with Cupola*, *Wash house*, *Well*, *Shop*, *Gate*, *Out Buildings*,
*U.S. Factor's House*, *Fort Cemetery*, the *Ferry*, and the Kinzie house opposite.

**Three limits, all of them stated on the source record.**

- The plate says on its own face that it carries "**additions and changes … suggested by
  the Memory of Early Settlers**". Period survey plus fifty-year-old recollection, mixed
  on the plate with no way to separate them. Nothing taken from it is graded `documented`.
- **There is no scale bar.**
- It is 1830, five years before the scene date.

**The scale.** Derived, not read: set the north range equal to the commandant's quarters
at "about 25 × 50 ft" from the 1855 photograph key, giving **1.10 ft per pixel** of the
archive.org page image (0.335 m/px). Two independent checks on the same plate:

| check | plate | source | agreement |
|---|---|---|---|
| commandant's quarters, length : depth | 1.9 : 1 | 2.0 : 1 (25 × 50 ft) | 5 % |
| gap between the west and east ranges | 71 ft | 80 ft parade width (1855 key) | 11 % |

So **±20 %** on every dimension derived this way, on top of the ±20 m the datum carries.
The fort's stockade comes out **about 53 m (174 ft) square** — somewhere between 140 and
210 ft on a side.

**The reading frame, written down (T-0881, 2026-09-06).** Every fort position in
`data/structures/` cites "pixels on the plate" and not one of them records WHICH pixels, so
the frame existed only inside the run that made it and the next placement had to rebuild it
from nothing. It is here now. Take the page image at
`https://archive.org/download/historyofchicago01andr/page/n242.jpg` (2003 × 2715), rotate it
**90° anticlockwise** so the sheet's north arrow stands vertical, and:

> the fort centre the committed records hang on — local **E +1152, N +221** — is at pixel
> **(1466.1, 647.9)**, at **0.335 m/px**, north up.
>
> `local_E = 1152 + (px − 1466.1) × 0.335` · `local_N = 221 − (py − 647.9) × 0.335`

**The anchor is fitted, not guessed.** The ink centroids of the two small buildings flanking
the south gate are at (1424.8, 707.7) and (1467.4, 713.5); solving each against the committed
position of `fort_dearborn_guard_house` and `fort_dearborn_store_house` gives (1465.8, 647.7)
and (1466.4, 648.1) — two independent solutions 0.6 px apart. Marking all fourteen committed
fort records back onto the plate at this frame puts every one of them on the feature it
describes, which is the check that matters: a wrong scale shows as an error that grows with
distance from the anchor, and there is none across the 170 px the complex spans.

**Two independent checks on the scale, and they do not quite agree with § 3's 1.10 ft/px.**
The guard house and store house stand 42.96 px apart on the plate and 14.19 m apart in the
committed dataset, which is **0.330 m/px**. And the plate's own building symbols measure close
to the footprints taken off them: the store house symbol is 12.79 × 4.69 m by the principal
axes of its connected ink against a committed 12.24 × 4.37 m, so the 2026-08 reader trimmed
0.55 m off the long axis and 0.32 m off the short one for the drawn line weight. **The source
record and this document disagree on the figure itself** — `harrison_1830_river_mouth.json`
prints "about 1.06 feet per pixel … 0.32 m/px" and the same two texts disagree on the parade
cross-check (74 ft there, 71 ft here). That is **T-0885**, and it is a disagreement in the
documentation rather than in the placements: the anchor absorbs a constant, so nothing
committed moves whichever figure wins.

**Rotation.** The fort's four walls are drawn a mean **8° clockwise of true north**,
measured against the sheet's own north arrow, which sits within 0.2° of vertical once the
leaf is rotated 90°. Eight degrees is inside what a woodcut can invent, so it is
`inferred` — but a square post whose four walls all lean the same way by the same amount
is more likely to be a fort that was not square with the meridian than an engraver who
tilted four lines consistently. The fort sat on a river bank inside a bend and had no
grid to align to.

**No dimension of the second fort exists in the literature.** Quaife's *Chicago and the
Old Northwest* (1913) is the standing monograph — its title page says "together with a
History of Fort Dearborn" — and he had the War Department files. He prints Captain
Whistler's measured 1808 draught of the **first** fort in full, with its scale ("twenty
feet to the Inch") and its distances ("From the northwest corner of the stockade to the
river was a distance of eighty feet"), and states **no dimension of the 1816 fort
anywhere**. Searched on `stockade`, `palisade`, `blockhouse`, `parade`, `second fort`.
The absence is in the literature, not in the searching.

---

## 4. The arrangement, and why it is the strongest thing here

Two witnesses, twenty-eight and three years apart, describe the same fort building by
building. The 1830 plan satisfies every clause of the earlier one.

**Gurdon S. Hubbard, of the fort in July 1827** (Andreas vol. 1, p. 264, quoting Fergus'
Historical Series No. 10):

> the brick building, just within the north stockade previously occupied by the
> commanding officers. The old officers' quarters built of logs on the west, and within
> the pickets, were occupied by Russel E. Heacock … while a number of voyageurs with
> their families were living in the soldiers' quarters, on the east side of the
> inclosure. The store-house and guard-house were on either side of the southern gate;
> the sutler's store was east of the north gate, and north of the soldiers' barracks; the
> block-house was located at the southwest and the bastion at the northwest corners of
> the fort, and the magazine, of brick, was situated about half way between the west end
> of the guard and block-houses.

**Andreas, of the rebuilt fort** (vol. 1, p. 84):

> The fort, as rebuilt, consisted of a square stockade inclosing barracks, quarters for
> the officers, magazine and provision-store, and was defended by bastions at the
> northwest and southeast angles. The block-house was in the southwest corner. The
> officers' quarters were on the west side and the soldiers' barracks on the east side.
> It had two gates, one on the north and the other on the south side.

**Juliette Kinzie, living in it in 1831** (Wau-Bun ch. XVII):

> The fort was inclosed by high pickets, with bastions at the alternate angles. Large
> gates opened to the north and south, and there were small posterns here and there for
> the accommodation of the inmates. … Beyond the parade-ground, which extended south of
> the pickets, were the company gardens, well filled with currant-bushes and young
> fruit-trees. … The bank of the river which stretches to the west … was then occupied by
> the root-houses of the garrison.

An 1830 engineer's plan and an 1827 eyewitness agreeing building by building on the same
sides of the same two gates is what licenses `inferred` rather than `conjectural` for
every position in the complex.

**One piece of reasoning decided two records.** Hubbard says the store-house and the
guard-house flank the south gate and does not say which is which; the plan draws two
buildings there and does not letter them. His next clause puts the magazine "about half
way between the west end of the guard and block-houses", and the block-house is at the
south-west angle. **That sentence only describes a real gap if the guard-house is the
western of the two.** So the guard-house takes the west building, the store-house the
east, and the magazine goes in the gap between the guard-house and the block-house. If
the assignment is wrong the two small buildings swap and nothing else moves.

**Buildings modelled** (14 records; sizes as built):

| record | side | size | footprint grade |
|---|---|---|---|
| `fort_dearborn_palisade` | the enceinte | 53 × 53 m | inferred |
| `fort_dearborn_commandants_quarters` | north, west of the gate | 15.24 × 7.62 m | **documented** |
| `fort_dearborn_sutlers_store` | north-east | 15.0 × 6.4 m | inferred |
| `fort_dearborn_officers_quarters` | west | 18.29 × 9.14 m | inferred |
| `fort_dearborn_barracks` | east | 27.6 × 11.0 m | inferred |
| `fort_dearborn_guard_house` | south, west of the gate | 10.9 × 4.2 m | inferred |
| `fort_dearborn_store_house` | south, east of the gate | 12.2 × 4.4 m | inferred |
| `fort_dearborn_magazine` | south-west, inside | 4.6 × 3.7 m | conjectural |
| `fort_dearborn_blockhouse` | south-west angle | 14.5 × 9.8 m | inferred |
| `fort_dearborn_artillery_house` | east, south end | 8.0 × 5.0 m | conjectural |
| `fort_dearborn_parade` | the court | 21.8 × 33.2 m | inferred |
| `fort_dearborn_root_house` | river bank, west | 5.0 × 3.6 m | conjectural |
| `fort_dearborn_garrison_garden` | south-west, outside | 77 × 77 m | inferred |
| `chicago_lighthouse_1832` | north-west, outside | 5.6 m dia. | conjectural |

---

## 5. The parade ground: two sources on one page, differing by a factor of two

- **1855 photograph key**: "C is the parade-ground (**80 × 200 ft**)."
- **Robert Fergus, of the fort in 1850**: "about **80 feet wide**, and extended from the
  river bank south, the full length of the enclosure — say **400 feet**."
- **The 1830 plan**: the court between the four ranges measures about **71 × 109 ft**.

`docs/research/04-structures-south.md` records only the first, as `[DOC]`. It is graded
**`inferred`** on the record, with the disagreement written on the footprint.

The reconciliation this project adopts, stated as an argument and not a finding: the
**width** agrees across all three (71, 80, 80), which is the check that the derived scale
is reading the plate. The **length** does not, and the likeliest reason is that both
later figures describe the compound **after the stockade came down** — Fergus says in
terms that his 400 ft runs "from the river bank south, the full length of the enclosure",
and by 1850 the "enclosure" was a whitewashed board fence, not the pickets. A third
witness supports the split: Kinzie, inside the stockaded fort in 1831, says the parade
"extended south of the pickets", so there was drill ground outside the south gate as well
as court inside. **That outside ground is not modelled** — nothing gives its extent.

---

## 6. The wrong-fort trap, and two corrections to this project's own dossier

The single largest hazard in this subject is that the most detailed published description
of "Fort Dearborn" is of the fort that burned in 1812. The passage — two blockhouses at
the south-east and north-west corners, a sally-port to the river, a strong palisade of
wooden pickets, the two-storey log U.S. factory west of the fort, the root-houses between
fort and factory, the garden on the south side, three pieces of light artillery, and "A
company of United-States troops, about fifty in number, many of whom were invalids" —
closes with the sentence **"Such was the old Fort previous to 1812."** John H. Kinzie
says the same thing from the other direction: the first fort, "although it stood upon the
same ground as the last Fort, … was differently constructed."

**What that excludes**, all now in `data/exclusions.json`: the first fort itself
(`fort_dearborn_first_1803`), the sally-port (`fort_dearborn_sally_port`), the three
artillery pieces and the fifty invalids (`fort_dearborn_artillery_pieces_1812`).

**Correction 1 — the sally-port.** `docs/research/04-structures-south.md` § 1.2 tags it
`[DOC]` as "attested for the 1816 fort's north side". The page it cites is describing the
pre-1812 fort, and Whistler's own 1808 index lists the feature as "N. 33 Covered Way to
procure Water". No source reached attests a sally-port at the second fort.

**Correction 2 — the officers' quarters were not brick.** The same dossier section reads
Andreas as giving "Officers' quarters — brick buildings on the west" and flags a conflict
with the 1855 key's "wood". Andreas p. 84 states **no material** for them; Andreas p. 264
— Hubbard's own words — says **logs**. The conflict was a misreading of a page, and the
two sources agree. What is genuinely brick is the **commandant's quarters** (Hubbard and
the 1855 key, independently) and the **magazine** (Hubbard).

**Correction 3 — there is no hospital building.** § 1.2 lists a hospital among the fort's
structures. The only hospital in the sources is the fort *becoming* a general hospital on
11 July 1832 during the cholera — a use of the existing buildings while the officers
camped outside — and the U.S. Marine Hospital of 1848+, which is the vantage point of the
1855 photograph. Excluded as `fort_dearborn_hospital`; **no hospital is modelled**.

**And a fourth thing, which is not a correction but is worth knowing.** The barracks and
the store-house **burned in September 1827**: after the annuity payment, "these quarters
were struck by lightning and totally consumed, together with the store-house and a portion
of the guard-house". The 1830 plan, three years later, draws a range on the east side and
two small buildings at the south gate. So they were rebuilt or replaced between 1827 and
1830, and the fabric standing in 1835 is partly newer than 1816. Nothing reached describes
the rebuilding.

---

## 7. What is attested and not built

Recorded here rather than silently omitted, and where a record states it the record
carries the `geometry:` declaration and a liberty:

- **Posterns.** "Small posterns here and there" (Kinzie). "Here and there" is not a
  position. `fort_dearborn_palisade.form.posterns`, `geometry: absent`, **L47**.
- **The garden's planting.** "Currant-bushes and young fruit-trees" (Kinzie).
  `data/flora/` has no cultivated zone and no garden species.
  `fort_dearborn_garrison_garden.form.planting`, `geometry: absent`, **L45**.
- **The drill ground south of the pickets** (Kinzie). No extent given.
- **Named ground on the 1830 plan and not modelled**: the Big Barn with Cupola, the Well,
  the Out Buildings, the U.S. Factor's House, the Cultivated Field, the Fort Cemetery, the
  Ferry. Each is a candidate for a later slice and each would be almost entirely invention
  today — the plan gives a symbol and a label and no form. The **Fort Cemetery** in
  particular is left alone deliberately.
  **The Wash house and the Shop came off this list on 2026-09-06** (T-0881, of T-0758):
  `fort_dearborn_wash_house` and `fort_dearborn_shop`, both placed off the plate at the
  frame recorded in § 3 below, both `inferred` in position and footprint, everything else
  the archetype's conventions. T-0758's other two children hold the rest: **T-0882** the
  Well and the Big Barn with Cupola (neither form exists in `generators/archetypes/`),
  **T-0883** the Out Buildings and the Fort Cemetery.
- **The ordnance.** No gun is drawn. See § 6.

---

## 8. Where this can be upgraded cleanly

Every attribute in these records carries its own confidence and its own note, so a new
source lifts one value without a rewrite. The three that would move most:

1. **Any quartermaster return, repair estimate or engineer's report for the post,
   1816–1836.** A picket count or a quantity of timber settles the stockade's height and
   spacing together (L47); a building return settles the storey counts and roofs (L42).
2. **A plan or measured view of the fort later than 1830** — the 1850 daguerreotype and
   the 1855 photograph both exist. A measured reading of either settles the lighthouse's
   shape at once (L44) and probably the barracks' storey count.
3. **The Chicago Democrat**, 1833 onward. It is the town's own paper through the scene
   date, it is where building notices and the fort's comings and goings would appear, and
   this project has not yet read it.

---

## 9. Sources used

| id | what it gave |
|---|---|
| `harrison_1830_river_mouth` | **the plan** — arrangement, proportions, rotation, the named ground |
| `andreas_1884_v1` | the square stockade, the two gates, the corner works, Hubbard's 1827 interior, the garrison chronology, the lighthouse sentence, the 1827 fire |
| `wentworth_1881_fort_dearborn` | the 1855 photograph key (the only stated dimensions), Fergus's 1850 addendum, the commandants, Beaubien's purchase |
| `kinzie_waubun_1856` | high pickets, bastions at alternate angles, gates north and south, posterns, the company gardens, the root-houses, the parade south of the pickets |
| `quaife_1913` | Whistler's 1808 draught and index (used only as a **guard**), Long's 1816 report, and the scholarly negative on the second fort's dimensions |
| `drloih_fort_dearborn` | the dated commandants table that brackets the scene date |
| `lighthousefriends_chicago` | the 1832 tower's height, builder, reflectors and lantern |
| `chicagology_prefire052` | the same text as `wentworth_1881_fort_dearborn`, at a URL; cite that one |

---

## 10. The flagstaff: what settled it, and what is still unsettled (T-0096, 2026-08-28)

T-0096 asked the question this memo's § 6 makes unavoidable: **did the SECOND fort carry a
flagstaff, and can anything but a retrospective plate say so?** The trap is set out in
`docs/RESEARCH/fort_dearborn_image_accuracy.md` § "The flagstaff is a documented trap" —
`p4_0` draws a staff, `data/exclusions.json` already excludes Whistler's 1808 one, and
raising the second fort's staff on a tier-5 retrospective view would be the commonest error
in the popular literature committed on purpose. T-0197 sharpened it on 2026-08-28 by
measuring where the plate's staff stands (0.495 of the drawn wall run — over the GATE, not
in the parade where the excluded one is), which closed off "the exclusion already covers it"
as an answer without supplying one.

**It is answered, and the answer is Andreas's own narrative rather than any plate.**

> It did not show a single steeple nor a chimney four feet above any roof. **A flagstaff at
> the fort, some fifty feet high, flaunted, in pleasant weather and on holidays** — a
> weather-beaten flag, as an emblem of civilization, patriotic pride, national domain, or
> anything else that might stir hearts of the denizens of the town. The buildings of the fort
> were low posted, and none of them exceeding two low stories in height.

— Andreas, *History of Chicago*, vol. 1, **p. 128**, in the section headed **"Chicago from
1833 to 1837"**, which opens at the close of 1833 with the town legally organized. The same
paragraph, describing the approach from the south: *"a line of almost indefinable structures,
and **the flag over the fort, if perchance it was flying**."*

**Why this reaches the 1816 post where nothing else does.** It is not the *"Such was the old
Fort previous to 1812"* passage; it is not Whistler's 1808 index; it is not a plate. It is
Andreas narrating the town across the four years the scene date sits inside, and the fort he
is looking at is the one standing in those years. He is corroborated on the same page by a
detail that only fits the second fort — *"the buildings of the fort were low posted, and none
of them exceeding two low stories"*, which is this project's fort, not the two-storey
galleried barracks of Whistler's draught.

### What was searched, and what it did not say

A negative finding is worth as much as the positive one here, so the search is recorded the
way `quaife_1913`'s is:

| searched | for | result |
|---|---|---|
| `quaife_1913`, full Gutenberg text | every occurrence of `flag` | **NEGATIVE for the second fort.** One flagstaff in the book, and it is the first fort: *"the barracks … occupied the middle of each side of the inclosure facing toward the parade ground, in the center of which stood a lofty flagstaff"*, from Whistler's 1808 draught. Nothing on a staff at the 1816 post; his account of it is Long's 1816 progress report and no plan. |
| `andreas_1884_v1`, full archive.org text of vol. 1 | every occurrence of `flag` (33) | **POSITIVE, once**: p. 128, above. Every other hit is a flag of truce, a Spanish or British flag, the 1848 fire-department review, or Mexican-War recruiting. The fort's own flagstaff appears in this dataset exactly once. |
| `kinzie_waubun_1856`, full archive.org text | every occurrence of `flag` (5) | **NEGATIVE.** She lived inside the fort in 1831 and describes the pickets, the bastions, the two gates, the posterns, the gardens, the root-houses and the parade — and no staff. Her five hits are rushes, a grave-flag, a conflagration, the *Little Belt* striking her colours, and an obituary. |
| `wentworth_1881_fort_dearborn` / `chicagology_prefire052` | every occurrence of `flag` | **NEGATIVE.** The 1855 Hesler key, Fergus's 1850 addendum and the commandants list carry no staff; the page's only fort flag is a caption on an image of a flag *"reportedly used at Fort Dearborn 1803-12"* — the first fort again. |

So **Andreas is the whole of the positive evidence**, and the record leans on nothing else.
Four independent texts that describe this fort at length do not mention its staff, which is
worth knowing when weighing how much silence in this literature means.

### What was built, and the two positions that were refused

`data/structures/fort_dearborn_flagstaff.json` — archetype `fort_structure`, new kind
`flagstaff`, a bare tapering spar **15.24 m** (Andreas's fifty feet) standing at the centre of
`fort_dearborn_parade`.

**The height is `attested`. The position is `reconstructed` and two candidates were refused
rather than used:**

1. **Whistler's parade centre.** The 1808 draught puts the FIRST fort's staff *"in the center
   of"* its parade. That fort is excluded whole in `data/exclusions.json`, whose entry ends
   *"none of it may be borrowed for the second fort's records"*. It is not the warrant here.
2. **`p4_0`'s over-the-gate staff.** T-0197 measured it at 0.495 of the drawn wall run, wedged
   between the two roofed lanterned works T-0095 read as first-fort signature. On that sheet
   the staff and the towers are ONE composition, so raising the staff on it raises two
   blockhouses with it — the exact conflation the image-accuracy pass refused.

What is left is a choice constrained by the model rather than by a source, and **L204** owns
it: the parade is the only open ground inside the stockade a fifty-foot spar can stand on
without standing on a range or a roof, and the centre of a rectangle is the only point on it
that does not need a second invention. **That this lands where Whistler's staff stood is a
coincidence of two rectangles and is not corroboration.**

### And it carries no flag, which is a reading of the source and not an omission

Andreas is precise about when the flag was up: *"in pleasant weather and on holidays"*, and
from the south *"if perchance it was flying."* The scene date is **Wednesday 1 July 1835** —
not a holiday, and weather is not modelled in this project. A flag drawn on this spar would be
a claim about one particular forenoon that the source explicitly declines to make. The refusal
is the same one § 2 makes about the gates: a shut gate claims a garrison, not an hour.

### What would still move it

A garrison return, a quartermaster's account or a post repair estimate for 1816–1836 would give
the staff a position and probably a spar — the same documents § 8.1 wants for the stockade. So
would the 1830 Harrison sheet re-read at page-image level for a staff symbol on the parade: this
project has taken the fort, the garden, the barn and the ferry off that plate and has never
looked at it for this.

### What the staff costs, measured — the question that held this work for a day

`p4_0`'s staff is the tallest thing on this reservation, and a 15 m vertical standing in the
open is exactly the shape that lands in the scene-detail ceilings four open tickets are
defending. **The run that built it could not attribute its own delta** — desktop stage 4 came
back with the `balanced` tier over and the light tier drawing 85 calls against a floor of 80,
both already open reds by ticket, but with the light-tier count moved from the 83 on record,
and `+2 draw calls` is the shape of a mesh that failed to batch. Rather than merge a possible
regression past a floor this project has spent four tickets defending, the work was parked on
`hold` unmerged with the command to settle it written on the PR.

**Settled on 2026-08-28, on an idle runner, with `tools/measure_detail_ceilings.mjs --against`
— twice.** First against this branch's own merge-base, which isolates the branch's own
contribution from everything else moving on `dev`; then again after `dev` was merged in, which
is the tree that actually ships. Both readings agree, to the triangle and to the call:

| | the Sauganash | Lake at Canal | the forks | the aerial | Lake and Market |
|---|---|---|---|---|---|
| triangles | 0 | **+22** | **+22** | 0 | 0 |
| draw calls | 0 | 0 | 0 | 0 | 0 |

Twenty-two triangles, at the two stands the fort is visible from, and **nothing at all on the
draw calls at any stand at any of the three tiers**. So the spar batches with the town like any
other `fort_structure` mesh, and the two desktop reds are inherited whole:

- the **light tier's 85 calls at Lake and Market** reads 85 on an unmodified `dev` as well. It
  is over the 80-call floor and that is real, but it is **T-0247**'s and not this staff's —
  and note that 85 dates T-0247's own figure of 83, which was taken before the content of
  2026-08-28 landed.
- the **`balanced` breach at the forks** was 5,290 triangles over on the merge-base and is
  **gone** on the merged tree: every tier now reads inside its ceiling, `balanced` with 6,107
  triangles to spare. `dev`'s own trimming closed it while this branch waited.

The general lesson is the one T-0089 and T-0126 already paid for and this makes three: *a red
ceiling does not say whose triangles they are*, and the two questions — "is the town over?"
and "did this branch put it over?" — are answered by different numbers. The second one takes
about nine minutes on a quiet box.
