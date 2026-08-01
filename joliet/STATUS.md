# Status

An honest per-area assessment. Written to be acted on, not to flatter.

**Last updated:** 2026-08-01 (revised)

---

## TL;DR

**What exists:** a working engine core, a synthesised audio engine, and **two
scenes** — 1.1 Perimeter Approach and 3.1b The Void — plus a cited research
dossier, a frozen material library, and a screenshot/performance harness. It
builds, it runs with zero page errors, and you can walk around both.
Frame rate on real hardware is **unmeasured** — see the bottom of this file.

**What does not exist:** the other seven scenes, any transition between the ones
that do exist, and the interaction, save and role-ability systems. The game is a
**look-dev vertical slice**, not a 30–45 minute experience.

**If you play it right now** you get an atmospheric night approach to a
historically-accurate Old Joliet perimeter wall (`?scene=perimeter`, the
default) and, separately, the sealed sub-level with its carved names
(`?scene=void`). Each is a couple of minutes. There is no way to walk from one
to the other — the scenes are reachable only by URL, because no transition
system exists.

---

## By area

| Area | State | Honest score |
|---|---|---|
| Historical research | **Done, and genuinely good.** 996 lines, cited throughout, including the full NRHP nomination with 41 survey photographs sampled numerically for the colour table. Corrected four errors in the original brief. | 9/10 |
| Renderer / post chain | Done. PBR + IBL, cascaded shadows with PCF contact hardening, SSAO2, ACES, restrained bloom, TAA, grain, motion blur, 4 quality tiers. | 8/10 |
| Character controller | Done. Walk/sprint/crouch/crawl, step-up assist, distance-driven footstep cadence, speed-scaled figure-eight head-bob, lean, stamina, headlamp with generated cookie and brownout. Feels good. | 8/10 |
| Material library | Done and frozen. 18 named presets, fully procedural, calibrated to reference photography. | 7/10 |
| Architectural kit | Done for exteriors: coursed wall with corbel course, tapered towers with corbelled collars and octagonal glazed cabs, segmental-arched barred windows, catenary barbed wire. No interior kit yet. | 7/10 |
| Scene 1.1 Perimeter | Built end to end. Composition, lighting split, masonry and silhouette all read; the trench is now a genuine aperture in the ground with coping stones. `a5-trench` is still a weak frame — the geometry is right, it just has no light in it. Missing foliage; entries are geometry without interaction. | 6.5/10 |
| Scene 3.1b The Void | **Built, and it works.** ~1,750 individually-placed stones batched to one mesh per material; 64 carved inscriptions across six hands on a generated height field. SAM'L O'KEEFE, No 738, 1862, tally counts and LET ME UP legible in one frame. 11 meshes, ~104k tris. Limestone reads faintly "quilted"; the headlamp still blows the near field. | 7/10 |
| Screenshot harness | Working. 5 fixed anchors, 1080p, per-anchor FPS / active meshes / triangles, page-error capture. | 8/10 |
| Critic loop | **Ran, but not to its own protocol.** See below. | 4/10 |
| Scenes 1.2, 2.1, 2.2, 3.1, 3.2, 4.1, 4.2 | **Not started.** | 0/10 |
| Scene transitions | **Not started.** The two built scenes are reachable only by `?scene=` URL. | 0/10 |
| Audio | **Built, never heard.** Synthesised footsteps with per-surface profiles, generated convolution reverb per space, ambience bed, lamp hum, radio degradation. The harness is silent and headless, so the whole system is verified by typecheck alone and needs a real mixing pass. | 5/10 |
| Interaction / save / journal | **Not started.** | 0/10 |
| Role abilities | **Not started.** Designed in `DESIGN.md`, no code. | 0/10 |
| Docs | Done: research, design, art bible, liberties, quality log, backlog, assets. | 8/10 |
| Accessibility | **Was scored 5/10 for three days and was really 0/10.** The settings store was complete from the first commit and *nothing could reach it* — every option needed a hand-edited localStorage entry, and pause silently froze the frame with no overlay. There is now a real pause menu (native controls, 44px targets, keyboard reachable, stacked under 560px). Still untested with a screen reader and with no real dialogue to caption. | 6/10 |
| Touch / mobile | Twin-stick layer: floating move stick, drag-to-look, sprint as a stick gesture, safe-area thumb cluster, multi-touch by pointerId. Boots and plays. **Nobody has held it** — every tuning constant is a reasoned guess, and nothing iOS-specific is verified. | 5/10 |
| Pause / settings UI | Built. Camera, comfort, accessibility, assist, graphics, audio. | 7/10 |

## The critic loop — what actually happened

