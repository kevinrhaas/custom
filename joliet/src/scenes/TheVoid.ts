import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { MeshBuilder } from '@babylonjs/core/Meshes/meshBuilder';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { CreateBoxVertexData } from '@babylonjs/core/Meshes/Builders/boxBuilder';
import { CreatePlaneVertexData } from '@babylonjs/core/Meshes/Builders/planeBuilder';
import { CreateTorusVertexData } from '@babylonjs/core/Meshes/Builders/torusBuilder';
import { Vector3, Matrix } from '@babylonjs/core/Maths/math.vector';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { FresnelParameters } from '@babylonjs/core/Materials/fresnelParameters';
import { SpotLight } from '@babylonjs/core/Lights/spotLight';
import { PointLight } from '@babylonjs/core/Lights/pointLight';
import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { RawTexture } from '@babylonjs/core/Materials/Textures/rawTexture';
import { Constants } from '@babylonjs/core/Engines/constants';
import type { Scene } from '@babylonjs/core/scene';

import '@babylonjs/core/Particles/particleSystemComponent';

import { GameScene, type SceneManifest } from './SceneBase';
import { C, srgb } from '../core/Palette';
import { fbm, heightToNormal, clamp01 } from '../core/Noise';
import { profile } from '../core/Settings';

/**
 * Scene 3.1b — The Void.
 *
 * A sealed barrel-vaulted sub-level beneath the east cell house: bricked over
 * at one end, broken into from above at the other, and absent from every
 * survey after 1910.
 *
 * The payload is not a monster. It is a punishment level from the decade when
 * the inmates hand-quarried the limestone that built the walls they were kept
 * behind — and their names are cut into that stone by their own tools. The
 * building was made by the people it consumed and somebody bricked over the
 * proof. That is the whole game in one room.
 *
 * **Register: institutional, never paranormal.** Nothing moves here that a
 * draught could not move. There is no scare beat, no audio sting, no
 * silhouette in a doorway, and there never will be. The horror is the
 * record-keeping, and it only lands if the room is quiet enough to read.
 *
 * Composition intent: the shaft of cold light through the broken floor is the
 * only thing in the room that reads as *up*, and it is the anchor of every
 * wide frame. Everything else is headlamp. The vault converges hard toward the
 * brick seal at the far end so the corridor perspective does the navigation
 * work, and the water at that end catches what little light reaches it. The
 * player's eye should go: shaft → floor → wall → and then, at reading
 * distance, the names.
 *
 * The Void is fiction on a documented foundation — see
 * docs/HISTORICAL-LIBERTIES.md §3. The convict-quarried limestone is real; the
 * sealed level is invented, and so is every name carved into it (see
 * `INSCRIPTIONS` below).
 */

/* -------------------------------------------------------------------------- */
/*  Room dimensions — one place, so every subsystem agrees                     */
/* -------------------------------------------------------------------------- */

/** Interior half-width. The chamber is 4 m across. */
const HALF_W = 2.0;
/** Top of the vertical wall / bottom of the vault. Deliberately at head height. */
const SPRING = 1.8;
/** Rise of the segmental vault above the springing line. Crown at 3.1 m. */
const RISE = 1.3;
/** Chamber runs from z = 0 (broken in) to z = Z_END (bricked up). */
const Z_END = 22;
/** The floor steps down at this z; beyond it is standing water. */
const Z_STEP = 13.5;
const FLOOR_LOW = -0.18;
const WATER_Y = -0.05;

/** Centre of the broken-through opening in the vault. Off-axis on purpose. */
const HOLE_X = 0.45;
const HOLE_Z = 3.0;
const HOLE_HALF_X = 1.0;
const HOLE_HALF_Z = 1.15;

interface Niche {
  side: 1 | -1;
  z: number;
}

/** Four punishment niches — barely more than recesses. Asymmetric on purpose. */
const NICHES: Niche[] = [
  { side: -1, z: 5.6 },
  { side: 1, z: 8.9 },
  { side: -1, z: 13.0 },
  { side: 1, z: 16.4 },
];
const NICHE_HALF_Z = 0.48;
const NICHE_H = 1.34;
const NICHE_DEPTH = 0.85;

/** The ventilator flue near the seal — the one warm thing in the room. */
const VENT_Z = 19.3;
const VENT_Y = 1.42;

/* -------------------------------------------------------------------------- */

export class TheVoid extends GameScene {
  readonly manifest: SceneManifest = {
    id: '3.1b-void',
    title: 'The Void',
    spawn: { position: [0.4, 1.4, 4.6], yaw: 0 },
    anchors: [
      {
        name: 'a1-descent',
        position: [0.95, 1.62, 7.4],
        rotation: [Math.PI, -0.1],
        note: 'The establishing frame, looking back at the way in. Tests the shaft as the only "up", the rubble spill, and whether the hand-cut vault reads under a single cold source plus headlamp.',
      },
      {
        name: 'a2-shaft',
        position: [-0.35, 1.24, 5.3],
        rotation: [Math.PI - 0.34, -0.58],
        note: 'Up into the break-in from beside the spill. Tests the broken floor slab, snapped joists, rim stones and the lit dust — the one moment the room admits there is a building above it.',
      },
      {
        name: 'a3-names',
        position: [-0.55, 1.34, 10.5],
        rotation: [Math.PI / 2, 0.03],
        note: 'THE scene. Square on the east wall from 2.55 m — the far side of the chamber, because the headlamp is an inverse-square 900 and anything inside ~2 m clips to white. Tests inscription legibility, the carve normal and block-face relief. If the names cannot be read here, nothing else matters.',
      },
      {
        name: 'a4-niche',
        position: [0.35, 1.08, 8.8],
        rotation: [Math.PI / 2 - 0.03, 0.08],
        note: 'A punishment niche at 1.6 m: iron staple, tally marks, segmental head, 0.85 m deep. Tests the arch geometry and that the recess reads as a place a person was put, not a decorative alcove.',
      },
      {
        name: 'a5-seal',
        position: [0.05, 1.5, 18.6],
        rotation: [0, 0.03],
        note: 'The brick seal at the far end over standing water, with the sodium bleed from the ventilator flue on the right. Tests brick-vs-limestone contrast, the water clear coat, the warm/cool split at depth, and the payload: someone did this deliberately.',
      },
    ],
  };

  private shaft!: SpotLight;
  private bleed?: PointLight;
  private above?: PointLight;
  private dust?: ParticleSystem;
  private beam?: Mesh;
  private beamOrigin = Vector3.Zero();
  private beamDir = Vector3.Up();
  private beamLen = 0;
  private beamR0 = 0;
  private beamR1 = 0;
  private t = 0;

  /** Wall faces the inscription pass is allowed to carve into. */
  private faces: CarveFace[] = [];

  async build(): Promise<void> {
    const ctx = this.kit();
    const p = profile();
    const rng = mulberry(18580412); // Boyington's office, allegedly

    // ---- Materials -------------------------------------------------------
    // This chamber is below grade and has been shut since 1910, so the
    // *dominant* stone is `limestone.wet` — darker, cooler, heavily soiled —
    // and `limestone.wall` is reserved for stone that has been broken open
    // recently: the rubble spill, the rim of the break-in, the near collapse.
    // That split is the room's only hue gradient and it points at the way out.
    const stone = this.mats.get('limestone.wall');
    const wet = this.mats.get('limestone.wet');
    const slab = this.mats.get('concrete.slab');
    const water = this.mats.get('water.standing');
    const steel = this.mats.get('steel.catwalk');
    const timber = this.mats.get('timber.rotten');

    // Seven lights can be in play here — moon, sky bounce, the shaft, the
    // bounce inside the sub-floor void, the vent bleed, and the player's
    // headlamp. `MaterialLibrary` now takes `maxSimultaneousLights` from the
    // quality tier and `main.ts` calls `rebindLights()` after the player
    // spawns, so library materials are covered; the scene-authored materials
    // below have to set it themselves. On the `low` tier the cap is four and
    // one of the minor lights will silently drop — acceptable, and not
    // something a scene may fix without touching core.

    // The seal is the one thing in the room that is not limestone, and that
    // difference is the point — so it gets a scene-specific material rather
    // than a library preset, the way 1.1 authors its glass and shingle.
    const brick = this.buildBrickMaterial();

    // ---- Masonry ---------------------------------------------------------
    // Every block in this room is placed individually and given world-space
    // UVs before it is batched, so no two blocks sample the same texels. That
    // is what makes hand-quarried stone read as hand-quarried rather than as a
    // tiled surface. The batches merge down to one mesh per material.
    const dry = new GeoBatch();
    const damp = new GeoBatch();
    const brickBatch = new GeoBatch();
    const rubbleBatch = new GeoBatch();
    const slabBatch = new GeoBatch();
    const steelBatch = new GeoBatch();
    const timberBatch = new GeoBatch();

    this.buildFloor(ctx, wet, slab, water, rng);
    this.buildSideWalls(dry, damp, rng);
    this.buildNiches(damp, steelBatch, rng);
    this.buildVault(dry, damp, rng);
    this.buildOuterMass(dry);
    this.buildBreakIn(dry, rubbleBatch, slabBatch, timberBatch, steelBatch, rng);
    this.buildSeal(dry, brickBatch, rng);
    this.buildNearCollapse(rubbleBatch, rng);
    this.buildCollapse(rubbleBatch, timberBatch, rng);
    this.buildVent(dry, steelBatch);

    // Texel density is a real decision here, not a knob. The library's
    // limestone bakes seven courses into a tile; at the global 1-tile-per-3-m
    // density the *texture's* coursing lands at 0.43 m and competes with the
    // real coursing of the real blocks, and at 1.2 m per tile it drops to
    // 0.17 m and the whole chamber reads as a Victorian brick sewer. 2 m per
    // tile puts the texture's courses at 0.29 m — the same family as the
    // geometry — so it reads as more joints rather than as a second wall.
    dry.finish(ctx, this.scene, 'voidStone', stone, {
      collide: false,
      cast: true,
      uvDensity: 0.45,
    });
    damp.finish(ctx, this.scene, 'voidStoneWet', wet, {
      collide: false,
      cast: true,
      uvDensity: 0.45,
    });
    brickBatch.finish(ctx, this.scene, 'voidSeal', brick, {
      collide: false,
      cast: true,
      uvDensity: 0.8,
    });
    rubbleBatch.finish(ctx, this.scene, 'voidRubble', stone, {
      collide: true,
      cast: true,
      surface: 'stone',
      uvDensity: 0.45,
    });
    slabBatch.finish(ctx, this.scene, 'voidSlab', slab, { collide: false, cast: true });
    steelBatch.finish(ctx, this.scene, 'voidSteel', steel, {
      collide: false,
      cast: true,
      uvDensity: 1.6,
    });
    timberBatch.finish(ctx, this.scene, 'voidTimber', timber, { collide: false, cast: true });

    // Iron staples in the niche backs — the mundane detail that says a person
    // was kept here, not stored here.
    this.buildStaples(ctx, steel);

    // ---- The names -------------------------------------------------------
    this.buildInscriptions(ctx, rng);

    // ---- Collision -------------------------------------------------------
    // Invisible proxies rather than collision on the batched masonry: a single
    // 30 k-vertex mesh is a poor thing to sweep an ellipsoid against every
    // frame, and the player only ever touches six planes in here.
    this.buildColliders(ctx);

    // ---- Light -----------------------------------------------------------
    this.buildShaft(p);

    await this.scene.whenReadyAsync();
  }

