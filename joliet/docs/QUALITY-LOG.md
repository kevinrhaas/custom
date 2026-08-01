# Quality log

Auditable record of every critic iteration: scores, the fixes they produced,
and the performance cost of those fixes.

## The protocol

A **separate agent that did not write the scene's code** scores each of the
scene's five fixed camera anchors 1–10 on eight axes, with written
justification and a specific actionable fix for every axis below 8:

1. Lighting & shadow — contact shadows, bounce, believable falloff, no leaks
2. Material realism — correct roughness/metalness, no plastic, layered wear
3. Texture detail & tiling — no visible repetition, appropriate texel density
4. Geometric detail & silhouette — bevels, trim, clutter, no naked boxes
5. Atmosphere — fog, motes, particulates, depth cueing, shafts
6. Post-processing — tone mapping, bloom restraint, grain, not over-processed
7. Composition & art direction — does the frame read, does it guide the eye
8. Historical & architectural accuracy vs `docs/RESEARCH.md` and reference photos

**Pass = mean ≥ 8.0 with no single axis below 7.**
**Hard cap: 4 iterations per scene.** Anything unresolved at iteration 4 goes to
`docs/QUALITY-BACKLOG.md` and the scene ships as-is.

### What the critic compares against

Reference photographs of the real Old Joliet Prison (the owner's site
photography, plus published documentation cited in `RESEARCH.md`), and
best-in-class real-time WebGL work it can name.

**Not** against commercial game frames. The original brief asked for a blind
side-by-side against Call of Duty. That test was dropped deliberately: the
frames cannot be legally obtained, so a critic claiming to have run it would be
fabricating its evidence — and an unsatisfiable exit condition reliably produces
either an infinite loop or a critic that starts rubber-stamping to escape. The
8-axis rubric above is a bar that can actually be held.

### Regression gate

Every iteration also records median FPS, draw calls and triangle count at all
five anchors. **A visual fix that drops any anchor below 60 FPS at `high` is a
rejected fix, not an accepted one.** Numbers below are captured under headless
SwiftShader (software rasterisation) unless marked otherwise — treat them as a
*relative* regression signal between iterations, not as the hardware target.
Hardware FPS is verified separately and noted where measured.

---

## Headlamp calibration — measured, not reasoned

`tools/light-calibrate.mjs` builds a bare scene (one flat lambertian surface,
the headlamp, every other light and the environment disabled), steps the camera
to 1 / 2 / 4 / 8 / 12 m and samples the centre pixel. Three runs:

| intensity | 1 m | 2 m | 4 m | 8 m | 12 m |
|---|---|---|---|---|---|
| 240, ambient 0.05 | 170 | 165 | 151 | 118 | 95 |
| **620, ambient 0.014** | **192** | **184** | 160 | 132 | 120 |
| 150, ambient 0.014 | 147 | 150 | 120 | — | — |

**Finding 1 — an ambient floor was flattening everything.** At the original
`scene.ambientColor` of 0.05/0.06/0.085, the lamp measured only 1.8x brighter at
1 m than at 12 m where inverse-square predicts ~36x. A distance-independent term
that large sits under every surface in the game: it is why night scenes read
flat, and it is a large part of why the headlamp appeared to "do nothing" — the
geometry was already lit before it arrived. Lowered to 0.014/0.017/0.026.

**Finding 2 — my target table was wrong, not the light.** The far-field bands
(5-25 at 12 m) assumed a roughly gamma response. With ACES and its strong
highlight shoulder, a 36:1 *linear* ratio compresses to under 2:1 on screen.
Scaling intensity by 4x (620 → 150) moved the 1 m reading only 192 → 147, which
is the shoulder dominating, not the falloff.

**Settled at intensity 620, emitter 1.2 m behind the eye, ambient floor
0.014.** That puts 1 m and 2 m in band and un-clipped, which is what The Void
needs — carved stone read at arm's length. The far field remains brighter than
intended.

**Open, honestly:** the residual flatness past 4 m is only *partly* explained by
the tone curve. Something is still contributing a near-constant term and I did
not isolate it before stopping. Candidates not yet ruled out: the per-material
`ambientColor = white` multiplier in `Materials.ts`, the spot's `range`
interacting with `FALLOFF_PHYSICAL`, or the exposure sitting the whole scene too
far up the shoulder. The rig now exists, so the next person can bisect this in
minutes rather than guessing — which was the point of building it.

## 1.1 Perimeter Approach

Nine iterations ran. **They were not scored to the protocol above**, and the
scene must not be described as having passed it. Iterations 1–8 were spent
finding and fixing hard breakage — scoring composition on a black or ghosted
frame would have been theatre. What follows is the honest record of what each
iteration found, because the bugs are more useful to the next scene than a
score would have been.

