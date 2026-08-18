/**
 * signage.js — the boards the town's businesses hung out over the footway.
 *
 * WHY THIS FILE EXISTS. `docs/ROADMAP.md` K5 (b) asked for signboards on the
 * businesses and pointed at the archetype parameter that draws one. That
 * parameter is Blender's, so every board it hangs waits on a bake — and the
 * town has had exactly ONE board since the day the parameter was written,
 * because exactly one record attests a sign (the Wolf Point Tavern's painted
 * wolf, docs/LIBERTIES.md L25).
 *
 * A board is a plank on a bracket hanging off a wall this project has already
 * drawn. Its position is arithmetic on the committed footprint and placement.
 * So the same argument that lets `enclosures.js` draw a fence from a perimeter
 * lets this draw a signboard from a facade: no GLB, no `assets/`, no nightly.
 * `tools/generate_business_signboards.py` does the arithmetic and the choosing,
 * `tools/check.sh` re-derives its record byte for byte, and this file only
 * draws what that record says.
 *
 * WHAT IT WILL AND WILL NOT DO.
 *
 *  * It hangs on the same datum as the wall. A board's height is measured from
 *    the base of the building's walls, and `buildings.js` puts that base at the
 *    LOWEST terrain sample under the footprint — so this samples the same 5×5
 *    grid over the same quad. Any other rule and a board on sloping ground
 *    would float off its own wall.
 *  * It draws no lettering, no image, no trade device. Not on any board, ever.
 *    L25 decided that for the one documented sign in the town and the reason
 *    generalises with force: no source gives the wording of a single Chicago
 *    sign of these years, and two dozen invented shop names would be the most
 *    conspicuous fiction in the scene.
 *  * It is ONE draw call for the whole layer, like the fences: a board is five
 *    small boxes and two dozen boards are not two dozen draws.
 *  * It marks itself. Every vertex carries `_confidence` at `reconstructed`,
 *    because the FACT of a board on these frontages is reconstructed — the
 *    weakest thing deciding that the vertex exists at all. So the whole layer
 *    disappears when a visitor hides `reconstructed`, and the town goes back to
 *    being mute. That is the truthful behaviour.
 *  * It answers a pick. A board belongs to a business with a card behind it, so
 *    clicking the sign opens the shop — which is what a sign is FOR.
 */

import * as THREE from 'three';

/** attested · inferred · reconstructed, as the confidence view reads them. */
const LEVEL = { attested: 0, documented: 0, inferred: 0.5, reconstructed: 1 };

/**
 * THE BOARD, AND WHY THESE NUMBERS ARE HERE. Arm length, board size and the two
 * hangers are how a board is DRAWN, not a claim about any shop — the division
 * `enclosures.js` makes between a fence's line (the record's) and a rail's
 * thickness (the renderer's). They are the wolf sign's own geometry, copied from
 * `generators/archetypes/log_dwelling.py::_sign`, so the town has one convention
 * for hanging a board rather than two. The record owns the anchor, the bearing
 * and the height.
 */
const ARM_M = 1.15;
const ARM_T_M = 0.045;
const BOARD_W_M = 0.88;
const BOARD_H_M = 0.50;
const BOARD_T_M = 0.05;
const DROP_M = 0.20;
const HANGER_T_M = 0.022;
const HANGER_W_M = 0.018;

/**
 * The archetype's own `SIGN_RGBA`, converted rather than copied. The generator
 * writes glTF `baseColorFactor`, which is LINEAR, at (0.60, 0.54, 0.44);
 * `THREE.Color.setHex` reads sRGB and `ColorManagement.enabled` is true, so the
 * hex that lands on the same linear triple is this one. Copying 0x998a70
 * straight across would have hung a board two stops darker than the wolf sign
 * beside it — see the same trap called out in `trees.js`. Blank: L25.
 */
const SIGN_COLOUR = 0xcbc2b1;

/**
 * One box, 12 triangles, flat-shaded from its own face normals. `u` is the
 * horizontal unit vector along the box's length; up is world Y always.
 * Deliberately the same helper shape as the enclosure layer's — two layers
 * drawing small timber the same way is one thing to reason about, not two.
 */