  /* ---------------------------------------------------------------- floor -- */

  private buildFloor(
    ctx: ReturnType<GameScene['kit']>,
    wet: PBRMaterial,
    slab: PBRMaterial,
    water: PBRMaterial,
    rng: () => number,
  ): void {
    // Upper floor: silt over stone, from the break-in to the step.
    const upper = MeshBuilder.CreateBox(
      'voidFloorUpper',
      { width: HALF_W * 2 + 1.6, height: 0.6, depth: Z_STEP + 2.4 },
      this.scene,
    );
    upper.position.set(0, -0.3, (Z_STEP - 1.2) / 2);
    upper.material = wet;
    ctx.register(upper, { collide: true, cast: false, surface: 'stone', uvDensity: 0.3 });

    // Lower floor: the far end has settled (or was always cut deeper), and it
    // holds water.
    const lower = MeshBuilder.CreateBox(
      'voidFloorLower',
      { width: HALF_W * 2 + 1.6, height: 0.6, depth: Z_END - Z_STEP + 2.2 },
      this.scene,
    );
    lower.position.set(0, FLOOR_LOW - 0.3, (Z_STEP + Z_END + 2.2) / 2 - 0.1);
    lower.material = wet;
    ctx.register(lower, { collide: true, cast: false, surface: 'water', uvDensity: 0.3 });

    // Standing water. Alpha-blended, never a shadow caster, never pickable —
    // the same rules 1.1's trench water follows.
    const pool = MeshBuilder.CreateGround(
      'voidWater',
      { width: HALF_W * 2 - 0.04, height: Z_END - Z_STEP - 0.4, subdivisions: 14 },
      this.scene,
    );
    pool.position.set(0, WATER_Y, (Z_STEP + Z_END) / 2 + 0.7);
    pool.material = water;
    pool.isPickable = false;
    pool.receiveShadows = false;
    this.meshes.push(pool);

    // Silt fans at the waterline and under the break-in. Flat, low, irregular.
    const silt = new GeoBatch();
    for (let i = 0; i < 26; i++) {
      const nearWater = i < 16;
      const z = nearWater ? Z_STEP - 1.6 + rng() * 5.4 : 1.4 + rng() * 5.2;
      const y = z > Z_STEP ? FLOOR_LOW : 0;
      silt.box(
        (rng() - 0.5) * 3.1,
        y + 0.018,
        z,
        0.5 + rng() * 1.3,
        0.045 + rng() * 0.05,
        0.5 + rng() * 1.2,
        0,
        rng() * Math.PI,
        0,
      );
    }
    silt.finish(ctx, this.scene, 'voidSilt', slab, {
      collide: false,
      cast: false,
      uvDensity: 0.45,
    });
  }

  /* ------------------------------------------------------------ side walls -- */

  /**
   * Coursed rubble ashlar up to the springing line, laid block by block.
   *
   * Courses vary in height, blocks vary in length, and every block's inner
   * face is jittered a centimetre or two proud or shy of the wall plane. That
   * jitter is the entire reason this reads as hand-cut: it is what gives a
   * raking headlamp something to catch on. Machine-dressed ashlar is flat and
   * would kill the scene.
   */
  private buildSideWalls(dry: GeoBatch, damp: GeoBatch, rng: () => number): void {
    for (const side of [-1, 1] as const) {
      // Blocks are cut slightly OVER their cell and butt into their
      // neighbours rather than leaving a modelled joint gap. A gap would be a
      // hole straight through the wall — which is what the first pass did, and
      // it turned every joint into a black slot and the wall into a stack of
      // crates. All the joint reading comes from the face jitter instead:
      // every stone stands up to 5 cm proud of its neighbour, which is what a
      // raking headlamp actually catches on in a hand-dressed wall.
      let y = -0.12;
      while (y < SPRING - 0.02) {
        const h = Math.min(0.23 + rng() * 0.2, SPRING - y);
        // Every course starts at a different offset, so the vertical joints
        // never line up into a grid.
        let z = -0.9 + rng() * 0.6;
        while (z < Z_END + 0.9) {
          const len = 0.32 + rng() * 0.54;
          const zc = z + len / 2;
          const centreY = y + h / 2;

          const inVent =
            side === 1 &&
            Math.abs(zc - VENT_Z) < 0.42 + len / 2 &&
            Math.abs(centreY - VENT_Y) < 0.26 + h / 2;

          if (!inVent && !this.inNicheOpening(side, zc, len, centreY, h)) {
            // Rising damp — except this whole chamber is below the water
            // table, so only the freshly-broken stone at the entrance is dry.
            const soaked = zc > 5.2 || y < 0.5;
            const batch = soaked ? damp : dry;
            const proud = rng() * rng() * 0.1;
            const depth = 0.46 + rng() * 0.13;
            const faceX = side * (HALF_W - proud);
            batch.box(
              faceX + side * (depth / 2),
              centreY,
              zc,
              depth,
              h * 1.06,
              len * 1.04,
              (rng() - 0.5) * 0.03,
              (rng() - 0.5) * 0.028,
              (rng() - 0.5) * 0.022,
            );

            // Big enough and at a height a man could reach sitting or
            // standing: a candidate for carving. Carvings cluster — men
            // wrote where other men had already written, and beside the
            // niches, and not much anywhere else.
            if (h > 0.28 && len > 0.44 && centreY > 0.4 && centreY < 1.66) {
              let weight = 0.55;
              if (zc > 8.4 && zc < 13.8) weight = 2.1; // the reading wall
              for (const n of NICHES) {
                if (Math.abs(zc - n.z) < 1.7) weight = Math.max(weight, 1.5);
              }
              this.faces.push({
                x: faceX,
                y: centreY,
                z: zc,
                nx: -side,
                nz: 0,
                w: len,
                h,
                weight,
                // The east wall between z 9.6 and 11.6 is the anchor frame for
                // the whole scene. It is not left to a dice roll.
                forced: side === 1 && zc > 9.5 && zc < 11.8,
              });
            }
          }
          z += len;
        }
        y += h;
      }
    }

    // A solid liner immediately behind the ashlar, so a joint that does open
    // up shows recessed stone rather than a view into empty space.
    for (const side of [-1, 1] as const) {
      const blocked: [number, number][] = NICHES.filter((n) => n.side === side).map((n) => [
        n.z - NICHE_HALF_Z - 0.3,
        n.z + NICHE_HALF_Z + 0.3,
      ]);
      if (side === 1) blocked.push([VENT_Z - 0.75, VENT_Z + 0.75]);
      blocked.sort((a, b) => a[0] - b[0]);

      let z = -1.2;
      for (const [z0, z1] of [...blocked, [Z_END + 1.2, Z_END + 1.2] as [number, number]]) {
        if (z0 - z > 0.05) {
          damp.box(side * (HALF_W + 0.7), 0.9, (z + z0) / 2, 0.44, 2.4, z0 - z);
        }
        z = Math.max(z, z1);
      }
    }

  }

  /**
   * The near end: the chamber continues that way and the roof came down on it
   * long before anybody found the place.
   *
   * Built as a talus — a wedge of stone tipping down and out into the room —
   * rather than blocks scattered through a bounding box. The first pass did
   * the latter and produced masonry hanging in mid-air, which is invisible in
   * the source and the first thing the eye finds in the capture.
   */
  private buildNearCollapse(rubble: GeoBatch, rng: () => number): void {
    for (let i = 0; i < 64; i++) {
      const t = rng() * rng(); // packed against the face, thinning outward
      const z = -0.75 + t * 2.6;
      const ceiling = 3.25 * (1 - t) + 0.2;
      const s = 0.24 + rng() * 0.42;
      rubble.box(
        (rng() - 0.5) * 3.6,
        s * 0.3 + rng() * ceiling,
        z,
        s * (0.8 + rng() * 0.8),
        s * (0.5 + rng() * 0.6),
        s * (0.8 + rng() * 0.8),
        (rng() - 0.5) * 1.0,
        rng() * Math.PI,
        (rng() - 0.5) * 1.0,
      );
    }
  }

  private inNicheOpening(
    side: number,
    z: number,
    len: number,
    y: number,
    h: number,
  ): boolean {
    for (const n of NICHES) {
      if (n.side !== side) continue;
      const dz = Math.abs(z - n.z);
      if (dz < NICHE_HALF_Z + len / 2 - 0.04 && y - h / 2 < NICHE_H - 0.02) return true;
    }
    return false;
  }

  /* ---------------------------------------------------------------- niches -- */

