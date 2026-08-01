import { Mesh } from '@babylonjs/core/Meshes/mesh';
import { MeshBuilder } from '@babylonjs/core/Meshes/meshBuilder';
import { VertexData } from '@babylonjs/core/Meshes/mesh.vertexData';
import { CreateBoxVertexData } from '@babylonjs/core/Meshes/Builders/boxBuilder';
import { CreatePlaneVertexData } from '@babylonjs/core/Meshes/Builders/planeBuilder';
import { CreateCylinderVertexData } from '@babylonjs/core/Meshes/Builders/cylinderBuilder';
import { Vector3, Matrix } from '@babylonjs/core/Maths/math.vector';
import { Color3, Color4 } from '@babylonjs/core/Maths/math.color';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { PointLight } from '@babylonjs/core/Lights/pointLight';
import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import type { Scene } from '@babylonjs/core/scene';

import '@babylonjs/core/Particles/particleSystemComponent';

import { GameScene, type SceneManifest } from './SceneBase';
import { C, srgb } from '../core/Palette';
import { profile } from '../core/Settings';

/**
 * Scene 3.1 — The Cellblocks.
 *
 * The **East Cell Block** (#29, Boyington & Wheelock, 1860): four tiers, four
 * hundred cells as built, gutted and refitted in 1951 with larger cells,
 * plumbing and a floor inserted between the second and third tiers. West is the
 * *five*-tier, five-hundred-cell block — a different building, and the two are
 * constantly confused. This is East. Four tiers.
 *
 * Layout comes straight out of RESEARCH.md §3.1: the cells are a **free-standing
 * block in the middle of the building**, set back from the exterior walls and
 * laid back-to-back in two lines facing the north and south walls. So each tier
 * has two galleries, one per side, and the gallery runs *between the cell fronts
 * and the exterior window wall*. You look out of a cell, across a narrow
 * walkway, at a wall of glazed openings. That is the defining view of the space
 * and it is what this scene builds: the south gallery, at x from the shell wall
 * (−3.9) to the cell fronts (0), running 58 m up +Z.
 *
 * There is **no central nave and no roundhouse**. Anything panoptic belongs to
 * Stateville.
 *
 * Composition intent: the money shot is straight down the hall. Four tiers of
 * railings and grating converge on a vanishing point 58 m away; the moon comes
 * in low (≈25°) through twelve double-height window bays on the left and rakes
 * long parallelograms of light across the foot-polished concrete and up the cell
 * fronts on the right; the open light well between the gallery edge and the
 * window wall lets that light fall all the way from the fourth tier to the
 * ground. Everything else is headlamp. The eye should go: floor specular →
 * vanishing point → up the tiers.
 *
 * **The gallery floors on the upper tiers are steel bar grating, not concrete.**
 * The NRHP nomination says "floors and ceilings are painted concrete" as a
 * blanket statement and its own survey photograph 12 contradicts it. The grating
 * is why footsteps carry the way they do in this building, so the decks are
 * tagged `surface: 'grating'` — the audio engine's grating profile rings rather
 * than thumps — and only the ground floor is `'concrete'`.
 *
 * The lever-and-rack gang lock is **typology-inferred, not Joliet-documented**
 * (RESEARCH.md §3.3): no source names Joliet's mechanism. A 1947–53 American
 * cell-house renovation would certainly have used a gang-locking system of this
 * family, so one is modelled — an operating lever at the head of each tier
 * driving a rack bar that runs the length of the run and throws a dog on every
 * door at once. If the Joliet Area Historical Museum ever confirms the make,
 * this is the object to revisit.
 */

/* -------------------------------------------------------------------------- */
/*  Dimensions — one place, so every subsystem agrees                          */
/* -------------------------------------------------------------------------- */

/** Length of the modelled gallery run. The real block is ~400 ft; this is compressed. */
const L = 58;

/** Inner face of the outer shell wall. The galleries run along +Z from here. */
const WALL_X = -3.9;
/**
 * Outer edge of the upper gallery decks. Between here and WALL_X is open well.
 *
 * The well is deliberately WIDER than the walkway. It is what makes the block
 * read as four hollow tiers rather than four corridors stacked on each other:
 * from the ground floor you look up through it and see every deck edge and every
 * railing receding, and the moon coming through the upper bays falls all the way
 * down it. The narrow first pass gave a ground-floor frame with a lid on it.
 */
const WELL_X = -2.05;
/** Front plane of the cell block. Cells run into +X. */
const FRONT_X = 0;
/** Solid curb strip along the cell fronts on the upper tiers (research: photo 12). */
const CURB_X = -0.38;

/** Tier-to-tier. RESEARCH.md §3.4 puts this at ~8'-6"; flagged as extrapolated. */
const TIER_H = 2.65;
const TIERS = 4;
/** Ceiling of the top tier. */
const CEIL_Y = TIERS * TIER_H;

/** Cell bay pitch on the front. The 1951 cells are "larger"; no dimension published. */
const CELL_PITCH = 1.5;
const CELL_N = 36;
const CELL_Z0 = 1.5;
const DOOR_W = 1.06;
const DOOR_H = 2.02;
/** Depth of a fully modelled cell, front plane to back wall. */
const CELL_DEPTH = 2.6;
/** Depth of the shallow shell behind every other door, so the bars have depth. */
const SHELL_DEPTH = 1.5;

/** Twelve bays, per the nomination's description of both cell blocks. */
const BAYS = 12;
const BAY_PITCH = L / BAYS;
/**
 * Clear width of a window opening, and the thickness of the wall it is cut in.
 *
 * These two numbers are a light-transport decision, not a styling one, and the
 * first pass got them wrong in a way that was completely invisible in the source.
 * The moon runs at 25 degrees elevation and about 52 degrees off the wall normal
 * in plan, so a ray crossing a reveal of depth D is displaced 1.31 * D along the
 * wall before it gets inside. At the first pass's 0.95 m wall and 0.96 m clear
 * pane that displacement was 1.24 m — WIDER than the opening — so the reveal
 * shadowed the aperture completely and not one photon of moonlight reached the
 * gallery. The capture looked plausible and was lit entirely by the hemispheric
 * fill; see artifacts/shots/3.1-cellblocks/iter-01 and the headlamp-off probe.
 *
 * At 0.55 m of wall and a 1.26 m clear pane the displacement is 0.72 m, which
 * leaves a 0.54 m band of real moonlight per pane — two per bay, twelve bays.
 * That is the frame.
 */
const OPEN_W = 3.1;
const WALL_T = 0.55;
/** The 1940s openings are double-height: one per external storey, two tiers each. */
const OPEN_LO_Y0 = 1.05;
const OPEN_LO_Y1 = 5.05;
const OPEN_HI_Y0 = 5.8;
const OPEN_HI_Y1 = 9.8;
/** Heavy limestone mullion splitting each opening. */
const MULLION_W = 0.26;
/** Limestone jamb reveal width. */
const JAMB_W = 0.16;
/** Glazed structural tile dado on the shell wall. */
const DADO_H = 1.0;

/** Ground-floor cells you can walk into. Non-adjacent so the slid doors do not collide. */
const OPEN_CELLS = [3, 12, 25];

/** Stair flights: [tier index climbed FROM, z at the bottom riser]. */
const STAIRS: { from: number; z: number }[] = [
  { from: 0, z: 12.4 },
  { from: 1, z: 28.2 },
  { from: 2, z: 43.6 },
];
const STAIR_W = 1.12;
const STAIR_TREADS = 14;
const STAIR_GOING = 0.27;

/* -------------------------------------------------------------------------- */

export class Cellblocks extends GameScene {
  readonly manifest: SceneManifest = {
    id: '3.1-cellblocks',
    title: 'The Cellblocks',
    spawn: { position: [-1.6, 0.15, 3.0], yaw: 0 },
    anchors: [
      {
        name: 'a1-down-the-hall',
        position: [-2.2, 1.66, 6.6],
        rotation: [0, 0.02],
        fov: 64,
        note: 'THE frame, and the one the scene exists for. Ground floor, mid-corridor, straight down 58 m of gallery: four tiers of railing and grating converging on the vanishing point, moonlight bars from the window bays raking left-to-right across foot-polished concrete and up the cell fronts, the first stair flight as a dark foreground silhouette in the light well. If the perspective and that long floor specular do not carry this frame, nothing else in the scene matters.',
      },
      {
        name: 'a2-tier-three',
        position: [-1.2, 6.96, 8.5],
        rotation: [0, 0.055],
        fov: 66,
        note: 'Standing on the third tier looking down the run. Tests the steel bar grating underfoot (alpha-tested open grid, tagged surface:grating), the cantilever brackets and the railing line receding, the cell-front rhythm at eye level, and the delaminating paint hanging from the fourth-tier soffit overhead.',
      },
      {
        name: 'a3-cell-fronts',
        position: [-2.35, 1.62, 15.2],
        rotation: [0.52, 0.03],
        fov: 60,
        note: 'Oblique on the ground-floor cell fronts from 1.6 m. Tests steel.cellFront — oxide-brown enamel over heavy orange rust bloom — the bar spacing and horizontal ties, the stencilled white cell numbers on the header band, and the lever/rack gang mechanism running the length of the run at hand height with a dog on every door.',
      },
      {
        name: 'a4-open-cell',
        position: [0.5, 1.52, 6.62],
        rotation: [Math.PI / 2 - 0.24, 0.05],
        fov: 72,
        note: 'Inside an open cell, looking at the back wall from just inside the door. Tests the paint stratigraphy (cream over mustard over blue-grey over sage over bare block), the stainless combination toilet/sink unit and the small steel wall desk and stool secured to the floor, at the 1–2 m range the headlamp is calibrated for.',
      },
      {
        name: 'a5-top-tier',
        position: [-1.2, 9.6, 12.0],
        rotation: [0.06, -0.2],
        fov: 66,
        note: 'Fourth tier, looking down the run and slightly up into the ceiling. Tests the catastrophic ceiling paint delamination — sheets curling down off the slab and littering the grating below — the exposed transverse beams and the dead recessed amber light boxes, and the heads of the upper window bays with the moon behind them.',
      },
    ],
  };

  private bleed?: PointLight;
  private dust?: ParticleSystem;
  private t = 0;

