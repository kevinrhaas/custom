/**
 * terrain.js — the ground, and the frame everything else is placed in.
 *
 * Two jobs:
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
 *   2. Sample ground height. Today that is a flat plane at y = 0, because the
 *      terrain epoch has not been baked yet (Track S2). The sampler below is the
 *      real bilinear one already — it just has nothing loaded, so it answers 0.
 *      When `heightfield.bin` lands, `loadHeightfield()` fills it in and the
 *      walker starts climbing the sand ridge without a line changing anywhere
 *      else.
 */

import * as THREE from 'three';

export const DEG = Math.PI / 180;

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
 * Layout, which is this renderer's REQUIREMENT on the terrain bake rather than
 * something the asset contract fixes yet (see the Track B report): row-major
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
 * The ground mesh. Flat until the epoch bake lands, but textured and lit so the
 * scene reads as ground rather than as a void, and so walking gives you the
 * motion parallax you need to judge distance.
 */
export function createTerrain({ sizeM = 2400, heightfield = new Heightfield() } = {}) {
  const group = new THREE.Group();
  group.name = 'terrain';

  const geo = new THREE.PlaneGeometry(sizeM, sizeM, 1, 1);
  geo.rotateX(-Math.PI / 2);

  const mat = new THREE.MeshStandardMaterial({
    color: 0x8a8b5e,
    roughness: 1,
    metalness: 0,
    map: prairieTexture(sizeM),
  });

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'ground';
  mesh.receiveShadow = true;
  mesh.position.y = heightfield.fallbackY;
  group.add(mesh);

  return {
    group,
    mesh,
    material: mat,
    heightfield,
    /** Ground elevation in metres at local ENU (e, n). */
    height(e, n) { return heightfield.sample(e, n); },
    dispose() {
      geo.dispose();
      mat.map?.dispose();
      mat.dispose();
    },
  };
}

/**
 * A cheap procedural prairie: value noise at two scales, drawn once into a
 * canvas. July 1835 grass, not a golf course — the point is legible motion, and
 * it costs one 256px texture instead of an asset with a license row.
 */
function prairieTexture(sizeM) {
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
  tex.repeat.set(sizeM / 6, sizeM / 6);   // one tile every 6 m
  tex.anisotropy = 4;
  tex.colorSpace = THREE.SRGBColorSpace;
  return tex;
}