The protocol in `QUALITY-LOG.md` calls for an independent agent scoring five
anchors on eight axes, passing at mean ≥8.0, capped at four iterations.

**That is not what ran.** Nine iterations happened, but they were driven by
direct inspection of the captures against reference photography, fixing hard
breakage rather than scoring composition. The full log with root causes is in
`QUALITY-LOG.md`; the headlines were:

1. **Iteration 1** — near-black frame, giant skewed black wedges across the sky.
   Root causes: `CubeTexture.CreateFromPrefilteredData` fails *silently* on a
   raw `.hdr` (all IBL lost), and scaling an already-rotated cylinder skews it.
2. **Iteration 2** — harness stalled indefinitely. The anchor settle loop drove
   `requestAnimationFrame`, which headless throttles for pages it treats as
   hidden, while also double-rendering against the engine's own loop. Separately,
   baking 18 materials at 1024² was tens of seconds of single-threaded JS and
   blew the load budget on its own.
3. **Iteration 3** — legible at last, but massively underexposed: PBR light
   intensities were set as if they were 0–1 dials. Also revealed the real
   material bug.
4. **Iterations 4–5** — a translucent panel smeared across the whole wall. Not
   geometry: TAA temporal history survived the anchor teleport with no motion
   vectors to invalidate it.
5. **Iterations 6–7** — the material bug, in two layers. Shared materials
   carried a *constant* UV scale, so an 88 m wall got 0.34 texture repeats and
   every large surface stretched into mush; and once that was fixed with
   world-space UV projection, `Texture.clone()` on a `RawTexture` turned out not
   to carry its pixel buffer, so every material was sampling a flat clone.
6. **Iterations 8–9** — look tuning (rock-face relief depth, blotching, runoff,
   warming the key) and a metric fix: the draw-call counter had been
   accumulating across frames, so every draw-call figure logged before then was
   a running total and meaningless.

Scoring composition on a black frame would have been theatre. But the
consequence is real: **scene 1.1 has not been through the formal 8-axis critique
and must not be described as having passed it.** One clean scored pass is the
next thing it needs.

## On the original brief's exit condition

The brief asked to loop until a critic, comparing blind side-by-side against
Call of Duty, judged this the better-looking image.

**That test was not run, and was never going to be.** Obtaining CoD frames to
compare against is not something that can be done legitimately, so any agent
reporting a completed blind comparison would be fabricating its evidence. An
exit condition that cannot be satisfied produces one of two failures — looping
until context runs out, or a critic that quietly starts rubber-stamping to
escape — and both would have burned the whole build.

The substituted bar is the 8-axis rubric in `QUALITY-LOG.md`, scored against
reference photographs of the real building. It is a real bar. This scene has not
cleared it yet.

**Where the gap to AAA actually is:** it is not the renderer. The post chain,
shadow filtering and material model are broadly the right ones. The gap is
*content density* — foliage, clutter, decals, wear passes, set dressing, and the
sheer number of authored props per square metre — plus audio, which is entirely
absent and which matters more here than in most games because the whole tension
model is sound in an empty building.

## Next things, in order

1. **Audio.** Footsteps by surface, ambience, wind, the radio comms bed. Biggest
   single quality gain available.
2. **One clean scored critic pass** on 1.1 to the documented protocol.
3. **Calibrate the headlamp against a test chart** at 1 / 2 / 4 / 8 m. It is
   currently reasoned, not measured, and it is what stands between The Void and
   its own purpose.
4. **Mix the audio** — an hour with headphones. None of it has been heard.
5. **Foliage and clutter** in 1.1 — thin-instanced weeds, saplings, debris. The
   most obvious remaining difference from the reference photographs.
6. **Interaction + save system**, then wire 1.1's three entries and a real
   transition between the two scenes.

## Verified / not verified

- ✅ Builds clean; typechecks clean; zero page errors in the harness.
- ✅ Runs and is walkable.
- ✅ Textures, geometry and lighting confirmed by capture at five fixed anchors.
- ⚠️ **`a5-trench` is a weak frame** — geometry fixed (real aperture), lighting not.
- ⚠️ **The audio has never been heard.** Typecheck-verified only.
- ⚠️ **The harness's anchor mode returns early from `Player.update`**, so every
  capture in this project runs a code path the player never takes. This is the
  most important caveat on the whole verification story.
- ❌ **60 FPS on real hardware is unverified.** All performance figures come
  from headless SwiftShader software rasterisation — valid as a relative
  regression signal between iterations, worthless as an absolute target.
- ❌ Not tested in Firefox or Safari.
- ❌ No playtest of any kind. "Time-to-first-frustration" is unmeasured because
  there is not yet enough game to be frustrated by.
