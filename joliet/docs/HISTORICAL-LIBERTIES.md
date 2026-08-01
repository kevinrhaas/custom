# Historical liberties

Every place where gameplay, performance or narrative wins over strict accuracy,
and why. This document is append-only — add entries, never rewrite them.

The standard this project holds itself to: **a visitor who has taken the Old
Joliet Prison tour should recognise every room, and should be able to tell you
which parts we made up.** Anything invented is listed here.

---

## 1. Framing and premise

| Liberty | Reasoning |
|---|---|
| The entire scenario is fictional. | The game is presented as *sanctioned after-hours access* granted for documentation purposes. No dialogue, UI text or marketing copy encourages, instructs or romanticises real-world trespass. The site is an operating museum with paid public tours; that is the legitimate way in and the end cards say so. |
| The four crew members are fictional composites. | They are not portrayals of real, identifiable people. Any resemblance to specific urbex personalities is unintended. |
| The sealed sub-level beneath the east cell house ("the Void") is **invented**. | It is the game's climax and its thematic payload. There is no documented sealed punishment level at Joliet. See §3 below — this is the single largest invention in the project and it is deliberately signposted in-game as a *fictional* discovery in the end cards. |

## 2. Architecture and site

| Liberty | Reasoning |
|---|---|
| **The site is compressed.** The real site is ~72 acres; the playable map is roughly 400 × 300 m with buildings pulled closer together than reality. | A faithful footprint would be several minutes of empty walking between beats. Relative *orientation* (Collins Street east, canal/rail corridor west, admin block centre, cell houses flanking) is preserved. |
| **Building interiors are simplified in plan.** Cell counts, exact tier lengths and room adjacencies are approximate. | Full fidelity would blow both the triangle budget and the schedule. Tier heights, cell dimensions, bar spacing and catwalk profiles are held to reference. |
| **The "glass-panelled central guard tower"** in the original outline is **not a liberty at all — it is a real building we initially failed to identify.** Scene 4.1 uses the **Yard Tower (Tower #12, 1940)**: round brick, standing at the literal centre of the yard, with a glazed observation drum and a low metal dome. | Research (`RESEARCH.md` §8) found that Joliet already has exactly the building the outline was reaching for. Better still, it has **no exterior door** — the only access was an underground tunnel from the Collins Street tunnel system, which flooded and was sealed. That is a *free* gameplay mechanic that the fictional version would have had to invent. The outline's phrasing sounded like Stateville's roundhouse; the answer was to look harder at Joliet, not to compromise. |
| The Yard Tower's **interior** is invented. | No interior documentation was found. |
| **The industrial shops are presented in their burned, roofless, tree-grown state**, with the powerhouse still enclosed. | Both conditions are real, but they are not from the same year. Presenting them simultaneously is a compression of the decay timeline. |
| Guard tower positions are **approximate**. | Exact surveyed tower coordinates could not be established from public sources. |
| **Perimeter wall height** is modelled at ~10 m (33 ft). | Research corrected a popular-source error here: 25 ft is the *1857 design specification*, which nearly every secondary source repeats. The wall **as built** is 32–35 ft (`RESEARCH.md` §2). The game uses the as-built figure. |
| The **"Yard Department" building** is labelled as such in-game. | It is really the **Mule Barn**; "YARD DEPARTMENT" is a later painted sign over its doors. The sign is real and photographed, so the game keeps it — but the building is identified correctly in the collectible text. |
| The dining hall is presented with its **1987** construction date and decorative band. | An earlier draft assumed the brown/orange striped band was 1970s. The building is 1987; the band is original to it. |
| Upper-tier gallery floors are **steel bar grating**, not concrete. | Corrected from NRHP survey photography, which contradicts the nomination's own blanket description of the floors. The grating matters — it is why footsteps carry the way they do in 3.1. |
| The dining hall's 1970s decorative band (brown/orange/tan stripes with a spiral motif over glazed block) is reproduced; **the murals on its walls are original artwork in a similar Chicago-crew idiom, not copies.** | The real murals are works by named, living graffiti writers, and one references a licensed film. Reproducing them would copy identifiable third-party artwork. The *fact* of a sanctioned mural programme is historical and is preserved. |
| The chapel's parabolic roof, exposed timber rafters, diamond-leaded apse window and the Ezekiel 18:31 lintel are reproduced closely. | These are strongly documented and highly distinctive. Edward Dart, 1966. |

## 3. Underground — the largest invention

**Documentation for Joliet's below-grade services is thin.** Research
established the existence of utility tunnels and steam distribution in general
terms but could not establish plans, dimensions, or extents.

Therefore:

- **The Siphon** (drainage/culvert route, chest-deep water, shifting cinder
  blocks) is **invented level design** on a plausible armature — prisons of this
  era and this site's canal-adjacency did have substantial storm drainage.
- **The Void** (sealed vaulted sub-level beneath the east cell house, hand-cut
  stone, inmate names carved by the quarrymen) is **entirely fictional**.
- The 1858 Boyington-office drawing showing an unrecorded "cistern", and its
  disappearance from post-1910 surveys, is **a fictional document invented for
  the plot**. No such drawing is known.

The *historical claim underneath the fiction* is true and is the reason the
scene exists: **the prison was built with convict labour from limestone the
inmates quarried on-site.** The men who were held there cut the stone that held
them. That is documented. The sealed level dramatises it; it does not report it.

The game's end cards state this distinction explicitly to the player.

## 4. Gameplay-driven

| Liberty | Reasoning |
|---|---|
| Restoring partial power in the Powerhouse turns lights on across the whole map. | A large, satisfying, earned world-state change. In reality the site's power was cut long ago and a boiler sequence would not re-energise anything. |
| Ambient wildlife, structural collapse and water levels are choreographed to beats. | Tension without combat has to come from somewhere. |
| Traversal uses forgiving hitboxes and ledge-snap assist. | "Fun and not too hard" is a spec. See docs/DESIGN.md. |
| No instant-fail states anywhere. Detection warns twice; a missed water-balance check costs stamina and makes noise. | Same. |
| Radio contact with the other three crew members is continuous, with diegetic dropout at depth. | Solves the "where did everyone go" problem and carries the history through argument rather than monologue. Real radio through this much limestone would be far worse than depicted. |

## 5. Materials and lighting

| Liberty | Reasoning |
|---|---|
| All surface textures are **procedurally generated**, not photogrammetry of the real building. | Licence-clean, tiny, and lets wear follow geometry. Colours are calibrated to reference photography — see `docs/RESEARCH.md` § palette and `src/core/Palette.ts`. |
| Night lighting is **brighter than a real moonless night**. | An accurate midnight interior would be an unplayable black screen. The game leans on a low moon key, sodium spill and headlamp, with raised ambient. This is the standard convention and it is a deliberate choice. |
| Sodium yard lamps still function. | Most site lighting is dead. Two working lamps give the frame its warm/cool split and its navigation cue. |

---

*Every item above is a decision, not an oversight. If something looks wrong and
is not on this list, it is a bug — please file it.*