  /**
   * The punishment cells. They are niches: 0.95 m wide, 0.85 m deep, 1.34 m to
   * the crown of a low segmental head. A man fits sitting. That is the whole
   * specification and it is worse than a room would be.
   */
  private buildNiches(damp: GeoBatch, steel: GeoBatch, rng: () => number): void {
    for (const n of NICHES) {
      const s = n.side;
      const backX = s * (HALF_W + NICHE_DEPTH);

      // Back wall, in courses, so the inscriptions inside sit on real stones.
      let y = 0;
      while (y < NICHE_H - 0.1) {
        const h = Math.min(0.3 + rng() * 0.16, NICHE_H - 0.1 - y);
        let z = n.z - NICHE_HALF_Z;
        while (z < n.z + NICHE_HALF_Z - 0.02) {
          const len = Math.min(0.42 + rng() * 0.3, n.z + NICHE_HALF_Z - z);
          const proud = rng() * rng() * 0.04;
          const faceX = backX - s * proud;
          damp.box(
            faceX + s * 0.24,
            y + h / 2,
            z + len / 2,
            0.5,
            h * 1.06,
            len * 1.05,
            (rng() - 0.5) * 0.024,
            0,
            (rng() - 0.5) * 0.02,
          );
          if (h > 0.26 && len > 0.36 && y > 0.1) {
            this.faces.push({
              x: faceX,
              y: y + h / 2,
              z: z + len / 2,
              nx: -s,
              nz: 0,
              w: len,
              h,
              // Men were left in here with nothing else to do.
              weight: 4,
              forced: true,
            });
          }
          z += len;
        }
        y += h;
      }

      // Jambs.
      for (const dz of [-1, 1]) {
        let jy = -0.1;
        while (jy < NICHE_H - 0.06) {
          const h = 0.28 + rng() * 0.14;
          damp.box(
            s * (HALF_W + NICHE_DEPTH / 2),
            jy + h / 2,
            n.z + dz * (NICHE_HALF_Z + 0.14),
            NICHE_DEPTH + 0.06,
            Math.min(h, NICHE_H - 0.06 - jy) * 1.05,
            0.28,
            0,
            0,
            (rng() - 0.5) * 0.02,
          );
          jy += h;
        }
      }

      // Segmental head. Seven voussoirs on a real arc struck from a centre
      // below the springing — the first pass rotated them about the wrong sign
      // and blew the head apart into a starburst, and the second struck it on
      // too tight a radius so the haunch stones speared out through the wall
      // face as fins. Both are invisible in the source and unmissable in the
      // capture. A 0.22 m rise over a 0.96 m span puts the springing angle at
      // 49°, which is a segmental arch and stays inside the reveal.
      const headRise = 0.22;
      const headSpring = NICHE_H - headRise;
      const R = (NICHE_HALF_Z * NICHE_HALF_Z) / (2 * headRise) + headRise / 2;
      const cy = headSpring + headRise - R;
      const span = Math.asin(Math.min(0.99, NICHE_HALF_Z / R));
      const nV = 7;
      const vW = ((2 * span * R) / nV) * 1.2;
      for (let i = 0; i < nV; i++) {
        const a = ((i + 0.5) / nV - 0.5) * 2 * span;
        const zc = n.z + Math.sin(a) * (R + 0.14);
        damp.box(
          s * (HALF_W + NICHE_DEPTH / 2 + 0.03),
          cy + Math.cos(a) * (R + 0.14),
          zc,
          NICHE_DEPTH - 0.02,
          0.27,
          vW,
          a,
          0,
          0,
        );
        // Backing over each voussoir, stepped to the curve. Without it the
        // square outer corners of the ring stand proud in the gap the wall
        // generator leaves above the head, and read as a row of dark fangs —
        // the sort of thing that looks like intent in the source and like a
        // bug in the frame.
        const top = cy + Math.cos(a) * (R + 0.28);
        if (top < 1.86) {
          damp.box(
            s * (HALF_W + NICHE_DEPTH / 2 + 0.03),
            (top + 1.86) / 2 - 0.02,
            zc,
            NICHE_DEPTH - 0.02,
            1.86 - top + 0.06,
            vW * 1.02,
            0,
            0,
            0,
          );
        }
      }

      // Relieving course and spandrels over the head.
      //
      // The wall generator removes a rectangle for the opening, but the arch
      // ring stands ~0.27 m above the intrados, so its extrados corners were
      // left projecting into the gap above as a row of dark spikes. This
      // closes the gap the way a mason would: a course carried across the
      // head, and a stone in each spandrel.
      const headTop = cy + R + 0.28;
      damp.box(s * (HALF_W + 0.3), headTop + 0.2, n.z, 0.6, 0.42, 1.95, 0, 0, 0);
      for (const dz of [-1, 1]) {
        damp.box(
          s * (HALF_W + 0.3),
          headSpring + 0.24,
          n.z + dz * 0.76,
          0.6,
          0.56,
          0.55,
          0,
          0,
          0,
        );
      }

      // Sill / floor of the niche, worn hollow.
      damp.box(
        s * (HALF_W + NICHE_DEPTH / 2),
        -0.02,
        n.z,
        NICHE_DEPTH + 0.06,
        0.16,
        NICHE_HALF_Z * 2 + 0.28,
        0,
        0,
        0,
      );

      // The staple plate the ring hangs from.
      steel.box(backX - s * 0.02, 0.72, n.z, 0.05, 0.14, 0.1, 0, 0, 0);
    }
  }

  /* ----------------------------------------------------------------- vault -- */

  /**
   * A segmental barrel vault, ring by ring, voussoir by voussoir.
   *
   * The springing line sits at 1.8 m — head height — which is the single most
   * important number in the room. You feel the ceiling. The crown is only
   * 3.1 m and the haunches come down to meet you if you walk near a wall.
   */
  private buildVault(dry: GeoBatch, damp: GeoBatch, rng: () => number): void {
    const ringDepth = 0.6;
    const rings = Math.ceil((Z_END + 1.4) / ringDepth);
    const perRing = 13;

    for (let r = 0; r < rings; r++) {
      const zc = -0.7 + (r + 0.5) * ringDepth;
      // Alternate rings are offset a little so the ring joints do not read as
      // a stack of identical hoops.
      const twist = (r % 2 === 0 ? 1 : -1) * 0.018;

      for (let i = 0; i < perRing; i++) {
        const t = (i + 0.5) / perRing;
        const phi = (t - 0.5) * Math.PI + twist;
        const px = HALF_W * Math.sin(phi);
        const py = SPRING + RISE * Math.cos(phi);

        // The break-in: no stone survives inside the hole.
        if (
          Math.abs(px - HOLE_X) < HOLE_HALF_X &&
          Math.abs(zc - HOLE_Z) < HOLE_HALF_Z &&
          py > SPRING + 0.35
        ) {
          continue;
        }

        // Outward normal of the ellipse.
        let nx = RISE * Math.sin(phi);
        let ny = HALF_W * Math.cos(phi);
        const nl = Math.hypot(nx, ny) || 1;
        nx /= nl;
        ny /= nl;

        const thick = 0.3 + rng() * 0.09;
        // Some stones hang below their neighbours. This, and nothing else, is
        // what makes a barrel vault read as cut by hand.
        const proud = rng() * rng() * 0.06;
        // Voussoirs are cut over-length and butt into each other; a modelled
        // joint gap would be a hole through the vault.
        const seg = (Math.PI / perRing) * ((HALF_W + RISE) / 2) * 1.22;

        // Rotate so the block's local +Y is the outward normal.
        const psi = Math.atan2(-nx, ny);

        // Only the stone within reach of the break-in has been dried out by a
        // century of the draught coming down it. The rest is saturated, which
        // is both true of a chamber below the water table and the reason the
        // room has a hue gradient at all.
        const batch = zc < 5.0 ? dry : damp;
        batch.box(
          px + nx * (thick / 2 - proud),
          py + ny * (thick / 2 - proud),
          zc,
          seg,
          thick,
          ringDepth * 1.07,
          (rng() - 0.5) * 0.03,
          (rng() - 0.5) * 0.024,
          psi + (rng() - 0.5) * 0.04,
        );
      }
    }
  }

  /**
   * The mass the vault is buried in. Never seen — its only job is to stop the
   * moon's directional shadow from leaking through the joints of a vault made
   * of eight hundred separate stones.
   */
  private buildOuterMass(dry: GeoBatch): void {
    // Everything here is held clear of any visible surface. Interpenetrating a
    // hidden box with a visible one produces near-coplanar faces, which
    // z-fight, which the temporal filter then smears into arcs across the
    // whole frame — the streaking that ruined the first pass at every anchor.
    for (const side of [-1, 1] as const) {
      dry.box(
        side * (HALF_W + NICHE_DEPTH + 0.95),
        1.9,
        (Z_END + 0.4) / 2,
        1.5,
        4.4,
        Z_END + 2.6,
      );
    }
    // Cap over the vault, in four pieces that clear the sub-floor shaft.
    const capY = SPRING + RISE + 1.05;
    const capH = 1.0;
    const clearX = HOLE_HALF_X + 0.8;
    const clearZ = HOLE_HALF_Z + 0.8;
    const z0 = HOLE_Z - clearZ;
    const z1 = HOLE_Z + clearZ;
    dry.box(0, capY, (-1.6 + z0) / 2, 9, capH, z0 + 1.6);
    dry.box(0, capY, (z1 + Z_END + 1.6) / 2, 9, capH, Z_END + 1.6 - z1);
    for (const side of [-1, 1] as const) {
      const inner = HOLE_X + side * clearX;
      const outer = side * 4.5;
      dry.box((inner + outer) / 2, capY, HOLE_Z, Math.abs(outer - inner), capH, clearZ * 2);
    }
    // Solid ends. These exist purely so the moon — which is still a
    // full-strength directional out there somewhere — cannot find its way in
    // past either end of a chamber whose walls are eight hundred loose stones.
    dry.box(0, 2.1, -1.25, 9, 4.6, 0.9);
    dry.box(0, 2.1, Z_END + 1.0, 9, 4.6, 0.9);
  }

  /* -------------------------------------------------------------- break-in -- */

