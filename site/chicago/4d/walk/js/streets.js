/**
 * streets.js — dated earth travelways, draped on the committed heightfield.
 *
 * The compiled scene index supplies two different widths and they stay
 * different here:
 *
 *   corridor_width_m  the 80-foot platted right-of-way used to answer
 *                     "which street am I standing in?"
 *   track_width_m     the narrower, visibly worn wagon path inside it
 *
 * The second is a stated visual liberty.  It is not allowed to flatten the
 * terrain or author a second collision surface: every ribbon vertex samples
 * terrain.surfaceHeight(), and the walker continues to stand on that exact same
 * heightfield.  Segments whose centres or edges are under water are omitted,
 * leaving honest gaps at unbridged channels rather than painting a ford.
 */

import * as THREE from 'three';

const STEP_M = 2.25;
const LIFT_M = 0.022;
const LEVEL = { documented: 0, inferred: 0.5, conjectural: 1 };

function pointSegment(e, n, a, b) {
  const dx = b[0] - a[0];
  const dn = b[1] - a[1];
  const len2 = dx * dx + dn * dn || 1e-9;
  const t = Math.max(0, Math.min(1, ((e - a[0]) * dx + (n - a[1]) * dn) / len2));
  const pe = a[0] + dx * t;
  const pn = a[1] + dn * t;
  return { distance: Math.hypot(e - pe, n - pn), e: pe, n: pn, t };
}

function prepare(raw) {
  const path = (raw.path_local_enu_m ?? []).map(([e, n]) => [Number(e), Number(n)]);
  const pad = Math.max(raw.corridor_width_m ?? 24.384, raw.track_width_m ?? 6) * 0.5;
  const es = path.map((p) => p[0]);
  const ns = path.map((p) => p[1]);
  return {
    ...raw,
    path,
    corridor_width_m: raw.corridor_width_m ?? 24.384,
    track_width_m: raw.track_width_m ?? 6,
    bounds: {
      e0: Math.min(...es) - pad, e1: Math.max(...es) + pad,
      n0: Math.min(...ns) - pad, n1: Math.max(...ns) + pad,
    },
  };
}

function nearestOn(record, e, n) {
  const b = record.bounds;
  if (e < b.e0 || e > b.e1 || n < b.n0 || n > b.n1) return null;
  let best = null;
  for (let i = 1; i < record.path.length; i++) {
    const hit = pointSegment(e, n, record.path[i - 1], record.path[i]);
    if (!best || hit.distance < best.distance) best = { ...hit, segment: i - 1 };
  }
  return best ? { ...best, street: record } : null;
}

function sampled(path) {
  const out = [];
  for (let i = 1; i < path.length; i++) {
    const a = path[i - 1];
    const b = path[i];
    const d = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const count = Math.max(1, Math.ceil(d / STEP_M));
    for (let j = 0; j < count; j++) {
      if (!out.length) out.push([a[0], a[1]]);
      const t = (j + 1) / count;
      out.push([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]);
    }
  }
  return out;
}

function addRecord(buffers, record, terrain) {
  const key = record.surface;
  const buf = buffers.get(key) ?? { pos: [], uv: [], conf: [], idx: [] };
  buffers.set(key, buf);
  const pts = sampled(record.path);
  let along = 0;
  const confidence = Math.max(
    LEVEL[record.surface_confidence] ?? 1,
    LEVEL[record.wear_confidence] ?? 1,
  );

  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1];
    const b = pts[i];
    const de = b[0] - a[0];
    const dn = b[1] - a[1];
    const length = Math.hypot(de, dn);
    if (length < 1e-5) continue;
    const half = record.track_width_m * 0.5;
    const le = -dn / length * half;
    const ln = de / length * half;
    const corners = [
      [a[0] + le, a[1] + ln], [a[0] - le, a[1] - ln],
      [b[0] + le, b[1] + ln], [b[0] - le, b[1] - ln],
    ];
    // The centre check removes river crossings; the edge checks keep a bank
    // road from painting over water just because its legal corridor reaches it.
    if (terrain.isWater(a[0], a[1]) || terrain.isWater(b[0], b[1])
        || corners.some(([e, n]) => terrain.isWater(e, n))) {
      along += length;
      continue;
    }

    const base = buf.pos.length / 3;
    for (const [e, n] of corners) {
      buf.pos.push(e, terrain.surfaceHeight(e, n) + LIFT_M, -n);
      buf.conf.push(confidence);
    }
    // Across first, distance along second. The texture repeats every eight
    // metres, long enough that its ruts read as travel rather than corduroy.
    buf.uv.push(0, along / 8, 1, along / 8,
      0, (along + length) / 8, 1, (along + length) / 8);
    buf.idx.push(base, base + 2, base + 1, base + 1, base + 2, base + 3);
    along += length;
  }
}

function hash(x, y) {
  let h = Math.imul(x + 17, 374761393) ^ Math.imul(y + 31, 668265263);
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
}