  async build(): Promise<void> {
    // Interior trim: the rig is calibrated for exteriors on limestone, and
    // cream institutional block is roughly 2.5x that albedo. Without this the
    // corridor stays fully readable with the headlamp off, which defeats the
    // entire point of a night scene lit by a lamp you have to manage.
    this.renderer.setLightingTrim({ fill: 0.68, environment: 0.72, fog: 1.15 });

    const ctx = this.kit();
    const p = profile();
    const rng = mulberry(18600229); // the year the East block opened

    // ---- Materials -------------------------------------------------------
    // Everything structural comes from the frozen library. Four scene-specific
    // materials are authored here because nothing in the library covers them
    // and none of them is a base surface: the translucent window glazing, the
    // stainless combination unit, the dead amber diffuser panel, and the open
    // grid of the bar grating (which needs an alpha channel the baked presets
    // do not have). That is the same call 1.1 makes for its cab glass.
    const floorMat = this.mats.get('concrete.floor');
    const slab = this.mats.get('concrete.slab');
    const stone = this.mats.get('limestone.wall');
    const wallPaint = this.mats.get('paint.corridor');
    const cellPaint = this.mats.get('paint.cell');
    const ceilPaint = this.mats.get('paint.ceiling');
    const cellSteel = this.mats.get('steel.cellFront');
    const catwalk = this.mats.get('steel.catwalk');
    const tile = this.mats.get('tile.corridor');
    const water = this.mats.get('water.standing');

    const grating = this.buildGratingMaterial();
    const glazing = this.buildGlazingMaterial();
    const stainless = this.buildStainlessMaterial();
    const diffuser = this.buildDiffuserMaterial();

    // ---- Batches ---------------------------------------------------------
    // One mesh per material. Everything below appends CPU-side geometry into
    // these and they are built once at the end — the same approach 3.1b uses
    // for its 1,750 hand-placed stones, for the same reason: this scene places
    // roughly 5,000 primitives and 5,000 Mesh objects would be 20,000 GL
    // buffers allocated and immediately discarded.
    const B = {
      stone: new GeoBatch(),
      paint: new GeoBatch(),
      block: new GeoBatch(),
      tile: new GeoBatch(),
      slab: new GeoBatch(),
      cellSteel: new GeoBatch(),
      catwalk: new GeoBatch(),
      winTrim: new GeoBatch(),
      grate: new GeoBatch(),
      grille: new GeoBatch(),
      glaze: new GeoBatch(),
      cellPaint: new GeoBatch(),
      stainless: new GeoBatch(),
      diffuser: new GeoBatch(),
      ceiling: new GeoBatch(),
      flakes: new GeoBatch(),
    };

    this.buildFloor(ctx, floorMat, water, rng);
    this.buildShellWall(B, rng);
    this.buildCellBlock(B, rng);
    this.buildCellInteriors(B, rng);
    this.buildGalleries(B, rng);
    this.buildStairs(B);
    this.buildCeiling(B, rng);
    this.buildDelamination(B, rng);
    this.buildDebris(B, rng);
    this.buildEnds(B);
    // Before the batches resolve: this appends the doorway furniture as well as
    // creating the light.
    this.buildFarDoor(B);

    // ---- Resolve the batches --------------------------------------------
    // Texel density is a decision per surface, not a knob. The library presets
    // already carry a scale multiplier (see Materials.ts); these override the
    // geometric density where the surface wants a different reading.
    // Texel density is a decision per surface, not a knob, and the first pass
    // got it wrong in the same direction everywhere: the library presets carry
    // their own scale multiplier (see Materials.ts), and at the global default
    // the CMU courses landed at roughly twice life size while the delamination
    // field ran so low-frequency that whole walls sat on the cream topcoat and
    // never showed a stratum. `paint` at 0.26 puts a block at 0.40 x 0.20 m,
    // which is a real concrete masonry unit, and drops the failure blobs to the
    // 0.2 m the reference shows.
    //
    // Every batch is emitted in five chunks along the run. One 58 m mesh per
    // material is always entirely inside the frustum, so a frame looking
    // sideways in a cell still paid for the far end of the building; chunking
    // takes the anchor that looks across the corridor from 380k triangles to
    // well under half that, which matters because the harness only gives TAA
    // 1.5 s to converge and a slow frame means it converges on the last anchor.
    const CH = 4;
    B.stone.finish(ctx, this.scene, 'cbStone', stone, { collide: false, cast: true }, CH);
    B.paint.finish(ctx, this.scene, 'cbWall', wallPaint, {
      collide: false,
      cast: true,
      uvDensity: 0.26,
    }, CH);
    B.block.finish(ctx, this.scene, 'cbBlock', cellPaint, {
      collide: false,
      cast: true,
      uvDensity: 0.26,
    }, CH);
    B.tile.finish(ctx, this.scene, 'cbTile', tile, {
      collide: false,
      cast: true,
      uvDensity: 0.23,
    }, CH);
    B.slab.finish(ctx, this.scene, 'cbSlab', slab, { collide: false, cast: true }, CH);
    B.cellSteel.finish(ctx, this.scene, 'cbCellFronts', cellSteel, {
      collide: false,
      cast: true,
    }, CH);
    B.catwalk.finish(ctx, this.scene, 'cbSteel', catwalk, { collide: false, cast: true }, CH);
    // Shadow-caster audit. The moon is the ONLY shadow-mapped light in the game
    // (the headlamp has shadowEnabled set but no generator), so anything the
    // moon can never reach has no business in four cascades of shadow map.
    // Window muntins sit inboard of the glass and behind the security bars,
    // which already throw the barred shadow; cell interiors are sealed boxes;
    // the ceiling is above every ray coming down through a window at 25 degrees.
    // Dropping them took roughly 2,600 boxes out of the shadow pass.
    B.winTrim.finish(ctx, this.scene, 'cbWinTrim', catwalk, { collide: false, cast: false }, CH);
    // The decks are real collision AND the surface tag the footstep engine
    // reads. This is the whole reason the tier sounds different from the floor.
    B.grate.finish(ctx, this.scene, 'cbGrating', grating, {
      collide: true,
      cast: true,
      surface: 'grating',
      uvDensity: 1 / 0.3,
    }, CH);
    B.grille.finish(ctx, this.scene, 'cbGrilles', grating, {
      collide: false,
      cast: false,
      uvDensity: 1 / 0.26,
    }, CH);
    // Never a shadow caster: the moon has to get through these to make the bars
    // on the floor, and they are the softest light source in the frame.
    B.glaze.finish(ctx, this.scene, 'cbGlazing', glazing, { collide: false, cast: false }, CH);
    B.cellPaint.finish(ctx, this.scene, 'cbCellPaint', cellPaint, {
      collide: false,
      cast: false,
      uvDensity: 0.62,
    }, CH);
    B.stainless.finish(ctx, this.scene, 'cbFixtures', stainless, {
      collide: false,
      cast: false,
      uvDensity: 1.2,
    });
    B.diffuser.finish(ctx, this.scene, 'cbDiffusers', diffuser, {
      collide: false,
      cast: false,
    });
    // High density on purpose. paint.ceiling bakes three blocks per tile, so at
    // the global default the joints landed as a 0.77 m grid of hard dark lines
    // and the ceiling read as suspended acoustic tile in a 1951 concrete
    // building. At 1.05 the same joints are a 0.25 m craze that reads as
    // texture, and the decay field mixes enough exposed substrate in to take
    // the ceiling off the cream topcoat it was sitting on.
    B.ceiling.finish(ctx, this.scene, 'cbCeiling', ceilPaint, {
      collide: false,
      cast: false,
      uvDensity: 1.8,
    }, CH);
    B.flakes.finish(ctx, this.scene, 'cbFlakes', ceilPaint, {
      collide: false,
      cast: false,
      uvDensity: 1.6,
    }, CH);

    // ---- Stencilled cell numbers ----------------------------------------
    this.buildCellNumbers(ctx);

    // ---- Collision -------------------------------------------------------
    // Invisible proxies rather than collision on the batched geometry: sweeping
    // an ellipsoid against a 40k-triangle mesh of cell bars every frame is a
    // poor trade when the player only ever touches a dozen planes.
    this.buildColliders(ctx);

    // ---- Atmosphere ------------------------------------------------------
    if (p.particleBudget > 200) this.buildDust(p.particleBudget);

    await this.scene.whenReadyAsync();
  }

  /* ----------------------------------------------------------------- floor -- */

  /**
   * The ground-floor gallery slab.
   *
   * `concrete.floor` is the preset with the polish pushed up, because the long
   * specular running away down the corridor is the single most recognisable
   * thing in the reference photography of this building. It is a traffic lane
   * that four hundred men walked twice a day for ninety years.
   */
  private buildFloor(
    ctx: ReturnType<GameScene['kit']>,
    floorMat: PBRMaterial,
    water: PBRMaterial,
    rng: () => number,
  ): void {
    const slabMesh = MeshBuilder.CreateBox(
      'cbFloor',
      { width: 4.4, height: 0.6, depth: L + 2.4 },
      this.scene,
    );
    slabMesh.position.set((WALL_X + 0.5) / 2, -0.3, L / 2);
    slabMesh.material = floorMat;
    ctx.register(slabMesh, { collide: true, cast: false, surface: 'concrete' });

    // Standing water is documented in the East Cell Block specifically (Drew
    // Pertl's photo tour). Shallow, still, and exactly where the roof above has
    // been letting go — which is under the window bays, not in the middle.
    const pools: [number, number, number, number][] = [
      [-2.6, 11.2, 2.1, 3.4],
      [-1.4, 30.6, 2.6, 4.2],
      [-2.9, 48.9, 1.8, 5.0],
    ];
    for (let i = 0; i < pools.length; i++) {
      const [px, pz, pw, pd] = pools[i];
      const pool = MeshBuilder.CreateGround(
        `cbPool${i}`,
        { width: pw, height: pd, subdivisions: 6 },
        this.scene,
      );
      pool.position.set(px + (rng() - 0.5) * 0.2, 0.012, pz);
      pool.material = water;
      pool.isPickable = false;
      pool.receiveShadows = false;
      pool.freezeWorldMatrix();
      this.meshes.push(pool);
    }
  }

  /* ------------------------------------------------------------ shell wall -- */

