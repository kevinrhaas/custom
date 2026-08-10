/**
 * terrain.js — the ground, the river, and the frame everything else is placed in.
 *
 * Three jobs:
 *
 *   1. Own the coordinate convention. The dataset speaks local ENU metres
 *      (`local_e` east, `local_n` north from the datum origin). three speaks
 *      Y-up right-handed. The mapping, fixed here once so nothing else guesses:
 *
 *          world.x = +local_e        east
 *          world.y = +elevation      up (Z = 0 at the summer-1835 lake surface)
 *          world.z = -local_n        north is -Z, the way a camera at yaw 0 looks
 *
 *      `yaw_deg` in the dataset is a compass bearing: 0 = north, 90 = east,
 *      clockwise. three's rotation about +Y runs the other way, so
 *      `object.rotation.y = -bearing`.
 *
 *   2. Sample ground height, bilinearly, out of `heightfield.bin` — the same
 *      grid `generators/terrain_gen.py` built the ground mesh from, so what the
 *      walker stands on and what the walker sees are the same surface. The
 *      generator measures that agreement by ray-casting the decimated mesh
 *      against the field and refuses to export if it drifts past 30 mm.
 *
 *   3. Put the river on the screen. The water needs no shoreline geometry: the
 *      water surface IS the plane Y = 0, which is the vertical datum, and the
 *      ground crosses that plane exactly along the bank line traced off the
 *      Wright 1834 survey. So the waterline you see is the traced waterline,
 *      drawn by the depth buffer rather than by a second outline that could
 *      drift out of step with it.
 *
 * Wading, and why `height()` is not `heightfield.sample()`
 * --------------------------------------------------------
 * The heightfield carries the real channel bed — about -12 ft in the main stem.
 * A walker whose eye is pinned to that surface walks into the river and ends up
 * looking at the world from under the water, which reads as a bug rather than
 * as a river. `height()` therefore reports the WALKABLE surface: dry ground
 * where there is dry ground, and a wall at the waterline where there is not, so
 * the walker stops at the water's edge the way a person without a boat does.
 * `groundHeight()` still reports the real surface, the mesh still draws it, and
 * the heightfield still stores it. This is a navigation rule, not a claim about
 * the terrain — the moment there is a boat or a bridge it should be revisited.
 *
 * Its one edge: a walker TELEPORTED into the channel stands on the barrier and
 * appears to float. Walking cannot get you there, and every camera anchor in the
 * scene file is on land, so it is unreachable in normal use — but see
 * docs/LIBERTIES.md L9 rather than rediscovering it.
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export const DEG = Math.PI / 180;

/** The vertical datum: the summer-1835 lake and river water surface. */
export const WATER_Y = 0;
/** Below this the ground is under water and the walker may not stand on it. */
const SHORE_Y = -0.10;
/** What `height()` reports over water: high enough that the walker's 0.35 m
 *  step-up rule refuses it from any bank in the dataset. */
const WATER_BARRIER_Y = 4.0;

/** local ENU metres -> three world position. */
export function enuToWorld(e, n, y = 0, target = new THREE.Vector3()) {
  return target.set(e, y, -n);
}

/** three world position -> local ENU metres. */
export function worldToEnu(v) {
  return { e: v.x, n: -v.z, y: v.y };
}

/** dataset compass bearing (deg, 0 = N, clockwise) -> three yaw about +Y. */
export function bearingToYaw(deg) {
  return -deg * DEG;
}

/** three yaw about +Y -> dataset compass bearing, normalised to [0, 360). */
export function yawToBearing(yaw) {
  return ((-yaw / DEG) % 360 + 360) % 360;
}

/**
 * A regular grid of elevations, sampled bilinearly.
 *
 * Layout, which `generators/terrain_gen.py` writes and this reads: row-major
 * Float32 (or scaled Int16) samples, row 0 at the SOUTH edge, column 0 at the
 * WEST edge, `cell_m` metres apart, the sample at [0][0] sitting exactly on
 * (`origin_e`, `origin_n`) in local ENU metres.
 */
