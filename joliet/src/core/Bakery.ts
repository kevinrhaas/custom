import { Scene } from '@babylonjs/core/scene';
import { RawTexture } from '@babylonjs/core/Materials/Textures/rawTexture';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { Engine } from '@babylonjs/core/Engines/engine';

import {
  fbm,
  worley,
  coursedStone,
  smoothstep,
  clamp01,
  hexToRgb,
  mixRgb,
  heightToNormal,
  hash2,
} from './Noise';
import { HEX } from './Palette';

/**
 * The procedural texture bakery.
 *
 * Every surface in this game is authored here rather than shipped as a photo
 * scan. Three reasons, in order of importance:
 *
 *  1. **Wear follows geometry.** A baked-in photo of a weathered wall puts the
 *     staining wherever the photographer's wall had it. Generated maps let the
 *     runoff streaks start at the cap rail and the biological blotching sit in
 *     the sheltered courses, which is what the reference actually shows.
 *  2. **No tiling.** Maps are baked seamless and the shader breaks up
 *     repetition with a second, much larger-scale modulation.
 *  3. **Budget.** The whole texture set costs a few hundred KB of code instead
 *     of 80 MB of downloads, which buys back the entire load-time budget.
 *
 * Baking happens once at load into RawTextures. A 1024² albedo+normal+ORM set
 * costs roughly 12 ms to generate, so the full library is well under a second
 * and runs while the loading screen is up.
 */

export interface BakedSet {
  albedo: Texture;
  normal: Texture;
  /** Packed: R = ambient occlusion, G = roughness, B = metallic. */
  orm: Texture;
}

/**
 * Bake resolution.
 *
 * 512² is a deliberate choice, not a compromise. Baking 18 material sets at
 * 1024² is tens of seconds of single-threaded JS — it blew the 15 s
 * time-to-playable budget on its own. At 512² the whole library bakes in a few
 * seconds, and the close-up frequency that the extra resolution would have
 * bought is recovered far more cheaply by the shared detail-normal overlay in
 * Materials.ts, which runs at ~12× tiling and never repeats visibly.
 */
const SIZE = 512;

function makeTexture(
  scene: Scene,
  data: Uint8ClampedArray,
  size: number,
  name: string,
  srgb: boolean,
): Texture {
  const tex = RawTexture.CreateRGBATexture(
    new Uint8Array(data.buffer),
    size,
    size,
    scene,
    true, // generate mipmaps
    false,
    Texture.TRILINEAR_SAMPLINGMODE,
    Engine.TEXTURETYPE_UNSIGNED_BYTE,
  );
  tex.name = name;
  tex.wrapU = Texture.WRAP_ADDRESSMODE;
  tex.wrapV = Texture.WRAP_ADDRESSMODE;
  tex.anisotropicFilteringLevel = 16;
  // Albedo is authored in sRGB; normal and ORM are data and must stay linear.
  (tex as Texture & { gammaSpace: boolean }).gammaSpace = srgb;
  return tex;
}

/* ========================================================================== */
/*  Joliet limestone — the signature material                                 */
/* ========================================================================== */

export interface LimestoneOptions {
  /** Courses visible across one tile. Perimeter wall ~7, tower ashlar ~11. */
  courses?: number;
  /** 0 = crisp ashlar, 1 = heavy quarry-faced rustication. */
  rustication?: number;
  /** 0..1 amount of black biological/soot blotching. */
  soiling?: number;
  /** 0..1 downward runoff streaking from the cap. */
  runoff?: number;
  /** 0..1 wetness. Darkens and smooths. */
  wetness?: number;
  seed?: number;
}

/**
 * The wall in the reference photographs is *not* a uniform gold. It is a mix
 * of pale cream, warm gold and cool grey blocks in irregular courses, with
 * black blotching concentrated in bands and heavy dark staining at the base.
 * Getting that per-block colour variance right is most of the realism.
 */
