/**
 * flora.js — the sward you stand in.
 *
 * The walkthrough's ground was a painted plane. This module puts the July 1835
 * lake-plain prairie on top of it: chest-high layered vegetation that hides the
 * ground a few metres from the camera and falls off into a green sea.
 *
 * It invents no plant. Which community is where (`extent`), what grows in it
 * (`species`), how tall it is ON 1 JULY (`height_m`), how much ground it covers
 * (`abundance`), its leaf colour and whether it flowers at all (`july`) all come
 * from `data/flora/`. A missing manifest draws NOTHING and says so; there is no
 * fallback community, because an invented prairie looks exactly like a
 * researched one and that is the failure this project exists to avoid
 * (AGENTS.md rule 2).
 *
 * THE JULY GATE, enforced here as well as in the data. A flower head is drawn
 * if and only if the record carries a `july.inflorescence` AND its phenology is
 * not `vegetative` or `budding`. Big bluestem, Indian grass and switchgrass are
 * vegetative in mid-July, and the dossier calls 2 m "turkey-foot" seed heads in
 * July "the single most common historical-reconstruction error". Keying the
 * head off the record makes that error impossible to draw: no code path puts an
 * inflorescence on a plant whose record has none. A record that contradicts
 * itself is a defect, not a licence, and it is reported.
 *
 * THREE LAYERS, because a prairie seen from inside it is three problems:
 *
 *   NEAR  to ~8 m   blade geometry. The layer the eye reads as plants, and the
 *                   one that has to hide the ground — at eye height the nearest
 *                   ground in frame is 3.4 m away.
 *   MID   to ~27 m  a blade is a third of a pixel at 20 m. Clump cards turned
 *                   to the camera: silhouette and colour, all that survives.
 *   FAR   beyond the instanced plants, the terrain material's procedural
 *                   prairie texture carries the unresolved colour. There is
 *                   deliberately no second horizontal vegetation surface:
 *                   one at plant-top height reads as elevated ground, hides
 *                   building bases, and leaves the visitor walking underneath
 *                   it at banks. Detailed plants remain rooted on the terrain.
 *
 * Placement is a deterministic world lattice: a plant's position, species,
 * height and colour are a hash of its cell, so re-centring on a walking camera
 * regenerates the same plants and nothing swims underfoot. Only the ring edge
 * changes, and it is scaled in rather than popped.
 *
 * Procedural per AGENTS.md and the publish budget: no image asset, no binary,
 * a bounded handful of draw calls. Every material carries `_CONFIDENCE` as a per-INSTANCE
 * attribute, so the confidence view grades each plant by its species' evidence.
 */

import * as THREE from 'three';

/** docs/PROVENANCE.md's three levels, as the shader reads them. */
const LEVEL = { documented: 0.0, inferred: 0.5, conjectural: 1.0 };

/**
 * July midday light ON A LEAF, which is not the same problem as light on a wall.
 *
 * A sward lit only by reflection cannot be brighter than its own albedo, and a
 * green leaf's albedo is about 0.14 in the green channel: under any exposure
 * that keeps a whitewashed wall white, a purely reflective prairie tops out at
 * about half grey and stays there. Measured against the bar that is exactly the
 * failure — round 1 put ZERO pixels over luminance 180 in the near five metres
 * where the July photographs put 15.0% (Woodworth) and 4.0% even in the October
 * negative control, and its p99 was 132 against the photographs' 252.
 *
 * The missing physics is that a grass blade is a thin membrane. It TRANSMITS:
 * roughly a fifth of the light that lands on it comes out the other side, and
 * it comes out FORWARD-SCATTERED, so the lobe leaving the far face is several
 * times brighter than an isotropic one. That is why a backlit blade out-glows
 * every front-lit blade around it, and it is what makes the photographs' white
 * tail. The transmitted light is filtered by chlorophyll on the way through,
 * which is why the tail is GREEN and not a white blowout. On top of that the
 * cuticle is a waxy film with a narrow specular lobe, which supplies the
 * glints, and the sky passes through the blade as well, which is what keeps
 * the shaded face off black now that it is no longer given a fake sunward
 * normal.
 *
 * These are render tuning, not evidence — no source records the transmittance
 * of Chicago cordgrass. They are recorded as such in docs/LIBERTIES.md.
 */
const LEAF = {
  /**
   * Multiple scattering inside the canopy, on the front-lit path. A green
   * photon that enters a sward is scattered rather than absorbed and bounces
   * from leaf to leaf until it escapes, so a CANOPY is far brighter and far
   * more saturated in the green band than any single leaf in it, while red and
   * blue are absorbed on the first hit. A single-scattering Lambert model
   * cannot exceed one leaf's albedo — 0.14 in green — and that ceiling is
   * exactly the flat top the structure critic measured. In the Woodworth
   * photograph the pixels over luminance 180 are not glints: they are ordinary
   * sunlit leaf FACES at (219, 233, 172), 95% of them green-dominant.
   */
  scatter: 0.34,
  /** Effective transmittance x forward-lobe gain, green channel. */
  transmit: 0.74,
  /** Sharpness of the forward lobe, on a (0.5 + 0.5 cos) remap: a 70-degree
   *  sun is overhead, not behind, so a raw cos^n lobe would never fire. */
  forward: 3.2,
  /** What chlorophyll passes, relative to the leaf's own hue. Green through,
   *  red partly, blue absorbed. */
  tint: [0.66, 1.0, 0.42],
  /** Skylight through the blade. Small, and it is the shaded face's floor. */
  skyTransmit: 0.05,
  /** The cuticle. A narrow lobe and a Fresnel edge, at a dielectric F0. */
  gloss: 38.0,
  specular: 0.85,
  f0: 0.035,
};

/**
 * Where the sun is if the scene graph has no directional light to ask. 1 July,
 * 41.85 N, local noon — the same instant world.js computes from the scene
 * record. It is only a fallback: `sunFromScene` prefers the light the scene
 * actually built, so the sward and the buildings are lit by one sun.
 */
const SUN_FALLBACK = {
  elevationDeg: 70.6,
  azimuthDeg: 180,
  /** 0xfff2dc x 3.0 and 0xa8c4e0 x 2.4, linear — world.js's own values. */
  colour: [3.0, 2.66, 2.17],
  sky: [0.40, 0.55, 0.75],
};

/**
 * Render tuning: how many polygons we spend and where, not evidence. A tuft
 * instance is not a plant but a BUNDLE of shoots standing for the fraction of a
 * square metre the matrix covers — the records give cover fractions and no
 * source gives stem counts. The records set the mix; `tuftsPerM2` sets the
 * geometry spent on it, tuned to the one thing a photograph can settle: at eye
 * height the ground is invisible. LIBERTIES L32.
 */
const TUNE = {
  near: { radius: 7.6, cell: 0.74, perCell: 4, tuftsPerM2: 7.30, band: 2.2 },
  mid: { inner: 4.5, radius: 27.0, cell: 1.55, perCell: 4, band: 7.0, innerBand: 3.0 },
  forb: { radius: 26.0, cell: 3.4, perCell: 4, band: 5.0 },
  /** Hard caps. The palette's `budget` is advisory; this is the ceiling. */
  cap: { near: 2400, mid: 4400, forb: 900, head: 820 },
  wind: { speedNear: 1.35, sway: 0.085, waveM: 9.0 },
  /**
   * Rebuild the lattice when the camera has moved this far. It is also the
   * margin the fade ring is inset by (`ringsFor`), so it is the width of the
   * annulus of already-placed, zero-height plants that stands between the
   * lattice edge and the first plant with any height in it. 1.2 m was the
   * figure while the fade was frozen between rebuilds; halved now that the
   * inset is what it buys, because a metre of the near ring is a lot of it.
   */
  step: { near: 0.6, mid: 3.0, forb: 3.0 },
};

/**
 * The lattice is world-anchored and rebuilt only every `step` metres walked;
 * the fade ramp is evaluated per FRAME, in the vertex shader, against where the
 * camera actually is. Those two rates are what the pop was made of, and they
 * are reconciled here rather than in either of them.
 *
 * A ring returned as `[outer, band, inner, innerBand]` — the four numbers the
 * shader reads out of `aChiRing` — is inset from the lattice that carries it by
 * `step` at BOTH edges, so a plant is always already placed, at scale zero,
 * before the distance at which it is worth any height at all. Without the inset
 * a plant outside the lattice at one rebuild is up to `step` inside the fade
 * ring by the next, and arrives at `step / band` of full size in a single
 * frame: 55% for the near ring as it stood, which is the "grass and flowers
 * appear out of the ground as you walk towards them" the owner reported.
 *
 * The outer edge is bought by moving the fade IN — growing the lattice instead
 * would cost a 34% wider near annulus of instances against 6% of triangle
 * headroom. The inner edge is bought by moving the lattice OUT, because the
 * inner annulus of the mid ring is 1.3% of its area and free, and because
 * moving that fade outward would thin the near/mid crossover where the change
 * of representation is supposed to be invisible.
 */
function ringsFor(layer, step) {
  const inner = layer.inner ?? 0;
  return {
    lattice: { outer: layer.radius, inner: Math.max(0, inner - step) },
    fade: [layer.radius - step, layer.band, inner, layer.innerBand ?? 0],
  };
}

/** Heads used to be gated at 35% of their plant's fade — a step in the middle
 *  of a ramp, and the most conspicuous pop in the field, because a flower is
 *  the brightest thing in it. Their own ring reaches zero exactly where the
 *  plant's ramp passes 0.35, so the same heads are drawn as before and the
 *  cap sees the same pressure; only the step is gone. */
const HEAD_FADE_AT = 0.35;
function headRingOf(fade) {
  return [fade[0] - HEAD_FADE_AT * fade[1], (1 - HEAD_FADE_AT) * fade[1], fade[2], fade[3]];
}

/** The ramp the vertex shader applies, in JS, so the two cannot disagree about
 *  where a plant starts to grow. Kept identical to the GLSL in `plantMaterial`. */
function fadeOf(ring, d) {
  const outer = clamp01((ring[0] - d) / Math.max(ring[1], 1e-4));
  const inner = ring[3] > 0 ? clamp01((d - ring[2]) / ring[3]) : 1;
  return outer * inner;
}

/** Nearer than this, plants go all the way round whatever the cone says. */
const CONE_KEEP_M = 3.5;
/** Cosine of the cone half-angle, and the yaw change that forces a rebuild. */
const CONE_COS = Math.cos(62 * Math.PI / 180);
const CONE_YAW_STEP = 0.20;

/** Everything gets halved on a phone; mobile 390x780 is a release gate. */
const LOW = {
  // A phone is not a small desktop: the mobile pass draws a 585x1170 buffer,
  // MORE pixels than the desktop one, on a fraction of the fill rate. So the
  // sward is not scaled down here, it is a shallower field — tight near and
  // mid rings, with the terrain's prairie texture carrying the far field.
  near: { radius: 4.6, tuftsPerM2: 4.6 },
  mid: { inner: 3.0, radius: 13.0 },
  forb: { radius: 13.0 },
  cap: { near: 420, mid: 900, forb: 260, head: 240 },
};

/**
 * The middle setting. It has to be a real tune rather than a scale factor on
 * TUNE's caps, because at full detail the CAPS ARE NOT WHAT BINDS — the ring
 * radii are. Scaling the caps alone was measured at 8 177 triangles off 461 112,
 * which is a setting that says "fewer plants" and does essentially nothing.
 * What costs geometry is the mid ring's area: 27 m against LOW's 13 m is over
 * four times the ground. So this sits between the two, and every number here is
 * a RENDERING radius or ceiling. The species mix, the July states and the rules
 * about where a plant may stand are untouched, because those are evidence.
 */
const MID = {
  near: { radius: 6.2, tuftsPerM2: 6.4 },
  mid: { inner: 4.0, radius: 18.0 },
  forb: { radius: 17.5 },
  cap: { near: 1500, mid: 2700, forb: 580, head: 520 },
};

/** The closed `form` list, split by how it is drawn. */
const GRAMINOID_FORMS = new Set([
  'grass_fine', 'grass_arching', 'grass_clump', 'sedge_tussock', 'rush_culm',
  'cattail', 'mat_prostrate',
]);
const FORB_FORMS = new Set([
  'forb_spike', 'forb_umbel', 'forb_daisy', 'forb_pompom', 'forb_globe',
  'forb_basal_scape', 'shrub_low', 'scape_leafless',
]);
/** Roles this module draws. `tree` and `thicket` belong to trees.js. */
const OUR_ROLES = new Set(['matrix', 'forb', 'emergent', 'shrub_low', 'ground']);

/**
 * Head archetype per RECORDED INFLORESCENCE SHAPE — `july.inflorescence.shape`,
 * against `index.json`'s published 26-value `inflorescence_shapes` vocabulary.
 *
 * Round 1 picked the geometry off `form` instead, an eight-value field about
 * the whole PLANT, and never read `inflorescence.shape` anywhere in the repo.
 * All 154 rows fill the shape field correctly, so that was 26 values of
 * researched morphology thrown away at the last step: Liatris's dense button
 * spike and Culver's root's candelabra spire came out as the same mesh in two
 * colours, and every `forb_umbel` — 47% of the wet prairie's forb population —
 * came out as one flat horizontal disc seen 11 degrees off the horizontal,
 * which is three pixels at five metres.
 *
 * The map is exhaustive over the published vocabulary and `compileZones`
 * checks that it stays so: a shape this renderer cannot draw is REPORTED and
 * draws nothing, rather than being quietly substituted, which is the whole
 * point of keying off the record in the first place.
 *
 * Each row carries four things the record cannot:
 *
 *   kind   which archetype mesh draws it.
 *   count  how many inflorescences one plant carries in mid-July. The records
 *          give the density of PLANTS and the size of ONE inflorescence and
 *          nothing about multiplicity, so this is a liberty either way and the
 *          honest thing is to key it to the architecture and say so
 *          (docs/LIBERTIES.md L35). A mountain mint is a mass of corymbs and a
 *          prairie dock a branched scape of ray heads, while Culver's root's
 *          candelabra IS the whole inflorescence and there is exactly one.
 *   tilt   radians off vertical, per instance. A corymb is FLAT-TOPPED and at
 *          1.68 m eye height a head at 0.7 m is seen eleven degrees above the
 *          horizontal, so a tilt near zero is a head that is not there.
 *          `umbel_nodding` is past 90 degrees, which is what nodding means.
 *   band   how far DOWN the plant the non-terminal heads are carried, as a
 *          fraction of its height. Axillary clusters run up the whole stem;
 *          a terminal spike does not.
 */
