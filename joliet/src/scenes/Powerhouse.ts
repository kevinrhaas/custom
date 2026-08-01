import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { MeshBuilder } from '@babylonjs/core/Meshes/meshBuilder';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { CreateBoxVertexData } from '@babylonjs/core/Meshes/Builders/boxBuilder';
import { CreatePlaneVertexData } from '@babylonjs/core/Meshes/Builders/planeBuilder';
import { CreateCylinderVertexData } from '@babylonjs/core/Meshes/Builders/cylinderBuilder';
import { CreateSphereVertexData } from '@babylonjs/core/Meshes/Builders/sphereBuilder';
import { CreateTorusVertexData } from '@babylonjs/core/Meshes/Builders/torusBuilder';
import { Vector3, Matrix } from '@babylonjs/core/Maths/math.vector';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { PointLight } from '@babylonjs/core/Lights/pointLight';
import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { RawTexture } from '@babylonjs/core/Materials/Textures/rawTexture';
import { Constants } from '@babylonjs/core/Engines/constants';
import type { Scene } from '@babylonjs/core/scene';

import '@babylonjs/core/Particles/particleSystemComponent';

import { GameScene, type SceneManifest } from './SceneBase';
import type { Player } from '../core/Player';
import { C, srgb } from '../core/Palette';
import { heightToNormal } from '../core/Noise';
import { profile } from '../core/Settings';

/**
 * Scene 2.1 — The Powerhouse.
 *
 * **Powerhouse and Well Pump House (#13), 1893.** Rubble and rock-faced cream
 * Joliet limestone in broken courses, asymmetrical side-gabled roof clad in
 * corrugated metal, circular gable oculi with cast metal grills — two on the
 * west flanking the chimney, one on the east — and a tall round red-and-brown
 * brick chimney rising along the centre of the west facade off a square base
 * with chamfered corners. It generated the power and steam for the whole
 * complex. **The southern half burned in the early 20th century and was
 * demolished**, so the building is half of what was built and one of its four
 * walls is a rebuilt blind end rather than an original elevation.
 *
 * ---
 *
 * ## ⚠️ THE INTERIOR IS PERIOD TYPOLOGY, NOT JOLIET EVIDENCE
 *
 * `RESEARCH.md` §7.2 is explicit: **the NRHP nomination does not describe the
 * powerhouse interior at all**, and its survey photo 15 is an exterior. The one
 * known interior record is a Matterport scan ("Old Joliet Prison Boiler Room")
 * that returned HTTP 403 to automated access and could not be retrieved. A
 * human can open it in a browser, and if anyone does, **this file is the thing
 * to revisit** — every dimension below is inference.
 *
 * What *is* built here is a sound typology for an 1893 institutional
 * power/boiler house: horizontal fire-tube boilers on brick settings, riveted
 * steel shells and headers, a coal-handling arrangement, ash pits, an operating
 * floor with steel bar-grating catwalks, cast-iron gate and globe valves with
 * spoked handwheels, gauge boards, and a slate switchboard with knife switches
 * and relays for the generators. It is flagged here the same way `Cellblocks`
 * flags its gang lock and `TheVoid` flags its inscriptions.
 *
 * **Five things in this room are documented, and the plan hangs off them:**
 * 1. Coal arrived by **rail spur along Main Street**, which is *north* — so the
 *    coal door, the bunker and the chutes are on the north wall.
 * 2. The **prison fire department occupied the NE corner** 1893–1914 — so there
 *    is an apparatus-bay-shaped arch in that corner, later bricked up.
 * 3. The **south half burned and was demolished** — so the south wall is a
 *    blind rebuilt end in brick, against three walls of rubble limestone.
 * 4. The **chimney is centred on the west** — so the boilers back west and the
 *    breeching ducts run into the chimney breast.
 * 5. A **1940s well pump house** is grafted onto the north end of the west
 *    facade — so there is a 20th-century doorway in that corner.
 *
 * ---
 *
 * ## The puzzle: two conduits, one bad sign
 *
 * `DESIGN.md` gives 2.1 the best puzzle in the game and it is built as written:
 * **two conduits, both plausible, one mislabelled by a period sign that was
 * accurate in 1901 and isn't now. The wrong turn is the player's misread, not a
 * cutscene.** Both routes are real geometry and both are enterable.
 *
 * - The **west duct** carries a cast-iron plate, `No. 1 CONDUIT · CELL HOUSES
 *   & YARD · 1901`, bolted to the original 1893 brick. In 1901 that was true.
 *   It is not true now: this duct ran south through the half of the building
 *   that burned, and the rebuild bricked it off — its cable trays are cut back
 *   and capped four metres in, and the run dies at a blind brick face. A later
 *   stencilled **2** sits on the head beside the plate, half scrubbed off.
 * - The **east duct** carries no plate at all, only a later stencilled
 *   **No. 1** on the brick head. Its trays are continuous, its armoured cable
 *   runs on into the dark, and its floor is boot-worn. This is the live route.
 *
 * So two things in the frame both claim to be No. 1, and the one that says it
 * loudest is wrong. Everything needed to tell them apart is physical and
 * visible with a headlamp: cut trays versus continuous trays, a blind brick
 * face versus a run that keeps going, rebuilt machine-made brick around the
 * west mouth versus original 1893 brick around the east. Nothing narrates it.
 *
 * ## The reward: `powered`
 *
 * Sequencing the three boiler stop valves and the relay board turns the
 * building's own festoon lighting on — `HEX.incandescent`, permanently, across
 * the map. **There is no save system, so cross-scene persistence cannot be
 * implemented here** (`QUALITY-BACKLOG.md` → "No save/checkpoint system"). What
 * this scene does provide is the state itself: `setPowered(true)` flips the
 * filament emissive, brings up the string point lights and the switchboard
 * pilots, and the room is composed to read in **both** states — dark, it is
 * moon through two roof breaches and the gable oculi plus a sodium bleed at the
 * east door; lit, it is a warm hall with the boilers in silhouette. Anchors
 * `a5` and `a6` capture the lit state, `a1`–`a4` the dark one.
 *
 * ## Composition
 *
 * The hall runs east–west, 22 m by 16 m, because the surviving half is wide and
 * shallow and because the gable ends (with the oculi) are east and west. The
 * money shot looks **west** from the entrance down the operating floor at three
 * riveted boiler fronts, with the grating catwalk crossing the frame at 3.9 m,
 * the steam header above it, and the moon coming through a torn bay of
 * corrugated roof to lay a hard parallelogram across the middle boiler's front.
 * Warm/cool split: cool from the roof, warm from the sodium at the door behind
 * you — and once the power is on, warm from overhead everywhere.
 */

/* -------------------------------------------------------------------------- */
/*  Dimensions — one place, so every subsystem agrees                          */
/* -------------------------------------------------------------------------- */

/** Inner faces of the four walls. West/east are the gable ends. */
const X_W = -18;
const X_E = 4;
const Z_S = -8;
const Z_N = 8;
/** Rubble limestone is thick. */
const WT = 0.72;
/** Wall head (eaves) and ridge. "One-and-one-half storeys" is the exterior read. */
const EAVE = 6.4;
const RIDGE = 9.6;
/** Roof pitch, derived once: rise over half-span. */
const SLOPE = (RIDGE - EAVE) / Z_N;
const SLOPE_A = Math.atan(SLOPE);

/** Three boilers, axes running east–west, fronts facing the operating floor. */
const BOILER_Z = [-5.2, 0, 5.2];
/** Brick setting: back, front, width across Z, top. */
const SET_X0 = -16.0;
const SET_X1 = -9.4;
const SET_W = 3.9;
const SET_H = 3.5;
/** The riveted shell inside the setting. */
const SHELL_D = 2.35;
const SHELL_Y = 2.15;
const SHELL_X0 = -15.5;
const SHELL_X1 = -9.85;

/** Chimney breast: square base with chamfered corners, centred on the west wall. */
const CHIM_X = -17.2;
const CHIM_HW = 1.62;
const CHIM_TOP = 8.6;

/** Grating catwalk along the boiler fronts. */
const CAT_X = -8.3;
const CAT_Y = 3.9;
const CAT_W = 1.5;
const CAT_Z0 = -7.0;
const CAT_Z1 = 7.0;

/** Main steam header, north–south above the catwalk. */
const HDR_X = -8.3;
const HDR_Y = 5.25;

/** Roof truss stations. Five, so four festoon bays. */
const TRUSS_X = [-16.2, -11.6, -7.0, -2.4, 2.2];
/** Bottom-chord height the festoon hangs from. */
const TRUSS_Y = 6.35;

/** The two conduit mouths in the blind south wall. */
const DUCT_A_X = -5.6; // the one carrying the 1901 plate. Dead.
const DUCT_B_X = -1.6; // unlabelled but for a later stencil. Live.
const DUCT_W = 1.15;
const DUCT_H = 1.45;
const DUCT_LEN = 4.6;
/** Where the rebuild's blind brick closes duct A off. */
const DUCT_A_BLIND = 3.3;

/** Slate switchboard, standing off the east wall and facing the hall. */
const SB_X = 3.35;
const SB_Z0 = -6.6;
const SB_Z1 = -2.2;
const SB_H = 2.45;

/** Torn bays in the south roof slope. [col, row] into the panel grid. */
const ROOF_COLS = 16;
const ROOF_ROWS = 5;
const ROOF_X0 = X_W - 0.8;
const ROOF_CW = (X_E + 0.8 - ROOF_X0) / ROOF_COLS;
const ROOF_RD = (Z_N + 0.8) / ROOF_ROWS;
const BREACH: [number, number][] = [
  [1, 2],
  [2, 2],
  [1, 3],
  [2, 3],
  [8, 3],
  [9, 3],
  [8, 4],
  [9, 4],
];

/* -------------------------------------------------------------------------- */

export class Powerhouse extends GameScene {
  readonly manifest: SceneManifest = {
    id: '2.1-powerhouse',
    title: 'The Powerhouse',
    spawn: { position: [1.6, 0.15, 1.2], yaw: -Math.PI / 2 },
    anchors: [
      {
        name: 'a1-boiler-hall',
        position: [2.0, 1.68, 0.7],
        rotation: [-Math.PI / 2 + 0.05, -0.03],
        fov: 66,
        note: 'THE frame, unpowered. From just inside the east entrance, straight west down 11 m of operating floor at three riveted boiler fronts on their brick settings, the grating catwalk crossing at 3.9 m, the steam header and the roof trusses above it, and moonlight through a torn bay of corrugated roof landing on the middle boiler. Tests the warm/cool split (sodium at the door behind, moon from the roof), the corridor perspective, and whether iron-and-brick reads at all with the headlamp as the only near source.',
      },
      {
        name: 'a2-boiler-front',
        position: [-7.2, 1.6, 0.15],
        rotation: [-Math.PI / 2, 0.04],
        fov: 62,
        note: 'Square on the middle boiler front from 2.2 m — the range the headlamp is calibrated for. Tests the cast-iron front plate over the riveted shell head, the two furnace doors and the ash doors under them, the water gauge glass and try-cocks, the main stop valve with its spoked handwheel on the crown, the stencilled valve numeral, and the brick setting with its arch.',
      },
      {
        name: 'a3-conduits',
        position: [-3.6, 1.55, -5.0],
        rotation: [Math.PI, 0.13],
        fov: 70,
        note: 'THE PUZZLE, in one frame. Both conduit mouths in the blind south wall from 3 m, with the 1901 cast plate over the west duct and the later stencilled No. 1 over the east one. Tests sign legibility at reading distance, the cut-and-capped trays inside the west duct against the continuous run inside the east, the rebuilt machine-made brick around the west mouth against original 1893 brick, and the blind brick face 3.3 m into the duct that says the loud label is wrong.',
      },
      {
        name: 'a4-switchboard',
        position: [0.55, 1.6, -4.4],
        rotation: [Math.PI / 2 + 0.06, 0.03],
        fov: 60,
        note: 'The relay board, unpowered. Four slate panels on a raised base against the east wall from 2.8 m: knife switches on their marble mounts, rheostat handwheels, dead ammeter and voltmeter faces, the open bus-bar cage overhead and the conduit drops into the floor. The second half of the puzzle and the thing the valves feed.',
      },
      {
        name: 'a5-hall-lit',
        position: [2.0, 1.68, 0.7],
        rotation: [-Math.PI / 2 + 0.05, -0.03],
        fov: 66,
        note: 'The reward, and deliberately the same pose as a1 so the two are a direct A/B. Powered: the festoon strings across all four truss bays are alight at HEX.incandescent, the boilers go to silhouette, the catwalk grating reads from underneath, and the switchboard pilots are on. If this frame is not obviously the same room with the power on, the reward has not landed.',
      },
      {
        name: 'a6-catwalk-lit',
        position: [-8.3, 5.56, -6.2],
        rotation: [0, 0.1],
        fov: 66,
        note: 'Powered, from the catwalk deck looking north along the run. Tests the grating underfoot (alpha-tested, surface:grating), the boiler crowns and their branch pipes into the steam header at head height, the riveted trusses and the torn roof bay overhead, and the festoon strands seen from inside their own light rather than under it.',
      },
    ],
  };

  /** Public so gameplay can flip it once an interaction system exists. */
  powered = false;

  private stringLights: PointLight[] = [];
  private sodium?: PointLight;
  private filamentMat!: PBRMaterial;
  private gaugeMat!: PBRMaterial;
  private dust?: ParticleSystem;
  private t = 0;
  /** Anchor eye positions that should capture the powered state. */
  private poweredAt: Vector3[] = [];

