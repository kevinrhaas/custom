# Art bible

The frozen look. Every scene composes from this; no scene authors a new base
material or a new light type without changing this document first.

---

## 1. The one-line brief

**A moonlit, overcast midnight at a decayed limestone prison, photographed on a
fast sensor.** Not a horror film. Not a music video. The building is beautiful
and it is not trying to frighten you; it is simply very large, very old, and
completely empty.

## 2. The lighting rig

Three sources carry the entire game. Everything else is bounce.

| Source | Colour | Role |
|---|---|---|
| **Moon** — one directional light, the only full-strength shadow caster | `#8fa6c4` cool but not cartoon-blue | Key. Kept **low** (≈25° elevation) so it rakes across the rustication. A high moon flattens the stone and kills the frame. |
| **Sodium vapour** — the two surviving yard lamps | `#ffb765` | The warm half of the frame's warm/cool split, and the navigation cue. Slow instability: two detuned sines plus a rare dropout. |
| **Headlamp** — spot, parented to the camera | `#fff2d6` slightly green, like real LEDs | Offset 11 cm left and 9 cm below the eye. **Never coincident with the view axis** — coincident light kills all shadow cueing and every surface reads flat. Uses a generated cookie with a hot centre, soft corona and faint reflector rings; a perfectly smooth cone is the loudest "this is a game engine" tell there is. |

Plus a hemispheric fill at 0.34 with a **cool sky and a warm ground** (`#57699e` /
`#292520`) — the ground bounce comes off asphalt and dead grass, so the two
hemispheres must differ — and an HDRI environment at 0.32 for specular.

**Rules**
- The shadow side is never pure black. Pure black reads as unfinished, not dark.
- Exactly one shadow-casting directional. Spots cast only where a scene proves
  it earns the cost.
- Night is rendered brighter than a real moonless night. This is deliberate and
  listed in `HISTORICAL-LIBERTIES.md`.
- The powerhouse restoration in 2.1 adds `#ffc98a` incandescent strings across
  the map, permanently. Scenes must look composed both before and after.

## 3. The post chain

Restrained on purpose. This is a real place.

| Stage | Setting | Why |
|---|---|---|
| Tone mapping | ACES, exposure 1.05, contrast 1.12 | |
| AA | TAA (8 samples, factor 0.06) above medium; FXAA below | TAA is what stops the barbed wire and the cell bars crawling, and those are in almost every frame |
| Bloom | threshold **0.86**, weight 0.34 | Only the sodium lens and the headlamp hotspot are genuinely bright. Nothing else may glow. If stone is blooming, the threshold is wrong. |
| SSAO2 | radius 1.1, strength 1.15 | The interiors are almost all soft indirect light; without AO the corners flatten and everything reads as cardboard |
| Grain | 9 × user scale, animated | Sells the low-light photographic read. A perfectly clean night frame looks synthetic. |
| Chromatic aberration | 6.5, radial 0.75 | Barely perceptible. If you can name it, it's too strong. |
| Vignette | weight 2.4, near-black | |
| Sharpen | edge 0.22 | Recovers the softness TAA + grain introduce |
| Motion blur | camera-based, 0.55 | **Off entirely under reduced-motion.** Accessibility, not preference. |
| Depth of field | **off** during traversal | Fights readability in a dark corridor. Scenes enable it only for scripted looks. |

Specular anti-aliasing is on for every material. Without it the wire, the bars
and the corbel edges shimmer at 1080p.

## 4. Materials

The library is `src/core/Materials.ts`. **Scene agents call `mats.get(id)` and
may override tiling. They do not author base materials.** That rule is the only
thing standing between "one building" and "eight inconsistent demos".

| Preset | Calibrated against | Authored range |
|---|---|---|
| `limestone.wall` | The wall plate: irregular course heights, pale-cream/warm-gold/grey block mix, black blotching in patches, heavy staining at grade | courses 6–8, rustication 0.85–0.95, soiling 0.45–0.6 |
| `limestone.tower` | Tower shafts — finer ashlar, cleaner, sheds water | courses 10–12, rustication 0.5–0.6, runoff ≤0.3 |
| `limestone.wet` | Trench and below-grade — saturated, mossy, much darker | wetness 0.7–0.85 |
| `paint.cell` | The cell-interior stratigraphy: cream → mustard → blue-grey → sage → bare block, with **lifted flake edges** | decay 0.55–0.7 |
| `paint.corridor` | Less advanced failure, traffic grime at hand height | decay 0.25–0.4 |
| `paint.ceiling` | Catastrophic delamination, sheets hanging down | decay 0.88–0.95 |
| `steel.cellFront` | Oxide-brown enamel over heavy orange rust bloom | corrosion 0.6–0.75 |
| `steel.door` | Institutional red oxide over grey primer, chipped | corrosion 0.35–0.5 |
| `concrete.floor` | Corridor slab **foot-polished** in the traffic lane | polish 0.65–0.8 |
| `tile.corridor` | Glazed structural tile — the one genuinely glossy surface | decay 0.3–0.45 |

### The three material rules

1. **Rust is not metal.** Metalness goes to ~0 wherever rust wins and roughness
   goes to ~0.95. Only intact paint and bare steel keep metalness. This is the
   single most common PBR error and it is instantly visible.
2. **Roughness contrast is the story.** Intact enamel is semi-gloss at 0.42;
   the exposed layers under it are matte at 0.62–0.94. That *difference* is what
   makes flaking paint read as paint rather than as a printed pattern.
3. **Wear follows geometry, never uniformly.** Runoff starts at the cap. Grime
   sits in joints and at the base. Paint fails where water gets in — high on the
   wall and along the joints. Nothing is evenly distributed.

## 5. Geometry

- **No naked boxes in the frame.** Every large mass gets a trim, a sill, a
  corbel or a cap. Boyington's vocabulary is small and repetitive, which is why
  `Kit.ts` generates it parametrically.
- **Openings need depth.** A window is a recessed reveal + a sloped sill +
  voussoirs + bars. A flat texture of a window reads as a sticker at any range.
- **Slack, not taut.** Barbed wire sags between every post. Straight lines read
  as CAD; that catenary is most of the silhouette against the sky.
- **Break symmetry.** Towers and lamps sit off-centre. Symmetry reads as level
  design, not as a real site.
- Thin instances for anything repeated more than ~20 times (corbels, bars,
  wire posts, mullions, merlons).
- Static architecture gets `freezeWorldMatrix()`.

## 6. Composition

Every anchor frame should answer: **where am I, where do I go, and what is this
place?**

- Hold a **warm/cool split** wherever a practical light exists. That contrast is
  both the beauty and the navigation cue — in 1.1 all three entries are *away*
  from the light.
- Lead the eye with the wall line, the corridor perspective, or the tier rail.
  The corridor shots in reference work because the vanishing point does the job.
- Keep a dark foreground element for depth. The frame needs something to be in
  front of.
- Fog is depth cueing, not weather. Exponential-squared at 0.0125, tinted to the
  sky, so distance reads without the scene going milky.

## 7. Budget

| | |
|---|---|
| Frame | ≤16.6 ms (60 FPS) at 1080p on a mid-range dGPU; ≥30 FPS on Iris Xe |
| Draw calls | ≤1,200 |
| Triangles | ≤3M visible |
| GPU memory | ≤1.5 GB |
| Load | ≤15 s to playable; total build ≤250 MB |

**A visual fix that drops any anchor below 60 FPS at `high` is a rejected fix.**
Ship a locked 60 over a prettier slideshow, every time.
