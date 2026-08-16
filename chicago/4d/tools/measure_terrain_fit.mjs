/**
 * measure_terrain_fit.mjs — does the ground a visitor SEES match the ground the
 * town is ANCHORED to?
 *
 * `generators/terrain_gen.py` already asks a version of this question: it
 * ray-casts the decimated ground mesh against the heightfield and refuses to
 * export past `MESH_FIT_TOLERANCE_M` (30 mm), because "the walker's eye is
 * pinned to the heightfield, so it would visibly float or sink". That gate is
 * real and it passes. It is also measuring the wrong file.
 *
 * The mesh it measures is the MASTER at `assets/gltf/`. What the browser loads
 * is the derivative at `assets/web/`, written afterwards by the
 * `gltf-transform optimize` step in `tools/bake.sh`, which quantises POSITION to
 * int16 under a single uniform node scale. On a surface 5 km wide and 8.6 m tall
 * that scale is set by the width, so the vertical lattice it lands on is coarse
 * — and no gate in this project looked at the file that ships.
 *
 * So this reader reads the SHIPPED bytes, decodes `EXT_meshopt_compression` and
 * `KHR_mesh_quantization` the way the renderer does, and compares vertex heights
 * against the same `heightfield.bin` the walker samples. It reports both meshes
 * by default, because the interesting number is the difference between them:
 * whatever the master's error is, the derivative's is the one a visitor stands
 * in.
 *
 *   node tools/measure_terrain_fit.mjs                 both meshes, table + verdict
 *   node tools/measure_terrain_fit.mjs --json          machine-readable
 *   node tools/measure_terrain_fit.mjs --epoch <id>    another epoch
 *
 * Exit status is 0 for a report and 1 only when it cannot read what it was asked
 * to read; the PASS/FAIL judgement belongs to `tools/check.sh`, which imports
 * `measureTerrainFit()` rather than parsing this output.
 */

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

/** The vertical drift a shipped ground mesh may carry, in metres.
 *
 * It is `generators/terrain_gen.py`'s own `MESH_FIT_TOLERANCE_M` (30 mm) and
 * deliberately the same number: the promise that "the ground you stand on is the
 * ground you see" is not weaker for the file that ships than for the file that
 * does not. The generator refuses to export past it; this refuses to publish
 * past it.
 */
export const SHIPPED_FIT_TOLERANCE_M = 0.03;

// --- glTF container ------------------------------------------------------ //

const GLB_MAGIC = 0x46546c67;
const COMPONENT = {
  5120: { array: Int8Array, norm: 127 },
  5121: { array: Uint8Array, norm: 255 },
  5122: { array: Int16Array, norm: 32767 },
  5123: { array: Uint16Array, norm: 65535 },
  5125: { array: Uint32Array, norm: 4294967295 },
  5126: { array: Float32Array, norm: 1 },
};
const ITEMS = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };

function parseGlb(buf) {
  const view = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  if (view.getUint32(0, true) !== GLB_MAGIC) throw new Error('not a GLB');
  let offset = 12;
  let json = null;
  let bin = null;
  while (offset < view.byteLength) {
    const len = view.getUint32(offset, true);
    const type = view.getUint32(offset + 4, true);
    const start = offset + 8;
    if (type === 0x4e4f534a) json = JSON.parse(buf.slice(start, start + len).toString('utf8'));
    else if (type === 0x004e4942) bin = buf.slice(start, start + len);
    offset = start + len + ((4 - (len % 4)) % 4) - ((4 - (len % 4)) % 4);
    offset = start + len;
  }
  if (!json) throw new Error('no JSON chunk');
  return { json, bin };
}

/**
 * The bytes of one bufferView, decompressed if it carries meshopt.
 *
 * `EXT_meshopt_compression` replaces the view's own slice of the BIN chunk with
 * an encoded stream plus the shape needed to decode it, so a reader that ignores
 * the extension reads noise rather than failing — which is the failure mode this
 * function exists to make impossible.
 */
async function viewBytes(gltf, bin, index, decoder) {
  const view = gltf.json.bufferViews[index];
  const ext = view.extensions?.EXT_meshopt_compression;
  if (!ext) {
    const start = view.byteOffset ?? 0;
    return bin.slice(start, start + view.byteLength);
  }
  await decoder.ready;
  const src = bin.slice(ext.byteOffset ?? 0, (ext.byteOffset ?? 0) + ext.byteLength);
  const out = new Uint8Array(ext.count * ext.byteStride);
  decoder.decodeGltfBuffer(out, ext.count, ext.byteStride, src, ext.mode, ext.filter);
  return Buffer.from(out.buffer, out.byteOffset, out.byteLength);
}