const HEAD_OF_SHAPE = {
  // Wands and columns.
  spike: { kind: 'spike', count: [1, 4], tilt: [0.00, 0.24], band: 0.16 },
  one_sided_spike: { kind: 'spike', count: [1, 2], tilt: [0.06, 0.34], band: 0.10 },
  raceme: { kind: 'spike', count: [1, 4], tilt: [0.05, 0.36], band: 0.18 },
  head_thimble: { kind: 'spike', count: [3, 10], tilt: [0.00, 0.28], band: 0.30 },
  // Flowers in the leaf AXILS, all the way up the stem — not a terminal head.
  cluster_axillary: { kind: 'spike', count: [8, 22], tilt: [0.60, 1.35], band: 0.66 },
  panicle_dense: { kind: 'spike', count: [1, 4], tilt: [0.00, 0.32], band: 0.16 },
  spadix_brown: { kind: 'spike', count: [1, 1], tilt: [0.00, 0.10], band: 0.04 },
  capsule_green: { kind: 'spike', count: [1, 3], tilt: [0.10, 0.50], band: 0.18 },
  // Culver's root: a terminal spire with lateral spires off its shoulder.
  spire_candelabra: { kind: 'spire', count: [1, 3], tilt: [0.00, 0.16], band: 0.08 },
  // Bluejoint, wild rice, wood nettle: an airy diffuse cloud, not a wand.
  panicle_open: { kind: 'panicle', count: [1, 2], tilt: [0.05, 0.42], band: 0.10 },
  // Composites, held up and out on branches.
  head_ray: { kind: 'ray', count: [5, 17], tilt: [0.25, 0.85], band: 0.38 },
  head_ray_drooping: { kind: 'raydroop', count: [5, 15], tilt: [0.20, 0.72], band: 0.36 },
  // Balls and buttons. A berry cluster, a burr, a hazel husk and a wild plum
  // all read as a small dense sphere at these sizes.
  head_pompom: { kind: 'pompom', count: [3, 11], tilt: [0.00, 0.40], band: 0.30 },
  head_globe: { kind: 'pompom', count: [3, 12], tilt: [0.00, 0.42], band: 0.32 },
  head_button: { kind: 'pompom', count: [2, 8], tilt: [0.00, 0.48], band: 0.28 },
  burr_spherical: { kind: 'pompom', count: [2, 8], tilt: [0.00, 0.48], band: 0.26 },
  berry_cluster: { kind: 'pompom', count: [3, 11], tilt: [0.10, 0.62], band: 0.36 },
  cherry: { kind: 'pompom', count: [3, 12], tilt: [0.10, 0.72], band: 0.38 },
  nut_husk: { kind: 'pompom', count: [2, 7], tilt: [0.10, 0.62], band: 0.32 },
  cluster_terminal: { kind: 'pompom', count: [1, 4], tilt: [0.15, 0.66], band: 0.12 },
  // Umbels: a DOME, never a plate.
  umbel_domed: { kind: 'dome', count: [3, 10], tilt: [0.05, 0.48], band: 0.34 },
  umbel_nodding: { kind: 'dome', count: [1, 4], tilt: [1.70, 2.45], band: 0.14 },
  bulbil_umbel: { kind: 'dome', count: [1, 2], tilt: [0.05, 0.35], band: 0.06 },
  // Flat-topped clusters, drawn as a tilted disc with a per-instance tilt.
  corymb_flat: { kind: 'corymb', count: [6, 20], tilt: [0.44, 0.74], band: 0.42 },
  umbel_flat: { kind: 'corymb', count: [4, 14], tilt: [0.40, 0.70], band: 0.34 },
  // Umbellets on rays from one point — the Queen-Anne's-lace architecture.
  umbel_compound: { kind: 'compound', count: [4, 14], tilt: [0.10, 0.46], band: 0.32 },
};

/** How each graminoid form deforms the one canonical tuft: `arch` is how far
 *  the tips fall away (cordgrass fountain vs bulrush culm), `spread` scales the
 *  clump's width against its height when no `width_m` is recorded. */
const GRASS_SHAPE = {
  grass_fine: { arch: 0.30, spread: 0.42 },
  grass_arching: { arch: 0.46, spread: 0.60 },
  grass_clump: { arch: 0.22, spread: 0.40 },
  sedge_tussock: { arch: 0.52, spread: 0.55 },
  rush_culm: { arch: 0.05, spread: 0.20 },
  cattail: { arch: 0.16, spread: 0.34 },
  mat_prostrate: { arch: 0.80, spread: 1.10 },
};

/* -------------------------------------------------------------------------- */
/* the module                                                                  */
/* -------------------------------------------------------------------------- */

/**
 * @param {object} o  dataBase (data/ root) · terrain (createTerrain's return) ·
 *   footprints (nothing grows through a wall) · growthBlocked (a narrow dated
 *   travelway clears plants, without clearing its whole legal corridor) ·
 *   confidence (every material is patched into it) · problems (the shared
 *   collector) · lowSpec (touch/mobile)
 */
export async function createFlora({
  dataBase, terrain, footprints = [], growthBlocked = () => false,
  confidence = null, problems = [], lowSpec = false, detail = 'full',
} = {}) {
  const group = new THREE.Group();
  group.name = 'flora';
  const disposables = [];
  const stats = {
    instances: 0, drawCalls: 0, triangles: 0, zones: 0, species: 0,
    unimplementedForms: [], unimplementedShapes: [], unzonedLandFraction: 0, rebuilds: 0,
  };

  const dataset = await loadFlora(dataBase, problems);
  if (!dataset) return inertRig(group, stats);

  // `lowSpec` is the device guess and still means the lightest tune; an
  // explicit visitor choice arrives as `detail` and outranks it.
  const tune = mergeTune(lowSpec && detail === 'full' ? 'light' : detail);
  const zones = compileZones(dataset, terrain, problems, stats);
  if (!zones.length) {
    problems.push('flora: the manifest named no usable zone — nothing is planted');
    return inertRig(group, stats);
  }
  stats.zones = zones.length;

  const water = waterField(terrain);
  const blocks = footprintCircles(footprints);
  const finder = zoneFinder(zones, terrain, water);
  stats.unzonedLandFraction = auditCoverage(terrain, finder);
  if (stats.unzonedLandFraction >= 0.999) {
    // Not a tolerance: records exist, ground exists, and NOTHING matches — the
    // layer would draw an empty prairie while looking healthy. Any fraction
    // short of that is a real mosaic and is reported through stats.
    problems.push('flora: no point on the modelled ground matches any zone extent — '
      + 'the sward is empty. Check data/flora/index.json extents against the heightfield.');
  }

  // ---- materials --------------------------------------------------------- //

  const uniforms = {
    uChiTime: { value: 0 },
    uChiWind: { value: new THREE.Vector2(0.82, 0.57) },
    uChiSway: { value: TUNE.wind.sway },
    uChiWaveK: { value: (Math.PI * 2) / TUNE.wind.waveM },
    // World space, pointing AT the sun. Filled from the scene's own light on
    // the first update; the fallback is the same instant world.js computes.
    uChiSun: { value: sunDirFallback() },
    uChiSunCol: { value: new THREE.Vector3(...SUN_FALLBACK.colour) },
    uChiSky: { value: new THREE.Vector3(...SUN_FALLBACK.sky) },
  };
  /** Resolved once, from the scene graph, at the first update. */
  let sunFound = false;

  const bladeMat = plantMaterial({ uniforms, billboard: false });
  const cardMat = plantMaterial({ uniforms, billboard: true, membrane: 0.30 });
  // Heads share the blade program deliberately. Under the software rasteriser
  // every extra shader program is seconds of compile time on the first frame,
  // and a flower head's own sway works out at four millimetres.
  const headMat = bladeMat;
  for (const m of [bladeMat, cardMat]) {
    confidence?.patch(m);
    disposables.push(m);
  }

  // ---- the layers -------------------------------------------------------- //

  const nearSet = instSet('flora-near', tuftGeometry(9, 2), bladeMat, tune.cap.near);
  const midSet = instSet('flora-mid', cardGeometry(7), cardMat, tune.cap.mid);
  const forbSet = instSet('flora-forb', forbGeometry(), bladeMat, tune.cap.forb);
  // A basal-scape plant is not a stem with leaves up it. Prairie dock and
  // compass plant are a 40 cm ROSETTE of huge paddle leaves at the ground with
  // a nearly naked flowering scape two or three metres over it — the dossier
  // names the rosette explicitly and it is the plant's whole diagnosis. Drawn
  // with the generic forb it became a leafy giant that filled the foreground.
  const rosetteSet = instSet('flora-rosette', rosetteGeometry(), bladeMat,
    Math.max(48, Math.round(tune.cap.forb * 0.45)));
  // One instanced set per ARCHETYPE, so the geometry a species gets is the
  // shape its record names. The flat horizontal plate is gone; nothing draws
  // one, because at 1.68 m eye height a corymb at 0.7 m is seen 11 degrees off
  // the horizontal and a flat disc is three pixels of nothing.
  const heads = {
    spike: instSet('flora-head-spike', spikeGeometry(), headMat, tune.cap.head),
    spire: instSet('flora-head-spire', spireGeometry(), headMat, tune.cap.head),
    panicle: instSet('flora-head-panicle', panicleGeometry(), headMat, tune.cap.head),
    ray: instSet('flora-head-ray', rayGeometry(false), headMat, tune.cap.head),
    raydroop: instSet('flora-head-raydroop', rayGeometry(true), headMat, tune.cap.head),
    pompom: instSet('flora-head-pompom', pompomGeometry(), headMat, tune.cap.head),
    dome: instSet('flora-head-dome', domeGeometry(), headMat, tune.cap.head),
    corymb: instSet('flora-head-corymb', corymbGeometry(), headMat, tune.cap.head),
    compound: instSet('flora-head-compound', compoundGeometry(), headMat, tune.cap.head),
  };
  const sets = [nearSet, midSet, forbSet, rosetteSet, ...Object.values(heads)];
  for (const s of sets) { group.add(s.mesh); disposables.push(s.mesh.geometry); }

  // ---- placement --------------------------------------------------------- //

  const centres = { near: null, yaw: null };
  const waterY = terrain.heightfield?.meta?.water_surface_m ?? 0;

  // The lattice each layer is scattered on, and the ring the shader fades it
  // over — the second strictly inside the first by `step`. See `ringsFor`.
  const step = tune.step.near;
  const rings = {};
  for (const layer of ['near', 'mid', 'forb']) {
    rings[layer] = ringsFor(tune[layer], step);
    rings[layer].head = headRingOf(rings[layer].fade);
  }
  /** Which ring each rooted set is drawn on. A rosette is a forb. */
  const ringOfSet = {
    'flora-near': rings.near, 'flora-mid': rings.mid,
    'flora-forb': rings.forb, 'flora-rosette': rings.forb,
  };

  /** A community that stands in no water, for the plantable-ground question the
   *  gate asks without naming a species. */
  const NO_COMMUNITY = { standsInWater: false };

  /** Ground the plant stands on, or null if it may not stand here. */
  function station(e, n, zone, species) {
    if (growthBlocked(e, n)) return null;
    if (water.isWater(e, n)) {
      // A water BUFFER is not permission for every member of that community to
      // stand in the channel. Only records whose role is explicitly `emergent`
      // may root in water, and the corrected signed shore-distance field below
      // keeps even those inside the eight-metre marsh edge rather than assigning
      // distance zero to the entire river.
      return zone.standsInWater && species?.role === 'emergent' ? waterY : null;
    }
    for (const b of blocks) {
      const dx = e - b.e;
      const dz = n - b.n;
      if (dx * dx + dz * dz < b.r2 && pointInPolygon(b.pts, e, n)) return null;
    }
    return terrain.surfaceHeight(e, n);
  }

  function rebuildGround(camE, camN, cone) {
    nearSet.reset();
    midSet.reset();
    for (const k in heads) heads[k].reset();

    const near = rings.near;
    const mid = rings.mid;
    // NEAR: individual tufts, dense enough to close the ground.
    nearSet.ring(near.fade);
    scatter(camE, camN, tune.near.cell, tune.near.perCell,
      near.lattice.outer, near.lattice.inner, 0x51ed27, cone,
      (e, n, r, rng) => {
        const zone = finder(e, n);
        if (!zone || !zone.graminoids.length) return;
        // The community's own recorded matrix cover decides whether this slot
        // carries a plant — the same rule the forb layer has always applied to
        // its own recorded densities, on the field the matrix layer ignored.
        if (rng() > zone.matrixShare) return;
        const sp = pick(zone.graminoids, rng());
        const y = station(e, n, zone, sp);
        if (y === null) return;
        if (crowdsTheWalker(sp, r)) return;
        // The head is placed off the height the PLANT was actually given, and
        // only if the plant was actually drawn. Round 1 drew the two from
        // independent draws of the same range, so a 2.0 m cordgrass spike
        // could stand over a 1.25 m tuft — which is the pair of flower heads
        // the critic found floating unattached in the open sky.
        const h = placeGraminoid(nearSet, sp, e, y, n, rng);
        if (h > 0 && r <= near.head[0] + step) {
          maybeHead(heads, sp, e, y, n, rng, h, near.head);
        }
      });

    // MID: clump cards. The inner edge overlaps the near ring so the change of
    // representation happens inside the field rather than at a visible circle.
    midSet.ring(mid.fade);
    scatter(camE, camN, tune.mid.cell, tune.mid.perCell,
      mid.lattice.outer, mid.lattice.inner, 0x9e3779, cone,
      (e, n, r, rng) => {
        const zone = finder(e, n);
        if (!zone || !zone.graminoids.length) return;
        // A clump card stands for the same matrix the near tufts do, so it is
        // thinned by the same recorded cover. Applying it to one layer and not
        // the other would put a seam at the near/mid crossover exactly where
        // the change of representation is supposed to be invisible.
        if (rng() > zone.matrixShare) return;
        const sp = pick(zone.graminoids, rng());
        const y = station(e, n, zone, sp);
        if (y === null) return;
        placeCard(midSet, sp, zone, e, y, n, rng);
      });
    stats.rebuilds++;
  }

  function rebuildForbs(camE, camN, cone) {
    forbSet.reset();
    rosetteSet.reset();
    const f = rings.forb;
    forbSet.ring(f.fade);
    rosetteSet.ring(f.fade);
    scatter(camE, camN, tune.forb.cell, tune.forb.perCell,
      f.lattice.outer, f.lattice.inner, 0x2545f9, cone, (e, n, r, rng) => {
        const zone = finder(e, n);
        if (!zone || !zone.forbs.length) return;
        // The forb layer's density is the zone's OWN summed density_per_ha, so a
        // sparse community stays sparse. `share` is the chance this lattice slot
        // is used at all.
        if (rng() > zone.forbShare) return;
        const sp = pick(zone.forbs, rng());
        const y = station(e, n, zone, sp);
        if (y === null) return;
        if (crowdsTheWalker(sp, r)) return;
        const set = sp.form === 'forb_basal_scape' ? rosetteSet : forbSet;
        const h = placeForb(set, sp, e, y, n, rng);
        if (h > 0 && r <= f.head[0] + step) {
          maybeHead(heads, sp, e, y, n, rng, h, f.head);
        }
      });
  }

  // Forbs and their heads share the head sets with the graminoids, so the two
  // ground rebuilds have to happen together or the heads would be half-cleared.
  function rebuildAll(camE, camN, cone) {
    rebuildGround(camE, camN, cone);
    rebuildForbs(camE, camN, cone);
    for (const s of sets) s.commit();
    stats.instances = sets.reduce((a, s) => a + s.mesh.count, 0);
    stats.sets = Object.fromEntries(sets.map((s) => [s.mesh.name, s.mesh.count]));
    stats.capped = sets.filter((s) => s.mesh.count >= s.max).map((s) => s.mesh.name);
    stats.triangles = sets.reduce((a, s) => a + s.mesh.count * s.tris, 0);
    stats.drawCalls = sets.filter((s) => s.mesh.count > 0).length;
  }

  const tmpV = new THREE.Vector3();
  const tmpF = new THREE.Vector3();

  return {
    group,
    stats,
    zoneAt(e, n) { return finder(e, n)?.id ?? null; },
    shoreDistance(e, n) { return water.distance(e, n); },
    /** May a rooted plant stand here at all — the travelled track, the
     *  building footprints and the water answered in one call. A gate
     *  measuring how densely a community was planted has to divide by the
     *  ground that was actually available to it, not by the disc it sampled. */
    plantableAt(e, n) { return station(e, n, NO_COMMUNITY, null) !== null; },
    /** What each compiled community carries out of its record, so the gate can
     *  ask whether the authored number reached the renderer rather than
     *  trusting that it did. */
    communities() {
      return zones.map((z) => ({
        id: z.id, matrixShare: z.matrixShare, bareSoil: z.bareSoil,
        graminoids: z.graminoids.length,
      }));
    },
    /** The lattice/fade rings and the rebuild step, for the gate that checks a
     *  plant cannot arrive already grown. */
    rings: { step, layers: rings },
    /** The height multiplier the vertex shader gives an instance of `setName`
     *  standing `d` metres from the camera — the same ramp, in JS. */
    fadeAt(setName, d) {
      const ring = ringOfSet[setName];
      return ring ? fadeOf(ring.fade, d) : null;
    },

    update(dt, camera) {
      uniforms.uChiTime.value += dt * TUNE.wind.speedNear;
      if (!sunFound) {
        sunFound = sunFromScene(group, uniforms, problems);
      }
      if (!camera) return;
      camera.getWorldPosition(tmpV);
      const e = tmpV.x;
      const n = -tmpV.z;

      // Forward in ENU; -Z is north (terrain.js).
      camera.getWorldDirection(tmpF);
      const fl = Math.hypot(tmpF.x, tmpF.z) || 1;
      const fe = tmpF.x / fl;
      const fn = -tmpF.z / fl;
      const yaw = Math.atan2(fe, fn);
      const turned = centres.yaw === null
        || Math.abs(((yaw - centres.yaw + Math.PI * 3) % (Math.PI * 2)) - Math.PI)
           > CONE_YAW_STEP;
      if (turned || moved(centres.near, e, n, step)) {
        rebuildAll(e, n, { fe, fn, cos: CONE_COS });
        centres.near = { e, n };
        centres.yaw = yaw;
      }
    },

    dispose() {
      for (const d of disposables) d?.dispose?.();
    },
  };
}

