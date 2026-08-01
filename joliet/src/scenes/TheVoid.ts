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
import { SpotLight } from '@babylonjs/core/Lights/spotLight';
import { PointLight } from '@babylonjs/core/Lights/pointLight';
import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { RawTexture } from '@babylonjs/core/Materials/Textures/rawTexture';
import { Constants } from '@babylonjs/core/Engines/constants';
import type { Scene } from '@babylonjs/core/scene';

import '@babylonjs/core/Particles/particleSystemComponent';

import { GameScene, type SceneManifest } from './SceneBase';
import { worldUV } from '../core/Kit';
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
        position: [0.5, 1.3, 4.7],
        rotation: [Math.PI, -0.72],
        note: 'Straight up into the break-in. Tests the broken floor slab, snapped joists, rim stones and the lit dust — the one moment the room admits there is a building above it.',
      },
      {
        name: 'a3-names',
        position: [1.1, 1.24, 10.6],
        rotation: [Math.PI / 2, 0.06],
        note: 'THE scene. Reading distance (0.9 m) on the east wall under headlamp. Tests inscription legibility, the carve normal, and block-face relief. If the names cannot be read here, nothing else matters.',
      },
      {
        name: 'a4-niche',
        position: [0.62, 1.0, 8.9],
        rotation: [Math.PI / 2, 0.12],
        note: 'The mouth of a punishment niche: iron staple, tally marks, low arched head. Tests tight-space headlamp falloff and that the niche reads as a place a person was put.',
      },
      {
        name: 'a5-seal',
        position: [0.05, 1.5, 17.2],
        rotation: [0, 0.04],
        note: 'The brick seal at the far end over standing water. Tests brick-vs-limestone material contrast, the water clear coat, and the payload: someone did this deliberately.',
      },
    ],
  };

  private shaft!: SpotLight;
  private bleed?: PointLight;
  private dust?: ParticleSystem;
  private t = 0;

  /** Wall faces the inscription pass is allowed to carve into. */
  private faces: CarveFace[] = [];

  async build(): Promise<void> {
    const ctx = this.kit();
    const p = profile();
    const rng = mulberry(18580412); // Boyington's office, allegedly

    // ---- Materials -------------------------------------------------------
    const stone = this.mats.get('limestone.wall');
    const wet = this.mats.get('limestone.wet');
    const slab = this.mats.get('concrete.slab');
    const water = this.mats.get('water.standing');
    const steel = this.mats.get('steel.catwalk');
    const timber = this.mats.get('timber.rotten');

    // Five lights can be in play here (moon, sky bounce, the shaft, the vent
    // bleed, and the headlamp). PBRMaterial defaults to four, and because the
    // player's headlamp is created *after* the scene it is the one that gets
    // dropped — in a headlamp scene. Raise the ceiling on everything used here.
    for (const id of [
      'limestone.wall',
      'limestone.wet',
      'concrete.slab',
      'water.standing',
      'steel.catwalk',
      'timber.rotten',
    ] as const) {
      this.mats.mutate(id, (m) => {
        m.maxSimultaneousLights = 6;
      });
    }

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
    this.buildVault(dry, rng);
    this.buildOuterMass(dry);
    this.buildBreakIn(dry, rubbleBatch, slabBatch, timberBatch, steelBatch, rng);
    this.buildSeal(dry, brickBatch, rng);
    this.buildCollapse(rubbleBatch, timberBatch, rng);
    this.buildVent(dry, steelBatch);

    dry.finish(ctx, this.scene, 'voidStone', stone, { collide: false, cast: true });
    damp.finish(ctx, this.scene, 'voidStoneWet', wet, { collide: false, cast: true });
    brickBatch.finish(ctx, this.scene, 'voidSeal', brick, {
      collide: false,
      cast: true,
      uvDensity: 1.1,
    });
    rubbleBatch.finish(ctx, this.scene, 'voidRubble', stone, {
      collide: true,
      cast: true,
      surface: 'stone',
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
    ctx.register(upper, { collide: true, cast: false, surface: 'stone' });

    // Lower floor: the far end has settled (or was always cut deeper), and it
    // holds water.
    const lower = MeshBuilder.CreateBox(
      'voidFloorLower',
      { width: HALF_W * 2 + 1.6, height: 0.6, depth: Z_END - Z_STEP + 2.2 },
      this.scene,
    );
    lower.position.set(0, FLOOR_LOW - 0.3, (Z_STEP + Z_END + 2.2) / 2 - 0.1);
    lower.material = wet;
    ctx.register(lower, { collide: true, cast: false, surface: 'water' });

    // Standing water. Alpha-blended, never a shadow caster, never pickable —
    // the same rules 1.1's trench water follows.
    const pool = MeshBuilder.CreateGround(
      'voidWater',
      { width: HALF_W * 2 - 0.04, height: Z_END - Z_STEP + 1.4, subdivisions: 14 },
      this.scene,
    );
    pool.position.set(0, WATER_Y, (Z_STEP + Z_END) / 2 + 0.3);
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
      uvDensity: 0.5,
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
      let y = 0;
      let course = 0;
      while (y < SPRING - 0.02) {
        const h = Math.min(0.32 + rng() * 0.17, SPRING - y);
        // Every course starts at a different offset, so the vertical joints
        // never line up into a grid.
        let z = -0.6 + rng() * 0.55;
        while (z < Z_END + 0.6) {
          const len = 0.42 + rng() * 0.52;
          const zc = z + len / 2;
          const centreY = y + h / 2;

          if (!this.inNicheOpening(side, zc, len, centreY, h)) {
            // Rising damp: the bottom two courses and everything past the step
            // are saturated.
            const soaked = y < 0.62 || zc > Z_STEP - 1.2;
            const batch = soaked ? damp : dry;
            const proud = -0.008 + rng() * 0.032;
            const depth = 0.38 + rng() * 0.1;
            const faceX = side * (HALF_W - proud);
            batch.box(
              faceX + side * (depth / 2),
              centreY,
              zc,
              depth,
              h * 0.985,
              len * 0.985,
              (rng() - 0.5) * 0.012,
              (rng() - 0.5) * 0.012,
              (rng() - 0.5) * 0.01,
            );

            // Big enough, dry enough and at a height a man could reach while
            // sitting or standing: a candidate for carving.
            if (h > 0.33 && len > 0.5 && centreY > 0.42 && centreY < 1.62) {
              this.faces.push({
                x: faceX,
                y: centreY,
                z: zc,
                nx: -side,
                nz: 0,
                w: len,
                h,
                weight: 1,
              });
            }
          }
          z += len + 0.012;
        }
        y += h + 0.012;
        course++;
      }
    }

    // End wall behind the player (the chamber continues into rubble that way,
    // so it is a collapsed face rather than a built one).
    for (let i = 0; i < 40; i++) {
      dry.box(
        -2.1 + rng() * 4.2,
        0.1 + rng() * 3.2,
        -0.9 + rng() * 0.8,
        0.5 + rng() * 0.4,
        0.3 + rng() * 0.3,
        0.4 + rng() * 0.4,
        (rng() - 0.5) * 0.5,
        rng() * Math.PI,
        (rng() - 0.5) * 0.5,
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
        const h = Math.min(0.26 + rng() * 0.14, NICHE_H - 0.1 - y);
        let z = n.z - NICHE_HALF_Z;
        while (z < n.z + NICHE_HALF_Z - 0.02) {
          const len = Math.min(0.3 + rng() * 0.3, n.z + NICHE_HALF_Z - z);
          const proud = rng() * 0.026;
          const faceX = backX - s * proud;
          damp.box(
            faceX + s * 0.2,
            y + h / 2,
            z + len / 2,
            0.4,
            h * 0.98,
            len * 0.98,
            (rng() - 0.5) * 0.01,
            0,
            (rng() - 0.5) * 0.01,
          );
          if (h > 0.24 && len > 0.34 && y > 0.16) {
            this.faces.push({
              x: faceX,
              y: y + h / 2,
              z: z + len / 2,
              nx: -s,
              nz: 0,
              w: len,
              h,
              // Men were left in here. This is where the carving would happen.
              weight: 4,
            });
          }
          z += len + 0.01;
        }
        y += h + 0.01;
      }

      // Jambs.
      for (const dz of [-1, 1]) {
        let jy = 0;
        while (jy < NICHE_H - 0.06) {
          const h = 0.28 + rng() * 0.12;
          damp.box(
            s * (HALF_W + NICHE_DEPTH / 2),
            jy + h / 2,
            n.z + dz * (NICHE_HALF_Z + 0.12),
            NICHE_DEPTH,
            Math.min(h, NICHE_H - 0.06 - jy) * 0.98,
            0.24,
            0,
            0,
            0,
          );
          jy += h + 0.01;
        }
      }

      // Segmental head — five voussoirs on a shallow arc, springing at 1.06.
      const headSpring = 1.06;
      const headRise = NICHE_H - headSpring;
      for (let i = 0; i < 5; i++) {
        const a = ((i + 0.5) / 5 - 0.5) * Math.PI;
        const zc = n.z + Math.sin(a) * NICHE_HALF_Z * 1.02;
        const yc = headSpring + Math.cos(a) * headRise;
        damp.box(
          s * (HALF_W + NICHE_DEPTH / 2),
          yc + 0.09,
          zc,
          NICHE_DEPTH + 0.02,
          0.19,
          (NICHE_HALF_Z * 2.3) / 5,
          -a,
          0,
          0,
        );
      }

      // Sill / floor of the niche, worn hollow.
      damp.box(
        s * (HALF_W + NICHE_DEPTH / 2),
        0.055,
        n.z,
        NICHE_DEPTH,
        0.11,
        NICHE_HALF_Z * 2,
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
  private buildVault(dry: GeoBatch, rng: () => number): void {
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
        const proud = rng() * 0.026; // some stones hang below their neighbours
        const seg = (Math.PI / perRing) * ((HALF_W + RISE) / 2) * 1.1;

        // Rotate so the block's local +Y is the outward normal.
        const psi = Math.atan2(-nx, ny);

        dry.box(
          px + nx * (thick / 2 - proud),
          py + ny * (thick / 2 - proud),
          zc,
          seg,
          thick,
          ringDepth * 0.97,
          (rng() - 0.5) * 0.02,
          (rng() - 0.5) * 0.016,
          psi + (rng() - 0.5) * 0.026,
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
    for (const side of [-1, 1] as const) {
      dry.box(
        side * (HALF_W + NICHE_DEPTH + 0.75),
        1.9,
        (Z_END + 0.4) / 2,
        1.5,
        4.4,
        Z_END + 2.6,
      );
    }
    // Cap over the vault, in four pieces around the break-in.
    const capY = SPRING + RISE + 0.55;
    const capH = 1.0;
    dry.box(0, capY, HOLE_Z - HOLE_HALF_Z - 1.5, 8, capH, 3.0);
    dry.box(0, capY, (HOLE_Z + HOLE_HALF_Z + Z_END + 1) / 2, 8, capH, Z_END + 1 - HOLE_Z - HOLE_HALF_Z);
    for (const side of [-1, 1] as const) {
      dry.box(
        side * (HOLE_X + side * (HOLE_HALF_X + 1.6)),
        capY,
        HOLE_Z,
        3.2,
        capH,
        HOLE_HALF_Z * 2,
      );
    }
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
    // Jagged rim stones around the opening — broken, not cut.
    for (let i = 0; i < 26; i++) {
      const a = (i / 26) * Math.PI * 2;
      const rx = HOLE_HALF_X * (0.92 + rng() * 0.3);
      const rz = HOLE_HALF_Z * (0.92 + rng() * 0.3);
      const x = HOLE_X + Math.cos(a) * rx;
      const z = HOLE_Z + Math.sin(a) * rz;
      const y = SPRING + RISE * Math.cos(Math.asin(clamp01(Math.abs(x) / HALF_W)));
      dry.box(
        x,
        y + 0.1 + rng() * 0.16,
        z,
        0.2 + rng() * 0.26,
        0.22 + rng() * 0.28,
        0.2 + rng() * 0.26,
        (rng() - 0.5) * 0.9,
        rng() * Math.PI,
        (rng() - 0.5) * 0.9,
      );
    }

    // The shaft up: four walls of the sub-floor void above, open at the top so
    // the light source has somewhere to be.
    const shaftTop = 5.7;
    const shaftBase = SPRING + RISE + 0.1;
    for (const [dx, dz, w, d] of [
      [HOLE_HALF_X + 0.3, 0, 0.6, HOLE_HALF_Z * 2 + 1.2],
      [-(HOLE_HALF_X + 0.3), 0, 0.6, HOLE_HALF_Z * 2 + 1.2],
      [0, HOLE_HALF_Z + 0.3, HOLE_HALF_X * 2 + 1.2, 0.6],
      [0, -(HOLE_HALF_Z + 0.3), HOLE_HALF_X * 2 + 1.2, 0.6],
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

    // Two snapped joists across the opening. One still spans it; one has come
    // down and is lying in the rubble.
    timber.box(HOLE_X - 0.15, shaftBase + 0.42, HOLE_Z - 0.5, 2.5, 0.18, 0.11, 0, 0, 0.03);
    timber.box(HOLE_X + 0.9, 0.72, HOLE_Z + 1.3, 2.2, 0.16, 0.1, 0.18, 0.5, 0.46);

    // The spill. A cone of vault stone and slab fragments on the floor — and
    // the only way down, so it has to be climbable.
    for (let i = 0; i < 46; i++) {
      const rr = rng();
      const a = rng() * Math.PI * 2;
      const rad = rr * 2.6;
      const s = 0.22 + rng() * 0.44;
      rubble.box(
        HOLE_X - 0.3 + Math.cos(a) * rad,
        0.06 + (1 - rr) * 1.05 + rng() * 0.16,
        HOLE_Z + 0.7 + Math.sin(a) * rad * 1.15,
        s * 1.45,
        s * 0.66,
        s * 1.15,
        (rng() - 0.5) * 0.7,
        rng() * Math.PI,
        (rng() - 0.5) * 0.7,
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

    // End wall around the opening.
    for (let i = 0; i < 46; i++) {
      const x = -3.2 + rng() * 6.4;
      const y = rng() * 3.4;
      if (Math.abs(x) < openHalf + 0.28 && y < openTop + 0.34) continue;
      dry.box(
        x,
        y,
        zFace + 0.28,
        0.44 + rng() * 0.4,
        0.32 + rng() * 0.18,
        0.55,
        0,
        (rng() - 0.5) * 0.012,
        (rng() - 0.5) * 0.01,
      );
    }
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

    // The infill. Common brick, 230 × 110 × 70, laid stretcher bond by
    // somebody who was not a bricklayer.
    const bh = 0.075;
    const bl = 0.23;
    let y = 0;
    let row = 0;
    while (y < openTop + 0.05) {
      const stagger = row % 2 === 0 ? 0 : bl / 2;
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
            bl * 0.955,
            bh * 0.9,
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
      const s = 0.24 + rng() * 0.4;
      rubble.box(
        (rng() - 0.5) * 3.3,
        y + s * 0.32,
        z,
        s * 1.5,
        s * 0.62,
        s * 1.1,
        (rng() - 0.5) * 0.4,
        rng() * Math.PI,
        (rng() - 0.5) * 0.4,
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
    const z = 19.3;
    const y = 1.48;
    // Reveal: a dark recessed box, so the opening has depth rather than being
    // a lit rectangle painted on the stone.
    const dark = MeshBuilder.CreateBox('ventReveal', { width: 0.7, height: 0.42, depth: 0.34 }, this.scene);
    dark.position.set(HALF_W + 0.2, y, z);
    const dm = new StandardMaterial('ventDark', this.scene);
    dm.diffuseColor = new Color3(0.02, 0.02, 0.022);
    dm.specularColor = Color3.Black();
    dm.emissiveColor = srgb('#3a2408').scale(0.5);
    dm.disableLighting = true;
    dark.material = dm;
    dark.isPickable = false;
    this.meshes.push(dark);

    // Head and sill of the opening.
    dry.box(HALF_W + 0.22, y + 0.28, z, 0.5, 0.16, 0.86);
    dry.box(HALF_W + 0.22, y - 0.28, z, 0.5, 0.16, 0.86);
    for (let i = 0; i < 4; i++) {
      steel.box(HALF_W + 0.03, y, z - 0.24 + i * 0.16, 0.03, 0.4, 0.03);
    }
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
    const origin = new Vector3(HOLE_X + 0.45, 5.4, HOLE_Z - 0.6);
    const dir = new Vector3(-0.22, -1, 0.3).normalize();

    this.shaft = new SpotLight('voidShaft', origin, dir, 0.62, 2.2, this.scene);
    this.shaft.diffuse = C.moonlight;
    this.shaft.specular = C.moonlight.scale(0.7);
    this.shaft.intensity = 620;
    this.shaft.range = 16;
    this.shaft.innerAngle = 0.22;
    this.shaft.falloffType = SpotLight.FALLOFF_PHYSICAL;
    this.shaft.shadowEnabled = false;

    // The sodium bleed through the ventilator, ninety metres and one wall away
    // from the nearest working lamp. Deliberately almost nothing.
    this.bleed = new PointLight('voidBleed', new Vector3(HALF_W + 0.5, 1.48, 19.3), this.scene);
    this.bleed.diffuse = C.sodiumVapour;
    this.bleed.specular = C.sodiumVapour.scale(0.4);
    this.bleed.intensity = 26;
    this.bleed.range = 8;

    // Dust in the shaft. In a sealed chamber this is the only thing that
    // moves, and it moves because a draught moves it — nothing else.
    if (p.particleBudget > 200) {
      const ps = new ParticleSystem('voidDust', Math.min(p.particleBudget, 1200), this.scene);
      ps.particleTexture = makeDotTexture(this.scene);
      ps.emitter = new Vector3(HOLE_X, 3.0, HOLE_Z + 0.3);
      ps.minEmitBox = new Vector3(-0.95, -2.9, -1.1);
      ps.maxEmitBox = new Vector3(0.95, 2.5, 1.1);
      ps.color1 = new Color4(0.72, 0.8, 0.95, 0.34);
      ps.color2 = new Color4(0.86, 0.9, 1.0, 0.16);
      ps.colorDead = new Color4(0.7, 0.78, 0.95, 0);
      ps.minSize = 0.008;
      ps.maxSize = 0.03;
      ps.minLifeTime = 8;
      ps.maxLifeTime = 18;
      ps.emitRate = 70;
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
    mat.maxSimultaneousLights = 6;
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

    // Weighted selection: the niches get carved far more heavily than the open
    // wall, because that is where a man had nothing else to do.
    const pool = this.faces.filter((f) => rng() < 0.055 * f.weight);
    const batch = new GeoBatch();
    let placed = 0;

    for (const f of pool) {
      if (placed >= 96) break;
      const cell = order[placed % CELLS];
      const maxW = Math.min(f.w * 0.86, 0.5);
      const maxH = Math.min(f.h * 0.8, 0.5);
      const size = Math.min(maxW, maxH);
      if (size < 0.16) continue;

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

  /** Common brick for the seal — the one non-limestone surface in the room. */
  private buildBrickMaterial(): PBRMaterial {
    const m = new PBRMaterial('sealBrick', this.scene);
    m.albedoColor = srgb('#6a4436');
    m.metallic = 0;
    m.roughness = 0.93;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.4;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = 6;
    m.freeze();
    return m;
  }

  override update(dt: number, _player?: unknown): void {
    this.t += dt;
    // The shaft breathes very slightly — cloud passing a window four floors
    // up, nothing more. If it reads as an effect it is too strong.
    if (this.shaft) {
      this.shaft.intensity = 620 * (1 + Math.sin(this.t * 0.21) * 0.045);
    }
  }

  override dispose(): void {
    this.dust?.dispose();
    this.shaft?.dispose();
    this.bleed?.dispose();
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

export { worldUV };