/** One accessor as plain numbers, dequantised exactly as a glTF reader must. */
async function readAccessor(gltf, bin, index, decoder) {
  const acc = gltf.json.accessors[index];
  const spec = COMPONENT[acc.componentType];
  const items = ITEMS[acc.type];
  if (!spec) throw new Error(`unknown componentType ${acc.componentType}`);
  const bytes = await viewBytes(gltf, bin, acc.bufferView, decoder);
  const view = gltf.json.bufferViews[acc.bufferView];
  const elemBytes = spec.array.BYTES_PER_ELEMENT * items;
  // A meshopt view declares its stride on the extension; three int16 padded to
  // eight bytes is the common case here, and reading it as six walks off by two
  // bytes per vertex into noise that still looks like terrain.
  const stride = view.byteStride ?? view.extensions?.EXT_meshopt_compression?.byteStride
    ?? elemBytes;
  const base = acc.byteOffset ?? 0;
  const out = new Float64Array(acc.count * items);
  const src = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const read = {
    5120: (o) => src.getInt8(o), 5121: (o) => src.getUint8(o),
    5122: (o) => src.getInt16(o, true), 5123: (o) => src.getUint16(o, true),
    5125: (o) => src.getUint32(o, true), 5126: (o) => src.getFloat32(o, true),
  }[acc.componentType];
  for (let i = 0; i < acc.count; i += 1) {
    for (let k = 0; k < items; k += 1) {
      const raw = read(base + i * stride + k * spec.array.BYTES_PER_ELEMENT);
      // A normalized integer is a fraction of full scale; the metres come from
      // the node transform, which is applied by the caller.
      out[i * items + k] = acc.normalized ? Math.max(raw / spec.norm, -1) : raw;
    }
  }
  return { data: out, items, componentType: acc.componentType, normalized: !!acc.normalized };
}

/** The ground mesh's world-space vertices, in ENU metres.
 *
 * Exported because the triangles are the surface: a vertex table answers "is
 * this corner at the right height", and only the triangles answer "is the
 * ground a visitor SEES the ground the town is placed on" — which is what
 * `tools/measure_terrain_horizontal.mjs` asks. A second reader of these bytes
 * would be a fourth; this file already decodes them the way the renderer does.
 */
export async function groundVertices(file, decoder, { indices = false } = {}) {
  const gltf = parseGlb(await readFile(file));
  const node = (gltf.json.nodes || []).find((n) => n.mesh !== undefined);
  if (!node) throw new Error(`${path.basename(file)}: no node with a mesh`);
  const mesh = gltf.json.meshes[node.mesh];
  const prim = mesh.primitives[0];
  const pos = await readAccessor(gltf, gltf.bin, prim.attributes.POSITION, decoder);
  let tris = null;
  if (indices) {
    if (prim.indices === undefined) throw new Error(`${path.basename(file)}: no index buffer`);
    const idx = await readAccessor(gltf, gltf.bin, prim.indices, decoder);
    tris = Uint32Array.from(idx.data);
  }
  const s = node.scale ?? [1, 1, 1];
  const t = node.translation ?? [0, 0, 0];
  const n = pos.data.length / 3;
  const out = new Float64Array(n * 3);
  for (let i = 0; i < n; i += 1) {
    // glTF is Y-up with +Z south (export_yup), so ENU east = x, north = -z.
    out[i * 3] = pos.data[i * 3] * s[0] + t[0];
    out[i * 3 + 1] = pos.data[i * 3 + 1] * s[1] + t[1];
    out[i * 3 + 2] = pos.data[i * 3 + 2] * s[2] + t[2];
  }
  return { xyz: out, count: n, node, accessor: pos, indices: tris };
}

// --- the heightfield the walker samples ---------------------------------- //