  /**
   * The outer shell wall with its twelve bays.
   *
   * The nomination gives the 1940s fenestration precisely: double-height
   * openings, limestone surrounds, a heavy limestone mullion splitting each
   * opening, steel sash faced with security bars. From inside, one bay reads as
   * a big soft-glowing translucent rectangle with a dark frame and a heavy stone
   * bar down the middle. Between the bays the piers carry the tall
   * perforated-metal ventilation grilles visible in survey photo 12.
   *
   * The interior face is painted (`paint.corridor`) rather than bare limestone —
   * this is a 1951 institutional interior, not a ruin of raw stone. The stone
   * only shows where the reveals cut through: jambs, sills, lintels, mullion.
   * That contrast is what gives the opening depth, and a flat texture of a
   * window reads as a sticker at any range.
   */
  private buildShellWall(B: Batches, rng: () => number): void {
    const back = WALL_X - WALL_T;
    const midX = (WALL_X + back) / 2;
    const top = CEIL_Y + 0.5;

    // Depth stack, room side outward: the reveal lining spans the full wall;
    // the muntin grid sits just inboard of the glass; the glass sits near the
    // outer face so you look down a real reveal at it; the security bars are
    // outboard of everything, which is both correct and what throws the barred
    // shadow across the floor.
    const xMuntin = back + 0.19;
    const xGlass = back + 0.13;
    const xBars = back + 0.05;

    for (let j = 0; j < BAYS; j++) {
      const zc = (j + 0.5) * BAY_PITCH;
      const o0 = zc - OPEN_W / 2;
      const o1 = zc + OPEN_W / 2;

      const pierZ0 = o1;
      const pierZ1 = zc + BAY_PITCH - OPEN_W / 2;
      const pierW = pierZ1 - pierZ0;
      const pierC = (pierZ0 + pierZ1) / 2;

      // Pier between this bay and the next, and a half-pier closing the near end.
      B.paint.box(midX, top / 2, pierC, WALL_T, top, pierW);
      if (j === 0) B.paint.box(midX, top / 2, (-1.0 + o0) / 2, WALL_T, top, o0 + 1.0);

      // Shallow pilaster on the corridor face, with a cap band at every tier.
      B.paint.box(WALL_X + 0.07, top / 2, pierC, 0.14, top, pierW - 0.5);
      for (let t = 1; t < TIERS; t++) {
        B.paint.box(WALL_X + 0.05, t * TIER_H - 0.16, pierC, 0.2, 0.2, pierW - 0.2);
      }

      // Glazed structural tile dado. The nomination calls the cell-house walls
      // "tiled"; in mid-century institutional practice that is a glazed tile
      // wainscot with paint above, and the horizontal break is most of what
      // stops a ten-metre wall reading as one flat panel.
      B.tile.box(WALL_X + 0.04, DADO_H / 2, pierC, 0.08, DADO_H, pierW);
      B.tile.box(WALL_X + 0.04, OPEN_LO_Y0 / 2, zc, 0.08, OPEN_LO_Y0, OPEN_W);
      B.slab.box(WALL_X + 0.02, DADO_H + 0.03, pierC, 0.14, 0.06, pierW);

      // Spandrels: below the lower opening, between the two, above the upper.
      B.paint.box(midX, OPEN_LO_Y0 / 2, zc, WALL_T, OPEN_LO_Y0, OPEN_W);
      B.paint.box(midX, (OPEN_LO_Y1 + OPEN_HI_Y0) / 2, zc, WALL_T, OPEN_HI_Y0 - OPEN_LO_Y1, OPEN_W);
      B.paint.box(midX, (OPEN_HI_Y1 + top) / 2, zc, WALL_T, top - OPEN_HI_Y1, OPEN_W);

      // The heavy limestone mullion, carried through both openings.
      B.stone.box(midX, (OPEN_LO_Y0 + OPEN_HI_Y1) / 2, zc, WALL_T + 0.06, OPEN_HI_Y1 - OPEN_LO_Y0, MULLION_W);

      for (const [y0, y1] of [
        [OPEN_LO_Y0, OPEN_LO_Y1],
        [OPEN_HI_Y0, OPEN_HI_Y1],
      ] as const) {
        const h = y1 - y0;
        for (const s of [-1, 1] as const) {
          B.stone.box(midX, (y0 + y1) / 2, zc + s * (OPEN_W / 2 - JAMB_W / 2), WALL_T + 0.04, h, JAMB_W);
        }
        // Sill, projecting into the room and sloped to shed water.
        B.stone.box(WALL_X - 0.16, y0 - 0.07, zc, 0.62, 0.17, OPEN_W + 0.5, 0, 0, 0.07);
        B.stone.box(midX - 0.04, y1 + 0.13, zc, WALL_T + 0.14, 0.26, OPEN_W + 0.5);

        const paneW = OPEN_W / 2 - JAMB_W - MULLION_W / 2;
        const paneH = h - 0.06;
        for (const s of [-1, 1] as const) {
          const pz = zc + s * (MULLION_W / 2 + paneW / 2);
          B.glaze.box(xGlass, (y0 + y1) / 2, pz, 0.04, paneH, paneW - 0.02);

          // Multi-light: ten courses of small sashes per pane, three across.
          // The nomination's "multi-light opaque glass with small single-light
          // inner sashes" is a lot of little panes, not four big ones.
          const rows = 10;
          for (let r = 1; r < rows; r++) {
            B.winTrim.box(xMuntin, y0 + 0.03 + (paneH * r) / rows, pz, 0.045, 0.028, paneW);
          }
          for (let cN = 1; cN < 3; cN++) {
            B.winTrim.box(xMuntin, (y0 + y1) / 2, pz - paneW / 2 + (paneW * cN) / 3, 0.045, paneH, 0.028);
          }
          // Frame around the pane.
          B.winTrim.box(xMuntin, y0 + 0.02, pz, 0.06, 0.07, paneW);
          B.winTrim.box(xMuntin, y1 - 0.02, pz, 0.06, 0.07, paneW);
          for (const e of [-1, 1] as const) {
            B.winTrim.box(xMuntin, (y0 + y1) / 2, pz + e * paneW / 2, 0.06, paneH, 0.07);
          }
          // The small single-light hopper sash, jammed open a few degrees.
          const sashY = y0 + h * (rng() > 0.5 ? 0.32 : 0.66);
          B.winTrim.box(xMuntin + 0.05, sashY, pz, 0.07, 0.5, paneW * 0.9, 0, 0, 0.05);
        }

        // Exterior security bars. These are the shadow caster that matters:
        // they chop the moonlight into the stripes on the floor.
        const nBars = 9;
        for (let b = 0; b < nBars; b++) {
          const bz = zc - OPEN_W / 2 + (OPEN_W * (b + 0.5)) / nBars;
          if (Math.abs(bz - zc) < MULLION_W / 2) continue;
          B.catwalk.box(xBars, (y0 + y1) / 2, bz, 0.05, h, 0.05);
        }
        for (let b = 0; b < 3; b++) {
          B.catwalk.box(xBars, y0 + (h * (b + 1)) / 4, zc, 0.05, 0.05, OPEN_W - 0.1);
        }
      }

      // Perforated-metal ventilation grille panels set into the piers, one per
      // external storey. Directly observed in NRHP survey photo 12.
      for (const [gy0, gy1] of [
        [1.35, 4.35],
        [6.1, 9.1],
      ] as const) {
        B.paint.box(WALL_X + 0.2, (gy0 + gy1) / 2, pierC, 0.26, gy1 - gy0, 0.86);
        B.grille.box(WALL_X + 0.03, (gy0 + gy1) / 2, pierC, 0.03, gy1 - gy0, 0.8);
        for (const s of [-1, 1] as const) {
          B.catwalk.box(WALL_X + 0.03, (gy0 + gy1) / 2, pierC + s * 0.44, 0.07, gy1 - gy0 + 0.08, 0.08);
          B.catwalk.box(WALL_X + 0.03, s > 0 ? gy1 + 0.04 : gy0 - 0.04, pierC, 0.07, 0.08, 0.88);
        }
      }

      // Dark furniture: a cast-iron rainwater pipe in the corner of every pier
      // and a conduit drop beside it. A ten-metre painted wall with nothing on
      // it reads as a corridor in a hospital, not a cell house — and this is
      // also most of what breaks up the pale block in the frame.
      B.catwalk.box(WALL_X + 0.13, top / 2, pierZ0 + 0.28, 0.2, top, 0.2);
      for (let k = 0; k < 5; k++) {
        B.catwalk.box(WALL_X + 0.19, 0.6 + k * 2.4, pierZ0 + 0.28, 0.3, 0.08, 0.3);
      }
      B.catwalk.box(WALL_X + 0.08, top / 2, pierZ1 - 0.22, 0.1, top, 0.1);
    }

    // A conduit run at deck level down the whole wall, and a dead lamp bracket
    // every other bay.
    for (let t = 0; t < TIERS; t++) {
      B.catwalk.box(WALL_X + 0.12, t * TIER_H + 2.28, L / 2, 0.1, 0.1, L);
    }

    // No outer skin is added behind all this on purpose: the piers, spandrels,
    // mullions and jambs each span the wall's full thickness and butt into each
    // other, so the assembly is genuinely solid and the openings are genuinely
    // the only way through. A backing slab would have sealed them and taken the
    // moon out of the scene entirely.
  }

  /* ------------------------------------------------------------ cell block -- */

