import { Scene } from '@babylonjs/core/scene';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';
import { Material } from '@babylonjs/core/Materials/material';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import { Vector2 } from '@babylonjs/core/Maths/math.vector';

import { C, HEX } from './Palette';
import { profile } from './Settings';
import {
  bakeLimestone,
  bakeFlakingPaint,
  bakeOxidisedSteel,
  bakeWornConcrete,
  bakeAsphalt,
  bakeGlazedTile,
  type BakedSet,
} from './Bakery';

/**
 * The frozen material library.
 *
 * **This file is owned by the core agent.** Scene agents compose from these
 * presets and may tune the documented per-instance parameters (tiling, wetness,
 * tint) — they must not author new base materials. That rule is the only thing
 * standing between "one building" and "eight inconsistent demos".
 *
 * Every preset is documented with the reference it was calibrated against.
 * See docs/ART-BIBLE.md for the authored parameter ranges.
 */

export type MaterialId =
  | 'limestone.wall'
  | 'limestone.tower'
  | 'limestone.wet'
  | 'paint.cell'
  | 'paint.corridor'
  | 'paint.ceiling'
  | 'steel.cellFront'
  | 'steel.door'
  | 'steel.catwalk'
  | 'concrete.floor'
  | 'concrete.floorWet'
  | 'concrete.slab'
  | 'tile.corridor'
  | 'tile.diningBand'
  | 'asphalt.yard'
  | 'water.standing'
  | 'timber.rotten'
  | 'timber.charred';

interface PresetSpec {
  /**
   * Multiplier on the global world-UV density (Kit.worldUV bakes 1 tile per
   * 3 m of surface). 1 = one tile per 3 m; 3 = one tile per metre.
   * Geometry carries the base density — this only trims it per material, so
   * no scene ever has to reason about tiling.
   */
  scale: number;
  build: (scene: Scene) => BakedSet;
  tune?: (m: PBRMaterial) => void;
}

export class MaterialLibrary {
  private cache = new Map<string, PBRMaterial>();
  private baked = new Map<string, BakedSet>();

  constructor(private scene: Scene) {}

  /** Bake everything up front so no hitch occurs mid-scene. */
  async prewarm(onProgress?: (done: number, total: number) => void): Promise<void> {
    const ids = Object.keys(PRESETS) as MaterialId[];
    for (let i = 0; i < ids.length; i++) {
      this.get(ids[i]);
      onProgress?.(i + 1, ids.length);
      // Yield so the loading screen can paint between bakes.
      await new Promise((r) => setTimeout(r, 0));
    }
  }

  get(id: MaterialId): PBRMaterial {
    const key = id;
    const hit = this.cache.get(key);
    if (hit) return hit;

    const spec = PRESETS[id];
    if (!spec) throw new Error(`Unknown material preset: ${id}`);

    // Share the baked texture set between tiling variants of the same preset.
    let set = this.baked.get(id);
    if (!set) {
      set = spec.build(this.scene);
      this.baked.set(id, set);
    }

    const m = new PBRMaterial(key, this.scene);
    const scale = spec.scale;

    m.albedoTexture = scaled(set.albedo, scale);
    m.bumpTexture = scaled(set.normal, scale);
    m.metallicTexture = scaled(set.orm, scale);
    // Tell Babylon how ORM is packed: AO in R, roughness in G, metallic in B.
    m.useAmbientOcclusionFromMetallicTextureRed = true;
    m.useRoughnessFromMetallicTextureGreen = true;
    m.useMetallnessFromMetallicTextureBlue = true;
    m.metallic = 1;
    m.roughness = 1;

    // Normals baked with +Y up (OpenGL convention).
    m.invertNormalMapY = false;
    m.invertNormalMapX = false;

    // Real-time IBL + one shadow-casting directional is not enough indirect
    // light for interiors; a small ambient term keeps the shadow side readable
    // without washing out the contact shadows.
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.55;

    // PBRMaterial defaults to FOUR simultaneous lights and silently drops the
    // rest. Scene 1.1 alone has moon + sky + two sodium lamps + the player's
    // headlamp — so the headlamp, which is the primary light source in every
    // interior scene in the game, was never rendering at all. Take the budget
    // from the quality tier.
    m.maxSimultaneousLights = profile().maxLights;

    // Specular anti-aliasing: without this the barbed wire, the bars and the
    // corbel edges shimmer badly at 1080p, which is the loudest "this is a
    // browser game" tell there is.
    m.enableSpecularAntiAliasing = true;

    spec.tune?.(m);

    m.freeze(); // none of these change at runtime
    this.cache.set(key, m);
    return m;
  }

