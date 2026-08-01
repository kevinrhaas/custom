# Joliet: Midnight Infiltration

A first-person urban-exploration game set in the **Old Joliet Prison** — the
Gothic Revival limestone castle at 1125 Collins Street, Joliet, Illinois, built
1857–68 by Boyington & Wheelock, closed in 2002, and rendered here in its
present decayed condition.

**There is no combat and there are no weapons.** It is a traversal and
observation game: you walk, crouch, crawl, climb and lean through a real
building at night with a headlamp and a finite battery. Tension comes from
darkness, sound, structural instability and light management.

Runs in the browser. Babylon.js, TypeScript, Vite. No runtime dependencies
beyond Babylon.

---

## Run it

```bash
npm install
npm run dev        # → http://localhost:5173
npm run build      # → dist/  (static, deployable anywhere)
npm run check      # typecheck
npm run shots      # Playwright screenshot + performance harness
```

Published at **`/joliet/`** on the site, with the game itself at
**`/joliet/app/`**. The `custom` repo's Pages workflow publishes only `site/`,
so the built bundle is committed to `site/joliet/app/`; source lives here in
`joliet/`.

## Controls

| | |
|---|---|
| `W A S D` | Move |
| `Shift` | Sprint |
| `C` | Crouch (toggle) |
| `Z` | Crawl (toggle) |
| `Space` | Climb / vault |
| `E` | Interact |
| `F` | Headlamp |
| `Q` | Role ability |
| `Tab` | Journal |
| `Esc` | Pause & settings |

Gamepad is supported throughout. Every binding is remappable.

**Touch.** Phones and tablets get an on-screen layer instead (`src/core/TouchControls.ts`):
the left half is a *floating* move stick that appears wherever the thumb lands,
the right half is drag-to-look, and there is a bottom-right cluster of Lamp /
Climb / Crouch / Use buttons. Sprint is a stick gesture — push past ~85% of the
stick's radius — rather than a button you have to hold while steering. Move,
look and a button all work at once. Touch devices are forced to the `low`
quality tier at ~1.8× hardware scaling; a phone will not hold 30 FPS at native
resolution with four shadow cascades. `?touch=1` forces the layer on for
testing on a desktop, `?touch=0` forces it off.

Accessibility is a ship requirement: subtitles on by default with speaker names,
head-bob / motion-blur / grain / vignette independently adjustable to zero,
`prefers-reduced-motion` honoured on first run, high-contrast prompts, and no
puzzle gated on audio alone.

## Architecture

```
joliet/
├── index.html              Entry; loads src/main.ts
├── src/
│   ├── main.ts             Boot: renderer → materials → scene → player → loop
│   ├── core/               ── core-owned. Scene code composes, never edits. ──
│   │   ├── Renderer.ts       Engine, scene, lights, CSM shadows, full post chain
│   │   ├── Player.ts         FPS character controller (collide-and-slide)
│   │   ├── Input.ts          Keyboard + mouse + gamepad → named actions
│   │   ├── Settings.ts       Persisted settings, 4 quality tiers, a11y
│   │   ├── Palette.ts        The calibrated Joliet colour palette
│   │   ├── Noise.ts          Seeded tileable noise (value/fBm/Worley/ashlar)
│   │   ├── Bakery.ts         Procedural PBR texture generation
│   │   ├── Materials.ts      The frozen named-material library
│   │   └── Kit.ts            Parametric Boyington architecture (wall/tower/…)
│   ├── scenes/             One directory per scene, one owner each
│   └── ui/                 HUD, loader, subtitles
├── tools/shots.mjs         Screenshot + perf harness (fixed camera anchors)
├── public/assets/          CC0 textures and HDRIs (see ASSETS.md)
├── docs/                   RESEARCH · DESIGN · ART-BIBLE · liberties · quality
└── artifacts/shots/        Per-iteration captures, the critic loop's evidence
```

### Two decisions worth knowing about

**Textures are generated, not photographed.** `Bakery.ts` synthesises every
surface — limestone, flaking paint, oxidised steel, worn concrete, glazed tile —
from seeded noise at load time. This is not a shortcut. A photo scan puts the
weathering wherever the photographer's wall had it; generated maps let runoff
start at the cap rail and biological blotching sit in the sheltered courses,
which is what the reference actually shows. It also costs a few hundred KB of
code instead of tens of MB of downloads. The CC0 sets in `public/assets/` are
used for detail overlays and foliage.

**The player is not a rigid body.** Movement uses Babylon's swept-ellipsoid
collide-and-slide plus an explicit step-up probe. For a walking human in a
hand-authored level this is more predictable and cheaper than a physics capsule,
and it never jitters against stairs or catches on thresholds — which matters
because this building is almost entirely stairs, thresholds and doorways.

## Documentation

| Document | What's in it |
|---|---|
| [`docs/RESEARCH.md`](docs/RESEARCH.md) | The source of truth. Timeline, site plan, cell-house interiors, decay taxonomy, measured colour palette, powerhouse, underground. Every claim cited or explicitly flagged unverified. |
| [`docs/DESIGN.md`](docs/DESIGN.md) | The spine, the four roles, scene beats, and how "fun and not too hard" is operationalised as a spec. |
| [`docs/ART-BIBLE.md`](docs/ART-BIBLE.md) | Lighting rig, material parameter ranges, composition rules. What scene agents must compose from. |
| [`docs/HISTORICAL-LIBERTIES.md`](docs/HISTORICAL-LIBERTIES.md) | Every place gameplay wins over accuracy, and why. Append-only. |
| [`docs/QUALITY-LOG.md`](docs/QUALITY-LOG.md) | Every critic iteration: 8-axis scores, fixes, and the perf cost of each fix. |
| [`docs/QUALITY-BACKLOG.md`](docs/QUALITY-BACKLOG.md) | What didn't reach the bar and what it would take. |
| [`ASSETS.md`](ASSETS.md) | Every third-party asset, its source URL and licence. CC0 only. |

## On accuracy

The building is the point, so the research came first and the modelling followed
it. Two things worth stating plainly:

**This is not Stateville.** Stateville is the nearby prison with the round
panopticon "roundhouse". Joliet has no such building and never did. The two were
administered under one warden from 1933 to 1973, which is why sources constantly
conflate them. Anything round and glass-domed in a reference image is Stateville.

**The story is fiction; the history under it is not.** The prison was built with
convict labour from limestone the inmates quarried on site — the men held there
cut the stone that held them. That is documented, and it is why the game exists.
The sealed sub-level the story builds toward is invented, and the game says so
on screen. Everything else made up is listed in `HISTORICAL-LIBERTIES.md`.

The scenario is fictional and framed as sanctioned after-hours access. The real
site is an operating museum that runs public tours; nothing here encourages
trespass, and the end cards point at the legitimate way in.

## Status

See [`STATUS.md`](STATUS.md) for an honest per-scene assessment — what hit the
quality bar, what didn't, and what's next.
