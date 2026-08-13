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
 * Wading, and why `walkHeight()` is not `surfaceHeight()`
 * --------------------------------------------------------
 * The heightfield carries the real channel bed — about -12 ft in the main stem.
 * A walker whose eye is pinned to that surface walks into the river and ends up
 * looking at the world from under the water, which reads as a bug rather than
 * as a river. `walkHeight()` therefore reports the WALKABLE surface: dry ground
 * where there is dry ground, and a wall at the waterline where there is not, so
 * the walker stops at the water's edge the way a person without a boat does.
 * `surfaceHeight()` still reports the real surface, the mesh still draws it, and
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
import { HORIZON_HAZE } from './world.js';

export const DEG = Math.PI / 180;

/** The vertical datum: the summer-1835 lake and river water surface. */
export const WATER_Y = 0;
/** Below this the ground is under water and the walker may not stand on it. */
const SHORE_Y = -0.10;
/** What `walkHeight()` reports over water: high enough that the walker's 0.35 m
 *  step-up rule refuses it from any bank in the dataset. */
const WATER_BARRIER_Y = 4.0;

/** How finely the ground is cut for frustum culling — a trade between triangles
 *  saved and draw calls spent, both of which main.js budgets (600 000 and 80).
 *  Measured end to end through the smoke at 1280×800, against 58 draw calls and
 *  550 513 triangles untiled:
 *
 *      8 × 4   71 calls   488 405 tris
 *     12 × 3   71 calls   461 112 tris   <- here
 *     12 × 6   79 calls   434 516 tris
 *
 *  12 × 3 is strictly better than 8 × 4: the same draw calls for 27 000 fewer
 *  triangles. 12 × 6 buys another 26 000 and costs eight more calls, which would
 *  leave ONE of headroom — a gate that fails on the next building batch is not
 *  headroom. Columns outnumber rows 4:1 rather than the 2.5:1 the box's own
 *  2 km × 800 m shape suggests because culling here is mostly by BEARING: a walker
 *  looks along the box, so cuts across the long axis are the ones that pay. */
const GROUND_TILE_COLS = 12;
const GROUND_TILE_ROWS = 3;

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
  // `.map` is null here — the prairie tile is bound as a shader uniform, not as
  // the standard material map, so disposing `.map` disposed nothing and leaked
  // the canvas texture on every epoch change.
  disposables.push(groundMat, groundMat.userData.groundTex);
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
  // The ground was `frustumCulled = false` because one mesh wrapped around the
  // camera always intersects the frustum, so testing it could only ever cost time
  // or throw the floor away by mistake. True of one mesh; not true of the ground.
  // Cut it into tiles and the half of the world behind you stops being drawn —
  // see tileGround() for the measurements behind the grid below.
  const tiles = tileGround(ground, GROUND_TILE_COLS, GROUND_TILE_ROWS);
  if (tiles) {
    for (const tile of tiles) {
      group.add(tile);
      disposables.push(tile.geometry);
    }
    // The source mesh is never added to the scene, so nothing else will dispose it.
    ground.geometry.dispose();
    ground = tiles[0];
  } else {
    // A ground too coarse to tile is small enough not to need it.
    ground.frustumCulled = false;
    group.add(ground);
    disposables.push(ground.geometry);
  }

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

    /** The one rendered terrain surface in metres at local ENU (e, n).
     * Buildings, streets, trees and plant roots all anchor to this sampler. */
    surfaceHeight(e, n) { return heightfield.sample(e, n); },

    /**
     * The WALKABLE surface: the rendered terrain on land, with the documented
     * navigation barrier over open water. See the note at the top of this file.
     */
    walkHeight(e, n) {
      const h = heightfield.sample(e, n);
      return h < SHORE_Y ? WATER_BARRIER_Y : h;
    },

    /** Backward-compatible names for older harnesses and external consumers. */
    height(e, n) {
      const h = heightfield.sample(e, n);
      return h < SHORE_Y ? WATER_BARRIER_Y : h;
    },
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