  /**
   * Force every material to recompile against the scene's *current* light list.
   *
   * Materials are baked and frozen during the loading screen, before the player
   * (and therefore the headlamp) exists. A frozen material never recompiles, so
   * it keeps the shader it built against the lights present at freeze time —
   * which meant the headlamp, added afterwards, was permanently invisible on
   * every surface in the game. Call this whenever a light is added or removed.
   */
  rebindLights(): void {
    for (const m of this.cache.values()) {
      m.unfreeze();
      m.maxSimultaneousLights = profile().maxLights;
      m.markAsDirty(Material.LightDirtyFlag);
      m.freeze();
    }
  }

  /** Unfreeze, mutate, refreeze — for the powerhouse lighting change. */
  mutate(id: MaterialId, fn: (m: PBRMaterial) => void): void {
    for (const [key, m] of this.cache) {
      if (key === id || key.startsWith(`${id}@`)) {
        m.unfreeze();
        fn(m);
        m.freeze();
      }
    }
  }

  dispose(): void {
    for (const m of this.cache.values()) m.dispose();
    this.cache.clear();
    this.baked.clear();
  }
}

/**
 * Apply the density multiplier to a baked texture.
 *
 * Deliberately NOT a clone. `Texture.clone()` on a `RawTexture` does not
 * reliably carry the pixel buffer across — the clones came back flat, which
 * cost an iteration to track down. Each preset owns its own `BakedSet` (the
 * cache is keyed by preset id and every preset has its own `build`), so no two
 * materials share a texture object and mutating it in place is safe.
 */
function scaled(tex: Texture, scale: number): Texture {
  tex.uScale = scale;
  tex.vScale = scale;
  return tex;
}

/* ========================================================================== */