export function bakeLimestone(scene: Scene, opts: LimestoneOptions = {}): BakedSet {
  const {
    courses = 7,
    rustication = 0.85,
    soiling = 0.5,
    runoff = 0.45,
    wetness = 0,
    seed = 1858, // the year they broke ground
  } = opts;

  const albedo = new Uint8ClampedArray(SIZE * SIZE * 4);
  const orm = new Uint8ClampedArray(SIZE * SIZE * 4);
  const height = new Float32Array(SIZE * SIZE);

  const warm = hexToRgb(HEX.limestoneWarm);
  const pale = hexToRgb(HEX.limestonePale);
  const cool = hexToRgb(HEX.limestoneCool);
  const weathered = hexToRgb(HEX.limestoneWeathered);
  const soot = hexToRgb(HEX.limestoneSoot);

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = x / SIZE;
      const v = y / SIZE;
      const i = (y * SIZE + x) * 4;

      const stone = coursedStone(u, v, courses, seed);

      // --- Per-block base colour ---------------------------------------
      // Three-way blend driven by the block id. Real coursed limestone has
      // blocks from different beds of the quarry side by side.
      const t = stone.id;
      let rgb =
        t < 0.42
          ? mixRgb(warm, pale, t / 0.42)
          : t < 0.78
            ? mixRgb(pale, warm, (t - 0.42) / 0.36)
            : mixRgb(warm, cool, (t - 0.78) / 0.22);

      // --- Quarry-face relief -------------------------------------------
      // Rock-faced blocks are convex, roughest at the centre, pinched at the
      // edges where the mason squared the margin.
      const edgeU = Math.min(stone.bu, 1 - stone.bu);
      const edgeV = Math.min(stone.bv, 1 - stone.bv);
      const margin = smoothstep(0.0, 0.16, Math.min(edgeU, edgeV));
      const faceNoise = fbm(u * 26, v * 26, 26, 4, seed + stone.id * 1000);
      const chunk = worley(u * 1.9, v * 1.9, 22, seed + 41);
      const relief =
        margin * rustication * (faceNoise * 0.62 + (1 - chunk.f1) * 0.38) +
        (1 - margin) * 0.18;

      // Fine bedding lamination — dolomitic limestone splits in layers.
      const bedding = fbm(u * 5, v * 96, 96, 2, seed + 7) * 0.06;

      // Rock-faced blocks stand well proud of the joint plane — this is the
      // difference between "quarried limestone" and "brick".
      let h = relief * 1.25 + bedding;

      // --- Joints --------------------------------------------------------
      // Raked mortar sits well back and is a cooler, greyer colour.
      const jointMask = 1 - stone.joint;
      if (jointMask > 0) {
        h -= jointMask * 0.42;
        rgb = mixRgb(rgb, [150, 146, 136], jointMask * 0.72);
      }

      // --- Value variation within a block --------------------------------
      const grain = fbm(u * 64, v * 64, 64, 3, seed + 19);
      rgb = mixRgb(rgb, mixRgb(rgb, pale, 0.55), grain * 0.7);

      // --- Biological / soot blotching ------------------------------------
      // In the reference this is patchy and *dark*, sitting on the rougher
      // faces and under the corbels rather than spread evenly.
      const blot = fbm(u * 7, v * 9, 9, 4, seed + 233);
      const blotMask = smoothstep(0.44, 0.70, blot) * soiling;
      rgb = mixRgb(rgb, soot, blotMask * 0.82);

      // --- Vertical runoff -------------------------------------------------
      // Streaks originate at the top of the tile (the cap rail) and fade with
      // depth, with a strong horizontal high-frequency break-up.
      const streakSeed = fbm(u * 140, 0.5, 140, 2, seed + 555);
      const streakMask =
        smoothstep(0.30, 0.78, streakSeed) *
        smoothstep(1.0, 0.15, v) *
        runoff;
      rgb = mixRgb(rgb, weathered, streakMask * 0.62);
      // Runoff also sits in the joints, so darken there harder.
      rgb = mixRgb(rgb, weathered, streakMask * jointMask * 0.5);

      // --- Base-course darkening -------------------------------------------
      const base = smoothstep(0.86, 1.0, v) * 0.55;
      rgb = mixRgb(rgb, weathered, base);

      // --- Efflorescence (salt bloom) --------------------------------------
      const eff = fbm(u * 17, v * 21, 21, 3, seed + 881);
      const effMask = smoothstep(0.72, 0.88, eff) * (1 - blotMask) * 0.4;
      rgb = mixRgb(rgb, [232, 228, 216], effMask);

      height[y * SIZE + x] = h;

      albedo[i] = rgb[0];
      albedo[i + 1] = rgb[1];
      albedo[i + 2] = rgb[2];
      albedo[i + 3] = 255;

      // --- ORM --------------------------------------------------------------
      // Cavity AO from the joints and the relief.
      const ao = clamp01(1 - jointMask * 0.75 - (1 - relief) * 0.16);
      // Rough stone, but the soiled and wet areas are smoother — organic film
      // and water both fill the micro-surface.
      let rough = 0.93 - grain * 0.1 - blotMask * 0.12;
      rough = rough * (1 - wetness * 0.55);
      // Joints are rougher than the faces.
      rough = clamp01(rough + jointMask * 0.05);

      orm[i] = ao * 255;
      orm[i + 1] = rough * 255;
      orm[i + 2] = 0; // limestone is a dielectric
      orm[i + 3] = 255;
    }
  }

  const normal = heightToNormal(height, SIZE, 4.4);

  return {
    albedo: makeTexture(scene, albedo, SIZE, 'limestone_albedo', true),
    normal: makeTexture(scene, normal, SIZE, 'limestone_normal', false),
    orm: makeTexture(scene, orm, SIZE, 'limestone_orm', false),
  };
}

