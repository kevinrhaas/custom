/**
 * trees.js — every woody plant taller than three metres, and the timber on the
 * horizon.
 *
 * Parcel `timber-edge`. It draws the two things the sward cannot:
 *
 *   1. **The near timber inside the 640 m box** — the riverbank gallery forest,
 *      the body of timber on the North Division, the sand-ridge oak stringers
 *      threading it, and the sandbar-willow thickets on the point bars.
 *   2. **The timber on the horizon** — the bodies the sources put BEYOND the
 *      modelled ground, drawn as a silhouette band at their true bearing,
 *      angular height and atmospheric contrast.
 *
 * `docs/research/02-flora.md` is the authority: § 1.4, § 1.5 (what the "Dense
 * Forest" north-east of the forks actually was), § 1.6 (the named groves), and
 * ZONE 5, ZONE 6, ZONE 7.
 *
 * The four rules this file is built to obey
 * -----------------------------------------
 *
 * **The plain was OPEN.** Andreas: *"The West Side was an open prairie, entirely
 * free from timber, except for a grove up the South Branch."* The West Division
 * therefore carries NO woody vegetation at all — no gallery, no thicket, not a
 * scattered oak. A treeline in the wrong place is a bigger error than an empty
 * horizon.
 *
 * **The timber was THIN.** § 0: across all PLS corners, 39% of the landscape was
 * open savanna (0–10 trees/ha) and 31% closed savanna (10–50/ha); even ground
 * the surveyors called *timber* was 64% savanna-density, and most bearing trees
 * were 12 inches dbh. Nothing here is a closed eastern hardwood forest: the mean
 * canopy tree is ~30 cm dbh and 15–20 m, and the crowns are open-grown.
 *
 * **Fire made the pattern.** McBride & Bowles found density and fire-intolerant
 * species concentrated on the EAST sides of watercourses, which broke prairie
 * fire running west to east. So the timber sits on the north and east banks and
 * the west banks stay prairie — independently what Andreas describes.
 *
 * **It is July.** Full summer canopy on every woody plant, no autumn colour. The
 * woodland floor (wood nettle, ferns, leaf litter — not spring ephemerals)
 * belongs to `flora.js`, which draws everything at or below 3 m.
 *
 * Why the horizon band computes its own haze
 * ------------------------------------------
 * The band is drawn on a ring at a fixed radius, so the scene's fog — which
 * works on distance to the geometry — would haze a grove four miles out exactly
 * as hard as a treeline at eleven hundred metres. It therefore runs `world.js`'s
 * own haze law by hand against each body's REAL distance, with `fog: false` so
 * the scene does not apply it twice, and one departure: a cap, because the
 * scene's haze is deliberately total by 1500 m and the dossier's horizon timber
 * is at three to six miles. See HAZE_MAX, and docs/LIBERTIES.md **L35**, which
 * records the cap as the liberty it is.
 *
 * What is deliberately NOT drawn
 * ------------------------------
 * The Big Woods of north-east Cook, Blue Island, La Framboise Woods and Cottage
 * Grove are all in § 1.6 and all are omitted: at 6 to 14 miles a 60-foot tree on
 * a flat lake plain stands less than a tenth of a degree above a standing eye's
 * horizon — under two pixels, below the contrast threshold, and in two cases
 * below the horizon entirely. `stats.omitted` carries the arithmetic so a critic
 * can check it. Drawing them would be prettier and would be a lie about how far
 * you can see from a flat plain.
 *
 * Where the numbers come from
 * ---------------------------
 * Species, July height, crown width, July foliage colour and confidence are
 * READ FROM `data/flora/zones/*.json` (roles `tree` and `thicket`) through the
 * manifest, per the CONTRACT: the dataset is the durable artifact and a renderer
 * with its own copy of the ecology drifts from it. What stays here is what the
 * records do not carry — the draw archetype per form, and WHERE a tree stands.
 * Zone extents describe ground communities; a tree's position is a question
 * about banks, ridges, fire and which side of the river the town was cutting,
 * answered from the heightfield. The tables below are render parameters and the
 * fallback for a species the records do not describe.
 */

import * as THREE from 'three';

/**
 * The zone records this module reads, by the CONTRACT's `z<NN>_<slug>` id. Only
 * these are opened, and only through the path the manifest gives: the repo smoke
 * fails on any HTTP >= 400, so nothing here may probe for a file.
 */
const TIMBER_ZONES = [
  'z05_riverbank_timber', 'z06_dense_forest', 'z07_bur_oak_savanna', 'z10_settled_town',
];

/* -------------------------------------------------------------------------- */
/* the physical constants this file reasons with                               */
/* -------------------------------------------------------------------------- */

/** Below this the heightfield is under water (same value terrain.js uses). */
const SHORE_Y = -0.10;
/**
 * How far ABOVE the water surface a stem's root has to stand.
 *
 * `terrain.isWater()` — the mask the gallery, the divisions and the release
 * smoke are all built on — asks whether the heightfield is below SHORE_Y, which
 * is 100 mm BELOW the water plane. It is the right question for "is this the
 * river", and it was the wrong question for "may a tree stand here": the water
 * surface is Z = 0 and the ground is drawn under it, so a stem rooted anywhere
 * in the 100 mm band between SHORE_Y and the datum passes the mask and then
 * renders standing in open water with its foot invisible. Thirty-six of the
 * scene's 618 stations were in that band, and because a gallery-edge willow may
 * stand at bank distance zero they were exactly the ones nearest the camera
 * across the channel. The fort views show timber ALONG the river and never in
 * it — see the module header and docs/research/02-flora.md ZONE 5.
 *
 * 0.20 m, and the number is the geometry rather than a taste: `addTree` sinks a
 * bole 0.15 m below its ground point so no trunk floats on uneven cells, and the
 * baked ground mesh is allowed to depart from the heightfield the placement
 * samples by up to 0.03 m (`generators/terrain_gen.py` MESH_FIT_TOLERANCE_M).
 * 0.15 + 0.03 puts the deepest modelled bark exactly at the water plane, so
 * 0.20 leaves 20 mm of daylight under the worst case and nothing more.
 *
 * This is a placement floor, NOT a new waterline: `isWater` still answers the
 * river question, the bank distance field is still measured to it, and the
 * willows the sources put at the water's edge still stand at the water's edge —
 * a few metres back up a bank that rises 0.2 m, which on the documented South
 * Division marsh strip is a handful of metres and on the north bank is under one.
 */
const TREE_DRY_MARGIN_M = 0.20;
/**
 * Below this is navigable channel rather than a shallow slough. Used only to
 * split the box into its three land divisions: the North Branch, the main stem
 * and the South Branch are all deeper than this, and the documented unnamed
 * slough on the north side is not, so the divisions come out as the three land
 * masses a person in 1835 would have named.
 */
const CHANNEL_Y = -0.60;

/** Earth radius corrected for standard atmospheric refraction (k = 0.13). */
const R_EFF = 6371000 / 0.87;

/**
 * The scene's own haze, copied from `world.js` — `FogExp2(HORIZON_HAZE,
 * HAZE_DENSITY)`. Copied, not imported: world.js belongs to another
 * parcel this round and a cross-parcel import that breaks takes the page with
 * it. **If world.js's haze moves, move these.** The band runs the law by hand
 * against each body's REAL distance because it is drawn on a ring at a fixed
 * radius, where the scene's own fog would haze a grove four miles out exactly
 * as hard as a treeline at eleven hundred metres.
 */
const HAZE_DENSITY = 0.00125;
/**
 * The fog COLOUR, copied verbatim from `world.js`'s `HORIZON_HAZE`. It is the
 * colour distance goes to, and it is deliberately not the sky: real haze pushes
 * distance BLUE, and the value here is the one the atmosphere parcel retargeted
 * to for that reason (the bar's distant land runs B-R +27; the grey-green this
 * replaced ran -13).
 *
 * **This hex IS the rendered colour, and this file spent three weeks assuming
 * it was not.** `world.js` feeds it to `FogExp2`, whose lerp runs after the
 * tone curve on a uniform uploaded in the output colour space, so a fully
 * fogged pixel displays sRGB (136,163,192) — this value, unmodified. The band
 * matches the fogged GROUND by decoding the same hex once and no more; see
 * `hazeDisplayLinear()`, which used to do more and is what put the band and the
 * ground in different tonal worlds.
 */
const HORIZON_HAZE = 0x88a3c0;
/**
 * The cap, and the one place this file argues with the scene's atmosphere.
 * world.js's haze is total by 1500 m by design — docs/LIBERTIES.md L17 leans on
 * that to hide a radial ground skirt nothing is claimed about. But the dossier
 * § 1.6 is a table of timber bodies at three, four and six miles, headed "for
 * distant LOD / horizon silhouettes", and total extinction at 1500 m erases
 * every one of them. Capping the band's haze keeps them on the horizon at a
 * contrast that never exceeds what the scene's own air allows anything else at
 * about 1.2 km. It is a compromise between two parcels' instructions, and it is
 * filed as docs/LIBERTIES.md **L35**.
 *
 * A WARNING ABOUT WHY THIS CONSTANT LOOKS LOAD-BEARING, AND IS NOT.
 *
 * It was briefly recorded — here and in L35 — that this cap had become the only
 * thing keeping the band darker than its own sky, because a fully-hazed surface
 * displayed BRIGHTER than the sky (L 170 against L 162). That measurement was
 * real and its subject was not.
 *
 * The scene's fog does not run where this file assumed. In the vendored r185 the
 * fragment order is `opaque -> tonemapping -> colorspace -> fog`, and the fog
 * colour uniform is uploaded through `getUnlitUniformColorSpace()`. So FogExp2
 * is a straight lerp toward the literal hex IN DISPLAY SPACE, after the tone
 * curve: a fully-fogged pixel is exactly sRGB (136,163,192), L 159.4 — four
 * levels BELOW the horizon sky, which is what airlight is supposed to do.
 *
 * The L 170 came from `hazeDisplayLinear()` below, which USED TO run
 * HORIZON_HAZE through ACES to derive this band's display colour. That was
 * arithmetically correct and answered a question the renderer never asks. The
 * consequence was live and was this file's bug, not the atmosphere's: the band
 * was aimed at (152,175,195) while the ground it stands on converges to
 * (136,163,192), so the far timber sat 16 red and 12 green off the far ground
 * it touches — and because the band is `toneMapped: false, fog: false`, nothing
 * downstream reconciles them. **Fixed 2026-08-13**: the tone curve is gone from
 * that function and both ends now decode the same hex once. The gate compares
 * the band's own hazed end against `scene.fog.color` rather than against a
 * number written down here.
 *
 * So: this cap is about EVIDENCE (holding the dossier's 3-6 mile timber on the
 * horizon), and only about that. Judge it on that argument alone. And do not
 * copy an atmosphere constant into this file and then transform it — the
 * copied values matched world.js exactly the whole time; it was the maths on
 * top of them that drifted, which no drift check on the constants would catch.
 */
const HAZE_MAX = 0.82;
/** Haze fraction for a body at `d` metres. */
function hazeAt(d) {
  const f = HAZE_DENSITY * d;
  return Math.min(HAZE_MAX, 1 - Math.exp(-f * f));
}
/** The colour of a mass of July deciduous canopy before any haze is added. */
const TIMBER_SRGB = 0x39482f;

/** Where the horizon band is drawn. Beyond any ground in the scene (the box's
 *  corner-to-corner diagonal is 905 m) and well inside the 3000 m far plane. */
const RING_RADIUS = 1100;
/** How far below the eye the band's foot reaches, in metres at RING_RADIUS.
 *  Enough to tuck under the water plane and under any far ground, not enough to
 *  occlude a horizon another parcel might extend. */
const RING_FOOT_M = -12;
/** Metres of camera movement that force the band to be re-solved. 0.75 m is
 *  about a sixth of a degree of parallax on the nearest far body — subpixel. */
const RING_REBUILD_M = 0.75;
/**
 * How near a far body may come before it is dropped from the band. A silhouette
 * on a ring is a FAR-field device: it carries angular size but no depth, and a
 * stand of timber a hundred metres past the edge of the heightfield renders as a
 * smooth black wall ten degrees high and reads as a mountain. On a lake plain
 * that is a worse lie than the gap it leaves.
 */
const MIN_FAR_M = 330;
/**
 * The floor under the crown/gap modulation, in FRAME PIXELS, and the reason the
 * band is solved against the viewport at all.
 *
 * The modulation below breaks the profile up crown by crown and opens sky
 * through the stand — `k` runs down to about 0.02 in a gap. That is texture on
 * a treeline four hundred metres out, where the band is forty pixels tall. On
 * the dossier's three-, four- and six-mile bodies the same multiplier is a
 * DELETION: a 20 m canopy at 9.7 km subtends 1.4 px at desktop, and two per
 * cent of 1.4 px is nothing at all. Measured at the spawn station with this
 * floor removed, the modulation cut **30 of 280 bearings on a phone and 14 of
 * 281 on a desktop** below one pixel, with the worst silhouette drawn at
 * **0.18 px** and **0.31 px** — geometry solved, written into the buffer, and
 * too thin to land on a pixel. That is the mechanism ROADMAP § S6a item 5 names
 * behind the photographic finding that only 31 % of horizon columns carried any
 * timber; the photograph's own measure is not re-run here, and the item says so.
 *
 * So the modulation may take a bearing down to this and no further, whenever
 * the bearing's own unmodulated crown is at least this tall. Below it — a body
 * so far off that its raw silhouette is already sub-pixel — the modulation is
 * suppressed entirely, because a texture that cannot be drawn can only subtract.
 * Where the band IS resolvable (a treeline at 400 m is 40 px) the floor binds
 * on nothing: 0.02 of 40 px is 0.8 px and the gaps stay open.
 *
 * 1.0 px rather than 2: at 1 px the silhouette is continuous and still thin
 * enough that no crown reads as a ridge, which is the failure the modulation
 * exists to prevent. The gate measures both directions — see
 * `horizonContinuity()`.
 */