  /**
   * The way in: a hole punched up through the vault crown from the cell-house
   * sub-floor, with the broken slab, two snapped joists and a fan of rubble
   * spilling down into the chamber.
   */
  private buildBreakIn(
    dry: GeoBatch,
    rubble: GeoBatch,
    slab: GeoBatch,
    timber: GeoBatch,
    steel: GeoBatch,
    rng: () => number,
  ): void {
    // Jagged rim stones: two rings that climb from the vault surface up to the
    // underside of the floor above, so the opening reads as a hole torn
    // through a thick structure rather than a rectangle cut in a shell.
    const shaftTop = 5.9;
    const shaftBase = SPRING + RISE + 0.52;
    for (let ring = 0; ring < 2; ring++) {
      const count = ring === 0 ? 28 : 22;
      for (let i = 0; i < count; i++) {
        const a = (i / count) * Math.PI * 2 + ring * 0.4;
        const rx = HOLE_HALF_X * (0.9 + rng() * 0.34 + ring * 0.1);
        const rz = HOLE_HALF_Z * (0.9 + rng() * 0.34 + ring * 0.1);
        const x = HOLE_X + Math.cos(a) * rx;
        const z = HOLE_Z + Math.sin(a) * rz;
        const surf = SPRING + RISE * Math.cos(Math.asin(clamp01(Math.abs(x) / HALF_W)));
        const y = ring === 0 ? surf + 0.06 + rng() * 0.3 : shaftBase - 0.3 + rng() * 0.34;
        const s = 0.24 + rng() * 0.26;
        dry.box(
          x,
          y,
          z,
          s * (0.8 + rng() * 0.7),
          s * (0.8 + rng() * 0.7),
          s * (0.8 + rng() * 0.7),
          (rng() - 0.5) * 0.7,
          rng() * Math.PI,
          (rng() - 0.5) * 0.7,
        );
      }
    }

    // The sub-floor void above: four walls and a lid. The lid matters — with
    // the shaft open the player looked straight up at the night sky and stars,
    // which is a lie. There is a cell house on top of this.
    for (const [dx, dz, w, d] of [
      [HOLE_HALF_X + 0.45, 0, 0.7, HOLE_HALF_Z * 2 + 1.7],
      [-(HOLE_HALF_X + 0.45), 0, 0.7, HOLE_HALF_Z * 2 + 1.7],
      [0, HOLE_HALF_Z + 0.45, HOLE_HALF_X * 2 + 1.7, 0.7],
      [0, -(HOLE_HALF_Z + 0.45), HOLE_HALF_X * 2 + 1.7, 0.7],
    ] as const) {
      dry.box(
        HOLE_X + dx,
        (shaftBase + shaftTop) / 2,
        HOLE_Z + dz,
        w,
        shaftTop - shaftBase,
        d,
      );
    }
    dry.box(HOLE_X, shaftTop + 0.3, HOLE_Z, 4.4, 0.6, 4.4);

    // The broken floor slab itself, hanging over the void. Concrete, later
    // than the vault by fifty years, and the reason the hole has a straight
    // edge on one side and a shattered one on the other.
    for (let i = 0; i < 12; i++) {
      const a = (i / 12) * Math.PI * 2;
      slab.box(
        HOLE_X + Math.cos(a) * (HOLE_HALF_X + 0.42),
        shaftBase + 0.28,
        HOLE_Z + Math.sin(a) * (HOLE_HALF_Z + 0.42),
        0.5 + rng() * 0.5,
        0.16,
        0.5 + rng() * 0.5,
        (rng() - 0.5) * 0.25,
        rng() * Math.PI,
        (rng() - 0.5) * 0.25,
      );
    }
    // Rebar, bent down into the opening.
    for (let i = 0; i < 7; i++) {
      steel.box(
        HOLE_X - HOLE_HALF_X + 0.1 + rng() * 0.5,
        shaftBase + 0.16,
        HOLE_Z - HOLE_HALF_Z + rng() * HOLE_HALF_Z * 2,
        0.018,
        0.5 + rng() * 0.4,
        0.018,
        0.4 + rng() * 0.7,
        0,
        (rng() - 0.5) * 0.4,
      );
    }

    // Two snapped joists. One still spans the opening; one came down with the
    // slab and is lying in the spill.
    timber.box(HOLE_X - 0.15, shaftBase + 0.34, HOLE_Z - 0.5, 2.4, 0.15, 0.09, 0, 0, 0.03);
    timber.box(HOLE_X + 1.0, 0.5, HOLE_Z + 1.7, 1.5, 0.12, 0.08, 0.12, 0.6, 0.3);

    // The spill. A cone of vault stone and slab fragments on the floor — and
    // the only way down, so it has to be climbable.
    for (let i = 0; i < 46; i++) {
      const rr = rng();
      const a = rng() * Math.PI * 2;
      const rad = rr * 2.6;
      const s = 0.2 + rng() * 0.42;
      rubble.box(
        HOLE_X - 0.3 + Math.cos(a) * rad,
        0.06 + (1 - rr) * 1.05 + rng() * 0.16,
        HOLE_Z + 0.7 + Math.sin(a) * rad * 1.15,
        s * (0.75 + rng() * 0.75),
        s * (0.5 + rng() * 0.6),
        s * (0.75 + rng() * 0.75),
        (rng() - 0.5) * 1.1,
        rng() * Math.PI,
        (rng() - 0.5) * 1.1,
      );
    }
  }

  /* ------------------------------------------------------------- the seal -- */

  /**
   * The bricked-up opening at the far end.
   *
   * A segmental limestone arch, the same hand as the rest of the chamber, with
   * a common-brick infill laid by somebody in a hurry decades later. The
   * courses do not line up, the mortar is smeared, and it does not reach the
   * crown cleanly. It is the single most deliberate object in the room.
   */
  private buildSeal(dry: GeoBatch, brick: GeoBatch, rng: () => number): void {
    const zFace = Z_END;
    const openHalf = 1.25;
    const openTop = 2.35;

    // End wall around the opening — coursed, like the rest of the chamber.
    // The first pass scattered these at random heights inside a bounding box,
    // which put loose stones hanging in the air above the vault crown.
    let wy = -0.2;
    while (wy < SPRING + RISE + 0.2) {
      const h = 0.26 + rng() * 0.18;
      let wx = -3.4 + rng() * 0.5;
      while (wx < 3.4) {
        const len = 0.4 + rng() * 0.42;
        const cx = wx + len / 2;
        const cyy = wy + h / 2;
        // Only where the chamber's section actually exists, and not across
        // the opening.
        const ceiling =
          Math.abs(cx) < HALF_W
            ? SPRING + RISE * Math.cos(Math.asin(Math.abs(cx) / HALF_W))
            : 0;
        const inSection = Math.abs(cx) < HALF_W + 0.5 && cyy - h / 2 < ceiling + 0.25;
        const inOpening = Math.abs(cx) < openHalf + 0.24 && cyy - h / 2 < openTop + 0.3;
        if (inSection && !inOpening) {
          dry.box(
            cx,
            cyy,
            zFace + 0.3,
            len * 1.04,
            h * 1.06,
            0.6,
            0,
            (rng() - 0.5) * 0.02,
            (rng() - 0.5) * 0.018,
          );
        }
        wx += len;
      }
      wy += h;
    }
    // Solid backing so the coursed face never shows daylight between stones.
    dry.box(0, 1.7, zFace + 0.75, 9, 5.2, 0.5);
    // Segmental arch over the opening.
    const rise = 0.55;
    const R = (openHalf * openHalf) / rise + rise;
    for (let i = 0; i < 11; i++) {
      const t = (i + 0.5) / 11;
      const a = (t - 0.5) * ((openHalf * 2.2) / R);
      dry.box(
        Math.sin(a) * R,
        openTop - rise + Math.cos(a) * R - R + rise + 0.16,
        zFace + 0.26,
        (openHalf * 2.35) / 11,
        0.36,
        0.52,
        0,
        0,
        -a,
      );
    }

    // Threshold under the opening — the brick was laid off a stone sill, and
    // without it the water at this end would run straight under the seal.
    dry.box(0, -0.28, zFace + 0.2, openHalf * 2 + 0.7, 0.62, 0.7);

    // The infill. Common brick, 230 × 110 × 70, laid stretcher bond by
    // somebody who was not a bricklayer.
    const bh = 0.075;
    const bl = 0.23;
    let y = 0;
    let row = 0;
    while (y < openTop + 0.05) {
      // The bond wanders. Whoever laid this was not a bricklayer and the
      // courses do not run true, which is most of what makes the seal read as
      // something done to the room rather than part of it.
      const stagger = (row % 2 === 0 ? 0 : bl / 2) + (rng() - 0.5) * 0.05;
      let x = -openHalf - bl + stagger;
      while (x < openHalf) {
        const yTop = y + bh;
        // Stop where the arch comes down.
        const half = openHalf * Math.sqrt(Math.max(0, 1 - Math.pow(Math.max(0, yTop - (openTop - rise)) / rise, 2)));
        const limit = yTop > openTop - rise ? half : openHalf;
        if (Math.abs(x + bl / 2) < limit - 0.02) {
          brick.box(
            x + bl / 2,
            y + bh / 2,
            zFace + 0.06 + (rng() - 0.5) * 0.02,
            bl * (0.93 + rng() * 0.05),
            bh * (0.86 + rng() * 0.06),
            0.11,
            (rng() - 0.5) * 0.02,
            (rng() - 0.5) * 0.03,
            (rng() - 0.5) * 0.022,
          );
        }
        x += bl;
      }
      y += bh + 0.012;
      row++;
    }
    // The top course never closes properly against the arch — it is packed
    // with stone spalls and mortar instead. That gap is the tell.
    for (let i = 0; i < 14; i++) {
      dry.box(
        -openHalf * 0.75 + rng() * openHalf * 1.5,
        openTop - 0.3 + rng() * 0.3,
        zFace + 0.09,
        0.1 + rng() * 0.16,
        0.08 + rng() * 0.1,
        0.12,
        (rng() - 0.5) * 0.6,
        rng() * Math.PI,
        (rng() - 0.5) * 0.6,
      );
    }
  }

  /* --------------------------------------------------------- decay & vent -- */