/** What it returns when there is nothing it is allowed to draw. */
function inertRig(group, stats) {
  return {
    group,
    stats,
    zoneAt() { return null; },
    update() {},
    dispose() {},
  };
}

function moved(centre, e, n, step) {
  if (!centre) return true;
  return Math.hypot(e - centre.e, n - centre.n) > step;
}

/** SUN_FALLBACK as a direction, in three's axes: +x east, +y up, -z north. */
function sunDirFallback() {
  const az = SUN_FALLBACK.azimuthDeg * Math.PI / 180;
  const el = SUN_FALLBACK.elevationDeg * Math.PI / 180;
  const horiz = Math.cos(el);
  return new THREE.Vector3(
    Math.sin(az) * horiz, Math.sin(el), -Math.cos(az) * horiz,
  ).normalize();
}

/**
 * Find the sun the SCENE already built and light the sward with it.
 *
 * main.js mounts this module with no reference to world.js, so the light is
 * found by walking up from our own group to the scene root. That is deliberate
 * rather than lazy: world.js derives the sun from the scene record's date,
 * latitude and local mean time, and a second sun invented here would light the
 * prairie from one direction and the buildings from another in the same frame.
 * If there is no directional light to find, the fallback is used and SAID —
 * silently lighting the sward from a guessed sun is the class of error this
 * project exists to avoid.
 *
 * @returns {boolean} true once it has an answer, right or fallback.
 */
function sunFromScene(group, uniforms, problems) {
  let root = group;
  while (root.parent) root = root.parent;
  if (root === group) return false;          // not mounted yet; ask again
  let sun = null;
  let sky = null;
  root.traverse((o) => {
    if (!sun && o.isDirectionalLight) sun = o;
    if (!sky && o.isHemisphereLight) sky = o;
  });
  if (!sun) {
    problems.push('flora: the scene carries no directional light — the sward is lit by '
      + `flora.js's own fallback sun (${SUN_FALLBACK.elevationDeg}° up, bearing `
      + `${SUN_FALLBACK.azimuthDeg}°) and may not agree with the rest of the frame`);
    return true;
  }
  sun.updateWorldMatrix(true, false);
  sun.target?.updateWorldMatrix(true, false);
  const from = new THREE.Vector3().setFromMatrixPosition(sun.matrixWorld);
  const to = sun.target
    ? new THREE.Vector3().setFromMatrixPosition(sun.target.matrixWorld)
    : new THREE.Vector3();
  uniforms.uChiSun.value.copy(from).sub(to).normalize();
  const i = sun.intensity;
  uniforms.uChiSunCol.value.set(sun.color.r * i, sun.color.g * i, sun.color.b * i);
  if (sky) {
    const j = sky.intensity;
    uniforms.uChiSky.value.set(sky.color.r * j, sky.color.g * j, sky.color.b * j);
  }
  return true;
}

function mergeTune(level) {
  const t = {
    near: { ...TUNE.near }, mid: { ...TUNE.mid }, forb: { ...TUNE.forb },
    cap: { ...TUNE.cap }, step: { ...TUNE.step },
  };
  const preset = level === 'light' ? LOW : level === 'balanced' ? MID : null;
  if (preset) {
    Object.assign(t.near, preset.near);
    Object.assign(t.mid, preset.mid);
    Object.assign(t.forb, preset.forb);
    Object.assign(t.cap, preset.cap);
  }
  return t;
}

/* -------------------------------------------------------------------------- */
/* the records                                                                 */
/* -------------------------------------------------------------------------- */

async function getJSON(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
}

/** One fetch for the manifest, then exactly the files it names — never a probe.
 *  A 404 in the network log is indistinguishable from a broken boot. */
async function loadFlora(dataBase, problems) {
  if (!dataBase) {
    problems.push('flora: no data base URL — nothing is planted');
    return null;
  }
  let index;
  const indexUrl = new URL('flora/index.json', dataBase);
  try {
    index = await getJSON(indexUrl);
  } catch (err) {
    problems.push(`flora: ${err.message} — no vegetation is drawn, and the ground is `
      + 'the bare terrain surface');
    return null;
  }
  if (!Array.isArray(index.zones) || !index.zones.length) {
    problems.push('flora: the manifest lists no zones — no vegetation is drawn');
    return null;
  }
  const files = new Map();
  const wanted = [
    ...index.zones.map((z) => ['zone', z.id, z.file]),
    ...(index.palettes ?? []).map((p) => ['palette', p.id, p.file]),
  ];
  const loaded = await Promise.all(wanted.map(async ([kind, id, file]) => {
    if (!file) return [kind, id, null, 'the manifest gave no file'];
    try {
      return [kind, id, await getJSON(new URL(`flora/${file}`, dataBase)), null];
    } catch (err) {
      return [kind, id, null, err.message];
    }
  }));
  for (const [kind, id, body, why] of loaded) {
    if (!body) { problems.push(`flora: ${kind} ${id} — ${why}`); continue; }
    files.set(`${kind}:${id}`, body);
  }
  return { index, files };
}

/** Per zone: a weighted graminoid list, a weighted forb list, colours, extent. */
function compileZones({ index, files }, terrain, problems, stats) {
  const seenForms = new Set();
  const out = [];
  // The manifest PUBLISHES the shape vocabulary, so a value added there and
  // not here is a flower the renderer would silently drop. Caught at boot,
  // once, against the list itself rather than against whatever happens to be
  // planted near the visitor.
  for (const shape of index.vocabulary?.inflorescence_shapes ?? []) {
    if (!HEAD_OF_SHAPE[shape]?.kind) {
      stats.unimplementedShapes.push(shape);
      problems.push(`flora: the manifest publishes inflorescence shape '${shape}' and this `
        + 'renderer has no archetype for it — any species recording it draws no flower');
    }
  }
  const byPriority = [...index.zones]
    .map((z) => ({ ...z, record: files.get(`zone:${z.id}`) }))
    .filter((z) => {
      if (!z.record) return false;
      if (!Array.isArray(z.record.species)) {
        problems.push(`flora: zone ${z.id} carries no species list`);
        return false;
      }
      return true;
    });

  for (const entry of byPriority) {
    const rec = entry.record;
    const palette = files.get(`palette:${rec.palette ?? entry.palette}`) ?? null;
    const graminoids = [];
    const forbs = [];
    let forbPerM2 = 0;
    let coverSum = 0;

    for (const sp of rec.species) {
      if (!OUR_ROLES.has(sp.role)) continue;          // trees.js draws the rest
      const form = sp.form;
      const isGrass = GRAMINOID_FORMS.has(form);
      const isForb = FORB_FORMS.has(form);
      if (!isGrass && !isForb) {
        if (!seenForms.has(form)) {
          seenForms.add(form);
          stats.unimplementedForms.push(form);
          problems.push(`flora: form '${form}' is not implemented — `
            + `${sp.id ?? sp.binomial} is recorded and not drawn`);
        }
        continue;
      }
      const built = buildSpecies(sp, palette, problems, entry.id);
      if (!built) continue;
      stats.species++;
      if (isGrass) {
        graminoids.push(built);
        coverSum += built.weight;
      } else {
        forbs.push(built);
        forbPerM2 += built.weight;
      }
    }
    if (coverSum > 0) for (const g of graminoids) g.weight /= coverSum;
    if (forbPerM2 > 0) for (const f of forbs) f.weight /= forbPerM2;

    // How much of the ground a community's matrix actually covers is AUTHORED,
    // per zone, in the record's own `cover` block — and nothing in this
    // renderer had ever asked for it. Every one of the ten communities was
    // planted at the single lattice density L32 tuned on the closed
    // wet-prairie sward, so the settled town (`bare_soil_fraction: 0.45` by
    // its own record), the shaded riverbank understory (`matrix_fraction`
    // 0.45) and the lakeshore sand (0.35) were all drawn as densely as prairie
    // that covers the ground completely. `tools/validate.py` gates this field
    // on every run and `index.json` denormalises `bare_soil_fraction` so the
    // ground shader can fetch it once: the number was written, checked and
    // shipped to the browser, and then never read.
    //
    // It is a probability directly, and that is the whole reason 1.0 is the
    // anchor rather than some scaling: a zone recording full matrix cover is
    // planted exactly as it was before, so the density tuned against the
    // reference photographs is untouched, and no zone can ask for more
    // geometry than the lattice already carries.
    const cover = rec.cover ?? {};
    let matrixShare = cover.matrix_fraction;
    if (typeof matrixShare !== 'number' || !(matrixShare >= 0)) {
      problems.push(`flora: zone ${entry.id} records no cover.matrix_fraction — its sward `
        + 'falls back to a fully closed one, which is a claim its record does not make');
      matrixShare = 1;
    }

    const cell = TUNE.forb.cell;
    out.push({
      id: entry.id,
      zone: entry.zone,
      extent: rec.extent ?? entry.extent ?? null,
      priority: rec.extent?.priority ?? entry.priority ?? 0,
      standsInWater: rec.extent?.kind === 'buffer' && rec.extent?.of === 'water'
        && rec.species.some((sp) => sp.role === 'emergent'),
      graminoids,
      forbs,
      /** Chance a matrix lattice slot is used at all: the record's own
       *  `cover.matrix_fraction`. Clamped only because a fraction over 1 would
       *  be a bookkeeping error the validator already refuses. */
      matrixShare: clamp01(matrixShare),
      bareSoil: typeof cover.bare_soil_fraction === 'number' ? cover.bare_soil_fraction : null,
      /** Chance a forb lattice slot is used, from the record's own densities. */
      forbShare: Math.min(1, forbPerM2 * cell * cell / TUNE.forb.perCell),
      matColor: meanColor(graminoids, palette),
      palette,
    });
  }
  out.sort((a, b) => b.priority - a.priority);
  for (let i = 1; i < out.length; i++) {
    if (out[i].priority === out[i - 1].priority) {
      problems.push(`flora: ${out[i - 1].id} and ${out[i].id} share priority `
        + `${out[i].priority} — which community wins where they overlap is undefined`);
      break;
    }
  }
  return out.filter((z) => z.extent);
}