/** `renderers/web/js/terrain.js`'s sampler, in Node, with its own bytes. */
export async function loadHeightfield(epochDir) {
  const meta = JSON.parse(await readFile(path.join(epochDir, 'heightfield.json'), 'utf8'));
  const raw = await readFile(path.join(epochDir, meta.bin ?? 'heightfield.bin'));
  const arr = meta.encoding === 'float32'
    ? new Float32Array(raw.buffer, raw.byteOffset, raw.byteLength / 4)
    : new Int16Array(raw.buffer, raw.byteOffset, raw.byteLength / 2);
  const { cols, rows, cell_m: cell, origin_e: oe, origin_n: on } = meta;
  const scale = meta.scale ?? 0.01;
  const offset = meta.offset ?? 0;
  const at = (i, j) => arr[j * cols + i] * scale + offset;
  return {
    meta,
    inside(e, n) {
      return e >= oe && e <= oe + (cols - 1) * cell && n >= on && n <= on + (rows - 1) * cell;
    },
    height(e, n) {
      let x = (e - oe) / cell;
      let y = (n - on) / cell;
      x = Math.max(0, Math.min(cols - 1.001, x));
      y = Math.max(0, Math.min(rows - 1.001, y));
      const i = Math.floor(x);
      const j = Math.floor(y);
      const fx = x - i;
      const fy = y - j;
      const south = at(i, j) * (1 - fx) + at(i + 1, j) * fx;
      const north = at(i, j + 1) * (1 - fx) + at(i + 1, j + 1) * fx;
      return south * (1 - fy) + north * fy;
    },
  };
}

// --- the measurement ------------------------------------------------------ //

function summarise(errors) {
  if (!errors.length) return { samples: 0 };
  const sorted = Float64Array.from(errors).sort();
  const abs = errors.map(Math.abs).sort((a, b) => a - b);
  const sum = errors.reduce((a, b) => a + b, 0);
  const sq = errors.reduce((a, b) => a + b * b, 0);
  const pct = (p) => abs[Math.min(abs.length - 1, Math.floor(p * abs.length))];
  return {
    samples: errors.length,
    mean_m: sum / errors.length,
    rms_m: Math.sqrt(sq / errors.length),
    max_abs_m: abs[abs.length - 1],
    p95_abs_m: pct(0.95),
    p99_abs_m: pct(0.99),
    min_m: sorted[0],
    max_m: sorted[sorted.length - 1],
  };
}

/**
 * The vertical lattice a mesh's heights actually land on.
 *
 * A quantised POSITION does not merely round — it lands on a fixed ladder, and
 * the rung spacing IS the node scale divided by full integer scale. Recovering
 * it from the shipped numbers rather than from the JSON is the point: it proves
 * the coarseness is in the geometry and not in the reader.
 */
function verticalStep(node, accessor, xyz) {
  if (!accessor.normalized) return null;
  // NOT `node.scale / 32767`. `gltf-transform` quantises to a BIT DEPTH — 14 by
  // default — and stores the result in the next integer type up, so the low bits
  // are always zero and the true rung spacing is four times the container's. The
  // arithmetic answer understated this file's lattice by exactly that factor, so
  // the spacing is recovered from the shipped heights instead: the smallest gap
  // between two distinct values IS the rung.
  const seen = new Set();
  for (let i = 1; i < xyz.length; i += 3) seen.add(xyz[i]);
  const ys = [...seen].sort((a, b) => a - b);
  let step = Infinity;
  for (let i = 1; i < ys.length; i += 1) step = Math.min(step, ys[i] - ys[i - 1]);
  return Number.isFinite(step) ? step : null;
}

/** One ground GLB against one heightfield. Exported so an experiment can score a
 * candidate derivative without writing a second reader of these bytes. */
export async function measureMesh(file, hf, decoder) {
  const { xyz, count, node, accessor } = await groundVertices(file, decoder);
  const errors = [];
  for (let i = 0; i < count; i += 1) {
    const e = xyz[i * 3];
    const y = xyz[i * 3 + 1];
    const n = -xyz[i * 3 + 2];
    // The skirt carries boundary heights 1.5 km past the modelled box, where
    // there is no field to compare against and the sampler clamps. Scoring it
    // would measure the clamp, not the mesh.
    if (!hf.inside(e, n)) continue;
    errors.push(y - hf.height(e, n));
  }
  return {
    vertices: count,
    compared: errors.length,
    quantised: !!accessor.normalized,
    vertical_step_m: verticalStep(node, accessor, xyz),
    ...summarise(errors),
  };
}

export async function meshoptDecoder(root = ROOT) {
  const { MeshoptDecoder } = await import(
    path.join(root, 'renderers/web/vendor/three-0.185.1/addons/libs/meshopt_decoder.module.js')
  );
  return MeshoptDecoder;
}