/* ========================================================================== */
/*  Flaking institutional paint over concrete block                           */
/* ========================================================================== */

export interface FlakingPaintOptions {
  /** 0..1 how far the delamination has progressed. */
  decay?: number;
  /** Blocks across the tile. CMU at 16"×8" reads ~6 across a 2.4 m tile. */
  blocksX?: number;
  blocksY?: number;
  /** Topcoat colour. Defaults to the cell-interior cream. */
  topcoat?: string;
  /** Layers revealed underneath, outermost first. */
  strata?: string[];
  seed?: number;
}

/**
 * The cell-interior paint in the reference is spectacular: a cream topcoat
 * curling away in hard-edged islands to reveal mustard yellow, then a pale
 * blue-grey, then bare block. The key detail is that the flakes have *lifted
 * edges* — they catch light along the boundary — and that the exposed layers
 * form nested, not random, regions.
 */
export function bakeFlakingPaint(scene: Scene, opts: FlakingPaintOptions = {}): BakedSet {
  const {
    decay = 0.55,
    blocksX = 6,
    blocksY = 12,
    topcoat = HEX.paintTopCream,
    strata = [HEX.paintMustard, HEX.paintBlueGrey, HEX.paintSage],
    seed = 1948,
  } = opts;

  const albedo = new Uint8ClampedArray(SIZE * SIZE * 4);
  const orm = new Uint8ClampedArray(SIZE * SIZE * 4);
  const height = new Float32Array(SIZE * SIZE);

  const top = hexToRgb(topcoat);
  const layers = strata.map(hexToRgb);
  const substrate = hexToRgb(HEX.blockRaw);

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = x / SIZE;
      const v = y / SIZE;
      const i = (y * SIZE + x) * 4;

      // --- Concrete block substrate ---------------------------------------
      const bx = u * blocksX;
      const by = v * blocksY;
      const bi = Math.floor(bx);
      const bj = Math.floor(by);
      // Running bond: every other course offsets by half a block.
      const stagger = bj % 2 === 0 ? 0 : 0.5;
      const sx = (u * blocksX + stagger) % 1;
      const sy = by % 1;
      const jointW = 0.045;
      const jointMask =
        1 -
        Math.min(
          smoothstep(0, jointW, Math.min(sx, 1 - sx)),
          smoothstep(0, jointW * 2, Math.min(sy, 1 - sy)),
        );

      // CMU face is a coarse aggregate speckle.
      const aggregate = fbm(u * 220, v * 220, 220, 3, seed + 3);
      let h = -jointMask * 0.3 + aggregate * 0.05;

      // --- Delamination field ---------------------------------------------
      // Nested thresholds on one smooth field give concentric strata, which is
      // exactly how successive paint layers fail.
      const field =
        fbm(u * 9, v * 9, 9, 5, seed + 71) * 0.65 +
        fbm(u * 34, v * 34, 34, 3, seed + 131) * 0.35;

      // Failure concentrates where water gets in: high on the wall and in the
      // joints.
      const bias = (1 - v) * 0.16 + jointMask * 0.1;
      const d = field + bias;

      // Threshold ladder. `decay` slides the whole ladder.
      const t0 = 0.72 - decay * 0.34; // topcoat gone
      const step = 0.1;

      let rgb: [number, number, number];
      let exposedLayer = -1;
      if (d < t0) {
        rgb = top;
      } else {
        exposedLayer = Math.min(layers.length, Math.floor((d - t0) / step));
        rgb = exposedLayer >= layers.length ? substrate : layers[exposedLayer];
      }

      // --- Lifted flake edges ----------------------------------------------
      // Within a narrow band of each threshold, raise the height and lighten:
      // that is the curled edge catching the light.
      let edgeLift = 0;
      const bandWidth = 0.014;
      for (let L = 0; L <= layers.length; L++) {
        const thresh = t0 + L * step;
        const dist = Math.abs(d - thresh);
        if (dist < bandWidth) {
          const e = 1 - dist / bandWidth;
          edgeLift = Math.max(edgeLift, e);
        }
      }
      if (edgeLift > 0) {
        h += edgeLift * 0.5;
        rgb = mixRgb(rgb, [255, 252, 244], edgeLift * 0.28);
      }

      // Intact paint sits proud of the exposed layers — each lost layer is a
      // step down. That micro-relief is what makes it read as paint and not a
      // printed pattern.
      const layerDepth = exposedLayer < 0 ? 0 : (exposedLayer + 1) * 0.055;
      h -= layerDepth;

      // Paint is not flat: it has brush texture and sags.
      const brush = fbm(u * 48, v * 150, 150, 2, seed + 401);
      if (exposedLayer < 0) h += brush * 0.045;

      // --- Grime -------------------------------------------------------------
      const grime = fbm(u * 6, v * 11, 11, 4, seed + 909);
      const grimeMask = smoothstep(0.5, 0.82, grime) * 0.34 + smoothstep(0.75, 1, v) * 0.3;
      rgb = mixRgb(rgb, [72, 66, 58], grimeMask * 0.6);
      // Joints hold dirt.
      rgb = mixRgb(rgb, [88, 82, 74], jointMask * 0.45);

      height[y * SIZE + x] = h;

      albedo[i] = rgb[0];
      albedo[i + 1] = rgb[1];
      albedo[i + 2] = rgb[2];
      albedo[i + 3] = 255;

      // Intact enamel is semi-gloss; exposed block and old chalked layers are
      // matte. That roughness *contrast* is a huge part of the read.
      const rough =
        exposedLayer < 0
          ? 0.42 + brush * 0.12
          : exposedLayer >= layers.length
            ? 0.94
            : 0.62 + exposedLayer * 0.1;
      const ao = clamp01(1 - jointMask * 0.6 - layerDepth * 1.2 - grimeMask * 0.15);

      orm[i] = ao * 255;
      orm[i + 1] = clamp01(rough - edgeLift * 0.1) * 255;
      orm[i + 2] = 0;
      orm[i + 3] = 255;
    }
  }

  const normal = heightToNormal(height, SIZE, 3.1);

  return {
    albedo: makeTexture(scene, albedo, SIZE, 'flakingPaint_albedo', true),
    normal: makeTexture(scene, normal, SIZE, 'flakingPaint_normal', false),
    orm: makeTexture(scene, orm, SIZE, 'flakingPaint_orm', false),
  };
}

