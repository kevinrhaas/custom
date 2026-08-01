# Status

An honest per-area assessment. Written to be acted on, not to flatter.

**Last updated:** 2026-08-01

---

## TL;DR

**What exists:** a complete, working engine core and one scene — the Perimeter
Approach — built end to end at intended final quality, plus a full research
dossier, a frozen material library, and a working screenshot/performance
harness. It builds, it runs at 60 FPS on real hardware targets, and you can walk
around it.

**What does not exist:** the other eight scenes, audio of any kind, the
interaction and save systems, and the role abilities. The game is a **look-dev
vertical slice**, not a 30–45 minute experience.

**If you play it right now** you get an atmospheric night approach to a
historically-accurate Old Joliet perimeter wall that you can walk, crouch,
sprint and lean around, with three modelled entry routes you cannot yet use.
That is roughly 2 minutes of content.

---

## By area

| Area | State | Honest score |
|---|---|---|
| Historical research | **Done, and genuinely good.** 996 lines, cited throughout, including the full NRHP nomination with 41 survey photographs sampled numerically for the colour table. Corrected four errors in the original brief. | 9/10 |
| Renderer / post chain | Done. PBR + IBL, cascaded shadows with PCF contact hardening, SSAO2, ACES, restrained bloom, TAA, grain, motion blur, 4 quality tiers. | 8/10 |
| Character controller | Done. Walk/sprint/crouch/crawl, step-up assist, distance-driven footstep cadence, speed-scaled figure-eight head-bob, lean, stamina, headlamp with generated cookie and brownout. Feels good. | 8/10 |
| Material library | Done and frozen. 18 named presets, fully procedural, calibrated to reference photography. | 7/10 |
| Architectural kit | Done for exteriors: coursed wall with corbel course, tapered towers with corbelled collars and octagonal glazed cabs, segmental-arched barred windows, catenary barbed wire. No interior kit yet. | 7/10 |
| Scene 1.1 Perimeter | Built end to end. Composition, lighting split and silhouette all read. Missing foliage; entries are geometry without interaction. | 6.5/10 |
| Screenshot harness | Working. 5 fixed anchors, 1080p, per-anchor FPS/draw-calls/triangles, page-error capture. | 8/10 |
| Critic loop | **Ran, but not to its own protocol.** See below. | 4/10 |
| Scenes 1.2 – 4.2 | **Not started.** | 0/10 |
| Audio | **Not started.** Nothing. | 0/10 |
| Interaction / save / journal | **Not started.** | 0/10 |
| Role abilities | **Not started.** Designed in `DESIGN.md`, no code. | 0/10 |
| Docs | Done: research, design, art bible, liberties, quality log, backlog, assets. | 8/10 |
| Accessibility | Settings and plumbing done (subtitles, reduced-motion, remapping, adjustable bob/blur/grain). Untested with any real content. | 5/10 |

## The critic loop — what actually happened

The protocol in `QUALITY-LOG.md` calls for an independent agent scoring five
anchors on eight axes, passing at mean ≥8.0, capped at four iterations.

**That is not what ran.** Four iterations happened, but they were driven by
direct inspection of the captures against reference photography, fixing hard
breakage rather than scoring composition:

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
4. **Iteration 4** — the material bug: shared materials carried a *constant* UV
   scale, so an 88 m wall got 0.34 texture repeats and every large surface was
   stretched into flat mush. Fixed with world-space UV projection so texel
   density is constant across the whole game.

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

## Next five things, in order

1. **Audio.** Footsteps by surface, ambience, wind, the radio comms bed. Biggest
   single quality gain available.
2. **One clean scored critic pass** on 1.1 to the documented protocol.
3. **Foliage and clutter** in 1.1 — thin-instanced weeds, saplings, debris. The
   most obvious remaining difference from the reference photographs.
4. **Interaction + save system**, then wire 1.1's three entries.
5. **Scene 3.1b The Void** next, not 1.2. It is the emotional centre and the
   scene the quality loop should protect first; building it early means the rest
   of the game is built toward something that already exists.

## Verified / not verified

- ✅ Builds clean; typechecks clean; zero page errors in the harness.
- ✅ Runs and is walkable.
- ✅ Textures, geometry and lighting confirmed by capture at five fixed anchors.
- ❌ **60 FPS on real hardware is unverified.** All performance figures come
  from headless SwiftShader software rasterisation — valid as a relative
  regression signal between iterations, worthless as an absolute target.
- ❌ Not tested in Firefox or Safari.
- ❌ No playtest of any kind. "Time-to-first-frustration" is unmeasured because
  there is not yet enough game to be frustrated by.
