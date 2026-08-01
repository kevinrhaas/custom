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

## 1.1 Perimeter Approach

*(Iterations recorded below as they complete.)*
