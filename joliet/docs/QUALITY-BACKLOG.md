# Quality backlog

What did not reach the bar, and what it would take. Written honestly — an
accurate status report is more useful than a flattering one.

Each item: what's wrong, what it would cost, and how much it matters.

---

## RESOLVED — the headlamp works; its falloff was miscalibrated

The P0 logged here ("the headlamp illuminates nothing") was **wrong about the
symptom**. Building The Void proved the light renders fine: in an interior with
no practical lights of its own, it lit the room — and blew a white hole in the
middle of every frame.

What was actually true:

- Three real bugs were found and fixed on the way (a 4-light material cap, an
  intensity set as if inverse-square falloff were a 0-1 dial, and materials
  frozen before the player existed so their shaders never saw the new light).
  All three were genuine. None was the reported symptom.
- The symptom in scene 1.1 was **an unlit corner plus a dominant moon key**, not
  a broken light. The trench simply has nothing lighting it, which is
  thematically correct and photographically unhelpful.
- Then intensity 900 **overcorrected**, which is what The Void's captures show.

The real problem is the shape of the curve, not the value. Inverse-square from
an emitter at the eye means a wall at 2.5 m and a wall at 8 m differ by 10x, so
no single intensity lights both. Current fix: move the emitter **1.2 m behind
the head** (3.7 m vs 9.2 m — a 6x ratio) and drop intensity 900 → 240.

**Still not calibrated.** This is reasoned, not measured. It needs a proper pass
against a test chart at 1 / 2 / 4 / 8 m, and a near-field clamp would be better
than the pull-back trick. Until then, treat headlamp exposure in any new
interior as unverified.

**The wider lesson, worth more than the bug:** the shot harness's anchor mode
returns early from `Player.update`, so every capture in this project runs a code
path the player never takes. It took building a second scene to notice, because
1.1 is an exterior where the moon hides the difference.

## Renderer / core

### Volumetric light shafts are declared but not implemented
`QualityProfile.volumetrics` and `volumetricSamples` are plumbed through the
settings tiers and read by scene code, but no volumetric pass is wired into the
pipeline yet. The sodium lamp cone and the shafts through the cell-house
clerestory are the two places it would matter most.
**Cost:** ~half a day. `VolumetricLightScatteringPostProcess` exists in the
bundle already; the work is authoring the occlusion meshes and keeping it off
the frame budget on low/medium.
**Impact:** high — atmosphere is a scored critic axis and this is the largest
single gap on it.

### Havok is a dependency but nothing uses it
`@babylonjs/havok` is installed. The player deliberately uses collide-and-slide
instead (documented in `Player.ts`), and no dynamic props exist yet, so the WASM
is currently dead weight in `package.json`.
**Cost:** trivial to remove; ~a day to actually use for debris, swinging doors
and the shifting cinder blocks in 1.2.
**Impact:** medium. Remove it or use it — shipping an unused 1.5 MB WASM
dependency is the worst of both.

### Screen-space reflections unused
`waterSSR` is defined on the ultra tier and never read. Standing water currently
relies on a clear-coat + IBL approximation, which is convincing on a still
puddle and less so on the large flooded areas in 1.2.
**Cost:** ~half a day. `SSRRenderingPipeline` is available.

### No save/checkpoint system
`Settings` persists, but there is no run state, no checkpoint, no journal
persistence. The design calls for checkpoints every 60–90 s.
**Cost:** ~a day.
**Impact:** high for a shippable game; zero for the look-dev slice.

### ~~Audio is entirely absent~~ — BUILT (unverified by ear)
`src/core/Audio.ts` now provides synthesised footsteps with per-surface
profiles, a breathing ambience bed, generated convolution reverb per space,
lamp hum, and radio comms with depth-based degradation, all wired to the
controller's existing hooks.

**Caveat: none of it has been heard.** The shot harness is silent and headless,
so the entire audio system is verified only by typecheck. Levels, filter
frequencies and the reverb impulses are authored by reasoning, not by ear, and
should be expected to need a real mixing pass.
**Cost:** an hour with headphones.

## Scene 1.1 — Perimeter Approach

### The three entries are geometry, not gameplay
The drainage trench, the wall breach and the maintenance gate are all modelled
and traversable, but none of them is wired to an interaction, a lockpick
minigame, Mike's Institutional Knowledge check, or a transition into 1.2.
**Cost:** ~a day once an interaction system exists.

### ~~The drainage trench has no hole in the ground~~ — FIXED
`buildGround` now takes aperture rectangles and drops any triangle whose
centroid falls inside one, cutting a real hole; coping stones along both lips
hide the ragged edge where the cut lands on triangle boundaries. The trench is
genuine geometry now.

**But `a5-trench` is still a poor frame** — it is dark, because the trench has
no light in it and the headlamp that should light it does not work (see the P0
above). The geometry is right and the lighting is not.

### No foliage
The reference photography is full of it — weeds through the asphalt cracks,
saplings against the wall base, the cottonwoods growing through the shop floors.
Currently there is a single flat lawn plane. Weeds are painted into the asphalt
albedo but nothing stands up off the ground.
**Cost:** ~half a day for thin-instanced cross-quad grass and a few sapling
cards.
**Impact:** high — it is a scored axis (geometric detail) and it is the most
obvious difference from the reference photographs.

### Cell house is a placeholder mass
Correctly proportioned and correctly fenestrated on the visible elevation, but
it is a box with a roof. It reads at distance and would not survive a closer
anchor.
**Cost:** it becomes real work in 3.1 anyway.

### Ground is a displaced plane, not terrain
Fine for this scene's flat asphalt apron. Will not hold up at the quarry cut.

## Scenes not yet built

**1.2 Siphon · 2.1 Powerhouse · 2.2 Armory Spiral · 3.1 Cellblocks ·
3.1b The Void · 3.2 Maintenance Ladder · 4.1 Guard Tower · 4.2 Exit** — none of
these exist. Scene 1.1 is the look-dev lock and the material library it froze is
the deliverable that makes them buildable; they are not started.

The research and design work for them *is* done — `RESEARCH.md` has the
architecture, tier counts, materials and the Yard Tower finding; `DESIGN.md` has
the beats. What is missing is the geometry and the scripting.

## Critic loop

### The loop has not run to its own protocol
`QUALITY-LOG.md` defines an 8-axis rubric scored by an independent agent, pass
at mean ≥8.0. In practice iterations 1–3 were driven by direct inspection of the
captures against reference, fixing objective breakage (a silently-failed
environment map, a skewed roof primitive, a stalled settle loop, a 4× overspent
texture-bake budget) rather than by scored critique. That was the right call
while the frame still had hard bugs in it — there is no point scoring
composition on an image that is black — but it means **the scene has not
actually been through the formal critic protocol**, and should not be described
as having passed it.
**Cost:** one clean pass once the frame is stable.

### Performance numbers are software-rendered
All FPS figures in `QUALITY-LOG.md` come from headless SwiftShader, which is
software rasterisation and 1–2 orders of magnitude slower than any real GPU.
They are a valid *relative* regression signal between iterations and worthless
as an absolute target. **The 60 FPS budget in `ART-BIBLE.md` §7 has not been
verified on real hardware.**
**Cost:** an hour on a machine with a GPU.
**Impact:** high — it is a stated non-negotiable constraint and it is currently
unmeasured.