/** One species entry, reduced to numbers the placer can use per instance. */
function buildSpecies(sp, palette, problems, zoneId) {
  const h = sp.height_m;
  if (!Array.isArray(h) || h.length !== 2 || !(h[1] > 0)) {
    problems.push(`flora: ${zoneId}/${sp.id ?? sp.binomial} has no usable height_m`);
    return null;
  }
  const july = sp.july ?? {};
  const veg = july.phenology === 'vegetative' || july.phenology === 'budding';
  let inflor = july.inflorescence ?? null;
  if (veg && inflor) {
    // CONTRACT.md §5.4 rule 1. The record contradicts itself; the July gate wins
    // and the head is not drawn, because a flowering culm on a vegetative grass
    // is the error the whole season check exists to prevent.
    problems.push(`flora: ${zoneId}/${sp.id ?? sp.binomial} is '${july.phenology}' and `
      + 'still carries an inflorescence — no head is drawn; the record needs fixing');
    inflor = null;
  }
  const greens = palette?.greens ?? [];
  const base = rgb(july.foliage_rgb) ?? rgb(greens[1]) ?? [0.32, 0.40, 0.17];
  const alt = rgb(july.foliage_rgb_alt) ?? rgb(greens[2]) ?? base;

  const ab = sp.abundance ?? {};
  let weight = 0;
  if (Array.isArray(ab.cover_fraction)) weight = mid(ab.cover_fraction);
  else if (Array.isArray(ab.density_per_ha)) weight = mid(ab.density_per_ha) / 10000;
  else if (Array.isArray(ab.stems_per_m2)) weight = mid(ab.stems_per_m2);
  if (!(weight > 0)) weight = 0.01;

  return {
    id: sp.id ?? sp.binomial ?? 'unnamed',
    form: sp.form,
    role: sp.role,
    weight,
    height: h,
    width: Array.isArray(sp.width_m) ? sp.width_m : null,
    shape: GRASS_SHAPE[sp.form] ?? { arch: 0.28, spread: 0.45 },
    base,
    alt,
    dry: rgb(palette?.dry_accent) ?? [0.55, 0.53, 0.35],
    head: headOf(inflor, sp, problems, zoneId),
    conf: LEVEL[sp.confidence] ?? LEVEL.inferred,
  };
}

/**
 * The flower, off the record's own `july.inflorescence.shape`. A shape the
 * renderer has no archetype for is REPORTED and draws nothing: substituting a
 * different archetype is exactly the failure this dispatch exists to end, and
 * a missing flower that is written down is recoverable in a way that a wrong
 * one silently drawn is not.
 */
function headOf(inflor, sp, problems, zoneId) {
  if (!inflor) return null;
  const style = HEAD_OF_SHAPE[inflor.shape];
  if (!style) {
    problems.push(`flora: ${zoneId}/${sp.id ?? sp.binomial} records inflorescence shape `
      + `'${inflor.shape}', which has no archetype — its flower is not drawn`);
    return null;
  }
  return {
    kind: style.kind,
    count: style.count,
    tilt: style.tilt,
    band: style.band,
    color: rgb(inflor.rgb) ?? [0.8, 0.8, 0.7],
    frac: clamp01(inflor.height_frac ?? 0.9),
    size: Array.isArray(inflor.size_m) ? inflor.size_m : [0.06, 0.12],
  };
}

function meanColor(graminoids, palette) {
  const fallback = rgb(palette?.greens?.[1]) ?? [0.30, 0.38, 0.16];
  if (!graminoids.length) return fallback;
  const out = [0, 0, 0];
  let w = 0;
  for (const g of graminoids) {
    for (let i = 0; i < 3; i++) out[i] += (g.base[i] * 0.6 + g.alt[i] * 0.4) * g.weight;
    w += g.weight;
  }
  return w > 0 ? out.map((v) => v / w) : fallback;
}

function rgb(v) {
  if (!Array.isArray(v) || v.length < 3) return null;
  // sRGB bytes in the record; linear in the shader. three's Color does the
  // transfer, and doing it here means the palette is authored the way a
  // photograph is measured.
  const c = new THREE.Color(v[0] / 255, v[1] / 255, v[2] / 255).convertSRGBToLinear();
  return [c.r, c.g, c.b];
}
function mid(range) { return (range[0] + range[1]) / 2; }
function clamp01(v) { return Math.min(1, Math.max(0, v)); }

/* -------------------------------------------------------------------------- */
/* where a community is — CONTRACT.md §4                                       */
/* -------------------------------------------------------------------------- */

/** Distance-to-water, two chamfer passes over the committed heightfield.
 *  `buffer` extents ask it for every plant placed. */
function waterField(terrain) {
  const hf = terrain.heightfield;
  const cell = 4.0;
  const surfaceY = hf?.meta?.water_surface_m ?? 0;
  if (!hf?.loaded) {
    return {
      surfaceY,
      isWater: (e, n) => terrain.isWater(e, n),
      distance: () => Infinity,
    };
  }
  const e0 = hf.originE;
  const n0 = hf.originN;
  const cols = Math.max(2, Math.ceil(hf.widthM / cell) + 1);
  const rows = Math.max(2, Math.ceil(hf.depthM / cell) + 1);
  const BIG = 1e6;
  // Two fields make this a distance to the SHORE, not merely a distance to
  // water. The old one seeded every water cell with zero, so a `0–8 m from
  // water` marsh extent matched the middle of the river just as strongly as
  // the bank. On land we ask for the nearest water cell; in water we ask for
  // the nearest land cell.
  const toWater = new Float32Array(cols * rows).fill(BIG);
  const toLand = new Float32Array(cols * rows).fill(BIG);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i = r * cols + c;
      if (terrain.isWater(e0 + c * cell, n0 + r * cell)) toWater[i] = 0;
      else toLand[i] = 0;
    }
  }
  const solve = (d) => {
    const put = (i, v) => { if (v < d[i]) d[i] = v; };
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const i = r * cols + c;
        if (c > 0) put(i, d[i - 1] + cell);
        if (r > 0) put(i, d[i - cols] + cell);
        if (c > 0 && r > 0) put(i, d[i - cols - 1] + cell * 1.4142);
        if (c < cols - 1 && r > 0) put(i, d[i - cols + 1] + cell * 1.4142);
      }
    }
    for (let r = rows - 1; r >= 0; r--) {
      for (let c = cols - 1; c >= 0; c--) {
        const i = r * cols + c;
        if (c < cols - 1) put(i, d[i + 1] + cell);
        if (r < rows - 1) put(i, d[i + cols] + cell);
        if (c < cols - 1 && r < rows - 1) put(i, d[i + cols + 1] + cell * 1.4142);
        if (c > 0 && r < rows - 1) put(i, d[i + cols - 1] + cell * 1.4142);
      }
    }
  };
  solve(toWater);
  solve(toLand);
  return {
    surfaceY,
    isWater: (e, n) => terrain.isWater(e, n),
    distance(e, n) {
      const c = Math.round((e - e0) / cell);
      const r = Math.round((n - n0) / cell);
      if (c < 0 || r < 0 || c >= cols || r >= rows) return Infinity;
      const i = r * cols + c;
      return terrain.isWater(e, n) ? toLand[i] : toWater[i];
    },
  };
}

/** Highest priority wins; a point that matches nothing gets nothing. */
function zoneFinder(zones, terrain, water) {
  return function find(e, n) {
    for (const z of zones) {
      if (matches(z.extent, e, n, terrain, water)) return z;
    }
    return null;
  };
}

function matches(x, e, n, terrain, water) {
  if (!x) return false;
  if (x.box) {
    const be = x.box.e;
    const bn = x.box.n;
    if (be && (e < be[0] || e > be[1])) return false;
    if (bn && (n < bn[0] || n > bn[1])) return false;
  }
  let ok = false;
  switch (x.kind) {
    case 'everywhere':
      ok = true;
      break;
    case 'elevation_band': {
      const y = terrain.surfaceHeight(e, n);
      ok = Array.isArray(x.elev_m) && y >= x.elev_m[0] && y <= x.elev_m[1];
      break;
    }
    case 'polygon':
      ok = Array.isArray(x.polygon) && pointInPolygon(x.polygon, e, n);
      break;
    case 'buffer': {
      if (x.of !== 'water') return false;
      const dist = water.distance(e, n);
      const band = x.distance_m ?? [0, 0];
      ok = dist >= band[0] && dist <= band[1];
      break;
    }
    default:
      return false;
  }
  if (!ok) return false;
  for (const hole of x.exclude_polygons ?? []) {
    if (pointInPolygon(hole, e, n)) return false;
  }
  return true;
}