function roadTexture(surface) {
  const canvas = document.createElement('canvas');
  canvas.width = 128;
  canvas.height = 256;
  const ctx = canvas.getContext('2d');
  const image = ctx.createImageData(canvas.width, canvas.height);
  const graded = surface === 'graded_earth';
  const light = surface === 'light_worn_earth';
  const base = graded ? [113, 91, 55] : light ? [102, 85, 55] : [106, 84, 50];
  for (let y = 0; y < canvas.height; y++) {
    for (let x = 0; x < canvas.width; x++) {
      const q = x / (canvas.width - 1);
      const edge = Math.min(1, Math.max(0, Math.min(q, 1 - q) / 0.12));
      const ruts = Math.exp(-(((q - 0.29) / 0.065) ** 2))
        + Math.exp(-(((q - 0.71) / 0.065) ** 2));
      const crown = Math.exp(-(((q - 0.5) / 0.13) ** 2));
      const grain = (hash(x >> 1, y >> 1) - 0.5) * 18
        + (hash(x >> 3, y >> 3) - 0.5) * 11;
      const wet = ruts * (graded ? 13 : 18);
      const i = (y * canvas.width + x) * 4;
      image.data[i] = Math.max(0, Math.min(255, base[0] + grain - wet));
      image.data[i + 1] = Math.max(0, Math.min(255, base[1] + grain * 0.74 - wet));
      image.data[i + 2] = Math.max(0, Math.min(255, base[2] + grain * 0.48 - wet * 0.58));
      const body = graded
        ? 0.54 + ruts * 0.25 - crown * 0.08
        : light ? 0.08 + ruts * 0.54 - crown * 0.04
          : 0.20 + ruts * 0.55 - crown * 0.08;
      image.data[i + 3] = Math.round(255 * edge * Math.max(0, Math.min(0.92, body)));
    }
  }
  ctx.putImageData(image, 0, 0);
  const texture = new THREE.CanvasTexture(canvas);
  texture.name = `street-${surface}`;
  texture.wrapS = THREE.ClampToEdgeWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.magFilter = THREE.LinearFilter;
  texture.minFilter = THREE.LinearMipmapLinearFilter;
  texture.anisotropy = 4;
  return texture;
}

function meshOf(surface, buf, confidence) {
  if (!buf.idx.length) return null;
  const geo = new THREE.BufferGeometry();
  geo.name = `streets-${surface}`;
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(buf.uv, 2));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.setIndex(buf.idx);
  geo.computeVertexNormals();
  const map = roadTexture(surface);
  const mat = new THREE.MeshStandardMaterial({
    map,
    transparent: true,
    alphaTest: 0.025,
    depthWrite: false,
    roughness: 1,
    metalness: 0,
    side: THREE.DoubleSide,
    polygonOffset: true,
    polygonOffsetFactor: -1,
    polygonOffsetUnits: -1,
  });
  mat.name = `street-${surface}`;
  confidence?.patch(mat);
  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = `streets-${surface}`;
  mesh.receiveShadow = true;
  mesh.castShadow = false;
  mesh.renderOrder = 0;
  return { mesh, geo, mat, map };
}

export function createStreets({ terrain, records = [], confidence = null } = {}) {
  const group = new THREE.Group();
  group.name = 'streets';
  const prepared = records.filter((r) => Array.isArray(r.path_local_enu_m)
      && r.path_local_enu_m.length >= 2).map(prepare);
  const buffers = new Map();
  for (const record of prepared) addRecord(buffers, record, terrain);
  const resources = [];
  for (const [surface, buf] of buffers) {
    const built = meshOf(surface, buf, confidence);
    if (!built) continue;
    group.add(built.mesh);
    resources.push(built);
  }

  function hitsAt(e, n, widthKey = 'corridor_width_m') {
    const hits = [];
    for (const street of prepared) {
      const hit = nearestOn(street, e, n);
      if (hit && hit.distance <= street[widthKey] * 0.5) hits.push(hit);
    }
    hits.sort((a, b) => a.distance - b.distance);
    return hits;
  }

  function ahead(e, n, bearingDeg, excluded = new Set()) {
    const th = bearingDeg * Math.PI / 180;
    const de = Math.sin(th);
    const dn = Math.cos(th);
    for (let d = 5; d <= 70; d += 2.5) {
      const pe = e + de * d;
      const pn = n + dn * d;
      const hits = hitsAt(pe, pn).filter((h) => !excluded.has(h.street.id));
      if (hits.length) return { ...hits[0], ahead_m: d };
    }
    return null;
  }

  function status(e, n, bearingDeg = 0) {
    const on = hitsAt(e, n);
    // At a crossing, report only streets whose travelled/platted centre is
    // genuinely near the visitor.  This prevents two broad 80-ft corridors
    // from being called an intersection near a far corner of the overlap.
    const crossing = on.filter((h) => h.distance <= Math.min(8, h.street.corridor_width_m * 0.5));
    if (crossing.length >= 2) {
      return { mode: 'intersection', streets: crossing.slice(0, 2).map((h) => h.street) };
    }
    if (on.length) {
      const current = on[0].street;
      const upcoming = ahead(e, n, bearingDeg, new Set([current.id]));
      return { mode: 'on', streets: [current], upcoming };
    }
    const coming = ahead(e, n, bearingDeg);
    return coming
      ? { mode: 'ahead', streets: [coming.street], distance_m: coming.ahead_m }
      : null;
  }

  function blocksGrowth(e, n) {
    // A small shoulder clears roots/blades off the visibly worn track while
    // preserving the grassy remainder of the 80-foot corridor.
    for (const street of prepared) {
      const hit = nearestOn(street, e, n);
      if (hit && hit.distance <= street.track_width_m * 0.5 + 0.65) return true;
    }
    return false;
  }

  return {
    group,
    records: prepared,
    status,
    hitsAt,
    blocksGrowth,
    dispose() {
      for (const r of resources) {
        r.geo.dispose();
        r.mat.dispose();
        r.map.dispose();
      }
    },
  };
}