/* ========================================================================== */
/*  Oxidised steel — cell fronts, gang doors, catwalks                        */
/* ========================================================================== */

export interface OxidisedSteelOptions {
  /** 0 = painted and sound, 1 = fully scaled rust. */
  corrosion?: number;
  /** Enamel colour over the steel. */
  paint?: string;
  seed?: number;
}

export function bakeOxidisedSteel(scene: Scene, opts: OxidisedSteelOptions = {}): BakedSet {
  const { corrosion = 0.6, paint = HEX.steelOxideBrown, seed = 1975 } = opts;

  const albedo = new Uint8ClampedArray(SIZE * SIZE * 4);
  const orm = new Uint8ClampedArray(SIZE * SIZE * 4);
  const height = new Float32Array(SIZE * SIZE);

  const enamel = hexToRgb(paint);
  const rust = hexToRgb(HEX.rustOrange);
  const rustHot = hexToRgb(HEX.rustBright);
  const scale = hexToRgb('#4a2f21');
  const bare = hexToRgb('#6c6a67');

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = x / SIZE;
      const v = y / SIZE;
      const i = (y * SIZE + x) * 4;

      // Rust does not appear uniformly — it blooms from nucleation points and
      // then runs downward. Two fields: bloom and run.
      const bloom = fbm(u * 11, v * 11, 11, 5, seed + 17);
      const run = fbm(u * 90, v * 6, 90, 3, seed + 53);
      const runMask = smoothstep(0.55, 0.85, run) * smoothstep(0.1, 0.6, bloom);

      const rustField = clamp01(bloom * 0.75 + runMask * 0.45 + corrosion * 0.55 - 0.35);
      const rustMask = smoothstep(0.18, 0.62, rustField);

      // Pitting: deep scaled craters inside the heavily rusted regions.
      const pit = worley(u * 3.2, v * 3.2, 34, seed + 211);
      const pitMask = smoothstep(0.55, 0.15, pit.f1) * rustMask;

      let rgb = enamel;
      // Chipped enamel exposes primer/bare metal at the edges of rust.
      const chipEdge = smoothstep(0.1, 0.24, rustField) * (1 - smoothstep(0.24, 0.4, rustField));
      rgb = mixRgb(rgb, bare, chipEdge * 0.5);
      rgb = mixRgb(rgb, rust, rustMask * 0.9);
      rgb = mixRgb(rgb, rustHot, smoothstep(0.5, 0.85, rustField) * 0.45);
      rgb = mixRgb(rgb, scale, pitMask * 0.7);

      // Fine directional mill grain on the intact enamel.
      const mill = fbm(u * 340, v * 12, 340, 2, seed + 3);
      rgb = mixRgb(rgb, mixRgb(rgb, [0, 0, 0], 0.12), (1 - rustMask) * mill * 0.3);

      const h =
        rustMask * 0.28 + // rust is bulky, it stands proud
        pitMask * -0.7 + // but pits are deep
        mill * 0.03;
      height[y * SIZE + x] = h;

      albedo[i] = rgb[0];
      albedo[i + 1] = rgb[1];
      albedo[i + 2] = rgb[2];
      albedo[i + 3] = 255;

      // Rust is fully rough and NON-metallic — this is the single most common
      // material error. Only the intact painted/bare metal keeps metalness.
      const metal = clamp01((1 - rustMask) * 0.85 - chipEdge * 0.2);
      const rough = clamp01(0.34 + rustMask * 0.62 + pitMask * 0.1 - mill * 0.05);
      const ao = clamp01(1 - pitMask * 0.55 - rustMask * 0.12);

      orm[i] = ao * 255;
      orm[i + 1] = rough * 255;
      orm[i + 2] = metal * 255;
      orm[i + 3] = 255;
    }
  }

  const normal = heightToNormal(height, SIZE, 2.9);

  return {
    albedo: makeTexture(scene, albedo, SIZE, 'oxidisedSteel_albedo', true),
    normal: makeTexture(scene, normal, SIZE, 'oxidisedSteel_normal', false),
    orm: makeTexture(scene, orm, SIZE, 'oxidisedSteel_orm', false),
  };
}