| # | What the capture showed | Root cause | Fix |
|---|---|---|---|
| 1 | Near-black frame; two giant skewed black wedges across the sky | `CubeTexture.CreateFromPrefilteredData` fails **silently** on a raw `.hdr` — it only accepts a prefiltered `.env`/`.dds`, so all IBL was lost while the scene still rendered. Separately, `scaling.y` applied to an already-rotated cylinder skews it. | Route `.hdr` through `HDRCubeTexture`; rebuild the gable from explicit slanted panes |
| 2 | Harness hung indefinitely, no output | Anchor settle loop drove `requestAnimationFrame`, which headless throttles for pages it treats as hidden, *and* called `scene.render()` by hand against the engine's own loop. Also: baking 18 materials at 1024² is tens of seconds of single-threaded JS. | Timer-based settle; `--disable-renderer-backgrounding`; bake at 512² and recover close-up frequency from the detail-normal overlay |
| 3 | Legible but massively underexposed; wall flat cream | PBR light intensities set as if they were 0–1 dials (moon at 1.35) | Moon 4.6, sky fill 0.95, env 0.75, exposure 1.45, sodium 1400 (physical falloff is inverse-square — 190 at 8 m was ~3) |
| 4 | Translucent panel smeared across the wall; ground in large shading facets | Alpha-blended double-sided cab glazing registered as a shadow caster; displaced ground plane with recomputed normals z-fighting a coplanar apron | Single-sided glass, `transparencyShadow = false`, flat base plane, lift apron clear |
| 5 | Ghost persisted | Not geometry — **TAA**. The temporal history survived the anchor teleport with no motion vectors to invalidate it, so the previous view stayed smeared permanently. | `disableOnCameraMove = true` + explicit `resetTAA()` on anchor change |
| 6 | Clean frame at last. Wall still smooth cream with horizontal banding only | Shared materials carried a **constant** UV scale, so an 88 m wall got 0.34 texture repeats — every large surface stretched into mush | World-space UV projection (`Kit.worldUV`): texel density now constant across the whole game, seams on face boundaries, no scene reasons about tiling |
| 7 | Coursing *still* absent despite correct UVs | `Texture.clone()` on a `RawTexture` does not reliably carry the pixel buffer — every material was sampling a flat clone | Stop cloning; each preset owns its own baked set, so scale it in place |
| 8 | Coursed ashlar reads fully. Stone too pale and too regular vs reference | Rock-face relief amplitude too low; blotching and runoff thresholded almost out; moon desaturating the limestone to grey | Relief ×2.3, normal strength 2.6→4.4, widen blotch/runoff thresholds, warm the key |
| 9 | Final capture of this session | — | Metric fix: `engine._drawCalls.current` accumulates across frames rather than resetting, so every draw-call number logged before this point was meaningless. Replaced with active-mesh count. |

### Standing regressions and caveats

- **All FPS figures are headless SwiftShader** — software rasterisation, 1–2
  orders of magnitude slower than any GPU. Valid as a relative signal between
  iterations, worthless as an absolute. **The 60 FPS constraint is unverified on
  real hardware.**
- Draw calls are not measured. Active mesh count is the proxy; the scene is
  mesh-heavy (per-voussoir, per-rubble-block meshes) and will need merging
  before the 1,200 draw-call budget can be claimed.
- Triangles ≈ 90k against a 3M budget — geometry is nowhere near the limit, so
  detail can be spent freely.
- Zero page errors across all iterations.

### Iterations 10–13 — the trench, and two lighting bugs

| # | Found | Fix |
|---|---|---|
| 10 | Ground aperture works — the trench is a genuine hole now, not walls standing on an unbroken floor. But `a5` is unreadable: too low, too close, almost entirely dark. | `buildGround` takes aperture rectangles and drops triangles whose centroid falls inside; coping stones hide the cut edge |
| 11 | Reframed `a5` to look at the trench from the approach. **Still black.** No headlamp cone anywhere, in any anchor, ever. | — |
| 12 | `PBRMaterial.maxSimultaneousLights` defaults to **4**. The scene has moon + sky + two sodium lamps + headlamp = 5, so the headlamp — *the player's primary light source in every interior scene in the game* — was being silently dropped by every material. | Take the light budget from the quality tier |
| 13 | Still dark, so the light cap was not the only cause: the headlamp uses `FALLOFF_PHYSICAL`, which is inverse-square, and was set to intensity 42. That delivers ~1.7 at five metres against a moon key of 4.6 — present, but invisible. Exactly the same units error already fixed on the sodium lamp in iteration 3. | Intensity 42 → 900 |

**The lesson worth carrying:** every light in this project that uses physical
falloff has been set at least an order of magnitude too low on first authoring,
because the number *looks* like a 0–1 dial and is not. Check any new light
against the sodium lamp (1400) and the headlamp (900), not against the moon
(4.6, directional, no falloff).

### What the next iteration should do

Run the **actual protocol**: independent critic, eight axes, five anchors,
written justification, specific fix per axis below 8. The frame is finally
stable enough for that to mean something. Expect it to score hardest on
*atmosphere* (no volumetrics wired) and *geometric detail* (no foliage, no
clutter).