const MIN_SILHOUETTE_PX = 1.0;
/**
 * Pixels per radian of vertical field, used when nothing supplies the live
 * viewport. 800 rows over a 55° vertical field — the desktop release viewport
 * at its narrowest clamp, so an unwired caller gets the conservative answer
 * rather than a generous one.
 */
const DEFAULT_PX_PER_RAD = 800 / (55 * Math.PI / 180);

/* -------------------------------------------------------------------------- */
/* the species                                                                 */
/* -------------------------------------------------------------------------- */

/**
 * One entry per woody species drawn. `h` is the JULY height in metres and `dbh`
 * the diameter at breast height, both straight out of the dossier's tables;
 * `dossier` names the section the row came from. The two greens are a shaded
 * and a sunlit July foliage colour — render tuning, not evidence, and the pair
 * the palette record will own once `data/flora/palettes/` is populated. `bark`
 * is the bole, and the optional `barkUpper` the upper bole and limbs where a
 * species is drawn in two tones; both are invented, as every colour here is,
 * and a species that omits `barkUpper` is drawn in one tone as before.
 *
 * form: gallery = tall crowded floodplain tree · open = open-grown, short bole
 * and heavy horizontal limbs · lean = bank willow leaning over the water ·
 * sub = subcanopy · thicket = clonal woody screen, no bole.
 */
const SPECIES = {
  // ---- ZONE 5, riverbank and floodplain timber --------------------------- //
  populus_deltoides: { common: 'eastern cottonwood', dossier: 'ZONE 5',
    form: 'gallery', h: [22, 30], dbh: [0.60, 1.00], spreadK: 0.56, boleK: 0.46, puffs: 7,
    dark: 0x3d5a2c, light: 0x86a252, bark: 0x6e6759,
  },
  salix_nigra: { common: 'black willow', dossier: 'ZONE 5',
    form: 'lean', h: [10, 16], dbh: [0.25, 0.55], spreadK: 0.74, boleK: 0.34, puffs: 5,
    dark: 0x44643a, light: 0x87a35c, bark: 0x38332a, lean: 0.30, water: true,
  },
  salix_amygdaloides: { common: 'peachleaf willow', dossier: 'ZONE 5',
    form: 'lean', h: [8, 14], dbh: [0.20, 0.45], spreadK: 0.70, boleK: 0.36, puffs: 5,
    dark: 0x53703f, light: 0x97ab63, bark: 0x4c4433, lean: 0.24, water: true,
  },
  acer_saccharinum: { common: 'silver maple', dossier: 'ZONE 5',
    form: 'gallery', h: [20, 28], dbh: [0.50, 0.90], spreadK: 0.62, boleK: 0.40, puffs: 7,
    dark: 0x425c32, light: 0x93a077, bark: 0x585144,
  },
  ulmus_americana: { common: 'American elm', dossier: 'ZONE 5',
    form: 'gallery', h: [18, 26], dbh: [0.35, 0.75], spreadK: 0.66, boleK: 0.46, puffs: 7,
    dark: 0x34502b, light: 0x6f8b46, bark: 0x4e4638,
  },
  fraxinus_pennsylvanica: { common: 'green ash', dossier: 'ZONE 5',
    form: 'gallery', h: [15, 22], dbh: [0.25, 0.55], spreadK: 0.54, boleK: 0.44, puffs: 6,
    dark: 0x3c5a2f, light: 0x76914b, bark: 0x4a4335,
  },
  quercus_bicolor: { common: 'swamp white oak', dossier: 'ZONE 5',
    form: 'open', h: [15, 20], dbh: [0.35, 0.70], spreadK: 0.92, boleK: 0.34, puffs: 9,
    dark: 0x2f4a27, light: 0x81916b, bark: 0x453d31,
  },
  celtis_occidentalis: { common: 'hackberry', dossier: 'ZONE 5',
    form: 'gallery', h: [12, 18], dbh: [0.20, 0.45], spreadK: 0.60, boleK: 0.42, puffs: 6,
    dark: 0x455f39, light: 0x7f954f, bark: 0x51493a,
  },
  juglans_nigra: { common: 'black walnut', dossier: 'ZONE 5',
    form: 'gallery', h: [18, 25], dbh: [0.35, 0.65], spreadK: 0.58, boleK: 0.48, puffs: 6,
    dark: 0x39552f, light: 0x718a49, bark: 0x3f382d,
  },
  // The one species carrying a second bark tone, and the only one whose record
  // says anything about its bark at all: "white mottled bark flashing on the
  // upper limbs" (`z05_riverbank_timber`). Both hexes are invented — no record
  // in `data/flora/` carries a colour — and bounded by this file's own barks:
  // the lower bole is the palest of the eighteen and the limbs are far paler
  // than any of them, because being the palest thing in the timber is the whole
  // of what that sentence describes. The MOTTLING is not drawn: the break is
  // between bole and limb, not a patchwork within either. docs/LIBERTIES.md
  // L118, ROADMAP K47. `dbh` sits at the top of this file's own height:diameter
  // ratios (0.035 against the gallery's 0.023–0.031) — the stoutest bole on the
  // bank, which is what a sycamore is; `boleK` forks it lower than the elm.
  platanus_occidentalis: { common: 'American sycamore', dossier: 'ZONE 5',
    form: 'gallery', h: [18, 25], dbh: [0.55, 0.95], spreadK: 0.62, boleK: 0.38, puffs: 6,
    dark: 0x60783e, light: 0x9bb06c, bark: 0x7a7263, barkUpper: 0xd9d3c2,
  },
  salix_interior: { common: 'sandbar willow', dossier: 'ZONE 5',
    form: 'thicket', h: [2.2, 4.0], dbh: [0.04, 0.08], spreadK: 1.30, boleK: 0, puffs: 4,
    dark: 0x63805a, light: 0xa4b487, bark: 0x4f4c3c,
  },

  // ---- ZONE 6a, the swampy timber thicket -------------------------------- //
  fraxinus_nigra: { common: 'black ash', dossier: 'ZONE 6a',
    form: 'gallery', h: [14, 20], dbh: [0.22, 0.45], spreadK: 0.48, boleK: 0.52, puffs: 5,
    dark: 0x35512c, light: 0x6b8743, bark: 0x474034,
  },

  // ---- ZONE 6b, the fire-protected mesic pocket -------------------------- //
  tilia_americana: { common: 'basswood', dossier: 'ZONE 6b',
    form: 'gallery', h: [18, 24], dbh: [0.35, 0.70], spreadK: 0.58, boleK: 0.46, puffs: 6,
    dark: 0x3d5c2e, light: 0x81994c, bark: 0x4d4638,
  },
  acer_saccharum: { common: 'sugar maple', dossier: 'ZONE 6b',
    form: 'gallery', h: [18, 24], dbh: [0.30, 0.65], spreadK: 0.56, boleK: 0.44, puffs: 7,
    dark: 0x2d4b26, light: 0x6a8940, bark: 0x4b4436,
  },
  quercus_rubra: { common: 'red oak', dossier: 'ZONE 6b',
    form: 'gallery', h: [20, 26], dbh: [0.40, 0.80], spreadK: 0.66, boleK: 0.44, puffs: 7,
    dark: 0x35502b, light: 0x728e45, bark: 0x494134,
  },
  ostrya_virginiana: { common: 'ironwood', dossier: 'ZONE 6b',
    form: 'sub', h: [6, 10], dbh: [0.12, 0.25], spreadK: 0.62, boleK: 0.42, puffs: 4,
    dark: 0x3e5a33, light: 0x789249, bark: 0x5a5142,
  },

  // ---- ZONE 6c / ZONE 7, the sand-ridge oaks ----------------------------- //
  quercus_macrocarpa: { common: 'bur oak', dossier: 'ZONE 6c / ZONE 7',
    form: 'open', h: [14, 19], dbh: [0.45, 0.95], spreadK: 1.18, boleK: 0.30, puffs: 10,
    dark: 0x334f29, light: 0x748d45, bark: 0x3a332a, fireScar: true,
  },
  quercus_alba: { common: 'white oak', dossier: 'ZONE 6c / ZONE 7',
    form: 'open', h: [16, 22], dbh: [0.40, 0.85], spreadK: 1.02, boleK: 0.34, puffs: 9,
    dark: 0x3a5730, light: 0x7c9349, bark: 0x6a6355, fireScar: true,
  },
  quercus_velutina: { common: 'black oak', dossier: 'ZONE 6c',
    form: 'open', h: [14, 20], dbh: [0.30, 0.65], spreadK: 0.92, boleK: 0.36, puffs: 8,
    dark: 0x2d4625, light: 0x67813e, bark: 0x332e26, fireScar: true,
  },
  carya_ovata: { common: 'shagbark hickory', dossier: 'ZONE 6c',
    form: 'gallery', h: [15, 20], dbh: [0.25, 0.50], spreadK: 0.50, boleK: 0.52, puffs: 5,
    dark: 0x405c2d, light: 0x7d974b, bark: 0x655c48,
  },
};

/**
 * The communities, and what fraction of the canopy each species holds in them.
 * Weights are the dossier's per-species densities; `perHa` is the STAND density
 * the dossier gives for the community as a whole, which is the number that
 * governs — the per-species figures are microsite densities and sum higher.
 *
 * THE WEIGHT WRITTEN HERE IS THE WEIGHT THAT PLANTS THE STEM (ROADMAP K46).
 * It was not, until 2026-08-16: `mixes` was rebuilt as
 * `records.density[id] ?? fallback`, so one global midpoint per species — taken
 * from whichever `TIMBER_ZONES` entry happened to name it first — overwrote
 * every per-community weight below, and seventeen of the twenty-six entries ran
 * at a number other than the one they are written to.
 *
 * K46 chose the literal, and the reason is a fact about the DATASET rather than
 * a preference. The alternative — key the density by (zone, species) and let
 * each community read the band from the zone its own `dossier` cites — cannot
 * express what this table says, because `wet_woods` cites ZONE 6a and
 * `mesic_pocket` cites ZONE 6b and BOTH resolve to the single record
 * `z06_dense_forest`. A zone-keyed density gives the elm 60 in both, and the
 * 12 that makes it incidental in the fire-protected pocket has nowhere to live.
 * The sub-community reading is real and is recorded nowhere else in this
 * project, so the file keeps it.
 *
 * The record is not discarded; it becomes the CONSTRAINT. Every weight below is
 * checked at load against the band of each zone its community's `zones` names,
 * and one that falls outside every such band is a claim no record carries: it
 * must be declared in that community's `departures`, with the reason, or the
 * load raises. Measured across the twenty-six entries: 23 sit inside their own
 * cited band, 3 fall below one, and none is above — so the hand weights were
 * never an inflation, and the three that depart are the three the prose already
 * explains. `perHa` is the STAND density the dossier gives for the community as
 * a whole, which is the number that governs — the per-species figures are
 * microsite densities and sum higher.
 *
 * `zones` is the machine-readable form of the `dossier` line and is held equal
 * to it by `tools/measure_planting_reach.py`, so the citation a reader sees and
 * the bands the loader checks against cannot drift apart.
 */
const COMMUNITIES = {
  gallery: {
    label: 'Riverbank & floodplain timber',
    dossier: 'ZONE 5 — “irregular gallery 30–120 m wide, canopy 30–80 trees/ha”',
    zones: ['z05_riverbank_timber'],
    perHa: [34, 62],
    mix: [
      ['populus_deltoides', 14], ['acer_saccharinum', 25], ['ulmus_americana', 25],
      ['fraxinus_pennsylvanica', 22], ['quercus_bicolor', 10], ['celtis_occidentalis', 8],
      ['juglans_nigra', 2], ['salix_amygdaloides', 8],
      // ROADMAP K45(b1). The American sycamore, at the midpoint of the [1, 3]
      // its own z05 record carries. K45(b) prescribed a 1: the bottom of the
      // band, and — under K46's rule, which plants the literal — a figure that
      // would now have halved the handful of sycamores actually standing.
      ['platanus_occidentalis', 2],
    ],
    /** At the water's edge the mix goes to willow, per the ZONE 5 densities. */
    edgeMix: [['salix_nigra', 42], ['salix_amygdaloides', 17], ['acer_saccharinum', 8]],
    /**
     * Weights that sit outside every band this community's `zones` record, and
     * why. A departure is an ecological claim of this file's own — see
     * docs/LIBERTIES.md L117 — so it is written down or the load raises.
     */
    departures: {
      'mix.salix_amygdaloides':
        'ZONE 5 bands the peachleaf willow at 10–25/ha across the whole gallery. This '
        + 'file splits that one band between its two lists — 17 at the water’s edge, '
        + 'inside the band, and 8 behind it — because the record describes a bank tree '
        + 'and the gallery is 30–120 m wide. The split is this file’s; the two lists '
        + 'together stand for the one recorded band.',
      'edgeMix.acer_saccharinum':
        'The edge mix exists to say what its own note says — at the water’s edge the mix '
        + 'goes to willow — and ZONE 5 bands the silver maple for the gallery as a whole '
        + '(15–35/ha) without banding the edge separately. Cutting it to 8 is how that '
        + 'sentence is expressed as a weight; the number is this file’s.',
    },
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
  },
  wet_woods: {
    label: 'Swampy timber thicket (the 1821 Walls note)',
    dossier: 'ZONE 6a — canopy 50–110/ha over the poorly drained clay',
    zones: ['z06_dense_forest'],
    perHa: [52, 84],
    mix: [
      ['ulmus_americana', 60], ['fraxinus_pennsylvanica', 32], ['fraxinus_nigra', 14],
      ['acer_saccharinum', 30], ['quercus_bicolor', 17],
    ],
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
  },
  mesic_pocket: {
    label: 'Fire-protected mesic pocket',
    dossier: 'ZONE 6b — east-of-water positions, the one place canopy closes',
    zones: ['z06_dense_forest'],
    perHa: [64, 96],
    mix: [
      ['tilia_americana', 25], ['acer_saccharum', 20], ['quercus_rubra', 14],
      ['ostrya_virginiana', 27], ['ulmus_americana', 12],
    ],
    departures: {
      'mix.ulmus_americana':
        'ZONE 6a, 6b and 6c share one record — `z06_dense_forest` — and its elm band, '
        + '40–80/ha, is the swamp thicket’s reading: the elm dominates the poorly drained '
        + 'clay. In the fire-protected pocket the closing canopy is basswood, sugar maple '
        + 'and ironwood and the elm is incidental to it, which is what 12 says. No record '
        + 'bands ZONE 6b apart from ZONE 6a, so this number is this file’s and is the '
        + 'reason K46 kept the hand weights at all.',
    },
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
  },
  ridge_oak: {
    label: 'Sand- and gravel-ridge oak stringers / bur oak savanna',
    dossier: 'ZONE 6c + ZONE 7 — 4–20/ha closed savanna, locally 1–4/ha open',
    // The dossier merges two zones and K45(b1) left "which band does it mean?"
    // as an open question. Under K46's rule it does not need answering: the
    // record is a constraint, not a source, and all four weights here sit
    // inside a band one of the two cited zones records.
    zones: ['z06_dense_forest', 'z07_bur_oak_savanna'],
    perHa: [7, 24],
    mix: [
      ['quercus_macrocarpa', 30], ['quercus_alba', 24], ['quercus_velutina', 12],
      ['carya_ovata', 8],
    ],
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
  },
};