/* ========================================================================== */
/*  Worn institutional concrete floor                                         */
/* ========================================================================== */

export function bakeWornConcrete(
  scene: Scene,
  opts: { polish?: number; cracks?: number; wet?: number; seed?: number } = {},
): BakedSet {
  const { polish = 0.6, cracks = 0.4, wet = 0, seed = 2002 } = opts;

  const albedo = new Uint8ClampedArray(SIZE * SIZE * 4);
  const orm = new Uint8ClampedArray(SIZE * SIZE * 4);
  const height = new Float32Array(SIZE * SIZE);

  const base = hexToRgb(HEX.concreteWorn);
  const cool = hexToRgb(HEX.concreteCool);
  const dark = hexToRgb('#5f5a52');

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = x / SIZE;
      const v = y / SIZE;
      const i = (y * SIZE + x) * 4;

      const mottle = fbm(u * 5, v * 5, 5, 4, seed);
      const fine = fbm(u * 130, v * 130, 130, 3, seed + 11);
      let rgb = mixRgb(base, cool, mottle * 0.55);
      rgb = mixRgb(rgb, mixRgb(rgb, dark, 0.4), fine * 0.35);

      // Exposed aggregate where the surface has worn through.
      const agg = worley(u * 6, v * 6, 120, seed + 71);
      const aggMask = smoothstep(0.45, 0.1, agg.f1) * (1 - polish) * 0.7;
      rgb = mixRgb(rgb, [150, 145, 136], aggMask);

      // Crack network from Worley cell boundaries.
      const cw = worley(u * 1.4, v * 1.4, 9, seed + 401);
      const crackLine = 1 - smoothstep(0.0, 0.055, cw.f2 - cw.f1);
      const crackJitter = fbm(u * 70, v * 70, 70, 2, seed + 5);
      const crackMask = crackLine * smoothstep(0.35, 0.6, crackJitter) * cracks;
      rgb = mixRgb(rgb, [58, 54, 49], crackMask * 0.8);

      // Control joints — straight sawn lines on a coarse grid.
      const jx = Math.abs(((u * 2) % 1) - 0.5);
      const jy = Math.abs(((v * 2) % 1) - 0.5);
      const joint = (1 - smoothstep(0.478, 0.5, jx)) + (1 - smoothstep(0.478, 0.5, jy));
      const jointMask = clamp01(joint);
      rgb = mixRgb(rgb, [72, 68, 62], jointMask * 0.6);

      const h = -crackMask * 0.5 - jointMask * 0.45 + fine * 0.06 - aggMask * 0.08;
      height[y * SIZE + x] = h;

      albedo[i] = rgb[0];
      albedo[i + 1] = rgb[1];
      albedo[i + 2] = rgb[2];
      albedo[i + 3] = 255;

      // Foot-polished concrete is genuinely quite smooth in the traffic lane,
      // and that is why the corridor photographs have those long soft
      // reflections. Polish varies spatially so it never looks uniform.
      const polishField = polish * (0.55 + mottle * 0.6);
      const rough = clamp01(0.88 - polishField * 0.42 + crackMask * 0.1 - wet * 0.45);
      const ao = clamp01(1 - crackMask * 0.5 - jointMask * 0.45);

      orm[i] = ao * 255;
      orm[i + 1] = rough * 255;
      orm[i + 2] = 0;
      orm[i + 3] = 255;
    }
  }

  const normal = heightToNormal(height, SIZE, 1.7);

  return {
    albedo: makeTexture(scene, albedo, SIZE, 'wornConcrete_albedo', true),
    normal: makeTexture(scene, normal, SIZE, 'wornConcrete_normal', false),
    orm: makeTexture(scene, orm, SIZE, 'wornConcrete_orm', false),
  };
}