/**
 * Cut the ground into a grid of tiles so frustum culling has something to bite on.
 *
 * The ground arrives as ONE mesh spanning the whole 2 km × 800 m box, and a single
 * mesh that surrounds the camera always intersects the frustum — so culling it can
 * never help, which is exactly why it was switched off. That was the correct
 * conclusion from a false premise: the premise is that the ground has to be one
 * mesh. Cut into tiles, each tile gets its own bounding sphere, and the ones behind
 * you stop being drawn.
 *
 * Measured on the committed 247,527-triangle ground, standing on South Water and
 * looking south: 4×2 culls 29 % of it, 6×3 and 8×4 both cull 54 %, 12×6 culls 79 %.
 * Looking straight down from the `from_above` anchor — where culling helps least and
 * costs most, because nearly everything is on screen — 12×6 still culls 54 % and
 * leaves 26 tiles visible. Tiles are cheap draw calls (one shared material, no state
 * change between them) but they are NOT free, and `main.js` budgets 80. The grid
 * finally chosen is at GROUND_TILE_COLS, with the end-to-end numbers beside it;
 * the per-tile percentages here are what made it worth trying at all.
 *
 * The split is by triangle CENTROID, so no triangle is duplicated and no seam is
 * introduced: every triangle lands in exactly one tile and the surface is the same
 * surface. Every attribute travels with it — `_confidence` included, which the
 * confidence view reads, and which a naive position-only split would silently drop.
 */
