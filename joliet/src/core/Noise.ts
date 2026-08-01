/**
 * Deterministic value/gradient noise used by the procedural texture bakery.
 *
 * Everything is seeded, so the same wall generates the same weathering on
 * every machine and every screenshot iteration. That determinism is what makes
 * the critic loop's fixed camera anchors comparable across iterations.
 */

export function hash2(x: number, y: number, seed: number): number {
  let h = x * 374761393 + y * 668265263 + seed * 1442695040888963407;
  h = (h ^ (h >> 13)) * 1274126177;
  return ((h ^ (h >> 16)) >>> 0) / 4294967296;
}

const fade = (t: number): number => t * t * t * (t * (t * 6 - 15) + 10);
const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;

/** Tileable value noise. Period must be an integer for seamless wrapping. */
export function valueNoise(x: number, y: number, period: number, seed: number): number {
  const xi = Math.floor(x);
  const yi = Math.floor(y);
  const xf = x - xi;
  const yf = y - yi;
  const w = (n: number) => ((n % period) + period) % period;

  const v00 = hash2(w(xi), w(yi), seed);
  const v10 = hash2(w(xi + 1), w(yi), seed);
  const v01 = hash2(w(xi), w(yi + 1), seed);
  const v11 = hash2(w(xi + 1), w(yi + 1), seed);

  const u = fade(xf);
  const v = fade(yf);
  return lerp(lerp(v00, v10, u), lerp(v01, v11, u), v);
}

/** Tileable fBm. `octaves` doublings from `period`. */
export function fbm(
  x: number,
  y: number,
  period: number,
  octaves: number,
  seed: number,
  gain = 0.5,
  lacunarity = 2,
): number {
  let amp = 1;
  let sum = 0;
  let norm = 0;
  let p = period;
  let f = 1;
  for (let o = 0; o < octaves; o++) {
    sum += valueNoise(x * f, y * f, p, seed + o * 97) * amp;
    norm += amp;
    amp *= gain;
    f *= lacunarity;
    p = Math.round(p * lacunarity);
  }
  return sum / norm;
}

/**
 * Tileable Worley/cellular noise. Returns { f1, f2, id } — f2-f1 gives crack
 * and mortar lines, `id` gives per-cell random values for brick/stone tinting.
 */
export function worley(
  x: number,
  y: number,
  cells: number,
  seed: number,
): { f1: number; f2: number; id: number } {
  const cx = Math.floor(x * cells);
  const cy = Math.floor(y * cells);
  let f1 = 1e9;
  let f2 = 1e9;
  let id = 0;

  for (let oy = -1; oy <= 1; oy++) {
    for (let ox = -1; ox <= 1; ox++) {
      const gx = cx + ox;
      const gy = cy + oy;
      const wx = ((gx % cells) + cells) % cells;
      const wy = ((gy % cells) + cells) % cells;
      const jx = hash2(wx, wy, seed);
      const jy = hash2(wx, wy, seed + 5171);
      const px = (gx + jx) / cells;
      const py = (gy + jy) / cells;
      const d = Math.hypot(x - px, y - py);
      if (d < f1) {
        f2 = f1;
        f1 = d;
        id = hash2(wx, wy, seed + 991);
      } else if (d < f2) {
        f2 = d;
      }
    }
  }
  return { f1: f1 * cells, f2: f2 * cells, id };
}

/**
 * Coursed-ashlar mask matching Joliet's perimeter wall: irregular course
 * heights, irregular block lengths within a course, deep raked joints.
 * Returns per-pixel { joint, blockId, uInBlock, vInBlock }.
 */
export function coursedStone(
  u: number,
  v: number,
  courses: number,
  seed: number,
): { joint: number; id: number; bu: number; bv: number } {
  // Irregular course heights: each course gets a jittered height.
  const cf = v * courses;
  let ci = Math.floor(cf);
  const jitterH = hash2(0, ((ci % courses) + courses) % courses, seed) * 0.42 - 0.21;
  const cLocal = cf - ci + jitterH * 0;
  const cwrap = ((ci % courses) + courses) % courses;

  // Blocks per course vary, and each course is offset — real coursed rubble
  // never lines up vertically.
  const perCourse = 5 + Math.floor(hash2(cwrap, 7, seed) * 4);
  const offset = hash2(cwrap, 13, seed);
  const bf = (u + offset) * perCourse;
  const bi = Math.floor(bf);
  const bLocal = bf - bi;
  const bwrap = ((bi % perCourse) + perCourse) % perCourse;

  // Joint width in block-local units, wider horizontally than vertically.
  const jh = 0.055;
  const jv = 0.085;
  const distToJointV = Math.min(cLocal, 1 - cLocal);
  const distToJointH = Math.min(bLocal, 1 - bLocal);
  const joint = Math.min(
    smoothstep(0, jh, distToJointV),
    smoothstep(0, jv, distToJointH),
  );

  return {
    joint,
    id: hash2(bwrap, cwrap, seed + 313),
    bu: bLocal,
    bv: cLocal,
  };
}

export function smoothstep(a: number, b: number, x: number): number {
  const t = Math.max(0, Math.min(1, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
}

export const clamp01 = (x: number): number => (x < 0 ? 0 : x > 1 ? 1 : x);

/** sRGB hex string to [r,g,b] 0-255. */
export function hexToRgb(hex: string): [number, number, number] {
  const h = hex.replace('#', '');
  return [
    parseInt(h.slice(0, 2), 16),
    parseInt(h.slice(2, 4), 16),
    parseInt(h.slice(4, 6), 16),
  ];
}

export function mixRgb(
  a: [number, number, number],
  b: [number, number, number],
  t: number,
): [number, number, number] {
  return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
}

/**
 * Build a tangent-space normal map from a height field by central differences.
 * `strength` in the 1-4 range reads well for masonry.
 */
export function heightToNormal(
  height: Float32Array,
  size: number,
  strength: number,
): Uint8ClampedArray {
  const out = new Uint8ClampedArray(size * size * 4);
  const at = (x: number, y: number): number =>
    height[((y + size) % size) * size + ((x + size) % size)];

  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const dx = (at(x + 1, y) - at(x - 1, y)) * strength;
      const dy = (at(x, y + 1) - at(x, y - 1)) * strength;
      // Normalise (-dx, -dy, 1)
      const len = Math.hypot(dx, dy, 1);
      const i = (y * size + x) * 4;
      out[i] = ((-dx / len) * 0.5 + 0.5) * 255;
      out[i + 1] = ((-dy / len) * 0.5 + 0.5) * 255; // OpenGL (+Y up) convention
      out[i + 2] = (1 / len) * 0.5 * 255 + 127.5;
      out[i + 3] = 255;
    }
  }
  return out;
}