  /**
   * The free-standing cell block: piers, header bands, doors, gang lock.
   *
   * Cell fronts are `steel.cellFront` — oxide-brown enamel with heavy orange
   * rust bloom pushing through and lifting it. Rust is not metal: the preset
   * takes metalness to nearly zero and roughness to nearly one wherever the
   * bloom wins, which is the single most common PBR error on a surface like
   * this and the one that is instantly visible.
   */
  private buildCellBlock(B: Batches, rng: () => number): void {
    // The mass of the block behind the cells. Never seen; its job is to stop
    // the moon leaking through a wall made of hundreds of separate pieces.
    B.block.box(4.6, CEIL_Y / 2, L / 2, 3.2, CEIL_Y + 1.2, L + 2.6);

    for (let t = 0; t < TIERS; t++) {
      const y0 = t * TIER_H;

      // Base curb along the foot of the run.
      B.slab.box(-0.14, y0 + 0.06, L / 2, 0.28, 0.12, L + 1.0);

      // The soffit band at the top of each tier.
      B.block.box(0.14, y0 + TIER_H - 0.12, L / 2, 0.28, 0.24, L + 1.0);

      // Continuous top track and bottom guide for the sliding doors.
      B.cellSteel.box(0.09, y0 + DOOR_H + 0.14, L / 2, 0.2, 0.14, L + 0.6);
      B.cellSteel.box(0.14, y0 + 0.035, L / 2, 0.24, 0.07, L + 0.6);

      // The rack bar. A jailer's operating lever drives this the length of the
      // run and it throws a locking dog on every door at once. Typology, not
      // Joliet-documented — see the class comment.
      B.cellSteel.box(-0.1, y0 + 1.16, L / 2, 0.09, 0.07, L + 0.4);

      for (let i = 0; i < CELL_N; i++) {
        const zc = CELL_Z0 + (i + 0.5) * CELL_PITCH;
        const open = t === 0 && OPEN_CELLS.includes(i);

        // Pier between doors: glazed structural tile, the one genuinely glossy
        // surface in the building.
        const pierW = CELL_PITCH - DOOR_W;
        B.block.box(0.16, y0 + TIER_H / 2, zc + CELL_PITCH / 2, 0.34, TIER_H - 0.1, pierW);
        // A shallow projecting nib on each pier so the run is not a flat plane.
        // Held clear of the curb below: two solids sharing a face is how you get
        // z-fighting smeared down the whole run by the temporal filter.
        B.block.box(-0.02, y0 + TIER_H / 2 + 0.02, zc + CELL_PITCH / 2, 0.05, TIER_H - 0.6, pierW - 0.16);
        // Glazed tile dado on the pier, matching the shell wall opposite.
        B.tile.box(-0.03, y0 + 0.5, zc + CELL_PITCH / 2, 0.06, 1.0, pierW - 0.16);

        // Header band over the door: the brown painted band the white cell
        // number is stencilled onto (research: photo 12, "338 339 340").
        B.cellSteel.box(0.08, y0 + DOOR_H + 0.36, zc, 0.14, 0.3, DOOR_W + 0.16);

        // Door frame.
        for (const s of [-1, 1] as const) {
          B.cellSteel.box(0.17, y0 + DOOR_H / 2, zc + s * (DOOR_W / 2 + 0.05), 0.16, DOOR_H, 0.1);
        }

        // The door leaf. Nine verticals and two horizontal ties — the 1857 spec
        // insisted on bars precisely so a cell would "admit nearly as much light
        // as when open", and the 1951 doors kept the logic.
        //
        // An open door is parked in the pocket behind the neighbouring pier,
        // which is where a sliding gang door actually goes — and, less
        // romantically, is the only place it can go without its bars occupying
        // the same cubic centimetres as the next door's.
        const leafZ = zc + (open ? DOOR_W * 0.74 : 0);
        const leafX = open ? 0.36 : 0.2;
        const nBars = 9;
        for (let b = 0; b < nBars; b++) {
          const bz = leafZ - DOOR_W / 2 + (DOOR_W * (b + 0.5)) / nBars;
          // Rust does not fall evenly: bars vary a few millimetres.
          const w = 0.032 + rng() * 0.008;
          B.cellSteel.box(leafX, y0 + DOOR_H / 2, bz, w, DOOR_H - 0.06, w);
        }
        for (const ty of [0.62, 1.44]) {
          B.cellSteel.box(leafX, y0 + ty, leafZ, 0.05, 0.055, DOOR_W - 0.02);
        }
        // Leaf head and foot rails.
        B.cellSteel.box(leafX, y0 + DOOR_H - 0.06, leafZ, 0.06, 0.1, DOOR_W);
        B.cellSteel.box(leafX, y0 + 0.09, leafZ, 0.06, 0.1, DOOR_W);

        // The locking dog: a short link from the rack bar up to the leaf head.
        B.cellSteel.box(-0.06, y0 + 1.28, leafZ - DOOR_W / 2 + 0.09, 0.05, 0.3, 0.05);
        // Rack bracket on the pier.
        B.cellSteel.box(0.02, y0 + 1.16, zc + CELL_PITCH / 2, 0.16, 0.12, 0.1);
      }

      // The operating lever stand at the head of the run.
      const lz = 0.7;
      B.catwalk.box(-0.42, y0 + 0.55, lz, 0.28, 1.1, 0.3);
      B.catwalk.box(-0.42, y0 + 1.16, lz, 0.34, 0.24, 0.36);
      // The lever itself, thrown over.
      B.catwalk.box(-0.55, y0 + 1.5, lz + 0.22, 0.06, 0.78, 0.06, 0.5, 0, 0.22);
      B.catwalk.box(-0.55, y0 + 1.86, lz + 0.4, 0.05, 0.05, 0.18);
      // The quadrant the lever runs in.
      B.catwalk.box(-0.42, y0 + 1.42, lz + 0.28, 0.05, 0.5, 0.5);
    }
  }

  /* ------------------------------------------------------- cell interiors -- */

  /**
   * Behind every door there is a real room, not a black rectangle.
   *
   * Most cells get a shallow shell — back wall, sides, floor, ceiling — so the
   * headlamp finds a surface at reading distance through the bars. Three
   * ground-floor cells are built out fully: the 1951 fitting-out is documented
   * as "tiled walls, concrete floors, a lavatory, a small table and stool
   * secured to the floor, and a barred metal door", plus spring beds and running
   * water. What survives today is the stainless combination toilet/sink unit and
   * the steel desk; the beds went for scrap.
   *
   * The walls carry `paint.cell` — the stratigraphy the owner recorded directly
   * off the building: cream topcoat curling away to mustard, then pale blue-grey,
   * then sage, then bare block. It is the single most valuable material spec in
   * the research and it is the reason a cell reads as a cell and not a cupboard.
   */
  private buildCellInteriors(B: Batches, rng: () => number): void {
    const HALF_W = 0.61;
    const PART_T = 0.14;
    const H = 2.2;
    const depthOf = (t: number, i: number): number =>
      t === 0 && OPEN_CELLS.includes(i) ? CELL_DEPTH : SHELL_DEPTH;

    for (let t = 0; t < TIERS; t++) {
      const y0 = t * TIER_H;

      // Partitions are built per BOUNDARY, not per cell, and each takes the
      // depth of the deeper of its two neighbours. Building them per cell put
      // two coplanar faces in the same place wherever a deep cell met a
      // shallow one, and coplanar faces are what the temporal filter smears
      // into arcs across the whole frame.
      for (let i = 0; i <= CELL_N; i++) {
        const z = CELL_Z0 + i * CELL_PITCH;
        const d = Math.max(
          i > 0 ? depthOf(t, i - 1) : SHELL_DEPTH,
          i < CELL_N ? depthOf(t, i) : SHELL_DEPTH,
        );
        B.cellPaint.box(0.3 + d / 2, y0 + H / 2, z, d, H, PART_T);
      }

      for (let i = 0; i < CELL_N; i++) {
        const zc = CELL_Z0 + (i + 0.5) * CELL_PITCH;
        const full = t === 0 && OPEN_CELLS.includes(i);
        const d = depthOf(t, i);
        const clear = CELL_PITCH - PART_T;

        // Back wall, floor, ceiling.
        B.cellPaint.box(0.3 + d + 0.11, y0 + H / 2, zc, 0.22, H, clear);
        B.slab.box(0.3 + d / 2, y0 + 0.05, zc, d, 0.1, clear);
        B.cellPaint.box(0.3 + d / 2, y0 + H + 0.08, zc, d, 0.16, clear);

        if (!full) continue;

        // ---- the fitting-out -------------------------------------------
        // Laid out for the frame you actually stand in: the combination unit on
        // the back wall to the -Z side, the desk on the +Z wall at mid-depth,
        // the bed brackets opposite. Iteration 1 put the desk directly under the
        // anchor camera, where it was invisible, and floated the stainless unit
        // in the middle of the back wall where it read as a white fridge.
        const bx = 0.3 + d - 0.11;
        const uz = zc - 0.26;

        // Stainless combination toilet/sink. A pedestal, a seat deck with a real
        // opening in it, a shroud carrying the basin, a spout and a push button.
        B.stainless.box(bx - 0.24, y0 + 0.21, uz, 0.44, 0.42, 0.44); // pedestal
        for (const e of [-1, 1] as const) {
          B.stainless.box(bx - 0.24, y0 + 0.44, uz + e * 0.19, 0.48, 0.06, 0.1); // seat rim
          B.stainless.box(bx - 0.24 + e * 0.19, y0 + 0.44, uz, 0.1, 0.06, 0.48);
        }
        B.stainless.template(
          CreateCylinderVertexData({ height: 0.1, diameter: 0.3, tessellation: 12 }),
          new Vector3(1, 1, 1),
          null,
          new Vector3(bx - 0.24, y0 + 0.32, uz),
        );
        B.stainless.box(bx - 0.1, y0 + 0.78, uz, 0.2, 0.72, 0.48); // shroud
        B.stainless.box(bx - 0.26, y0 + 1.1, uz, 0.42, 0.1, 0.46); // basin surround
        B.stainless.box(bx - 0.25, y0 + 1.13, uz, 0.3, 0.08, 0.34); // basin well
        B.stainless.box(bx - 0.12, y0 + 1.24, uz, 0.08, 0.16, 0.06); // spout
        B.stainless.box(bx - 0.13, y0 + 1.34, uz - 0.15, 0.1, 0.06, 0.06); // push button
        B.stainless.box(bx - 0.24, y0 + 1.5, uz, 0.04, 0.3, 0.24); // mirror plate

        // Small steel wall desk and stool, secured to the floor. On the +Z wall,
        // clear of the doorway, at the depth you see when you step in.
        const dz = zc + HALF_W - 0.28;
        const dxc = 0.3 + 1.45;
        B.catwalk.box(dxc, y0 + 0.74, dz, 0.78, 0.04, 0.5); // desk top
        B.catwalk.box(dxc, y0 + 0.66, dz + 0.22, 0.78, 0.14, 0.05); // apron
        B.catwalk.box(dxc - 0.33, y0 + 0.37, dz - 0.2, 0.05, 0.74, 0.05); // leg
        B.catwalk.box(dxc + 0.33, y0 + 0.37, dz - 0.2, 0.05, 0.74, 0.05); // leg
        B.catwalk.box(dxc, y0 + 0.44, dz - 0.42, 0.32, 0.04, 0.32); // stool seat
        B.catwalk.box(dxc, y0 + 0.22, dz - 0.42, 0.06, 0.44, 0.06); // stool stem
        B.catwalk.box(dxc, y0 + 0.02, dz - 0.42, 0.26, 0.04, 0.26); // floor plate

        // The bed frame brackets on the -Z wall, still bolted up. The spring
        // beds themselves went for scrap after 2002.
        for (const by of [0.44, 1.34]) {
          B.catwalk.box(0.3 + d / 2, y0 + by, zc - HALF_W + 0.03, d - 0.34, 0.05, 0.06);
          B.catwalk.box(0.3 + 0.2, y0 + by - 0.12, zc - HALF_W + 0.07, 0.07, 0.24, 0.1);
          B.catwalk.box(0.3 + d - 0.3, y0 + by - 0.12, zc - HALF_W + 0.07, 0.07, 0.24, 0.1);
        }

        // A shelf, and the conduit drop that once fed the cell light.
        B.catwalk.box(0.3 + 0.34, y0 + 1.66, zc - HALF_W + 0.18, 0.42, 0.03, 0.42);
        B.catwalk.box(bx - 0.03, y0 + 1.78, zc + 0.3, 0.05, 0.84, 0.05);
        B.catwalk.box(0.3 + d / 2, y0 + H - 0.06, zc + 0.3, d, 0.05, 0.05);

        // Paint hanging off the cell ceiling too — the failure is not confined
        // to the galleries.
        for (let k = 0; k < 7; k++) {
          B.ceiling.box(
            0.55 + rng() * (d - 0.5),
            y0 + H - 0.14 - rng() * 0.1,
            zc + (rng() - 0.5) * HALF_W * 1.5,
            0.09 + rng() * 0.14,
            0.006,
            0.09 + rng() * 0.14,
            (rng() - 0.5) * 1.4,
            rng() * Math.PI,
            (rng() - 0.5) * 1.4,
          );
        }

        // Fallen paint from the cell ceiling, on the cell floor.
        for (let k = 0; k < 14; k++) {
          B.flakes.box(
            0.4 + rng() * (d - 0.3),
            y0 + 0.11,
            zc + (rng() - 0.5) * HALF_W * 1.7,
            0.05 + rng() * 0.12,
            0.006,
            0.05 + rng() * 0.12,
            0,
            rng() * Math.PI,
            0,
          );
        }
      }
    }
  }

