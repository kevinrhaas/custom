# ROADMAP

The build order and the work parcels. `docs/PLAN.md` carries the full reasoning; this is the
operational view — what to pick up next, and what it depends on.

```
S0 scaffold ─┬─► S1 georeference + datum ──► S2 terrain e1834 ──► S3 M0 Sauganash walkable
   [DONE]     ├─► R1 renderer shell (synthetic geometry) ────────┘
              ├─► P1 research dossiers (read-only) ──► S5 structure records ──► S8 M1
              └─► S4 archetype generators (golden params) ──────► S5 bakes
S2 ──► S6 flora + fauna ──► S7 polish, audio, perf ──► release sweep
```

**Critical path: S1 → S2 → S3.** The datum gates every coordinate in the project. Work that does
not need coordinates is deliberately structured to proceed in parallel.

---

## S1 — Georeference and verify the datum · **NEXT, blocking, do serially**

The single most consequential task in the project. Everything regenerates if the origin moves.

| | |
|---|---|
| **Inputs** | BPL Wright 1834 GeoTIFF (open rights, already georeferenced) · LOC Hathaway 1834 JP2 (6536×9318) · Thompson 1830 plat dimensions (80-ft streets, 18-ft alleys) |
| **Method** | Warp against surviving PLSS section-line geometry legible in the modern street grid. **Do not warp against buildings** — the buildings are what we are trying to locate. |
| **Outputs** | `data/traces/allmaps/*.json` (W3C georeference annotations) · `data/traces/gcp/` · `datum.json` with `origin_utm_e/n`, `verified: true`, method, residuals, who and when |
| **Gate** | `tools/check.sh` green + a written derivation memo a reader can check |
| **Watch** | The LOC catalogs Hathaway as "[1820?]" — a cataloging error. Record the discrepancy; do not silently correct it. |

## S2 — Terrain, epoch `e1834_harbor_cut`

Parcels (parallel once S1 lands):

- **(a) Shoreline + river vectors** — banks, the 1834 cut, the decaying old southward channel behind the sand tongue, the accretion wedge north of the north pier.
- **(b) Heightfield** — the 30-zone table in `docs/research/01-terrain-hydrology.md`, quantized ≤0.25 ft at 5–10 ft cells. Z=0 at the 1835 lake surface.
- **(c) Hydrology** — the slough (public-square pond → past Lake & Dearborn → river at the foot of State), Frog Pond at Lake & LaSalle, the Wells Street marsh, the marshy river-shore strip.
- **(d) `terrain_gen.py`** — spec + vectors → terrain mesh + `heightfield.bin` for collision.

Reminder: piers and bridges are **structures with phases**, not terrain (see `docs/EPOCHS.md`).

## R1 — Renderer shell · *can start now, needs no datum*

Parcels: (a) shell + input-intent layer + walker; (b) confidence shader + provenance popup
against a hand-written test sidecar; (c) `tools/smoke.mjs`.

Build against synthetic geometry and flat ground. Contract in `docs/PLAN.md`. Mobile
(390×780) is a release gate from the first walkable commit — retrofitting touch into a 3D
walkthrough later is the expensive way to do it.

## S3 — Milestone 0: the Sauganash, end to end

Definition of done in `docs/PLAN.md`. The record, the sources, and the dossier are already
written; what remains is the `frame_tavern` archetype, the first bake, and the walkable page
with a working confidence toggle.

Success is not "a building appears". Success is that a viewer can toggle the confidence view
and see exactly which parts of the Sauganash we can defend — the white two-story block and the
blue shutters solid, the invented footprint and the disputed gallery dithered.

## S4 — Archetype generators

One parcel per archetype, each with a golden-parameter GLB and a reference shot:

`frame_tavern` · `frame_storefront` · `frame_dwelling` · `log_dwelling` · `institutional` ·
`fort_structure` · `outbuilding` · `plank_walk` · `bridge_timber` · `pier_crib` · `palisade`

Balloon-frame logic (stud spacing, sheathing, proportions) is a first-class requirement, not a
detail: 1833–35 Chicago is where balloon framing was invented, and it is the first thing a
knowledgeable viewer checks.

## S5 — Structure records

Per-cluster parcels, each one file per structure so parallel agents never collide:

| parcel | contents |
|---|---|
| Wolf Point west bank | Wolf Tavern (painted wolf sign), Green Tree, Western Hotel, James Kinzie house, R. A. Kinzie store |
| North bank | Miller House, Miller tannery, Cobweb Castle, Walker's meeting house, Steamboat Hotel, Lake House (under construction) |
| South Water blocks A–G | the block-by-block sketch in `docs/research/04-structures-south.md` is the work order |
| Lake Street | Tremont House I, Mansion House, Exchange Coffee House, St. Mary's, First Presbyterian, Thomas Church store |
| Civic square | estray pen, log jail, courthouse (under construction, month unfixed) |
| Fort Dearborn | palisade, blockhouse, bastion, magazine, quarters, barracks, sutler, hospital, parade, gardens |
| Harbor works | north pier, south pier, the cut, the lighthouse, wharves |

## S6 — Flora and fauna

Per-zone parcels from the dossiers: 10 flora zones, 7 fauna zones. Honor the July phenology
rules — big bluestem is vegetative in July, cordgrass is the tall flowering element, ramps are
leafless scapes. Negative findings (no ring-billed gulls, no beaver, no periodical cicadas) go
into the data as `absent` entries with citations, so nobody re-adds them later.

## S7 — Polish

Performance against the budgets, licensed ambience audio, provenance-popup UX, `LIBERTIES.md`
completeness pass, mobile release gate.

## S8 — Milestone 1

Wolf Point cluster + South Water block D (LaSalle–Clark). The first test of whether the
archetype approach actually pays for itself.

## Later — the 4D proof

A second scene (1833 or 1830) exercising the epoch machinery, the `pre_fire_v1` crosswalk, and
a Manager row with the changelog cadence running.

---

## Working notes

- `tools/check.sh` before every commit. It takes under a second.
- One coherent unit of work per run.
- Writing subagents each get their own git worktree.
- Update `STATUS.md` in the same commit as the work, and keep it unflattering.
- No model identifiers in repo artifacts.