  async build(): Promise<void> {
    // Interior trim. The rig is calibrated for exteriors on limestone, so an
    // interior needs it pulled down — but this room is brick, cast iron and
    // coal soot, which is roughly a third of cream institutional block's
    // albedo, so it wants a MUCH softer trim than Cellblocks' 0.68. At that
    // value the first pass was a black rectangle with three headlamp-lit
    // patches in it and no readable architecture at all. Fog goes up because
    // twenty years of a leaking roof over a coal hall is genuinely dusty and
    // because it is the only depth cue in a room with no bright far end.
    this.renderer.setLightingTrim({ fill: 0.92, environment: 0.8, fog: 1.5 });

    for (const a of this.manifest.anchors) {
      if (a.name.endsWith('-lit')) this.poweredAt.push(new Vector3(...a.position));
    }

    const ctx = this.kit();
    const p = profile();
    const rng = mulberry(18930601); // the year the powerhouse opened

    // ---- Materials -------------------------------------------------------
    // Structure comes from the frozen library. Six scene-authored materials,
    // and each of them is something the library genuinely does not cover:
    // two bricks (the 1893 original and the post-fire rebuild — the whole
    // puzzle turns on being able to tell them apart), switchboard slate, the
    // alpha-tested bar grating, the translucent glazing, and the lamp glass
    // whose emissive is the `powered` flip itself.
    const stone = this.mats.get('limestone.wall');
    const wet = this.mats.get('limestone.wet');
    const floorMat = this.mats.get('concrete.floor');
    const slab = this.mats.get('concrete.slab');
    const catwalkSteel = this.mats.get('steel.catwalk');
    const frontSteel = this.mats.get('steel.cellFront');
    const doorSteel = this.mats.get('steel.door');
    const timber = this.mats.get('timber.rotten');

    const brick = this.buildBrickMaterial('phBrick', 18930601, false);
    const brickLate = this.buildBrickMaterial('phBrickLate', 19120704, true);
    const slate = this.buildSlateMaterial();
    const grating = this.buildGratingMaterial();
    const glazing = this.buildGlazingMaterial();
    this.filamentMat = this.buildFilamentMaterial();
    this.gaugeMat = this.buildGaugeMaterial();

    // ---- Batches ---------------------------------------------------------
    // One mesh per material, accumulated CPU-side and built once at the end,
    // the same device Cellblocks and TheVoid use. This scene places on the
    // order of four thousand primitives and four thousand Mesh objects would
    // be sixteen thousand GL buffers allocated and immediately discarded.
    const B: Batches = {
      stone: new GeoBatch(),
      brick: new GeoBatch(),
      brickLate: new GeoBatch(),
      slab: new GeoBatch(),
      wet: new GeoBatch(),
      steel: new GeoBatch(),
      front: new GeoBatch(),
      door: new GeoBatch(),
      grate: new GeoBatch(),
      glaze: new GeoBatch(),
      timber: new GeoBatch(),
      slate: new GeoBatch(),
      filament: new GeoBatch(),
      gauge: new GeoBatch(),
    };

    this.buildFloor(ctx, floorMat, slab);
    this.buildWalls(B, rng);
    this.buildRoof(B, rng);
    this.buildChimney(B);
    this.buildBoilers(B, rng);
    this.buildCatwalk(B, rng);
    this.buildPipework(B);
    this.buildCoalRoad(B, rng);
    this.buildFireBay(B);
    this.buildGenerator(B);
    this.buildSwitchboard(B);
    this.buildConduits(B, rng);
    this.buildFestoon(B);
    this.buildDebris(B, rng);

    // ---- Resolve the batches --------------------------------------------
    // Chunked along +X, which is the long axis: one 22 m mesh per material is
    // never outside the frustum, so a frame looking at a boiler front would
    // still pay for the switchboard at the far end.
    const CH = 4;
    B.stone.finish(ctx, this.scene, 'phStone', stone, { collide: false, cast: true }, CH);
    // 1.2 m per tile puts a course at 75 mm and a stretcher at 200 mm, which
    // is a real brick. The library default (3 m per tile) rendered the setting
    // arches at roughly two and a half times life size.
    B.brick.finish(ctx, this.scene, 'phBrick', brick, {
      collide: false,
      cast: true,
      uvDensity: 1 / 1.2,
    }, CH);
    B.brickLate.finish(ctx, this.scene, 'phBrickLate', brickLate, {
      collide: false,
      cast: true,
      uvDensity: 1 / 1.2,
    });
    B.slab.finish(ctx, this.scene, 'phSlab', slab, { collide: false, cast: true }, CH);
    B.wet.finish(ctx, this.scene, 'phWet', wet, { collide: false, cast: true });
    B.steel.finish(ctx, this.scene, 'phSteel', catwalkSteel, { collide: false, cast: true }, CH);
    B.front.finish(ctx, this.scene, 'phFronts', frontSteel, { collide: false, cast: true }, CH);
    B.door.finish(ctx, this.scene, 'phDoors', doorSteel, { collide: false, cast: true }, CH);
    // The decks are real collision AND the surface tag the footstep engine
    // reads — a grating gallery rings where the floor thumps, and that
    // difference is a navigation cue in the dark.
    B.grate.finish(ctx, this.scene, 'phGrating', grating, {
      collide: true,
      cast: true,
      surface: 'grating',
      uvDensity: 1 / 0.3,
    }, CH);
    // Never a shadow caster: the moon has to get through the oculi and the
    // north sashes, and these are the softest sources in the dark frame.
    B.glaze.finish(ctx, this.scene, 'phGlazing', glazing, { collide: false, cast: false });
    B.timber.finish(ctx, this.scene, 'phTimber', timber, { collide: false, cast: true }, 2);
    B.slate.finish(ctx, this.scene, 'phSlate', slate, {
      collide: false,
      cast: false,
      uvDensity: 1.1,
    });
    // Lamp glass and gauge faces are emitters, not occluders.
    B.filament.finish(ctx, this.scene, 'phFilaments', this.filamentMat, {
      collide: false,
      cast: false,
    }, 2);
    B.gauge.finish(ctx, this.scene, 'phGauges', this.gaugeMat, { collide: false, cast: false });

    // ---- Signage ---------------------------------------------------------
    this.buildSigns(ctx);

    // ---- Collision -------------------------------------------------------
    // Invisible proxies rather than collision on the batched geometry: sweeping
    // an ellipsoid against a 30k-triangle mesh of rivets and pipework every
    // frame is a poor trade when the player only ever touches a dozen planes.
    this.buildColliders(ctx);

    // ---- Practicals ------------------------------------------------------
    this.buildLights(p);
    if (p.particleBudget > 200) this.buildDust(p.particleBudget);

    await this.scene.whenReadyAsync();
  }

  /* ----------------------------------------------------------------- floor -- */

  /**
   * The operating floor.
   *
   * `concrete.floor` with its polish pushed up along the walking lane, because
   * the long specular running away down a dark hall is what carries the
   * perspective; `concrete.slab` for the raised firing platform in front of the
   * settings, which is a different pour and has never been walked smooth.
   */
  private buildFloor(
    ctx: ReturnType<GameScene['kit']>,
    floorMat: PBRMaterial,
    slabMat: PBRMaterial,
  ): void {
    const f = MeshBuilder.CreateBox(
      'phFloor',
      { width: X_E - X_W + 1.4, height: 0.6, depth: Z_N - Z_S + 1.4 },
      this.scene,
    );
    f.position.set((X_W + X_E) / 2, -0.3, (Z_S + Z_N) / 2);
    f.material = floorMat;
    ctx.register(f, { collide: true, cast: false, surface: 'concrete' });

    // Firing platform: the strip the stokers stood on, 60 mm proud, running the
    // whole boiler front. Tagged metal — it is a chequer-plate deck over the
    // ash channel, not concrete, and it is the one place in the hall where the
    // footsteps change without the player leaving the ground floor.
    const plat = MeshBuilder.CreateBox(
      'phFiringFloor',
      { width: 1.9, height: 0.12, depth: SET_W * 3 + 4.0 },
      this.scene,
    );
    plat.position.set(SET_X1 + 0.95, 0.06, 0);
    plat.material = slabMat;
    ctx.register(plat, { collide: true, cast: false, surface: 'metal' });
  }

  /* ----------------------------------------------------------------- walls -- */

  /**
   * Three walls of rubble limestone and one of brick.
   *
   * The south wall is the rebuilt blind end where the burnt half was taken off,
   * and making it brick against three limestone elevations is the single
   * clearest way to say so without a line of dialogue. The gable ends (east and
   * west) carry the building's signature: circular openings in the upper
   * half-storey with rock-faced stone surrounds and circular metal grills.
   */
  private buildWalls(B: Batches, rng: () => number): void {
    const mid = (a: number, b: number): number => (a + b) / 2;

    // ---- North wall: coal road side, four barred openings + the coal door --
    const nOuter = Z_N + WT;
    const nZ = mid(Z_N, nOuter);
    {
      // Openings: heavy stone lintels and sills, metal bars, glass block.
      const wins: [number, number][] = [
        [-14.6, 2.0],
        [-11.0, 2.0],
        [-4.2, 2.0],
        [-0.4, 2.0],
      ];
      const y0 = 2.0;
      const y1 = 5.1;
      // Solid wall, then subtract by building the pieces between the openings.
      const cuts: [number, number][] = wins.map(([cx, w]) => [cx - w / 2, cx + w / 2]);
      // The coal door and the fire-bay arch are also holes in this wall.
      cuts.push([-8.6, -6.2]); // coal door
      cuts.push([0.9, 3.7]); // fire apparatus bay
      cuts.sort((a, b) => a[0] - b[0]);

      let x = X_W - WT;
      for (const [c0, c1] of [...cuts, [X_E + WT, X_E + WT] as [number, number]]) {
        if (c0 - x > 0.05) B.stone.box(mid(x, c0), EAVE / 2, nZ, c0 - x, EAVE, WT);
        x = Math.max(x, c1);
      }
      // Spandrels over and under each window opening.
      for (const [cx, w] of wins) {
        B.stone.box(cx, y0 / 2, nZ, w, y0, WT);
        B.stone.box(cx, mid(y1, EAVE), nZ, w, EAVE - y1, WT);
        // Sill sloped to shed, and a heavy lintel.
        B.stone.box(cx, y0 - 0.09, Z_N - 0.13, w + 0.5, 0.2, 0.5, 0.09, 0, 0);
        B.stone.box(cx, y1 + 0.16, nZ, w + 0.6, 0.32, WT + 0.1);
        // Glazing set near the outer face so the reveal has depth.
        B.glaze.box(cx, mid(y0, y1), Z_N + WT - 0.14, w - 0.16, y1 - y0 - 0.1, 0.05);
        // Bars: "most secured with metal bars".
        for (let b = 0; b < 5; b++) {
          B.steel.box(
            cx - w / 2 + (w * (b + 0.5)) / 5,
            mid(y0, y1),
            Z_N + WT - 0.06,
            0.045,
            y1 - y0,
            0.045,
          );
        }
        for (let b = 1; b < 4; b++) {
          B.steel.box(cx, y0 + ((y1 - y0) * b) / 4, Z_N + WT - 0.06, w - 0.1, 0.045, 0.045);
        }
      }
      // Coal door head and the apparatus arch head are handled by their owners.
      B.stone.box(-7.4, mid(3.4, EAVE), nZ, 2.4, EAVE - 3.4, WT);
      B.stone.box(-7.4, 3.4 + 0.17, nZ, 2.9, 0.34, WT + 0.1);
    }

    // ---- South wall: rebuilt blind end, brick, no openings above ----------
    {
      const sOuter = Z_S - WT;
      const sZ = mid(Z_S, sOuter);
      // Limestone plinth: the original 1893 footing survived the fire.
      B.stone.box(mid(X_W - WT, X_E + WT), 0.5, sZ, X_E - X_W + WT * 2, 1.0, WT + 0.08);
      const cuts: [number, number][] = [
        [DUCT_A_X - DUCT_W / 2 - 0.2, DUCT_A_X + DUCT_W / 2 + 0.2],
        [DUCT_B_X - DUCT_W / 2 - 0.2, DUCT_B_X + DUCT_W / 2 + 0.2],
      ];
      let x = X_W - WT;
      for (const [c0, c1] of [...cuts, [X_E + WT, X_E + WT] as [number, number]]) {
        if (c0 - x > 0.05) {
          B.brick.box(mid(x, c0), mid(1.0, EAVE), sZ, c0 - x, EAVE - 1.0, WT);
        }
        x = Math.max(x, c1);
      }
      // Over the two ducts.
      for (const dx of [DUCT_A_X, DUCT_B_X]) {
        B.brick.box(dx, mid(DUCT_H + 0.34, EAVE), sZ, DUCT_W + 0.4, EAVE - DUCT_H - 0.34, WT);
      }
      // Blind brick pilasters — the rebuild braced the new end wall.
      for (const px of [-13.0, -8.6, 1.2]) {
        B.brick.box(px, mid(1.0, EAVE - 0.4), Z_S + 0.16, 0.9, EAVE - 1.4, 0.32);
      }
      // Corbelled brick band at the head, which is what a rebuilt gable end
      // gets instead of stone coping.
      B.brick.box(mid(X_W, X_E), EAVE - 0.2, Z_S + 0.1, X_E - X_W, 0.28, 0.2);
    }

    // ---- West gable: chimney breast, two oculi -----------------------------
    this.buildGableWall(B, X_W, -1, [
      { z: -3.1, y: 7.3, d: 1.5 },
      { z: 3.1, y: 7.3, d: 1.5 },
    ], null, rng);

    // ---- East gable: primary entrance centred, one oculus, two windows -----
    this.buildGableWall(B, X_E, 1, [{ z: 0, y: 7.7, d: 1.5 }], { z: 0, w: 2.4, h: 3.1 }, rng);

    // The 1940s well pump house doorway, north end of the west facade. A
    // one-storey shed-roofed volume grafted on, so a later opening cut through
    // 1893 rubble with a concrete head rather than a stone one.
    {
      const dz = 6.1;
      const dw = 1.3;
      const dh = 2.15;
      B.slab.box(X_W - WT / 2, mid(dh, dh + 0.26), dz, WT, 0.26, dw + 0.5);
      for (const s of [-1, 1] as const) {
        B.slab.box(X_W - WT / 2, dh / 2, dz + s * (dw / 2 + 0.1), WT, dh, 0.2);
      }
      // The pump room beyond: a shallow box so the doorway is not a black hole.
      B.slab.box(X_W - WT - 1.4, 1.3, dz, 2.8, 0.16, 3.0);
      B.slab.box(X_W - WT - 2.8, 1.3, dz, 0.2, 2.6, 3.0);
      B.slab.box(X_W - WT - 1.4, 0.06, dz, 2.8, 0.12, 3.0);
      // The well pump on its plinth.
      B.slab.box(X_W - WT - 1.5, 0.28, dz - 0.2, 1.1, 0.44, 1.0);
      B.steel.cylY(X_W - WT - 1.5, 0.92, dz - 0.2, 0.52, 0.84);
      B.steel.cylY(X_W - WT - 1.5, 1.42, dz - 0.2, 0.2, 0.3);
      B.steel.torusY(X_W - WT - 1.5, 1.6, dz - 0.2, 0.46, 0.05);
      B.steel.cylZ(X_W - WT - 1.5, 0.55, dz + 0.7, 0.16, 1.2);
    }
  }

  /**
   * One gable end: solid wall to the eaves, a triangle above it to the ridge,
   * circular oculi with rock-faced surrounds and cast metal grills, and
   * optionally a doorway.
   *
   * The oculi are the building's signature and they are also, at night, the
   * only openings the moon can reach — it runs low in the west-south-west, so
   * the two on the west gable are what put cool light into the hall at all.
   * They are built as a ring of trapezoid blocks around a real hole rather than
   * a disc on a wall: a flat texture of an opening reads as a sticker at any
   * range, and more practically a solid wall with a decal on it lets no light
   * through at all.
   */
  private buildGableWall(
    B: Batches,
    xFace: number,
    dir: -1 | 1,
    oculi: { z: number; y: number; d: number }[],
    door: { z: number; w: number; h: number } | null,
    rng: () => number,
  ): void {
    const xMid = xFace + (dir * WT) / 2;
    const zSpan = Z_N - Z_S + WT * 2;

    // Solid below the eaves, cut for the doorway.
    if (door) {
      const c0 = door.z - door.w / 2;
      const c1 = door.z + door.w / 2;
      B.stone.box(xMid, EAVE / 2, (Z_S - WT + c0) / 2, WT, EAVE, c0 - (Z_S - WT));
      B.stone.box(xMid, EAVE / 2, (c1 + Z_N + WT) / 2, WT, EAVE, Z_N + WT - c1);
      B.stone.box(xMid, (door.h + EAVE) / 2, door.z, WT, EAVE - door.h, door.w);
      // Segmental-arch rock-faced stone lintel and the jamb reveals.
      B.stone.box(xMid, door.h + 0.2, door.z, WT + 0.12, 0.4, door.w + 0.7);
      for (const s of [-1, 1] as const) {
        B.stone.box(xMid, door.h / 2, door.z + s * (door.w / 2 + 0.1), WT + 0.08, door.h, 0.2);
      }
      // Double-leaf doors, a chain-link security gate, a tall metal transom.
      for (const s of [-1, 1] as const) {
        B.door.box(
          xFace + dir * 0.06,
          door.h / 2 - 0.35,
          door.z + s * door.w / 4,
          0.08,
          door.h - 0.7,
          door.w / 2 - 0.06,
        );
      }
      B.door.box(xFace + dir * 0.06, door.h - 0.24, door.z, 0.08, 0.44, door.w - 0.06);
      // The gate stands open — this is how the crew got in.
      B.steel.box(xFace + dir * 0.2, 1.05, door.z - door.w / 2 - 0.28, 0.06, 2.1, 0.6, 0, 0.5, 0);
      // Warm sodium spill on the ground beyond the opening.
      B.slab.box(xFace + dir * 0.9, 0.02, door.z, 1.6, 0.06, door.w + 1.2);
    } else {
      B.stone.box(xMid, EAVE / 2, (Z_S - WT + Z_N + WT) / 2, WT, EAVE, zSpan);
    }

    // The gable triangle above the eaves, as stepped courses. Stepping it means
    // the raking edge is real geometry rather than a hard box corner poking
    // through the roof plane.
    const steps = 10;
    for (let i = 0; i < steps; i++) {
      const y0 = EAVE + ((RIDGE - EAVE) * i) / steps;
      const y1 = EAVE + ((RIDGE - EAVE) * (i + 1)) / steps;
      const half = (Z_N + 0.9) * (1 - i / steps);
      B.stone.box(xMid, (y0 + y1) / 2, 0, WT, y1 - y0 + 0.02, half * 2);
    }

    for (const o of oculi) {
      const r = o.d / 2;
      // Circular metal grill: a hub, four rings' worth of radial bars and two
      // concentric rings. Documented as "circular metal grills".
      const N = 20;
      for (let i = 0; i < N; i++) {
        const a = (i / N) * Math.PI * 2;
        // Voussoir-ish rock-faced surround block.
        B.stone.box(
          xMid,
          o.y + Math.sin(a) * (r + 0.19),
          o.z + Math.cos(a) * (r + 0.19),
          WT + 0.1,
          0.34,
          0.34,
          0,
          0,
          a,
        );
      }
      // Glazing disc behind the grill so the opening glows rather than reading
      // as a black hole in a dark wall.
      B.glaze.cylX(xFace + dir * (WT - 0.1), o.y, o.z, o.d - 0.06, 0.05);
      for (let i = 0; i < 8; i++) {
        const a = (i / 8) * Math.PI;
        B.steel.box(
          xFace + dir * 0.09,
          o.y,
          o.z,
          0.05,
          o.d - 0.04,
          0.05,
          0,
          0,
          a,
        );
      }
      B.steel.torusX(xFace + dir * 0.09, o.y, o.z, o.d * 0.62, 0.05);
      B.steel.torusX(xFace + dir * 0.09, o.y, o.z, o.d * 0.98, 0.06);
      // A pane or two gone, which is why there is guano on the sill below.
      if (rng() < 0.7) B.slab.box(xFace + dir * 0.3, o.y - r - 0.24, o.z, 0.5, 0.1, o.d);
    }
  }

