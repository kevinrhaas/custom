import { MeshBuilder } from '@babylonjs/core/Meshes/meshBuilder';
import { Vector3 } from '@babylonjs/core/Maths/math.vector';
import { Color3 } from '@babylonjs/core/Maths/math.color';
import { PBRMaterial } from '@babylonjs/core/Materials/PBR/pbrMaterial';
import { StandardMaterial } from '@babylonjs/core/Materials/standardMaterial';
import { SpotLight } from '@babylonjs/core/Lights/spotLight';
import { PointLight } from '@babylonjs/core/Lights/pointLight';
import { ParticleSystem } from '@babylonjs/core/Particles/particleSystem';
import { Texture } from '@babylonjs/core/Materials/Textures/texture';
import { Color4 } from '@babylonjs/core/Maths/math.color';

import '@babylonjs/core/Particles/particleSystemComponent';

import { GameScene, type SceneManifest } from './SceneBase';
import { buildWall, buildTower, buildGround, buildBarredWindow } from '../core/Kit';
import { C, HEX, srgb } from '../core/Palette';
import { profile } from '../core/Settings';

/**
 * Scene 1.1 — Perimeter Approach.
 *
 * The look-dev lock scene. Everything downstream composes from what gets
 * frozen here.
 *
 * Composition intent: the player arrives from Collins Street on the east. The
 * wall runs away north-south across the whole frame, foreshortened, with one
 * tower breaking the skyline left of centre and the cell-house gable behind
 * it. A single surviving sodium lamp on a pole throws a warm pool onto the
 * asphalt that reads against the cold moon on the stone — that warm/cool
 * split is the frame's whole reason to exist, and it is also the navigation
 * cue: the three entries are all *away* from the light.
 *
 * Three entries, per the design doc: drainage trench (wet/fast/loud), wall
 * breach at the old quarry cut (exposed, needs a climb), maintenance gate
 * (Mike's knowledge or a lockpick). Each drops into 1.2 at a different point.
 */
export class PerimeterApproach extends GameScene {
  readonly manifest: SceneManifest = {
    id: '1.1-perimeter',
    title: 'Perimeter Approach',
    spawn: { position: [0, 0.2, -34], yaw: 0 },
    anchors: [
      {
        name: 'a1-arrival',
        position: [24, 1.68, -25],
        rotation: [-0.86, -0.05],
        note: 'The establishing frame. Wall foreshortened, tower left of centre, sodium pool right.',
      },
      {
        name: 'a2-wall-raking',
        position: [-9.5, 1.68, -12],
        rotation: [1.24, 0.06],
        note: 'Moon rakes the rustication. Tests the limestone normal + per-block colour variance.',
      },
      {
        name: 'a3-tower-up',
        position: [-16.2, 1.55, -3.4],
        rotation: [0.5, -0.62],
        note: 'Looking up the tower shaft to the corbel collar and glazed cab. Silhouette test.',
      },
      {
        name: 'a4-sodium-pool',
        position: [7.5, 1.68, -18],
        rotation: [-0.35, -0.1],
        note: 'Warm/cool split. Tests bloom restraint, tone mapping and asphalt roughness.',
      },
      {
        name: 'a5-trench',
        position: [13.5, 1.55, -12.5],
        rotation: [0.02, 0.42],
        note: 'The drainage trench entry. Wet stone, standing water, foliage intrusion.',
      },
    ],
  };

  private sodium!: SpotLight;
  private flicker = 0;
  private motes?: ParticleSystem;

  /** The trench mouth. Every ground surface omits this rectangle. */
  private static readonly TRENCH_APERTURE = {
    minX: 12.15,
    maxX: 14.85,
    minZ: -8.5,
    maxZ: 8.5,
  };