function pushBox(buf, cx, cy, cz, ux, uz, halfLen, halfW, halfH, level) {
  const vx = -uz;
  const vz = ux;
  const P = (a, b, c) => [
    cx + ux * a * halfLen + vx * b * halfW,
    cy + c * halfH,
    cz + uz * a * halfLen + vz * b * halfW,
  ];
  const p = [
    P(-1, -1, -1), P(1, -1, -1), P(1, 1, -1), P(-1, 1, -1),
    P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1),
  ];
  const faces = [
    [[1, 5, 6], [1, 6, 2], [ux, 0, uz]],
    [[4, 0, 3], [4, 3, 7], [-ux, 0, -uz]],
    [[3, 2, 6], [3, 6, 7], [vx, 0, vz]],
    [[0, 4, 5], [0, 5, 1], [-vx, 0, -vz]],
    [[4, 7, 6], [4, 6, 5], [0, 1, 0]],
    [[0, 1, 2], [0, 2, 3], [0, -1, 0]],
  ];
  for (const [t1, t2, n] of faces) {
    for (const tri of [t1, t2]) {
      for (const i of tri) {
        buf.pos.push(p[i][0], p[i][1], p[i][2]);
        buf.nrm.push(n[0], n[1], n[2]);
        buf.conf.push(level);
      }
    }
  }
}

/**
 * The base of this building's walls, by the rule `buildings.js` uses: the LOWEST
 * of a 5×5 grid of terrain samples over the footprint. Bilinear over the quad
 * the record carries, which is the footprint's bounding box already turned into
 * local ENU, so nothing here re-does the placement arithmetic the generator did.
 */
function wallBase(quad, terrain) {
  if (!Array.isArray(quad) || quad.length !== 4) return null;
  const [a, b, c, d] = quad;
  let lowest = Infinity;
  const STEPS = 4;
  for (let i = 0; i <= STEPS; i += 1) {
    const s = i / STEPS;
    for (let j = 0; j <= STEPS; j += 1) {
      const t = j / STEPS;
      const e = (a[0] * (1 - s) + b[0] * s) * (1 - t) + (d[0] * (1 - s) + c[0] * s) * t;
      const n = (a[1] * (1 - s) + b[1] * s) * (1 - t) + (d[1] * (1 - s) + c[1] * s) * t;
      const y = terrain.surfaceHeight(e, n);
      if (Number.isFinite(y)) lowest = Math.min(lowest, y);
    }
  }
  return Number.isFinite(lowest) ? lowest : null;
}

/**
 * One signboard: the bracket arm out of the wall, its strut, two hangers and the
 * board. Returns true if it drew.
 *
 * The frame, for anyone checking the arithmetic against docs/GLB-CONTRACT.md:
 * the record's `facade_bearing_deg` is a compass bearing, so the outward normal
 * is (sin b, cos b) in ENU and the along-wall direction is (cos b, −sin b). The
 * renderer's world is (E, up, −N), which is where every negated north below
 * comes from.
 */
function buildSign(buf, sign, terrain, problems) {
  const anchor = sign.anchor_local_enu_m;
  if (!Array.isArray(anchor) || anchor.length !== 2) {
    problems.push(`signage: ${sign.structure_id} carries no anchor — no board is hung`);
    return false;
  }
  const base = wallBase(sign.ground_quad_local_enu_m, terrain);
  if (base === null) {
    problems.push(`signage: ${sign.structure_id} has no ground under its footprint — `
      + 'no board is hung');
    return false;
  }
  const level = LEVEL[sign.confidence] ?? 1;
  const b = ((sign.facade_bearing_deg ?? 0) * Math.PI) / 180;
  // Out of the wall, and along it. Both in the renderer's world axes.
  const ox = Math.sin(b);
  const oz = -Math.cos(b);
  const wx = Math.cos(b);
  const wz = Math.sin(b);
  const ax = anchor[0];
  const az = -anchor[1];
  const y = base + (sign.arm_height_m ?? 2.55);

  // The arm, springing from the wall face and running out along the normal.
  pushBox(buf, ax + ox * (ARM_M / 2), y + ARM_T_M, az + oz * (ARM_M / 2),
    ox, oz, ARM_M / 2, ARM_T_M, ARM_T_M, level);
  // The strut under it, a shorter diagonal-ish brace kept slim on purpose: an
  // earlier bracket in this project read as the object with a board attached
  // rather than the other way round. On a shop the board is the point.
  pushBox(buf, ax + ox * 0.30, y - 0.19, az + oz * 0.30,
    ox, oz, 0.30, ARM_T_M * 0.6, ARM_T_M * 0.6, level);
  // Two hangers dropping from near the arm's outer end.
  const hang = ARM_M * 0.72;
  for (const s of [-1, 1]) {
    pushBox(buf,
      ax + ox * hang + wx * s * BOARD_W_M * 0.32,
      y - DROP_M / 2,
      az + oz * hang + wz * s * BOARD_W_M * 0.32,
      ox, oz, HANGER_T_M, HANGER_W_M, DROP_M / 2, level);
  }
  // The board. Its long axis runs ALONG the wall and its face looks out of it,
  // which is how the wolf sign is built and how a board is read from the street.
  pushBox(buf,
    ax + ox * hang, y - DROP_M - BOARD_H_M / 2, az + oz * hang,
    wx, wz, BOARD_W_M / 2, BOARD_T_M / 2, BOARD_H_M / 2, level);
  return true;
}