  /* ------------------------------------------------------------------ roof -- */

  /**
   * Corrugated metal on riveted steel trusses, with two torn bays.
   *
   * The roof is built as a grid of panels rather than two big planes precisely
   * so bays can be MISSING. That is not decoration: the moon runs at 25 degrees
   * in the west-south-west, the south elevation is a blind rebuilt wall and the
   * west gable is mostly chimney, so without holes in the roof there is almost
   * no path for moonlight into this room at all and the whole frame collapses
   * onto the headlamp. The fire took the south half of the building; the roof
   * over what is left of the south slope is exactly where it would still be
   * failing.
   */
  private buildRoof(B: Batches, rng: () => number): void {
    const isBreached = (c: number, r: number): boolean =>
      BREACH.some(([bc, br]) => bc === c && br === r);

    for (let c = 0; c < ROOF_COLS; c++) {
      const x = ROOF_X0 + (c + 0.5) * ROOF_CW;
      for (let r = 0; r < ROOF_ROWS; r++) {
        for (const side of [-1, 1] as const) {
          const z = side * (r + 0.5) * ROOF_RD;
          const y = RIDGE - SLOPE * Math.abs(z);
          if (side < 0 && isBreached(c, r)) {
            // Torn edge: a couple of curled sheet fragments hanging off the
            // purlin, so the hole has a lip rather than a clean rectangle.
            if (rng() < 0.55) {
              B.steel.box(
                x + (rng() - 0.5) * 0.8,
                y - 0.2 - rng() * 0.4,
                z + (rng() - 0.5) * 0.9,
                0.5 + rng() * 0.5,
                0.02,
                0.4 + rng() * 0.4,
                (rng() - 0.5) * 1.4,
                rng() * Math.PI,
                (rng() - 0.5) * 1.2,
              );
            }
            continue;
          }
          B.steel.box(
            x,
            y,
            z,
            ROOF_CW + 0.02,
            0.07,
            ROOF_RD / Math.cos(SLOPE_A) + 0.02,
            -side * SLOPE_A,
            0,
            0,
          );
        }
      }
    }
    // Ridge capping.
    B.steel.box(0, RIDGE + 0.12, 0, X_E - X_W + 1.6, 0.14, 0.5);

    // Purlins, running the length under the sheeting.
    for (let r = 0; r < ROOF_ROWS; r++) {
      for (const side of [-1, 1] as const) {
        const z = side * (r + 0.5) * ROOF_RD;
        const y = RIDGE - SLOPE * Math.abs(z) - 0.14;
        B.steel.box(0, y, z, X_E - X_W + 1.4, 0.12, 0.12);
      }
    }

    // Riveted trusses. Bottom chord at the eaves line, apex just under the
    // ridge, king post and paired diagonals — the standard 1890s shop truss and
    // the thing that makes the volume overhead read as iron rather than as a lid.
    for (const tx of TRUSS_X) {
      B.steel.box(tx, TRUSS_Y, 0, 0.16, 0.16, Z_N - Z_S + 1.2);
      for (const side of [-1, 1] as const) {
        // Rafter chord, eaves to apex.
        const len = Math.hypot(Z_N + 0.6, RIDGE - 0.4 - TRUSS_Y);
        const a = Math.atan2(RIDGE - 0.4 - TRUSS_Y, Z_N + 0.6);
        B.steel.box(
          tx,
          (TRUSS_Y + RIDGE - 0.4) / 2,
          (side * (Z_N + 0.6)) / 2,
          0.15,
          0.15,
          len,
          side * a,
          0,
          0,
        );
        // Two diagonals per side.
        for (const f of [0.36, 0.68]) {
          const zz = side * (Z_N + 0.6) * f;
          const yy = TRUSS_Y + (RIDGE - 0.4 - TRUSS_Y) * f;
          B.steel.box(
            tx,
            (TRUSS_Y + yy) / 2,
            (zz + side * (Z_N + 0.6) * (f - 0.28)) / 2,
            0.09,
            0.09,
            Math.hypot(yy - TRUSS_Y, (Z_N + 0.6) * 0.28) + 0.1,
            side * Math.atan2(yy - TRUSS_Y, (Z_N + 0.6) * 0.28),
            0,
            0,
          );
          // Gusset plate at the joint.
          B.steel.box(tx, yy, zz, 0.03, 0.34, 0.34);
        }
      }
      // King post and its gussets.
      B.steel.box(tx, (TRUSS_Y + RIDGE - 0.4) / 2, 0, 0.12, RIDGE - 0.4 - TRUSS_Y, 0.12);
      B.steel.box(tx, TRUSS_Y + 0.16, 0, 0.03, 0.44, 0.5);
      B.steel.box(tx, RIDGE - 0.5, 0, 0.03, 0.5, 0.6);
      // Bearing shoe where the chord lands on the wall head.
      for (const side of [-1, 1] as const) {
        B.slab.box(tx, EAVE - 0.14, side * (Z_N + 0.2), 0.5, 0.3, 0.6);
      }
    }
  }

  /* --------------------------------------------------------------- chimney -- */

  /**
   * The chimney breast: square base with **chamfered corners**, documented.
   *
   * Originally 145 feet of round red-and-brown brick above this, lowered in
   * 2022 with the removed bricks retained on site. None of that shaft is
   * visible from inside the hall, so what is modelled is the base — the mass
   * the breeching ducts run into, and the thing the two west oculi flank.
   */
  private buildChimney(B: Batches): void {
    const h = CHIM_TOP;
    // Body.
    B.brick.box(CHIM_X, h / 2, 0, CHIM_HW * 2, h, CHIM_HW * 2);
    // Chamfers: four 45-degree fillets down the corners.
    for (const sx of [-1, 1] as const) {
      for (const sz of [-1, 1] as const) {
        B.brick.box(
          CHIM_X + sx * CHIM_HW,
          h / 2,
          sz * CHIM_HW,
          0.62,
          h,
          0.62,
          0,
          Math.PI / 4,
          0,
        );
      }
    }
    // Corbelled cap band and a plinth, so it is not a naked box.
    B.brick.box(CHIM_X, 0.42, 0, CHIM_HW * 2 + 0.32, 0.84, CHIM_HW * 2 + 0.32);
    B.brick.box(CHIM_X, h - 0.36, 0, CHIM_HW * 2 + 0.26, 0.34, CHIM_HW * 2 + 0.26);
    B.brick.box(CHIM_X, h - 0.68, 0, CHIM_HW * 2 + 0.14, 0.3, CHIM_HW * 2 + 0.14);

    // The soot door and the damper linkage at the base.
    B.door.box(CHIM_X + CHIM_HW - 0.02, 0.72, 0, 0.08, 0.86, 0.72);
    B.steel.box(CHIM_X + CHIM_HW + 0.06, 0.72, 0.42, 0.05, 0.05, 0.3);
    B.steel.cylY(CHIM_X + CHIM_HW + 0.06, 1.5, 0.42, 0.06, 1.5);
  }

  /* --------------------------------------------------------------- boilers -- */

  /**
   * Three horizontal fire-tube boilers on brick settings.
   *
   * The whole scene's centre of gravity. Each is a riveted steel shell inside a
   * brick setting with a segmental arch over the furnace mouths, a cast-iron
   * front plate carrying two furnace doors and two ash doors, a water gauge
   * glass with try-cocks, a pressure gauge on a siphon, and — on the crown — the
   * **main stop valve with its spoked handwheel**, which is what the puzzle
   * actually asks the player to sequence. Each wheel carries a stencilled
   * numeral so the sequence is stateable without a HUD.
   *
   * Rust is not metal: `steel.catwalk` takes metalness to nearly zero and
   * roughness to nearly one wherever the bloom wins, and the fronts use
   * `steel.cellFront`'s oxide-brown enamel so the two families read apart.
   */
  private buildBoilers(B: Batches, rng: () => number): void {
    for (let i = 0; i < BOILER_Z.length; i++) {
      const bz = BOILER_Z[i];
      const half = SET_W / 2;

      // ---- Brick setting ----------------------------------------------
      // Side cheeks and the crown over the shell, left open at the front for
      // the arch. Built as pieces rather than one box so the shell sits IN it.
      for (const s of [-1, 1] as const) {
        B.brick.box(
          (SET_X0 + SET_X1) / 2,
          SET_H / 2,
          bz + s * (half - 0.38),
          SET_X1 - SET_X0,
          SET_H,
          0.76,
        );
      }
      // Crown above the shell.
      B.brick.box(
        (SET_X0 + SET_X1) / 2,
        SET_H - 0.3,
        bz,
        SET_X1 - SET_X0,
        0.6,
        SET_W - 1.4,
      );
      // Back wall of the setting, pierced for the breeching.
      B.brick.box(SET_X0 - 0.2, SET_H / 2, bz, 0.4, SET_H, SET_W);
      // Front face of the setting with a segmental arch over the mouths.
      const archY = 2.55;
      for (const s of [-1, 1] as const) {
        B.brick.box(SET_X1 + 0.22, archY / 2, bz + s * (half - 0.34), 0.44, archY, 0.68);
      }
      B.brick.box(SET_X1 + 0.22, (archY + SET_H) / 2, bz, 0.44, SET_H - archY, SET_W);
      // Voussoirs.
      for (let v = 0; v < 9; v++) {
        const a = Math.PI * (0.08 + (v / 8) * 0.84);
        B.brick.box(
          SET_X1 + 0.22,
          archY - 0.2 + Math.sin(a) * 0.62,
          bz + Math.cos(a) * 1.44,
          0.5,
          0.34,
          0.3,
          0,
          0,
          a - Math.PI / 2,
        );
      }
      // Ash pit below the mouths, and the ash channel in front.
      B.wet.box(SET_X1 + 0.5, 0.24, bz, 1.2, 0.48, SET_W - 1.5);
      for (let g = 0; g < 5; g++) {
        B.steel.box(SET_X1 + 0.5, 0.5, bz - 1.1 + g * 0.55, 1.16, 0.05, 0.16);
      }

      // ---- The riveted shell -------------------------------------------
      const len = SHELL_X1 - SHELL_X0;
      B.steel.cylX((SHELL_X0 + SHELL_X1) / 2, SHELL_Y, bz, SHELL_D, len);
      // Butt straps at the ring seams, with a full circle of rivets on each.
      for (const sx of [SHELL_X0 + 1.5, SHELL_X0 + 3.1, SHELL_X0 + 4.7]) {
        B.steel.cylX(sx, SHELL_Y, bz, SHELL_D + 0.05, 0.24);
        for (let k = 0; k < 26; k++) {
          const a = (k / 26) * Math.PI * 2;
          B.steel.sphere(
            sx,
            SHELL_Y + Math.sin(a) * (SHELL_D / 2 + 0.035),
            bz + Math.cos(a) * (SHELL_D / 2 + 0.035),
            0.058,
          );
        }
      }
      // Longitudinal seam along the crown, double-riveted.
      for (let k = 0; k < 26; k++) {
        const sx = SHELL_X0 + 0.3 + (k / 25) * (len - 0.6);
        for (const off of [-0.09, 0.09]) {
          B.steel.sphere(sx, SHELL_Y + SHELL_D / 2 + 0.028, bz + off, 0.055);
        }
      }
      // Steam dome on the crown, and the safety valve on top of it.
      const domeX = SHELL_X0 + 2.1;
      B.steel.cylY(domeX, SET_H + 0.1, bz, 0.82, 0.66);
      B.steel.cylY(domeX, SET_H + 0.46, bz, 0.92, 0.1);
      B.steel.cylY(domeX, SET_H + 0.66, bz, 0.24, 0.34);
      B.steel.box(domeX, SET_H + 0.92, bz, 0.16, 0.5, 0.16, 0, 0, 0.35);

      // ---- Cast-iron front plate ---------------------------------------
      const fx = SET_X1 + 0.46;
      B.front.box(fx, SHELL_Y, bz, 0.1, 2.72, 2.72);
      // Rim rivets on the front plate.
      for (let k = 0; k < 30; k++) {
        const a = (k / 30) * Math.PI * 2;
        B.front.sphere(
          fx + 0.06,
          SHELL_Y + Math.sin(a) * 1.28,
          bz + Math.cos(a) * 1.28,
          0.05,
        );
      }
      // Two furnace doors and two ash doors under them.
      for (const s of [-1, 1] as const) {
        const dz = bz + s * 0.62;
        B.door.cylX(fx + 0.09, 1.62, dz, 0.8, 0.09);
        B.door.cylX(fx + 0.14, 1.62, dz, 0.3, 0.06);
        // Dog latch and hinge.
        B.steel.box(fx + 0.16, 1.62, dz + 0.44, 0.06, 0.3, 0.1, 0, 0, 0.6);
        B.steel.box(fx + 0.14, 1.62, dz - 0.42, 0.08, 0.22, 0.09);
        // Ash door.
        B.door.box(fx + 0.08, 0.78, dz, 0.08, 0.5, 0.58);
        B.steel.box(fx + 0.14, 0.78, dz + 0.3, 0.06, 0.16, 0.09);
      }
      // Water gauge glass and three try-cocks, on the plate's north side.
      const gx = fx + 0.12;
      const gz = bz + 1.05;
      B.steel.cylY(gx, 2.62, gz, 0.11, 0.62);
      B.gauge.cylY(gx + 0.03, 2.62, gz, 0.055, 0.5);
      for (const ty of [2.36, 2.6, 2.84]) {
        B.steel.cylX(gx + 0.1, ty, gz, 0.05, 0.16);
        B.steel.box(gx + 0.2, ty, gz, 0.03, 0.14, 0.03);
      }
      // Pressure gauge on its siphon.
      B.steel.cylY(gx, 3.05, bz - 1.0, 0.05, 0.5);
      B.steel.cylX(gx + 0.06, 3.28, bz - 1.0, 0.34, 0.08);
      B.gauge.cylX(gx + 0.11, 3.28, bz - 1.0, 0.3, 0.02);

      // ---- The stop valve: the thing the puzzle is about ----------------
      const vx = SET_X1 - 0.5;
      const vy = SET_H + 0.26;
      B.steel.cylY(vx, vy, bz, 0.36, 0.5);
      B.steel.cylY(vx, vy + 0.3, bz, 0.44, 0.1);
      B.steel.cylY(vx, vy + 0.46, bz, 0.11, 0.3);
      // Spoked handwheel.
      B.steel.torusY(vx, vy + 0.62, bz, 0.66, 0.055);
      for (let k = 0; k < 5; k++) {
        const a = (k / 5) * Math.PI * 2;
        B.steel.box(
          vx + Math.cos(a) * 0.17,
          vy + 0.62,
          bz + Math.sin(a) * 0.17,
          0.36,
          0.04,
          0.05,
          0,
          -a,
          0,
        );
      }
      B.steel.cylY(vx, vy + 0.64, bz, 0.16, 0.1);
      // Riser into the branch that goes to the header.
      B.steel.cylY(vx, vy - 0.4, bz, 0.28, 0.5);

      // ---- Breeching: the flue duct back into the chimney ---------------
      const by = 2.5;
      B.steel.cylX(SET_X0 - 0.7, by, bz, 1.25, 1.1);
      if (bz === 0) {
        B.steel.cylX(SET_X0 - 1.5, by, bz, 1.25, 1.0);
      } else {
        // The outer boilers turn toward the chimney.
        const s = Math.sign(bz);
        B.steel.cylZ(SET_X0 - 1.25, by, bz - s * 1.4, 1.25, 2.6);
        B.steel.cylX(SET_X0 - 1.25, by, bz - s * 3.0, 1.25, 1.2);
        B.steel.cylX(SET_X0 - 2.4, by, bz - s * 3.0, 1.25, 1.4);
      }
      // Straps around the breeching, and a hanger to the truss.
      for (let k = 0; k < 3; k++) {
        B.steel.cylX(SET_X0 - 0.4 - k * 0.5, by, bz, 1.32, 0.09);
      }
      B.steel.box(SET_X0 - 0.7, (by + 1.3 + TRUSS_Y) / 2, bz, 0.06, TRUSS_Y - by - 0.6, 0.06);

      // ---- Feed pump and its pipework, alongside every other setting ----
      if (i !== 1) {
        const px = SET_X1 + 1.9;
        const pz = bz + (i === 0 ? 2.2 : -2.2);
        B.slab.box(px, 0.16, pz, 1.1, 0.32, 0.8);
        B.steel.cylZ(px, 0.62, pz, 0.62, 0.9);
        B.steel.cylY(px + 0.4, 0.66, pz, 0.18, 0.9);
        B.steel.torusY(px + 0.4, 1.14, pz, 0.4, 0.05);
        B.steel.cylZ(px - 0.4, 1.1, pz, 0.14, 1.6);
      }

      // Coal spilled at the mouth of every setting, and a shovel or a rake.
      for (let k = 0; k < 26; k++) {
        const s = 0.05 + rng() * 0.11;
        B.wet.box(
          SET_X1 + 0.7 + rng() * 1.5,
          0.14 + s * 0.3,
          bz + (rng() - 0.5) * (SET_W + 1.2),
          s,
          s * 0.7,
          s * 1.2,
          rng() * 2,
          rng() * 3,
          rng() * 2,
        );
      }
    }

    // The chequer-plate over the ash channel has a section lifted out, which is
    // where the ash actually shows.
    B.wet.box(SET_X1 + 0.5, 0.16, 2.4, 1.2, 0.3, 1.2);
    B.steel.box(SET_X1 + 1.6, 0.32, 2.4, 0.06, 0.6, 1.1, 0, 0, 0.45);
  }