/* ========================================================================== */
/*  Cracked asphalt with weed intrusion — the perimeter approach              */
/* ========================================================================== */

export function bakeAsphalt(scene: Scene, seed = 1963): BakedSet {
  const albedo = new Uint8ClampedArray(SIZE * SIZE * 4);
  const orm = new Uint8ClampedArray(SIZE * SIZE * 4);
  const height = new Float32Array(SIZE * SIZE);

  const base = hexToRgb(HEX.asphalt);
  const pale = hexToRgb('#6d6a65');
  const weed = hexToRgb(HEX.mossGreen);

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = x / SIZE;
      const v = y / SIZE;
      const i = (y * SIZE + x) * 4;

      const agg = fbm(u * 190, v * 190, 190, 3, seed);
      const oxidation = fbm(u * 4, v * 4, 4, 4, seed + 31);
      let rgb = mixRgb(base, pale, oxidation * 0.6 + agg * 0.25);

      // Alligator cracking: two Worley scales overlaid.
      const c1 = worley(u * 1.1, v * 1.1, 7, seed + 61);
      const c2 = worley(u * 2.6, v * 2.6, 17, seed + 97);
      const crack =
        (1 - smoothstep(0, 0.05, c1.f2 - c1.f1)) * 0.7 +
        (1 - smoothstep(0, 0.04, c2.f2 - c2.f1)) * 0.5;
      const crackMask = clamp01(crack * smoothstep(0.3, 0.7, oxidation));
      rgb = mixRgb(rgb, [26, 24, 22], crackMask * 0.85);

      // Weeds only in the cracks. Sparse.
      const weedNoise = fbm(u * 30, v * 30, 30, 3, seed + 313);
      const weedMask = crackMask * smoothstep(0.62, 0.85, weedNoise);
      rgb = mixRgb(rgb, weed, weedMask * 0.8);

      const h = -crackMask * 0.6 + agg * 0.09 + weedMask * 0.15;
      height[y * SIZE + x] = h;

      albedo[i] = rgb[0];
      albedo[i + 1] = rgb[1];
      albedo[i + 2] = rgb[2];
      albedo[i + 3] = 255;

      orm[i] = clamp01(1 - crackMask * 0.6) * 255;
      orm[i + 1] = clamp01(0.86 - oxidation * 0.12 + crackMask * 0.08) * 255;
      orm[i + 2] = 0;
      orm[i + 3] = 255;
    }
  }

  const normal = heightToNormal(height, SIZE, 2.0);
  return {
    albedo: makeTexture(scene, albedo, SIZE, 'asphalt_albedo', true),
    normal: makeTexture(scene, normal, SIZE, 'asphalt_normal', false),
    orm: makeTexture(scene, orm, SIZE, 'asphalt_orm', false),
  };
}