export class Heightfield {
  constructor() {
    this.loaded = false;
    this.cols = 0;
    this.rows = 0;
    this.cellM = 1;
    this.originE = 0;
    this.originN = 0;
    this.data = null;
    this.meta = null;
    /** Height used outside the grid and before anything is loaded. */
    this.fallbackY = 0;
  }

  get widthM() { return (this.cols - 1) * this.cellM; }
  get depthM() { return (this.rows - 1) * this.cellM; }

  /**
   * @param {object} meta  { cols, rows, cell_m, origin_e, origin_n, encoding?, scale?, offset? }
   * @param {ArrayBuffer} buffer  raw samples, row-major from the south-west corner
   */
  adopt(meta, buffer) {
    const cols = meta.cols | 0;
    const rows = meta.rows | 0;
    if (!(cols > 1 && rows > 1)) throw new Error('heightfield: cols/rows must be > 1');

    const encoding = meta.encoding || 'float32';
    let data;
    if (encoding === 'float32') {
      data = new Float32Array(buffer, 0, cols * rows);
    } else if (encoding === 'int16') {
      // Quantised metres: y = raw * scale + offset. The plan quantises to
      // <= 0.25 ft, which int16 carries comfortably over 15 ft of relief.
      const raw = new Int16Array(buffer, 0, cols * rows);
      const scale = meta.scale ?? 0.01;
      const offset = meta.offset ?? 0;
      data = new Float32Array(raw.length);
      for (let i = 0; i < raw.length; i++) data[i] = raw[i] * scale + offset;
    } else {
      throw new Error(`heightfield: unknown encoding '${encoding}'`);
    }
    if (data.length < cols * rows) {
      throw new Error(`heightfield: ${data.length} samples for a ${cols}x${rows} grid`);
    }

    this.cols = cols;
    this.rows = rows;
    this.cellM = meta.cell_m ?? meta.cellM ?? 1;
    this.originE = meta.origin_e ?? meta.originE ?? 0;
    this.originN = meta.origin_n ?? meta.originN ?? 0;
    this.data = data;
    this.meta = meta;
    this.loaded = true;
    return this;
  }

  async load(metaUrl, binUrl) {
    const meta = await (await fetch(metaUrl)).json();
    const buffer = await (await fetch(binUrl ?? new URL(meta.bin, metaUrl))).arrayBuffer();
    return this.adopt(meta, buffer);
  }

  /** Elevation in metres at local ENU (e, n). Bilinear; clamped at the edges. */
  sample(e, n) {
    if (!this.loaded) return this.fallbackY;
    const gx = (e - this.originE) / this.cellM;
    const gy = (n - this.originN) / this.cellM;
    if (gx < 0 || gy < 0 || gx > this.cols - 1 || gy > this.rows - 1) return this.fallbackY;

    const x0 = Math.min(Math.floor(gx), this.cols - 2);
    const y0 = Math.min(Math.floor(gy), this.rows - 2);
    const fx = gx - x0;
    const fy = gy - y0;
    const d = this.data;
    const r0 = y0 * this.cols;
    const r1 = r0 + this.cols;
    const h00 = d[r0 + x0], h10 = d[r0 + x0 + 1];
    const h01 = d[r1 + x0], h11 = d[r1 + x0 + 1];
    return (h00 * (1 - fx) + h10 * fx) * (1 - fy) + (h01 * (1 - fx) + h11 * fx) * fy;
  }

  /** Surface normal by central differences — for slope limits and shading. */
  normal(e, n, target = new THREE.Vector3()) {
    if (!this.loaded) return target.set(0, 1, 0);
    const d = this.cellM;
    const dydE = (this.sample(e + d, n) - this.sample(e - d, n)) / (2 * d);
    const dydN = (this.sample(e, n + d) - this.sample(e, n - d)) / (2 * d);
    return target.set(-dydE, 1, dydN).normalize();
  }
}