  /* --------------------------------------------------------------- catwalk -- */

  /**
   * The operating gallery: bar grating along the boiler fronts at 3.9 m, with
   * cantilever brackets off the settings, a stringer and railing on the hall
   * side, and one steel stair down at the south end.
   *
   * It crosses the money shot at exactly the height that gives the frame a
   * middle ground, and it is the reason the boiler crowns and the stop valves
   * are reachable at all. Grating rather than plate because that difference —
   * ringing rather than thumping underfoot — is a real navigation cue in a dark
   * building, and because you should be able to see the floor through your feet.
   */
  private buildCatwalk(B: Batches, rng: () => number): void {
    const len = CAT_Z1 - CAT_Z0;
    const zc = (CAT_Z0 + CAT_Z1) / 2;

    B.grate.box(CAT_X, CAT_Y - 0.03, zc, CAT_W, 0.06, len);
    // Stringer channels both sides, and a nosing angle at the hall edge.
    for (const s of [-1, 1] as const) {
      B.steel.box(CAT_X + s * (CAT_W / 2 - 0.05), CAT_Y - 0.17, zc, 0.11, 0.28, len);
    }
    B.steel.box(CAT_X + CAT_W / 2 - 0.02, CAT_Y + 0.01, zc, 0.06, 0.05, len);

    // Cantilever brackets back to the boiler settings.
    const nBr = 8;
    for (let b = 0; b <= nBr; b++) {
      const bz = CAT_Z0 + (b * len) / nBr;
      B.steel.box((CAT_X + SET_X1) / 2, CAT_Y - 0.22, bz, CAT_X - SET_X1, 0.12, 0.09);
      B.steel.box(
        (CAT_X + SET_X1) / 2 - 0.1,
        CAT_Y - 0.62,
        bz,
        1.3,
        0.08,
        0.07,
        0,
        0,
        0.7,
      );
    }

    // Railing, with a gap where the stair lands.
    const gap: [number, number] = [CAT_Z0 - 0.2, CAT_Z0 + 1.3];
    const posts = 10;
    for (let q = 0; q <= posts; q++) {
      const pz = CAT_Z0 + (q * len) / posts;
      if (pz > gap[0] && pz < gap[1]) continue;
      B.steel.box(CAT_X + CAT_W / 2, CAT_Y + 0.56, pz, 0.05, 1.12, 0.05);
    }
    for (const [z0, z1] of [
      [gap[1], CAT_Z1],
    ] as [number, number][]) {
      for (const ry of [1.1, 0.57]) {
        B.steel.box(CAT_X + CAT_W / 2, CAT_Y + ry, (z0 + z1) / 2, 0.055, 0.055, z1 - z0);
      }
      B.steel.box(CAT_X + CAT_W / 2 - 0.01, CAT_Y + 0.09, (z0 + z1) / 2, 0.03, 0.15, z1 - z0);
    }

    // The stair down at the south end. Treads run south, away from the deck.
    const TREADS = 14;
    const GOING = 0.28;
    const rise = CAT_Y / TREADS;
    const sz0 = CAT_Z0 - 0.4;
    const angle = Math.atan2(CAT_Y, TREADS * GOING);
    for (let i = 0; i < TREADS; i++) {
      const tz = sz0 - (i + 0.5) * GOING;
      const ty = CAT_Y - (i + 0.5) * rise;
      B.grate.box(CAT_X, ty, tz, CAT_W - 0.2, 0.04, GOING + 0.03);
      B.steel.box(CAT_X, ty - rise / 2, tz - GOING / 2 + 0.01, CAT_W - 0.2, rise * 0.55, 0.02);
    }
    for (const s of [-1, 1] as const) {
      const sx = CAT_X + s * (CAT_W / 2 - 0.06);
      const runLen = TREADS * GOING;
      B.steel.box(
        sx,
        CAT_Y / 2,
        sz0 - runLen / 2,
        0.06,
        0.3,
        Math.hypot(runLen, CAT_Y) + 0.2,
        angle,
        0,
        0,
      );
      B.steel.box(
        sx,
        CAT_Y / 2 + 0.9,
        sz0 - runLen / 2,
        0.05,
        0.05,
        Math.hypot(runLen, CAT_Y) + 0.1,
        angle,
        0,
        0,
      );
      for (let q = 0; q < 4; q++) {
        const f = (q + 0.5) / 4;
        B.steel.box(sx, CAT_Y * (1 - f) + 0.5, sz0 - f * runLen, 0.045, 1.0, 0.045);
      }
    }

    // Fallen scale and paint on the deck — twenty years of a leaking roof.
    for (let k = 0; k < 60; k++) {
      B.steel.box(
        CAT_X + (rng() - 0.5) * (CAT_W - 0.3),
        CAT_Y + 0.015,
        CAT_Z0 + rng() * len,
        0.05 + rng() * 0.14,
        0.006,
        0.05 + rng() * 0.14,
        (rng() - 0.5) * 0.2,
        rng() * Math.PI,
        (rng() - 0.5) * 0.2,
      );
    }
  }

  /* -------------------------------------------------------------- pipework -- */

  /**
   * The main steam header and everything hanging off it.
   *
   * A single lagged run north–south above the catwalk, fed by a branch off each
   * boiler's stop valve and taken away east to the engine bed. This is the pipe
   * that makes the volume above head height read as machinery rather than as
   * empty air, and it is the visual line connecting the three valves the puzzle
   * asks you to sequence to the board that switches what they drive.
   */
  private buildPipework(B: Batches): void {
    const len = 15.2;
    B.steel.cylZ(HDR_X, HDR_Y, 0, 0.44, len);
    // Lagging bands.
    for (let k = -7; k <= 7; k++) {
      B.steel.cylZ(HDR_X, HDR_Y, k * 1.05, 0.48, 0.07);
    }
    // Branch from each boiler crown up into the header, with a flange.
    for (const bz of BOILER_Z) {
      const vx = SET_X1 - 0.5;
      B.steel.cylY(vx, (SET_H + 0.9 + HDR_Y) / 2, bz, 0.24, HDR_Y - SET_H - 0.9);
      B.steel.cylX((vx + HDR_X) / 2, HDR_Y, bz, 0.24, HDR_X - vx);
      B.steel.cylX(vx + 0.1, HDR_Y, bz, 0.36, 0.06);
      B.steel.cylX(HDR_X - 0.32, HDR_Y, bz, 0.36, 0.06);
      // Elbow.
      B.steel.sphere(vx, HDR_Y, bz, 0.3);
    }
    // Hangers up to the trusses.
    for (const tx of TRUSS_X) {
      if (tx > HDR_X + 1 || tx < HDR_X - 1) continue;
      for (const hz of [-5.5, 0, 5.5]) {
        B.steel.box(HDR_X, (HDR_Y + 0.5 + TRUSS_Y) / 2, hz, 0.05, TRUSS_Y - HDR_Y - 0.5, 0.05);
        B.steel.box(HDR_X, HDR_Y + 0.5, hz, 0.5, 0.06, 0.06);
      }
    }
    // The take-off east to the engine bed, dropping and running low.
    B.steel.cylX((HDR_X + 0.5) / 2 + 0.5, HDR_Y, -1.4, 0.34, Math.abs(HDR_X) + 1.0);
    B.steel.sphere(HDR_X, HDR_Y, -1.4, 0.4);
    B.steel.cylY(0.9, (HDR_Y + 1.7) / 2, -1.4, 0.34, HDR_Y - 1.7);
    B.steel.sphere(0.9, HDR_Y, -1.4, 0.38);
    B.steel.cylZ(0.9, 1.7, -1.4, 0.34, 1.2);

    // Condensate and feed lines at low level along the boiler fronts, with a
    // pair of globe valves. Dark furniture: without it the base of the setting
    // is a blank 22 m of brick.
    for (const [py, pd] of [
      [1.35, 0.16],
      [1.05, 0.13],
    ] as [number, number][]) {
      B.steel.cylZ(SET_X1 + 1.75, py, 0, pd, 15.0);
      for (const bz of BOILER_Z) {
        B.steel.cylZ(SET_X1 + 1.75, py, bz, pd + 0.09, 0.16);
        B.steel.cylX(SET_X1 + 1.2, py, bz + 0.5, pd, 1.1);
        B.steel.cylY(SET_X1 + 1.75, py + 0.22, bz - 0.9, 0.12, 0.28);
        B.steel.torusY(SET_X1 + 1.75, py + 0.38, bz - 0.9, 0.3, 0.04);
      }
    }
    // Conduit drops down the piers of the north wall — dark vertical furniture.
    for (const cx of [-12.8, -2.4]) {
      B.steel.box(cx, EAVE / 2, Z_N - 0.14, 0.11, EAVE, 0.11);
      for (let k = 0; k < 4; k++) {
        B.steel.box(cx, 0.7 + k * 1.6, Z_N - 0.2, 0.26, 0.09, 0.26);
      }
    }
  }

  /* -------------------------------------------------------------- coal road -- */

  /**
   * Coal handling, on the north wall — because the rail spur ran into the yard
   * along **Main Street**, which is north of this building. That is one of the
   * five documented facts the plan hangs off.
   *
   * A raised concrete bunker against the wall, three steel chutes down to the
   * firing floor, the coal door onto the road, and the timber staging the
   * barrows ran on.
   */
  private buildCoalRoad(B: Batches, rng: () => number): void {
    const bx0 = -16.4;
    const bx1 = -9.6;
    const bz = Z_N - 1.8;

    // Bunker box: a raised concrete hopper, open at the top.
    B.slab.box((bx0 + bx1) / 2, 1.55, bz + 1.5, bx1 - bx0, 3.1, 0.4);
    B.slab.box((bx0 + bx1) / 2, 1.55, bz - 1.5, bx1 - bx0, 3.1, 0.4);
    for (const e of [bx0, bx1]) B.slab.box(e, 1.55, bz, 0.4, 3.1, 3.4);
    // Sloped hopper bottom, as three stepped slabs.
    for (let k = 0; k < 3; k++) {
      B.slab.box(
        (bx0 + bx1) / 2,
        1.0 + k * 0.34,
        bz + (k - 1) * 0.5,
        bx1 - bx0 - 0.6,
        0.22,
        1.5,
        -0.45,
        0,
        0,
      );
    }
    // Coal still in it.
    for (let k = 0; k < 90; k++) {
      const s = 0.08 + rng() * 0.16;
      B.wet.box(
        bx0 + 0.5 + rng() * (bx1 - bx0 - 1.0),
        1.6 + rng() * 0.5,
        bz + (rng() - 0.5) * 2.4,
        s,
        s * 0.75,
        s * 1.15,
        rng() * 2,
        rng() * 3,
        rng() * 2,
      );
    }

    // Three chutes down to the firing floor, one per boiler.
    for (const cz of BOILER_Z) {
      if (cz < 0) continue;
      const cx = -13.0;
      B.steel.box(cx, 1.2, bz - 2.6, 0.9, 0.7, 2.0, 0.6, 0, 0);
      B.steel.box(cx, 0.55, bz - 3.4, 0.9, 0.05, 1.2);
    }
    // Two more chutes, staggered so the bank is not symmetrical.
    for (const cx of [-15.2, -10.6]) {
      B.steel.box(cx, 1.35, bz - 2.3, 0.85, 0.65, 1.9, 0.55, 0, 0);
      B.steel.box(cx, 0.7, bz - 3.1, 0.85, 0.05, 1.1);
    }

    // The coal door: a wide sliding steel leaf on a top track, half open.
    {
      const dz = Z_N + WT / 2;
      B.steel.box(-7.4, 3.5, Z_N - 0.12, 2.6, 0.16, 0.2);
      B.door.box(-8.2, 1.7, Z_N - 0.16, 1.5, 3.4, 0.1);
      B.steel.box(-8.2, 3.42, Z_N - 0.16, 1.5, 0.12, 0.16);
      // The road surface beyond, catching a little light.
      B.slab.box(-7.4, 0.02, dz + 1.2, 2.4, 0.06, 2.4);
      // The rail the coal cars ran on, just outside the door.
      for (const rz of [-0.4, 0.4]) {
        B.steel.box(-7.4, 0.07, Z_N + 2.0 + rz, 3.4, 0.1, 0.09);
      }
    }

    // Timber staging along the bunker face, where the barrows ran.
    for (let k = 0; k < 9; k++) {
      B.timber.box(bx0 + 0.6 + k * 0.78, 0.62, bz - 4.3, 0.7, 0.08, 2.2);
    }
    for (const sx of [bx0 + 0.8, -13.2, bx1 - 0.8]) {
      B.timber.box(sx, 0.3, bz - 3.4, 0.14, 0.6, 0.14);
      B.timber.box(sx, 0.3, bz - 5.2, 0.14, 0.6, 0.14);
      B.timber.box(sx, 0.6, bz - 4.3, 0.12, 0.12, 2.0);
    }
    // A barrow tipped on its side, and a shovel.
    B.steel.box(-11.4, 0.28, 2.2, 0.9, 0.5, 0.62, 0.2, 1.1, 1.4);
    B.timber.box(-10.8, 0.16, 2.8, 1.2, 0.07, 0.07, 0, 0.7, 0.1);
  }

  /* -------------------------------------------------------------- fire bay -- */