  private buildCollapse(rubble: GeoBatch, timber: GeoBatch, rng: () => number): void {
    // Fallen vault stones down the length of the chamber. Sparse — this is a
    // structure that is failing slowly, not a set-dressed ruin.
    for (let i = 0; i < 30; i++) {
      const z = 6 + rng() * (Z_END - 7.5);
      const y = z > Z_STEP ? FLOOR_LOW : 0;
      const s = 0.2 + rng() * 0.36;
      rubble.box(
        (rng() - 0.5) * 3.3,
        y + s * 0.32,
        z,
        s * (0.8 + rng() * 0.8),
        s * (0.45 + rng() * 0.5),
        s * (0.8 + rng() * 0.8),
        (rng() - 0.5) * 0.7,
        rng() * Math.PI,
        (rng() - 0.5) * 0.7,
      );
    }
    // A larger partial fall at the haunch around z = 11, with the stone still
    // half in the wall.
    for (let i = 0; i < 12; i++) {
      rubble.box(
        -1.35 - rng() * 0.5,
        0.1 + rng() * 0.9,
        10.4 + rng() * 1.6,
        0.4 + rng() * 0.3,
        0.3 + rng() * 0.2,
        0.4 + rng() * 0.3,
        (rng() - 0.5) * 0.8,
        rng() * Math.PI,
        (rng() - 0.5) * 0.8,
      );
    }
    // A board floating at the waterline.
    timber.box(0.5, WATER_Y + 0.03, 18.4, 1.9, 0.05, 0.24, 0, 0.22, 0);
    timber.box(-1.1, WATER_Y + 0.05, 15.9, 1.1, 0.06, 0.18, 0, -0.6, 0.02);
  }

  /**
   * A ventilator flue high on the east wall near the seal. Whatever is on the
   * other side of it is a hundred metres away and orange, and it is the only
   * warm thing in the room.
   */
  private buildVent(dry: GeoBatch, steel: GeoBatch): void {
    const z = VENT_Z;
    const y = VENT_Y;
    // Reveal: a dark recessed box behind the wall plane, so the opening has
    // depth rather than being a lit rectangle painted on the stone.
    const dark = MeshBuilder.CreateBox(
      'ventReveal',
      { width: 0.62, height: 0.38, depth: 0.72 },
      this.scene,
    );
    dark.position.set(HALF_W + 0.31, y, z);
    const dm = new StandardMaterial('ventDark', this.scene);
    dm.diffuseColor = new Color3(0.02, 0.02, 0.022);
    dm.specularColor = Color3.Black();
    // The far end of the flue, ninety metres from the nearest working lamp.
    dm.emissiveColor = srgb('#4a2c08');
    dm.disableLighting = true;
    dark.material = dm;
    dark.isPickable = false;
    dark.receiveShadows = false;
    dark.freezeWorldMatrix();
    this.meshes.push(dark);

    // Head and sill of the opening, and the jambs.
    dry.box(HALF_W + 0.24, y + 0.28, z, 0.52, 0.2, 1.0);
    dry.box(HALF_W + 0.24, y - 0.28, z, 0.52, 0.2, 1.0);
    for (const dz of [-1, 1]) {
      dry.box(HALF_W + 0.24, y, z + dz * 0.46, 0.52, 0.4, 0.24);
    }
    for (let i = 0; i < 4; i++) {
      steel.box(HALF_W + 0.05, y, z - 0.21 + i * 0.14, 0.055, 0.36, 0.05);
    }
    steel.box(HALF_W + 0.05, y, z, 0.05, 0.05, 0.62);
  }

  private buildStaples(ctx: ReturnType<GameScene['kit']>, steel: PBRMaterial): void {
    const batch = new GeoBatch();
    for (const n of NICHES) {
      const x = n.side * (HALF_W + NICHE_DEPTH) - n.side * 0.1;
      batch.template(
        CreateTorusVertexData({ diameter: 0.15, thickness: 0.022, tessellation: 10 }),
        new Vector3(1, 1, 1),
        Matrix.RotationYawPitchRoll(Math.PI / 2, 0, 0),
        new Vector3(x, 0.66, n.z),
      );
    }
    // One more in the main wall, opposite nothing at all.
    batch.template(
      CreateTorusVertexData({ diameter: 0.15, thickness: 0.022, tessellation: 10 }),
      new Vector3(1, 1, 1),
      Matrix.RotationYawPitchRoll(Math.PI / 2, 0, 0),
      new Vector3(-HALF_W + 0.08, 0.71, 11.4),
    );
    batch.finish(ctx, this.scene, 'voidRings', steel, {
      collide: false,
      cast: true,
      uvDensity: 2.4,
    });
  }

  /* ---------------------------------------------------------- collision ---- */

  private buildColliders(ctx: ReturnType<GameScene['kit']>): void {
    const invisible = (
      name: string,
      x: number,
      y: number,
      z: number,
      w: number,
      h: number,
      d: number,
    ): void => {
      const m = MeshBuilder.CreateBox(name, { width: w, height: h, depth: d }, this.scene);
      m.position.set(x, y, z);
      m.isVisible = false;
      m.checkCollisions = true;
      m.isPickable = true;
      m.freezeWorldMatrix();
      this.meshes.push(m);
    };

    for (const side of [-1, 1] as const) {
      invisible(`wallCol${side}`, side * (HALF_W + 0.3), 1.7, Z_END / 2, 0.6, 3.4, Z_END + 3);
    }
    invisible('endColFar', 0, 1.7, Z_END + 0.5, 8, 3.4, 0.6);
    invisible('endColNear', 0, 1.7, -1.0, 8, 3.4, 0.6);
    invisible('crownCol', 0, SPRING + RISE + 0.4, Z_END / 2, 8, 0.6, Z_END + 3);
  }

  /* ------------------------------------------------------------- lighting -- */

  /**
   * One cold source, and it comes from the hole.
   *
   * Everything else in this room is the player's headlamp. The shaft is not
   * decorative — it is the only navigational fact in the chamber and the only
   * thing that says there is a building overhead.
   */
  private buildShaft(p: ReturnType<typeof profile>): void {
    const origin = new Vector3(HOLE_X + 0.42, 5.55, HOLE_Z - 0.55);
    const dir = new Vector3(-0.2, -1, 0.28).normalize();

    this.shaft = new SpotLight('voidShaft', origin, dir, 0.66, 1.5, this.scene);
    this.shaft.diffuse = C.moonlight;
    this.shaft.specular = C.moonlight.scale(0.7);
    // The headlamp is 42 at a metre; this has to travel five before it reaches
    // anything, so it needs an order more to hold its half of the frame.
    this.shaft.intensity = 820;
    this.shaft.range = 18;
    this.shaft.innerAngle = 0.2;
    this.shaft.falloffType = SpotLight.FALLOFF_PHYSICAL;
    this.shaft.shadowEnabled = false;

    // The visible column. Additive, fresnel-softened at the silhouette so it
    // has no cylinder edge, and faded out at the bottom by a gradient — a
    // hard-edged cone is worse than no cone at all.
    // Built as a tube along an explicit path rather than a rotated cylinder:
    // orienting a primitive by Euler angles is exactly the class of mistake
    // that does not show up until the capture comes back pointing at the
    // ceiling, and a path has no orientation to get wrong.
    const SEGS = 10;
    const LEN = 6.4;
    const R0 = 0.3;
    const R1 = 1.15;
    const path: Vector3[] = [];
    for (let i = 0; i <= SEGS; i++) path.push(origin.add(dir.scale((i / SEGS) * LEN)));
    const cone = MeshBuilder.CreateTube(
      'voidShaftCone',
      {
        path,
        radiusFunction: (i: number) => R0 + (i / SEGS) * (R1 - R0),
        tessellation: 20,
        cap: Mesh.NO_CAP,
        sideOrientation: Mesh.DOUBLESIDE,
      },
      this.scene,
    );
    this.beamOrigin = origin;
    this.beamDir = dir;
    this.beamLen = LEN;
    this.beamR0 = R0;
    this.beamR1 = R1;
    this.beam = cone;
    const cm = new StandardMaterial('shaftBeam', this.scene);
    cm.emissiveColor = C.moonlight.scale(0.5);
    cm.diffuseColor = Color3.Black();
    cm.specularColor = Color3.Black();
    cm.disableLighting = true;
    cm.backFaceCulling = false;
    cm.alpha = 0.1;
    cm.alphaMode = Constants.ALPHA_ADD;
    cm.opacityTexture = makeBeamGradient(this.scene);
    cm.opacityFresnelParameters = beamFresnel();
    cone.material = cm;
    cone.isPickable = false;
    cone.receiveShadows = false;
    cone.freezeWorldMatrix();
    this.meshes.push(cone);

    // A little bounce inside the sub-floor void so there is visibly a room up
    // there rather than a lamp in a box.
    const above = new PointLight('voidAbove', new Vector3(HOLE_X, 5.0, HOLE_Z), this.scene);
    above.diffuse = C.moonlight;
    above.specular = Color3.Black();
    above.intensity = 34;
    above.range = 4.2;
    this.above = above;

    // The sodium bleed through the ventilator, ninety metres and one wall away
    // from the nearest working lamp. Deliberately almost nothing.
    this.bleed = new PointLight('voidBleed', new Vector3(HALF_W + 0.5, 1.48, 19.3), this.scene);
    this.bleed.diffuse = C.sodiumVapour;
    this.bleed.specular = C.sodiumVapour.scale(0.4);
    this.bleed.intensity = 18;
    this.bleed.range = 8;

    // Dust in the shaft. In a sealed chamber this is the only thing that
    // moves, and it moves because a draught moves it — nothing else.
    if (p.particleBudget > 200) {
      const ps = new ParticleSystem('voidDust', Math.min(p.particleBudget, 900), this.scene);
      ps.particleTexture = makeDotTexture(this.scene);
      ps.emitter = new Vector3(HOLE_X - 0.1, 2.6, HOLE_Z + 0.5);
      ps.minEmitBox = new Vector3(-0.85, -2.5, -1.0);
      ps.maxEmitBox = new Vector3(0.85, 2.9, 1.0);
      ps.color1 = new Color4(0.72, 0.8, 0.96, 0.4);
      ps.color2 = new Color4(0.58, 0.68, 0.9, 0.18);
      ps.colorDead = new Color4(0.58, 0.68, 0.9, 0);
      ps.minSize = 0.006;
      ps.maxSize = 0.022;
      ps.minLifeTime = 8;
      ps.maxLifeTime = 18;
      ps.emitRate = 150;
      ps.blendMode = ParticleSystem.BLENDMODE_ADD;
      ps.gravity = new Vector3(0, -0.02, 0);
      ps.direction1 = new Vector3(-0.03, -0.05, -0.03);
      ps.direction2 = new Vector3(0.03, 0.01, 0.03);
      ps.minEmitPower = 0.005;
      ps.maxEmitPower = 0.03;
      ps.updateSpeed = 0.012;
      ps.start();
      this.dust = ps;
    }
  }

