import { Color3 } from '@babylonjs/core/Maths/math.color';

/**
 * The calibrated Old Joliet Prison palette.
 *
 * Every value here is read off reference photography of the real site (see
 * docs/RESEARCH.md § Material & colour palette). Nothing in the game is
 * allowed to invent a base colour — scenes compose from this file so that
 * eight different scenes still read as one building.
 *
 * Values are sRGB hex as observed under overcast daylight. The renderer works
 * in linear space, so always go through `srgb()` rather than
 * `Color3.FromHexString`, which does not de-gamma.
 */

/** Convert an sRGB hex string to a linear-space Color3. */
export function srgb(hex: string): Color3 {
  const c = Color3.FromHexString(hex);
  return new Color3(Math.pow(c.r, 2.2), Math.pow(c.g, 2.2), Math.pow(c.b, 2.2));
}

export const HEX = {
  // ---- Exterior limestone (Joliet/Lemont dolomitic "Athens marble") --------
  /** Sunlit rock-face block, warm buff-gold. */
  limestoneWarm: '#c9ad74',
  /** The lighter, more bleached ashlar found on tower shafts. */
  limestonePale: '#d6be8c',
  /** Cooler grey-buff blocks that speckle the coursing. */
  limestoneCool: '#b7b2a0',
  /** Weathered base course and water-runnel streaking, near-black green. */
  limestoneWeathered: '#6e6a5e',
  /** Deepest soot/organic staining at grade. */
  limestoneSoot: '#413f3a',

  // ---- Interior masonry ---------------------------------------------------
  /** Glazed structural tile / painted CMU corridor walls. */
  blockCream: '#d8d2be',
  /** Grey-painted lower band (dado) common in the shops and admin rooms. */
  blockDadoGrey: '#8d9295',
  /** Raw exposed concrete block behind failed paint. */
  blockRaw: '#a09a90',

  // ---- Paint stratigraphy (cell interiors) --------------------------------
  // Topcoat delaminates to reveal these in order. Drives the flaking-paint
  // material's layer stack.
  paintTopCream: '#e4dcc4',
  paintMustard: '#d6a32b',
  paintBlueGrey: '#9fb0b5',
  paintSage: '#b6b49a',

  // ---- Steel --------------------------------------------------------------
  /** Cell-front and gang-door oxide brown. */
  steelOxideBrown: '#6b4437',
  /** Active orange rust bloom. */
  rustOrange: '#8a5a32',
  /** Bright fresh rust in runnels. */
  rustBright: '#a8623a',
  /** Institutional red-oxide door enamel (Machine Shop, service gates). */
  doorRedOxide: '#b5424a',
  /** Grey primer showing through chipped enamel. */
  primerGrey: '#7d7b76',
  /** Galvanised chain-link and conduit. */
  galvanised: '#9aa0a2',

  // ---- Floors -------------------------------------------------------------
  /** Cell-house corridor concrete, polished pale grey-tan by foot traffic. */
  concreteWorn: '#b4ab99',
  /** Newer/darker slab in the shops. */
  concreteCool: '#8f8d88',
  /** Dining-hall terrazzo. */
  terrazzo: '#c6c0b2',
  /** Cracked exterior asphalt. */
  asphalt: '#4a4845',

  // ---- Dining hall 1970s decorative band ----------------------------------
  bandBrown: '#8a5a32',
  bandOrange: '#d98a3c',
  bandTan: '#c19a63',
  bandCream: '#efe9dc',
  /** Fixed-stool fibreglass seats. */
  stoolOrange: '#e2582a',

  // ---- Organic / decay ----------------------------------------------------
  mossGreen: '#5c6b3f',
  lawnGreen: '#6f8348',
  /** Cottonwood/poplar saplings growing through the shop floors. */
  saplingGreen: '#7d9455',
  guano: '#cfc9bb',
  /** Charred roof timber in the burned industrial shops. */
  charredTimber: '#2a2521',
  rottenTimber: '#6a5540',
  /** Standing water in the siphon and basements. */
  waterMurk: '#2b3230',

  // ---- Night lighting -----------------------------------------------------
  /** Moonlight key. Cool but not cartoon-blue. */
  moonlight: '#8fa6c4',
  /** Sodium-vapour yard lights on the surviving poles. */
  sodiumVapour: '#ffb765',
  /** The crew's headlamps — a warm-neutral LED, slightly green like real ones. */
  headlamp: '#fff2d6',
  /** Restored powerhouse incandescent string lights. */
  incandescent: '#ffc98a',
  /** Jsn's camera / scan UI accent. */
  scanCyan: '#5fe3d6',
} as const;

export type PaletteKey = keyof typeof HEX;

/** Linear-space Color3 for every palette entry, built once at module load. */
export const C = Object.fromEntries(
  Object.entries(HEX).map(([k, v]) => [k, srgb(v)]),
) as Record<PaletteKey, Color3>;