/**
 * Load the terrain for one epoch: the heightfield the walker samples, the
 * ground mesh, and the water surface.
 *
 * Degrades in one step at a time. No heightfield means a flat plane at the
 * datum and a recorded problem; no ground GLB means a mesh built here from the
 * heightfield, which is the same surface by construction and costs one boot
 * frame. Nothing here silently renders a fiction.
 *
 * @param {object} o
 * @param {URL} o.dataBase        where data/ lives
 * @param {URL} o.assetBase       where the GLBs live
 * @param {string} o.epochId      terrain epoch, from the scene file
 * @param {object} [o.confidence] the confidence view, to patch the materials into
 * @param {string[]} [o.problems] collector, same list the scene loader writes to
 */
export async function createTerrain({
  dataBase, assetBase, epochId, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'terrain';
  const heightfield = new Heightfield();
  const disposables = [];

  let meta = null;
  if (dataBase && epochId) {
    const metaUrl = new URL(`terrain/epochs/${epochId}/heightfield.json`, dataBase);
    try {
      meta = await (await fetchOk(metaUrl)).json();
      const bin = await (await fetchOk(new URL(meta.bin, metaUrl))).arrayBuffer();
      heightfield.adopt(meta, bin);
    } catch (err) {
      problems.push(`terrain ${epochId}: no heightfield (${err.message}) — `
        + 'the ground is a flat plane at the datum and the walker will not climb a bank');
      meta = null;
    }
  }

  // ---- the ground -------------------------------------------------------- //

  const groundMat = groundMaterial();
  disposables.push(groundMat, groundMat.map);
  confidence?.patch(groundMat);

  let ground = null;
  const groundPath = meta?.glb?.ground;
  if (groundPath && assetBase) {
    ground = await loadGlbMesh(new URL(groundPath, assetBase))
      .catch((err) => {
        problems.push(`terrain ${epochId}: ${groundPath} (${err.message}) — `
          + 'ground rebuilt from the heightfield instead');
        return null;
      });
  }
  if (ground) {
    confidence?.ensureAttribute(ground.geometry, `terrain ${epochId} ground`);
  } else {
    ground = new THREE.Mesh(gridGeometry(heightfield));
    ground.name = `terrain__${epochId ?? 'flat'}`;
  }
  ground.material = groundMat;
  ground.receiveShadow = true;
  ground.castShadow = false;
  // The ground is the biggest thing in the scene and it is always around the
  // camera; frustum culling it can only ever throw it away by mistake.
  ground.frustumCulled = false;
  group.add(ground);
  disposables.push(ground.geometry);

  // ---- the water --------------------------------------------------------- //

  const waterMat = waterMaterial();
  disposables.push(waterMat, waterMat.normalMap);
  confidence?.patch(waterMat);

  let water = null;
  const waterPath = meta?.glb?.water;
  if (waterPath && assetBase) {
    water = await loadGlbMesh(new URL(waterPath, assetBase)).catch(() => null);
  }
  if (!water) {
    const g = new THREE.PlaneGeometry(2400, 2400, 1, 1);
    g.rotateX(-Math.PI / 2);
    // The confidence channel is part of the contract even for a fallback mesh:
    // the water surface at the datum is the one DOCUMENTED thing in this layer.
    g.setAttribute('_confidence', new THREE.BufferAttribute(new Float32Array(4), 1));
    water = new THREE.Mesh(g);
    water.name = `water__${epochId ?? 'flat'}`;
  } else {
    confidence?.ensureAttribute(water.geometry, `terrain ${epochId} water`);
  }
  water.material = waterMat;
  water.position.y = WATER_Y;
  water.receiveShadow = false;
  water.castShadow = false;
  water.frustumCulled = false;
  // Draw the water AFTER the ground so the depth buffer rejects the water
  // fragments the bank hides — which is most of them, this being a 640 m box
  // with a river through it rather than a lake.
  water.renderOrder = 1;
  group.add(water);
  disposables.push(water.geometry);

  let t = 0;

  return {
    group,
    mesh: ground,
    water,
    material: groundMat,
    waterMaterial: waterMat,
    heightfield,
    meta,
    epochId,
    loaded: heightfield.loaded,

    /**
     * The WALKABLE surface in metres at local ENU (e, n): real ground on land,
     * a wall at the waterline. See the note at the top of this file.
     */
    height(e, n) {
      const h = heightfield.sample(e, n);
      return h < SHORE_Y ? WATER_BARRIER_Y : h;
    },

    /** The real surface, bank and channel bed alike. */
    groundHeight(e, n) { return heightfield.sample(e, n); },

    /** True where the terrain is below the water surface. */
    isWater(e, n) { return heightfield.sample(e, n) < SHORE_Y; },

    /** Drift the ripples. One line in the render loop; nothing else animates. */
    update(dt) {
      t += dt;
      const nm = waterMat.normalMap;
      if (nm) {
        nm.offset.set((t * 0.011) % 1, (t * 0.0068) % 1);
        nm.needsUpdate = false;      // offset is a uniform, not a re-upload
      }
    },

    dispose() {
      for (const d of disposables) d?.dispose?.();
    },
  };
}

async function fetchOk(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res;
}

/** Load a GLB and hand back its first mesh, detached from the loaded scene. */
async function loadGlbMesh(url) {
  const buffer = await (await fetchOk(url)).arrayBuffer();
  const loader = new GLTFLoader();
  const gltf = await new Promise((resolve, reject) => {
    loader.parse(buffer, String(url), resolve, reject);
  });
  let found = null;
  gltf.scene.traverse((o) => { if (!found && o.isMesh) found = o; });
  if (!found) throw new Error('no mesh in the GLB');
  found.removeFromParent();
  found.position.set(0, 0, 0);
  found.rotation.set(0, 0, 0);
  found.scale.set(1, 1, 1);
  found.updateMatrix();
  return found;
}

/**
 * Build the ground straight from the heightfield. Used when the baked GLB is
 * missing; identical surface, more triangles, and it means a missing asset
 * degrades to "slower" rather than to "no ground".
 */
function gridGeometry(hf) {
  if (!hf.loaded) {
    const g = new THREE.PlaneGeometry(2400, 2400, 1, 1);
    g.rotateX(-Math.PI / 2);
    g.setAttribute('_confidence',
      new THREE.BufferAttribute(new Float32Array(4).fill(1), 1));
    return g;
  }
  const { cols, rows, cellM, originE, originN } = hf;
  const pos = new Float32Array(cols * rows * 3);
  const conf = new Float32Array(cols * rows).fill(0.5);
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      const i = (r * cols + c) * 3;
      const y = hf.data[r * cols + c];
      pos[i] = originE + c * cellM;
      pos[i + 1] = y;
      pos[i + 2] = -(originN + r * cellM);
      if (y < SHORE_Y) conf[r * cols + c] = 1.0;
    }
  }
  const idx = new Uint32Array((cols - 1) * (rows - 1) * 6);
  let k = 0;
  for (let r = 0; r < rows - 1; r++) {
    for (let c = 0; c < cols - 1; c++) {
      const a = r * cols + c;
      // -Z is north, so the row-major grid is mirrored relative to ENU and the
      // winding has to be flipped to keep the normals up.
      idx[k++] = a; idx[k++] = a + cols; idx[k++] = a + 1;
      idx[k++] = a + 1; idx[k++] = a + cols; idx[k++] = a + cols + 1;
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.setAttribute('_confidence', new THREE.BufferAttribute(conf, 1));
  g.setIndex(new THREE.BufferAttribute(idx, 1));
  g.computeVertexNormals();
  return g;
}

/* -------------------------------------------------------------------------- */
/* materials                                                                   */
/* -------------------------------------------------------------------------- */

const WORLD_POS_VERT = /* glsl */`
  vChiWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;
`;

/**
 * Ground: a procedural prairie sampled in WORLD space, darkening to wet mud as
 * the surface approaches the water.
 *
 * World-space sampling rather than UVs, deliberately. The bake decimates the
 * ground wherever it is planar — which is most of it, this being Chicago — and
 * a UV set carried through a planar dissolve stretches across every dissolved
 * region. Sampling by world XZ cannot stretch, and it costs the GLB no
 * attribute at all.
 *
 * The wetness band is not decoration: dossier zone 11 puts a strip along the
 * South Division shore "where land and water mingled, covered with tall grass,
 * reeds and rushes" at +0.5 to +2.0 ft, and the heightfield puts that strip at
 * +1.25 ft. Keying the mud on elevation therefore paints exactly the zone the
 * source describes, and paints it narrow on the higher north and west banks —
 * which is also what the sources say.
 */
function groundMaterial() {
  const mat = new THREE.MeshStandardMaterial({
    color: 0xffffff, roughness: 1, metalness: 0,
  });
  const tex = prairieTexture();
  mat.map = null;
  mat.userData.groundTex = tex;

  const prior = mat.onBeforeCompile;
  mat.onBeforeCompile = (shader, renderer) => {
    if (typeof prior === 'function') prior(shader, renderer);
    shader.uniforms.uGround = { value: tex };
    shader.vertexShader = 'varying vec3 vChiWorld;\n' + shader.vertexShader.replace(
      '#include <begin_vertex>', '#include <begin_vertex>' + WORLD_POS_VERT,
    );
    shader.fragmentShader = `
varying vec3 vChiWorld;
uniform sampler2D uGround;
` + shader.fragmentShader.replace('#include <map_fragment>', /* glsl */`
  // ONE texture fetch, deliberately. The ground covers most of the screen, so
  // every instruction here is paid a million times a frame; a second octave
  // fetched from the same texture at a different scale looked slightly better
  // and halved the frame rate under software rasterisation. The large-scale
  // variation that stops the 11 m tile from reading as a tile is two sines
  // instead, which cost a fraction of a filtered fetch.
  vec3 chiTex = texture2D(uGround, vChiWorld.xz * 0.0909).rgb;
  float chiBroad = sin(vChiWorld.x * 0.031) * sin(vChiWorld.z * 0.0271) * 0.5 + 0.5;
  diffuseColor.rgb *= chiTex * (0.86 + 0.28 * chiBroad);

  // Wet ground: the marshy shore strip, keyed on height above the datum.
  // Dossier zone 11 puts that strip at +0.5 to +2.0 ft and the heightfield puts
  // it at +1.25 ft, so elevation is the honest driver — it paints the mud wide
  // on the low South Division shore and narrow on the higher north and west
  // banks, which is what the sources say.
  float chiWet = 1.0 - smoothstep(0.05, 0.78, vChiWorld.y);
  diffuseColor.rgb = mix(diffuseColor.rgb,
                         diffuseColor.rgb * vec3(0.46, 0.42, 0.30) + vec3(0.042, 0.034, 0.020),
                         chiWet);
  // Drier, tawnier prairie on the higher ground away from the river.
  diffuseColor.rgb *= mix(vec3(1.0), vec3(1.12, 1.06, 0.85),
                          smoothstep(0.55, 1.25, vChiWorld.y));
`);
  };
  mat.needsUpdate = true;
  return mat;
}

/**
 * Water: a silty prairie river, not a swimming pool.
 *
 * There is no environment map in this scene on purpose (see world.js — a PMREM
 * of the analytic sky swamped every albedo), so the water cannot get its look
 * from a reflection probe. It gets it from three cheap things instead: a
 * drifting ripple normal map, a low roughness so the single directional light
 * leaves a real sun glint, and a Fresnel term that turns the surface toward the
 * sky colour at grazing angles — which is most of what makes a flat plane read
 * as water when you are standing on the bank looking across it.
 */
function waterMaterial() {
  const mat = new THREE.MeshStandardMaterial({
    color: 0x3e4a38,
    roughness: 0.17,
    metalness: 0.0,
    normalMap: rippleTexture(),
    normalScale: new THREE.Vector2(0.55, 0.55),
  });
  // 2400 m of plane / 700 tiles = a 3.4 m ripple cell, which is the scale you
  // actually read from a bank. Mipmaps + anisotropy fade it to flat by the far
  // shore instead of aliasing into noise.
  mat.normalMap.wrapS = mat.normalMap.wrapT = THREE.RepeatWrapping;
  mat.normalMap.repeat.set(700, 700);
  mat.normalMap.anisotropy = 8;

  const prior = mat.onBeforeCompile;
  mat.onBeforeCompile = (shader, renderer) => {
    if (typeof prior === 'function') prior(shader, renderer);
    shader.uniforms.uSky = { value: new THREE.Color(0x93a2a4).convertSRGBToLinear() };
    shader.vertexShader = 'varying vec3 vChiWorld;\n' + shader.vertexShader.replace(
      '#include <begin_vertex>', '#include <begin_vertex>' + WORLD_POS_VERT,
    );
    shader.fragmentShader = `
varying vec3 vChiWorld;
uniform vec3 uSky;
` + shader.fragmentShader.replace('#include <opaque_fragment>', /* glsl */`
  {
    // Fresnel toward the sky, capped well short of 1. A full Fresnel makes the
    // whole river read as one slab of sky-blue paint from bank level, which is
    // where a visitor actually stands; capping it keeps the silt colour of a
    // prairie river in the mix all the way to the far shore.
    vec3 chiV = normalize(cameraPosition - vChiWorld);
    float chiF = pow(1.0 - clamp(dot(chiV, vec3(0.0, 1.0, 0.0)), 0.0, 1.0), 4.0);
    float chiRip = sin(vChiWorld.x * 0.42 + vChiWorld.z * 0.31) * 0.5 + 0.5;
    vec3 chiSky = uSky * (0.90 + 0.14 * chiRip);
    outgoingLight = mix(outgoingLight, chiSky, clamp(chiF, 0.0, 0.70));
  }
#include <opaque_fragment>
`);
  };
  mat.needsUpdate = true;
  return mat;
}

/**
 * A cheap procedural prairie: value noise at two scales, drawn once into a
 * canvas. July 1835 grass, not a golf course — the point is legible motion, and
 * it costs one 256px texture instead of an asset with a license row.
 */
function prairieTexture() {
  const S = 256;
  const c = document.createElement('canvas');
  c.width = c.height = S;
  const ctx = c.getContext('2d');
  const img = ctx.createImageData(S, S);
  let seed = 20260809;
  const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;

  const coarse = new Float32Array(32 * 32);
  for (let i = 0; i < coarse.length; i++) coarse[i] = rnd();
  const at = (x, y) => coarse[((y & 31) * 32) + (x & 31)];

  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const gx = x / 8, gy = y / 8;
      const x0 = Math.floor(gx), y0 = Math.floor(gy);
      const fx = gx - x0, fy = gy - y0;
      const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
      const n = (at(x0, y0) * (1 - sx) + at(x0 + 1, y0) * sx) * (1 - sy)
              + (at(x0, y0 + 1) * (1 - sx) + at(x0 + 1, y0 + 1) * sx) * sy;
      const v = n * 0.55 + rnd() * 0.45;
      const i = (y * S + x) * 4;
      img.data[i]     = 116 + v * 46;
      img.data[i + 1] = 118 + v * 42;
      img.data[i + 2] = 74 + v * 34;
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);

  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.anisotropy = 4;
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}

