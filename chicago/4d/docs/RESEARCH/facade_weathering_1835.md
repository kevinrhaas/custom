# The finish on a wall in 1835 Chicago, and what the model was drawing instead

**Parcel:** ROADMAP § K4, first slice. **Date:** 2026-08-13.
**Outputs:** `renderers/web/js/facade.js`, `docs/LIBERTIES.md` L91, six assertions in
`tools/smoke_renderer.mjs`.

The owner's finding, verbatim: *the buildings read as freshly painted and identical*. This memo
records what the dataset already said about that, what it did not say, and which of the numbers
now in the renderer are readings and which are inventions.

---

## 1. What the records already state

`paint` has been a form attribute since the schema was written, and it is authored on **174 of
the scene's 243 phases**:

| value | phases |
|---|---|
| `unpainted` | 142 |
| `whitewash` | 14 |
| `red` | 12 |
| `brick` | 2 |
| `earth` | 2 |
| `stone` | 1 |
| `white` | 1 |
| *(absent)* | 69 |

Graded: **163 `derived`, 9 `inferred`, 2 `documented`** (in the post-K16 vocabulary). The two documented ones are the
Sauganash's white — Wau-Bun's white frame building with bright-blue shutters — and St Mary's.

So the distribution the parcel asks for is not a research gap: the dataset already says this was
an overwhelmingly unpainted town, and it says so per building with a note per building. What it
did not have was any consequence.

## 2. What the dossiers say the result looked like

Three passages, all committed, all pre-dating this slice:

- **The fort.** *"no source reports dilapidation before the late 1830s; the fort was still an
  active, maintained post in 1835… Model as **serviceable, weathered, whitewashed/unpainted
  log-and-brick**."* `[INF]` — `docs/research/04-structures-south.md` § Fort Dearborn, condition
  1835.
- **The Dearborn Street bridge.** Repaired in 1834 and again in 1835, struck repeatedly by
  vessels, the draw jammed for 48 hours on one occasion: *"Model as **weathered, patched,
  sagging**."* — ibid., § the bridge, with the repair payments cited to Andreas I and chicagology.
- **The Green Tree, and the argument in one sentence.** `docs/RESEARCH/green_tree_tavern.md` § 4
  corrects a claim in circulation that the Green Tree was whitewashed — Gale's testimony is about
  the *interior* walls and partitions — and states why the correction matters visually: it is
  *"the difference between a white building and a weathered one standing a block from the
  Sauganash, whose white paint was remarkable precisely because its neighbours were not."*

That last is the whole of K4's evidence base, and it was already written down. **The Sauganash's
white is legible as remarkable only if the town around it is not.**

## 3. What the renderer was drawing

`generators/common/mesh.py` holds one table:

```
PAINT_RGBA = { "white": (0.90, 0.89, 0.85), "unpainted": (0.52, 0.44, 0.34),
               "whitewash": (0.88, 0.87, 0.83), "red": (0.55, 0.16, 0.13) }
```

Every archetype resolves the record's value through it, so all 142 unpainted phases baked the
same warm fresh-sawn tan, and `buildings.js` then collapses materials that render identically
into one `BatchedMesh` each — which is what keeps 242 structures inside an 80-draw-call budget.
Both halves of the owner's sentence follow from those two facts. Neither is a bug.

## 4. Why the fix is in the renderer and not in the bake

Two reasons, and the second is the one worth keeping.

**The budget.** Per-building colour variation baked into materials is per-building materials, and
therefore per-building draw calls: 242 against a budget of 80. Variation has to ride inside the
shared batch as a per-vertex channel — the shape `_CONFIDENCE` already has.

**The palette pass.** The obvious implementation tints each surface toward a chosen weathered
grey, and to avoid greying out glazing and window voids it would have to know which surface it
was looking at. The generators name their materials (`wall`, `log`, `roof`, `glass`, `dark`,
`chinking`, …), so that looks free. It is not available where it counts:

| | materials | primitives |
|---|---|---|
| `assets/gltf/sauganash_hotel__frame_1831.glb` (master) | `wall`, `roof`, `log`, `shutter`, `glass` | 5 |
| `assets/web/…` and `site/chicago/4d/data/gltf/…` (published) | `PaletteMaterial001–003` | 3 |