  async build(): Promise<void> {
    const ctx = this.kit();
    const p = profile();
    const aperture = [PerimeterApproach.TRENCH_APERTURE];

    // ---- Materials -------------------------------------------------------
    const stone = this.mats.get('limestone.wall');
    const towerStone = this.mats.get('limestone.tower');
    const wetStone = this.mats.get('limestone.wet');
    const asphalt = this.mats.get('asphalt.yard');
    const slab = this.mats.get('concrete.slab');
    const steel = this.mats.get('steel.catwalk');
    const doorSteel = this.mats.get('steel.door');
    const water = this.mats.get('water.standing');

    const glass = new PBRMaterial('cabGlass', this.scene);
    glass.albedoColor = new Color3(0.015, 0.02, 0.026);
    glass.metallic = 0;
    glass.roughness = 0.14;
    glass.alpha = 0.3;
    glass.environmentIntensity = 1.9;
    // Single-sided and drawn late. Double-sided alpha on a mesh this large
    // smeared a translucent panel across the whole wall behind it.
    glass.backFaceCulling = true;
    glass.separateCullingPass = true;
    glass.forceDepthWrite = false;

    const roof = new PBRMaterial('shingle', this.scene);
    roof.albedoColor = srgb('#4a3a34');
    roof.metallic = 0;
    roof.roughness = 0.92;

    // ---- Ground ----------------------------------------------------------
    // Asphalt apron in front of the wall; gravel/dirt beyond the kerb.
    // Subdivided finely enough that the trench aperture cuts on a boundary
    // close to the intended line — the coping stones cover the remainder.
    const apron = MeshBuilder.CreateGround(
      'apron',
      { width: 90, height: 46, subdivisions: 120 },
      this.scene,
    );
    apron.position.set(0, 0.06, -22);
    apron.material = asphalt;
    cutGroundAperture(apron, aperture, new Vector3(0, 0.06, -22));
    ctx.register(apron, { collide: true, cast: false, surface: 'asphalt' });

    // A single flat base plane well below the apron. The earlier displaced
    // version produced large shading facets and z-fought the apron across the
    // whole frame; the site is a flat asphalt yard and does not need terrain.
    buildGround(ctx, slab, {
      size: 190,
      subdivisions: 128,
      amplitude: 0,
      surface: 'gravel',
      apertures: aperture,
    });

    // Mown lawn strip between the apron and the wall — the site is maintained.
    const lawn = MeshBuilder.CreateGround(
      'lawn',
      { width: 90, height: 6.5, subdivisions: 90 },
      this.scene,
    );
    lawn.position.set(0, 0.05, 2.4);
    cutGroundAperture(lawn, aperture, new Vector3(0, 0.05, 2.4));
    const lawnMat = new PBRMaterial('lawn', this.scene);
    lawnMat.albedoColor = C.lawnGreen;
    lawnMat.metallic = 0;
    lawnMat.roughness = 0.95;
    lawn.material = lawnMat;
    ctx.register(lawn, { collide: true, cast: false, surface: 'grass' });

    // ---- The wall --------------------------------------------------------
    // Runs east-west across the frame at z = +6, with a return leg.
    const wall = buildWall(ctx, { stone, metal: steel }, {
      length: 88,
      height: 7.6,
      thickness: 1.15,
    });
    wall.position.set(0, 0, 6);

    const returnWall = buildWall(ctx, { stone, metal: steel }, {
      length: 40,
      height: 7.6,
      thickness: 1.15,
    });
    returnWall.position.set(-44, 0, 26);
    returnWall.rotation.y = Math.PI / 2;

    // ---- Towers ----------------------------------------------------------
    // One at the corner, one mid-run. Placed off-centre so the frame is not
    // symmetrical — symmetry reads as level design, not as a real site.
    const t1 = buildTower(
      ctx,
      { stone: towerStone, metal: steel, glass, roof },
      { shaftHeight: 9.4, baseRadius: 1.85, cab: 'octagon' },
    );
    t1.position.set(-17.5, 0, 6);

    const t2 = buildTower(
      ctx,
      { stone: towerStone, metal: steel, glass, roof },
      { shaftHeight: 8.6, baseRadius: 1.7, cab: 'octagon' },
    );
    t2.position.set(30, 0, 6);

    // ---- Cell house behind the wall (silhouette only from here) ----------
    const block = MeshBuilder.CreateBox(
      'cellHouse',
      { width: 54, height: 15.5, depth: 20 },
      this.scene,
    );
    block.position.set(-4, 7.75, 24);
    block.material = stone;
    ctx.register(block, { collide: true, cast: true, surface: 'stone' });

    // Gable roof: two slanted planes plus the end walls. Built explicitly
    // rather than as a scaled 3-sided cylinder — scaling a rotated primitive
    // skews it, which is how the first iteration ended up with a pair of giant
    // black wedges across the sky.
    const roofPitch = 0.46; // ≈26°, the shallow pitch in the reference
    const halfSpan = 10;
    const slope = Math.hypot(halfSpan, halfSpan * Math.tan(roofPitch));
    for (const side of [-1, 1]) {
      const pane = MeshBuilder.CreateBox(
        'roofPane',
        { width: 54.6, height: 0.35, depth: slope * 2 * 0.52 },
        this.scene,
      );
      pane.position.set(-4, 15.5 + (halfSpan * Math.tan(roofPitch)) / 2, 24 + side * halfSpan * 0.5);
      pane.rotation.x = -side * roofPitch;
      pane.material = roof;
      ctx.register(pane, { collide: false, cast: true });
    }
    // Gable end walls close the triangle so you never see under the roof.
    for (const end of [-1, 1]) {
      const tri = MeshBuilder.CreateBox(
        'gableEnd',
        { width: 0.6, height: halfSpan * Math.tan(roofPitch), depth: 20 },
        this.scene,
      );
      tri.position.set(-4 + end * 27, 15.5 + (halfSpan * Math.tan(roofPitch)) / 2, 24);
      tri.material = stone;
      ctx.register(tri, { collide: false, cast: true });
    }

    // Barred windows along the visible upper elevation.
    for (let i = 0; i < 9; i++) {
      const w = buildBarredWindow(ctx, { stone, metal: steel }, {
        width: 1.2,
        height: 2.5,
        bars: 5,
      });
      w.position.set(-26 + i * 5.6, 11.4, 13.9);
      w.rotation.y = Math.PI;
    }

    // ---- Entry 1: the drainage trench (east end) -------------------------
    this.buildTrench(ctx, wetStone, water);

    // ---- Entry 2: wall breach at the old quarry cut ----------------------
    this.buildBreach(ctx, stone, wetStone);

    // ---- Entry 3: maintenance gate ---------------------------------------
    this.buildGate(ctx, stone, doorSteel, steel);

    // ---- Lighting --------------------------------------------------------
    this.buildSodiumLamp(ctx, steel);

    // A second, failing lamp far down the wall gives depth cueing and a
    // reason for the eye to travel along the wall line.
    const distant = new PointLight('distantLamp', new Vector3(34, 8.2, -6), this.scene);
    distant.diffuse = C.sodiumVapour;
    distant.intensity = 260;
    distant.range = 34;

    // ---- Atmosphere ------------------------------------------------------
    if (p.particleBudget > 200) this.buildMotes(p.particleBudget);

    await this.scene.whenReadyAsync();
  }