/** A drifting ripple normal map, generated once. */
function rippleTexture() {
  const S = 128;
  const c = document.createElement('canvas');
  c.width = c.height = S;
  const ctx = c.getContext('2d');
  const img = ctx.createImageData(S, S);

  const h = new Float32Array(S * S);
  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const u = (x / S) * Math.PI * 2;
      const v = (y / S) * Math.PI * 2;
      h[y * S + x] = Math.sin(u * 3 + Math.cos(v * 2) * 0.8) * 0.5
                   + Math.sin(v * 5 - u * 2) * 0.3
                   + Math.sin(u * 9 + v * 7) * 0.2;
    }
  }
  const at = (x, y) => h[((y + S) % S) * S + ((x + S) % S)];
  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const dx = (at(x + 1, y) - at(x - 1, y)) * 0.5;
      const dy = (at(x, y + 1) - at(x, y - 1)) * 0.5;
      const len = Math.hypot(dx, dy, 1);
      const i = (y * S + x) * 4;
      img.data[i]     = Math.round((-dx / len * 0.5 + 0.5) * 255);
      img.data[i + 1] = Math.round((-dy / len * 0.5 + 0.5) * 255);
      img.data[i + 2] = Math.round((1 / len * 0.5 + 0.5) * 255);
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  return tex;
}