function tileGround(mesh, cols, rows) {
  const geo = mesh.geometry;
  const pos = geo.attributes.position;
  if (!pos) return null;
  const index = geo.index ? geo.index.array : null;
  const triCount = index ? index.length / 3 : pos.count / 3;
  if (triCount < cols * rows * 4) return null;   // too coarse to be worth splitting

  geo.computeBoundingBox();
  const bb = geo.boundingBox;
  const spanX = (bb.max.x - bb.min.x) / cols;
  const spanZ = (bb.max.z - bb.min.z) / rows;
  if (!(spanX > 0) || !(spanZ > 0)) return null;

  const px = pos.array;
  const buckets = new Map();
  for (let t = 0; t < triCount; t++) {
    const a = index ? index[t * 3] : t * 3;
    const b = index ? index[t * 3 + 1] : t * 3 + 1;
    const c = index ? index[t * 3 + 2] : t * 3 + 2;
    const cx = (px[a * 3] + px[b * 3] + px[c * 3]) / 3;
    const cz = (px[a * 3 + 2] + px[b * 3 + 2] + px[c * 3 + 2]) / 3;
    const col = Math.min(cols - 1, Math.max(0, Math.floor((cx - bb.min.x) / spanX)));
    const row = Math.min(rows - 1, Math.max(0, Math.floor((cz - bb.min.z) / spanZ)));
    const key = row * cols + col;
    let bucket = buckets.get(key);
    if (!bucket) { bucket = []; buckets.set(key, bucket); }
    bucket.push(a, b, c);
  }
  if (buckets.size < 2) return null;

  const names = Object.keys(geo.attributes);
  const tiles = [];
  for (const [key, verts] of [...buckets.entries()].sort((x, y) => x[0] - y[0])) {
    const tileGeo = new THREE.BufferGeometry();
    for (const name of names) {
      const src = geo.attributes[name];
      const size = src.itemSize;
      const out = new Float32Array(verts.length * size);
      for (let i = 0; i < verts.length; i++) {
        const v = verts[i];
        for (let k = 0; k < size; k++) out[i * size + k] = src.array[v * size + k];
      }
      tileGeo.setAttribute(name, new THREE.BufferAttribute(out, size));
    }
    tileGeo.computeBoundingSphere();
    const tile = new THREE.Mesh(tileGeo, mesh.material);
    tile.name = `${mesh.name || 'terrain'}__t${key}`;
    tile.receiveShadow = mesh.receiveShadow;
    tile.castShadow = mesh.castShadow;
    tile.frustumCulled = true;
    tiles.push(tile);
  }
  return tiles;
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
  // BAKE the node transform into the geometry before flattening it. Resetting
  // position/rotation/scale to identity is the right normalisation for an
  // AUTHORED transform and catastrophic for an ENCODED one: under
  // `KHR_mesh_quantization` the dequantisation lives on the node as a scale and
  // a translation, so discarding it collapses the ground to a fraction of its
  // size and drops it under the water plane. Applying it first keeps the mesh
  // exactly where the file says while still handing back something at identity.
  found.updateWorldMatrix(true, false);
  found.geometry = found.geometry.clone();
  found.geometry.applyMatrix4(found.matrixWorld);
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
 *
 * WHAT THE DRY BAND MAY AND MAY NOT DO. It used to multiply the high ground by
 * (1.12, 1.06, 0.85) across `smoothstep(0.55, 1.25)`. The committed heightfield
 * puts the whole west-side plain between 0.87 and 1.24 m — its own gradient audit
 * reports under 0.5 ft of relief per 300 ft — so that band was not selecting
 * anything: it applied at 77–92 % strength over the entire open prairie and
 * turned it straw. Straw is the October negative control, not July. The
 * replacement is a narrow, gentle mesic tint over the top of the actual
 * elevation range: enough that the driest ground is a lighter, yellower green
 * than the swales, nowhere near enough to senesce it.
 *
 * So what this paints is WETNESS, from the heightfield, and nothing else. It is
 * not a community map: there is no plant-community record in `data/` for it to
 * read yet, and a renderer that invented the boundary between wet and mesic
 * prairie would be filling a gap silently. When those records land, the zone a
 * point falls in belongs here — and the ground stops being one green.
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
  // and halved the frame rate under software rasterisation. The finer octaves
  // are therefore baked INTO that one texture (see prairieTexture) and the
  // patch-scale variation above the tile is arithmetic, which costs a fraction
  // of a filtered fetch.
  vec3 chiTex = texture2D(uGround, vChiWorld.xz * 0.0909).rgb;

  // Community mosaic — 42 m by 48 m, broken by a 15 m diagonal. The two sines
  // this replaces beat at ~200 m, a soft blur the size of a city block that read
  // as cloud shadow rather than as ground; prairie patchiness is a
  // swale-and-rise business at tens of metres, which is the scale the
  // heightfield's own relief works at. THREE sines total, one more than before
  // and no more: this runs once per ground fragment and the ground is most of
  // the screen, so the count is a budget, not a taste (the same reason there is
  // exactly one texture fetch above). Amplitude is held near +/-14 % — past that
  // the pattern competes with the sward instead of sitting under it.
  float chiPatch = sin(vChiWorld.x * 0.1496 + 1.7) * sin(vChiWorld.z * 0.1309)
                 + 0.6 * sin(vChiWorld.x * 0.3307 - vChiWorld.z * 0.2712 + 4.1);
  diffuseColor.rgb *= chiTex * (1.0 + 0.088 * chiPatch);

  // Wet ground: the marshy shore strip, keyed on height above the datum.
  // Dossier zone 11 puts that strip at +0.5 to +2.0 ft and the heightfield puts
  // it at +1.25 ft, so elevation is the honest driver — it paints the mud wide
  // on the low South Division shore and narrow on the higher north and west
  // banks, which is what the sources say. The top of the band is pulled in to
  // 0.70 m so it stops at the foot of the plain (p25 of the land is 0.83 m)
  // instead of tinting it.
  float chiWet = 1.0 - smoothstep(0.05, 0.70, vChiWorld.y);
  diffuseColor.rgb = mix(diffuseColor.rgb,
                         diffuseColor.rgb * vec3(0.46, 0.42, 0.30) + vec3(0.042, 0.034, 0.020),
                         chiWet);

  // Drier mesic prairie on the rises. A July shift, not a September one: a few
  // per cent lighter and a few per cent less blue, so the crown of the plain
  // reads finer and yellower than the swale beside it and still reads green.
  diffuseColor.rgb *= mix(vec3(1.0), vec3(1.05, 1.03, 0.92),
                          smoothstep(0.95, 1.28, vChiWorld.y));
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
    // The same colour the far ground goes to (world.js HORIZON_HAZE), so the
    // river and the plain agree about what distance looks like — a hand-picked
    // grey-green here used to leave the water reading a season cooler than the
    // air above it.
    //
    // ONE conversion, not two. `new THREE.Color(hex)` already reads the hex as
    // sRGB and stores it in the renderer's linear working space
    // (ColorManagement.enabled is true by default since three r152), so the
    // `.convertSRGBToLinear()` that used to follow it applied the transfer
    // function a second time: the old 0x98a69d reached the shader as linear
    // (0.080,0.120,0.093) instead of (0.314,0.381,0.337) — 31 % of its intended
    // radiance. `outgoingLight` is linear at this point in the fragment, so what
    // the grazing angle mixed toward was not distance at all, it was a dark
    // olive: the far water read as a stain on the plain rather than as sky lying
    // on it, and the comment above it claimed the opposite in good faith.
    shader.uniforms.uSky = { value: new THREE.Color(HORIZON_HAZE) };
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
 * The July ground: one 256 px tile of procedural prairie, drawn once into a
 * canvas. It is the ALBEDO of what lies under the sward — visible as itself
 * between the clumps, and standing in for the sward wholesale past the range
 * where flora.js still plants instances.
 *
 * The colour is a measurement, not a taste. In the two verified July
 * photographs, Illinois tallgrass in the last week of July sits around sRGB
 * (122,139,74) in the middle distance and (109,128,78) at the far edge of the
 * field — a yellow-green whose green channel leads its red by about fifteen.
 * Working that target back through this scene's light (measured off the render
 * itself: the sky fill plus sun multiply albedo by ×1.42 red, ×1.42 green,
 * ×1.63 blue) and its ACES + sRGB output chain asks for a mean albedo near sRGB
 * (95,107,62), which is what this tile averages. It lands at (119,134,75) in the
 * middle distance of `prairie_west` — within three or four units of the
 * photograph on every channel.
 *
 * What it replaces averaged (139,139,91) — red and green level, a khaki closer
 * in hue to `bar/mesic_remnant_2016-10-27.jpg`, the OCTOBER negative control,
 * than to either July photograph. That is the failure this ramp exists to fix,
 * so the numbers are written down rather than left as three literals.
 *
 * Four octaves, not two, and all four baked into the same tile so the shader
 * still costs exactly one fetch: 0.7 m clumps, 0.35 m tussocks, 0.17 m leaf
 * mass and a per-texel grain that mipmaps away into tone by twenty metres out.
 * A minority of dry thatch is mixed in — last season's litter is present under a
 * July sward, and the palette record keeps it to a minority, which is where it
 * stays: it tints about a quarter of the tile and reaches half strength nowhere,
 * moving the mean by roughly two units.
 *
 * The tile stays 256 px, i.e. 4 cm per texel over its 11 m footprint. Doubling
 * it bought nothing the eye can find past the first few metres — the octave
 * sizes are fractions of the tile and so do not change with resolution — and
 * cost the software rasteriser measurably, this being the one texture that
 * covers the screen. Detail here is bought in octaves, not in pixels.
 */