  /**
   * The NE corner.
   *
   * **The prison fire department occupied the north-east corner of the
   * powerhouse from 1893 until the 1914 Fire House opened** — documented. So
   * there is an apparatus-bay-shaped opening in the north wall here, wide
   * enough for a hose cart, and it has been dead for a century: bricked up
   * (later, machine-made, tight joints) with a small pedestrian door left in
   * it, the hose-drying rack still bolted to the wall inside, and the apron
   * worn into the floor where the cart came and went.
   */
  private buildFireBay(B: Batches): void {
    const x0 = 0.9;
    const x1 = 3.7;
    const xc = (x0 + x1) / 2;
    const h = 3.3;
    const nZ = Z_N + WT / 2;

    // Segmental brick arch head, springing off stone jambs.
    for (let v = 0; v < 11; v++) {
      const a = Math.PI * (0.1 + (v / 10) * 0.8);
      B.brick.box(
        xc + Math.cos(a) * 1.55,
        h - 0.15 + Math.sin(a) * 0.5,
        nZ,
        0.34,
        0.34,
        WT + 0.06,
        0,
        0,
        a - Math.PI / 2,
      );
    }
    B.stone.box(xc, (h + 0.6 + EAVE) / 2, nZ, x1 - x0 + 0.9, EAVE - h - 0.6, WT);
    for (const s of [-1, 1] as const) {
      B.stone.box(xc + s * ((x1 - x0) / 2 + 0.2), h / 2, nZ, 0.4, h, WT + 0.06);
    }

    // The infill: later brick, laid flush, with a pedestrian door in it.
    B.brickLate.box(xc - 0.75, h / 2, nZ, x1 - x0 - 1.5, h, WT - 0.1);
    B.brickLate.box(xc + 0.95, h / 2, nZ, 0.9, h, WT - 0.1);
    B.brickLate.box(xc + 0.35, (2.15 + h) / 2, nZ, 1.3, h - 2.15, WT - 0.1);
    B.door.box(xc + 0.35, 1.07, Z_N - 0.06, 1.0, 2.14, 0.09);
    B.steel.box(xc - 0.1, 1.05, Z_N - 0.12, 0.07, 0.16, 0.07);

    // Hose-drying rack: a run of iron pins high on the wall inside.
    for (let k = 0; k < 7; k++) {
      B.steel.cylZ(x0 + 0.2 + k * 0.42, 4.35, Z_N - 0.35, 0.05, 0.6);
      B.steel.sphere(x0 + 0.2 + k * 0.42, 4.35, Z_N - 0.62, 0.09);
    }
    B.steel.box(xc, 4.55, Z_N - 0.1, x1 - x0, 0.12, 0.14);

    // The worn apron in the floor where the cart ran, and its two rail stubs.
    B.slab.box(xc, 0.015, Z_N - 1.9, x1 - x0 + 0.4, 0.05, 3.4);
    for (const s of [-1, 1] as const) {
      B.steel.box(xc + s * 0.62, 0.04, Z_N - 1.6, 0.07, 0.07, 2.6);
    }
  }

  /* ------------------------------------------------------------- generator -- */

  /**
   * The engine and generator on their concrete bed.
   *
   * "Generators and boilers for the whole complex" is documented; the machine
   * itself is typology — a horizontal engine belted to a DC generator, which is
   * what a small 1893 municipal-scale plant looked like. It sits north of the
   * hall's centre line so the corridor view stays open and so the plan is not
   * symmetrical.
   */
  private buildGenerator(B: Batches): void {
    const gx = -3.4;
    const gz = 4.0;

    B.slab.box(gx, 0.28, gz, 5.2, 0.56, 3.0);
    B.slab.box(gx, 0.06, gz, 5.8, 0.12, 3.6);
    // Anchor bolts.
    for (let k = 0; k < 6; k++) {
      for (const s of [-1, 1] as const) {
        B.steel.cylY(gx - 2.2 + k * 0.88, 0.62, gz + s * 1.3, 0.07, 0.16);
      }
    }

    // The engine: a horizontal cylinder, crosshead guide, crank and flywheel.
    B.steel.cylX(gx - 1.7, 1.15, gz - 0.6, 1.0, 1.7);
    B.steel.cylX(gx - 0.75, 1.15, gz - 0.6, 1.16, 0.16);
    B.steel.box(gx - 0.1, 1.15, gz - 0.6, 1.3, 0.5, 0.62);
    B.steel.cylX(gx + 0.4, 1.15, gz - 0.6, 0.16, 0.8);
    // Flywheel, standing in the XY plane.
    B.steel.torusX(gx + 1.1, 1.15, gz - 0.6, 2.1, 0.22);
    B.steel.cylX(gx + 1.1, 1.15, gz - 0.6, 0.44, 0.34);
    for (let k = 0; k < 6; k++) {
      const a = (k / 6) * Math.PI * 2;
      B.steel.box(
        gx + 1.1,
        1.15 + Math.sin(a) * 0.5,
        gz - 0.6 + Math.cos(a) * 0.5,
        0.12,
        1.05,
        0.09,
        a,
        0,
        0,
      );
    }
    // Governor on its stand.
    B.steel.cylY(gx - 1.4, 2.1, gz - 0.6, 0.09, 0.9);
    for (const s of [-1, 1] as const) {
      B.steel.sphere(gx - 1.4 + s * 0.22, 2.4, gz - 0.6, 0.16);
      B.steel.box(gx - 1.4 + s * 0.11, 2.52, gz - 0.6, 0.28, 0.04, 0.04, 0, 0, s * 0.5);
    }

    // The generator: a big drum with a commutator end and brush gear.
    B.steel.cylX(gx + 0.4, 1.3, gz + 1.0, 1.7, 2.2);
    B.steel.cylX(gx - 0.75, 1.3, gz + 1.0, 1.1, 0.3);
    B.steel.cylX(gx + 1.6, 1.3, gz + 1.0, 0.9, 0.4);
    B.steel.box(gx + 0.4, 2.2, gz + 1.0, 1.4, 0.5, 1.2);
    // Pedestal bearings.
    for (const bx of [gx - 1.0, gx + 1.85]) {
      B.steel.box(bx, 0.85, gz + 1.0, 0.4, 0.9, 0.7);
    }
    // The belt between them, slack — nothing here is taut.
    for (let k = 0; k < 9; k++) {
      const f = k / 8;
      const sag = Math.sin(f * Math.PI) * 0.22;
      B.timber.box(
        gx + 1.1 - 0.02,
        1.15 + 1.05 - sag,
        gz - 0.6 + f * 1.6,
        0.3,
        0.04,
        0.24,
        0,
        0,
        0,
      );
    }
    // Cable trunking from the generator into the floor, heading for the board.
    B.steel.box(gx + 2.3, 0.5, gz + 1.0, 0.3, 1.0, 0.3);
    B.steel.box((gx + 2.3 + SB_X) / 2, 0.14, gz + 1.0, SB_X - gx - 2.3, 0.28, 0.34);
  }

  /* ------------------------------------------------------------ switchboard -- */

  /**
   * The relay board — four slate panels on a raised base, facing the hall.
   *
   * Period practice: black enamelled slate or marble panels carrying knife
   * switches on marble mounts, rheostat handwheels, circular ammeter and
   * voltmeter faces, and open bus bars on standoff insulators behind and above.
   * "Open" is the point: pre-1910 switchgear had live copper hanging in free
   * air behind a rail, which is exactly why the DANGER plate exists.
   *
   * With the power off the dial faces are dead grey. With it on the pilots come
   * up and the faces catch the string light — that is half the reward read.
   */
  private buildSwitchboard(B: Batches): void {
    const zc = (SB_Z0 + SB_Z1) / 2;
    const len = SB_Z1 - SB_Z0;

    // Raised base and the frame.
    B.slab.box(SB_X + 0.1, 0.14, zc, 1.1, 0.28, len + 0.5);
    for (const s of [-1, 1] as const) {
      B.steel.box(SB_X + 0.22, SB_H / 2 + 0.28, zc + s * (len / 2 + 0.1), 0.14, SB_H, 0.16);
    }
    B.steel.box(SB_X + 0.22, SB_H + 0.34, zc, 0.16, 0.14, len + 0.4);

    // Four panels, with a narrow reveal between them.
    for (let p = 0; p < 4; p++) {
      const pz = SB_Z0 + (len * (p + 0.5)) / 4;
      const pw = len / 4 - 0.06;
      B.slate.box(SB_X, SB_H / 2 + 0.28, pz, 0.06, SB_H, pw);
      // Bevelled slate edge.
      B.slate.box(SB_X - 0.02, SB_H + 0.24, pz, 0.1, 0.1, pw);

      // Instrument faces: a big one over a small one on each panel.
      B.steel.cylX(SB_X - 0.05, 2.18, pz, 0.36, 0.09);
      B.gauge.cylX(SB_X - 0.11, 2.18, pz, 0.31, 0.02);
      B.steel.cylX(SB_X - 0.05, 1.72, pz - 0.14, 0.22, 0.08);
      B.gauge.cylX(SB_X - 0.1, 1.72, pz - 0.14, 0.18, 0.02);

      // Knife switch: two jaws, a blade thrown down, an insulating handle.
      const ky = 1.2;
      for (const s of [-1, 1] as const) {
        B.slate.box(SB_X - 0.06, ky + s * 0.19, pz + 0.12, 0.07, 0.12, 0.22);
        B.steel.box(SB_X - 0.11, ky + s * 0.19, pz + 0.12, 0.05, 0.07, 0.16);
      }
      // Blade, open on three panels and closed on one, so the state is legible.
      const closed = p === 1;
      B.steel.box(
        SB_X - 0.12,
        ky,
        pz + 0.12,
        0.04,
        0.44,
        0.09,
        0,
        0,
        closed ? 0 : 0.85,
      );
      B.timber.box(
        SB_X - 0.14,
        ky - (closed ? 0.28 : 0.18),
        pz + (closed ? 0.12 : 0.3),
        0.05,
        0.16,
        0.06,
      );

      // Rheostat handwheel, low on the panel.
      B.steel.cylX(SB_X - 0.06, 0.78, pz - 0.14, 0.16, 0.1);
      B.steel.torusX(SB_X - 0.13, 0.78, pz - 0.14, 0.4, 0.035);
      for (let k = 0; k < 4; k++) {
        const a = (k / 4) * Math.PI * 2;
        B.steel.box(
          SB_X - 0.13,
          0.78 + Math.sin(a) * 0.1,
          pz - 0.14 + Math.cos(a) * 0.1,
          0.03,
          0.22,
          0.03,
          a,
          0,
          0,
        );
      }

      // Pilot lamp above each panel — dark now, alight when powered.
      B.steel.cylX(SB_X - 0.04, 2.6, pz + 0.16, 0.11, 0.08);
      B.filament.sphere(SB_X - 0.1, 2.6, pz + 0.16, 0.075);
    }

    // Open bus bars behind and above, on standoff insulators.
    for (let k = 0; k < 3; k++) {
      B.steel.box(SB_X + 0.34, 2.95 + k * 0.16, zc, 0.05, 0.1, len + 0.3);
    }
    for (let k = 0; k < 5; k++) {
      const iz = SB_Z0 + (len * k) / 4;
      B.slate.cylX(SB_X + 0.34, 2.78, iz, 0.16, 0.22);
    }
    // Cable drops from the bus into the floor trunking.
    for (const dz of [SB_Z0 + 0.4, zc, SB_Z1 - 0.4]) {
      B.steel.box(SB_X + 0.34, 1.6, dz, 0.07, 2.5, 0.07);
    }
    // The guard rail in front of it, which is all that stood between a man and
    // several hundred volts.
    for (const s of [-1, 1] as const) {
      B.steel.box(SB_X - 1.05, 0.55, zc + s * (len / 2), 0.06, 1.1, 0.06);
    }
    B.steel.box(SB_X - 1.05, 1.08, zc, 0.055, 0.055, len);
  }

  /* -------------------------------------------------------------- conduits -- */

  /**
   * **The puzzle.** Two ducts leaving the blind south wall.
   *
   * Read the class comment for the design. What matters here is that the
   * evidence is entirely physical and entirely visible:
   *
   * - the west duct's mouth is framed in **rebuilt** brick (`brickLate`,
   *   machine-made, tight joints, cooler) where the east duct's is original
   *   1893 stock;
   * - the west duct's cable trays are **cut off and capped** two metres in with
   *   the conductors sheared and hanging, and its run ends at a blind brick
   *   face at 3.3 m — visible from the mouth with a headlamp;
   * - the east duct's trays run continuously into the dark with armoured cable
   *   still on them, and its floor has a worn lane down the middle.
   *
   * The 1901 cast plate over the west duct is the only *label* in the frame and
   * it is the thing that is wrong. Nothing announces that.
   */
  private buildConduits(B: Batches, rng: () => number): void {
    const z0 = Z_S; // inner face of the wall
    for (const [dx, live] of [
      [DUCT_A_X, 0],
      [DUCT_B_X, 1],
    ] as [number, number][]) {
      const late = live === 0;
      const jamb = late ? B.brickLate : B.brick;

      // The duct box itself: floor, crown, cheeks, running away from the hall.
      const dz = z0 - DUCT_LEN / 2;
      jamb.box(dx, -0.06, dz, DUCT_W + 0.5, 0.12, DUCT_LEN);
      jamb.box(dx, DUCT_H + 0.14, dz, DUCT_W + 0.5, 0.28, DUCT_LEN);
      for (const s of [-1, 1] as const) {
        jamb.box(dx + s * (DUCT_W / 2 + 0.16), DUCT_H / 2, dz, 0.32, DUCT_H, DUCT_LEN);
      }

      // The mouth: a segmental brick arch on stone skewbacks, and a reveal.
      for (let v = 0; v < 9; v++) {
        const a = Math.PI * (0.1 + (v / 8) * 0.8);
        jamb.box(
          dx + Math.cos(a) * (DUCT_W / 2 + 0.13),
          DUCT_H - 0.06 + Math.sin(a) * 0.24,
          z0 - 0.12,
          0.24,
          0.24,
          0.42,
          0,
          0,
          a - Math.PI / 2,
        );
      }
      for (const s of [-1, 1] as const) {
        B.stone.box(dx + s * (DUCT_W / 2 + 0.16), DUCT_H - 0.16, z0 - 0.1, 0.3, 0.2, 0.44);
      }
      // Threshold stone, worn on the live duct and clean on the dead one.
      B.stone.box(dx, 0.05, z0 - 0.08, DUCT_W + 0.5, 0.14, 0.5);

      // Cable trays, both sides, on wall brackets.
      const trayEnd = late ? z0 - 2.0 : z0 - DUCT_LEN;
      for (const s of [-1, 1] as const) {
        const tx = dx + s * (DUCT_W / 2 - 0.02);
        const tz = (z0 + trayEnd) / 2;
        B.steel.box(tx, 0.95, tz, 0.1, 0.05, z0 - trayEnd);
        B.steel.box(tx, 0.86, tz, 0.1, 0.05, z0 - trayEnd);
        for (let k = 0; k < Math.round((z0 - trayEnd) / 0.6); k++) {
          B.steel.box(tx, 0.9, z0 - 0.3 - k * 0.6, 0.16, 0.14, 0.05);
        }
        if (late) {
          // Cut and capped. The sheared conductors hang out of the cap.
          B.steel.box(tx, 0.9, trayEnd - 0.03, 0.16, 0.2, 0.06);
          for (let k = 0; k < 4; k++) {
            B.steel.box(
              tx,
              0.86 - k * 0.02,
              trayEnd - 0.16 - k * 0.05,
              0.03,
              0.03,
              0.24,
              -0.5 - rng() * 0.5,
              0,
              0,
            );
          }
        } else {
          // Armoured cable still on the tray, running on into the dark.
          for (const cy of [0.99, 0.93]) {
            B.steel.cylZ(tx, cy, tz, 0.075, z0 - trayEnd);
          }
        }
      }

      if (late) {
        // The blind face: the rebuild bricked this run off. Machine-made brick,
        // laid straight across, three metres in. This is the whole tell.
        B.brickLate.box(dx, DUCT_H / 2, z0 - DUCT_A_BLIND, DUCT_W + 0.6, DUCT_H + 0.3, 0.32);
        // Rubble that has come down against it.
        for (let k = 0; k < 14; k++) {
          const s = 0.1 + rng() * 0.2;
          B.brick.box(
            dx + (rng() - 0.5) * DUCT_W,
            0.06 + s * 0.4,
            z0 - DUCT_A_BLIND + 0.2 + rng() * 0.9,
            s * 1.6,
            s * 0.6,
            s * 0.8,
            rng() * 2,
            rng() * 3,
            rng() * 2,
          );
        }
      } else {
        // The live duct keeps going. A black end plane, a worn lane in the
        // floor, and one more tray bracket just at the edge of the light.
        B.wet.box(dx, DUCT_H / 2, z0 - DUCT_LEN - 0.1, DUCT_W + 0.6, DUCT_H + 0.3, 0.2);
        B.slab.box(dx, 0.02, z0 - DUCT_LEN / 2, DUCT_W - 0.4, 0.05, DUCT_LEN);
      }
    }

    // A junction box and a run of conduit on the wall between the two mouths —
    // the thing that makes both ducts look like live infrastructure.
    B.steel.box((DUCT_A_X + DUCT_B_X) / 2, 2.05, Z_S + 0.14, 0.44, 0.6, 0.24);
    B.steel.box((DUCT_A_X + DUCT_B_X) / 2, 3.0, Z_S + 0.1, 0.09, 1.3, 0.09);
    for (const dx of [DUCT_A_X, DUCT_B_X]) {
      B.steel.box(
        (dx + (DUCT_A_X + DUCT_B_X) / 2) / 2,
        1.85,
        Z_S + 0.14,
        Math.abs(dx - (DUCT_A_X + DUCT_B_X) / 2),
        0.09,
        0.09,
      );
      B.steel.box(dx, 1.4, Z_S + 0.14, 0.09, 0.9, 0.09);
    }
  }