/* ========================================================================== */
/*  Glazed structural tile — corridor walls, dining hall                      */
/* ========================================================================== */

export function bakeGlazedTile(
  scene: Scene,
  opts: { colour?: string; tilesX?: number; tilesY?: number; decay?: number; seed?: number } = {},
): BakedSet {
  const { colour = HEX.blockCream, tilesX = 8, tilesY = 16, decay = 0.35, seed = 1910 } = opts;

  const albedo = new Uint8ClampedArray(SIZE * SIZE * 4);
  const orm = new Uint8ClampedArray(SIZE * SIZE * 4);
  const height = new Float32Array(SIZE * SIZE);
  const base = hexToRgb(colour);

  for (let y = 0; y < SIZE; y++) {
    for (let x = 0; x < SIZE; x++) {
      const u = x / SIZE;
      const v = y / SIZE;
      const i = (y * SIZE + x) * 4;

      const tx = (u * tilesX) % 1;
      const ty = (v * tilesY) % 1;
      const idx = Math.floor(u * tilesX);
      const idy = Math.floor(v * tilesY);
      const id = hash2(idx, idy, seed);

      const jw = 0.03;
      const jointMask =
        1 -
        Math.min(
          smoothstep(0, jw, Math.min(tx, 1 - tx)),
          smoothstep(0, jw * 2, Math.min(ty, 1 - ty)),
        );

      // Glaze varies subtly tile to tile — kiln variation.
      let rgb = mixRgb(base, mixRgb(base, [255, 255, 255], 0.18), id * 0.7);
      rgb = mixRgb(rgb, [176, 170, 156], jointMask * 0.8);

      // Crazing in the glaze plus staining running down from above.
      const craze = worley(u * 4, v * 4, 60, seed + 71);
      const crazeMask = (1 - smoothstep(0, 0.06, craze.f2 - craze.f1)) * decay;
      rgb = mixRgb(rgb, [140, 132, 118], crazeMask * 0.5);

      const stain = fbm(u * 26, v * 5, 26, 3, seed + 401);
      const stainMask = smoothstep(0.58, 0.85, stain) * decay * smoothstep(0.0, 0.7, v);
      rgb = mixRgb(rgb, [122, 110, 92], stainMask * 0.55);

      const h = -jointMask * 0.35 - crazeMask * 0.06;
      height[y * SIZE + x] = h;

      albedo[i] = rgb[0];
      albedo[i + 1] = rgb[1];
      albedo[i + 2] = rgb[2];
      albedo[i + 3] = 255;

      // Glaze is the one genuinely glossy surface in the building. That
      // specular contrast against everything else is worth protecting.
      const rough = clamp01(0.24 + jointMask * 0.62 + crazeMask * 0.25 + stainMask * 0.3);
      orm[i] = clamp01(1 - jointMask * 0.55) * 255;
      orm[i + 1] = rough * 255;
      orm[i + 2] = 0;
      orm[i + 3] = 255;
    }
  }

  const normal = heightToNormal(height, SIZE, 1.5);
  return {
    albedo: makeTexture(scene, albedo, SIZE, 'glazedTile_albedo', true),
    normal: makeTexture(scene, normal, SIZE, 'glazedTile_normal', false),
    orm: makeTexture(scene, orm, SIZE, 'glazedTile_orm', false),
  };
}
