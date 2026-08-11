
# Philo Carpenter's Log Drug Store — research dossier

**Record:** `data/structures/philo_carpenter_log_shop.json` · **Scene status:** standing on
1835-07-01 **on the weakest continuity argument in the parcel** · **South Water Street parcel**

A rare combination, and the reason the record is worth having: **the footprint is evidence and the
existence is not.**

## 1. What is documented

- Chicago's **first drug store**, opened by Philo Carpenter, who reached the town **18 July 1832**.
- A **log building, 16 x 20 ft**, on **Lake Street near the river**, *"immediately adjacent to the
  Sauganash's public bar"*.

16 x 20 ft = 4.877 x 6.096 m. This is only the **second footprint in the dataset that is evidence
rather than a placeholder**, after Hogan's store — and at 30 m² it is the smallest building here.
Chicago's first drug store was a room.

## 2. The doubt, argued

In the **summer of 1833** Carpenter bought a lot on South Water Street between LaSalle and Wells
and *"erected a small store"* — `carpenter_south_water_store` in this dataset. **No source reached
says what became of the log shop.** So this building is placed in a scene set two years after its
proprietor built himself a better one.

**The counter-argument is specific and strong.** Lake Street beside the Sauganash was the most
valuable frontage at the forks; this is the smallest building in the dataset; and its one attested
occupant demonstrably left it.

**The contemporary advertisement does not rescue it.** *The Chicago Democrat* of 26 November 1833
carries Carpenter's own notice, dated 22 November 1833:

> "PHILO CARPENTER, CHICAGO—[ILL] … WILL keep constantly [on hand a general] assortment of DRUGS,
> MEDICINES, Oils, Paints, [Dye-Stuffs] &c. &c. — ALSO — Dry Groceries, Glass[, Nails, &c.]"

That is genuine primary evidence that Carpenter was **trading**, sixteen months after arriving and
**nineteen months before the scene date**. It carries **no address**, and by then he already had
two premises, so it cannot say which building held the trade. Treating it as evidence that the log
shop survived would be exactly the move the confidence model exists to prevent.

**Grade:** this record's existence at the scene date is the single most likely thing in the parcel
to be wrong. If evidence turns up that the shop came down or was moved before July 1835 it belongs
in `data/exclusions.json` and the record leaves the scene.

## 3. The position is derived from another record — a first here

The sources give a **relation**, not an address. The shop is set hard against the Sauganash's east
wall: `sauganash_hotel`'s `frame_1831` origin is E 447174.1, N 4637265.2, 12 m wide and 8 m deep at
bearing 0, so its north face is on the Lake Street frontage at N 4637273.2 and its east face at
E 447186.1. **This shop's west wall is on that easting and its north face on the same frontage** —
the two footprints touch, deliberately, because "immediately adjacent" is what the source says.

**Which side the bar was on is not attested.** East is chosen by elimination: the Sauganash's west
face stands on the Market Street frontage, and both retrospective depictions put the surviving 1829
log wing on the building's left front, which is the Market side. If the bar was on the west or the
river side, this shop is on the wrong flank and moves about 20 m.

The 20 ft dimension runs along the street and the 16 ft is the depth, following the convention
`hogan_store` argues for — an inference, not evidence.

## 4. Open threads

- **The individual building rectangles on Hathaway 1834 or Wright 1834** at the Lake and Market
  corner, which would show whether one building or two stood on that frontage. This is the check
  that would settle the record.
- The *Chicago Democrat* for 1834-35: an address in a later Carpenter advertisement.
- The DRLOIH treatment of Carpenter, cited in `docs/research/03-structures-north.md` and not yet
  held as a source record.

## The parcel's shared inventions

Three things are true of every record in the South Water Street parcel and are written once here
rather than sixteen times:

1. **The borrowed rectangle.** No period map this project has georeferenced shows a building
   footprint, and no source gives a South Water or Lake Street commercial building a dimension
   except Hogan's store (45 x 20 ft) and Philo Carpenter's log shop (16 x 20 ft). Every other
   footprint in the parcel is a rectangle built from figures borrowed from the dataset's own
   attested buildings — 40 ft frontage (Green Tree Tavern, Western Hotel), 25 ft depth (derived
   from the Green Tree's room module), 20 ft depth (Hogan's store) — capped by Andreas's
   documented **55 ft South Water lot width**. The repetition is the admission.
2. **The position method.** Modern intersection centres read from OpenStreetMap at EPSG:26916 on
   2026-08-11, offset 12.2 m (half an 80 ft platted street) to the kerb. South Water Street is
   today's Wacker Drive along the south bank; Wacker was built on its right of way in 1924-26 and
   widened northward over the old dock line, so the two lines are close but not identical.
   Working uncertainty is about **20 m** — the georeference's own residual (17.5 m RMS on Wright
   1834, 3.7 per cent paper stretch) — plus whatever the source's own vagueness adds, which is
   stated per record.
3. **The ground is not there.** Everything in this parcel east of about local E +320 stands
   outside the committed `e1834_harbor_cut` terrain box and is declared
   `ground_contact: outside_modelled_ground`. That is a terrain gap, not a structure gap.