  /* ---------------------------------------------------------- inscriptions -- */

  /**
   * The names.
   *
   * A procedural inscription pass: 64 unique carvings are rendered into one
   * atlas — careful serif capitals, rough jittered capitals, half-legible
   * remains, scratched phrases, tally marks, and cold institutional register
   * numbers — and then placed as alpha-tested, normal-mapped quads onto
   * individual wall blocks, tilted a degree or two off level because nobody
   * carving in the dark works to a line.
   *
   * Every name is INVENTED. Real Joliet inmates of the quarry era are
   * identifiable people with living descendants, and putting a real man's name
   * on a fictional punishment wall would be a lie about a person rather than a
   * dramatisation of a fact. The names here are period-plausible for the
   * Illinois population of the 1860s–70s (Irish, German, Bohemian,
   * Scandinavian, English and Black American) and belong to nobody.
   */
  private buildInscriptions(ctx: ReturnType<GameScene['kit']>, rng: () => number): void {
    const { albedo, normal } = buildInscriptionAtlas(this.scene);

    const mat = new PBRMaterial('inscription', this.scene);
    mat.albedoTexture = albedo;
    mat.bumpTexture = normal;
    mat.useAlphaFromAlbedoTexture = true;
    mat.transparencyMode = PBRMaterial.PBRMATERIAL_ALPHATEST;
    mat.alphaCutOff = 0.4;
    mat.metallic = 0;
    mat.roughness = 0.86;
    mat.ambientColor = new Color3(1, 1, 1);
    mat.environmentIntensity = 0.5;
    mat.enableSpecularAntiAliasing = true;
    mat.maxSimultaneousLights = 8;
    mat.backFaceCulling = true;
    // Nudge toward the camera so the 6 mm physical offset never z-fights the
    // block face it is carved into.
    mat.zOffset = -2;
    (mat.bumpTexture as Texture).level = 1.35;
    mat.freeze();

    // Shuffle the atlas cells deterministically so neighbouring carvings are
    // never the same hand.
    const order: number[] = [];
    for (let i = 0; i < CELLS; i++) order.push(i);
    for (let i = order.length - 1; i > 0; i--) {
      const j = Math.floor(rng() * (i + 1));
      [order[i], order[j]] = [order[j], order[i]];
    }

    // Weighted selection.
    const pool = this.faces.filter((f) => f.forced || rng() < Math.min(0.85, 0.26 * f.weight));
    const batch = new GeoBatch();
    let placed = 0;

    for (const f of pool) {
      if (placed >= 140) break;
      const cell = order[placed % CELLS];
      const maxW = Math.min(f.w * 0.86, 0.44);
      const maxH = Math.min(f.h * 0.82, 0.44);
      // Not every hand had the same reach or the same nerve — a few are
      // deliberately small enough that you have to lean in.
      const size = Math.min(maxW, maxH) * (0.66 + rng() * 0.34);
      if (size < 0.14) continue;

      // Plane's own front normal is -Z; rotate it onto the wall normal.
      const yaw = f.nx < 0 ? Math.PI / 2 : f.nx > 0 ? -Math.PI / 2 : f.nz < 0 ? 0 : Math.PI;
      const rot = Matrix.RotationYawPitchRoll(yaw, 0, (rng() - 0.5) * 0.09);
      const vd = CreatePlaneVertexData({ width: size, height: size, sideOrientation: Mesh.DOUBLESIDE });
      remapUV(vd, cell);
      batch.template(
        vd,
        new Vector3(1, 1, 1),
        rot,
        new Vector3(
          f.x + f.nx * 0.007,
          f.y + (rng() - 0.5) * (f.h - size) * 0.5,
          f.z + f.nz * 0.007 + (rng() - 0.5) * (f.w - size) * 0.4,
        ),
      );
      placed++;
    }

    // Two on stones that fell out of the wall and landed name-up in the
    // rubble. Finding one of those on the floor is the moment the room lands.
    for (const [x, y, z, yaw] of [
      [-0.35, 0.36, 6.2, 0.4],
      [1.05, 0.24, 11.9, -1.1],
    ] as const) {
      const cell = order[(placed + 3) % CELLS];
      const vd = CreatePlaneVertexData({ width: 0.3, height: 0.3, sideOrientation: Mesh.DOUBLESIDE });
      remapUV(vd, cell);
      batch.template(
        vd,
        new Vector3(1, 1, 1),
        Matrix.RotationYawPitchRoll(yaw, -Math.PI / 2, 0),
        new Vector3(x, y, z),
      );
      placed++;
    }

    batch.finish(ctx, this.scene, 'voidInscriptions', mat, {
      collide: false,
      cast: false,
      keepUV: true,
    });
  }

  /**
   * Common brick for the seal — the one non-limestone surface in the room.
   *
   * Kept dark and desaturated on purpose: a bright orange brick reads as a
   * modern machine product and undercuts the whole point of the object, which
   * is that somebody closed this in a hurry with whatever was to hand.
   */
  private buildBrickMaterial(): PBRMaterial {
    const m = new PBRMaterial('sealBrick', this.scene);
    m.albedoColor = srgb('#65483c');
    m.metallic = 0;
    m.roughness = 0.93;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.4;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = 8;
    m.freeze();
    return m;
  }

  override update(dt: number, _player?: unknown): void {
    this.t += dt;
    // The shaft breathes very slightly — cloud passing a window four floors
    // up, nothing more. If it reads as an effect it is too strong.
    if (this.shaft) {
      this.shaft.intensity = 820 * (1 + Math.sin(this.t * 0.21) * 0.045);
    }

    // Hide the light column whenever the camera is inside it. The player walks
    // through this beam to reach the rest of the chamber, and a double-sided
    // additive tube seen from within becomes a set of enormous translucent
    // facets smeared across the whole frame — which is precisely what one
    // capture came back showing.
    const cam = this.scene.activeCamera;
    if (this.beam && cam) {
      const rel = cam.globalPosition.subtract(this.beamOrigin);
      const along = Vector3.Dot(rel, this.beamDir);
      let inside = false;
      if (along > -0.6 && along < this.beamLen + 0.6) {
        const t = Math.max(0, Math.min(1, along / this.beamLen));
        const radial = rel.subtract(this.beamDir.scale(along)).length();
        inside = radial < (this.beamR0 + t * (this.beamR1 - this.beamR0)) * 1.5;
      }
      if (this.beam.isEnabled() === inside) this.beam.setEnabled(!inside);
    }
  }

  override dispose(): void {
    this.dust?.dispose();
    this.shaft?.dispose();
    this.bleed?.dispose();
    this.above?.dispose();
    super.dispose();
  }
}

/* ========================================================================== */
/*  Geometry batching                                                         */
/* ========================================================================== */

interface CarveFace {
  x: number;
  y: number;
  z: number;
  /** Outward normal of the face, in x and z. */
  nx: number;
  nz: number;
  w: number;
  h: number;
  weight: number;
  /** Always carved, regardless of the dice — used to protect anchor frames. */
  forced?: boolean;
}

/** Shared unit-box template. Built once, transformed thousands of times. */
const BOX = CreateBoxVertexData({ size: 1 });

/**
 * A CPU-side mesh accumulator.
 *
 * This room is roughly 1,400 individually-placed stones. Creating 1,400
 * `Mesh`es and calling `MergeMeshes` would allocate and immediately discard
 * about six thousand GL buffers; appending transformed vertex data into plain
 * arrays and building one mesh at the end costs nothing and is what makes the
 * "every block is its own stone" approach affordable at all.
 *
 * UVs are deliberately NOT written here — the batch bakes world positions into
 * the vertices, so `worldUV` at the end gives every block a different patch of
 * the limestone texture for free. That is the whole trick: no two blocks in
 * this chamber sample the same texels.
 */
class GeoBatch {
  private positions: number[] = [];
  private normals: number[] = [];
  private uvs: number[] = [];
  private indices: number[] = [];
  private hasUV = false;
  private base = 0;

  box(
    x: number,
    y: number,
    z: number,
    w: number,
    h: number,
    d: number,
    rx = 0,
    ry = 0,
    rz = 0,
  ): void {
    const rot = rx || ry || rz ? Matrix.RotationYawPitchRoll(ry, rx, rz) : null;
    this.append(BOX, w, h, d, rot, x, y, z);
  }

  template(vd: VertexData, scale: Vector3, rot: Matrix | null, pos: Vector3): void {
    this.append(vd, scale.x, scale.y, scale.z, rot, pos.x, pos.y, pos.z);
  }

  private append(
    vd: VertexData,
    sx: number,
    sy: number,
    sz: number,
    rot: Matrix | null,
    tx: number,
    ty: number,
    tz: number,
  ): void {
    const src = vd.positions as ArrayLike<number>;
    const nrm = vd.normals as ArrayLike<number>;
    const idx = vd.indices as ArrayLike<number>;
    const uv = vd.uvs as ArrayLike<number> | null | undefined;

    const m = rot ? rot.m : null;
    for (let i = 0; i < src.length; i += 3) {
      let px = src[i] * sx;
      let py = src[i + 1] * sy;
      let pz = src[i + 2] * sz;
      let nx = nrm[i];
      let ny = nrm[i + 1];
      let nz = nrm[i + 2];
      if (m) {
        const qx = px * m[0] + py * m[4] + pz * m[8];
        const qy = px * m[1] + py * m[5] + pz * m[9];
        const qz = px * m[2] + py * m[6] + pz * m[10];
        px = qx;
        py = qy;
        pz = qz;
        const ax = nx * m[0] + ny * m[4] + nz * m[8];
        const ay = nx * m[1] + ny * m[5] + nz * m[9];
        const az = nx * m[2] + ny * m[6] + nz * m[10];
        nx = ax;
        ny = ay;
        nz = az;
      }
      this.positions.push(px + tx, py + ty, pz + tz);
      this.normals.push(nx, ny, nz);
    }
    if (uv && uv.length) {
      this.hasUV = true;
      for (let i = 0; i < uv.length; i++) this.uvs.push(uv[i]);
    }
    for (let i = 0; i < idx.length; i++) this.indices.push(idx[i] + this.base);
    this.base += src.length / 3;
  }