  /**
   * The drainage trench: a stone-lined cut running under the wall, half full
   * of standing water, with vegetation over the lip. Fast and loud.
   */
  private buildTrench(
    ctx: ReturnType<GameScene['kit']>,
    wetStone: PBRMaterial,
    water: PBRMaterial,
  ): void {
    const x = 13.5;
    const walls: [number, number, number][] = [
      [x - 1.6, -1.3, 0],
      [x + 1.6, -1.3, 0],
    ];
    for (const [wx, wy] of walls) {
      const side = MeshBuilder.CreateBox(
        'trenchSide',
        { width: 0.7, height: 2.8, depth: 16 },
        this.scene,
      );
      side.position.set(wx, wy, 0);
      side.material = wetStone;
      ctx.register(side, { collide: true, cast: true, surface: 'stone' });
    }

    const floor = MeshBuilder.CreateBox(
      'trenchFloor',
      { width: 3.9, height: 0.3, depth: 16 },
      this.scene,
    );
    floor.position.set(x, -2.6, 0);
    floor.material = wetStone;
    ctx.register(floor, { collide: true, cast: false, surface: 'water' });

    const surface = MeshBuilder.CreateGround(
      'trenchWater',
      { width: 3.85, height: 15.8, subdivisions: 12 },
      this.scene,
    );
    surface.position.set(x, -2.15, 0);
    surface.material = water;
    surface.isPickable = false;
    surface.receiveShadows = false;
    this.meshes.push(surface);

    // The culvert head under the wall — a segmental arch in the stone.
    const arch = MeshBuilder.CreateCylinder(
      'culvert',
      { height: 2.2, diameter: 3.4, tessellation: 12, arc: 0.5 },
      this.scene,
    );
    arch.rotation.x = Math.PI / 2;
    arch.rotation.y = Math.PI;
    arch.position.set(x, -1.2, 6);
    arch.material = wetStone;
    ctx.register(arch, { collide: false, cast: true });

    // Coping stones along both lips. They read as the real kerb of a drainage
    // cut AND they hide the ragged edge where the ground aperture had to cut
    // on triangle boundaries.
    for (const side of [-1, 1]) {
      const coping = MeshBuilder.CreateBox(
        'trenchCoping',
        { width: 0.85, height: 0.26, depth: 17.4 },
        this.scene,
      );
      coping.position.set(x + side * 1.92, 0.02, 0);
      coping.material = wetStone;
      ctx.register(coping, { collide: true, cast: true, surface: 'stone' });
    }
  }