  /* --------------------------------------------------------------- festoon -- */

  /**
   * The building's own festoon lighting: three strands per truss bay, hung off
   * the bottom chords, with an incandescent lamp every metre and a half.
   *
   * They are present in **both** states. Dark, they are a sagging line of dead
   * glass overhead; lit, they are `HEX.incandescent` and they are the reward.
   * Building them only in the powered state would mean the dark room had no
   * explanation for where the light came from.
   *
   * The cable sags. Straight lines read as CAD, and the catenary is most of
   * what a hanging cable is.
   */
  private buildFestoon(B: Batches): void {
    for (const sz of [-5.0, 0.4, 5.4]) {
      for (let bay = 0; bay < TRUSS_X.length - 1; bay++) {
        const x0 = TRUSS_X[bay];
        const x1 = TRUSS_X[bay + 1];
        const span = x1 - x0;
        const sag = 0.85;
        const yAt = (f: number): number => TRUSS_Y - 0.2 - sag * 4 * f * (1 - f);

        const SEG = 8;
        for (let s = 0; s < SEG; s++) {
          const f0 = s / SEG;
          const f1 = (s + 1) / SEG;
          const ax = x0 + span * f0;
          const bx = x0 + span * f1;
          const ay = yAt(f0);
          const by = yAt(f1);
          B.steel.box(
            (ax + bx) / 2,
            (ay + by) / 2,
            sz,
            Math.hypot(bx - ax, by - ay),
            0.022,
            0.022,
            0,
            0,
            Math.atan2(by - ay, bx - ax),
          );
        }
        // Lamps: socket, bulb, and the little hook that carries it.
        const N = 3;
        for (let k = 0; k < N; k++) {
          const f = (k + 0.5) / N;
          const lx = x0 + span * f;
          const ly = yAt(f);
          B.steel.cylY(lx, ly - 0.07, sz, 0.05, 0.11);
          B.filament.sphere(lx, ly - 0.19, sz, 0.115);
          B.filament.cylY(lx, ly - 0.12, sz, 0.045, 0.05);
        }
        // Tie-off at the truss.
        B.steel.box(x0, TRUSS_Y - 0.16, sz, 0.06, 0.16, 0.06);
      }
    }
  }

  /* ---------------------------------------------------------------- debris -- */

  private buildDebris(B: Batches, rng: () => number): void {
    // Fallen roof sheet, brick and mortar under the two breaches — a building
    // failing slowly, not a set-dressed ruin.
    for (const [bx, bz] of [
      [-15.8, -5.0],
      [-5.4, -6.4],
    ] as [number, number][]) {
      for (let k = 0; k < 22; k++) {
        const s = 0.1 + rng() * 0.24;
        B.brick.box(
          bx + (rng() - 0.5) * 4.5,
          0.06 + s * 0.3,
          bz + (rng() - 0.5) * 3.2,
          s * 1.7,
          s * 0.55,
          s * 0.8,
          rng() * 2,
          rng() * 3,
          rng() * 2,
        );
      }
      for (let k = 0; k < 6; k++) {
        B.steel.box(
          bx + (rng() - 0.5) * 4.0,
          0.05,
          bz + (rng() - 0.5) * 3.0,
          0.6 + rng() * 1.0,
          0.03,
          0.4 + rng() * 0.7,
          (rng() - 0.5) * 0.3,
          rng() * Math.PI,
          (rng() - 0.5) * 0.3,
        );
      }
    }

    // Scale and rust flake off the boilers, along the firing floor.
    for (let k = 0; k < 200; k++) {
      B.steel.box(
        SET_X1 + 0.4 + rng() * 2.6,
        0.15,
        (rng() - 0.5) * 15.5,
        0.04 + rng() * 0.14,
        0.006,
        0.04 + rng() * 0.14,
        (rng() - 0.5) * 0.16,
        rng() * Math.PI,
        (rng() - 0.5) * 0.16,
      );
    }

    // Odds and ends a working plant leaves behind: a bench, a barrel, a stack
    // of firebrick, a length of pipe. Sparse and against the walls.
    B.timber.box(-1.2, 0.85, -7.0, 2.2, 0.08, 0.7);
    for (const lx of [-2.1, -0.3]) {
      B.timber.box(lx, 0.42, -7.0, 0.1, 0.84, 0.6);
    }
    B.timber.box(-1.2, 0.55, -7.24, 2.2, 0.06, 0.14);
    B.steel.cylY(-6.6, 0.42, 6.6, 0.62, 0.84);
    B.steel.torusY(-6.6, 0.8, 6.6, 0.66, 0.04);
    for (let k = 0; k < 12; k++) {
      B.brick.box(
        1.4 + (k % 3) * 0.24,
        0.05 + Math.floor(k / 3) * 0.09,
        6.4,
        0.22,
        0.08,
        0.46,
        0,
        (rng() - 0.5) * 0.08,
        0,
      );
    }
    for (let k = 0; k < 5; k++) {
      B.steel.cylZ(-11.0 + rng() * 1.4, 0.09, 6.9 + rng() * 0.6, 0.11, 1.4 + rng() * 1.2);
    }
  }

  /* ----------------------------------------------------------------- signs -- */

  /**
   * Every piece of legible text in the room, on one atlas and one draw call.
   *
   * The cast plate is the puzzle, so it is rendered large enough to read at the
   * anchor distance — 1.3 m across at 3 m from the camera is roughly 280 px of
   * a 1920 px frame, which puts its main line at about 30 px tall. Anything
   * smaller and the puzzle would only exist in the source.
   */
  private buildSigns(ctx: ReturnType<GameScene['kit']>): void {
    const tex = buildSignAtlas(this.scene);
    const mat = new PBRMaterial('phSignMat', this.scene);
    mat.albedoTexture = tex;
    mat.useAlphaFromAlbedoTexture = true;
    mat.transparencyMode = PBRMaterial.PBRMATERIAL_ALPHATEST;
    mat.alphaCutOff = 0.3;
    mat.metallic = 0;
    mat.roughness = 0.72;
    mat.ambientColor = new Color3(1, 1, 1);
    mat.environmentIntensity = 0.5;
    mat.enableSpecularAntiAliasing = true;
    mat.maxSimultaneousLights = profile().maxLights;
    mat.backFaceCulling = true;
    // Nudge toward the camera so a 10 mm physical offset never z-fights.
    mat.zOffset = -2;

    const batch = new GeoBatch();
    /** Face directions: 0 = -Z (south), PI = +Z, PI/2 = -X, -PI/2 = +X. */
    const place = (
      cell: number,
      x: number,
      y: number,
      z: number,
      w: number,
      h: number,
      yaw: number,
    ): void => {
      const vd = CreatePlaneVertexData({ width: w, height: h });
      remapUV(vd, cell);
      batch.template(
        vd,
        new Vector3(1, 1, 1),
        Matrix.RotationYawPitchRoll(yaw, 0, 0),
        new Vector3(x, y, z),
      );
    };

    // --- The puzzle, in three pieces --------------------------------------
    // 1901 cast plate over the WEST duct, bolted to original 1893 brick.
    place(0, DUCT_A_X, 2.32, Z_S + 0.11, 1.3, 0.5, Math.PI);
    // The later stencil beside it, half scrubbed: this duct is No. 2 now.
    place(1, DUCT_A_X + 1.15, 2.0, Z_S + 0.1, 0.42, 0.5, Math.PI);
    // The later stencil on the EAST duct's head: No. 1. Nothing else labels it.
    place(2, DUCT_B_X, 2.06, Z_S + 0.1, 0.9, 0.42, Math.PI);

    // --- Plant labelling ---------------------------------------------------
    // Valve numerals on each setting front, facing the hall.
    for (let i = 0; i < 3; i++) {
      place(4 + i, SET_X1 + 0.52, 3.0, BOILER_Z[i], 0.42, 0.42, -Math.PI / 2);
    }
    // Danger plate on the switchboard frame.
    place(3, SB_X - 0.05, 2.88, SB_Z1 + 0.02, 0.62, 0.24, Math.PI / 2);
    // "MAIN STEAM" stencilled on the header lagging.
    place(7, HDR_X - 0.46, HDR_Y + 0.06, -3.2, 1.0, 0.26, Math.PI / 2);
    // The ghost of the fire department's lettering over the bricked-up bay.
    place(8, 2.3, 3.9, Z_N - 0.09, 2.2, 0.42, 0);
    // Boiler-maker's plate on the middle setting.
    place(9, SET_X1 + 0.52, 1.02, BOILER_Z[1] + 1.35, 0.44, 0.3, -Math.PI / 2);
    // Coal-door notice.
    place(10, -8.2, 2.4, Z_N - 0.23, 0.6, 0.3, 0);

    batch.finish(ctx, this.scene, 'phSigns', mat, {
      collide: false,
      cast: false,
      keepUV: true,
    });
  }

  /* ------------------------------------------------------------- colliders -- */

  private buildColliders(ctx: ReturnType<GameScene['kit']>): void {
    const solid = (
      name: string,
      x: number,
      y: number,
      z: number,
      w: number,
      h: number,
      d: number,
      surface?: string,
    ): void => {
      const m = MeshBuilder.CreateBox(name, { width: w, height: h, depth: d }, this.scene);
      m.position.set(x, y, z);
      m.isVisible = false;
      m.material = null;
      ctx.register(m, { collide: true, cast: false, surface });
    };

    const H = RIDGE + 1;
    solid('phColW', X_W - WT / 2, H / 2, 0, WT, H, Z_N - Z_S + WT * 2);
    solid('phColE', X_E + WT / 2, H / 2, 0, WT, H, Z_N - Z_S + WT * 2);
    solid('phColN', 0, H / 2, Z_N + WT / 2, X_E - X_W + WT * 2, H, WT);
    // South wall, cut for the two ducts so both are genuinely enterable.
    {
      const cuts: [number, number][] = [
        [DUCT_A_X - DUCT_W / 2, DUCT_A_X + DUCT_W / 2],
        [DUCT_B_X - DUCT_W / 2, DUCT_B_X + DUCT_W / 2],
      ];
      let x = X_W - WT;
      let i = 0;
      for (const [c0, c1] of [...cuts, [X_E + WT, X_E + WT] as [number, number]]) {
        if (c0 - x > 0.05) {
          solid(`phColS${i++}`, (x + c0) / 2, H / 2, Z_S - WT / 2, c0 - x, H, WT);
        }
        x = Math.max(x, c1);
      }
      // Duct cheeks and crowns, and the blind face that stops the dead one.
      for (const dx of [DUCT_A_X, DUCT_B_X]) {
        for (const s of [-1, 1] as const) {
          solid(
            `phColDuct${dx}${s}`,
            dx + s * (DUCT_W / 2 + 0.2),
            DUCT_H / 2,
            Z_S - DUCT_LEN / 2,
            0.4,
            DUCT_H,
            DUCT_LEN,
          );
        }
        solid(`phColDuctTop${dx}`, dx, DUCT_H + 0.3, Z_S - DUCT_LEN / 2, DUCT_W + 0.8, 0.6, DUCT_LEN);
      }
      solid('phColBlind', DUCT_A_X, DUCT_H / 2, Z_S - DUCT_A_BLIND, DUCT_W + 0.6, DUCT_H, 0.4);
      solid('phColDuctEnd', DUCT_B_X, DUCT_H / 2, Z_S - DUCT_LEN - 0.1, DUCT_W + 0.6, DUCT_H, 0.3);
    }

    // The three boiler settings, the chimney breast and the plant.
    for (const bz of BOILER_Z) {
      solid(`phColSet${bz}`, (SET_X0 + SET_X1) / 2 + 0.4, SET_H / 2, bz, SET_X1 - SET_X0 + 1.4, SET_H, SET_W);
    }
    solid('phColChim', CHIM_X, CHIM_TOP / 2, 0, CHIM_HW * 2 + 0.4, CHIM_TOP, CHIM_HW * 2 + 0.4);
    solid('phColBunker', -13.0, 1.6, Z_N - 1.8, 7.2, 3.2, 3.6);
    solid('phColGen', -3.4, 1.4, 4.0, 5.8, 2.8, 3.6);
    solid('phColBoard', SB_X + 0.1, 1.6, (SB_Z0 + SB_Z1) / 2, 1.2, 3.2, SB_Z1 - SB_Z0 + 0.5);
    solid('phColPump', X_W - WT - 1.5, 0.9, 6.1, 1.4, 1.8, 1.2);

    // The catwalk: deck (grating), railing, and the stair as a ramp — collide-
    // and-slide plus the step-up probe handles a ramp far more predictably
    // than fourteen tread boxes.
    solid('phColCatRail', CAT_X + CAT_W / 2, CAT_Y + 0.6, (CAT_Z0 + CAT_Z1) / 2 + 0.8, 0.14, 1.2, CAT_Z1 - CAT_Z0 - 1.6);
    {
      const TREADS = 14;
      const GOING = 0.28;
      const runLen = TREADS * GOING;
      const angle = Math.atan2(CAT_Y, runLen);
      const ramp = MeshBuilder.CreateBox(
        'phStairRamp',
        { width: CAT_W - 0.2, height: 0.3, depth: Math.hypot(runLen, CAT_Y) },
        this.scene,
      );
      ramp.position.set(CAT_X, CAT_Y / 2 - 0.12, CAT_Z0 - 0.4 - runLen / 2);
      ramp.rotation.x = angle;
      ramp.isVisible = false;
      ramp.material = null;
      ctx.register(ramp, { collide: true, cast: false, surface: 'grating' });
    }

    // A lid, so nothing can be climbed out through the roof.
    solid('phColCeil', 0, EAVE + 1.2, 0, X_E - X_W, 0.4, Z_N - Z_S);
  }

  /* ------------------------------------------------------------- practicals -- */