  finish(
    ctx: { register: (m: Mesh, o?: Record<string, unknown>) => void },
    scene: Scene,
    name: string,
    material: PBRMaterial,
    opts: {
      collide?: boolean;
      cast?: boolean;
      surface?: string;
      uvDensity?: number;
      keepUV?: boolean;
    },
  ): Mesh | null {
    if (!this.indices.length) return null;
    const mesh = new Mesh(name, scene);
    const vd = new VertexData();
    vd.positions = this.positions;
    vd.normals = this.normals;
    vd.indices = this.indices;
    if (this.hasUV) vd.uvs = this.uvs;
    else vd.uvs = new Array((this.positions.length / 3) * 2).fill(0);
    vd.applyToMesh(mesh, false);
    mesh.material = material;
    ctx.register(mesh, opts);
    return mesh;
  }
}

/* ========================================================================== */
/*  The inscription atlas                                                     */
/* ========================================================================== */

const ATLAS = 2048;
const GRID = 8;
const CELL = ATLAS / GRID;
const CELLS = GRID * GRID;
const PAD = 20;

type Hand =
  /** A literate man taking his time. Serif capitals, even baseline. */
  | 'careful'
  /** A blunt tool and a hurry. Sans capitals, jittered. */
  | 'rough'
  /** Ninety years of damp has taken most of it. */
  | 'faint'
  /** Scratched with something that was not a chisel. */
  | 'scratch'
  /** Days. */
  | 'tally'
  /** Not a name at all — a register number, or a quarry mark. */
  | 'stamp';

interface Carving {
  text: string;
  hand: Hand;
}

/**
 * 64 inscriptions.
 *
 * All names are invented (see `buildInscriptions`). The registry numbers, the
 * gang number, the stone marks and the dates are invented too. The intent is
 * that a player reading the wall closely finds the same thing a researcher
 * would: mostly names and dates, a handful of tallies, a few sentences that
 * were worth the effort of cutting, and — coldest of all — men recorded by
 * number instead.
 */
const INSCRIPTIONS: Carving[] = [
  { text: 'J. MERRICK\n1863', hand: 'careful' },
  { text: 'THOS.\nCALLAN', hand: 'careful' },
  { text: 'WM. PRYOR\n1859', hand: 'careful' },
  { text: 'A. HOLMBERG', hand: 'careful' },
  { text: 'E. VAN\nDER KAMP', hand: 'careful' },
  { text: 'H. STRAUB\n1864', hand: 'careful' },
  { text: 'P. GALLAGHER', hand: 'careful' },
  { text: 'MOSES REDD', hand: 'careful' },
  { text: 'C. NOVOTNY\n1877', hand: 'careful' },
  { text: "SAM'L\nO'KEEFE", hand: 'careful' },
  { text: 'D. LOWRY\n1861', hand: 'careful' },
  { text: 'F. BRENNEMAN', hand: 'careful' },

  { text: 'ISAAC TULL', hand: 'rough' },
  { text: 'R. McQUADE\n1869', hand: 'rough' },
  { text: 'J. B. ANSTED', hand: 'rough' },
  { text: 'L. FERRARO', hand: 'rough' },
  { text: 'G. PLUMB', hand: 'rough' },
  { text: 'TOM ASHE\n1866', hand: 'rough' },
  { text: 'W. KEHOE', hand: 'rough' },
  { text: 'N. SOBOTKA', hand: 'rough' },
  { text: 'E. DRISCOLL', hand: 'rough' },
  { text: 'J. HAAKON\n1874', hand: 'rough' },
  { text: 'A. CRUMP', hand: 'rough' },
  { text: 'S. WEIDNER', hand: 'rough' },
  { text: 'B. FOLEY\n1858', hand: 'rough' },
  { text: 'M. TIERNAN', hand: 'rough' },

  { text: 'J. OSTRANDER', hand: 'faint' },
  { text: 'R. SEELY', hand: 'faint' },
  { text: 'W. AMSDEN\n186', hand: 'faint' },
  { text: 'ELIAS\nBURKE', hand: 'faint' },
  { text: 'H. DELANEY', hand: 'faint' },
  { text: 'C. RAU', hand: 'faint' },
  { text: 'P. MAGUIRE', hand: 'faint' },
  { text: 'A. THORNE', hand: 'faint' },

  { text: 'No 1147', hand: 'stamp' },
  { text: 'No 0913', hand: 'stamp' },
  { text: 'No 2206', hand: 'stamp' },
  { text: 'No 738', hand: 'stamp' },
  { text: 'No 3051', hand: 'stamp' },
  { text: 'STONE\n4412', hand: 'stamp' },
  { text: 'QUARRY\nGANG 3', hand: 'stamp' },
  { text: 'CUT No 19', hand: 'stamp' },

  { text: '1859', hand: 'careful' },
  { text: 'MCH\n1867', hand: 'rough' },
  { text: 'APRIL\n1871', hand: 'careful' },
  { text: '1862', hand: 'rough' },
  { text: 'NOV\n1875', hand: 'faint' },
  { text: 'OCT 12\n1866', hand: 'careful' },
  { text: '1878', hand: 'rough' },
  { text: 'FEB\n1860', hand: 'faint' },

  { text: '17', hand: 'tally' },
  { text: '23', hand: 'tally' },
  { text: '9', hand: 'tally' },
  { text: '31', hand: 'tally' },
  { text: '12', hand: 'tally' },
  { text: '48', hand: 'tally' },

  { text: 'MOTHER\nI AM WELL', hand: 'scratch' },
  { text: 'WE CUT\nTHIS STONE', hand: 'scratch' },
  { text: 'SEND WORD\nTO ELLEN', hand: 'scratch' },
  { text: 'STILL HERE', hand: 'scratch' },
  { text: 'NO SUN\nSINCE MAY', hand: 'scratch' },
  { text: 'GOD SEES', hand: 'scratch' },
  { text: 'LET ME UP', hand: 'scratch' },
  { text: 'BUILT BY US', hand: 'scratch' },
];

/**
 * Render every inscription into one atlas and derive an albedo (with alpha)
 * and a tangent-space normal from it.
 *
 * The carve is a real height field, not a painted shadow: the mask becomes a
 * groove, the groove becomes a normal map, and the headlamp does the rest.
 * Painting the shading in would read correctly from exactly one angle, and
 * this is a scene the player is expected to walk along with a light in their
 * hand.
 */
function buildInscriptionAtlas(scene: Scene): { albedo: Texture; normal: Texture } {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = ATLAS;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, ATLAS, ATLAS);
  ctx.fillStyle = '#fff';
  ctx.strokeStyle = '#fff';
  ctx.textBaseline = 'middle';
  ctx.textAlign = 'left';

  const rng = mulberry(19100617); // the year it left the surveys
  const wear = new Float32Array(CELLS);

  for (let c = 0; c < CELLS; c++) {
    const carving = INSCRIPTIONS[c % INSCRIPTIONS.length];
    const cx = (c % GRID) * CELL;
    const cy = Math.floor(c / GRID) * CELL;
    wear[c] =
      carving.hand === 'faint' ? 0.62 : carving.hand === 'scratch' ? 0.34 : 0.12 + rng() * 0.26;
    drawCarving(ctx, carving, cx, cy, rng);
  }

  const img = ctx.getImageData(0, 0, ATLAS, ATLAS).data;

  // Erosion field, evaluated at 1/8 resolution and bilinearly sampled — full
  // resolution fBm over four million pixels is seconds of single-threaded JS
  // and buys nothing at this scale.
  const NS = 256;
  const noise = new Float32Array(NS * NS);
  for (let y = 0; y < NS; y++) {
    for (let x = 0; x < NS; x++) {
      noise[y * NS + x] = fbm((x / NS) * 26, (y / NS) * 26, 26, 4, 4412);
    }
  }
  const sampleNoise = (x: number, y: number): number => {
    const fx = (x / ATLAS) * NS;
    const fy = (y / ATLAS) * NS;
    const x0 = Math.floor(fx) % NS;
    const y0 = Math.floor(fy) % NS;
    const x1 = (x0 + 1) % NS;
    const y1 = (y0 + 1) % NS;
    const tx = fx - Math.floor(fx);
    const ty = fy - Math.floor(fy);
    const a = noise[y0 * NS + x0] * (1 - tx) + noise[y0 * NS + x1] * tx;
    const b = noise[y1 * NS + x0] * (1 - tx) + noise[y1 * NS + x1] * tx;
    return a * (1 - ty) + b * ty;
  };

  // Build the height field with rows already flipped into texture space (row 0
  // is v = 0), so the normal map and the albedo agree and nothing has to be
  // inverted afterwards.
  const height = new Float32Array(ATLAS * ATLAS);
  const albedo = new Uint8ClampedArray(ATLAS * ATLAS * 4);

  // The interior of a fresh chisel cut in dolomitic limestone is paler than
  // the weathered face around it, then fills with grime. Both are present.
  const cutDark = [26, 24, 21];
  const cutPale = [122, 116, 100];

  for (let y = 0; y < ATLAS; y++) {
    const srcRow = (ATLAS - 1 - y) * ATLAS;
    const cellRow = Math.floor((ATLAS - 1 - y) / CELL);
    for (let x = 0; x < ATLAS; x++) {
      let m = img[(srcRow + x) * 4] / 255;
      if (m > 0) {
        const cellIdx = cellRow * GRID + Math.floor(x / CELL);
        const w = wear[cellIdx];
        const n = sampleNoise(x, y);
        // Wear eats the shallow parts of the cut first, which is exactly how
        // a half-legible inscription actually fails.
        m *= clamp01((n - w) * 3.4 + 0.72);
        m = clamp01(m);
      }
      height[y * ATLAS + x] = -m;

      const i = (y * ATLAS + x) * 4;
      const grime = 0.35 + sampleNoise(x * 1.7, y * 1.7) * 0.5;
      albedo[i] = cutDark[0] + (cutPale[0] - cutDark[0]) * (1 - grime) * (1 - m * 0.55);
      albedo[i + 1] = cutDark[1] + (cutPale[1] - cutDark[1]) * (1 - grime) * (1 - m * 0.55);
      albedo[i + 2] = cutDark[2] + (cutPale[2] - cutDark[2]) * (1 - grime) * (1 - m * 0.55);
      albedo[i + 3] = clamp01(m * 2.4) * 255;
    }
  }

  const normalData = heightToNormal(height, ATLAS, 3.2);

  const albedoTex = rawTexture(scene, albedo, 'inscriptionAlbedo', true);
  albedoTex.hasAlpha = true;
  const normalTex = rawTexture(scene, normalData, 'inscriptionNormal', false);
  return { albedo: albedoTex, normal: normalTex };
}