/* -------------------------------------------------------------------------- */
/* the layer                                                                   */
/* -------------------------------------------------------------------------- */

async function getJSON(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
}

/**
 * @param {object} o dataBase (data/ root) · terrain · confidence · problems
 * @returns {Promise<{group: THREE.Group, records: object[], census: object,
 *                    pickAt: function, dispose: function}>}
 */
export async function createSignage({
  dataBase, terrain, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'signage';
  const out = {
    group,
    records: [],
    signs: [],
    census: { records: 0, boards: 0, refused: 0 },
    pickAt: () => null,
    dispose: () => {},
  };

  if (!dataBase || !terrain) {
    problems.push('signage: no data base or no terrain — no board is hung');
    return out;
  }
  let index;
  try {
    index = await getJSON(new URL('signage/index.json', dataBase));
  } catch (err) {
    // Degrade to NOTHING drawn plus a recorded problem, never to an invented
    // board: the same contract the enclosure and vegetation layers keep.
    problems.push(`signage: ${err.message} — no signboard is hung`);
    return out;
  }
  const wanted = Array.isArray(index.signage) ? index.signage : [];
  const loaded = await Promise.all(wanted.map(async (s) => {
    if (!s.file) return [s.id, null, 'the manifest gave no file'];
    try {
      return [s.id, await getJSON(new URL(`signage/${s.file}`, dataBase)), null];
    } catch (err) { return [s.id, null, err.message]; }
  }));

  const buf = { pos: [], nrm: [], conf: [] };
  /**
   * WHICH BUSINESS A TRIANGLE BELONGS TO. The layer is one draw call, so a hit
   * on the mesh knows nothing about which board it landed on unless each board
   * banks the half-open range of triangles it emitted. Every board here has a
   * structure record behind it by construction — the rule that chose it started
   * from one — so unlike the fences there is no unpickable case.
   */
  const spans = [];
  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`signage: ${id} — ${why}`); continue; }
    out.records.push(record);
    out.census.records += 1;
    out.census.refused += (record.refused ?? []).length;
    for (const sign of record.signs ?? []) {
      const from = buf.pos.length / 9;
      if (!buildSign(buf, sign, terrain, problems)) continue;
      spans.push({ id: sign.structure_id, from, to: buf.pos.length / 9 });
      out.signs.push(sign);
      out.census.boards += 1;
    }
  }
  if (!buf.pos.length) {
    if (out.census.records) {
      problems.push('signage: the records loaded and not one board was hung');
    }
    return out;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(buf.nrm, 3));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.computeBoundingSphere();

  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(SIGN_COLOUR), roughness: 0.85, metalness: 0.0,
  });
  mat.name = 'signboard-timber';
  confidence?.patch(mat);
  /**
   * ITS OWN PROGRAM CACHE KEY, AND WHY THIS LINE IS NOT OPTIONAL. three caches a
   * compiled program under a key ending in `material.customProgramCacheKey()`,
   * whose default is the SOURCE TEXT of `onBeforeCompile` — so every material
   * `confidence.patch()` touches reports the same key, and two patched materials
   * that agree on their other program parameters share one program. The
   * enclosure layer was drawn in solid black by a building's shader that way,
   * with no page error and no warning, on the first build of that layer. This
   * layer is the same shape of material and would walk into the same collision;
   * ticket T-0053 is the general fix.
   */
  mat.customProgramCacheKey = () => 'chicago4d-signboard-timber';

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'signage';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  group.userData.census = out.census;

  const raycaster = new THREE.Raycaster();
  /** The business this board hangs on, or null. Same ray budget as the fences. */
  out.pickAt = (ndc, camera) => {
    if (!camera) return null;
    raycaster.setFromCamera(ndc ?? new THREE.Vector2(0, 0), camera);
    raycaster.far = Math.max(400, camera.position.y * 4);
    const hits = raycaster.intersectObject(mesh, false);
    if (!hits.length) return null;
    const hit = hits[0];
    const span = spans.find((sp) => hit.faceIndex >= sp.from && hit.faceIndex < sp.to);
    if (!span) return null;
    return { id: span.id, point: hit.point.clone(), distance: hit.distance };
  };

  out.dispose = () => { geo.dispose(); mat.dispose(); };
  return out;
}