  /**
   * Two lighting states in one rig.
   *
   * **Dark:** the moon through two torn roof bays and the four gable oculi,
   * plus a single sodium bleed through the east entrance — the warm half of the
   * frame's warm/cool split, and the only thing that says *this way out*.
   *
   * **Powered:** the festoon strands come up. Point lights are budgeted against
   * `profile().maxLights`, because moon + hemispheric fill + headlamp already
   * take three slots and a PBR material silently drops everything past its cap
   * — which is exactly how the headlamp went missing across the whole game
   * once already. They are created at zero intensity rather than disabled, so
   * the shader defines never change between states and nothing has to
   * recompile mid-frame.
   */
  private buildLights(p: ReturnType<typeof profile>): void {
    // The sodium spill through the entrance. Dim, warm, and a long way from
    // the nearest working lamp.
    this.sodium = new PointLight('phSodium', new Vector3(X_E + 1.1, 1.9, 0), this.scene);
    this.sodium.diffuse = C.sodiumVapour;
    this.sodium.specular = C.sodiumVapour.scale(0.35);
    // Physical falloff — this is not a 0-1 dial. Checked against Cellblocks'
    // doorway bleed at 150 and TheVoid's vent bleed at 18.
    this.sodium.intensity = 190;
    this.sodium.range = 17;
    this.sodium.shadowEnabled = false;

    const budget = Math.max(0, Math.min(3, p.maxLights - 4));
    const xs = [-13.4, -5.6, 1.4];
    for (let i = 0; i < budget; i++) {
      const l = new PointLight(`phString${i}`, new Vector3(xs[i], 5.35, 0.4), this.scene);
      l.diffuse = C.incandescent;
      l.specular = C.incandescent.scale(0.5);
      l.intensity = 0;
      l.range = 20;
      l.shadowEnabled = false;
      this.stringLights.push(l);
    }
  }

  /**
   * Flip the whole building's power state.
   *
   * Public because this is the scene's one piece of gameplay API: once an
   * interaction system exists, sequencing the three stop valves and closing the
   * board calls this. It cannot persist across scenes — there is no save
   * system — so what it guarantees instead is that the room is correct in
   * either state at any moment.
   */
  setPowered(on: boolean): void {
    if (on === this.powered) return;
    this.powered = on;

    this.filamentMat.unfreeze();
    // Above the 0.86 bloom threshold on purpose: an incandescent filament is
    // one of the two things in this game that has earned the right to glow.
    this.filamentMat.emissiveColor = on
      ? C.incandescent.scale(2.4)
      : new Color3(0.014, 0.012, 0.009);
    this.filamentMat.albedoColor = on ? srgb('#ffe6c2') : srgb('#3b3833');
    this.filamentMat.freeze();

    this.gaugeMat.unfreeze();
    this.gaugeMat.emissiveColor = on ? srgb('#4a4232') : new Color3(0.01, 0.01, 0.012);
    this.gaugeMat.freeze();

    for (const l of this.stringLights) l.intensity = on ? 240 : 0;
  }

  /**
   * Coal dust and roof dust in the two moon shafts.
   *
   * There is no volumetric pass in the renderer (`QualityProfile.volumetrics`
   * is plumbed and nothing reads it), and the same lesson Cellblocks recorded
   * applies here: a low-alpha additive prism seen close to edge-on veils the
   * whole frame. The moon in this room comes down through the roof almost
   * perpendicular to the money shot's view axis, so a shaft WOULD read here —
   * but it would be the only one in the game and it would be a scene-authored
   * fake of a renderer feature. Particles in the lit volume are honest and they
   * are what a coal hall actually has in it.
   */
  private buildDust(budget: number): void {
    const ps = new ParticleSystem('phDust', Math.min(budget, 1100), this.scene);
    ps.particleTexture = makeDotTexture(this.scene);
    ps.emitter = new Vector3(-7.0, 3.4, -1.0);
    ps.minEmitBox = new Vector3(-9.5, -3.0, -6.0);
    ps.maxEmitBox = new Vector3(9.5, 3.4, 6.0);
    ps.color1 = new Color4(0.74, 0.8, 0.95, 0.36);
    ps.color2 = new Color4(0.58, 0.62, 0.8, 0.14);
    ps.colorDead = new Color4(0.58, 0.62, 0.8, 0);
    ps.minSize = 0.006;
    ps.maxSize = 0.026;
    ps.minLifeTime = 9;
    ps.maxLifeTime = 20;
    ps.emitRate = 190;
    ps.blendMode = ParticleSystem.BLENDMODE_ADD;
    ps.gravity = new Vector3(0, -0.02, 0);
    ps.direction1 = new Vector3(-0.03, -0.05, -0.04);
    ps.direction2 = new Vector3(0.04, 0.02, 0.04);
    ps.minEmitPower = 0.005;
    ps.maxEmitPower = 0.035;
    ps.updateSpeed = 0.012;
    ps.start();
    this.dust = ps;
  }

  /* ---------------------------------------------------- scene materials ---- */