`tools/bake.sh` runs gltf-transform over `assets/web/`, and its palette pass merges materials and
moves their colours into a texture. **38 of the published building assets are in that state.**
`tools/smoke_renderer.mjs` loads the masters from `assets/gltf/`; the live site loads the
derivatives from `data/gltf/`. A renderer keyed on material names would therefore be gated on one
pipeline and shipped on another — the exact failure `docs/STATUS.md` records for the nightly bake
gate ("a green local gate was reporting on a pipeline it was not running").

So the rule reads no names and no colours. **Weathering here is the removal of colour**: each
fragment is mixed toward its own Rec. 709 luminance. A tan board goes grey-brown, a shingle roof
greys, and a near-neutral window void moves by almost nothing because it has almost no colour to
lose. The surfaces that would have needed protecting protect themselves, arithmetically, in both
pipelines. This is recorded here because it constrains future work as much as this slice: **any
per-surface facade treatment is blocked until the derivative carries surface identity**, which is
a change to `tools/bake.sh` and to `docs/GLB-CONTRACT.md` and therefore a proposal, not a slice.

## 5. The rules, and which side of the line each is on

| input | source | grade |
|---|---|---|
| the finish | the record's `attributes.paint` | as the record grades it |
| how long it had stood | `documented_range.from` against the scene's `target_date` | as the record grades it |
| travel per finish — `unpainted` 0.80, `whitewash` 0.35, `white`/`red` 0.18, masonry 0.00 | invented | L91 |
| the 0.55 floor and the 8-year saturation | invented | L91 |
| the ±7.5 % per-building lightness spread | invented | L91 |

Three rules govern the edges.

**1 — a finish that cannot silver, does not.** `brick`, `stone` and `earth` weather, but not by
going grey the way bare timber does, and this treatment has no vocabulary for what they do
instead. They get an honest zero. So do the 69 phases that state no finish at all.

**2 — age is a lower bound and is used as one.** `documented_range.from` is the first date a
record *claims* the phase existed. That is on or before the date it was built and never after, so
the age term may only ever ADD to a floor every building of that finish already carries. **173 of
the scene's 242 structures carry a range that opens inside 1835 itself** — overwhelmingly the
inferred-infill roofs, for which nothing is known about when they went up. They stand within half a
year of the scene date, so the age term adds at most 3 % of their finish's travel; the 69 whose
ranges open earlier, back to 1816, are the ones it moves. Years standing across the scene run 0.06
to 19.0, and unpainted silvering therefore spans 0.462 to 0.800.

**3 — a documented finish is drawn as documented.** The Sauganash and St Mary's get neither the
silvering nor the tone offset. This leaves St Mary's, whose documented finish is `unpainted`, as
the one unweathered unpainted building in the town. That is accepted rather than special-cased:
the alternative is a rule with a clause in it for a case no visitor can see, and the general
principle — where a source states the colour, the colour it states is what is drawn — is worth
more than the exception costs.

**The per-building offset is keyed on the structure id, not on position.** Almost every
coordinate in this dataset is symbolic and moves as research lands. A building that changed colour
because its position was corrected would be reporting a research result as a repaint.

## 6. Measured

Against the 242 committed sidecars of the 1835 scene:

- **141 unpainted, undocumented phases** silver between **0.462 and 0.800**; **167 structures**
  carry a non-zero silvering; 5 masonry and 68 finish-less structures carry none.
- **Tone spread 0.1406** across the scene, peak **0.0715** against the ±0.075 bound.
- **128 generated roofs** — the ids that would betray a weak hash, sharing 22 leading characters
  — take **127 distinct tones**. One collision.
- Silvering is monotonic in years standing across the whole unpainted set, by construction and by
  measurement.
- **Draw calls unchanged.** The channel is two floats per vertex inside the existing batches.

## 7. What this does not do

It does not vary anything *within* a wall: board tone, board width, hewn-versus-round logs and
weathering by elevation are all archetype work and all still open under K4. It does not repaint
anything — the finish drawn is the finish the record already claimed (`derived` on 163 of the 174
phases that state one, `inferred` on 9), and no confidence grade moved. And it is not evidence: nothing in § 5's invented column is a reading of a source, which is
what L91 exists to say.
