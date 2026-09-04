---
id: T-0616
title: "The Sauganash is one 12x8 box: its two-storey rear wing is missing, its log annex stands in front, and four attested views resolve the massing, the door, the windows and the roof"
state: split
epic: META
requested_by: owner
seen: false
effort: L
legacy_id: null
parent: null
opened: 2026-09-03
closed: 2026-09-03
pr: null
claimed_by: null
blocked_on: null
needs_bake: true
closed_at: 2026-09-04T02:14:44.075Z
claimed_run: null
---

A deep dive on the Sauganash Hotel, asked for by the owner on 2026-09-03 from the
dev preview. **This is an ATTESTED structure and this ticket is about putting fine
points on it** — not about whether it stood, but about what it looked like, which
four drawn views answer far better than the record currently admits.

The owner's report, in his words: *"there is an extra log structure you have in
front and i think there is a structure missing but you have it on the front and
they have it on the rear in pictures, and it looks like the full height of the
main building and similar design as the main building appears to be almost the
same size, it connects from the back and side in the images."* And, on the level
of finish: *"you are missing a fair amount of detail, like the door, the windows,
the roof, etc."*

## The evidence — four views, deposited by the owner

`chicago/reference/images/chicago/sauganash-hotel/`

| file | what it is |
|---|---|
| `sauganashhotel.jpg` | **C. E. Petford, "Sauganash Hotel. 1831"** — watercolour, the clearest of the four: colour, full massing, fenestration, chimneys, roof texture, and the log annex's corner notching all legible |
| `sauganash.jpg` | **F. Braunhold engraving, "The Sauganash Hotel"**, copyright A. T. Andreas 1884 — same three-part massing from a near-identical angle, line work sharper on the siding courses and the roof shingles |
| `sauganash2.jpg` | a wash/pencil view of the same corner with figures and the street — the one that also carries the ground: plank walk, hitching posts, fence line |
| `images.jpeg` | a small colour thumbnail of the Petford (stock-agency watermark) — corroborates the colour reading, adds nothing the full plate does not |

Two of these are already in the tree one directory up as
`chicago_sauganash_hotel_1831_petford.jpg` and `chicago_sauganash_tavern_1835.jpg`;
part of this ticket is to say plainly which asset id each of the four is, and to
stop the same plate living under two names.

## What the views show, and what we draw instead

**All three drawn views agree on a THREE-PART building:**

1. **The main block** — two storeys, clapboard, its long eaves face to the street,
   a brick chimney on the ridge at the far end, five bays of sash above and a
   door-plus-four below, the door with a moulded architrave and a transom.
2. **A second two-storey wing** set BACK, its gable end to the viewer, its ridge
   running away at right angles to the main block's, **its ridge at essentially
   the main block's own height**, the same clapboard, its own brick chimney and a
   light in the gable. This is the owner's "full height … similar design … almost
   the same size … connects from the back and side."
3. **A one-storey LOG annex** at the far end — round logs with saddle-notched,
   projecting corner ends, a shingled gable roof, its own small chimney, one door
   and two windows. It stands beside and slightly forward of the tall wing, at the
   END of the composition. **It never stands in front of the main block's street
   face**, which is unobstructed in all three views.

**What `data/structures/sauganash_hotel.json` carries today:** phase `frame_1831`
(1831-01-01 → 1851-03-04) is **one 12 × 8 m rectangle**, and its own note says so —
*"PLACEHOLDER — the central unresolved question of this record. NO DIMENSIONS FOR
THE SAUGANASH ARE ATTESTED in any source reached. This 12 x 8 m rectangle is a
plausible two-story frame tavern footprint and nothing more."* Two storeys, white
paint and bright-blue louvred shutters are attested and carried; everything about
the SHAPE is a guess, and the second mass is not there at all. The `log_1829`
phase ends in 1831, so at the scene date nothing log-built belongs to this record —
yet a log structure is drawn standing in front of the hotel in the preview.

So there are three faults, and they are different in kind:

- **(a) A mass that is missing.** The rear/side wing is in every view and in no
  record.
