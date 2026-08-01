# Quality backlog

What did not reach the bar, and what it would take. Written honestly — an
accurate status report is more useful than a flattering one.

Each item: what's wrong, what it would cost, and how much it matters.

---

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

### Audio is entirely absent
No footstep system, no ambience, no radio comms, no mix bus. `Player` exposes
`setFootstepHandler`/`setLandHandler` and nothing subscribes.
**Cost:** several days including CC0 sourcing.
**Impact:** very high. In a game whose whole tension model is *sound* in an
empty building, silence is the single biggest thing missing. This is the top of
the list.

## Scene 1.1 — Perimeter Approach

### The three entries are geometry, not gameplay
The drainage trench, the wall breach and the maintenance gate are all modelled
and traversable, but none of them is wired to an interaction, a lockpick
minigame, Mike's Institutional Knowledge check, or a transition into 1.2.
**Cost:** ~a day once an interaction system exists.

### The drainage trench is broken — the ground has no hole in it
**This is a visible defect, not a rough edge.** The trench is excavated to
y = −2.6 but the base ground is a single solid plane at y = 0 with no aperture,
so the trench reads as two stone walls floating on an unbroken floor and the
water surface is buried. Anchor `a5-trench` shows it plainly.
**Cost:** ~half a day. The ground needs to be built as a CSG subtraction or,
better, authored as a set of tiles with the trench corridor simply omitted —
which is the approach the Siphon needs anyway.
**Impact:** high. It is one of the scene's three entry routes and currently the
worst frame in the game.

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