function rawTexture(
  scene: Scene,
  data: Uint8ClampedArray,
  name: string,
  gamma: boolean,
): Texture {
  const tex = RawTexture.CreateRGBATexture(
    new Uint8Array(data.buffer),
    ATLAS,
    ATLAS,
    scene,
    true,
    false,
    Texture.TRILINEAR_SAMPLINGMODE,
    Constants.TEXTURETYPE_UNSIGNED_BYTE,
  );
  tex.name = name;
  tex.wrapU = Texture.CLAMP_ADDRESSMODE;
  tex.wrapV = Texture.CLAMP_ADDRESSMODE;
  tex.anisotropicFilteringLevel = 8;
  (tex as Texture & { gammaSpace: boolean }).gammaSpace = gamma;
  return tex;
}

/** Draw one inscription, white on black, inside its atlas cell. */
function drawCarving(
  ctx: CanvasRenderingContext2D,
  carving: Carving,
  cx: number,
  cy: number,
  rng: () => number,
): void {
  const inner = CELL - PAD * 2;
  ctx.save();
  ctx.translate(cx + PAD, cy + PAD);

  if (carving.hand === 'tally') {
    drawTally(ctx, parseInt(carving.text, 10), inner, rng);
    ctx.restore();
    return;
  }

  const lines = carving.text.split('\n');
  const font =
    carving.hand === 'careful'
      ? 'bold {S}px Georgia, "Times New Roman", serif'
      : carving.hand === 'stamp'
        ? 'bold {S}px "Courier New", monospace'
        : carving.hand === 'scratch'
          ? '{S}px "Arial Narrow", Helvetica, sans-serif'
          : 'bold {S}px Helvetica, Arial, sans-serif';

  const jitter = carving.hand === 'careful' ? 0.16 : carving.hand === 'stamp' ? 0.04 : 1;
  const stroke = carving.hand === 'scratch';

  // Shrink to fit. Long phrases get small and cramped, which is right — a man
  // with a nail and a limited stretch of stone writes small.
  let size = Math.floor(inner / Math.max(1.9, lines.length * 1.35));
  for (let guard = 0; guard < 24; guard++) {
    ctx.font = font.replace('{S}', String(size));
    const widest = Math.max(...lines.map((l) => measureTracked(ctx, l, size)));
    if (widest <= inner * 0.96 || size <= 12) break;
    size = Math.floor(size * 0.92);
  }
  ctx.font = font.replace('{S}', String(size));

  const lh = size * 1.22;
  const top = inner / 2 - ((lines.length - 1) * lh) / 2;
  ctx.lineWidth = Math.max(2.5, size * 0.075);
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';

  for (let i = 0; i < lines.length; i++) {
    drawTracked(ctx, lines[i], inner / 2, top + i * lh, size, jitter, rng, stroke);
  }

  // A rule scored under a careful hand, or a stray slip from a rough one.
  if (carving.hand === 'careful' && rng() < 0.35) {
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(inner * 0.2, top + (lines.length - 1) * lh + size * 0.85);
    ctx.lineTo(inner * 0.8 + (rng() - 0.5) * 20, top + (lines.length - 1) * lh + size * 0.85 + (rng() - 0.5) * 6);
    ctx.stroke();
  }
  if (carving.hand === 'scratch') {
    ctx.lineWidth = 2;
    for (let i = 0; i < 3; i++) {
      ctx.beginPath();
      const x0 = rng() * inner;
      const y0 = rng() * inner;
      ctx.moveTo(x0, y0);
      ctx.lineTo(x0 + (rng() - 0.5) * inner * 0.4, y0 + (rng() - 0.5) * inner * 0.2);
      ctx.stroke();
    }
  }

  ctx.restore();
}

function measureTracked(ctx: CanvasRenderingContext2D, text: string, size: number): number {
  const chars = [...text];
  let w = 0;
  for (const c of chars) w += ctx.measureText(c).width;
  return w + size * 0.09 * Math.max(0, chars.length - 1);
}

function drawTracked(
  ctx: CanvasRenderingContext2D,
  text: string,
  cx: number,
  y: number,
  size: number,
  jitter: number,
  rng: () => number,
  stroke: boolean,
): void {
  const chars = [...text];
  const widths = chars.map((c) => ctx.measureText(c).width);
  const track = size * 0.09;
  const total = widths.reduce((a, b) => a + b, 0) + track * Math.max(0, chars.length - 1);
  let x = cx - total / 2;
  for (let i = 0; i < chars.length; i++) {
    ctx.save();
    ctx.translate(x + widths[i] / 2, y + (rng() - 0.5) * jitter * size * 0.11);
    ctx.rotate((rng() - 0.5) * jitter * 0.1);
    if (stroke) ctx.strokeText(chars[i], -widths[i] / 2, 0);
    else ctx.fillText(chars[i], -widths[i] / 2, 0);
    ctx.restore();
    x += widths[i] + track;
  }
}

/** Days, in fives. Counting is the only thing left to do. */
function drawTally(
  ctx: CanvasRenderingContext2D,
  count: number,
  inner: number,
  rng: () => number,
): void {
  const perRow = 15;
  const rows = Math.ceil(count / perRow);
  const gap = inner / (perRow + 2);
  const h = Math.min(inner / (rows * 1.9), gap * 3.2);
  ctx.lineWidth = Math.max(3.5, gap * 0.34);
  ctx.lineCap = 'round';

  for (let i = 0; i < count; i++) {
    const row = Math.floor(i / perRow);
    const col = i % perRow;
    const group = Math.floor(col / 5);
    const x = gap * (1 + col + group * 0.5);
    const y = inner / 2 - ((rows - 1) * h * 1.7) / 2 + row * h * 1.7;
    ctx.beginPath();
    if (col % 5 === 4) {
      // The fifth stroke goes across the other four.
      ctx.moveTo(x - gap * 4.1, y + h / 2 + (rng() - 0.5) * 4);
      ctx.lineTo(x + gap * 0.3, y - h / 2 + (rng() - 0.5) * 4);
    } else {
      ctx.moveTo(x + (rng() - 0.5) * 3, y - h / 2 + (rng() - 0.5) * 4);
      ctx.lineTo(x + (rng() - 0.5) * 3, y + h / 2 + (rng() - 0.5) * 4);
    }
    ctx.stroke();
  }
}

/** Point a unit-square plane's UVs at one atlas cell. */
function remapUV(vd: VertexData, cell: number): void {
  const uv = vd.uvs as number[] | Float32Array | null;
  if (!uv) return;
  const col = cell % GRID;
  const row = GRID - 1 - Math.floor(cell / GRID);
  const s = 1 / GRID;
  for (let i = 0; i < uv.length; i += 2) {
    uv[i] = (col + uv[i]) * s;
    uv[i + 1] = (row + uv[i + 1]) * s;
  }
}

/* ========================================================================== */

/** The same deterministic PRNG 1.1 uses, so captures are byte-stable. */
function mulberry(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Vertical fade for the light column: strongest just under the opening, gone
 * before it reaches the floor. Real shafts are only visible where there is
 * enough dust in them, and they never end in a hard disc.
 */
function makeBeamGradient(scene: Scene): Texture {
  const w = 8;
  const h = 128;
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const c = canvas.getContext('2d')!;
  // Deliberately near-symmetric: which end of the tube v = 0 lands on depends
  // on the texture's Y convention, and a beam that is soft at both ends reads
  // correctly either way.
  // Greyscale, fully opaque, because `getAlphaFromRGB` reads the *luminance*
  // — a gradient painted in the alpha channel comes back as a flat white
  // opacity map and the beam gets a hard end.
  const g = c.createLinearGradient(0, 0, 0, h);
  g.addColorStop(0.0, '#000');
  g.addColorStop(0.22, '#fff');
  g.addColorStop(0.62, '#b4b4b4');
  g.addColorStop(1.0, '#000');
  c.fillStyle = g;
  c.fillRect(0, 0, w, h);
  const t = new Texture(canvas.toDataURL('image/png'), scene, true, false);
  t.wrapU = Texture.CLAMP_ADDRESSMODE;
  t.wrapV = Texture.CLAMP_ADDRESSMODE;
  t.getAlphaFromRGB = true;
  return t;
}

/** Kill the beam's alpha at its silhouette so the cylinder has no edge. */
function beamFresnel(): FresnelParameters {
  const f = new FresnelParameters();
  f.isEnabled = true;
  f.bias = 0.12;
  f.power = 2.2;
  f.leftColor = Color3.Black(); // grazing → invisible
  f.rightColor = Color3.White(); // head-on → full
  return f;
}

/** A soft round dot for the dust. Generated, not shipped. */
function makeDotTexture(scene: Scene): Texture {
  const size = 32;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const c = canvas.getContext('2d')!;
  const g = c.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.4, 'rgba(255,255,255,0.5)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  c.fillStyle = g;
  c.fillRect(0, 0, size, size);
  const t = new Texture(canvas.toDataURL('image/png'), scene, true, false);
  t.hasAlpha = true;
  return t;
}
