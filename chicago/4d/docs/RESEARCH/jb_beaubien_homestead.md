
# Col. Jean Baptiste Beaubien's Homestead — research dossier

**Record:** `data/structures/jb_beaubien_homestead.json` · **Scene status:** standing on
1835-07-01 · **South Water Street parcel** · **`review_required: true`**

The **oldest building in this dataset** and the **least precisely placed**.

## 1. What is documented

Andreas: the **American Fur Company factory building**, erected by Capt. Bradley, bought by Jean
Baptiste Beaubien in **1817**. Beaubien afterwards converted an earlier cabin to a barn and built
a new residence and a small trading post.

**A live fact for the scene:** Beaubien's pre-emption certificate for the whole 75.69-acre fort
reservation is dated **28 May 1835**, recorded **26 June 1835**, price **$94.61** — five weeks old
and unchallenged on 1835-07-01. It was voided by *Wilcox v. Jackson*, 38 U.S. 498, in **1839**,
which is outside this scene.

## 2. The corner is contested inside a single source

| passage | reading | what the passage is about |
|---|---|---|
| Andreas, scan p. 185 | *"where now is the **southwest** corner of South Water Street and Michigan Avenue"* | the homestead itself |
| Andreas, scan p. 339 | *"go east upon South Water Street until you come to the **northeast** corner"* | a boundary walk in Block 5, using the corner as a waypoint |

**The south-west is adopted**, on the ground that a statement *about* the thing outranks a
statement that passes it. The two readings are about **45 m** apart — roughly twice the
georeference's own error, and the largest single uncertainty on the record.

## 3. A caveat that matters more than the corner

**Neither street existed here in 1835.** The reservation was unplatted, no street crossed it, and
South Water Street was ordered pitched only *"from the United States Reservation to Randolph
Street"*. Andreas is writing in 1884 and locating an 1817 building by the streets of his own day.
Any future evidence should be read as fixing this building relative to the **fort**, not to a grid
that arrived later. The facade bearing has **no attested basis whatever** and is a placeholder
inherited from the retrospective grid.

## 4. The homestead was four buildings and one is modelled

Andreas describes: the factory building (this record), a **new residence**, a **small trading
post**, and a **cabin converted to a barn**. The other three are attested and **not built** —
nothing reached gives any of them a size, a material, a form, or a position relative to the
factory building, so they would be three invented boxes placed by eye around a fourth. They are
recorded here and in the record's `research_note` instead.

Note the consequence for `occupants`: Andreas says Beaubien built a **new residence**, so which
building of the group he actually slept in on the scene date is unattested, and the record says so.

## 5. Why review is flagged

Same reasoning as `madore_beaubien_house` § 4. `AGENTS.md`'s standing constraint on Native
presence and representation, the August 1835 removal, and the reservation claim all meet in this
record. It states built fabric and the documented dates of the claim and leaves interpretation to
a review this project has not yet sought.

## 6. Open threads

- Any description of the factory building's material or size. **Construction is `inferred` as log
  from date and place alone**; if it was frame the record is on the wrong archetype.
- Wentworth and Quaife on Fort Dearborn (both now source records in this project) for the
  reservation's building group.
- The 1835 pre-emption papers themselves, which may describe improvements.

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