/* -------------------------------------------------------------------------- */
/* the timber beyond the modelled ground                                       */
/* -------------------------------------------------------------------------- */

/**
 * Every body of timber the sources put outside the 640 m box, as a polyline of
 * its NEAR EDGE in local ENU metres — the near edge is what sets a silhouette.
 * `canopy` is the July canopy height range.
 *
 * These coordinates are NOT survey positions. Bearings and distances come from
 * § 1.6 and from the modern course of the rivers the sources name; the working
 * uncertainty on anything traced from the 1834 sheets is ~20 m, and on these,
 * kilometres out, far more. What is asserted is *there was timber over there,
 * about that far away, standing about that tall* — which is all a silhouette
 * shows.
 */
const FAR_TIMBER = [
  {
    id: 'south_branch_belt',
    label: 'The South Branch timber belt',
    canopy: [15, 26],
    crown: 13,
    path: [
      [82, -430], [78, -700], [10, -1180], [-40, -1700], [-64, -2166],
      [-250, -2700], [-470, -3120], [-620, -3400], [-665, -4100], [-690, -4900],
    ],
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
    note: 'Andreas: the South Side timber "follow[ed] the bend of the river … and '
        + 'extend[ed] south two or three miles". Documented as a body; the line '
        + 'drawn here is the east bank of the South Branch on its modern course, '
        + 'offset ~60 m from the channel, which is an inference about geometry, '
        + 'not about existence.',
  },
  {
    id: 'north_division_timber',
    label: 'The North Side body of timber',
    canopy: [14, 22],
    crown: 12,
    path: [
      [-60, 352], [40, 336], [130, 358], [215, 334], [300, 349], [385, 331],
      [470, 356], [560, 337], [645, 361], [730, 340], [820, 366],
    ],
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
    note: 'Andreas: the North Side carried "a body of thrifty heavy growth of '
        + 'timber", continuous except for the sandy hills near the lake and the '
        + 'marshy places; the 1821 PLS calls the ground north of the forks a '
        + '"swampy timber thicket". The front is carried east to about e +820, '
        + 'roughly 300 m short of the 1835 shore, because the sandy hills near '
        + 'the lake are the stated exception. The waviness is generated.',
  },
  {
    id: 'north_branch_belt',
    label: 'The North Branch timber, toward the Caldwell reservation',
    canopy: [13, 21],
    crown: 12,
    path: [
      [-95, 345], [-190, 700], [-300, 1150], [-470, 1750], [-700, 2450],
      [-1050, 3400], [-1500, 4300], [-1900, 5000],
    ],
    confidence: 'inferred',
    sources: [],
    note: 'The PLS surveyed the Sauganash / Billy Caldwell reservation up the '
        + 'North Branch and noted timber there (dossier § 1.6, NNW 4–8 mi). The '
        + 'belt is placed on the EAST bank, the fire-protected side — McBride & '
        + 'Bowles found density and fire-intolerant species concentrated east of '
        + 'watercourses. West of the channel stays prairie.',
  },
  {
    id: 'main_stem_belt_east',
    label: 'The South Water Street belt, east to Wells Street',
    canopy: [16, 24],
    crown: 13,
    path: [[326, 46], [360, 58], [396, 68]],
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
    note: 'Andreas: the South Side timber "extend[ed] east as far as Wells '
        + 'Street". Wells is about 400 m east of the datum in this frame, so the '
        + 'belt stops just outside the box rather than running on to the lake — '
        + 'this stub exists so it ends where the source ends it and not at the '
        + 'edge of the heightfield.',
  },
  {
    id: 'south_branch_grove',
    label: 'The grove up the South Branch (Hardscrabble / Lee\'s Place)',
    canopy: [13, 20],
    crown: 12,
    /** A closed ring: the near edge of a grove is its whole outline. */
    path: ringPath(-2323, -5355, 430, 14),
    confidence: 'inferred',
    sources: ['chicagology_prefire273'],
    note: 'Andreas names it as the ONE piece of West Side timber. Its bearing '
        + '(about 203°) and distance (about 3.6 mi) are read off the modern '
        + 'position of Bridgeport, which is where Hardscrabble was.',
  },
];

/**
 * The named groves § 1.6 lists that are NOT drawn, with the arithmetic that
 * rules each one out. `elevation_deg` is how far the top of a canopy tree at
 * that distance stands above a standing eye's horizon, refraction included.
 * Under about a tenth of a degree is under two pixels at this field of view and
 * under the contrast threshold through 15 km of July haze.
 */
const OMITTED_TIMBER = [
  { id: 'cottage_grove', label: 'Cottage Grove', bearing_deg: 180, distance_m: 9660,
    canopy_m: 18, confidence: 'inferred',
    why: 'inferred, and at 6 mi it clears the horizon by under a tenth of a degree' },
  { id: 'big_woods', label: 'The Big Woods of north-east Cook', bearing_deg: 350,
    distance_m: 17700, canopy_m: 18, confidence: 'documented',
    why: 'documented, but at 11 mi the curvature of a flat plain has taken all but '
       + 'a few centimetres of it below the horizon' },
  { id: 'la_framboise', label: 'La Framboise Woods, Des Plaines River', bearing_deg: 270,
    distance_m: 16100, canopy_m: 20, confidence: 'documented',
    why: 'documented, same arithmetic as the Big Woods' },
  { id: 'blue_island', label: 'Blue Island', bearing_deg: 200, distance_m: 22500,
    canopy_m: 36, confidence: 'inferred',
    why: 'the moraine lifts its oaks 18 m, the only reason it clears the horizon at '
       + 'all — and then by a third of a pixel' },
];

/** A closed ring of points, for a grove whose outline is its silhouette. */
function ringPath(e, n, radius, steps) {
  const pts = [];
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * Math.PI * 2;
    pts.push([e + Math.cos(a) * radius, n + Math.sin(a) * radius]);
  }
  return pts;
}

/* -------------------------------------------------------------------------- */
/* the zone records                                                            */
/* -------------------------------------------------------------------------- */

