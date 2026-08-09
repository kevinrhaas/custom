# Liberties taken

**Append-only.** Every compression, simplification, and invention gets a row. Nothing is ever
removed from this file; if a liberty is later resolved by evidence, add a line saying so.

The standard, borrowed from the Joliet project in this repo:

> A visitor should be able to tell you which parts we made up.

The per-attribute confidence model in the data covers *attributes*. This file covers the
decisions that do not live in any single attribute — scope, scale, omission, and the choices a
reader would otherwise have to reverse-engineer.

---

## Standing liberties

### L1 — No people, anywhere
**Decision:** version 1 ships with no human figures of any kind.
**Why:** the final removal of the Potawatomi from Chicago occurred in August 1835, inside the
target year. Depicting Native presence is not a research gap to be filled by inference; it
requires consultation (see `AGENTS.md`). Rather than depict some people and not others — which
would itself make a claim — the scene is uniformly unpopulated. An empty, accurate town is
honest; a populated, invented one is not.
**Consequence:** the town reads quieter than it was. Chicago in July 1835 held roughly 3,265
people and was booming. The absence is a deliberate statement of scope, not an estimate of
population.
**Recorded:** 2026-08-09.

### L2 — Fauna presented at low density, and often as sound only
**Decision:** ambient wildlife is rendered sparsely, with many species present as audio or as
traces (tracks, feeding sign) rather than animated animals.
**Why:** two reasons, both evidential. July is the quietest wildlife date in the Chicago year —
no migration, silent leks, moulting waterfowl — and a summer scene populated with the spectacle
of *other* seasons would be wrong. And a boomtown of 3,265 people is not a wilderness; wild
animal density inside the platted grid was low.
**Recorded:** 2026-08-09.

### L3 — Vertical exaggeration available but off by default
**Decision:** the renderer may offer a vertical-exaggeration toggle; it defaults to off.
**Why:** total natural relief across the entire modeled area is under fifteen feet. Flatness is
the single most important fact about this landscape and the reason the city later had to raise
itself out of the mud. Exaggeration aids legibility and falsifies the experience, so it is opt-in
and clearly labeled.
**Recorded:** 2026-08-09.

---

## Per-subject liberties

### L4 — Sauganash Hotel: the gallery question, and how it was decided
**Decision (revised same day):** **no** gallery, tagged `inferred`.
**Why:** no period source attests one either way. The first reading followed the secondary
literature, which describes the surviving retrospective images as disagreeing, and modelled a
gallery as `conjectural`. Examining the two images the project actually holds — the Braunhold
engraving in Andreas (1884) and Kurz & Allison panel 14 (1893) — showed both depicting the
building with **no** veranda. Since the Kurz & Allison composition is probably copied from
Andreas, that is one witness and a copy rather than two, so the finding is `inferred`, not
`documented`.
**Worth noting as a process point:** the correction came from looking at the pictures instead of
reading about the pictures. Both are in the repo and both were a minute's work to open.
**How to resolve further:** any pre-1860 depiction or a written description.
**Recorded:** 2026-08-09. **Revised:** 2026-08-09.

### L4a — Sauganash Hotel: the log wing is inferred from two derivative images
**Decision:** the 1829 log cabin is modelled as an attached single-story wing on the 1831
building, tagged `inferred`.
**Why:** both retrospective depictions draw it plainly, with log courses and corner notching,
and it matches the documentary account that the frame block was "built onto" the cabin. But the
two images are not independent, and neither is a period record.
**Consequence:** the `frame_tavern` archetype has to support an attached log wing — a Milestone 0
geometry requirement that came out of the evidence rather than the plan.
**Recorded:** 2026-08-09.

### L5 — Sauganash Hotel: both footprints are invented
**Decision:** placeholder rectangles (7×6 m log, 12×8 m frame), tagged `conjectural`.
**Why:** no dimensions are attested in any source reached. The rectangles are plausible for the
type and carry no evidence whatsoever.
**How to resolve:** Andreas vol. 1 p. 106 at page-image level; then the Hathaway 1834 building
rectangle once the datum is verified.
**Recorded:** 2026-08-09.

### L6 — Sauganash Hotel: the pre-1830 position is not represented
**Decision:** the `log_1829` phase is placed at the post-move Lake & Market site for its whole
span, although the cabin stood somewhere else until about 1830.
**Why:** the original site is described only as "near the forks, on the south side" and as
having fallen inside a platted street — not precisely enough to place. Splitting the phase would
require inventing the first position.
**Recorded:** 2026-08-09.

---

## Resolved

*(none yet — entries move here with the evidence that settled them, and stay in place above)*