  /**
   * Brick — the one thing the frozen library genuinely does not have, and this
   * scene needs **two** of it.
   *
   * `phBrick` is the 1893 stock: hand-made, red-to-brown (`#7c4a38`–`#96604a`
   * off NRHP photo 15 of the chimney), irregular in colour, with wide lime
   * joints and a lot of soot. `phBrickLate` is what came back after the fire —
   * machine-made, cooler, far more uniform, tight cement joints. Telling them
   * apart at reading distance IS the puzzle, so they are deliberately as
   * different as real brick of those two dates actually is.
   */
  private buildBrickMaterial(name: string, seed: number, late: boolean): PBRMaterial {
    const { albedo, normal } = makeBrickMaps(this.scene, name, seed, late);
    const m = new PBRMaterial(name, this.scene);
    m.albedoTexture = albedo;
    m.bumpTexture = normal;
    m.invertNormalMapY = false;
    m.invertNormalMapX = false;
    m.metallic = 0;
    // Rule 2: roughness contrast is the story. A machine-made cement-jointed
    // wall is measurably less rough than lime-jointed hand-made stock.
    m.roughness = late ? 0.72 : 0.9;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.55;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /** Switchboard slate: black enamelled, semi-gloss, nearly featureless. */
  private buildSlateMaterial(): PBRMaterial {
    const m = new PBRMaterial('phSlate', this.scene);
    m.albedoColor = srgb('#22242a');
    m.metallic = 0.1;
    // Semi-gloss on purpose. Enamelled slate is the only sheen on that wall and
    // it is what makes the board read as an instrument rather than a cupboard.
    m.roughness = 0.34;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.6;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /**
   * Steel bar grating, as an alpha-tested open grid — the same call Cellblocks
   * makes and for the same reason: real grating is ~80% open, which averages to
   * nothing in the mip chain, so the bars are thickened to ~40% coverage and
   * the cutoff dropped so the far end of the run stays solid rather than fizzing.
   */
  private buildGratingMaterial(): PBRMaterial {
    const m = new PBRMaterial('phGratingMat', this.scene);
    m.albedoTexture = makeGratingTexture(this.scene);
    m.useAlphaFromAlbedoTexture = true;
    m.transparencyMode = PBRMaterial.PBRMATERIAL_ALPHATEST;
    m.alphaCutOff = 0.22;
    m.metallic = 0.35;
    m.roughness = 0.66;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.5;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    // Every mesh using this is a closed slab, so the underside is its own face.
    // A double-sided alpha-tested surface at a grazing angle doubles the
    // discard work with no early-Z to save it.
    m.backFaceCulling = true;
    m.freeze();
    return m;
  }

  /**
   * Window and oculus glazing. Opaque emissive rather than alpha-blended: same
   * read, no sorting risk, and because it is registered as a non-caster the
   * moon still passes cleanly through the opening behind it.
   */
  private buildGlazingMaterial(): PBRMaterial {
    const m = new PBRMaterial('phGlazing', this.scene);
    m.albedoColor = new Color3(0.03, 0.035, 0.04);
    m.metallic = 0;
    m.roughness = 0.45;
    // Below the bloom threshold. If this blooms, it is wrong.
    m.emissiveColor = C.moonlight.scale(0.72);
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.4;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /** Lamp glass. Its emissive IS the `powered` flip. */
  private buildFilamentMaterial(): PBRMaterial {
    const m = new PBRMaterial('phFilament', this.scene);
    m.albedoColor = srgb('#3b3833');
    m.metallic = 0;
    m.roughness = 0.24;
    m.emissiveColor = new Color3(0.014, 0.012, 0.009);
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.5;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /** Gauge and instrument faces: enamel dials, dead until the board is live. */
  private buildGaugeMaterial(): PBRMaterial {
    const m = new PBRMaterial('phGauge', this.scene);
    m.albedoColor = srgb('#b8b2a2');
    m.metallic = 0;
    m.roughness = 0.5;
    m.emissiveColor = new Color3(0.01, 0.01, 0.012);
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.45;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /* ------------------------------------------------------------- runtime --- */

  override update(dt: number, player?: Player): void {
    this.t += dt;

    // The shot harness has no way to ask a scene for a gameplay state, and this
    // scene's whole point is that it has two of them. So the two anchors whose
    // names end in `-lit` carry the powered state: when the camera is sitting
    // exactly on one of their eye positions (anchor mode copies the position
    // verbatim, so the match is exact rather than approximate), the power is
    // on. During real play nothing ever lands on those coordinates to within a
    // centimetre, and `setPowered` remains the real entry point.
    if (player) {
      const eye = player.eyePosition;
      let lit = false;
      for (const a of this.poweredAt) {
        if (Vector3.DistanceSquared(eye, a) < 1e-4) {
          lit = true;
          break;
        }
      }
      if (lit !== this.powered) this.setPowered(lit);
    }

    // The sodium outside is on a failing ballast: two detuned sines and a rare
    // dropout reads as electrical rather than as an animation curve.
    if (this.sodium) {
      const slow = Math.sin(this.t * 0.47) * 0.5 + Math.sin(this.t * 1.31) * 0.22;
      const dropout = Math.sin(this.t * 0.09) > 0.988 ? 0.35 : 1;
      this.sodium.intensity = (190 + slow * 20) * dropout;
    }

    // A hundred and thirty year old plant on a hundred year old wiring: the
    // strings breathe slightly rather than sitting on a flat DC value.
    if (this.powered) {
      const f = 1 + Math.sin(this.t * 0.83) * 0.03 + Math.sin(this.t * 2.17) * 0.015;
      for (const l of this.stringLights) l.intensity = 240 * f;
    }
  }

  override dispose(): void {
    this.dust?.dispose();
    this.sodium?.dispose();
    for (const l of this.stringLights) l.dispose();
    this.stringLights = [];
    super.dispose();
  }
}

/* ========================================================================== */
/*  Geometry batching                                                         */
/* ========================================================================== */

interface Batches {
  stone: GeoBatch;
  brick: GeoBatch;
  brickLate: GeoBatch;
  slab: GeoBatch;
  wet: GeoBatch;
  steel: GeoBatch;
  front: GeoBatch;
  door: GeoBatch;
  grate: GeoBatch;
  glaze: GeoBatch;
  timber: GeoBatch;
  slate: GeoBatch;
  filament: GeoBatch;
  gauge: GeoBatch;
}

/* Shared templates. Built once, transformed thousands of times. */
const BOX = CreateBoxVertexData({ size: 1 });
/** Unit cylinder: height 1, diameter 1, so scale is (d, len, d). */
const CYL = CreateCylinderVertexData({ height: 1, diameter: 1, tessellation: 18 });
/** Low-poly sphere for rivets and lamp glass — 18 tris a piece. */
const SPH = CreateSphereVertexData({ diameter: 1, segments: 4 });
/** Unit torus: outside diameter 1, so scale is (d, d, d). */
const TORUS = CreateTorusVertexData({ diameter: 1, thickness: 0.14, tessellation: 14 });

/** Cylinder/torus axis rotations. A primitive's own axis is +Y. */
const AX_X = Matrix.RotationYawPitchRoll(0, 0, Math.PI / 2);
const AX_Z = Matrix.RotationYawPitchRoll(0, Math.PI / 2, 0);

/**
 * A CPU-side mesh accumulator — the same device Cellblocks and TheVoid use.
 *
 * UVs are deliberately NOT written for primitive geometry: the batch bakes
 * world positions into the vertices, so `worldUV` at the end gives every piece
 * a different patch of the texture for free, and no two boiler fronts in the
 * run sample the same rust.
 */
class GeoBatch {
  private positions: number[] = [];
  private normals: number[] = [];
  private uvs: number[] = [];
  private indices: number[] = [];
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

  cylY(x: number, y: number, z: number, d: number, len: number): void {
    this.append(CYL, d, len, d, null, x, y, z);
  }

  cylX(x: number, y: number, z: number, d: number, len: number): void {
    this.append(CYL, d, len, d, AX_X, x, y, z);
  }

  cylZ(x: number, y: number, z: number, d: number, len: number): void {
    this.append(CYL, d, len, d, AX_Z, x, y, z);
  }

  torusY(x: number, y: number, z: number, d: number, t: number): void {
    this.append(TORUS, d, (t / 0.14) * d, d, null, x, y, z);
  }

  torusX(x: number, y: number, z: number, d: number, t: number): void {
    this.append(TORUS, d, (t / 0.14) * d, d, AX_X, x, y, z);
  }

  sphere(x: number, y: number, z: number, d: number): void {
    this.append(SPH, d, d, d, null, x, y, z);
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
    // Always write a UV pair per vertex, even when the source has none: a batch
    // that mixes authored-UV geometry (a sign quad pointed at an atlas cell)
    // with unauthored geometry otherwise ends up with the two streams out of
    // step and every quad after the first reads the wrong texels.
    if (uv && uv.length === (src.length / 3) * 2) {
      for (let i = 0; i < uv.length; i++) this.uvs.push(uv[i]);
    } else {
      for (let i = 0; i < src.length / 3; i++) this.uvs.push(0, 0);
    }
    for (let i = 0; i < idx.length; i++) this.indices.push(idx[i] + this.base);
    this.base += src.length / 3;
  }

  /**
   * Emit the batch as `chunks` meshes, split along +X by triangle centroid.
   *
   * One mesh per material is the cheap way to build a scene like this, but a
   * single 22 m mesh is never outside the frustum, so every frame would pay for
   * the whole hall no matter where it was pointed. Vertices are compacted per
   * chunk so a slice carries only the vertices its own triangles use.
   */
  finish(
    ctx: { register: (m: Mesh, o?: Record<string, unknown>) => void },
    scene: Scene,
    name: string,
    material: PBRMaterial | StandardMaterial,
    opts: {
      collide?: boolean;
      cast?: boolean;
      surface?: string;
      uvDensity?: number;
      keepUV?: boolean;
    },
    chunks = 1,
  ): Mesh[] {
    if (!this.indices.length) return [];

    const emit = (idx: ArrayLike<number>, meshName: string): Mesh | null => {
      if (!idx.length) return null;
      const map = new Map<number, number>();
      const pos: number[] = [];
      const nrm: number[] = [];
      const uv: number[] = [];
      const ind: number[] = [];
      for (let i = 0; i < idx.length; i++) {
        const src = idx[i];
        let n = map.get(src);
        if (n === undefined) {
          n = pos.length / 3;
          map.set(src, n);
          pos.push(
            this.positions[src * 3],
            this.positions[src * 3 + 1],
            this.positions[src * 3 + 2],
          );
          nrm.push(this.normals[src * 3], this.normals[src * 3 + 1], this.normals[src * 3 + 2]);
          uv.push(this.uvs[src * 2], this.uvs[src * 2 + 1]);
        }
        ind.push(n);
      }
      const mesh = new Mesh(meshName, scene);
      const vd = new VertexData();
      vd.positions = pos;
      vd.normals = nrm;
      vd.uvs = uv;
      vd.indices = ind;
      vd.applyToMesh(mesh, false);
      mesh.material = material;
      ctx.register(mesh, opts);
      return mesh;
    };

    if (chunks <= 1) {
      const m = emit(this.indices, name);
      return m ? [m] : [];
    }

    let lo = Infinity;
    let hi = -Infinity;
    for (let i = 0; i < this.positions.length; i += 3) {
      const x = this.positions[i];
      if (x < lo) lo = x;
      if (x > hi) hi = x;
    }
    const span = Math.max(1e-6, hi - lo);
    const buckets: number[][] = [];
    for (let k = 0; k < chunks; k++) buckets.push([]);
    for (let t = 0; t < this.indices.length; t += 3) {
      const a = this.indices[t];
      const b = this.indices[t + 1];
      const c = this.indices[t + 2];
      const xc = (this.positions[a * 3] + this.positions[b * 3] + this.positions[c * 3]) / 3;
      const k = Math.max(0, Math.min(chunks - 1, Math.floor(((xc - lo) / span) * chunks)));
      buckets[k].push(a, b, c);
    }

    const out: Mesh[] = [];
    for (let k = 0; k < chunks; k++) {
      const m = emit(buckets[k], `${name}_${k}`);
      if (m) out.push(m);
    }
    return out;
  }
}

/* ========================================================================== */
/*  Generated textures                                                        */
/* ========================================================================== */

const BRICK_S = 512;

/**
 * One tile of brickwork, 1.2 m square: sixteen courses of 75 mm on a running
 * bond of 200 mm stretchers with a 10 mm joint.
 *
 * Two flavours, and they must be distinguishable at three metres because the
 * whole puzzle turns on it. The 1893 stock is hand-made: wide colour spread
 * from `#7c4a38` to `#96604a`, some badly overburnt, deep raked lime joints,
 * heavy soot low in the tile. The rebuild is machine-made: narrow spread,
 * cooler, flush cement joints and almost no soot, because it has only been
 * there since the fire.
 */
function makeBrickMaps(
  scene: Scene,
  name: string,
  seed: number,
  late: boolean,
): { albedo: Texture; normal: Texture } {
  const S = BRICK_S;
  const rows = 16;
  const cols = 6;
  const joint = late ? 3 : 5; // px
  const rh = S / rows;
  const cw = S / cols;

  const albedo = new Uint8ClampedArray(S * S * 4);
  const height = new Float32Array(S * S);
  const rng = mulberry(seed);

  // Per-brick colour and depth, decided once so a brick is one colour.
  const nBricks = rows * (cols + 1);
  const cols3: [number, number, number][] = [];
  const depth: number[] = [];
  const base: [number, number, number] = late ? [150, 116, 100] : [140, 84, 62];
  const spread = late ? 16 : 44;
  for (let i = 0; i < nBricks; i++) {
    const j = (rng() - 0.5) * 2;
    const burnt = !late && rng() < 0.13;
    const k = burnt ? -0.75 : j;
    cols3.push([
      Math.max(20, base[0] + k * spread),
      Math.max(16, base[1] + k * spread * 0.72 + (burnt ? 6 : 0)),
      Math.max(14, base[2] + k * spread * 0.52 + (burnt ? 12 : 0)),
    ]);
    depth.push(late ? 0.9 + rng() * 0.1 : 0.78 + rng() * 0.22);
  }

  const mortar: [number, number, number] = late ? [138, 136, 130] : [146, 138, 120];

  for (let y = 0; y < S; y++) {
    const row = Math.floor(y / rh);
    const inRowY = y - row * rh;
    const stagger = row % 2 === 0 ? 0 : cw / 2;
    for (let x = 0; x < S; x++) {
      const sx = (x + stagger) % S;
      const col = Math.floor(sx / cw);
      const inColX = sx - col * cw;

      const isJoint =
        inRowY < joint || inRowY > rh - joint || inColX < joint || inColX > cw - joint;

      const idx = (y * S + x) * 4;
      // Fine grain, and a soot gradient that is strongest low in the tile —
      // wear follows geometry, never uniformly.
      const grain = 0.86 + rng() * 0.28;
      const soot = late ? 0.03 : 0.34 * (1 - y / S) ** 1.6 + 0.06;

      if (isJoint) {
        const g = grain * 0.96;
        albedo[idx] = mortar[0] * g * (1 - soot);
        albedo[idx + 1] = mortar[1] * g * (1 - soot);
        albedo[idx + 2] = mortar[2] * g * (1 - soot);
        height[y * S + x] = late ? 0.72 : 0.4;
      } else {
        const b = cols3[(row * (cols + 1) + col) % nBricks];
        albedo[idx] = b[0] * grain * (1 - soot);
        albedo[idx + 1] = b[1] * grain * (1 - soot * 1.08);
        albedo[idx + 2] = b[2] * grain * (1 - soot * 1.12);
        // Arris rounding at the brick edges — a hand-made brick is not a slab.
        const eu = Math.min(inColX - joint, cw - joint - inColX) / 6;
        const ev = Math.min(inRowY - joint, rh - joint - inRowY) / 5;
        const edge = Math.min(1, Math.max(0, Math.min(eu, ev)));
        height[y * S + x] =
          depth[(row * (cols + 1) + col) % nBricks] * (late ? 1 : 0.9 + edge * 0.1) * edge +
          0.5 * (1 - edge);
      }
      albedo[idx + 3] = 255;
    }
  }

  const normal = heightToNormal(height, S, late ? 5 : 9);

  return {
    albedo: rawTex(scene, albedo, S, `${name}Albedo`, true),
    normal: rawTex(scene, normal, S, `${name}Normal`, false),
  };
}

function rawTex(
  scene: Scene,
  data: Uint8ClampedArray,
  size: number,
  name: string,
  gamma: boolean,
): Texture {
  const tex = RawTexture.CreateRGBATexture(
    new Uint8Array(data.buffer),
    size,
    size,
    scene,
    true,
    false,
    Texture.TRILINEAR_SAMPLINGMODE,
    Constants.TEXTURETYPE_UNSIGNED_BYTE,
  );
  tex.name = name;
  tex.wrapU = Texture.WRAP_ADDRESSMODE;
  tex.wrapV = Texture.WRAP_ADDRESSMODE;
  tex.anisotropicFilteringLevel = 8;
  (tex as Texture & { gammaSpace: boolean }).gammaSpace = gamma;
  return tex;
}

/**
 * One tile of steel bar grating, 0.30 m square. Bearing bars on the short
 * pitch, cross rods on the long one, and a bright worn line along the top of
 * every bearing bar — the boot polish a headlamp finds first on a walkway.
 */
function makeGratingTexture(scene: Scene): Texture {
  const S = 512;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = S;
  const c = canvas.getContext('2d')!;
  c.clearRect(0, 0, S, S);

  const bearing = 10;
  const bp = S / bearing;
  const bw = Math.round(bp * 0.31);
  for (let i = 0; i < bearing; i++) {
    const x = Math.round(i * bp);
    c.fillStyle = '#413c36';
    c.fillRect(x, 0, bw, S);
    c.fillStyle = '#8d867c';
    c.fillRect(x, 0, Math.max(2, Math.round(bw * 0.34)), S);
    c.fillStyle = '#5b544c';
    c.fillRect(x + bw - 2, 0, 2, S);
  }
  const cross = 3;
  const cp = S / cross;
  const cw = Math.round(cp * 0.13);
  for (let i = 0; i < cross; i++) {
    const y = Math.round(i * cp + cp * 0.3);
    c.fillStyle = '#4c463f';
    c.fillRect(0, y, S, cw);
    c.fillStyle = '#7c756b';
    c.fillRect(0, y, S, Math.max(2, Math.round(cw * 0.4)));
  }

  const img = c.getImageData(0, 0, S, S);
  const d = img.data;
  const rng = mulberry(18930922);
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 8) continue;
    const n = 0.76 + rng() * 0.44;
    d[i] = Math.min(255, d[i] * n * 1.06);
    d[i + 1] = Math.min(255, d[i + 1] * n);
    d[i + 2] = Math.min(255, d[i + 2] * n * 0.92);
  }
  c.putImageData(img, 0, 0);

  const tex = new Texture(canvas.toDataURL('image/png'), scene, false, false);
  tex.hasAlpha = true;
  tex.anisotropicFilteringLevel = 8;
  return tex;
}

/* ---------------------------------------------------------------- signage -- */

const SIGN_ATLAS = 2048;
const SIGN_GRID = 4;
const SIGN_CELL = SIGN_ATLAS / SIGN_GRID;

interface SignSpec {
  /** Width / height of the quad this cell is drawn for. */
  aspect: number;
  draw: (c: CanvasRenderingContext2D, w: number, h: number, rng: () => number) => void;
}

/**
 * Every legible label in the room, on one 2048 atlas.
 *
 * Each cell is drawn in a virtual space matching its quad's aspect ratio and
 * then squashed into the square cell, so nothing is stretched when it lands on
 * geometry. The atlas is worth it for one reason: **the puzzle is text**, and a
 * sign you cannot read is a sign that does not exist.
 */
function buildSignAtlas(scene: Scene): Texture {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = SIGN_ATLAS;
  const c = canvas.getContext('2d')!;
  c.clearRect(0, 0, SIGN_ATLAS, SIGN_ATLAS);

  const rng = mulberry(19010518);

  /** A stencilled character set: hard edges, bridges, uneven ink. */
  const stencil = (
    ctx: CanvasRenderingContext2D,
    text: string,
    w: number,
    h: number,
    colour: string,
    alpha: number,
  ): void => {
    ctx.save();
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const size = Math.min(h * 0.82, (w / Math.max(1, text.length)) * 1.5);
    ctx.font = `bold ${Math.round(size)}px "Arial Narrow", Helvetica, Arial, sans-serif`;
    ctx.fillStyle = colour;
    ctx.globalAlpha = alpha;
    ctx.translate(w / 2, h / 2);
    ctx.rotate((rng() - 0.5) * 0.03);
    ctx.fillText(text, 0, 0);
    // Stencil bridges.
    ctx.globalCompositeOperation = 'destination-out';
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#000';
    for (let b = 0; b < 2; b++) {
      ctx.fillRect(-w, -size * 0.22 + b * size * 0.44, w * 2, Math.max(3, size * 0.05));
    }
    ctx.restore();
  };

  const specs: SignSpec[] = [
    // 0 — THE cast plate. Raised letters on an enamelled iron ground.
    {
      aspect: 1.3 / 0.5,
      draw: (ctx, w, h) => {
        ctx.fillStyle = '#1d211f';
        roundRect(ctx, 0, 0, w, h, h * 0.08);
        ctx.fill();
        ctx.strokeStyle = '#6d6a60';
        ctx.lineWidth = h * 0.035;
        roundRect(ctx, h * 0.07, h * 0.07, w - h * 0.14, h - h * 0.14, h * 0.05);
        ctx.stroke();
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#ded8c8';
        ctx.font = `bold ${Math.round(h * 0.28)}px Georgia, "Times New Roman", serif`;
        ctx.fillText('No. 1 CONDUIT', w / 2, h * 0.3);
        ctx.font = `${Math.round(h * 0.165)}px Georgia, "Times New Roman", serif`;
        ctx.fillText('CELL HOUSES & YARD', w / 2, h * 0.56);
        ctx.font = `${Math.round(h * 0.14)}px Georgia, "Times New Roman", serif`;
        ctx.fillStyle = '#b9b3a2';
        ctx.fillText('ILL. STATE PENITENTIARY  ·  1901', w / 2, h * 0.79);
        // Four bolt heads.
        ctx.fillStyle = '#8c8578';
        for (const bx of [h * 0.16, w - h * 0.16]) {
          for (const by of [h * 0.16, h - h * 0.16]) {
            ctx.beginPath();
            ctx.arc(bx, by, h * 0.05, 0, Math.PI * 2);
            ctx.fill();
          }
        }
      },
    },
    // 1 — the later "2" on the west duct, mostly scrubbed off.
    { aspect: 0.42 / 0.5, draw: (ctx, w, h) => stencil(ctx, '2', w, h, '#d8d2c0', 0.34) },
    // 2 — the later "No. 1" on the east duct. Faded but intact.
    { aspect: 0.9 / 0.42, draw: (ctx, w, h) => stencil(ctx, 'No. 1', w, h, '#d8d2c0', 0.72) },
    // 3 — the danger plate on the board.
    {
      aspect: 0.62 / 0.24,
      draw: (ctx, w, h) => {
        ctx.fillStyle = '#7a2a22';
        ctx.fillRect(0, 0, w, h);
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#e8e2d2';
        ctx.font = `bold ${Math.round(h * 0.44)}px Helvetica, Arial, sans-serif`;
        ctx.fillText('DANGER', w / 2, h * 0.32);
        ctx.font = `${Math.round(h * 0.3)}px Helvetica, Arial, sans-serif`;
        ctx.fillText('250 VOLTS', w / 2, h * 0.72);
      },
    },
    // 4,5,6 — the boiler valve numerals.
    { aspect: 1, draw: (ctx, w, h) => stencil(ctx, '1', w, h, '#dcd6c4', 0.8) },
    { aspect: 1, draw: (ctx, w, h) => stencil(ctx, '2', w, h, '#dcd6c4', 0.8) },
    { aspect: 1, draw: (ctx, w, h) => stencil(ctx, '3', w, h, '#dcd6c4', 0.8) },
    // 7 — MAIN STEAM on the header lagging.
    { aspect: 1.0 / 0.26, draw: (ctx, w, h) => stencil(ctx, 'MAIN STEAM', w, h, '#d4cebc', 0.6) },
    // 8 — the ghost of the fire department's lettering.
    {
      aspect: 2.2 / 0.42,
      draw: (ctx, w, h) => {
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.globalAlpha = 0.26;
        ctx.fillStyle = '#e6dfcc';
        ctx.font = `bold ${Math.round(h * 0.74)}px Georgia, "Times New Roman", serif`;
        ctx.fillText('FIRE  APPARATUS', w / 2, h * 0.52);
      },
    },
    // 9 — a boiler maker's plate.
    {
      aspect: 0.44 / 0.3,
      draw: (ctx, w, h) => {
        ctx.fillStyle = '#3a3128';
        roundRect(ctx, 0, 0, w, h, h * 0.1);
        ctx.fill();
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#cfc7b2';
        ctx.font = `bold ${Math.round(h * 0.24)}px Georgia, serif`;
        ctx.fillText('W. P. Co.', w / 2, h * 0.3);
        ctx.font = `${Math.round(h * 0.19)}px Georgia, serif`;
        ctx.fillText('JOLIET  ILL.', w / 2, h * 0.58);
        ctx.fillText('1893', w / 2, h * 0.82);
      },
    },
    // 10 — the coal-door notice.
    { aspect: 0.6 / 0.3, draw: (ctx, w, h) => stencil(ctx, 'COAL', w, h, '#d4cebc', 0.55) },
  ];

  for (let i = 0; i < specs.length; i++) {
    const cx = (i % SIGN_GRID) * SIGN_CELL;
    const cy = Math.floor(i / SIGN_GRID) * SIGN_CELL;
    const spec = specs[i];
    c.save();
    c.beginPath();
    c.rect(cx, cy, SIGN_CELL, SIGN_CELL);
    c.clip();
    c.translate(cx, cy);
    // Draw in a space with the quad's aspect, then squash into the square cell.
    const vw = SIGN_CELL * spec.aspect;
    c.scale(1 / spec.aspect, 1);
    spec.draw(c, vw, SIGN_CELL, rng);
    c.restore();
  }

  // invertY LEFT ON (Babylon's default) so v = 0 is the bottom of the canvas,
  // which is the convention `remapUV` assumes. Turning it off and "fixing" the
  // mirroring with a u flip is how Cellblocks rendered 144 cell numbers upside
  // down, legible only in the capture.
  const tex = new Texture(canvas.toDataURL('image/png'), scene, false);
  tex.hasAlpha = true;
  tex.wrapU = Texture.CLAMP_ADDRESSMODE;
  tex.wrapV = Texture.CLAMP_ADDRESSMODE;
  tex.anisotropicFilteringLevel = 8;
  return tex;
}

function roundRect(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  w: number,
  h: number,
  r: number,
): void {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + w, y, x + w, y + h, r);
  ctx.arcTo(x + w, y + h, x, y + h, r);
  ctx.arcTo(x, y + h, x, y, r);
  ctx.arcTo(x, y, x + w, y, r);
  ctx.closePath();
}

/** Point a unit-square plane's UVs at one atlas cell. */
function remapUV(vd: VertexData, cell: number): void {
  const uv = vd.uvs as number[] | Float32Array | null;
  if (!uv) return;
  const col = cell % SIGN_GRID;
  const row = SIGN_GRID - 1 - Math.floor(cell / SIGN_GRID);
  const s = 1 / SIGN_GRID;
  for (let i = 0; i < uv.length; i += 2) {
    uv[i] = (col + uv[i]) * s;
    uv[i + 1] = (row + uv[i + 1]) * s;
  }
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

/* ========================================================================== */

/** The same deterministic PRNG the other scenes use, so captures are stable. */
function mulberry(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