async function fetchOk(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} ${url}`);
  return res.json();
}

/** sRGB [r,g,b] 0-255 from a record -> the hex this file's tables speak. */
function rgbHex(rgb) {
  if (!Array.isArray(rgb) || rgb.length < 3) return null;
  return ((rgb[0] & 255) << 16) | ((rgb[1] & 255) << 8) | (rgb[2] & 255);
}

/** A lighter companion green, for a record that carries only one. */
function lighten(hex) {
  const r = Math.min(255, Math.round(((hex >> 16) & 255) * 1.34 + 26));
  const g = Math.min(255, Math.round(((hex >> 8) & 255) * 1.28 + 22));
  const b = Math.min(255, Math.round((hex & 255) * 1.42 + 20));
  return (r << 16) | (g << 8) | b;
}

const FORM_OF = {
  tree_gallery: 'gallery',
  tree_open_crown: 'open',
  tree_leaning: 'lean',
  tree_columnar: 'columnar',
  thicket_clonal: 'thicket',
};

const CONFIDENCE_VALUE = { attested: 0.0, inferred: 0.5, reconstructed: 1.0 };

/* -------------------------------------------------------------------------- */
/* the woody head — ROADMAP K45(c)                                             */
/* -------------------------------------------------------------------------- */

/**
 * Head archetype per RECORDED INFLORESCENCE SHAPE, for the woody cohort.
 *
 * K44 measured that three recorded July inflorescences draw no flower and named
 * the cause exactly: *"`trees.js` has no head archetype at all"*. Two of the
 * three are this file's — the **American basswood in bloom** (`flowering`,
 * `cluster_terminal`, sRGB 222,214,152) and the **ironwood's hop-like fruit**
 * (`fruiting`, `cluster_terminal`, 214,212,180), both in `z06_dense_forest` and
 * both in the `mesic_pocket` mix, so both stand in this scene today with nothing
 * on them. The third is the riverbank grape, whose `vine_drape` form no reader
 * implements; it is a ROUTING gap and stays K45(b)'s, not this parcel's.
 *
 * **The repair K44 wrote down is one step short of the truth, and this is the
 * finding.** Handing this file `flora.js`'s `HEAD_OF_SHAPE` verbatim draws
 * `cluster_terminal`'s count — **1 to 4 heads** — because that table is
 * calibrated for a forb, where the whole plant IS one flowering scape. On a
 * basswood the arithmetic says what that looks like: the record's own
 * `size_m` is [0.06, 0.12] m for ONE inflorescence, and a 0.09 m cluster at the
 * 23 m slant range of a neighbouring crown (11 m up, 20 m out) subtends
 * 0.0039 rad — **3.3 px** at this file's `DEFAULT_PX_PER_RAD` of 833. The crown
 * carrying them is 10–16 m across, which is **580 px** at the same range. Four
 * 3-px specks on a 580-px crown is not a tree in flower; it is four pixels of
 * noise, and it would have banked a false pass on K44's own assertion 5.
 *
 * So SIZE comes from the record exactly and MULTIPLICITY is keyed to the crown,
 * which is a liberty and is recorded as one (docs/LIBERTIES.md L115) for the
 * same reason `flora.js`'s is (L35): **the records give the density of PLANTS
 * and the size of ONE inflorescence, and say nothing about how many a plant
 * carries.** Keying it to the crown rather than to a constant is what makes an
 * 18 m basswood and a 7 m ironwood differ by their own evidenced `width_m`
 * instead of by a number typed here.
 *
 *   kind   which archetype draws it. `cluster` is a small dense blob; a
 *          pendulous `catkin` is drawn longer than it is wide. At 3 px the
 *          difference is a silhouette, not a shape, which is why there are two
 *          and not nine — this file is not `flora.js` and must not pretend the
 *          extra archetypes are resolvable at the ranges it draws at.
 *   perM   heads per metre of crown width, before the clamp below.
 *   band   how far DOWN from `height_frac` the heads are carried, as a fraction
 *          of crown height. A terminal cluster sits in the outer shell of the
 *          canopy; it is not scattered through its interior, where nothing
 *          would see it.
 *
 * The map is exhaustive over the shapes the woody records actually carry, and a
 * shape it cannot draw is REPORTED and draws nothing rather than being quietly
 * substituted — the same rule as `flora.js`, for the same reason.
 */
const WOODY_HEAD_OF_SHAPE = {
  cluster_terminal: { kind: 'cluster', perM: 1.6, band: 0.30 },
  berry_cluster: { kind: 'cluster', perM: 1.3, band: 0.34 },
  cluster_axillary: { kind: 'catkin', perM: 1.8, band: 0.52 },
  raceme: { kind: 'catkin', perM: 1.4, band: 0.36 },
  nut_husk: { kind: 'cluster', perM: 0.9, band: 0.30 },
  cherry: { kind: 'cluster', perM: 1.2, band: 0.34 },
};

/**
 * The clamp on that multiplicity, and both ends of it are about legibility
 * rather than botany. Below the floor a crown reads as unflowered and the
 * layer may as well not have been drawn; above the ceiling the heads merge into
 * a pale cap and the tree stops reading as a tree in flower and starts reading
 * as a tree with a different foliage colour. A 13 m basswood crown lands on 21
 * and a 5.5 m ironwood on 9.
 */
const HEADS_MIN = 6;
const HEADS_MAX = 26;

/** The July gate, copied from `flora.js` rather than imported, because these two
 *  files share no module and the rule is CONTRACT.md §5.4 rule 1 rather than
 *  either file's. A record that is vegetative or in bud in mid-July draws no
 *  head even if it carries one, and the contradiction is reported. K44: the
 *  woody layer had no July gate at all, because `july.phenology` was read by
 *  `flora.js` alone. */
const VEGETATIVE_PHASES = ['vegetative', 'budding'];

/**
 * One species' head spec, or null. Mirrors `flora.js`'s `headOf` — same gate,
 * same refusal to substitute an archetype — and differs only in what it keys
 * the count to.
 */
function woodyHeadOf(sp, zoneId, problems) {
  const july = sp.july ?? {};
  // Named for the field it holds, and that is load-bearing rather than a style
  // choice: `rgb` is an ambiguous leaf, so `tools/measure_layer_reads.py` scans
  // it PARENT-QUALIFIED (`inflorescence.rgb`). A local called `inflor` reads
  // the record just as truly and is invisible to the scan, which is how
  // `flora.js` ends up needing its whole expression matched verbatim instead.
  const inflorescence = july.inflorescence;
  if (!inflorescence) return null;
  if (VEGETATIVE_PHASES.includes(july.phenology)) {
    problems.push(`trees: ${zoneId}/${sp.id ?? sp.binomial} is '${july.phenology}' and `
      + 'still carries an inflorescence — no head is drawn; the record needs fixing');
    return null;
  }
  const style = WOODY_HEAD_OF_SHAPE[inflorescence.shape];
  if (!style) {
    problems.push(`trees: ${zoneId}/${sp.id ?? sp.binomial} records inflorescence shape `
      + `'${inflorescence.shape}', which has no woody archetype — its flower is not drawn`);
    return null;
  }
  const size = Array.isArray(inflorescence.size_m) && inflorescence.size_m.length === 2
    ? inflorescence.size_m : [0.06, 0.12];
  // `inflorescence.fruit` is deliberately NOT read here. K44 measured that the
  // boolean reaches nothing and that 29 of the 31 records carrying it are drawn
  // in the fruit's own colour and shape anyway — it is redundant with
  // `phenology: 'fruiting'`, which this function does read. Storing it on the
  // spec and drawing nothing from it would BE the fault K44 named, one field
  // further along, and would take it off that gate's banked list while changing
  // nothing a visitor sees.
  return {
    kind: style.kind,
    perM: style.perM,
    band: style.band,
    // The record's sRGB bytes. See `linear()` for why the transfer happens
    // exactly once on the way to a vertex colour.
    rgb: rgbHex(inflorescence.rgb),
    frac: clamp01(inflorescence.height_frac ?? 0.8),
    size,
    phenology: july.phenology ?? null,
  };
}

/**
 * Read the timber zones and hand back one render spec per species. The record
 * wins on everything it carries — height, crown width, July foliage, density,
 * confidence — and this file supplies only the draw archetype (bole fraction,
 * puff count, bark colour) plus a fallback for a species the records do not
 * name. A `form` this module cannot draw is recorded in
 * `stats.unimplementedForms` and drawn as nothing: reported through stats
 * rather than `problems`, because it is a gap in the RENDERER and `problems` is
 * what the repo smoke reads to decide whether the DATA loaded.
 */
async function loadTimberZones(dataBase, problems = []) {
  const manifestUrl = new URL('flora/index.json', dataBase);
  const manifest = await fetchOk(manifestUrl);
  const specs = {};
  const bands = {};
  const unimplemented = new Set();
  const zonesRead = [];
  const heads = [];
  for (const id of TIMBER_ZONES) {
    const entry = (manifest.zones ?? []).find((z) => z.id === id);
    if (!entry) throw new Error(`flora/index.json names no zone ${id}`);
    const rec = await fetchOk(new URL(entry.file, manifestUrl));
    zonesRead.push(id);
    bands[id] = {};
    for (const sp of rec.species ?? []) {
      if (sp.role !== 'tree' && sp.role !== 'thicket') continue;
      const form = FORM_OF[sp.form];
      if (!form) { unimplemented.add(sp.form); continue; }
      // The recorded band, kept PER ZONE. It is the constraint a community's
      // hand weight is checked against (ROADMAP K46) and no longer a value
      // that replaces one: collapsing it to a first-zone-wins midpoint is
      // exactly what overwrote seventeen of the twenty-six mix entries.
      const perHa = sp.abundance?.density_per_ha;
      if (Array.isArray(perHa) && perHa.length === 2) {
        bands[id][sp.id] = [perHa[0], perHa[1]];
      }
      if (specs[sp.id]) continue;
      const base = SPECIES[sp.id] ?? SPECIES.ulmus_americana;
      const dark = rgbHex(sp.july?.foliage_rgb);
      const light = rgbHex(sp.july?.foliage_rgb_alt);
      specs[sp.id] = {
        ...base,
        common: sp.common ?? base.common,
        form,
        h: Array.isArray(sp.height_m) && sp.height_m.length === 2 ? sp.height_m : base.h,
        crownW: Array.isArray(sp.width_m) && sp.width_m.length === 2 ? sp.width_m : null,
        dark: dark ?? base.dark,
        light: light ?? (dark != null ? lighten(dark) : base.light),
        // Never better than `inferred`, whatever the species record says: the
        // record attests that the species stood in this community, and this
        // module invented the position of every individual stem in the scene.
        conf: Math.max(0.5, CONFIDENCE_VALUE[sp.confidence] ?? 0.5),
        july: sp.july?.appearance ?? base.july,
        // The recorded July inflorescence, or null. A thicket is drawn by
        // `addThicket`, which has no head path, so a head on one would be
        // silently dropped — reported here instead, because a dropped flower
        // that nothing says was dropped is exactly the fault K44 measured.
        head: woodyHeadOf(sp, id, problems),
        fromRecord: true,
      };
      if (specs[sp.id].head) {
        if (form === 'thicket') {
          problems.push(`trees: ${id}/${sp.id} is a thicket carrying a `
            + `'${sp.july.inflorescence.shape}' inflorescence, and the clonal path draws `
            + 'no head — its flower is not drawn');
          specs[sp.id].head = null;
        } else {
          heads.push(sp.id);
        }
      }
    }
  }
  return { specs, bands, unimplemented: [...unimplemented], zonesRead, heads };
}

/* -------------------------------------------------------------------------- */
/* small maths                                                                 */
/* -------------------------------------------------------------------------- */

function mulberry32(seed) {
  let a = seed >>> 0;
  return function rnd() {
    a = (a + 0x6D2B79F5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const lerp = (a, b, t) => a + (b - a) * t;
const clamp01 = (v) => (v < 0 ? 0 : v > 1 ? 1 : v);
function smoothstep(a, b, v) {
  const t = clamp01((v - a) / (b - a || 1e-6));
  return t * t * (3 - 2 * t);
}

/** Deterministic hash of two integers -> [0,1). */
function hash2(x, y) {
  let h = Math.imul(x | 0, 374761393) ^ Math.imul(y | 0, 668265263);
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

/** Smooth value noise on a lattice of `cell` metres, in [0,1]. */
function noise2(e, n, cell, salt = 0) {
  const x = e / cell;
  const y = n / cell;
  const x0 = Math.floor(x);
  const y0 = Math.floor(y);
  const fx = x - x0;
  const fy = y - y0;
  const sx = fx * fx * (3 - 2 * fx);
  const sy = fy * fy * (3 - 2 * fy);
  const a = hash2(x0 + salt, y0);
  const b = hash2(x0 + 1 + salt, y0);
  const c = hash2(x0 + salt, y0 + 1);
  const d = hash2(x0 + 1 + salt, y0 + 1);
  return lerp(lerp(a, b, sx), lerp(c, d, sx), sy);
}

/** Smooth value noise along one axis, in [0,1]. */
function noise1(u, salt = 0) {
  const i = Math.floor(u);
  const f = u - i;
  const s = f * f * (3 - 2 * f);
  return lerp(hash2(i, salt), hash2(i + 1, salt), s);
}

/** Squared distance from a point to a segment, in the plane. */
function segDist2(px, py, ax, ay, bx, by) {
  const vx = bx - ax;
  const vy = by - ay;
  const wx = px - ax;
  const wy = py - ay;
  const len = vx * vx + vy * vy;
  const t = len > 0 ? clamp01((wx * vx + wy * vy) / len) : 0;
  const dx = wx - vx * t;
  const dy = wy - vy * t;
  return dx * dx + dy * dy;
}

/** The 12 unit vertices and 20 faces of an icosahedron — one foliage puff. */
const ICO_V = (() => {
  const t = (1 + Math.sqrt(5)) / 2;
  const raw = [
    [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
    [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
    [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1],
  ];
  return raw.map(([x, y, z]) => {
    const l = Math.hypot(x, y, z);
    return [x / l, y / l, z / l];
  });
})();
const ICO_F = [
  [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
  [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
  [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
  [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
];

/* -------------------------------------------------------------------------- */
/* a growable mesh                                                             */
/* -------------------------------------------------------------------------- */

/**
 * Trees are MERGED rather than instanced, on purpose. An InstancedMesh is one
 * draw call for the lot, but every tree of a species is then the same tree at a
 * different scale, and a stand of clones is exactly what an open-grown savanna
 * must not look like. Chunked spatially — four quadrants, four calls, each
 * culled on its own — merging costs no more and buys real per-tree variation.
 */
class MeshBuf {
  constructor() {
    /** How many inflorescences landed in this chunk (ROADMAP K45(c)). Counted
     *  where they are built rather than estimated from the stem count, because
     *  the multiplicity is a function of each tree's own crown width. */
    this.heads = 0;
    this.pos = [];
    this.nrm = [];
    this.col = [];
    this.flex = [];
    this.conf = [];
    this.idx = [];
  }

  get count() { return this.pos.length / 3; }

  vert(x, y, z, nx, ny, nz, r, g, b, flex, conf) {
    this.pos.push(x, y, z);
    this.nrm.push(nx, ny, nz);
    this.col.push(r, g, b);
    this.flex.push(flex);
    this.conf.push(conf);
    return this.count - 1;
  }

  tri(a, b, c) { this.idx.push(a, b, c); }

  build() {
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(this.pos), 3));
    g.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(this.nrm), 3));
    g.setAttribute('color', new THREE.BufferAttribute(new Float32Array(this.col), 3));
    g.setAttribute('aFlex', new THREE.BufferAttribute(new Float32Array(this.flex), 1));
    g.setAttribute('_confidence',
      new THREE.BufferAttribute(new Float32Array(this.conf), 1));
    g.setIndex(new THREE.BufferAttribute(new Uint32Array(this.idx), 1));
    g.computeBoundingSphere();
    return g;
  }
}

/* -------------------------------------------------------------------------- */
/* building one tree                                                           */
/* -------------------------------------------------------------------------- */

const _c = new THREE.Color();
/**
 * sRGB hex -> linear rgb triple, which is what a vertex colour must be.
 *
 * ONE conversion, and the reason is worth stating because this function used to
 * do two. `THREE.ColorManagement.enabled` is true by default from r152, and
 * `Color.setHex(hex)` takes `SRGBColorSpace` as its default argument — so it has
 * ALREADY landed the value in the linear working space by the time it returns.
 * The `.convertSRGBToLinear()` that used to follow squared the transfer, which
 * for a July green is a factor of about twelve: the horizon band rendered at
 * L 102 where this file's own haze law asks for L 158, and the near timber was
 * only survivable because the error was being paid for twice over in the
 * lighting. `flora.js` builds its colours from a float triple, which
 * `Color(r,g,b)` does NOT convert, so its single explicit conversion is correct
 * — that asymmetry is exactly why the sward and the timber disagreed.
 */
function linear(hex) {
  _c.setHex(hex);
  return [_c.r, _c.g, _c.b];
}

/**
 * The vertex colour whose DISPLAYED value is the one a fully fogged surface
 * displays — the colour the band's hazed end has to reach for, because that is
 * where the far ground it stands on converges.
 *
 * **It is `linear(HORIZON_HAZE)`, and until 2026-08-13 it was that run through
 * ACES as well.** The tone curve was not wrong arithmetic; it answered a
 * question the renderer never asks. The band is a `MeshBasicMaterial` with
 * `toneMapped = false`, so its fragment goes `opaque → colorspace` and a linear
 * vertex colour displays as exactly the sRGB hex it decodes from. The ground's
 * fragment goes `opaque → tonemapping → colorspace → fog`, and in the vendored
 * r185 `fogColor` is uploaded through `getUnlitUniformColorSpace()` — so the
 * fog is a straight lerp toward the literal hex AFTER the tone curve. Both ends
 * therefore land on the same target by decoding the same hex once, and the tone
 * curve was applied to one of them and to nothing it had to match.
 *
 * What that error cost is measured in docs/LIBERTIES.md L35: the band was aimed
 * at sRGB (152,175,195) while the ground under it converges to (136,163,192),
 * so the far timber sat **16 red and 12 green** off the far ground it touches,
 * with nothing downstream to reconcile them — `fog: false` on this material
 * means the band never meets the lerp that would have closed the gap. That is
 * the hard chroma break along the horizon, and it is this file's bug rather
 * than the atmosphere's: the copied constants matched `world.js` exactly the
 * whole time; it was the maths on top of them that drifted.
 *
 * Kept as a function, and derived rather than pasted, so the band still cannot
 * silently drift when the atmosphere parcel next moves `HORIZON_HAZE`.
 */
function hazeDisplayLinear() {
  return linear(HORIZON_HAZE);
}

/* -------------------------------------------------------------------------- */
/* how a crown is lit                                                          */
/* -------------------------------------------------------------------------- */

/**
 * A last multiplier on the record's foliage colour before it is used as diffuse
 * reflectance — the one calibration knob for how dark the timber stands.
 *
 * It sits at 1.0, and that is the finding rather than a default: the record's
 * `july.foliage_rgb`, converted ONCE to linear, is already a plausible leaf
 * reflectance (sRGB 57,72,47 is 4 % / 6 % / 3 %), so nothing needs scaling. What
 * had to be modelled instead was the crown's own SELF-SHADOWING, below. That
 * distinction matters: round 1 hit roughly the right average by squaring the
 * sRGB transfer, which darkened the sunlit cap and the deep interior by the same
 * factor and so flattened the crown into a ball. The darkness of a stand is a
 * lighting fact, not a pigment fact, and it belongs in the shading term.
 *
 * Kept as a named constant because it is where a future change to `world.js`'s
 * rig (a 3.0 sun plus a 2.4 hemisphere today) has to be absorbed. The check is
 * measured, not judged, exactly as `world.js` does for `SKY_EXPOSURE`: the near
 * stand should hold the Weber contrast the bar photograph's own tree mass holds
 * against its sky — 0.625 in `bar/dupage_tallgrass_2018-07-24.jpg`, against
 * 0.655 here.
 */
const CANOPY_ALBEDO = 1.00;
/**
 * A canopy is optically THICK. The sun reaches its upper outer shell and very
 * little else, so the visible surface of a crown runs from a bright sunlit top
 * to a deep interior shade — and that RANGE, not the average, is what makes a
 * tree read as a tree rather than as a green ball.
 *
 * Measured the same way on both, the bar photograph's tree mass carries a
 * standard deviation of 33 and round 1 drew 26, because the old ramp only ever
 * moved between two fairly close greens and modelled no self-shadowing at all.
 *
 * `_P` is how fast the shell falls into shade: above 1 it means most of the
 * crown surface is shaded and only the cap is fully lit, which is the right
 * shape for a dense July canopy.
 *
 * `_FLOOR` is what the deep interior keeps, and it is NOT a pure shadow term —
 * it must not be driven toward zero. A canopy UNDERSIDE, which is the whole of
 * what you see standing under a gallery tree on the river bank, is lit by
 * skylight and by sunlight transmitted THROUGH the leaves; that is why a summer
 * canopy glows from below rather than going black. At 0.028 the near trees in
 * the `river_bank` shot rendered as flat black plates, which is what set this.
 */
const CROWN_SHADE_FLOOR = 0.060;
const CROWN_SHADE_P = 2.4;
/** The same conversion for bark. See the bole comment in `addTree`. */
const BARK_ALBEDO = 0.30;

/** Add one foliage puff: a jittered icosahedron with a light-from-above ramp. */
function addPuff(buf, cx, cy, cz, radius, squash, dark, light, shade, flexBase, rnd, conf) {
  const base = buf.count;
  for (let i = 0; i < 12; i++) {
    const v = ICO_V[i];
    // Radial jitter so the silhouette is ragged rather than spherical.
    const k = radius * (0.62 + rnd() * 0.64);
    const x = cx + v[0] * k;
    const y = cy + v[1] * k * squash;
    const z = cz + v[2] * k;
    // Where this vertex sits between the underside of the mass and its cap,
    // and how much of the crown stands above it — a puff low in the tree is
    // shaded by everything over it, which `shade` carries.
    const up = clamp01(v[1] * 0.5 + 0.5);
    // Self-shadowing. Most of a crown's surface is interior and dark; the lit
    // shell is thin. The jitter keeps two puffs from shading identically.
    const lit = clamp01(Math.pow(up, CROWN_SHADE_P) * (0.35 + 0.65 * shade)
      * (0.80 + rnd() * 0.40));
    const occ = CANOPY_ALBEDO * lerp(CROWN_SHADE_FLOOR, 1, lit);
    // Hue follows the light: a shaded July leaf mass is a colder, deeper green
    // than the same mass in the sun, so the two recorded greens are the ends of
    // the shading ramp rather than a decorative tint.
    const t = clamp01(0.10 + shade * 0.28 + up * 0.74);
    const r = lerp(dark[0], light[0], t) * occ;
    const g = lerp(dark[1], light[1], t) * occ;
    const b = lerp(dark[2], light[2], t) * occ;
    buf.vert(x, y, z, v[0], v[1], v[2], r, g, b, flexBase + up * 0.22, conf);
  }
  for (const f of ICO_F) buf.tri(base + f[0], base + f[1], base + f[2]);
}

/**
 * The head primitive: an OCTAHEDRON, six vertices and eight faces.
 *
 * The cheapest closed solid is a tetrahedron and it was rejected on its
 * silhouette rather than on its cost — edge-on a tetrahedron is a sliver, and a
 * flower cluster that disappears from a third of the bearings around the tree is
 * a worse artefact than the two extra vertices are a saving. Eight faces is
 * still an eighth of the twenty `addPuff` spends on a foliage mass, which is the
 * right ratio: at the ranges this file draws at a head is 3 px and a crown is
 * 580 (see `WOODY_HEAD_OF_SHAPE`), so the head is where the geometry budget must
 * NOT be spent.
 */
const OCT_V = [
  [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1],
];
const OCT_F = [
  [0, 2, 4], [2, 1, 4], [1, 3, 4], [3, 0, 4],
  [2, 0, 5], [1, 2, 5], [3, 1, 5], [0, 3, 5],
];

/**
 * Add one inflorescence: a small blob in the record's own flower colour,
 * sitting in the outer shell of the crown.
 *
 * `stretch` is what separates the two archetypes — a `catkin` hangs, so it is
 * drawn longer than it is wide and dropped below its anchor; a `cluster` is
 * roughly isotropic. `lit` carries the same crown self-shadowing the foliage
 * gets, because a flower deep in a canopy is in the same shade the leaves
 * around it are, and a bloom drawn at full brightness through the whole crown
 * is the "glowing lights in a dark tree" failure.
 */
function addHead(buf, cx, cy, cz, radius, stretch, colour, lit, flex, rnd, conf) {
  const base = buf.count;
  const shade = lerp(0.34, 1.0, lit);
  const r = colour[0] * shade;
  const g = colour[1] * shade;
  const b = colour[2] * shade;
  for (let i = 0; i < 6; i++) {
    const v = OCT_V[i];
    const k = radius * (0.72 + rnd() * 0.56);
    buf.vert(
      cx + v[0] * k,
      cy + v[1] * k * stretch,
      cz + v[2] * k,
      v[0], v[1], v[2],
      r, g, b, flex, conf,
    );
  }
  for (const f of OCT_F) buf.tri(base + f[0], base + f[1], base + f[2]);
}

/** Add a tapered n-sided prism — a bole, or a limb. */
function addStem(buf, x0, y0, z0, x1, y1, z1, r0, r1, colour, sides, flex0, flex1, conf) {
  const dx = x1 - x0;
  const dy = y1 - y0;
  const dz = z1 - z0;
  const len = Math.hypot(dx, dy, dz) || 1e-4;
  // A frame perpendicular to the stem.
  const ux = dx / len;
  const uy = dy / len;
  const uz = dz / len;
  let ax = 0;
  let ay = 0;
  let az = 1;
  if (Math.abs(uz) > 0.9) { ax = 1; az = 0; }
  let px = uy * az - uz * ay;
  let py = uz * ax - ux * az;
  let pz = ux * ay - uy * ax;
  const pl = Math.hypot(px, py, pz) || 1e-4;
  px /= pl; py /= pl; pz /= pl;
  const qx = uy * pz - uz * py;
  const qy = uz * px - ux * pz;
  const qz = ux * py - uy * px;

  const base = buf.count;
  for (let ring = 0; ring < 2; ring++) {
    const bx = ring ? x1 : x0;
    const by = ring ? y1 : y0;
    const bz = ring ? z1 : z0;
    const rr = ring ? r1 : r0;
    const fl = ring ? flex1 : flex0;
    for (let s = 0; s < sides; s++) {
      const a = (s / sides) * Math.PI * 2;
      const ca = Math.cos(a);
      const sa = Math.sin(a);
      const nx = px * ca + qx * sa;
      const ny = py * ca + qy * sa;
      const nz = pz * ca + qz * sa;
      buf.vert(bx + nx * rr, by + ny * rr, bz + nz * rr, nx, ny, nz,
        colour[0], colour[1], colour[2], fl, conf);
    }
  }
  for (let s = 0; s < sides; s++) {
    const a = base + s;
    const b = base + ((s + 1) % sides);
    const c = a + sides;
    const d = b + sides;
    buf.tri(a, c, b);
    buf.tri(b, c, d);
  }
}

/**
 * A clonal thicket — sandbar willow on a point bar, and the one woody form in
 * this file that genuinely has no bole.
 *
 * Round 1 drew it as four loose icosahedra with `addStem` skipped entirely, so
 * a thicket was a handful of pale cushions scattered up to 3.6 m off-axis with
 * NOTHING underneath any of them, spreading to 7.8 m and with single puffs
 * about 5 m across. They read as floating polygons near the camera because that
 * is what they were. On the brief's own test — do the willow thickets screen
 * the point bars? — the answer was no; 202 isolated cushions screen nothing,
 * which is the exact opposite of the dossier's "dense clonal screens" at 2–6
 * stems/m².
 *
 * So it is built the way the plant grows: many thin whippy stems off one
 * rootstock, rising from a small basal patch and splaying into a fountain, with
 * every foliage mass centred ON a stem axis rather than hovering near one. That
 * is what makes the clump continuous from the ground up, and a row of them a
 * screen. A clump is about as wide as it is tall — sandbar willow gets its
 * width by standing shoulder to shoulder, not by each stool sprawling.
 */
function addThicket(buf, spec, x, groundY, z, rnd, scale = 1) {
  const conf = spec.conf ?? 0.5;
  const h = lerp(spec.h[0], spec.h[1], rnd()) * scale;
  const spread = h * 0.78 * (0.85 + rnd() * 0.30);

  const dark = linear(spec.dark);
  const light = linear(spec.light);
  const bark = linear(spec.bark).map((v) => v * BARK_ALBEDO);
  const tint = 0.90 + rnd() * 0.20;
  const d2 = dark.map((v) => v * tint);
  const l2 = light.map((v) => v * tint);

  const stems = 7 + Math.floor(rnd() * 5);
  const basal = 0.16 + rnd() * 0.26;
  for (let i = 0; i < stems; i++) {
    const a = (i / stems) * Math.PI * 2 + rnd() * 0.9;
    const br = basal * (0.30 + rnd() * 0.70);
    const bx = x + Math.cos(a) * br;
    const bz = z + Math.sin(a) * br;
    const out = (0.22 + rnd() * 0.28) * spread;
    const sh = h * (0.62 + rnd() * 0.38);
    const tx = x + Math.cos(a) * out;
    const tz = z + Math.sin(a) * out;
    const ty = groundY + sh;
    const rad = 0.018 + rnd() * 0.022;
    // Below ground at the foot, so a clump on uneven bar sand never floats.
    addStem(buf, bx, groundY - 0.10, bz, tx, ty, tz, rad, rad * 0.45,
      bark, 4, 0.10, 0.62, conf);

    // The foliage rides the stem: a mass at the tip, and on most stems a second
    // one lower down, which is what fills the screen from about knee height up.
    // A thicket is a DENSE mass, so most of its surface is shaded by the rest
    // of the clump — the shade values stay well below a free-standing crown's,
    // or the screen renders as a heap of pale pebbles rather than as willow.
    const pr = spread * (0.20 + rnd() * 0.12);
    addPuff(buf, tx, ty - pr * 0.25, tz, pr, 0.72, d2, l2,
      0.34 + rnd() * 0.38, 0.62, rnd, conf);
    if (rnd() < 0.55) {
      const f = 0.34 + rnd() * 0.30;
      addPuff(buf, lerp(bx, tx, f), lerp(groundY, ty, f), lerp(bz, tz, f),
        pr * 0.82, 0.78, d2, l2, 0.08 + rnd() * 0.24, 0.34, rnd, conf);
    }
  }
  return h;
}

/**
 * One tree, written into `buf` at (x, groundY, z). The forms differ where the
 * sources say they differ: a bur oak is not a gallery elm with a wider crown,
 * it is a short bole under heavy horizontal limbs holding a wide flat crown —
 * the dossier's "signature of the 1835 Chicago horizon" — and it carries fire
 * scarring on the lower bole because the surveyors kept noting burned trees.
 */
function addTree(buf, spec, x, groundY, z, rnd, scale = 1) {
  if (spec.form === 'thicket') return addThicket(buf, spec, x, groundY, z, rnd, scale);
  const conf = spec.conf ?? 0.5;
  const h = lerp(spec.h[0], spec.h[1], rnd()) * scale;
  const dbh = lerp(spec.dbh[0], spec.dbh[1], rnd()) * scale;
  // Crown diameter: the zone record's `width_m` when it carries one, because
  // that is the evidenced figure; the archetype ratio only when it does not.
  const spread = spec.crownW
    ? lerp(spec.crownW[0], spec.crownW[1], rnd()) * scale
    : h * spec.spreadK * (0.86 + rnd() * 0.30);
  const boleH = Math.max(0.4, h * spec.boleK);
  const crownBase = groundY + boleH * 0.72;
  const crownTop = groundY + h;
  const crownH = Math.max(0.6, crownTop - crownBase);

  const dark = linear(spec.dark);
  const light = linear(spec.light);
  // Bark takes the same appearance -> reflectance scaling as the foliage (see
  // CANOPY_ALBEDO), at its own value: a bole stands UNDER its own crown, so
  // almost none of it is ever in direct sun, but bark is a lighter material
  // than a shaded leaf mass and must not go to a silhouette.
  const bark = linear(spec.bark).map((v) => v * BARK_ALBEDO);
  // A second bark tone, for the one species whose record singles its bark out:
  // the sycamore's upper limbs are the pale half of "white mottled bark
  // flashing on the upper limbs", and the trunk under them is not. The tree was
  // already drawn as three colours' worth of wood — lower bole, upper bole,
  // limbs — so carrying the pale tone is a value, not a mesh. A species that
  // does not declare one is unchanged: `barkUpper` falls back to `bark`.
  // docs/LIBERTIES.md L118 owns the invention; ROADMAP K47.
  const barkUpper = spec.barkUpper != null
    ? linear(spec.barkUpper).map((v) => v * BARK_ALBEDO)
    : bark;
  // Fire-scarred boles: blackened to 1–2 m on 20–40 % of trees in the savanna.
  const scarred = spec.fireScar && rnd() < 0.32;
  const bole = scarred ? [bark[0] * 0.34, bark[1] * 0.32, bark[2] * 0.30] : bark;

  // A per-tree tint, so no two crowns are exactly the same green.
  const tint = 0.90 + rnd() * 0.20;
  const d2 = [dark[0] * tint, dark[1] * tint, dark[2] * tint];
  const l2 = [light[0] * tint, light[1] * tint, light[2] * tint];

  const leanA = rnd() * Math.PI * 2;
  const leanR = (spec.lean ?? 0) * (0.4 + rnd() * 0.6);
  const topX = x + Math.cos(leanA) * leanR * boleH;
  const topZ = z + Math.sin(leanA) * leanR * boleH;

  {
    const r0 = dbh * 0.62;
    const midY = groundY + boleH * 0.55;
    addStem(buf, x, groundY - 0.15, z,
      x + (topX - x) * 0.55, midY, z + (topZ - z) * 0.55,
      r0, r0 * 0.66, bole, 5, 0, 0.10, conf);
    addStem(buf, x + (topX - x) * 0.55, midY, z + (topZ - z) * 0.55,
      topX, groundY + boleH, topZ,
      r0 * 0.66, r0 * 0.46, barkUpper, 5, 0.10, 0.22, conf);
  }

  // Where the foliage masses sit. `open` spreads them wide and low, `gallery`
  // stacks them, `lean` throws them out over the water.
  const puffs = spec.puffs;
  const centres = [];
  for (let i = 0; i < puffs; i++) {
    const a = (i / puffs) * Math.PI * 2 + rnd() * 1.4;
    let rad;
    let hy;
    if (spec.form === 'open') {
      rad = (i === 0 ? 0.14 : 0.30 + rnd() * 0.24) * spread;
      hy = i === 0 ? 0.62 : 0.18 + rnd() * 0.62;
    } else {
      rad = (i === 0 ? 0.10 : 0.14 + rnd() * 0.22) * spread;
      hy = i === 0 ? 0.34 : 0.14 + rnd() * 0.84;
    }
    centres.push([
      topX + Math.cos(a) * rad,
      crownBase + crownH * hy,
      topZ + Math.sin(a) * rad,
      hy,
    ]);
  }

  // Limbs — the wood that carries the foliage.
  //
  // Round 1 gated this whole block on `form === 'open'`, so 91 % of the near
  // timber drew no limbs at all: crowns hung as plates in clear sky over a bare
  // pole, and daylight ran straight through the stand. That is the "colonnade"
  // the round-1 critique measured, and it is a drawing error rather than an
  // ecological one — every one of these species carries its crown on wood.
  {
    const r0 = dbh * 0.62;
    const openForm = spec.form === 'open';
    // An open-grown oak forks LOW into a few heavy, near-horizontal limbs — the
    // dossier's "signature of the 1835 Chicago horizon". A crowded gallery tree
    // is the other shape: it sheds a lighter limb at intervals up the whole
    // bole. Drawing both the same way is what made every species read alike.
    const stride = openForm ? 2 : 1;
    for (let i = openForm ? 1 : 0; i < centres.length; i += stride) {
      const c = centres[i];
      const fork = openForm ? 0.94 : lerp(0.58, 1.0, c[3]);
      const fx = x + (topX - x) * fork;
      const fz = z + (topZ - z) * fork;
      const fy = groundY + boleH * fork;
      // Stop the limb INSIDE the puff, so no tip pokes out of the foliage.
      const tip = openForm ? 0.82 : 0.76;
      addStem(buf, fx, fy, fz,
        lerp(fx, c[0], tip),
        lerp(fy, c[1], tip) - crownH * (openForm ? 0.12 : 0.04),
        lerp(fz, c[2], tip),
        r0 * (openForm ? 0.44 : 0.30), r0 * (openForm ? 0.20 : 0.11),
        barkUpper, 4, 0.20, 0.42, conf);
    }
  }

  for (const c of centres) {
    // The masses have to OVERLAP into one crown. Drawn small against a wide
    // scatter they read as a loose cloud of separate blobs with daylight
    // between them, which at town-edge range is the same "you can see straight
    // through the stand" failure the bare trunks were.
    const rad = spread * (spec.form === 'open' ? 0.255 : 0.245)
      * (0.72 + rnd() * 0.58);
    const squash = spec.form === 'open' ? 0.58 : 0.78;
    const flexBase = 0.42 + 0.44 * c[3];
    addPuff(buf, c[0], c[1], c[2], rad, squash, d2, l2, c[3], flexBase, rnd, conf);
  }

  // The flower, if the record carries one and July allows it. Drawn LAST so it
  // sits over the foliage it is carried on rather than being buried by a puff
  // added after it — the crown is opaque and merged, and there is no depth sort
  // inside one buffer to fix an ordering mistake here.
  //
  // Placement is on the outer SHELL: the record's `height_frac` picks the band
  // up the crown and `band` gives it depth, then each head is thrown out to
  // 0.72–1.0 of the crown radius at that height. A cluster at the centre of a
  // canopy is inside 12 m of leaves and is drawn for nobody.
  if (spec.head) {
    const head = spec.head;
    const n = Math.max(HEADS_MIN,
      Math.min(HEADS_MAX, Math.round(spread * head.perM)));
    const stretch = head.kind === 'catkin' ? 2.1 : 1.0;
    const colour = linear(head.rgb);
    // The crown radius at a given height, as an ellipsoid: widest at mid-crown,
    // closing at the cap. Without this the heads at `height_frac` 0.9 stand out
    // in clear air a metre off the foliage.
    const shellR = (t) => (spread * 0.5) * Math.sqrt(Math.max(0.08, 1 - Math.pow(2 * t - 1, 2)));
    for (let i = 0; i < n; i++) {
      const t = clamp01(head.frac - head.band * rnd());
      const a = (i / n) * Math.PI * 2 + rnd() * 1.1;
      const rr = shellR(t) * (0.72 + rnd() * 0.28);
      const hy = crownBase + crownH * t;
      const rad = lerp(head.size[0], head.size[1], rnd()) * 0.5;
      // Same self-shadowing law the foliage gets: high in the crown is lit,
      // low is interior. `t` is already that fraction.
      addHead(buf, topX + Math.cos(a) * rr, hy - (stretch > 1 ? rad * 1.4 : 0),
        topZ + Math.sin(a) * rr,
        rad, stretch, colour, Math.pow(clamp01(t), 1.5),
        0.42 + 0.44 * t, rnd, conf);
    }
    buf.heads += n;
  }
  return h;
}

/* -------------------------------------------------------------------------- */
/* the module                                                                  */
/* -------------------------------------------------------------------------- */

/**
 * @param {object} o
 * @param {URL} [o.dataBase]        where data/ lives (unused until the zone records land)
 * @param {object} o.terrain        what createTerrain() returned
 * @param {Array<{id:string, pts:number[][]}>} [o.footprints]
 * @param {object} [o.confidence]   the confidence view — every material goes through it
 * @param {string[]} [o.problems]   the shared collector
 * @param {boolean} [o.lowSpec]     true on touch/mobile: fewer stems, coarser band
 */
export async function createTrees({
  dataBase, terrain, footprints = [], growthBlocked = () => false,
  confidence = null, problems = [], lowSpec = false, detail = 'full',
  pixelsPerRadian = null,
} = {}) {
  const group = new THREE.Group();
  group.name = 'trees';
  // Placement stations are lightweight test observability: the release smoke
  // checks each against the authoritative water mask AND against the water
  // surface itself, which is stronger than a screenshot and cheaper than
  // reverse-engineering roots out of merged meshes. Each carries the ground
  // height the stem was actually built at, so the check is on the number the
  // renderer used rather than on one the test re-derives.
  group.userData.stations = [];

  const hf = terrain?.heightfield;
  const stats = {
    trees: 0, thickets: 0, drawCalls: 0, triangles: 0,
    communities: {}, species: {},
    horizonBodies: 0, horizonBins: 0, timberedBearingFraction: 0,
    horizonDrawnFraction: 0, horizonPxPerRad: 0,
    omitted: OMITTED_TIMBER.map((o) => ({
      ...o, elevation_deg: apparentTopDeg(o.canopy_m, o.distance_m, 1.68) + horizonDipDeg(1.68),
    })),
    zoneRecords: [], unimplementedForms: [], speciesFromRecord: 0,
    rejectedBelowWaterline: 0, lowestStationY: null,
    // ROADMAP K45(c). `headSpecies` is which records carry a July
    // inflorescence this file draws; `headStems` is how many stems actually
    // got one, which is the number that says whether the flower is IN the
    // scene rather than merely implemented.
    headSpecies: [], headStems: 0, heads: 0, headStations: [],
  };

  if (!hf?.loaded) {
    problems.push('trees: no heightfield, so no bank, no ridge and no division to '
      + 'place woody vegetation from — nothing planted');
    return { group, update() {}, stats, dispose() {} };
  }

  /* ---- 0. the ecology, from the dataset ---------------------------------- */

  // Missing or unparseable records draw NOTHING. There is no fallback community
  // here on purpose: AGENTS.md rule 2 is that a gap is recorded, never filled,
  // and a renderer that plants a forest when the dataset failed to load is
  // asserting an ecology nobody wrote down.
  let records;
  try {
    if (!dataBase) throw new Error('no dataBase');
    records = await loadTimberZones(dataBase, problems);
  } catch (err) {
    problems.push(`trees: the flora zone records did not load (${err.message}) — `
      + 'no woody vegetation placed');
    return { group, update() {}, stats, dispose() {} };
  }
  stats.zoneRecords = records.zonesRead;
  stats.unimplementedForms = records.unimplemented;
  stats.speciesFromRecord = Object.keys(records.specs).length;
  stats.headSpecies = records.heads;

  /** The render spec per species: the record's ecology over this file's forms. */
  const specs = {};
  for (const [id, base] of Object.entries(SPECIES)) {
    specs[id] = { ...base, conf: 0.5, crownW: null };
  }
  Object.assign(specs, records.specs);

  /**
   * The community mixes, weighted as they are written (ROADMAP K46).
   *
   * The record's band is the CONSTRAINT and not the value: a weight outside
   * every band its own community's `zones` record is an ecological claim no
   * source carries, so it must be declared in that community's `departures` or
   * this raises. `problems` is what the repo smoke reads to decide whether the
   * data loaded, which is the right severity — an undeclared departure means
   * the file and the dataset disagree and nothing says which is meant.
   */
  const mixes = {};
  for (const [key, c] of Object.entries(COMMUNITIES)) {
    const cited = c.zones ?? [];
    if (!cited.length) {
      problems.push(`trees: the community ${key} names no zones, so nothing constrains `
        + 'the weights it plants by');
    }
    const w = (list, listName) => list.filter(([id]) => specs[id]).map(([id, weight]) => {
      const seen = cited.map((z) => records.bands[z]?.[id]).filter(Boolean);
      const declared = c.departures?.[`${listName}.${id}`];
      if (!seen.length) {
        problems.push(`trees: ${key}.${listName}.${id} is weighted ${weight} and no zone `
          + `this community cites (${cited.join(', ')}) records a density for it`);
      } else if (!seen.some(([lo, hi]) => weight >= lo && weight <= hi)) {
        if (!declared) {
          problems.push(`trees: ${key}.${listName}.${id} is weighted ${weight}, outside `
            + `every band its own community's zones record (${seen
              .map(([lo, hi]) => `${lo}–${hi}`).join(', ')}) — declare it in `
            + `${key}.departures with the reason, or move it inside the band`);
        }
      } else if (declared) {
        // Exact the other way too. A departure that has been repaired leaves a
        // note behind claiming the file disagrees with the dataset when it no
        // longer does, and a stale declaration is how a gate stops meaning
        // anything.
        problems.push(`trees: ${key}.departures declares ${listName}.${id}, and its weight `
          + `${weight} is inside a band its own zones record — drop the declaration in the `
          + 'commit that brought it back inside');
      }
      return [id, weight];
    });
    mixes[key] = { mix: w(c.mix, 'mix'), edgeMix: c.edgeMix ? w(c.edgeMix, 'edgeMix') : null };
  }

  /* ---- 1. read the ground ------------------------------------------------ */

  const { cols, rows, cellM, originE, originN, data } = hf;
  const cells = cols * rows;

  // The water surface, read from the epoch's own heightfield record rather than
  // restated here: `water_surface_m` is what generators/terrain_gen.py wrote and
  // what the internal datum means. A renderer carrying its own copy of the datum
  // is how the two drift apart.
  const waterY = Number.isFinite(hf.meta?.water_surface_m) ? hf.meta.water_surface_m : 0;
  const dryFloorY = waterY + TREE_DRY_MARGIN_M;
  /**
   * The one question every stem must answer YES to. Sampled at the exact planting
   * point with the same bilinear sampler that supplies `groundY`, not at the
   * nearest cell centre: a 2.5 m cell is wider than a bank, so a nearest-cell
   * test can pass on the land side of a boundary the tree is then planted on the
   * water side of.
   */
  const standsDry = (e, n) => terrain.surfaceHeight(e, n) >= dryFloorY;

  // Distance from every cell to the nearest water, by two-pass chamfer. This is
  // the field the whole gallery depends on: ZONE 5 is defined as a band along
  // the bank, not as a polygon someone drew.
  const dw = new Float32Array(cells);
  const D1 = cellM;
  const D2 = cellM * Math.SQRT2;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i = r * cols + c;
      dw[i] = terrain.isWater(originE + c * cellM, originN + r * cellM) ? 0 : 1e9;
    }
  }
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i = r * cols + c;
      let v = dw[i];
      if (c > 0) v = Math.min(v, dw[i - 1] + D1);
      if (r > 0) v = Math.min(v, dw[i - cols] + D1);
      if (c > 0 && r > 0) v = Math.min(v, dw[i - cols - 1] + D2);
      if (c < cols - 1 && r > 0) v = Math.min(v, dw[i - cols + 1] + D2);
      dw[i] = v;
    }
  }
  for (let r = rows - 1; r >= 0; r--) {
    for (let c = cols - 1; c >= 0; c--) {
      const i = r * cols + c;
      let v = dw[i];
      if (c < cols - 1) v = Math.min(v, dw[i + 1] + D1);
      if (r < rows - 1) v = Math.min(v, dw[i + cols] + D1);
      if (c < cols - 1 && r < rows - 1) v = Math.min(v, dw[i + cols + 1] + D2);
      if (c > 0 && r < rows - 1) v = Math.min(v, dw[i + cols - 1] + D2);
      dw[i] = v;
    }
  }

  // The three land divisions, as connected components of land separated by the
  // navigable channels. Nobody draws a polygon: the river already divides the
  // box the way 1835 Chicago was divided, and the documented shallow slough on
  // the north side is above CHANNEL_Y so it does not cut the North Division.
  const div = new Int8Array(cells).fill(-1);
  const stack = new Int32Array(cells);
  let labels = 0;
  for (let s = 0; s < cells; s++) {
    if (data[s] < CHANNEL_Y || div[s] >= 0) continue;
    let sp = 0;
    stack[sp++] = s;
    div[s] = labels;
    while (sp > 0) {
      const j = stack[--sp];
      const c = j % cols;
      const r = (j - c) / cols;
      if (c > 0 && div[j - 1] < 0 && data[j - 1] >= CHANNEL_Y) { div[j - 1] = labels; stack[sp++] = j - 1; }
      if (c < cols - 1 && div[j + 1] < 0 && data[j + 1] >= CHANNEL_Y) { div[j + 1] = labels; stack[sp++] = j + 1; }
      if (r > 0 && div[j - cols] < 0 && data[j - cols] >= CHANNEL_Y) { div[j - cols] = labels; stack[sp++] = j - cols; }
      if (r < rows - 1 && div[j + cols] < 0 && data[j + cols] >= CHANNEL_Y) { div[j + cols] = labels; stack[sp++] = j + cols; }
    }
    labels++;
  }
  const cellAt = (e, n) => {
    const c = Math.round((e - originE) / cellM);
    const r = Math.round((n - originN) / cellM);
    if (c < 0 || r < 0 || c >= cols || r >= rows) return -1;
    return r * cols + c;
  };
  const WEST = div[cellAt(-300, 0)];
  const NORTH = div[cellAt(200, 250)];
  const SOUTH = div[cellAt(200, -250)];
  if (WEST < 0 || NORTH < 0 || SOUTH < 0 || WEST === NORTH || NORTH === SOUTH || WEST === SOUTH) {
    problems.push('trees: the heightfield no longer divides into the West, North and '
      + 'South Divisions, so which bank a point is on cannot be answered — nothing planted');
    return { group, update() {}, stats, dispose() {} };
  }

  /* ---- 2. where a tree may stand ---------------------------------------- */

  // Nothing grows through a building, and the blocks around one are being
  // cleared: ZONE 10 puts relict trees at 8–25/ha in the riverside blocks against
  // 30–80/ha in the untouched belt, so the town reads as timber being taken.
  const fps = footprints.map((f) => {
    let e = 0;
    let n = 0;
    for (const p of f.pts) { e += p[0]; n += p[1]; }
    return { pts: f.pts, e: e / f.pts.length, n: n / f.pts.length };
  });
  const CLEAR_MARGIN = 4.5;
  function blocked(e, n) {
    if (growthBlocked(e, n)) return true;
    for (const f of fps) {
      if (Math.abs(e - f.e) > 60 || Math.abs(n - f.n) > 60) continue;
      const pts = f.pts;
      let inside = false;
      for (let i = 0, j = pts.length - 1; i < pts.length; j = i++) {
        const [xi, yi] = pts[i];
        const [xj, yj] = pts[j];
        if ((yi > n) !== (yj > n) && e < ((xj - xi) * (n - yi)) / (yj - yi) + xi) inside = !inside;
        if (segDist2(e, n, xi, yi, xj, yj) < CLEAR_MARGIN * CLEAR_MARGIN) return true;
      }
      if (inside) return true;
    }
    return false;
  }
  function clearedFactor(e, n) {
    let f = 1;
    for (const p of fps) {
      const d = Math.hypot(e - p.e, n - p.n);
      f = Math.min(f, lerp(0.20, 1, smoothstep(50, 135, d)));
    }
    return f;
  }

  /**
   * Which community stands at (e, n), or null for ground that carries no woody
   * plant at all — which is most of the box, and is the point.
   */
  function communityAt(e, n) {
    const i = cellAt(e, n);
    if (i < 0) return null;
    const y = data[i];
    if (terrain.isWater(e, n)) return null;      // authoritative traced water mask
    if (!standsDry(e, n)) return null;           // and not on the waterline either
    const d = div[i];
    if (d === WEST) return null;                // Andreas: open prairie, entirely
    const bank = dw[i];

    // ZONE 5: an irregular gallery 30–120 m wide. The width wanders rather than
    // being a constant offset, because a gallery forest follows the floodplain
    // and floodplains are not parallel to the channel. The low half of the
    // documented range is used: this is the reach where the town was taking
    // timber, and a belt that reaches its 120 m maximum everywhere would put a
    // wall of trees across the "free and boundless prospect of open prairie"
    // Andreas describes from the south.
    const width = lerp(30, 74, noise2(e, n, 130, 11));
    if (bank <= width) return bank <= 16 ? 'gallery_edge' : 'gallery';

    // Behind the gallery: the West Division is out, and the South Division is
    // "low and marshy ground" with "a free and boundless prospect of open
    // prairie" beyond it — so only the North Division carries a body of timber.
    if (d !== NORTH) return null;

    // The ZONE 6 mosaic — "build as four sub-patches, not one texture", with
    // more than 30 % of the area at savanna density. A generated field lays it
    // out, nudged by what relief the heightfield has (the natural levee crest
    // against the backswamp behind it). It has very little: the whole North
    // Division sits inside 11 cm of itself, so the terrain cannot answer this
    // question, and a generated pattern that says so is better than a
    // terrain-derived one that pretends.
    const relief = clamp01((y - 1.02) / 0.16);
    const f = noise2(e, n, 96, 27) + (relief - 0.5) * 0.30;
    if (f > 0.66) return 'ridge_oak';
    if (f < 0.34) return 'mesic_pocket';
    return 'wet_woods';
  }

  /* ---- 3. plant ---------------------------------------------------------- */

  const rnd = mulberry32(18350701);
  const buffers = [new MeshBuf(), new MeshBuf(), new MeshBuf(), new MeshBuf()];
  const chunkOf = (e, n) => (e < 0 ? 0 : 1) + (n < 0 ? 0 : 2);

  // Scene detail sets how many stems are drawn and how coarsely the ground is
  // sampled for them. It does NOT touch the species mix, the zone rules or the
  // waterline margin: fewer of the same trees in the same places, never a
  // different wood. `lowSpec` is the device guess; an explicit choice outranks it.
  const level = lowSpec && detail === 'full' ? 'light' : detail;
  const STEMS = {
    full:     { step: 4.0, trees: 820, thickets: 420 },
    balanced: { step: 4.7, trees: 520, thickets: 270 },
    light:    { step: 5.6, trees: 300, thickets: 170 },
  };
  const stems = STEMS[level] ?? STEMS.full;
  const step = stems.step;
  const cellArea = step * step;
  const maxTrees = stems.trees;
  const maxThickets = stems.thickets;

  const pick = (mix, r) => {
    let total = 0;
    for (const m of mix) total += m[1];
    let t = r * total;
    for (const m of mix) { t -= m[1]; if (t <= 0) return m[0]; }
    return mix[mix.length - 1][0];
  };
  const bump = (obj, key) => { obj[key] = (obj[key] ?? 0) + 1; };
  /** Record a planted stem for the smoke suite, with the height it stands at. */
  const noteStation = (e, n, y) => {
    group.userData.stations.push({ e, n, y });
    if (stats.lowestStationY === null || y < stats.lowestStationY) stats.lowestStationY = y;
  };

  const half = 320 - step;
  for (let n = -half; n <= half; n += step) {
    for (let e = -half; e <= half; e += step) {
      const px = e + (rnd() - 0.5) * step * 0.92;
      const pz = n + (rnd() - 0.5) * step * 0.92;
      if (terrain.isWater(px, pz)) continue;
      // THE WATERLINE GATE, and it is deliberately the first thing after the
      // river mask and ahead of every ecological question below. `gy` is the
      // height the stem will actually be built at, so testing anything else here
      // — the nearest cell, the community's own idea of the bank — is testing a
      // different point from the one the tree stands on.
      const gy = terrain.surfaceHeight(px, pz);
      if (gy < dryFloorY) { stats.rejectedBelowWaterline++; continue; }
      const comm = communityAt(px, pz);
      if (!comm) continue;

      const i = cellAt(px, pz);
      const y = data[i];
      const bank = dw[i];

      // Sandbar willow: "thickets 2–6 stems/m² on point bars". Point bars are
      // the low, freshly worked ground between the waterline and about half a
      // metre above it — which the heightfield resolves as a 6–9 m strip.
      if (bank <= 9 && y <= 0.60) {
        if (stats.thickets >= maxThickets) continue;
        // Nearly every bar cell takes a stool. A sandbar-willow thicket is a
        // SCREEN, and a screen needs its clumps to touch: at a 4 m planting step
        // and a clump about 3 m across, thinning these to half was what left
        // them standing as separate cushions on open sand.
        if (rnd() > 0.84 || blocked(px, pz)) continue;
        addTree(buffers[chunkOf(px, pz)], specs.salix_interior, px, gy, pz, rnd,
          0.8 + rnd() * 0.5);
        noteStation(px, pz, gy);
        stats.thickets++;
        bump(stats.species, 'salix_interior');
        continue;
      }

      const key = comm === 'gallery_edge' ? 'gallery' : comm;
      const c = COMMUNITIES[key];
      // The gallery is not the same on both sides of the river. The North Side
      // is Andreas's "body of thrifty heavy growth of timber" and takes the top
      // of ZONE 5's 30–80/ha range; the South Water Street belt is the one being
      // cut for a town that has grown tenfold in two years, and takes the bottom.
      const range = key === 'gallery' && div[i] === NORTH ? [50, 78] : c.perHa;
      // A gallery forest does not stop at a line: it thins into the prairie it
      // is standing in. Without this the belt has a cut face, which is the
      // silhouette of a plantation and not of a floodplain wood.
      const edgeFade = key === 'gallery'
        ? 1 - smoothstep(0.5, 1.0, bank / lerp(30, 74, noise2(px, pz, 130, 11))) * 0.74
        : 1;
      const perHa = lerp(range[0], range[1], noise2(px, pz, 58, 7))
        * clearedFactor(px, pz) * edgeFade;
      if (rnd() > (perHa * cellArea) / 10000) continue;
      if (stats.trees >= maxTrees) continue;
      // A canopy tree needs its roots out of the channel; a bank willow does not.
      if (bank < 3.0 && comm !== 'gallery_edge') continue;
      if (blocked(px, pz)) continue;

      const m = mixes[key];
      const mix = comm === 'gallery_edge' && m.edgeMix ? m.edgeMix : m.mix;
      const id = pick(mix, rnd());
      const spec = specs[id];
      if (!spec) continue;
      addTree(buffers[chunkOf(px, pz)], spec, px, gy, pz, rnd);
      noteStation(px, pz, gy);
      stats.trees++;
      if (spec.head) {
        stats.headStems++;
        // Where the flowering stems actually stand. A layer that is implemented
        // and a layer a visitor can SEE are different claims, and this is the
        // only field that lets anything downstream tell them apart: the mesic
        // pocket is a minority community and its two flowering species are 14
        // stems of 159 (ROADMAP K45(c)).
        stats.headStations.push({ e: px, n: pz, id });
      }
      bump(stats.communities, key);
      bump(stats.species, id);
    }
  }

  /* ---- 4. the material --------------------------------------------------- */

  const uWind = { value: 0 };
  const nearMat = new THREE.MeshStandardMaterial({
    vertexColors: true, roughness: 0.94, metalness: 0,
  });
  nearMat.name = 'timber';
  {
    const prior = nearMat.onBeforeCompile;
    nearMat.onBeforeCompile = (shader, renderer) => {
      if (typeof prior === 'function') prior(shader, renderer);
      shader.uniforms.uWind = uWind;
      shader.vertexShader = `