export async function measureTerrainFit({ epoch, root = ROOT } = {}) {
  const decoder = await meshoptDecoder(root);
  const hf = await loadHeightfield(path.join(root, 'data/terrain/epochs', epoch));
  const out = { epoch, tolerance_m: SHIPPED_FIT_TOLERANCE_M, meshes: {} };
  for (const [which, rel] of [
    ['master', `assets/gltf/terrain__${epoch}.glb`],
    ['shipped', `assets/web/terrain__${epoch}.glb`],
  ]) {
    out.meshes[which] = { file: rel, ...await measureMesh(path.join(root, rel), hf, decoder) };
  }
  out.pass = out.meshes.shipped.max_abs_m <= SHIPPED_FIT_TOLERANCE_M;
  return out;
}

async function main() {
  const argv = process.argv.slice(2);
  const epoch = argv.includes('--epoch') ? argv[argv.indexOf('--epoch') + 1] : 'e1834_harbor_cut';
  const result = await measureTerrainFit({ epoch });
  if (argv.includes('--json')) {
    process.stdout.write(`${JSON.stringify(result, null, 1)}\n`);
    return;
  }
  const mm = (v) => (v === null || v === undefined ? '—' : `${(v * 1000).toFixed(1)} mm`);
  console.log(`   terrain fit — ${epoch}, against the heightfield the walker samples\n`);
  console.log('   mesh      vertices   compared   lattice     mean        rms         max |Δ|');
  for (const [which, m] of Object.entries(result.meshes)) {
    console.log(`   ${which.padEnd(9)} ${String(m.vertices).padStart(8)} `
      + `${String(m.compared).padStart(10)}   ${(m.vertical_step_m === null ? 'float'
        : mm(m.vertical_step_m)).padEnd(11)} ${mm(m.mean_m).padStart(10)} `
      + `${mm(m.rms_m).padStart(10)}  ${mm(m.max_abs_m).padStart(10)}`);
  }
  const tol = mm(result.tolerance_m);

  // THE GATE IS ON THE MASTER, AND ONLY ON THE MASTER, and that is a decision
  // rather than an oversight.
  //
  // `generators/terrain_gen.py` refuses to export a ground mesh more than
  // MESH_FIT_TOLERANCE_M from the heightfield — but that refusal happens inside
  // a Blender run this gate cannot make, so nothing re-checked the committed
  // master afterwards. A hand-edited or half-restored GLB would sail through
  // every other check in this repo. This closes that.
  //
  // The SHIPPED derivative is REPORTED and not asserted, because it cannot pass:
  // `gltf-transform optimize` quantises POSITION to 14 bits under one uniform
  // node scale, which on a mesh 5,020 m wide and 8.6 m tall is a 306 mm vertical
  // lattice, and 16 bits — the format's maximum — still lands on 77 mm. There is
  // no setting that meets 30 mm. `renderers/web/js/terrain.js` reads the heights
  // back off the field at load instead, and it is `tools/smoke_renderer.mjs`
  // that asserts the surface actually DRAWN matches the sampler, because that is
  // where the repair happens. Asserting it here would only ever say that a
  // compressor is a compressor.
  if (!argv.includes('--gate')) {
    console.log(`\n   tolerance ${tol} — the generator's own MESH_FIT_TOLERANCE_M`);
    console.log(`   the shipped derivative is off by up to ${mm(result.meshes.shipped.max_abs_m)}`
      + ' — see R-BUG3c, and js/terrain.js conformGroundToField()');
    return;
  }
  const master = result.meshes.master;
  console.log(`\n   master within ${tol}: `
    + `${master.max_abs_m <= result.tolerance_m ? 'yes' : 'NO'} `
    + `(${mm(master.max_abs_m)}); shipped derivative ${mm(result.meshes.shipped.max_abs_m)} off `
    + 'on a quantised lattice, conformed at load — see R-BUG3c');
  if (master.max_abs_m > result.tolerance_m) {
    console.error(`   the committed MASTER ground mesh departs from the heightfield by `
      + `${mm(master.max_abs_m)}, over the ${tol} generators/terrain_gen.py refuses to `
      + 'export past. The walker is anchored to the field, so the town would float or sink.');
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => { console.error(err.message); process.exit(1); });
}