function pointInPolygon(pts, e, n) {
  let inside = false;
  for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
    const [xi, yi] = pts[i];
    const [xj, yj] = pts[j];
    if ((yi > n) !== (yj > n) && e < ((xj - xi) * (n - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
}

/** What fraction of the modelled DRY ground matches no community. Sampled over
 *  the whole heightfield, so it is a property of the dataset and not of where
 *  the visitor happens to stand. */
function auditCoverage(terrain, finder) {
  const hf = terrain.heightfield;
  if (!hf?.loaded) return 0;
  const step = 8;
  let land = 0;
  let bare = 0;
  for (let n = hf.originN; n <= hf.originN + hf.depthM; n += step) {
    for (let e = hf.originE; e <= hf.originE + hf.widthM; e += step) {
      if (terrain.isWater(e, n)) continue;
      land++;
      if (!finder(e, n)) bare++;
    }
  }
  return land ? bare / land : 0;
}

/** Buildings as centre + radius + polygon, so most rejections are one test. */
function footprintCircles(footprints) {
  return footprints.map((f) => {
    let e = 0;
    let n = 0;
    for (const p of f.pts) { e += p[0]; n += p[1]; }
    e /= f.pts.length;
    n /= f.pts.length;
    let r2 = 0;
    for (const p of f.pts) r2 = Math.max(r2, (p[0] - e) ** 2 + (p[1] - n) ** 2);
    // A metre of clearance: a wall meeting the sward flush reads as a wall
    // sunk in a lawn.
    const r = Math.sqrt(r2) + 1.0;
    return { e, n, r2: r * r, pts: f.pts };
  });
}

/* -------------------------------------------------------------------------- */
/* the lattice                                                                 */
/* -------------------------------------------------------------------------- */

/** Deterministic hash -> a repeatable per-slot random stream, so re-centring
 *  the lattice puts every plant back exactly where it was. */
function hash3(a, b, c) {
  // Math.imul throughout, and it is load-bearing rather than tidy: `a * k` on a
  // full 32-bit seed is a ~2^62 double, the low bits fall off the mantissa, and
  // the four plants in a cell all drew the same "random" number and stacked up
  // on the same blade of grass. The field looked a quarter as dense as it was.
  let h = Math.imul(a, 0x27d4eb2d) ^ Math.imul(b, 0x165667b1) ^ Math.imul(c, 0x9e3779b1);
  h = Math.imul(h ^ (h >>> 15), 0x85ebca6b);
  h = Math.imul(h ^ (h >>> 13), 0xc2b2ae35);
  return (h ^ (h >>> 16)) >>> 0;
}

function rngFrom(seed) {
  let s = seed >>> 0 || 1;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >>> 17;
    s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
}

/** Walk the lattice cells around the camera, calling `emit` per jittered slot
 *  inside the ring. The grid is world-anchored, not camera-anchored. */
function scatter(camE, camN, cell, perCell, radius, inner, salt, cone, emit) {
  const c0 = Math.floor((camE - radius) / cell);
  const c1 = Math.ceil((camE + radius) / cell);
  const r0 = Math.floor((camN - radius) / cell);
  const r1 = Math.ceil((camN + radius) / cell);
  const sub = Math.max(1, Math.round(Math.sqrt(perCell)));
  const rr = radius * radius;
  const ri = inner * inner;
  for (let r = r0; r <= r1; r++) {
    for (let c = c0; c <= c1; c++) {
      const cellSeed = hash3(c, r, salt);
      for (let k = 0; k < perCell; k++) {
        const rng = rngFrom(hash3(cellSeed, k, 0x68bc21eb));
        // A jittered sub-grid, not free scatter: free scatter leaves holes
        // the eye reads as bare soil and clusters it reads as one plant.
        const sx = k % sub;
        const sy = (k / sub) | 0;
        const e = (c + (sx + rng()) / sub) * cell;
        const n = (r + (sy + rng()) / sub) * cell;
        const d2 = (e - camE) ** 2 + (n - camN) ** 2;
        if (d2 > rr || d2 < ri) continue;
        const d = Math.sqrt(d2);
        // Outside the view cone there is nothing to see and everything to pay
        // for: three has no per-instance culling, so a plant behind the walker
        // still runs its vertex shader. The cone is far wider than the frame
        // (62 degrees against 38) so a turn of a dozen degrees is planted
        // before the lattice catches up; inside CONE_KEEP_M everything is kept,
        // because that ring must not flicker as you turn on the spot.
        if (cone && d > CONE_KEEP_M
          && ((e - camE) * cone.fe + (n - camN) * cone.fn) / d < cone.cos) continue;
        emit(e, n, d, rng, cellSeed);
      }
    }
  }
}

/** Weighted pick from a compiled species list (weights sum to 1). */
function pick(list, u) {
  let acc = 0;
  for (const item of list) {
    acc += item.weight;
    if (u <= acc) return item;
  }
  return list[list.length - 1];
}

/* -------------------------------------------------------------------------- */
/* placing one plant                                                           */
/* -------------------------------------------------------------------------- */

const _m = new THREE.Matrix4();
const _e = new THREE.Euler();
const _c = new THREE.Color();

/**
 * A plant may not be standing where the walker is standing.
 *
 * The near ring is camera-relative and had no inner radius, so a three-metre
 * prairie dock could be planted at arm's length and fill the frame — which is
 * what the timber critic handed back as "the giant yellow-flowered plant at
 * absurd scale in the immediate foreground". The clearance is not a fudge
 * factor: it is the walker's own shoulder half-width (walker.js WALK.radius,
 * 0.34 m) plus the radius of the clump the record itself gives, because a
 * plant whose crown overlaps the body of the person looking at it is a plant
 * that person has walked through.
 */
const WALKER_RADIUS_M = 0.34;
function crowdsTheWalker(sp, r) {
  const clump = sp.width ? mid(sp.width) * 0.5 : Math.min(0.35, mid(sp.height) * 0.16);
  return r < WALKER_RADIUS_M + clump;
}

function instSet(name, geometry, material, max) {
  const mesh = new THREE.InstancedMesh(geometry, material, max);
  mesh.name = name;
  mesh.castShadow = false;
  mesh.receiveShadow = false;
  // Always around the viewer; culling can only throw it away by mistake.
  mesh.frustumCulled = false;
  // Drawn BEFORE the ground on purpose: the ground is a full-screen standard
  // material with a shadow lookup and is the most expensive thing in the frame,
  // so every sward fragment that lands first is one the depth test never
  // shades. Measured: at eye height in open prairie it pays for the sward.
  mesh.renderOrder = -3;
  mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  mesh.instanceColor = new THREE.InstancedBufferAttribute(new Float32Array(max * 3), 3);
  mesh.instanceColor.setUsage(THREE.DynamicDrawUsage);
  const params = new THREE.InstancedBufferAttribute(new Float32Array(max * 4), 4);
  params.setUsage(THREE.DynamicDrawUsage);
  geometry.setAttribute('aFlora', params);
  // docs/PROVENANCE.md: per-PLANT here, because the evidence behind a species
  // belongs to the species, not to the archetype it is drawn with. An instanced
  // attribute reaches the same shader declaration a per-vertex one would.
  const conf = new THREE.InstancedBufferAttribute(new Float32Array(max), 1);
  conf.setUsage(THREE.DynamicDrawUsage);
  geometry.setAttribute('_confidence', conf);
  // The ring this instance is faded over, and how far its origin stands above
  // the base of its own plant — zero for anything rooted, the stalk height for
  // a flower head, which is what lets the shader lower a head to the ground as
  // its plant shrinks instead of leaving it hanging where the CPU put it.
  const ringAttr = new THREE.InstancedBufferAttribute(new Float32Array(max * 4), 4);
  ringAttr.setUsage(THREE.DynamicDrawUsage);
  geometry.setAttribute('aChiRing', ringAttr);
  const riseAttr = new THREE.InstancedBufferAttribute(new Float32Array(max), 1);
  riseAttr.setUsage(THREE.DynamicDrawUsage);
  geometry.setAttribute('aChiRise', riseAttr);
  /** Never fades: overwritten before the first push of every pass. */
  let ringNow = [1e9, 1e-4, 0, 0];

  const tris = (geometry.index ? geometry.index.count : geometry.attributes.position.count) / 3;
  let n = 0;
  return {
    mesh,
    tris,
    max,
    reset() { n = 0; },
    /** The ring every following push is drawn on, `[outer, band, inner,
     *  innerBand]`. A head set is pushed to from two different rings in one
     *  rebuild, so this is per-push state rather than per-set. */
    ring(r) { ringNow = r; },
    /**
     * @param {number} [tilt] radians off vertical, baked into the INSTANCE
     *   matrix rather than the vertex program: a flower head is held at an
     *   angle and the tilt has to vary per instance, while the yaw slot in
     *   `aFlora` can only turn it about the vertical. Pass `yaw` 0 alongside a
     *   tilt — the matrix carries the whole rotation.
     * @param {number} [tiltAz] which way it leans.
     * @param {number} [rise] metres this instance's origin stands above the
     *   base of its plant. The shader lowers it by `rise * (1 - fade)`.
     * @returns {boolean} false when the cap is reached — the caller stops.
     */
    push(e, y, n2, yaw, height, spread, arch, r, g, b, conf2, tilt = 0, tiltAz = 0, rise = 0) {
      if (n >= max) return false;
      if (tilt !== 0) {
        _e.set(Math.cos(tiltAz) * tilt, yaw, Math.sin(tiltAz) * tilt, 'YXZ');
        _m.makeRotationFromEuler(_e);
        _m.setPosition(e, y, -n2);
      } else {
        _m.makeTranslation(e, y, -n2);
      }
      mesh.setMatrixAt(n, _m);
      mesh.instanceColor.setXYZ(n, r, g, b);
      params.setXYZW(n, height, spread, arch, yaw);
      conf.setX(n, conf2);
      ringAttr.setXYZW(n, ringNow[0], ringNow[1], ringNow[2], ringNow[3]);
      riseAttr.setX(n, rise);
      n++;
      return true;
    },
    commit() {
      mesh.count = n;
      mesh.instanceMatrix.needsUpdate = true;
      mesh.instanceColor.needsUpdate = true;
      params.needsUpdate = true;
      conf.needsUpdate = true;
      ringAttr.needsUpdate = true;
      riseAttr.needsUpdate = true;
    },
  };
}

/** Uneven light is most of what separates the July photographs from the
 *  October one (luminance spanning 150-210 levels against 90). A per-plant
 *  patch factor from a smooth world-space field buys that mottling for one
 *  noise lookup — and it is patchiness in the vegetation, not a light. */
function patchOf(e, n) {
  return 0.66 + 0.72 * vnoise(e * 0.21 + 5.5, n * 0.21 - 2.3)
    * (0.72 + 0.42 * vnoise(e * 0.74 - 1.1, n * 0.74 + 6.2));
}

function tint(sp, u, v) {
  // Two greens per species, plus a small tonal jitter: the bar photographs show
  // several distinct greens within a metre, and one flat green reads as carpet.
  const t = u * u;
  const k = 0.82 + v * 0.40;
  return [
    (sp.base[0] * (1 - t) + sp.alt[0] * t) * k,
    (sp.base[1] * (1 - t) + sp.alt[1] * t) * k,
    (sp.base[2] * (1 - t) + sp.alt[2] * t) * k,
  ];
}

function placeGraminoid(set, sp, e, y, n, rng) {
  const u = rng();
  // The record's own height, at full size. The ring fade that used to be baked
  // in here is applied per frame in the vertex shader instead: baked, it could
  // only change when the lattice was rebuilt, which made it a step rather than
  // a ramp and put the plant's whole growth into one frame.
  const h = sp.height[0] + (sp.height[1] - sp.height[0]) * u;
  // width_m is the clump diameter the record gives; only fall back to a
  // proportion of the height when it does not. The proportion had cordgrass
  // splaying 1.1 m against a recorded 0.5-0.9.
  const spread = (sp.width ? mid(sp.width) : h * sp.shape.spread) * (0.78 + rng() * 0.5);
  const c = tint(sp, rng(), rng()).map((x) => x * patchOf(e, n));
  // A minority of dead thatch from last year's growth, at the base of the
  // clump. Kept a minority on purpose: a straw-coloured sward is October.
  const dry = rng() < 0.07;
  const col = dry
    ? [c[0] * 0.6 + sp.dry[0] * 0.5, c[1] * 0.6 + sp.dry[1] * 0.45, c[2] * 0.6 + sp.dry[2] * 0.5]
    : c;
  // The height is returned, and it is the height the HEAD must be hung off:
  // a zero says the cap was reached and nothing was drawn here, so nothing may
  // be hung off it either.
  return set.push(e, y, n, rng() * Math.PI * 2, h, spread,
    sp.shape.arch * (0.7 + rng() * 0.7), col[0], col[1], col[2], sp.conf) ? h : 0;
}

function placeCard(set, sp, zone, e, y, n, rng) {
  const u = rng();
  const h = (sp.height[0] + (sp.height[1] - sp.height[0]) * u) * 0.92;
  // A clump, not a hoarding. Width 1.25-2.15 x height made 2.5 m billboards
  // that tiled the mid-ground into flat-topped dark blocks.
  const w = h * (0.42 + rng() * 0.44);
  const c = tint(sp, rng(), rng()).map((x) => x * patchOf(e, n));
  // Mid-distance clumps carry a little of the zone's own mean, so the sea reads
  // as one community rather than as a spray of unrelated colours.
  const m = zone.matColor;
  set.push(e, y, n, 0, h, w, 0.5 + rng(),
    c[0] * 0.72 + m[0] * 0.28,
    c[1] * 0.72 + m[1] * 0.28,
    c[2] * 0.72 + m[2] * 0.28, sp.conf);
}

function placeForb(set, sp, e, y, n, rng) {
  const h = sp.height[0] + (sp.height[1] - sp.height[0]) * rng();
  // The leaf archetype is drawn at a nominal one metre, so whatever scales the
  // plant also scales its leaves. `width_m` is the CLUMP diameter, and a
  // riverbank shrub recorded at two metres across therefore grew sixty-
  // centimetre leaves and filled the river-bank shot with pale green arrowheads.
  // Clamped to the size a broad prairie leaf actually is — EXCEPT for a basal
  // rosette, whose recorded width IS the leaf span and whose whole diagnosis is
  // that the leaves are huge (prairie dock, 0.6-1.0 m across the rosette).
  const rosette = sp.form === 'forb_basal_scape';
  const spread = rosette
    ? THREE.MathUtils.clamp((sp.width ? mid(sp.width) * 0.5 : h * 0.18), 0.05, 0.55)
    : THREE.MathUtils.clamp(sp.width ? mid(sp.width) * 0.45 : h * 0.26, 0.07, 0.40);
  const c = tint(sp, rng() * 0.6, rng()).map((x) => x * patchOf(e, n));
  return set.push(e, y, n, rng() * Math.PI * 2, h, spread, 0.1 + rng() * 0.2,
    c[0], c[1], c[2], sp.conf) ? h : 0;
}

/**
 * The flower, and ONLY when the record says there is one: `sp.head` is null for
 * every vegetative grass, so no branch here can put a seed head on big bluestem
 * in July. See the July gate in the file header — it is unchanged.
 *
 * `plantH` is the height the plant was ACTUALLY given, not a fresh draw of the
 * same range, and it is only ever non-zero when the plant was actually drawn.
 * Both of those are the fix for the two heads the critic found floating in the
 * open sky with no stem beneath them.
 */
function maybeHead(heads, sp, e, y, n, rng, plantH, ring) {
  if (!sp.head || !(plantH > 0)) return;
  const set = heads[sp.head.kind];
  if (!set) return;
  set.ring(ring);
  // A forb instance IS one plant. A matrix instance is a bundle of shoots, and
  // only a minority of shoots in a grass clump carry a culm in mid-July — a
  // head on every tuft made a flowering cordgrass sward look like a wheat
  // field. L32.
  if (sp.role === 'matrix' || sp.role === 'emergent') {
    if (rng() > 0.16) return;
  }
  _c.setRGB(sp.head.color[0], sp.head.color[1], sp.head.color[2]);
  // One plant, several inflorescences, by architecture — see HEAD_OF_SHAPE.
  // A grass culm carries one panicle however the forb beside it branches.
  const grass = sp.role === 'matrix' || sp.role === 'emergent';
  const range = sp.head.count;
  const many = grass ? 1 : range[0] + ((rng() * (range[1] - range[0] + 1)) | 0);
  const spread = sp.width ? mid(sp.width) * 0.5 : plantH * 0.22;
  const tilt = sp.head.tilt;
  const top = plantH * sp.head.frac;
  const reach = PEDUNCLE[sp.head.kind] ?? 1.5;
  for (let i = 0; i < many; i++) {
    const size = sp.head.size[0] + (sp.head.size[1] - sp.head.size[0]) * rng();
    const lean = tilt[0] + (tilt[1] - tilt[0]) * rng();
    const a = rng() * Math.PI * 2;
    // The first head is terminal. The rest are carried DOWN the plant over the
    // architecture's own band, and the lower a branch starts the further out it
    // reaches — which is what puts a mountain mint's colour at knee height and
    // a loosestrife's up the whole stem, instead of parking every flower in the
    // scene on one plane a metre and a half off the ground where a standing
    // eye can barely see it against the sky.
    const down = i === 0 ? 0 : sp.head.band * rng();
    // ...and no further out than the branch under it can lean back and touch
    // the stem. The stalk is `reach` head-sizes long and leans by `lean`, so
    // that product IS the offset the plant can actually support.
    const r = i === 0 ? 0
      : Math.min(spread * (0.30 + rng() * 0.60) * (0.45 + 1.7 * down),
        reach * size * Math.sin(lean) * 0.94);
    // How far over its plant's base this head hangs. It is passed to the shader
    // as well as added to y, because the shader has to bring the head DOWN with
    // the plant as the ring fades it: a head left at the height the CPU put it
    // would hang in the air over a shrinking stem.
    const rise = top * (1 - down) * (0.94 + rng() * 0.10);
    if (!set.push(
      e + Math.sin(a) * r,
      y + rise,
      n + Math.cos(a) * r,
      rng() * Math.PI * 2, size, size, 0, _c.r, _c.g, _c.b, sp.conf, lean,
      // Leaning OUTWARD, along the branch that carries it, so the stalk below
      // it leans back toward the stem instead of hanging in the air.
      i === 0 ? rng() * Math.PI * 2 : a + Math.PI / 2,
      rise,
    )) return;
  }
}

/* -------------------------------------------------------------------------- */
/* archetype geometry                                                          */
/* -------------------------------------------------------------------------- */

/**
 * Every archetype is built at NOMINAL size — one metre tall, one across, at the
 * origin — and the vertex shader scales it per instance from the record's own
 * `height_m`, which is how one geometry is cordgrass at 1.8 m and little
 * bluestem at 0.5 m in the same draw call. `aDir` is the blade's azimuth; the
 * shader arches each blade outward along it, so a tuft opens into a fountain.
 */
function emptyGeo() {
  return { pos: [], nor: [], col: [], dir: [], side: [], idx: [], n: 0 };
}
function finishGeo(g, name) {
  const geo = new THREE.BufferGeometry();
  geo.name = name;
  geo.setAttribute('position', new THREE.Float32BufferAttribute(g.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(g.nor, 3));
  geo.setAttribute('color', new THREE.Float32BufferAttribute(g.col, 3));
  geo.setAttribute('aDir', new THREE.Float32BufferAttribute(g.dir, 2));
  geo.setAttribute('aSide', new THREE.Float32BufferAttribute(g.side, 3));
  geo.setIndex(g.idx);
  return geo;
}
function vert(g, x, y, z, nx, ny, nz, r, gg, b, dx, dz, sx = 0, sy = 0, sz = 0) {
  g.pos.push(x, y, z);
  g.nor.push(nx, ny, nz);
  g.col.push(r, gg, b);
  g.dir.push(dx, dz);
  // aSide is the offset from the archetype's own axis, in REAL metres, added
  // AFTER the height and spread scales — otherwise a wide clump gets wide
  // leaves, and cordgrass (0.5-0.9 m across, blades a centimetre or two wide)
  // ended up with leaves the width of a hand. It carries Y as well as XZ
  // because a grass blade TWISTS as it rises, so its width vector leaves the
  // horizontal plane, and because a basal rosette's leaves are a real size in
  // metres and must not scale with a three-metre flowering scape.
  g.side.push(sx, sy, sz);
  return g.n++;
}

/**
 * Light inside a closed sward, as a multiple of the species' own colour.
 *
 * Two things the round-1 ramp got wrong, and they are most of the near field's
 * tone. First, the argument is the height IN THE CANOPY and not the distance
 * along the blade: keyed off the blade's own length, a basal leaf 30 cm up in
 * a metre-and-a-half sward got the same lit tip as a culm reaching the top, so
 * the upper half of EVERY tuft came out pale and the near field read as a
 * bleached gradient. Second, and more important, sunlight does not arrive in a
 * stand as a smooth gradient — it arrives in FLECKS. At midday a fraction of
 * the leaves deep inside a prairie are in full sun through a gap and the rest
 * are in their neighbours' shade, and in the Woodworth photograph's nearest
 * five metres that is exactly what the bright pixels are: whole leaf faces at
 * (219, 233, 172), scattered at every depth, against a dark mass. A smooth
 * ramp cannot produce that. It produced a 25th percentile of 92 where the
 * photograph's is 31.
 *
 * `u` is height in the canopy, 0 at the floor and 1 at the surface; `fleck` is
 * this blade's own sunfleck gain, 0 when it is in shade.
 */
const CANOPY = {
  /** Diffuse light on the floor of a closed sward, and at its surface. */
  floor: 0.135,
  gradient: 0.62,
  gamma: 1.35,
  /** Chance a blade sits in a sunfleck, on the floor and at the surface. */
  fleckFloor: 0.05,
  fleckTop: 0.60,
  /** What a fleck is worth, and how much of it survives to depth u. */
  fleckGain: [0.80, 1.55],
  fleckReach: 0.55,
};
function shade(u, fleck = 0) {
  return CANOPY.floor + CANOPY.gradient * u ** CANOPY.gamma
    + fleck * (CANOPY.fleckReach + (1 - CANOPY.fleckReach) * u);
}

/** The same, shallower: a card is read almost edge-on, so the near field's
 *  near-black base turned the whole mid-ground into a dark wall. */
function cardShade(t) { return 0.22 + 0.62 * t; }

/**
 * A tuft of blades: the near-field workhorse. Half the blades are BASAL — short,
 * wide, low-angled leaves — and they are what closes the ground. A clump of
 * equal straps at full height reads as reeds in a pond; a real grass clump is
 * mostly leaf near the soil with a few shoots reaching the top of the sward.
 */
function tuftGeometry(blades = 12, segments = 2) {
  const g = emptyGeo();
  const rng = rngFrom(0x1835f10a);
  for (let b = 0; b < blades; b++) {
    // Half the blades are basal. They sprawl outward at a low angle, which is
    // where ground cover is cheapest to buy: a leaf lying over the soil hides
    // far more of it per triangle than one standing up in the air, and a real
    // grass clump is mostly leaf near the ground anyway.
    const basal = b < Math.round(blades / 2);
    const phi = (b / blades) * Math.PI * 2 + rng() * 0.9;
    const dx = Math.sin(phi);
    const dz = Math.cos(phi);
    // Lengths biased short: many leaves, few culms.
    const len = basal ? 0.24 + rng() * 0.34 : 0.40 + 0.60 * rng() ** 0.8;
    // Real half-widths, in metres: a coarse basal leaf is 3-6 cm across, a
    // culm leaf 1.5-3 cm. These are no longer multiplied by the clump spread.
    const wide = (basal ? 0.020 + rng() * 0.016 : 0.008 + rng() * 0.010);
    const lean = basal ? 0.52 + rng() * 0.44 : 0.14 + rng() * 0.26;
    const tone = 0.86 + rng() * 0.30;
    // Is THIS blade in a sunfleck? Decided once per blade, at the height its
    // tip reaches, so the lit leaves are scattered through the depth of the
    // stand instead of banded across the top of it. Nothing shades the topmost
    // leaves of a canopy, which is why fleckTop is essentially 1.
    const uTip = Math.min(1, (len * (1 - lean * 0.62)) / 0.92);
    const fleck = rng() < CANOPY.fleckFloor + (CANOPY.fleckTop - CANOPY.fleckFloor) * uTip
      ? CANOPY.fleckGain[0] + (CANOPY.fleckGain[1] - CANOPY.fleckGain[0]) * rng()
      : 0;
    // How far the blade rolls about its own axis between base and tip. A grass
    // leaf is not a flat ribbon standing on edge: it twists, which is why a
    // sward catches the sun in flecks rather than as one sheet. Round 1 gave
    // every blade in every tuft the same hand-set normal, and that — far more
    // than the exposure — is why 204,748 near-field pixels resolved into 697
    // colours against a photograph's 4,837.
    const roll = (rng() - 0.5) * 2.3;
    let prev = null;
    for (let s = 0; s <= segments; s++) {
      const t = s / segments;
      const half = wide * Math.max(0, 1 - t ** 1.5);
      // A grass leaf ARCHES: it rises, slows, and its tip falls away. Without
      // the droop term the tuft is a spray of straight straps and reads as a
      // yucca, which is what the first pass looked like.
      const y = len * (t - lean * 0.62 * t * t);
      const out = lean * t * t;
      const cx = dx * out;
      const cz = dz * out;
      // The blade's own frame at this station: tangent along it, width across
      // it, normal off its face — the normal is DERIVED from the arch instead
      // of asserted, so the vertical base of a blade presents a vertical face
      // and its drooping tip presents its face to the sky, which is what puts
      // a 70-degree sun on the top of the sward and nothing on its floor.
      const tx = dx * 2 * lean * t;
      const ty = len * (1 - 1.24 * lean * t);
      const tz = dz * 2 * lean * t;
      let wx = dz;
      let wy = 0;
      let wz = -dx;
      let nx = -dx * ty;
      let ny = dx * tx + dz * tz;
      let nz = -dz * ty;
      const nl = Math.hypot(nx, ny, nz) || 1;
      nx /= nl; ny /= nl; nz /= nl;
      // Roll the (width, normal) pair about the tangent. Both turn together,
      // so the twist is in the GEOMETRY and not a shading trick painted on a
      // flat ribbon.
      const cs = Math.cos(roll * t);
      const sn = Math.sin(roll * t);
      const wx2 = wx * cs + nx * sn;
      const wy2 = wy * cs + ny * sn;
      const wz2 = wz * cs + nz * sn;
      const nx2 = nx * cs - wx * sn;
      const ny2 = ny * cs - wy * sn;
      const nz2 = nz * cs - wz * sn;
      wx = wx2; wy = wy2; wz = wz2;
      const px = wx * half;
      const py = wy * half;
      const pz = wz * half;
      // 0.92 is the tallest blade's own top: `len` runs to 1.0 and the droop
      // takes about eight per cent off it, so a culm tip lands at the sward's
      // surface and reads as fully lit.
      const k = shade(Math.min(1, y / 0.92), fleck) * tone;
      const a = vert(g, cx, y, cz, nx2, ny2, nz2, k, k, k, dx, dz, -px, -py, -pz);
      const c = vert(g, cx, y, cz, nx2, ny2, nz2, k, k, k, dx, dz, px, py, pz);
      if (prev) g.idx.push(prev[0], prev[1], a, prev[1], c, a);
      prev = [a, c];
    }
  }
  return finishGeo(g, 'flora-tuft');
}

/**
 * A serrated clump card for the mid field, turned to the camera in the shader.
 * Four columns of different heights, because a rectangle reads as a fence and a
 * flat top edge reads as mown.
 */
function cardGeometry(columns = 7) {
  const g = emptyGeo();
  const rng = rngFrom(0x5a17c001);
  for (let i = 0; i < columns; i++) {
    // Tapered blades with a gap either side. Adjacent columns tile into a
    // rectangle, and a rectangle at 20 m reads as a hoarding however finely
    // its top edge is stepped.
    const cx = -0.5 + (i + 0.5) / columns + (rng() - 0.5) * 0.20;
    // Narrow, with real gaps. A column at 1.15/columns is a 23 cm 'blade' at
    // the card's own width, and at five metres that reads as a pale sail
    // hanging over the sward rather than as a clump of grass.
    const w0 = (0.5 / columns) * (0.34 + rng() * 0.40);
    const top = 0.38 + rng() * 0.62;
    const tip = (rng() - 0.5) * 0.40 * top;
    const k0 = cardShade(0);
    const k1 = cardShade(top) * (0.86 + rng() * 0.30);
    const a = vert(g, cx - w0, 0, 0, 0, 0.90, 0.44, k0, k0, k0, 0, 0);
    const b = vert(g, cx + w0, 0, 0, 0, 0.90, 0.44, k0, k0, k0, 0, 0);
    const c = vert(g, cx + tip - w0 * 0.14, top, 0, 0, 0.90, 0.44, k1, k1, k1, 0, 0);
    const d = vert(g, cx + tip + w0 * 0.14, top, 0, 0, 0.90, 0.44, k1, k1, k1, 0, 0);
    g.idx.push(a, b, c, b, d, c);
  }
  return finishGeo(g, 'flora-card');
}

/** A forb: one stem, four leaves. The flower is a separate archetype. */
function forbGeometry() {
  const g = emptyGeo();
  const rng = rngFrom(0x7c0ffee1);
  const w = 0.012;
  for (const ang of [0, Math.PI / 2]) {
    const dx = Math.sin(ang) * w;
    const dz = Math.cos(ang) * w;
    const k0 = shade(0.15);
    const k1 = shade(0.95);
    const a = vert(g, -dx, 0, -dz, 0, 1, 0, k0, k0, k0, 0, 0);
    const b = vert(g, dx, 0, dz, 0, 1, 0, k0, k0, k0, 0, 0);
    const c = vert(g, -dx, 1, -dz, 0, 1, 0, k1, k1, k1, 0, 0);
    const d = vert(g, dx, 1, dz, 0, 1, 0, k1, k1, k1, 0, 0);
    g.idx.push(a, b, c, b, d, c);
  }
  for (let i = 0; i < 4; i++) {
    const y = 0.22 + i * 0.17;
    const phi = i * 1.9 + rng();
    const dx = Math.sin(phi);
    const dz = Math.cos(phi);
    // Broad leaves: a mid-July near field is as much milkweed and bergamot
    // foliage as grass, and a forb drawn as a wire with four slivers on it
    // vanishes into the sward instead of breaking it up.
    const len = 0.42 - i * 0.055;
    const half = 0.150 - i * 0.020;
    const k0 = shade(y * 0.8);
    const k1 = shade(Math.min(1, y + 0.2));
    const a = vert(g, -dz * half, y, dx * half, dx * 0.3, 0.9, dz * 0.3, k0, k0, k0, dx, dz);
    const b = vert(g, dz * half, y, -dx * half, dx * 0.3, 0.9, dz * 0.3, k0, k0, k0, dx, dz);
    const c = vert(g, dx * len, y + len * 0.30, dz * len,
      dx * 0.3, 0.9, dz * 0.3, k1, k1, k1, dx, dz);
    g.idx.push(a, b, c);
    const d = vert(g, -dx * len * 0.55, y + len * 0.22, -dz * len * 0.55,
      -dx * 0.3, 0.9, -dz * 0.3, k1, k1, k1, -dx, -dz);
    g.idx.push(b, a, d);
  }
  return finishGeo(g, 'flora-forb');
}

/* --- the nine flower archetypes, one per row of HEAD_OF_SHAPE ------------- */
/*
 * All nine are built in a NOMINAL unit box: one across and one tall, centred on
 * the attachment point at y = 0, so the record's `inflorescence.size_m` scales
 * a Liatris spike to 30 cm and a Dalea thimble to 3 cm through the same two
 * numbers. Each carries a PEDUNCLE below the head, proportioned to it, because
 * a flower that ends where its stalk should begin is the floating sprite the
 * critic caught in the sky. And each is drawn about the vertical: the tilt is
 * per instance, on the instance matrix, so no two heads of a species present
 * the same face and none of them is ever exactly edge-on.
 */

/**
 * How far below its own head each archetype's stalk reaches, in units of the
 * head's size. It is a module constant and not a local because `maybeHead` has
 * to know it: a head is only ever offset from the plant's stem by as far as its
 * own stalk can lean back to reach it. Without that the branched inflorescences
 * came out as lollipops hanging in the air beside the scape — the same
 * unattached-flower failure the critic caught, one level down.
 */
const PEDUNCLE = {
  spike: 1.6,
  spire: 1.2,
  panicle: 1.4,
  ray: 2.2,
  raydroop: 2.2,
  pompom: 2.2,
  dome: 2.0,
  corymb: 2.2,
  compound: 2.0,
};

/** A thin stalk from the attachment point down, in the archetype's own units. */
function peduncle(g, drop = 1.5, wide = 0.022, k = 0.42) {
  for (let i = 0; i < 2; i++) {
    const a = (i / 2) * Math.PI;
    const dx = Math.sin(a) * wide;
    const dz = Math.cos(a) * wide;
    const p0 = vert(g, -dx, -drop, -dz, dx, 0.4, dz, k, k, k, 0, 0);
    const p1 = vert(g, dx, -drop, dz, dx, 0.4, dz, k, k, k, 0, 0);
    const p2 = vert(g, -dx, 0, -dz, dx, 0.4, dz, k * 1.5, k * 1.5, k * 1.5, 0, 0);
    const p3 = vert(g, dx, 0, dz, dx, 0.4, dz, k * 1.5, k * 1.5, k * 1.5, 0, 0);
    g.idx.push(p0, p1, p2, p1, p3, p2);
  }
}

/** A dense column: Liatris's button spike, Physostegia, Amorpha, the cattail's
 *  brown spadix, Spiraea's conical panicle. A WAND, not a cone — a cordgrass
 *  spike is millimetres across on a culm a quarter-metre long. */
function spikeGeometry() {
  const g = emptyGeo();
  for (let i = 0; i < 3; i++) {
    const a = (i / 3) * Math.PI;
    // A WAND. Round 1's comment about a field of pale traffic cones was right
    // and this stays narrow: the whole one-sided cordgrass inflorescence is two
    // or three centimetres across on a spike a quarter-metre long.
    const dx = Math.sin(a) * 0.062;
    const dz = Math.cos(a) * 0.062;
    // Florets open from the top down, so a spike is paler at its shoulder.
    const p0 = vert(g, -dx * 0.55, -0.48, -dz * 0.55, dx, 0.2, dz, 0.72, 0.72, 0.72, 0, 0);
    const p1 = vert(g, dx * 0.55, -0.48, dz * 0.55, dx, 0.2, dz, 0.72, 0.72, 0.72, 0, 0);
    const p2 = vert(g, -dx, 0.06, -dz, dx, 0.2, dz, 1.10, 1.10, 1.10, 0, 0);
    const p3 = vert(g, dx, 0.06, dz, dx, 0.2, dz, 1.10, 1.10, 1.10, 0, 0);
    const p4 = vert(g, 0, 0.50, 0, dx, 0.5, dz, 1.22, 1.22, 1.22, 0, 0);
    g.idx.push(p0, p1, p2, p1, p3, p2, p2, p3, p4);
  }
  peduncle(g, PEDUNCLE.spike, 0.016);
  return finishGeo(g, 'flora-head-spike');
}

/**
 * Culver's root: a terminal spire with two to four lateral spires off its
 * shoulder, which is the candelabra the vocabulary names and the plant's whole
 * silhouette. Drawn as the same mesh as a Liatris button it scored under ten
 * pixels and was indistinguishable from it.
 */
function spireGeometry() {
  const g = emptyGeo();
  const wand = (cx, cz, base, top, wide, k) => {
    for (let i = 0; i < 2; i++) {
      const a = (i / 2) * Math.PI;
      const dx = Math.sin(a) * wide;
      const dz = Math.cos(a) * wide;
      const p0 = vert(g, cx - dx, base, cz - dz, dx, 0.2, dz, k * 0.72, k * 0.72, k * 0.72, 0, 0);
      const p1 = vert(g, cx + dx, base, cz + dz, dx, 0.2, dz, k * 0.72, k * 0.72, k * 0.72, 0, 0);
      const p2 = vert(g, cx - dx, top - 0.12, cz - dz, dx, 0.2, dz, k, k, k, 0, 0);
      const p3 = vert(g, cx + dx, top - 0.12, cz + dz, dx, 0.2, dz, k, k, k, 0, 0);
      const p4 = vert(g, cx, top, cz, dx, 0.5, dz, k * 1.15, k * 1.15, k * 1.15, 0, 0);
      g.idx.push(p0, p1, p2, p1, p3, p2, p2, p3, p4);
    }
  };
  wand(0, 0, -0.34, 0.50, 0.055, 1.06);
  for (let i = 0; i < 4; i++) {
    // The laterals spread about a third of the terminal spire's own length —
    // narrower than that and the candelabra collapses back into the single
    // wand it is supposed to be distinguishable from.
    const a = (i / 4) * Math.PI * 2 + 0.4;
    const r = 0.30 + (i % 2) * 0.10;
    wand(Math.sin(a) * r, Math.cos(a) * r, -0.40, 0.24 + (i % 2) * 0.16, 0.046, 0.94);
  }
  peduncle(g, PEDUNCLE.spire, 0.020);
  return finishGeo(g, 'flora-head-spire');
}

/** Bluejoint, wild rice, wood nettle: an OPEN panicle — a diffuse airy cloud
 *  of fine branches, which is nothing like a wand and is why the wet prairie's
 *  second grass read as a second cordgrass. */
function panicleGeometry() {
  const g = emptyGeo();
  const rng = rngFrom(0x9a11c1e0);
  for (let i = 0; i < 7; i++) {
    const a = rng() * Math.PI * 2;
    const t = rng();
    const y0 = -0.42 + t * 0.55;
    const len = 0.20 + rng() * 0.28;
    const dx = Math.sin(a);
    const dz = Math.cos(a);
    const w = 0.012;
    const k0 = 0.70;
    const k1 = 1.16;
    const p0 = vert(g, -dz * w, y0, dx * w, dx * 0.5, 0.7, dz * 0.5, k0, k0, k0, 0, 0);
    const p1 = vert(g, dz * w, y0, -dx * w, dx * 0.5, 0.7, dz * 0.5, k0, k0, k0, 0, 0);
    const p2 = vert(g, dx * len * 0.5, y0 + len * 0.62, dz * len * 0.5,
      dx * 0.5, 0.7, dz * 0.5, k1, k1, k1, 0, 0);
    g.idx.push(p0, p1, p2);
  }
  peduncle(g, PEDUNCLE.panicle, 0.014);
  return finishGeo(g, 'flora-head-panicle');
}

/**
 * A composite head. `droop` swings the rays DOWN around a raised central cone
 * — Ratibida and Echinacea — while the flat form is Rudbeckia, Heliopsis and
 * the Silphiums. Two shapes, one builder, because the difference between them
 * is exactly one sign and the vocabulary distinguishes them.
 */
function rayGeometry(droop) {
  const g = emptyGeo();
  // Enough rays that they OVERLAP into a disc with a toothed rim. Nine spokes
  // radiating off a small centre reads as a spider, not a flower, and at nine
  // centimetres on a prairie-dock scape it was a yellow star in the sky.
  const rays = 14;
  const coneY = droop ? 0.20 : 0.09;
  const tipY = droop ? -0.24 : 0.015;
  const disc = [];
  const rim = droop ? 0.30 : 0.34;
  const c0 = vert(g, 0, coneY, 0, 0, 1, 0, 0.55, 0.55, 0.55, 0, 0);
  for (let i = 0; i < rays; i++) {
    const a = (i / rays) * Math.PI * 2;
    disc.push(vert(g, Math.sin(a) * rim, coneY * 0.35, Math.cos(a) * rim,
      Math.sin(a) * 0.5, 0.86, Math.cos(a) * 0.5, 0.74, 0.74, 0.74, 0, 0));
  }
  for (let i = 0; i < rays; i++) g.idx.push(c0, disc[i], disc[(i + 1) % rays]);
  for (let i = 0; i < rays; i++) {
    // Each ray is a broad petal spanning two rim points and reaching past its
    // neighbours, so the outline closes.
    const a = ((i + 0.5) / rays) * Math.PI * 2;
    const dx = Math.sin(a);
    const dz = Math.cos(a);
    const nx = droop ? dx * 0.45 : dx * 0.16;
    const nz = droop ? dz * 0.45 : dz * 0.16;
    const b = disc[i];
    const c = disc[(i + 1) % rays];
    const d = vert(g, dx * 0.50, tipY, dz * 0.50, nx, 0.90, nz, 1.18, 1.18, 1.18, 0, 0);
    g.idx.push(b, c, d);
  }
  peduncle(g, droop ? PEDUNCLE.raydroop : PEDUNCLE.ray, 0.020);
  return finishGeo(g, droop ? 'flora-head-raydroop' : 'flora-head-ray');
}

/** Monarda, Dalea, a rattlesnake-master globe, a hazel husk, a dogwood berry
 *  cluster: a small dense ball on the stem tip. */
function pompomGeometry() {
  const g = emptyGeo();
  for (let i = 0; i < 3; i++) {
    const phi = (i / 3) * Math.PI;
    const dx = Math.sin(phi) * 0.5;
    const dz = Math.cos(phi) * 0.5;
    const nx = Math.cos(phi);
    const nz = -Math.sin(phi);
    const a = vert(g, -dx, -0.30, -dz, nx, 0.5, nz, 0.72, 0.72, 0.72, 0, 0);
    const b = vert(g, dx, -0.30, dz, nx, 0.5, nz, 0.72, 0.72, 0.72, 0, 0);
    const c = vert(g, -dx, 0.34, -dz, nx, 0.5, nz, 1.14, 1.14, 1.14, 0, 0);
    const d = vert(g, dx, 0.34, dz, nx, 0.5, nz, 1.14, 1.14, 1.14, 0, 0);
    g.idx.push(a, b, c, b, d, c);
  }
  peduncle(g, PEDUNCLE.pompom, 0.030);
  return finishGeo(g, 'flora-head-pompom');
}

/**
 * A DOMED umbel — swamp milkweed, common milkweed, a nodding onion. A
 * hemisphere of florets, and emphatically not the flat horizontal plate that
 * used to stand in for it: at 1.68 m eye height a head at 0.6-0.9 m is seen
 * about eleven degrees above the horizontal, so a plate presented its EDGE and
 * a seven-centimetre umbel came out three pixels wide at five metres.
 */
function domeGeometry() {
  const g = emptyGeo();
  const rings = 2;
  const seg = 7;
  const grid = [];
  for (let r = 0; r <= rings; r++) {
    const row = [];
    const th = (r / rings) * (Math.PI / 2);
    const rr = Math.sin(th) * 0.5;
    const yy = Math.cos(th) * 0.40;
    const k = 1.20 - 0.42 * (r / rings);
    for (let s = 0; s < seg; s++) {
      const a = (s / seg) * Math.PI * 2;
      const dx = Math.sin(a);
      const dz = Math.cos(a);
      row.push(vert(g, dx * rr, yy - 0.08, dz * rr,
        dx * Math.sin(th), Math.cos(th) + 0.15, dz * Math.sin(th), k, k, k, 0, 0));
    }
    grid.push(row);
  }
  for (let r = 0; r < rings; r++) {
    for (let s = 0; s < seg; s++) {
      const s1 = (s + 1) % seg;
      g.idx.push(grid[r][s], grid[r + 1][s], grid[r][s1],
        grid[r][s1], grid[r + 1][s], grid[r + 1][s1]);
    }
  }
  peduncle(g, PEDUNCLE.dome, 0.024);
  return finishGeo(g, 'flora-head-dome');
}

/**
 * A flat-topped corymb — ironweed, mountain mint, wild quinine, butterfly
 * weed. Still a disc, because that is what the plant is, but built with a
 * standing TILT so it is never read edge-on, and given a shallow crown so it
 * has a silhouette from the side as well as a face from above. The rest of the
 * tilt is per instance, on the instance matrix.
 */
function corymbGeometry() {
  const g = emptyGeo();
  const seg = 9;
  const ring = [];
  const c0 = vert(g, 0, 0.13, 0, 0, 1, 0, 1.22, 1.22, 1.22, 0, 0);
  for (let i = 0; i < seg; i++) {
    const a = (i / seg) * Math.PI * 2;
    const dx = Math.sin(a);
    const dz = Math.cos(a);
    // A corymb is a cluster of heads, not a wheel: the rim is uneven.
    const rr = 0.42 + 0.08 * Math.sin(a * 3.0 + 1.1);
    ring.push(vert(g, dx * rr, 0.02 + 0.03 * Math.sin(a * 2.0), dz * rr,
      dx * 0.30, 0.94, dz * 0.30, 0.90, 0.90, 0.90, 0, 0));
  }
  for (let i = 0; i < seg; i++) g.idx.push(c0, ring[i], ring[(i + 1) % seg]);
  // The under-side, so the disc has a body when it is seen from below.
  const u0 = vert(g, 0, -0.09, 0, 0, -1, 0, 0.58, 0.58, 0.58, 0, 0);
  for (let i = 0; i < seg; i++) g.idx.push(u0, ring[(i + 1) % seg], ring[i]);
  peduncle(g, PEDUNCLE.corymb, 0.020);
  return finishGeo(g, 'flora-head-corymb');
}

/** A COMPOUND umbel — water hemlock, golden alexanders, sweet cicely: several
 *  small domed umbellets on rays from one point, which is the architecture
 *  that reads as an umbellifer and nothing else does. */
function compoundGeometry() {
  const g = emptyGeo();
  const umbellets = 5;
  const seg = 4;
  for (let u = 0; u <= umbellets; u++) {
    const a = ((u - 1) / umbellets) * Math.PI * 2 + 0.3;
    const cx = u === 0 ? 0 : Math.sin(a) * 0.38;
    const cz = u === 0 ? 0 : Math.cos(a) * 0.38;
    const cy = u === 0 ? 0.16 : 0.02 + 0.05 * Math.sin(a * 2.0);
    const rr = u === 0 ? 0.15 : 0.13;
    const c0 = vert(g, cx, cy + 0.05, cz, 0, 1, 0, 1.20, 1.20, 1.20, 0, 0);
    const ring = [];
    for (let i = 0; i < seg; i++) {
      const b = (i / seg) * Math.PI * 2;
      ring.push(vert(g, cx + Math.sin(b) * rr, cy, cz + Math.cos(b) * rr,
        Math.sin(b) * 0.4, 0.9, Math.cos(b) * 0.4, 0.86, 0.86, 0.86, 0, 0));
    }
    for (let i = 0; i < seg; i++) g.idx.push(c0, ring[i], ring[(i + 1) % seg]);
    // The ray that carries it back to the centre.
    if (u > 0) {
      const w = 0.010;
      const p0 = vert(g, cx - Math.cos(a) * w, cy - 0.01, cz + Math.sin(a) * w,
        0, 1, 0, 0.50, 0.50, 0.50, 0, 0);
      const p1 = vert(g, cx + Math.cos(a) * w, cy - 0.01, cz - Math.sin(a) * w,
        0, 1, 0, 0.50, 0.50, 0.50, 0, 0);
      const p2 = vert(g, 0, -0.14, 0, 0, 1, 0, 0.44, 0.44, 0.44, 0, 0);
      g.idx.push(p0, p1, p2);
    }
  }
  peduncle(g, PEDUNCLE.compound, 0.022);
  return finishGeo(g, 'flora-head-compound');
}

/**
 * A basal-scape plant: prairie dock, compass plant, wild iris, plantain. A
 * ROSETTE of big paddle leaves lying at the ground and a nearly naked scape
 * over it — the dossier names prairie dock's 40 cm basal rosette explicitly,
 * and it is the plant's whole diagnosis. Drawn with the generic forb it became
 * a three-metre leafy stalk with sixty-centimetre leaves halfway up it, which
 * is the giant the timber critic handed back from the foreground.
 *
 * The rosette is scaled by the instance's SPREAD, which `placeForb` takes from
 * the record's own `width_m`, so the leaves are the recorded size of the
 * rosette and do not grow with the flowering scape above them.
 */
function rosetteGeometry() {
  const g = emptyGeo();
  const rng = rngFrom(0x51190010);
  // The scape: bare, thin, and the full height of the plant.
  for (const ang of [0.3, 0.3 + Math.PI / 2]) {
    const dx = Math.sin(ang) * 0.010;
    const dz = Math.cos(ang) * 0.010;
    const k0 = shade(0.10);
    const k1 = shade(0.98);
    const a = vert(g, -dx, 0, -dz, dz, 0.3, -dx, k0, k0, k0, 0, 0);
    const b = vert(g, dx, 0, dz, dz, 0.3, -dx, k0, k0, k0, 0, 0);
    const c = vert(g, -dx, 1, -dz, dz, 0.3, -dx, k1, k1, k1, 0, 0);
    const d = vert(g, dx, 1, dz, dz, 0.3, -dx, k1, k1, k1, 0, 0);
    g.idx.push(a, b, c, b, d, c);
  }
  // Five huge paddle leaves, rising out of the crown and arching back down.
  // Their SPAN is in the archetype's own units and is scaled by the rosette's
  // recorded radius; their rise is a small fraction of the plant's height, so a
  // 40 cm prairie-dock rosette stands about 15 cm proud of the ground while a
  // plantain's lies flat, which is what both plants do.
  for (let i = 0; i < 5; i++) {
    const phi = (i / 5) * Math.PI * 2 + rng() * 0.7;
    const dx = Math.sin(phi);
    const dz = Math.cos(phi);
    const len = 0.80 + rng() * 0.20;
    const wide = 0.30 + rng() * 0.12;
    const rise = 0.050 + rng() * 0.026;
    const k0 = shade(0.14);
    const k1 = shade(0.34 + rng() * 0.12);
    const k2 = shade(0.22);
    const nx = -dx * 0.30;
    const nz = -dz * 0.30;
    const a = vert(g, dx * 0.06, 0.004, dz * 0.06, nx, 0.95, nz, k0, k0, k0, 0, 0);
    const b = vert(g, dx * len * 0.45 - dz * wide, rise, dz * len * 0.45 + dx * wide,
      nx, 0.95, nz, k1, k1, k1, 0, 0);
    const c = vert(g, dx * len * 0.45 + dz * wide, rise, dz * len * 0.45 - dx * wide,
      nx, 0.95, nz, k1, k1, k1, 0, 0);
    const d = vert(g, dx * len, rise * 0.42, dz * len, nx, 0.95, nz, k2, k2, k2, 0, 0);
    g.idx.push(a, b, c, b, d, c);
  }
  return finishGeo(g, 'flora-rosette');
}

/** Smooth value noise, 0..1. No texture, no table. */
function vnoise(x, z) {
  const xi = Math.floor(x);
  const zi = Math.floor(z);
  const fx = x - xi;
  const fz = z - zi;
  const sx = fx * fx * (3 - 2 * fx);
  const sz = fz * fz * (3 - 2 * fz);
  const h = (a, b) => (hash3(a, b, 0x2f1c) & 0xffff) / 65535;
  const a0 = h(xi, zi) * (1 - sx) + h(xi + 1, zi) * sx;
  const a1 = h(xi, zi + 1) * (1 - sx) + h(xi + 1, zi + 1) * sx;
  return a0 * (1 - sz) + a1 * sz;
}

/* -------------------------------------------------------------------------- */
/* materials                                                                   */
/* -------------------------------------------------------------------------- */

/**
 * One material family for every plant: Lambert, vertex colours, double sided,
 * per-instance transform and wind in the vertex shader. The instance matrix
 * carries the POSITION ONLY; yaw, height, spread and arch arrive in `aFlora`,
 * which is what lets one canonical tuft be six species at six heights in one
 * draw call, and keeps the wind in world space — a rotation baked into the
 * instance matrix would have silently turned it per plant.
 */
function plantMaterial({ uniforms, billboard = false, membrane = 1.0 }) {
  const mat = new THREE.MeshLambertMaterial({
    color: 0xffffff,
    vertexColors: true,
    side: THREE.DoubleSide,
  });
  const prior = mat.onBeforeCompile;
  mat.onBeforeCompile = (shader, renderer) => {
    if (typeof prior === 'function') prior(shader, renderer);
    Object.assign(shader.uniforms, {
      uChiTime: uniforms.uChiTime,
      uChiWind: uniforms.uChiWind,
      uChiSway: uniforms.uChiSway,
      uChiWaveK: uniforms.uChiWaveK,
    });
    Object.assign(shader.uniforms, {
      uChiSun: uniforms.uChiSun,
      uChiSunCol: uniforms.uChiSunCol,
      uChiSky: uniforms.uChiSky,
    });
    shader.vertexShader = `
attribute vec2 aDir;
attribute vec3 aSide;       // offset from the archetype's axis, in real metres
attribute vec4 aFlora;      // height, spread, arch, yaw
attribute vec4 aChiRing;    // fade ring: outer, band, inner, innerBand
attribute float aChiRise;   // metres this origin stands over its plant's base
uniform float uChiTime;
uniform vec2  uChiWind;
uniform float uChiSway;
uniform float uChiWaveK;
varying vec3 vChiNW;        // world normal, unflipped
varying vec3 vChiPW;        // world position
varying float vChiLit;      // how much of the sky this point can see, 0..1.6
` + shader.vertexShader
      .replace('#include <beginnormal_vertex>', /* glsl */`
#include <beginnormal_vertex>
{
  float cy = cos(aFlora.w), sy = sin(aFlora.w);
  objectNormal.xz = vec2(objectNormal.x * cy + objectNormal.z * sy,
                        -objectNormal.x * sy + objectNormal.z * cy);
}
`)
      .replace('#include <begin_vertex>', /* glsl */`
#include <begin_vertex>
float chiDrop = 0.0;
{
  vec3 chiInst = vec3(instanceMatrix[3][0], instanceMatrix[3][1], instanceMatrix[3][2]);
  float chiT = clamp(transformed.y, 0.0, 1.0);
  // The ring fade, measured from where the camera IS this frame. It used to be
  // baked into the height on the CPU, where it could only change when the
  // lattice was rebuilt — every 1.2 m walked, against a 2.2 m band, so a plant
  // came up out of the ground to 55% of its height between one frame and the
  // next. Here it is continuous, and the lattice is inset from it by the
  // rebuild step (see \`ringsFor\`) so nothing is ever drawn before it is placed.
  float chiD = distance(cameraPosition.xz, chiInst.xz);
  float chiFade = clamp((aChiRing.x - chiD) / max(aChiRing.y, 1e-4), 0.0, 1.0);
  if (aChiRing.w > 0.0) chiFade *= clamp((chiD - aChiRing.z) / aChiRing.w, 0.0, 1.0);
  // A flower head's origin is up the stem, so shrinking it in place would leave
  // it hanging over its own plant. It descends to the base at the same rate.
  chiDrop = aChiRise * (1.0 - chiFade);
  // Arch each blade outward along its own azimuth, in nominal space.
  transformed.xz += aDir * (aFlora.z * chiT * chiT);
  // Scale: height from the record, spread from the archetype's own proportions.
  transformed.y *= aFlora.x;
  transformed.xz *= aFlora.y;
  transformed += aSide;
  // ...and then the whole plant, uniformly, about its own base. Uniform because
  // a plant that grows in is a plant, and one that only gets taller is a stretch.
  transformed *= chiFade;
  ${billboard ? /* glsl */`
  // Turn the card to the camera about Y. Nothing else uses the yaw slot here.
  vec2 chiToCam = cameraPosition.xz - chiInst.xz;
  float chiLen = length(chiToCam);
  vec2 chiF = chiLen > 0.001 ? chiToCam / chiLen : vec2(0.0, 1.0);
  transformed.xz = vec2(transformed.x * chiF.y + transformed.z * chiF.x,
                       -transformed.x * chiF.x + transformed.z * chiF.y);
  objectNormal.xz = vec2(objectNormal.x * chiF.y + objectNormal.z * chiF.x,
                        -objectNormal.x * chiF.x + objectNormal.z * chiF.y);
  ` : /* glsl */`
  float chiCy = cos(aFlora.w), chiSy = sin(aFlora.w);
  transformed.xz = vec2(transformed.x * chiCy + transformed.z * chiSy,
                       -transformed.x * chiSy + transformed.z * chiCy);
  `}
  ${/* glsl */`
  // Wind, in world space, after the plant has been turned: a travelling wave
  // across the field plus a slow gust, both fixed at the base and free at the
  // tip. This is the "wind-combed" reading the sources give the wet prairie.
  float chiPh = dot(chiInst.xz, uChiWind) * uChiWaveK + uChiTime;
  float chiGust = 0.62 + 0.38 * sin(chiPh * 0.31 + 1.7);
  transformed.xz += uChiWind
    * (uChiSway * chiGust * sin(chiPh) * chiT * chiT * aFlora.x * chiFade);
  `}
  // The world-space frame the sun terms need, built HERE rather than read off
  // three's vNormal: <defaultnormal_vertex> has already run by this point, so
  // three's normal never sees the billboard turn above, and the instance
  // matrix carries a real rotation for the tilted flower heads.
  vChiNW = normalize(mat3(modelMatrix) * mat3(instanceMatrix) * objectNormal);
  vChiPW = (modelMatrix * instanceMatrix * vec4(transformed, 1.0)).xyz;
  vChiPW.y -= chiDrop;
  // The archetype's own base-to-tip ramp, BEFORE the species colour multiplies
  // it. It is the one occlusion term this module has — how deep in the clump
  // this point sits — and it has to gate every light path, not just the
  // reflected one: a transmission term that ignores it puts the same glow on
  // the floor of the sward as on the blade tips, and a sward with no floor is
  // as wrong as one with no sun (measured: median 56 -> 148, nothing under 20).
  vChiLit = color.g;
}
`)
      // `chiDrop` is a WORLD-space descent of the instance's origin, and the
      // instance matrix carries a real rotation for the tilted heads, so it
      // cannot be folded into `transformed` — it goes on after the instance
      // transform and before the view matrix.
      .replace('#include <project_vertex>', /* glsl */`
vec4 mvPosition = vec4(transformed, 1.0);
#ifdef USE_INSTANCING
  mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition.y -= chiDrop;
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;
`);
    // The fake sunward normal that used to live at <normal_fragment_begin> —
    // `normal.y = abs(normal.y)` — is GONE. It was standing in for exactly the
    // transmission this block now models, and while it stopped back faces going
    // black it also meant nothing in the sward was ever properly lit or
    // properly shaded: every fragment got the same middling wash, which is the
    // truncated distribution the structure critic measured (p99 132, not one
    // pixel over 230). Three's own double-sided flip is left to do its job, so
    // dot(N, L) is now a real two-sided term.
    shader.fragmentShader = `
uniform vec3 uChiSun;
uniform vec3 uChiSunCol;
uniform vec3 uChiSky;
varying vec3 vChiNW;
varying vec3 vChiPW;
varying float vChiLit;
` + shader.fragmentShader.replace('#include <opaque_fragment>', /* glsl */`
{
  // The face we can see, whichever side of the sheet it is.
  vec3 chiN = normalize(vChiNW) * (gl_FrontFacing ? 1.0 : -1.0);
  vec3 chiV = normalize(cameraPosition - vChiPW);
  float chiNL = dot(chiN, uChiSun);

  // What the leaf lets through. Keyed on the NEGATIVE half of the same N.L
  // three used for the reflection, so a blade is lit on one side and glowing
  // on the other and never both. The lobe is a (0.5 + 0.5 cos) remap rather
  // than a raw cos^n: at 70 degrees the July sun is overhead, not behind the
  // subject, and a hard forward lobe would never fire at eye height.
  float chiFwd = pow(clamp(dot(chiV, -uChiSun) * 0.5 + 0.5, 0.0, 1.0), ${f(LEAF.forward)});
  // What comes THROUGH is the leaf's own hue at the leaf's own transmittance —
  // not its albedo, which is what caps a reflective model — gated by how much
  // of the sky this point in the clump can see.
  vec3 chiHue = diffuseColor.rgb
    / max(max(diffuseColor.r, diffuseColor.g), max(diffuseColor.b, 1e-4));
  // SQUARED, and that is the whole difference between a sward with a sun in it
  // and a sward painted lime. A linear gate spread the glow evenly over every
  // blade from floor to tip and lifted the median from 56 to 148 while the
  // photographs sit at 72 and 93; squared, the floor of a clump keeps a
  // hundredth of it and the exposed tips keep more than all of it, which is
  // what a canopy actually does to light on its way down.
  // ...and by how much of this fragment is one leaf rather than a stand-in for
  // many. A mid-field CARD is already an average of lit blades and shaded
  // interior, so giving it a whole leaf's transmission bleached the middle
  // distance into a field of pale spikes brighter than the near ground — a
  // clump at twenty metres is a dark green mass in every one of the bar
  // photographs.
  float chiOpen = pow(clamp(vChiLit, 0.0, 2.30), 2.0) * ${f(membrane)};
  vec3 chiFilter = chiHue
    * vec3(${f(LEAF.tint[0])}, ${f(LEAF.tint[1])}, ${f(LEAF.tint[2])}) * chiOpen;
  vec3 chiExtra = uChiSunCol * (
      ${f(LEAF.transmit)} * max(-chiNL, 0.0) * (0.42 + 0.58 * chiFwd)   // through it
    + ${f(LEAF.scatter)} * max(chiNL, 0.0)                              // and around it
  ) * chiFilter;
  chiExtra += uChiSky * (${f(LEAF.skyTransmit)} * chiFilter);

  // The cuticle: a waxy film over the leaf, so a narrow lobe at a dielectric
  // F0 with the Fresnel edge that makes a grazing blade flare.
  vec3 chiH = normalize(uChiSun + chiV);
  float chiSpec = pow(max(dot(chiN, chiH), 0.0), ${f(LEAF.gloss)});
  float chiF = ${f(LEAF.f0)} + ${f(1 - LEAF.f0)}
    * pow(1.0 - clamp(dot(chiV, chiH), 0.0, 1.0), 5.0);
  chiExtra += uChiSunCol
    * (chiSpec * chiF * ${f(LEAF.specular)} * step(0.0, chiNL) * chiOpen);

  outgoingLight += chiExtra;
}
#include <opaque_fragment>
`);
  };
  mat.needsUpdate = true;
  return mat;
}

/** A float that always carries a decimal point, because GLSL will not take
 *  `0` where it wants a float and a template literal will happily write one. */
function f(v) {
  return Number.isInteger(v) ? `${v}.0` : String(v);
}