  /* --------------------------------------------------------- the galleries -- */

  /**
   * Three upper tiers of gallery: grating deck, solid curb, cantilever
   * brackets, stringer, railing.
   *
   * The floors are **steel bar grating**, not concrete — corrected from the
   * survey photography against the nomination's own blanket text. It is built
   * as an alpha-tested open grid rather than a textured plank, so you genuinely
   * see the tier below through your feet and the moon genuinely dapples through
   * it onto the floor. That, and the sound it makes, is what the whole scene is
   * organised around.
   */
  private buildGalleries(B: Batches, rng: () => number): void {
    for (let t = 1; t < TIERS; t++) {
      const y = t * TIER_H;

      // The grating deck. Modelled as a thin slab rather than a plane so it has
      // a readable edge and so collide-and-slide has something with thickness
      // to land on.
      B.grate.box(
        (WELL_X + CURB_X) / 2,
        y - 0.03,
        L / 2,
        Math.abs(CURB_X - WELL_X),
        0.06,
        L + 0.4,
      );

      // The narrow solid curb strip along the cell fronts (research: photo 12).
      B.slab.box((CURB_X + FRONT_X) / 2, y - 0.04, L / 2, Math.abs(CURB_X), 0.08, L + 0.4);

      // Edge stringer channel, and a nosing angle at the well edge.
      B.catwalk.box(WELL_X + 0.06, y - 0.16, L / 2, 0.12, 0.26, L + 0.4);
      B.catwalk.box(WELL_X + 0.02, y + 0.01, L / 2, 0.06, 0.04, L + 0.4);

      // Cantilever brackets back to the cell block, every ~2.4 m.
      const nBr = Math.floor(L / 2.4);
      for (let b = 0; b <= nBr; b++) {
        const bz = 0.4 + (b * (L - 0.8)) / nBr;
        B.catwalk.box(
          (WELL_X + FRONT_X) / 2,
          y - 0.2,
          bz,
          Math.abs(WELL_X),
          0.13,
          0.09,
        );
        // The knee under each bracket. Tucked against the cell block and kept
        // ABOVE 2.3 m: iteration 1 hung it at 2.15 in the middle of the
        // walkway, where it read as a rusty beam across every gallery frame and
        // filled a third of the wide shot when the camera stood under one.
        B.catwalk.box(-0.52, y - 0.4, bz, 0.62, 0.08, 0.07, 0, 0, 0.72);
      }

      // The railing. Posts, top rail, mid rail, toe plate — and gaps where a
      // stair lands, because a railing across a stair head is a level-design
      // tell of the first order.
      const gaps = STAIRS.filter((s) => s.from + 1 === t).map(
        (s) => [s.z + STAIR_TREADS * STAIR_GOING - 0.3, s.z + STAIR_TREADS * STAIR_GOING + 1.7] as [number, number],
      );
      const inGap = (z: number): boolean => gaps.some(([a, b]) => z > a && z < b);

      const postPitch = 1.6;
      const nPosts = Math.floor(L / postPitch);
      for (let q = 0; q <= nPosts; q++) {
        const pz = 0.3 + q * postPitch;
        if (pz > L - 0.2 || inGap(pz)) continue;
        B.catwalk.box(WELL_X + 0.04, y + 0.55, pz, 0.05, 1.1, 0.05);
      }
      // Rails, laid in runs between the gaps.
      const bounds = [0.2, ...gaps.flat(), L - 0.2].sort((a, b) => a - b);
      for (let s = 0; s < bounds.length - 1; s += 2) {
        const z0 = bounds[s];
        const z1 = bounds[s + 1];
        if (z1 - z0 < 0.4) continue;
        for (const ry of [1.08, 0.56]) {
          B.catwalk.box(WELL_X + 0.04, y + ry, (z0 + z1) / 2, 0.055, 0.055, z1 - z0);
        }
        B.catwalk.box(WELL_X + 0.05, y + 0.09, (z0 + z1) / 2, 0.03, 0.14, z1 - z0);
      }

      // Fallen paint on the grating — a carpet of it, per the survey photo.
      for (let k = 0; k < 90; k++) {
        B.flakes.box(
          WELL_X + 0.12 + rng() * (Math.abs(CURB_X - WELL_X) - 0.24),
          y + 0.012,
          0.6 + rng() * (L - 1.2),
          0.05 + rng() * 0.16,
          0.006,
          0.05 + rng() * 0.16,
          (rng() - 0.5) * 0.2,
          rng() * Math.PI,
          (rng() - 0.5) * 0.2,
        );
      }
    }
  }

  /* -------------------------------------------------------------- stairs --- */

  /**
   * Three steel flights, staggered down the run so they never stack.
   *
   * They live in the light well against the window wall, which means every one
   * of them is backlit by the moon coming through a bay — the dark foreground
   * element the frame needs to have depth.
   */
  private buildStairs(B: Batches): void {
    const x0 = WALL_X + 0.08;
    const xc = x0 + STAIR_W / 2;

    for (const s of STAIRS) {
      const yBase = s.from * TIER_H;
      const rise = TIER_H / STAIR_TREADS;
      const runLen = STAIR_TREADS * STAIR_GOING;
      const angle = Math.atan2(TIER_H, runLen);

      // Treads.
      for (let i = 0; i < STAIR_TREADS; i++) {
        const tz = s.z + (i + 0.5) * STAIR_GOING;
        const ty = yBase + (i + 1) * rise;
        B.grate.box(xc, ty - 0.02, tz, STAIR_W, 0.04, STAIR_GOING + 0.03);
        // Riser plate, open at the back the way real stair grating is.
        B.catwalk.box(xc, ty - rise / 2, tz + STAIR_GOING / 2 - 0.01, STAIR_W, rise * 0.55, 0.02);
      }

      // Stringers.
      for (const side of [-1, 1] as const) {
        B.catwalk.box(
          xc + side * (STAIR_W / 2 + 0.03),
          yBase + TIER_H / 2 - 0.08,
          s.z + runLen / 2,
          0.06,
          0.3,
          Math.hypot(runLen, TIER_H) + 0.2,
          -angle,
          0,
          0,
        );
        // Handrail and its posts.
        B.catwalk.box(
          xc + side * (STAIR_W / 2 + 0.03),
          yBase + TIER_H / 2 + 0.86,
          s.z + runLen / 2,
          0.05,
          0.05,
          Math.hypot(runLen, TIER_H) + 0.1,
          -angle,
          0,
          0,
        );
        for (let q = 0; q < 4; q++) {
          const f = (q + 0.5) / 4;
          B.catwalk.box(
            xc + side * (STAIR_W / 2 + 0.03),
            yBase + f * TIER_H + 0.48,
            s.z + f * runLen,
            0.045,
            0.95,
            0.045,
          );
        }
      }

      // Landing at the top, lapping the deck edge so there is no gap to fall in.
      // It stops 1 cm short of the deck rather than lapping it: two grating
      // slabs sharing a plane would z-fight down the whole landing.
      const lz0 = s.z + runLen;
      const landW = Math.abs(WALL_X - WELL_X) - 0.02;
      const landX = (WALL_X + WELL_X) / 2 - 0.01;
      B.grate.box(landX, yBase + TIER_H - 0.03, lz0 + 0.7, landW, 0.06, 1.4);
      B.catwalk.box(landX, yBase + TIER_H - 0.16, lz0 + 0.7, landW, 0.2, 0.12);
      // Landing guard on the far side.
      B.catwalk.box(WELL_X + 0.04, yBase + TIER_H + 0.55, lz0 + 1.36, 0.05, 1.1, 0.05);
      for (const ry of [1.08, 0.56]) {
        B.catwalk.box(landX, yBase + TIER_H + ry, lz0 + 1.37, landW, 0.055, 0.055);
      }
    }
  }

  /* ------------------------------------------------------------- ceiling --- */

  /**
   * Painted concrete, flat, with exposed transverse beams and recessed box
   * fixtures — exactly what survey photo 12 shows. The fixtures still hold their
   * warm amber diffuser panels; nothing has fed them since 2002.
   */
  private buildCeiling(B: Batches, rng: () => number): void {
    B.ceiling.box((WALL_X + 0.4) / 2, CEIL_Y + 0.2, L / 2, Math.abs(WALL_X) + 0.4, 0.4, L + 2.2);

    for (let j = 0; j < BAYS; j++) {
      const zc = (j + 0.5) * BAY_PITCH;
      // Transverse beam, aligned with the bay.
      B.ceiling.box((WALL_X + 0.3) / 2, CEIL_Y - 0.2, zc, Math.abs(WALL_X) + 0.3, 0.42, 0.36);

      // Recessed light box between beams: a dark reveal with an amber panel.
      const fz = zc + BAY_PITCH / 2;
      B.ceiling.box(-1.5, CEIL_Y + 0.02, fz, 0.66, 0.2, 1.3);
      B.diffuser.box(-1.5, CEIL_Y - 0.055, fz, 0.5, 0.03, 1.14);
      B.catwalk.box(-1.5, CEIL_Y - 0.05, fz, 0.6, 0.05, 0.06);
      for (const s of [-1, 1] as const) {
        B.catwalk.box(-1.5, CEIL_Y - 0.05, fz + s * 0.6, 0.62, 0.06, 0.06);
        B.catwalk.box(-1.5 + s * 0.28, CEIL_Y - 0.05, fz, 0.05, 0.06, 1.2);
      }

      // Conduit and a length of failed duct running the length between beams.
      if (j % 2 === 0) {
        B.catwalk.box(-3.2, CEIL_Y - 0.34, zc + BAY_PITCH / 2, 0.07, 0.07, BAY_PITCH - 0.5);
      }
      // A hanging fragment of the ceiling's own substrate.
      if (rng() < 0.5) {
        B.ceiling.box(
          -1.0 - rng() * 2.2,
          CEIL_Y - 0.5,
          zc + (rng() - 0.5) * 2.4,
          0.5 + rng() * 0.5,
          0.06,
          0.5 + rng() * 0.5,
          (rng() - 0.5) * 0.5,
          rng() * Math.PI,
          (rng() - 0.5) * 0.5,
        );
      }
    }
  }