- **(b) A mass in the wrong place.** Something log-built is drawn in front of the
  street face. Establish what it is — the retained 1829 Beaubien cabin (the
  record's own position note says the frame block "was later built onto it"), or
  `philo_carpenter_log_shop` mis-sited, or both conflated — and put it where the
  views put it.
- **(c) Fabric the views resolve and the model generalises.** Door, windows, roof,
  chimneys, siding. See the axis list below.

## The owner's plan sketch

He supplied a plan-view sketch (not committed — it is a working diagram, and this
transcription is the durable record of it):

```
            +---------------------------+
            |                           |
            |   SAUGANASH HOTEL         |     <- rear wing, running BACK
            |   REAR WING               |        from the main block
            |                           |
   +--------+---------------------------+--------+
   | PHILO  |                                    |
   | CARPEN.|   SAUGANASH HOTEL MAIN             |   <- main block, long face
   | DRUGG. |                                    |      to the street
   +--------+------------------------------------+
                        (street)
```

**One thing in it must be adjudicated rather than copied.** The sketch puts the
rear wing back from the RIGHT-OF-CENTRE of the main block, and labels the small
end block "Philo Carpenter Druggist". The three drawn views put the tall gabled
wing at ONE END of the main block with the log annex in front of that same end,
not mid-run. The views are the attested evidence and should win unless the run
finds a reason they cannot — but the run must SAY which reading it took, and why,
in the record. The sketch is the owner's intent about the relationship (main +
rear wing + a small end block); the images are the authority on where they sit.

The Carpenter question is real and is part of this ticket: is the log annex in
these views Philo Carpenter's drug store — which the preview labels on a log
building at this corner — or Mark Beaubien's retained 1829 cabin? They cannot both
be the same logs. Whatever the answer, it is a claim with a source, not a
convenience.

## The axes to read, each graded on its own

No dimension of this building is attested in prose. So the reading is
PROPORTIONAL: pick a stated scale datum in the views (the figures, the door
height, the storey height — say which, and what it was assumed to be), measure
against it, and carry the result as `inferred` where three views agree and
`reconstructed` where only one resolves it. The ratified ladder governs; a
single-view detail is graded the way T-0092 graded the shutter leaves.

- **Plan** — main block length and depth; the wing's length, depth, which end it
  attaches to and how far it projects; the log annex's size and where its walls
  meet the wing. The whole point is to retire the 12 × 8 placeholder.
- **Roof** — pitch of each mass (measure the rake against the eaves run), ridge
  heights relative to each other, eaves height, overhang at eaves and rake,
  covering (the views draw shingles, and the Petford draws them mossy).
- **Chimneys** — how many, which mass each stands on, where on the ridge, brick,
  and how far they stand proud.
- **The door** — position in the bay rhythm, the moulded architrave and the
  transom over it, whether there is a step or sill, and the small porch/hood the
  engraving suggests.
- **Windows** — bay count and rhythm on each visible face, sash pattern (the
  views draw 6-over-6), the shutters (colour is attested `bright_blue` from
  Wau-Bun; leaf type is the weak single-view claim already carded), and the gable
  light on the wing.
- **Siding** — clapboard course spacing on the frame masses, corner boards; and
  on the annex, log diameter, course count and the saddle-notch projection, which
  the Petford draws plainly.
- **The ground it meets** — the views draw a plank walk along the street face and
  posts at the kerb. `data/frontage/sauganash_frontage.json` already lays a walk,
  a crossing and two hitching posts here; check the reading against them rather
  than inventing a second set.

## Acceptance (stated before the work, and not weakened to pass)

1. A findings document under `docs/RESEARCH/` that records, per axis above, the
   measurement, which of the four views it came from, the scale datum assumed,
   and the grade — so the next run can argue with the numbers instead of redoing
   them.
2. `data/structures/sauganash_hotel.json` phase `frame_1831` carries the derived
   plan for BOTH masses in place of the 12 × 8 placeholder, with the placeholder
   note replaced by the derivation; every new attribute carries its own
   confidence and sources.
3. The log annex is sited where the views put it, and the record says what it is.
   Nothing log-built stands in front of the main block's street face.
4. The preview, at the Lake & South Water stand, reads as the three-part building
   the four views show: two storeys, two masses of near-equal ridge height, the
   annex at the end. A before/after pair of frames from the same pose goes on the
   PR.
5. `bash tools/check.sh` green, the smoke's Sauganash assertions updated to the
   new massing rather than deleted, and the bake re-run (`needs_bake`).

## Why it is L, and where it splits

Reading four plates to a stated scale datum is one demonstration; rewriting the
record, teaching `frame_tavern` a second mass and re-baking is another. Split on
that line: **the reading** first, **spending it into the record and the geometry**
second. The children take this ticket's place in the owner's order.