  /** The quarry-cut breach: collapsed masonry making a climbable ramp. */
  private buildBreach(
    ctx: ReturnType<GameScene['kit']>,
    stone: PBRMaterial,
    wetStone: PBRMaterial,
  ): void {
    const bx = -32;
    // Tumbled blocks. Deterministic placement so the climb always works.
    const rng = mulberry(20250801);
    for (let i = 0; i < 22; i++) {
      const s = 0.5 + rng() * 0.75;
      const b = MeshBuilder.CreateBox(
        `rubble${i}`,
        { width: s * 1.5, height: s * 0.62, depth: s * 1.1 },
        this.scene,
      );
      const t = i / 22;
      b.position.set(
        bx + (rng() - 0.5) * 5.5,
        0.3 + t * 3.1 + rng() * 0.3,
        2.2 - t * 3.4 + (rng() - 0.5) * 1.4,
      );
      b.rotation.set((rng() - 0.5) * 0.5, rng() * Math.PI, (rng() - 0.5) * 0.42);
      b.material = i % 4 === 0 ? wetStone : stone;
      ctx.register(b, { collide: true, cast: true, surface: 'stone' });
    }
  }

  /** The maintenance gate: a steel leaf in a stone opening, chained. */
  private buildGate(
    ctx: ReturnType<GameScene['kit']>,
    stone: PBRMaterial,
    doorSteel: PBRMaterial,
    metal: PBRMaterial,
  ): void {
    const gx = 2.5;
    // Concrete lintel over the opening, as in the reference service gate.
    const lintel = MeshBuilder.CreateBox(
      'gateLintel',
      { width: 5.2, height: 0.85, depth: 1.5 },
      this.scene,
    );
    lintel.position.set(gx, 4.3, 6);
    lintel.material = stone;
    ctx.register(lintel, { collide: true, cast: true });

    for (const dx of [-1.1, 1.1]) {
      const leaf = MeshBuilder.CreateBox(
        'gateLeaf',
        { width: 2.1, height: 3.8, depth: 0.12 },
        this.scene,
      );
      leaf.position.set(gx + dx, 1.9, 5.42);
      leaf.material = doorSteel;
      ctx.register(leaf, { collide: true, cast: true, surface: 'metal' });
    }

    // The diagonal brace strut lying against the leaf in the reference photo.
    const brace = MeshBuilder.CreateBox(
      'gateBrace',
      { width: 0.16, height: 4.6, depth: 0.16 },
      this.scene,
    );
    brace.position.set(gx - 1.4, 1.5, 5.1);
    brace.rotation.x = 0.42;
    brace.rotation.z = 0.28;
    brace.material = metal;
    ctx.register(brace, { collide: true, cast: true });
  }

  /**
   * The surviving sodium lamp. Warm, buzzing, and slightly unstable — old
   * high-pressure sodium cycles as it ages, and that slow breathe is free
   * atmosphere.
   */
  private buildSodiumLamp(ctx: ReturnType<GameScene['kit']>, metal: PBRMaterial): void {
    const px = 9.5;
    const pz = -14;
    const poleH = 8.4;

    const pole = MeshBuilder.CreateCylinder(
      'lampPole',
      { height: poleH, diameter: 0.19, tessellation: 8 },
      this.scene,
    );
    pole.position.set(px, poleH / 2, pz);
    pole.material = metal;
    ctx.register(pole, { collide: true, cast: true });

    const arm = MeshBuilder.CreateBox('lampArm', { width: 1.5, height: 0.11, depth: 0.11 }, this.scene);
    arm.position.set(px - 0.7, poleH - 0.15, pz);
    arm.material = metal;
    ctx.register(arm, { collide: false, cast: true });

    const head = MeshBuilder.CreateBox(
      'lampHead',
      { width: 0.72, height: 0.2, depth: 0.42 },
      this.scene,
    );
    head.position.set(px - 1.35, poleH - 0.28, pz);
    head.material = metal;
    ctx.register(head, { collide: false, cast: true });

    // The emissive lens itself — small and genuinely bright, which is what
    // gives bloom something honest to bloom on.
    const lens = MeshBuilder.CreateBox(
      'lampLens',
      { width: 0.56, height: 0.05, depth: 0.3 },
      this.scene,
    );
    lens.position.set(px - 1.35, poleH - 0.39, pz);
    const lensMat = new PBRMaterial('lampLens', this.scene);
    lensMat.albedoColor = Color3.Black();
    lensMat.emissiveColor = C.sodiumVapour.scale(3.4);
    lensMat.metallic = 0;
    lensMat.roughness = 0.3;
    lens.material = lensMat;
    lens.isPickable = false;
    this.meshes.push(lens);

    this.sodium = new SpotLight(
      'sodium',
      new Vector3(px - 1.35, poleH - 0.45, pz),
      new Vector3(0, -1, 0),
      1.5,
      3,
      this.scene,
    );
    this.sodium.diffuse = C.sodiumVapour;
    this.sodium.specular = C.sodiumVapour;
    this.sodium.intensity = 1400;
    this.sodium.range = 26;
    this.sodium.innerAngle = 0.5;
    this.sodium.falloffType = SpotLight.FALLOFF_PHYSICAL;
    this.sodium.shadowEnabled = false; // one shadow-casting light is enough
  }