  /* -------------------------------------------------------- delamination --- */

  /**
   * The signature effect of this building's decay: the ceiling paint has failed
   * as large curling sheets that hang down and litter the walkway below. Survey
   * photo 12 shows dozens of them 6–18 in. across, and a carpet of fallen flakes
   * on the grating. Tour writers describe paint "hanging from ceilings like
   * stalactites."
   *
   * A sheet is built as three strips with increasing tilt, so it curls away from
   * the substrate rather than hanging as one flat flag. That progression is most
   * of what sells it.
   */
  private buildDelamination(B: Batches, rng: () => number): void {
    // The strip's own +X axis is the direction it runs, so the step from one
    // segment to the next is that axis transformed by the same matrix the
    // geometry gets. Deriving the offset by hand from the Euler angles is how
    // you end up with a sheet whose three strips do not touch — invisible in
    // the source, unmissable in the capture.
    const runDir = new Vector3(1, 0, 0);
    const sheet = (x: number, y: number, z: number, size: number, yaw: number): void => {
      const p = new Vector3(x, y, z);
      // `tilt` is the angle off vertical: 0 hangs straight down, and it grows
      // segment by segment so the sheet curls back on itself the way failed
      // paint actually does rather than hanging as a flat flag.
      let tilt = 0.14 + rng() * 0.26;
      for (let s = 0; s < 3; s++) {
        const len = size * (0.55 - s * 0.12);
        const rot = Matrix.RotationYawPitchRoll(yaw, 0, tilt - Math.PI / 2);
        const axis = Vector3.TransformNormal(runDir, rot);
        const mid = p.add(axis.scale(len / 2));
        B.ceiling.template(
          BOX,
          new Vector3(len * 0.92, 0.007, size * (0.85 - s * 0.15)),
          rot,
          mid,
        );
        p.addInPlace(axis.scale(len));
        tilt = Math.min(1.5, tilt + 0.45 + rng() * 0.35);
      }
    };

    // Off the main ceiling. Heaviest where the roof above has been letting go —
    // over the light well, not over the cell fronts.
    for (let i = 0; i < 105; i++) {
      sheet(
        WALL_X + 0.5 + rng() * 3.2,
        CEIL_Y - 0.42 - rng() * 0.05,
        0.8 + rng() * (L - 1.6),
        0.16 + rng() * 0.3,
        rng() * Math.PI * 2,
      );
    }

    // Off the soffit of every gallery deck, which is what the player standing on
    // the ground floor actually looks up into.
    for (let t = 1; t < TIERS; t++) {
      const y = t * TIER_H - 0.3;
      for (let i = 0; i < 34; i++) {
        sheet(
          WELL_X + 0.2 + rng() * 1.9,
          y,
          0.8 + rng() * (L - 1.6),
          0.13 + rng() * 0.24,
          rng() * Math.PI * 2,
        );
      }
      // And off the tier soffit above the cell doors.
      for (let i = 0; i < 16; i++) {
        sheet(
          -0.35 - rng() * 0.55,
          t * TIER_H - 0.28,
          1.2 + rng() * (L - 2.4),
          0.12 + rng() * 0.2,
          rng() * Math.PI * 2,
        );
      }
    }
  }

  /* -------------------------------------------------------------- debris --- */

  private buildDebris(B: Batches, rng: () => number): void {
    // Fallen paint on the ground floor, thickest under the well.
    for (let i = 0; i < 260; i++) {
      const nearWell = rng() < 0.66;
      B.flakes.box(
        nearWell ? WALL_X + 0.3 + rng() * 2.0 : WELL_X + rng() * 2.3,
        0.011,
        0.6 + rng() * (L - 1.2),
        0.05 + rng() * 0.2,
        0.006,
        0.05 + rng() * 0.2,
        (rng() - 0.5) * 0.14,
        rng() * Math.PI,
        (rng() - 0.5) * 0.14,
      );
    }

    // Concrete spall, a fallen light diffuser, a length of conduit. Sparse: this
    // is a building failing slowly, not a set-dressed ruin.
    for (let i = 0; i < 42; i++) {
      const s = 0.1 + rng() * 0.26;
      B.slab.box(
        WALL_X + 0.4 + rng() * 3.1,
        0.03 + s * 0.2,
        1.0 + rng() * (L - 2.0),
        s * (0.8 + rng() * 0.8),
        s * (0.3 + rng() * 0.4),
        s * (0.8 + rng() * 0.8),
        (rng() - 0.5) * 0.5,
        rng() * Math.PI,
        (rng() - 0.5) * 0.5,
      );
    }
    for (let i = 0; i < 5; i++) {
      B.diffuser.box(
        WALL_X + 0.7 + rng() * 2.6,
        0.02,
        3 + rng() * (L - 6),
        0.5,
        0.02,
        1.1,
        (rng() - 0.5) * 0.1,
        rng() * Math.PI,
        (rng() - 0.5) * 0.1,
      );
    }
    for (let i = 0; i < 7; i++) {
      B.catwalk.box(
        WALL_X + 0.5 + rng() * 2.8,
        0.04,
        2 + rng() * (L - 4),
        0.05,
        0.05,
        0.7 + rng() * 1.6,
        0,
        rng() * Math.PI,
        0,
      );
    }
  }

  /* ---------------------------------------------------------------- ends --- */

  private buildEnds(B: Batches): void {
    const top = CEIL_Y + 0.5;
    // Near end, behind the spawn.
    B.block.box((WALL_X - 0.5 + 3.2) / 2, top / 2, -0.7, 8.7, top, 0.8);
    // Far end, with the doorway out to the rotunda.
    const doorZ = L + 0.4;
    const dx = -1.65;
    const dw = 1.35;
    const dh = 2.45;
    B.block.box(dx - dw / 2 - 1.4, top / 2, doorZ, 2.8, top, 0.8);
    B.block.box(dx + dw / 2 + 1.9, top / 2, doorZ, 3.8, top, 0.8);
    B.block.box(dx, (dh + top) / 2, doorZ, dw, top - dh, 0.8);
    // Jamb linings and a heavy lintel, so the opening has depth.
    for (const s of [-1, 1] as const) {
      B.slab.box(dx + s * (dw / 2 + 0.09), dh / 2, doorZ - 0.02, 0.18, dh, 0.86);
    }
    B.slab.box(dx, dh + 0.13, doorZ - 0.02, dw + 0.44, 0.26, 0.86);
  }

  /* ------------------------------------------------------- cell numbers ---- */

  /**
   * Stencilled cell numbers, ~4 in. tall, white on the brown header band —
   * directly observed in NRHP survey photo 12 ("338", "339", "340" in sequence
   * along the West Block's second-floor south tier). Numbered here by tier:
   * 101–136, 201–236, 301–336, 401–436.
   *
   * Rendered into one atlas and placed as alpha-tested quads, so 144 numbers
   * cost one draw call and one texture.
   */
  private buildCellNumbers(ctx: ReturnType<GameScene['kit']>): void {
    const tex = buildNumberAtlas(this.scene);
    const mat = new PBRMaterial('cbNumbers', this.scene);
    mat.albedoTexture = tex;
    mat.useAlphaFromAlbedoTexture = true;
    mat.transparencyMode = PBRMaterial.PBRMATERIAL_ALPHATEST;
    mat.alphaCutOff = 0.3;
    mat.metallic = 0;
    mat.roughness = 0.78;
    mat.ambientColor = new Color3(1, 1, 1);
    mat.environmentIntensity = 0.5;
    mat.enableSpecularAntiAliasing = true;
    mat.maxSimultaneousLights = profile().maxLights;
    mat.backFaceCulling = true;
    // Nudge toward the camera so the 8 mm physical offset never z-fights the
    // header band it is stencilled onto.
    mat.zOffset = -2;
    mat.freeze();

    const batch = new GeoBatch();
    let cell = 0;
    for (let t = 0; t < TIERS; t++) {
      const y0 = t * TIER_H;
      for (let i = 0; i < CELL_N; i++) {
        const zc = CELL_Z0 + (i + 0.5) * CELL_PITCH;
        const vd = CreatePlaneVertexData({ width: 0.3, height: 0.3 });
        remapUV(vd, cell);
        batch.template(
          vd,
          new Vector3(1, 1, 1),
          Matrix.RotationYawPitchRoll(Math.PI / 2, 0, 0),
          new Vector3(0.0, y0 + DOOR_H + 0.36, zc),
        );
        cell++;
      }
    }
    batch.finish(ctx, this.scene, 'cbCellNumbers', mat, {
      collide: false,
      cast: false,
      keepUV: true,
    });
  }

  /* ----------------------------------------------------------- collision --- */