attribute float aFlex;
uniform float uWind;
` + shader.vertexShader.replace('#include <begin_vertex>', /* glsl */`
#include <begin_vertex>
  {
    // Two crossing waves so a stand never sways in unison, keyed on world
    // position rather than on object position — there is one merged object per
    // quadrant, so anything keyed on the object would move a hundred trees as
    // one. Amplitude is a metre at most, on a 25 m crown: a 3 m/s breeze.
    vec3 chiW = (modelMatrix * vec4(transformed, 1.0)).xyz;
    float chiS = sin(uWind * 0.85 + chiW.x * 0.055 + chiW.z * 0.041) * 0.62
               + sin(uWind * 1.63 + chiW.x * 0.113 - chiW.z * 0.087) * 0.28;
    transformed.x += chiS * aFlex * 0.42;
    transformed.z += chiS * aFlex * 0.26;
  }
`);
    };
    nearMat.needsUpdate = true;
  }
  confidence?.patch(nearMat);

  const disposables = [nearMat];
  for (let i = 0; i < buffers.length; i++) {
    if (buffers[i].count === 0) continue;
    const geo = buffers[i].build();
    const mesh = new THREE.Mesh(geo, nearMat);
    mesh.name = `timber__q${i}`;
    // Timber that casts no shadow is pasted onto the ground rather than
    // standing on it, and a crown that receives none is lit from every side at
    // once — which is half of why round 1's crowns read as flat green balls.
    // The sun's shadow camera is only +/-60 m around the walker (world.js), so
    // this costs a shadow pass on the few stands actually near the visitor.
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);
    disposables.push(geo);
    stats.drawCalls++;
    stats.triangles += buffers[i].idx.length / 3;
  }
  for (const b of buffers) stats.heads += b.heads;

  /* ---- 5. the horizon ---------------------------------------------------- */

  const BINS = lowSpec ? 480 : 900;
  const binRad = (Math.PI * 2) / BINS;
  const topRad = new Float32Array(BINS);
  const binDist = new Float32Array(BINS);
  // The profile BEFORE the crown/gap modulation, kept so the gate can ask what
  // the modulation did rather than re-deriving the noise that drives it.
  const rawRad = new Float32Array(BINS);
  // Vertical pixels per radian, re-read from the live viewport each solve. The
  // band is the one thing in this file whose correctness is measured in pixels
  // rather than in metres, because what it draws is an angular silhouette.
  let pxPerRad = DEFAULT_PX_PER_RAD;
  const readPxPerRad = () => {
    const v = pixelsPerRadian?.();
    return Number.isFinite(v) && v > 0 ? v : DEFAULT_PX_PER_RAD;
  };
  const continuity = {
    bins: BINS, pxPerRad, covered: 0, resolvable: 0, drawn: 0,
    fraction: 0, worstResolvablePx: 0, minSilhouettePx: MIN_SILHOUETTE_PX,
  };

  const horizon = new THREE.Group();
  horizon.name = 'horizon-timber';
  const hPos = new Float32Array(BINS * 4 * 3);
  const hCol = new Float32Array(BINS * 4 * 3);
  const hIdx = new Uint32Array(BINS * 6);
  const hGeo = new THREE.BufferGeometry();
  hGeo.setAttribute('position', new THREE.BufferAttribute(hPos, 3).setUsage(THREE.DynamicDrawUsage));
  hGeo.setAttribute('color', new THREE.BufferAttribute(hCol, 3).setUsage(THREE.DynamicDrawUsage));
  hGeo.setAttribute('_confidence', new THREE.BufferAttribute(new Float32Array(BINS * 4).fill(0.5), 1));
  hGeo.setIndex(new THREE.BufferAttribute(hIdx, 1));
  hGeo.setDrawRange(0, 0);
  // The band is drawn as a ring around the camera; frustum culling a bounding
  // sphere that always contains the camera can only ever throw it away by
  // mistake, exactly as with the ground.
  hGeo.boundingSphere = new THREE.Sphere(new THREE.Vector3(), RING_RADIUS * 1.2);

  const farMat = new THREE.MeshBasicMaterial({ vertexColors: true, fog: false });
  farMat.name = 'horizon-timber';
  // Authored in display space against the rendered sky, so it must not be tone
  // mapped a second time. See the header: this band opts out of the scene fog.
  farMat.toneMapped = false;
  confidence?.patch(farMat);
  const hMesh = new THREE.Mesh(hGeo, farMat);
  hMesh.name = 'horizon-timber';
  hMesh.frustumCulled = false;
  hMesh.renderOrder = -1;
  horizon.add(hMesh);
  group.add(horizon);
  disposables.push(hGeo, farMat);

  const haze = hazeDisplayLinear();
  const timber = linear(TIMBER_SRGB);

  /** Solve the band for an eye at (e, n, eyeY) and write it into the buffers. */
  function solveHorizon(camE, camN, eyeY) {
    topRad.fill(-1);
    binDist.fill(0);
    rawRad.fill(0);
    pxPerRad = readPxPerRad();

    for (const body of FAR_TIMBER) {
      const path = body.path;
      for (let s = 0; s < path.length - 1; s++) {
        const [ax, ay] = path[s];
        const [bx, by] = path[s + 1];
        const segLen = Math.hypot(bx - ax, by - ay);
        let t = 0;
        while (t <= segLen) {
          const f = segLen > 0 ? t / segLen : 0;
          const pe = ax + (bx - ax) * f;
          const pn = ay + (by - ay) * f;
          const dx = pe - camE;
          const dn = pn - camN;
          const d = Math.hypot(dx, dn);
          // Adaptive: a body four kilometres out does not need a sample every
          // twenty metres, and a body four hundred metres out does.
          const stepM = Math.max(16, d * 0.030);
          t += stepM;
          if (d < MIN_FAR_M) continue;

          const bearing = Math.atan2(dx, dn);
          const hgt = lerp(body.canopy[0], body.canopy[1],
            noise1((bearing * d) / 55, 3));
          const theta = (hgt - eyeY) / d - d / (2 * R_EFF);
          if (theta <= 0) continue;
          const halfAng = (stepM * 0.5 + body.crown * 0.5) / d;
          const lo = Math.floor((bearing - halfAng) / binRad);
          const hi = Math.ceil((bearing + halfAng) / binRad);
          for (let k = lo; k <= hi; k++) {
            const b = ((k % BINS) + BINS) % BINS;
            if (theta > topRad[b]) { topRad[b] = theta; binDist[b] = d; }
          }
        }
      }
    }

    // Break the profile up crown by crown, measured in METRES along the
    // treeline rather than in degrees, so the bumps stay crown-sized whether
    // the timber is four hundred metres away or four kilometres.
    let timbered = 0;
    let resolvable = 0;
    let drawn = 0;
    let worstResolvablePx = Infinity;
    for (let b = 0; b < BINS; b++) {
      if (topRad[b] <= 0) { topRad[b] = 0; continue; }
      timbered++;
      rawRad[b] = topRad[b];
      const rawPx = topRad[b] * pxPerRad;
      const d = binDist[b];
      const bearing = (b + 0.5) * binRad;
      const u = (bearing * d) / 15;
      const crownN = noise1(u, 5) * 0.28 + noise1(u * 2.6, 9) * 0.24
        + noise1(u * 6.4, 17) * 0.26 + noise1(u * 13.1, 23) * 0.22;
      const gapN = noise1(u / 6, 13);
      let k = 0.40 + crownN * 0.60;
      // Sky through the stand. A treeline read from the prairie is holed, not
      // solid — without this the band is a silhouette with one outline, which
      // on a flat plain reads as a distant RIDGE and there are no ridges here.
      if (gapN < 0.40) k *= lerp(0.05, 0.92, gapN / 0.40);
      // ...but a hole the frame cannot resolve is not sky through a stand, it
      // is the stand deleted. The modulation may cut a bearing to
      // MIN_SILHOUETTE_PX and no further; where the raw crown is already under
      // that it is suppressed outright (kFloor reaches 1). This is a floor on
      // the RESULT rather than a cap on `k`, so it binds exactly where the
      // pixels are scarce and nowhere else — the near treelines keep their
      // gaps to the last per cent.
      const kFloor = Math.min(1, MIN_SILHOUETTE_PX / Math.max(rawPx, 1e-6));
      if (k < kFloor) k = kFloor;
      topRad[b] = topRad[b] * k;
      const px = topRad[b] * pxPerRad;
      if (rawPx >= MIN_SILHOUETTE_PX) {
        resolvable++;
        if (px < worstResolvablePx) worstResolvablePx = px;
      }
      if (px >= MIN_SILHOUETTE_PX - 1e-6) drawn++;
      if (topRad[b] <= 1e-5) topRad[b] = 0;
    }
    continuity.pxPerRad = pxPerRad;
    continuity.covered = timbered;
    continuity.resolvable = resolvable;
    continuity.drawn = drawn;
    continuity.fraction = resolvable > 0 ? drawn / resolvable : 0;
    continuity.worstResolvablePx = Number.isFinite(worstResolvablePx) ? worstResolvablePx : 0;

    // Emit each contiguous run of timbered bearings as ONE strip, with the
    // profile carried on shared vertices. Quad-per-bin looks like a staircase:
    // at four hundred metres a bin is six pixels wide and eight tall, and a
    // flat-topped six-pixel block reads as a distant BUILDING, not as a tree.
    let verts = 0;
    let indices = 0;
    const footTheta = RING_FOOT_M / RING_RADIUS;
    const y0 = RING_RADIUS * footTheta;
    const putVert = (ang, theta, d) => {
      const sx = Math.sin(ang) * RING_RADIUS;
      const sz = -Math.cos(ang) * RING_RADIUS;
      const mixTop = hazeAt(d);
      // The foot of a treeline is a shade deeper than its crowns, never paler:
      // haze applies to both equally and the trunk zone is in its own shadow.
      const mixBot = mixTop * 0.94;
      const i0 = verts * 3;
      hPos[i0] = sx; hPos[i0 + 1] = y0; hPos[i0 + 2] = sz;
      hCol[i0] = lerp(timber[0], haze[0], mixBot);
      hCol[i0 + 1] = lerp(timber[1], haze[1], mixBot);
      hCol[i0 + 2] = lerp(timber[2], haze[2], mixBot);
      verts++;
      const i1 = verts * 3;
      hPos[i1] = sx; hPos[i1 + 1] = RING_RADIUS * Math.tan(theta); hPos[i1 + 2] = sz;
      hCol[i1] = lerp(timber[0], haze[0], mixTop);
      hCol[i1 + 1] = lerp(timber[1], haze[1], mixTop);
      hCol[i1 + 2] = lerp(timber[2], haze[2], mixTop);
      verts++;
    };

    let b = 0;
    // Start on a bearing that has no timber, so a run that wraps past north is
    // not cut in half by the seam.
    let start = 0;
    while (start < BINS && topRad[start] > 0) start++;
    if (start >= BINS) start = 0;
    while (b < BINS) {
      const idx = (start + b) % BINS;
      if (topRad[idx] <= 0) { b++; continue; }
      let len = 0;
      while (b + len < BINS && topRad[(start + b + len) % BINS] > 0) len++;
      if (verts + 2 * (len + 1) > BINS * 4) break;

      const first = verts;
      for (let j = 0; j <= len; j++) {
        const left = (start + b + j - 1 + BINS) % BINS;
        const right = (start + b + j) % BINS;
        const tl = j === 0 ? 0 : topRad[left];
        const tr = j === len ? 0 : topRad[right];
        // A run ends in its outermost CROWN, at nearly full height. Tapering
        // the ends to the ground instead draws a smooth dome, and a smooth dome
        // on a lake-plain horizon reads as a hill — there are no hills here, so
        // that silhouette is a geological claim the sources flatly contradict.
        const theta = j === 0 ? tr * 0.88 : j === len ? tl * 0.88 : (tl + tr) * 0.5;
        const d = j === len ? binDist[left] : binDist[right];
        putVert((start + b + j) * binRad, Math.max(theta, 1e-5), d);
      }
      // Wound so the INSIDE of the ring faces the camera at its centre. The
      // other winding is silently invisible — a back-faced band culls away and
      // leaves an empty horizon that looks exactly like an honest one.
      for (let j = 0; j < len; j++) {
        const q = first + j * 2;
        hIdx[indices++] = q; hIdx[indices++] = q + 2; hIdx[indices++] = q + 1;
        hIdx[indices++] = q + 1; hIdx[indices++] = q + 2; hIdx[indices++] = q + 3;
      }
      b += len;
    }

    hGeo.attributes.position.needsUpdate = true;
    hGeo.attributes.color.needsUpdate = true;
    hGeo.index.needsUpdate = true;
    hGeo.setDrawRange(0, indices);
    stats.horizonBins = timbered;
    stats.timberedBearingFraction = timbered / BINS;
    stats.horizonDrawnFraction = continuity.fraction;
    stats.horizonPxPerRad = pxPerRad;
    stats.triangles = stats.triangles - (stats.horizonTriangles ?? 0) + indices / 3;
    stats.horizonTriangles = indices / 3;
  }

  stats.horizonBodies = FAR_TIMBER.length;
  stats.drawCalls++;
  solveHorizon(0, 0, 2.7);

  /* ---- 6. the frame ------------------------------------------------------ */

  let wind = 0;
  let lastE = Infinity;
  let lastN = Infinity;
  let lastY = Infinity;

  return {
    group,
    /** The far-timber table, so a test can assert what is on the horizon. */
    farTimber: FAR_TIMBER,
    omitted: OMITTED_TIMBER,
    stats,

    /**
     * What the crown/gap modulation did to the silhouette, in the band's own
     * terms — asked of the solver rather than re-derived from its noise.
     *
     * `covered` is the bearings a timber body reaches at all; `resolvable`
     * those whose unmodulated crown is at least one pixel of THIS viewport;
     * `drawn` those the modulation leaves at a pixel or more. The fraction is
     * drawn/resolvable, because a body whose raw silhouette is already
     * sub-pixel — a 20 m canopy at 9.7 km is 0.7 px on a phone — cannot be
     * made visible by any choice this function has, and counting it as a
     * failure would only invite the floor to be raised until it lies.
     */
    horizonContinuity() {
      return { ...continuity };
    },

    /**
     * The sRGB the band's fully-hazed end displays at, so the gate can compare
     * it against `scene.fog.color` — the two must be the same colour, and were
     * 16 red and 12 green apart until 2026-08-13.
     */
    hazeTargetHex() {
      const c = new THREE.Color().setRGB(haze[0], haze[1], haze[2]);
      return c.getHex(THREE.SRGBColorSpace);
    },

    update(dt, camera) {
      wind += (dt || 0);
      uWind.value = wind;
      if (!camera) return;
      const p = camera.position;
      horizon.position.set(p.x, p.y, p.z);
      const e = p.x;
      const n = -p.z;
      // A viewport change moves the pixel the floor is measured in, so it is a
      // reason to re-solve exactly as walking is. 2 % keeps a drag-resize from
      // re-solving every frame.
      const pxNow = readPxPerRad();
      if (Math.abs(e - lastE) > RING_REBUILD_M || Math.abs(n - lastN) > RING_REBUILD_M
        || Math.abs(p.y - lastY) > 0.30 || Math.abs(pxNow - pxPerRad) > pxPerRad * 0.02) {
        lastE = e; lastN = n; lastY = p.y;
        solveHorizon(e, n, p.y);
      }
    },

    dispose() {
      for (const d of disposables) d?.dispose?.();
    },
  };
}

/** How far a canopy top at `d` metres stands above a level line of sight. */
function apparentTopDeg(canopyM, d, eyeY) {
  return ((canopyM - eyeY) / d - d / (2 * R_EFF)) * 180 / Math.PI;
}
/** How far the visible horizon sits below a level line of sight, in degrees. */
function horizonDipDeg(eyeY) {
  return Math.sqrt((2 * eyeY) / R_EFF) * 180 / Math.PI;
}

export { SPECIES, COMMUNITIES, FAR_TIMBER, OMITTED_TIMBER };