function prairieTexture() {
  const S = 256;
  const c = document.createElement('canvas');
  c.width = c.height = S;
  const ctx = c.getContext('2d');
  const img = ctx.createImageData(S, S);
  let seed = 20260809;
  const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;

  /** A tiling value-noise octave: `n` cells across the tile, smoothstepped. */
  const octave = (n) => {
    const g = new Float32Array(n * n);
    for (let i = 0; i < g.length; i++) g[i] = rnd();
    const at = (x, y) => g[(((y % n) + n) % n) * n + (((x % n) + n) % n)];
    return (x, y) => {
      const gx = x * n / S, gy = y * n / S;
      const x0 = Math.floor(gx), y0 = Math.floor(gy);
      const fx = gx - x0, fy = gy - y0;
      const sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
      return (at(x0, y0) * (1 - sx) + at(x0 + 1, y0) * sx) * (1 - sy)
           + (at(x0, y0 + 1) * (1 - sx) + at(x0 + 1, y0 + 1) * sx) * sy;
    };
  };
  const o16 = octave(16);   // ~0.7 m — clump scale
  const o32 = octave(32);   // ~0.35 m — tussock
  const o64 = octave(64);   // ~0.17 m — leaf mass
  const oThatch = octave(48);

  // The July ramp. Dark = shaded green between the clumps; light = sunlit blade,
  // which is also the yellower of the two. Their midpoint plus the thatch below
  // is the (95,107,62) mean quoted above.
  const DARK = [68, 87, 49];
  const LIGHT = [118, 125, 72];
  // Last year's litter. Kept to a minority on purpose — this is the one colour
  // in the tile that, given its head, would turn the render into October.
  const THATCH = [138, 134, 94];

  for (let y = 0; y < S; y++) {
    for (let x = 0; x < S; x++) {
      const v = 0.42 * o16(x, y) + 0.26 * o32(x, y) + 0.18 * o64(x, y) + 0.14 * rnd();
      // Thatch shows only where the litter octave peaks and the sward is thin.
      const t = Math.max(0, oThatch(x, y) - 0.62) * (1.6 - v) * 0.9;
      const i = (y * S + x) * 4;
      for (let ch = 0; ch < 3; ch++) {
        const green = DARK[ch] + (LIGHT[ch] - DARK[ch]) * v;
        img.data[i + ch] = green + (THATCH[ch] - green) * Math.min(0.5, t);
      }
      img.data[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);

  const tex = new THREE.CanvasTexture(c);
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  // Anisotropy stays at 4. Eight taps on a 512 px tile looked slightly cleaner
  // on the grazing mid-field and cost the software rasteriser half its frame
  // rate — the ground is most of the screen, so doubling its filter taps doubles
  // the most expensive fetch in the frame. Measured against this file's previous
  // revision on the `prairie_west` pose: 2.0 fps before, 1.0 with the eight taps,
  // 2.2 back at four on a 256 tile. One fps is enough to fail the smoke's "walk
  // intent moves the camera" check, which is wall-clock. Same lesson as the
  // one-fetch rule above; do not raise it without re-running that check.
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