  private buildColliders(ctx: ReturnType<GameScene['kit']>): void {
    const invisible = (
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

    // Outer shell wall and the cell-block face, tier by tier so the open
    // ground-floor cells are genuinely enterable and the tiers above them are
    // not.
    invisible('cbWallCol', WALL_X - 0.35, CEIL_Y / 2, L / 2, 0.7, CEIL_Y + 1, L + 2);
    for (let t = 0; t < TIERS; t++) {
      const y0 = t * TIER_H;
      const open = t === 0 ? OPEN_CELLS : [];
      const cuts: [number, number][] = open
        .map((i) => {
          const zc = CELL_Z0 + (i + 0.5) * CELL_PITCH;
          return [zc - DOOR_W / 2, zc + DOOR_W / 2] as [number, number];
        })
        .sort((a, b) => a[0] - b[0]);

      let z = -0.4;
      for (const [c0, c1] of [...cuts, [L + 0.4, L + 0.4] as [number, number]]) {
        if (c0 - z > 0.05) {
          invisible(`cbFrontCol${t}_${z.toFixed(1)}`, 0.18, y0 + TIER_H / 2, (z + c0) / 2, 0.36, TIER_H, c0 - z);
        }
        z = Math.max(z, c1);
      }
      // Side and back walls of each open cell.
      for (const i of open) {
        const zc = CELL_Z0 + (i + 0.5) * CELL_PITCH;
        invisible(`cbCellBack${i}`, 0.3 + CELL_DEPTH + 0.1, y0 + 1.1, zc, 0.3, 2.2, 1.8);
        for (const s of [-1, 1] as const) {
          invisible(`cbCellSide${i}_${s}`, 0.3 + CELL_DEPTH / 2, y0 + 1.1, zc + s * 0.79, CELL_DEPTH, 2.2, 0.24);
        }
      }
    }

    // Gallery railings.
    for (let t = 1; t < TIERS; t++) {
      const y = t * TIER_H;
      const gaps = STAIRS.filter((s) => s.from + 1 === t).map(
        (s) =>
          [
            s.z + STAIR_TREADS * STAIR_GOING - 0.3,
            s.z + STAIR_TREADS * STAIR_GOING + 1.7,
          ] as [number, number],
      );
      const bounds = [0.2, ...gaps.flat(), L - 0.2].sort((a, b) => a - b);
      for (let s = 0; s < bounds.length - 1; s += 2) {
        const z0 = bounds[s];
        const z1 = bounds[s + 1];
        if (z1 - z0 < 0.4) continue;
        invisible(`cbRail${t}_${s}`, WELL_X + 0.02, y + 0.6, (z0 + z1) / 2, 0.16, 1.2, z1 - z0);
      }
    }

    // Stair flights, as a smooth ramp each — collide-and-slide plus the step-up
    // probe handles a ramp far more predictably than fourteen tread boxes.
    for (const s of STAIRS) {
      const runLen = STAIR_TREADS * STAIR_GOING;
      const angle = Math.atan2(TIER_H, runLen);
      const ramp = MeshBuilder.CreateBox(
        `cbStairRamp${s.from}`,
        { width: STAIR_W, height: 0.3, depth: Math.hypot(runLen, TIER_H) },
        this.scene,
      );
      ramp.position.set(WALL_X + 0.08 + STAIR_W / 2, s.from * TIER_H + TIER_H / 2 - 0.13, s.z + runLen / 2);
      ramp.rotation.x = -angle;
      ramp.isVisible = false;
      ramp.material = null;
      ctx.register(ramp, { collide: true, cast: false, surface: 'grating' });
    }

    // Ceiling, so nothing can be climbed out through the roof.
    invisible('cbCeilCol', (WALL_X + 0.3) / 2, CEIL_Y + 0.4, L / 2, 5, 0.5, L + 2);
  }

  /* -------------------------------------------------------------- light ---- */

  /**
   * One practical, and it is a long way off: sodium spill through the doorway at
   * the far end of the run, from the yard lamp outside the block.
   *
   * The art bible asks for a warm/cool split wherever a practical exists, and in
   * a corridor this long that warm patch at the vanishing point is also the
   * navigation cue — it is the only thing in the frame that says *this way*.
   * Everything else here is moon and headlamp; a room this dark is meant to be
   * dark, and adding fill to compensate would throw away the whole point of the
   * window bays.
   */
  private buildFarDoor(B: Batches): void {
    const doorZ = L + 0.4;
    const dx = -1.65;

    // The lit surface beyond the opening. Dim, warm, and NOT bright enough to
    // bloom — nothing in this game glows except the sodium lens and the headlamp
    // hotspot.
    const beyond = MeshBuilder.CreateBox(
      'cbBeyond',
      { width: 1.5, height: 2.6, depth: 0.06 },
      this.scene,
    );
    beyond.position.set(dx, 1.24, doorZ + 0.56);
    const bm = new StandardMaterial('cbBeyondMat', this.scene);
    bm.diffuseColor = new Color3(0.02, 0.018, 0.014);
    bm.specularColor = Color3.Black();
    bm.emissiveColor = srgb('#3a2409');
    bm.disableLighting = true;
    beyond.material = bm;
    beyond.isPickable = false;
    beyond.receiveShadows = false;
    beyond.freezeWorldMatrix();
    this.meshes.push(beyond);

    this.bleed = new PointLight('cbSodiumBleed', new Vector3(dx, 1.7, doorZ + 0.1), this.scene);
    this.bleed.diffuse = C.sodiumVapour;
    this.bleed.specular = C.sodiumVapour.scale(0.4);
    // Physical falloff: this is not a 0–1 dial. Checked against 1.1's sodium
    // lamp at 1400 and the headlamp at 620, not against the moon at 4.6.
    this.bleed.intensity = 150;
    this.bleed.range = 16;
    this.bleed.shadowEnabled = false;

    // A dead conduit box and a fire-alarm bell beside the doorway — the small
    // institutional furniture that says a person worked here.
    B.catwalk.box(dx + 1.05, 2.1, doorZ - 0.5, 0.2, 0.26, 0.14);
    B.catwalk.box(dx + 1.05, 1.6, doorZ - 0.5, 0.06, 0.74, 0.06);
  }

  /**
   * There are no volumetric shafts here, and the reason is worth recording.
   *
   * The first pass swept a low-alpha additive prism out of every window opening
   * along the moon vector, the way 3.1b draws the shaft down its break-in. In
   * that room it works because the shaft is perpendicular to the view. Here it
   * is not: the moon runs at roughly 37 degrees off the corridor axis in plan,
   * so every prism sits nearly parallel to the way the player is looking, every
   * side quad is seen almost edge-on, and twenty-four of them stacked up into a
   * radial smear that veiled the entire frame from the vanishing point outward.
   * The capture is in artifacts/shots/3.1-cellblocks/iter-01.
   *
   * A shaft you look ALONG is not a shaft, it is a fog volume, and this renderer
   * has no volumetric integrator wired (the quality tiers carry a `volumetrics`
   * flag that nothing reads yet). So the moonlight in this scene is carried by
   * what actually carries it in the reference photography: the shadow-mapped
   * bars the openings throw across the floor and up the cell fronts, the glow of
   * the glazing itself, and dust in the well. That is honest, and it is the
   * frame the scene was composed for.
   *
   * If core ever grows a volumetric pass, this is the scene that wants it most.
   */

  /**
   * Dust in the well.
   *
   * A cell house that has been open to the weather for twenty years is full of
   * it, and with no volumetric pass in the renderer this is the only thing
   * standing between the moonlit half of the frame and a hard-edged patch of
   * light on a floor. Confined to the well and the band of floor the lower
   * openings actually reach, because particles are only worth their cost where
   * a light can catch them.
   */
  private buildDust(budget: number): void {
    const ps = new ParticleSystem('cbDust', Math.min(budget, 1200), this.scene);
    ps.particleTexture = makeDotTexture(this.scene);
    ps.emitter = new Vector3(WALL_X + 1.6, CEIL_Y / 2, L / 2);
    ps.minEmitBox = new Vector3(-1.5, -CEIL_Y / 2 + 0.4, -L / 2 + 1);
    ps.maxEmitBox = new Vector3(2.4, CEIL_Y / 2 - 0.4, L / 2 - 1);
    ps.color1 = new Color4(0.72, 0.81, 0.97, 0.4);
    ps.color2 = new Color4(0.56, 0.66, 0.88, 0.16);
    ps.colorDead = new Color4(0.56, 0.66, 0.88, 0);
    ps.minSize = 0.006;
    ps.maxSize = 0.024;
    ps.minLifeTime = 9;
    ps.maxLifeTime = 20;
    ps.emitRate = 180;
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
   * Steel bar grating, as an alpha-tested open grid.
   *
   * Real grating is ~80% open, which would average down to nothing in the
   * mip chain and make the far end of a 58 m gallery vanish. The bars here are
   * thickened to ~40% coverage and the alpha cutoff dropped to 0.22 so distant
   * mips stay solid rather than fizzing — the far tiers read as a dark deck,
   * which is what they look like anyway, and the near grating stays crisp and
   * genuinely see-through.
   *
   * Colour is sampled off NRHP photo 12: a dark warm grey body with much
   * brighter worn top edges where boots have polished the bearing bars.
   */
  private buildGratingMaterial(): PBRMaterial {
    const tex = makeGratingTexture(this.scene);
    const m = new PBRMaterial('cbGratingMat', this.scene);
    m.albedoTexture = tex;
    m.useAlphaFromAlbedoTexture = true;
    m.transparencyMode = PBRMaterial.PBRMATERIAL_ALPHATEST;
    m.alphaCutOff = 0.22;
    m.metallic = 0.4;
    m.roughness = 0.62;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.55;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    // Back faces OFF. Every mesh that uses this material is a closed slab, so
    // the underside of a walkway is its own face and nothing is lost — but a
    // double-sided alpha-tested surface filling the screen at a grazing angle
    // doubles the discard work with no early-Z to save it, and that is most of
    // why iteration 1 could not hold a frame rate looking down a tier.
    m.backFaceCulling = true;
    m.freeze();
    return m;
  }

  /**
   * The window glazing: multi-light opaque glass, not clear glass.
   *
   * From inside at night this is a big soft-glowing translucent rectangle — the
   * moon is behind it and the glass is diffusing everything that gets through.
   * Modelled as an opaque emissive panel rather than an alpha-blended one: it
   * gives the same read with no sorting risk, and because it is registered as a
   * non-caster the moon still passes cleanly through the opening to make the
   * bars on the floor.
   */
  private buildGlazingMaterial(): PBRMaterial {
    const m = new PBRMaterial('cbGlazing', this.scene);
    m.albedoColor = new Color3(0.03, 0.035, 0.04);
    m.metallic = 0;
    m.roughness = 0.42;
    // Below the 0.86 bloom threshold on purpose. If this blooms, it is wrong.
    m.emissiveColor = C.moonlight.scale(0.8);
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.4;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /** The stainless combination toilet/sink unit. Brushed, not mirror. */
  private buildStainlessMaterial(): PBRMaterial {
    const m = new PBRMaterial('cbStainless', this.scene);
    // Rougher and darker than "stainless" sounds. At 0.38 roughness the
    // specular lobe was tight enough that a headlamp two metres away clipped the
    // whole unit to a white blob; a real fixture in a dark cell reads as a grey
    // body with one soft sheen down its front.
    m.albedoColor = srgb('#7f8486');
    m.metallic = 0.88;
    m.roughness = 0.9;
    m.ambientColor = new Color3(1, 1, 1);
    m.environmentIntensity = 0.4;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /** The amber diffuser panels in the dead ceiling fixtures. */
  private buildDiffuserMaterial(): PBRMaterial {
    const m = new PBRMaterial('cbDiffuser', this.scene);
    m.albedoColor = srgb('#b98c3c');
    m.metallic = 0;
    m.roughness = 0.68;
    m.ambientColor = new Color3(1, 1, 1);
    // Kept low deliberately: the IBL is a night golf course and at 0.6 its green
    // grass bounce turned every amber diffuser lime.
    m.environmentIntensity = 0.2;
    m.enableSpecularAntiAliasing = true;
    m.maxSimultaneousLights = profile().maxLights;
    m.freeze();
    return m;
  }

  /* ------------------------------------------------------------- runtime --- */

  override update(dt: number, _player?: unknown): void {
    this.t += dt;
    // The far sodium is on a failing ballast a hundred metres away and one wall
    // out. Two detuned sines and a rare dropout reads as electrical rather than
    // as an animation curve.
    if (this.bleed) {
      const slow = Math.sin(this.t * 0.51) * 0.5 + Math.sin(this.t * 1.37) * 0.2;
      const dropout = Math.sin(this.t * 0.11) > 0.988 ? 0.4 : 1;
      this.bleed.intensity = (150 + slow * 16) * dropout;
    }
  }

  override dispose(): void {
    this.dust?.dispose();
    this.bleed?.dispose();
    super.dispose();
  }
}

/* ========================================================================== */
/*  Geometry batching                                                         */
/* ========================================================================== */

interface Batches {
  stone: GeoBatch;
  paint: GeoBatch;
  block: GeoBatch;
  tile: GeoBatch;
  slab: GeoBatch;
  cellSteel: GeoBatch;
  catwalk: GeoBatch;
  winTrim: GeoBatch;
  grate: GeoBatch;
  grille: GeoBatch;
  glaze: GeoBatch;
  cellPaint: GeoBatch;
  stainless: GeoBatch;
  diffuser: GeoBatch;
  ceiling: GeoBatch;
  flakes: GeoBatch;
}

/** Shared unit-box template. Built once, transformed thousands of times. */
const BOX = CreateBoxVertexData({ size: 1 });

/**
 * A CPU-side mesh accumulator — the same device 3.1b uses.
 *
 * This scene places on the order of five thousand primitives. Creating five
 * thousand `Mesh`es and calling `MergeMeshes` would allocate and immediately
 * discard about twenty thousand GL buffers; appending transformed vertex data
 * into plain arrays and building one mesh at the end costs nothing.
 *
 * UVs are deliberately NOT written for box geometry — the batch bakes world
 * positions into the vertices, so `worldUV` at the end gives every piece a
 * different patch of the texture for free, and no two cell doors in the run
 * sample the same rust.
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
    // Always write a UV pair per vertex, even when the source has none. A batch
    // that mixes authored-UV geometry (a plane pointed at an atlas cell) with
    // unauthored geometry (a box that will be world-projected) otherwise ends up
    // with the two streams out of step, and every quad after the first one reads
    // the wrong texels.
    if (uv && uv.length === (src.length / 3) * 2) {
      for (let i = 0; i < uv.length; i++) this.uvs.push(uv[i]);
    } else {
      for (let i = 0; i < src.length / 3; i++) this.uvs.push(0, 0);
    }
    for (let i = 0; i < idx.length; i++) this.indices.push(idx[i] + this.base);
    this.base += src.length / 3;
  }

  /**
   * Emit the batch as `chunks` meshes, split along +Z by triangle centroid.
   *
   * One mesh per material is the cheap way to build this scene, but a single
   * 58 m mesh is never outside the frustum, so every frame paid for the entire
   * building no matter where it was pointed. Splitting the run into slices lets
   * the culler do its job without giving up the batching. Vertices are compacted
   * per chunk, so a slice carries only the vertices its own triangles use.
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
          pos.push(this.positions[src * 3], this.positions[src * 3 + 1], this.positions[src * 3 + 2]);
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

    let zMin = Infinity;
    let zMax = -Infinity;
    for (let i = 2; i < this.positions.length; i += 3) {
      const z = this.positions[i];
      if (z < zMin) zMin = z;
      if (z > zMax) zMax = z;
    }
    const span = Math.max(1e-6, zMax - zMin);
    const buckets: number[][] = [];
    for (let k = 0; k < chunks; k++) buckets.push([]);
    for (let t = 0; t < this.indices.length; t += 3) {
      const a = this.indices[t];
      const b = this.indices[t + 1];
      const c = this.indices[t + 2];
      const zc =
        (this.positions[a * 3 + 2] + this.positions[b * 3 + 2] + this.positions[c * 3 + 2]) / 3;
      const k = Math.max(0, Math.min(chunks - 1, Math.floor(((zc - zMin) / span) * chunks)));
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

/**
 * One tile of steel bar grating, 0.30 m square.
 *
 * Bearing bars on the short pitch, cross rods on the long one, with a bright
 * worn line along the top of every bearing bar — the boot-polish that is the
 * first thing you see when a headlamp rakes across a walkway.
 */
function makeGratingTexture(scene: Scene): Texture {
  const S = 512;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = S;
  const c = canvas.getContext('2d')!;
  c.clearRect(0, 0, S, S);

  // Bearing bars: 10 across the tile → 30 mm centres.
  const bearing = 10;
  const bp = S / bearing;
  const bw = Math.round(bp * 0.31);
  for (let i = 0; i < bearing; i++) {
    const x = Math.round(i * bp);
    c.fillStyle = '#3f3d3a';
    c.fillRect(x, 0, bw, S);
    // Worn top edge.
    c.fillStyle = '#8e8c86';
    c.fillRect(x, 0, Math.max(2, Math.round(bw * 0.34)), S);
    c.fillStyle = '#5a5852';
    c.fillRect(x + bw - 2, 0, 2, S);
  }
  // Cross rods: 3 across the tile → 100 mm centres.
  const cross = 3;
  const cp = S / cross;
  const cw = Math.round(cp * 0.13);
  for (let i = 0; i < cross; i++) {
    const y = Math.round(i * cp + cp * 0.3);
    c.fillStyle = '#4a4844';
    c.fillRect(0, y, S, cw);
    c.fillStyle = '#7d7b75';
    c.fillRect(0, y, S, Math.max(2, Math.round(cw * 0.4)));
  }

  // Grime and rust variation, on the bars only.
  const img = c.getImageData(0, 0, S, S);
  const d = img.data;
  const rng = mulberry(19510401); // the year the East block was refitted
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 8) continue;
    const n = 0.78 + rng() * 0.42;
    d[i] = Math.min(255, d[i] * n * 1.04);
    d[i + 1] = Math.min(255, d[i + 1] * n);
    d[i + 2] = Math.min(255, d[i + 2] * n * 0.94);
  }
  c.putImageData(img, 0, 0);

  const tex = new Texture(canvas.toDataURL('image/png'), scene, false, false);
  tex.hasAlpha = true;
  tex.anisotropicFilteringLevel = 8;
  return tex;
}

const NUM_ATLAS = 2048;
const NUM_GRID = 16;
const NUM_CELL = NUM_ATLAS / NUM_GRID;

/**
 * The stencilled cell numbers. 144 of them, one atlas, one draw call.
 *
 * Numbered by tier — 101–136, 201–236, 301–336, 401–436 — in the sequence the
 * survey photograph shows running along a tier. Deliberately imperfect: a
 * stencil brush leaves ragged edges and ninety years of repaint fills the
 * counters in.
 */
function buildNumberAtlas(scene: Scene): Texture {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = NUM_ATLAS;
  const c = canvas.getContext('2d')!;
  c.clearRect(0, 0, NUM_ATLAS, NUM_ATLAS);
  c.textAlign = 'center';
  c.textBaseline = 'middle';

  const rng = mulberry(19511112);
  let cell = 0;
  for (let t = 0; t < TIERS; t++) {
    for (let i = 0; i < CELL_N; i++) {
      const cx = (cell % NUM_GRID) * NUM_CELL;
      const cy = Math.floor(cell / NUM_GRID) * NUM_CELL;
      const label = String((t + 1) * 100 + i + 1);

      c.save();
      c.translate(cx + NUM_CELL / 2, cy + NUM_CELL / 2);
      c.rotate((rng() - 0.5) * 0.04);
      const size = Math.round(NUM_CELL * 0.46);
      c.font = `bold ${size}px "Arial Narrow", Helvetica, Arial, sans-serif`;
      // Wear: some numbers are almost gone, most are merely dirty.
      const wear = rng();
      const alpha = wear < 0.12 ? 0.34 : wear < 0.4 ? 0.68 : 0.92;
      c.fillStyle = `rgba(238,236,228,${alpha})`;
      c.fillText(label, 0, 0);
      // Stencil bridges: the gaps a real stencil leaves in the strokes.
      c.globalCompositeOperation = 'destination-out';
      c.fillStyle = '#000';
      for (let b = 0; b < 3; b++) {
        c.fillRect(-size, -size * 0.5 + b * size * 0.5 - 2, size * 2, 3);
      }
      c.restore();
      cell++;
    }
  }

  // invertY LEFT ON (Babylon's default) so v = 0 is the bottom of the canvas,
  // which is the convention `remapUV` below assumes. With it off — and with the
  // u flip that was added to "fix" the mirroring it caused — every cell number
  // rendered rotated 180 degrees, legible only in the capture. Mipmaps left on
  // as well; 144 numbers seen down a 58 m gallery alias badly without them.
  const tex = new Texture(canvas.toDataURL('image/png'), scene, false);
  tex.hasAlpha = true;
  tex.wrapU = Texture.CLAMP_ADDRESSMODE;
  tex.wrapV = Texture.CLAMP_ADDRESSMODE;
  tex.anisotropicFilteringLevel = 8;
  return tex;
}

/** Point a unit-square plane's UVs at one atlas cell. */
function remapUV(vd: VertexData, cell: number): void {
  const uv = vd.uvs as number[] | Float32Array | null;
  if (!uv) return;
  const col = cell % NUM_GRID;
  const row = NUM_GRID - 1 - Math.floor(cell / NUM_GRID);
  const s = 1 / NUM_GRID;
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

/** The same deterministic PRNG 1.1 and 3.1b use, so captures are byte-stable. */
function mulberry(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