  /**
   * Dust and insects in the lamp cone. Particles are only worth their cost
   * where a light can catch them, so they are confined to the sodium pool.
   */
  private buildMotes(budget: number): void {
    const ps = new ParticleSystem('motes', Math.min(budget, 900), this.scene);
    ps.particleTexture = makeDotTexture(this.scene);
    ps.emitter = new Vector3(8.2, 5.2, -14);
    ps.minEmitBox = new Vector3(-3.5, -3.5, -3.5);
    ps.maxEmitBox = new Vector3(3.5, 3.2, 3.5);
    ps.color1 = new Color4(1, 0.78, 0.45, 0.5);
    ps.color2 = new Color4(1, 0.86, 0.6, 0.28);
    ps.colorDead = new Color4(1, 0.8, 0.5, 0);
    ps.minSize = 0.012;
    ps.maxSize = 0.038;
    ps.minLifeTime = 5;
    ps.maxLifeTime = 12;
    ps.emitRate = 90;
    ps.blendMode = ParticleSystem.BLENDMODE_ADD;
    ps.gravity = new Vector3(0, -0.035, 0);
    ps.direction1 = new Vector3(-0.12, -0.04, -0.12);
    ps.direction2 = new Vector3(0.12, 0.06, 0.12);
    ps.minEmitPower = 0.02;
    ps.maxEmitPower = 0.09;
    ps.updateSpeed = 0.012;
    ps.start();
    this.motes = ps;
  }

  override update(dt: number, _player?: unknown): void {
    // Ageing HPS lamps cycle slowly. Two detuned sines plus a rare dropout
    // reads as electrical rather than as an animation curve.
    this.flicker += dt;
    const slow = Math.sin(this.flicker * 0.7) * 0.5 + Math.sin(this.flicker * 1.9) * 0.22;
    const dropout = Math.sin(this.flicker * 0.13) > 0.985 ? 0.45 : 1;
    if (this.sodium) this.sodium.intensity = (1400 + slow * 120) * dropout;
  }

  override dispose(): void {
    this.motes?.dispose();
    super.dispose();
  }
}

/**
 * Cut an aperture out of a ground mesh built directly (rather than via
 * `buildGround`, which takes apertures itself). `origin` is the mesh's world
 * position, because the aperture is specified in world space and the vertex
 * data is local.
 */
function cutGroundAperture(
  mesh: import('@babylonjs/core/Meshes/mesh').Mesh,
  apertures: { minX: number; maxX: number; minZ: number; maxZ: number }[],
  origin: Vector3,
): void {
  const positions = mesh.getVerticesData('position');
  const indices = mesh.getIndices();
  if (!positions || !indices) return;

  const kept: number[] = [];
  for (let t = 0; t < indices.length; t += 3) {
    let cx = 0;
    let cz = 0;
    for (let k = 0; k < 3; k++) {
      cx += positions[indices[t + k] * 3];
      cz += positions[indices[t + k] * 3 + 2];
    }
    cx = cx / 3 + origin.x;
    cz = cz / 3 + origin.z;
    const inside = apertures.some(
      (a) => cx >= a.minX && cx <= a.maxX && cz >= a.minZ && cz <= a.maxZ,
    );
    if (!inside) kept.push(indices[t], indices[t + 1], indices[t + 2]);
  }
  mesh.setIndices(kept);
}

/** Small deterministic PRNG so rubble placement is stable across iterations. */
function mulberry(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** A soft round dot for particles, generated rather than shipped. */
function makeDotTexture(scene: import('@babylonjs/core/scene').Scene): Texture {
  const size = 32;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d')!;
  const g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  g.addColorStop(0, 'rgba(255,255,255,1)');
  g.addColorStop(0.4, 'rgba(255,255,255,0.5)');
  g.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, size, size);
  const t = new Texture(canvas.toDataURL('image/png'), scene, true, false);
  t.hasAlpha = true;
  return t;
}

export { HEX };