const PRESETS: Record<MaterialId, PresetSpec> = {
  /**
   * Perimeter wall and cell-house exterior. Calibrated against the reference
   * plate of the wall below the cap rail: irregular courses, pale-cream to
   * warm-gold block mix, black biological blotching in patches, heavy dark
   * staining at grade.
   */
  'limestone.wall': {
    scale: 1, // one tile per 3 m → ~7 courses ≈ 0.43 m each
    build: (s) => bakeLimestone(s, { courses: 7, rustication: 0.9, soiling: 0.55, runoff: 0.5 }),
  },

  /** Tower shafts: finer ashlar, cleaner, less runoff (they shed water). */
  'limestone.tower': {
    scale: 1.35, // tower ashlar is finer than the wall
    build: (s) =>
      bakeLimestone(s, { courses: 11, rustication: 0.55, soiling: 0.28, runoff: 0.25, seed: 1892 }),
  },

  /** Below-grade and drainage-trench stone: saturated, mossy, much darker. */
  'limestone.wet': {
    scale: 1,
    build: (s) =>
      bakeLimestone(s, {
        courses: 7,
        rustication: 0.9,
        soiling: 0.85,
        runoff: 0.9,
        wetness: 0.75,
        seed: 1871,
      }),
    tune: (m) => {
      m.albedoColor = new Color3(0.72, 0.76, 0.72);
      // Wet stone gets a real specular sheen; this is most of "it looks wet".
      m.environmentIntensity = 0.95;
    },
  },

  /**
   * Cell interiors. The stratigraphy is straight off the reference: cream
   * topcoat curling away to mustard, then pale blue-grey, then sage, then
   * bare block.
   */
  'paint.cell': {
    scale: 1.6, // CMU courses want ~1.9 m per tile
    build: (s) =>
      bakeFlakingPaint(s, {
        decay: 0.62,
        topcoat: HEX.paintTopCream,
        strata: [HEX.paintMustard, HEX.paintBlueGrey, HEX.paintSage],
      }),
  },

  /** Corridor walls: less advanced failure, more traffic grime at hand height. */
  'paint.corridor': {
    scale: 1.6,
    build: (s) => bakeFlakingPaint(s, { decay: 0.3, seed: 1931 }),
  },

  /**
   * Ceilings. The reference corridors have catastrophic delamination — sheets
   * hanging down. Decay is pushed near maximum and the strata read cooler.
   */
  'paint.ceiling': {
    scale: 1.3,
    build: (s) =>
      bakeFlakingPaint(s, {
        decay: 0.92,
        blocksX: 3,
        blocksY: 3, // ceilings are plaster, not block — near-invisible joints
        topcoat: '#ded6c2',
        strata: ['#c9c0a8', '#a8a292', '#8d8778'],
        seed: 1966,
      }),
  },

  /** Cell fronts and gang doors: oxide-brown enamel over heavy rust bloom. */
  'steel.cellFront': {
    scale: 3, // one tile per metre — read at arm's length
    build: (s) => bakeOxidisedSteel(s, { corrosion: 0.68, paint: HEX.steelOxideBrown }),
  },

  /** Machine Shop / service gates: institutional red oxide over grey primer. */
  'steel.door': {
    scale: 2.2,
    build: (s) => bakeOxidisedSteel(s, { corrosion: 0.42, paint: HEX.doorRedOxide, seed: 1901 }),
  },

  /** Catwalk stringers and railings — most corroded, least paint left. */
  'steel.catwalk': {
    scale: 3.6,
    build: (s) => bakeOxidisedSteel(s, { corrosion: 0.85, paint: '#5a4a3e', seed: 1888 }),
  },

  /**
   * Cell-house corridor floor. Foot-polished to a soft sheen in the traffic
   * lane — that long specular running away down the corridor is the single
   * most recognisable thing in the reference photography.
   */
  'concrete.floor': {
    scale: 0.85, // ~3.5 m per tile, hides repetition underfoot
    build: (s) => bakeWornConcrete(s, { polish: 0.72, cracks: 0.25 }),
  },

  'concrete.floorWet': {
    scale: 0.85,
    build: (s) => bakeWornConcrete(s, { polish: 0.8, cracks: 0.3, wet: 0.8, seed: 1975 }),
    tune: (m) => {
      m.albedoColor = new Color3(0.6, 0.63, 0.63);
      m.environmentIntensity = 1.1;
    },
  },

  /** Exterior slab and walkways: unpolished, cracked, weathered. */
  'concrete.slab': {
    scale: 0.9,
    build: (s) => bakeWornConcrete(s, { polish: 0.18, cracks: 0.7, seed: 1954 }),
  },

  /** Glazed structural tile corridor wainscot. */
  'tile.corridor': {
    scale: 1.8,
    build: (s) => bakeGlazedTile(s, { colour: HEX.blockCream, decay: 0.4 }),
  },

  /** Dining hall: the 1970s decorative band lives on this as a decal. */
  'tile.diningBand': {
    scale: 1.8,
    build: (s) => bakeGlazedTile(s, { colour: HEX.bandCream, decay: 0.22, seed: 1972 }),
  },

  'asphalt.yard': {
    scale: 0.7, // ~4.3 m per tile
    build: (s) => bakeAsphalt(s),
  },

  /**
   * Standing water in the siphon and the basements. Reuses the concrete
   * normal at low amplitude for the bed, then overrides to a clear-coated
   * dark dielectric. Scenes animate the UV offset for drift.
   */
  'water.standing': {
    scale: 1.5,
    build: (s) => bakeWornConcrete(s, { polish: 1, cracks: 0, wet: 1, seed: 1888 }),
    tune: (m) => {
      m.albedoColor = C.waterMurk;
      m.albedoTexture = null;
      m.metallic = 0;
      m.roughness = 0.06;
      m.alpha = 0.86;
      m.environmentIntensity = 1.4;
      // A clear coat is what makes a puddle read as a *surface* rather than a
      // dark patch of floor.
      m.clearCoat.isEnabled = true;
      m.clearCoat.intensity = 1;
      m.clearCoat.roughness = 0.04;
      if (m.bumpTexture) {
        (m.bumpTexture as Texture).level = 0.14;
      }
    },
  },

  'timber.rotten': {
    scale: 2,
    build: (s) => bakeWornConcrete(s, { polish: 0, cracks: 0.9, seed: 1899 }),
    tune: (m) => {
      m.albedoColor = C.rottenTimber;
      m.roughness = 1;
    },
  },

  /** Burned roof timbers in the industrial shops. */
  'timber.charred': {
    scale: 2,
    build: (s) => bakeWornConcrete(s, { polish: 0, cracks: 1, seed: 1977 }),
    tune: (m) => {
      m.albedoColor = C.charredTimber;
      m.roughness = 0.98;
      m.environmentIntensity = 0.25; // char swallows light
    },
  },
};

/**
 * Detail-normal overlay shared by every large surface.
 *
 * Close to the camera, a 1 k tile stretched over 3 m of wall has no
 * micro-surface left. A second high-frequency normal at ~40× breaks that up
 * and is the cheapest large win available in the whole renderer.
 */
export function applyDetailNormal(m: PBRMaterial, tex: Texture, strength = 0.35): void {
  m.unfreeze();
  m.detailMap.isEnabled = true;
  m.detailMap.texture = tex;
  m.detailMap.bumpLevel = strength;
  m.detailMap.diffuseBlendLevel = 0.08;
  m.detailMap.roughnessBlendLevel = 0.12;
  (tex as Texture).uScale = 12;
  (tex as Texture).vScale = 12;
  m.freeze();
}

/** Parallax on the deepest masonry. Cheap POM, big silhouette payoff. */
export function applyParallax(m: PBRMaterial, scale = 0.045): void {
  m.unfreeze();
  m.useParallax = true;
  m.useParallaxOcclusion = true;
  m.parallaxScaleBias = scale;
  m.freeze();
}

export const UV_ZERO = new Vector2(0, 0);
