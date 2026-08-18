/**
 * yard.js — the goods a working town left standing on its own ground.
 *
 * WHY THIS FILE EXISTS. `docs/ROADMAP.md` K5 (c) asks for *"crates and barrels
 * at the stores"* and *"wagons/drays"*, and ticket T-0040 is that clause for
 * the taverns and the stores. Unlike the signboards one layer over, it does not
 * start from silence: the village corporation's **Ordinance 9 of 7 November
 * 1833** is about timber, stone, brick, boxes and barrels stacked in the
 * streets, and a corporation does not legislate against a thing nobody does.
 * What the ordinance gives is the treatment and no location at all, so
 * `tools/generate_yard_goods.py` answers "which frontage" with a rule,
 * `tools/check.sh` re-derives its record byte for byte, and this file only
 * draws what that record says.
 *
 * WHAT IT WILL AND WILL NOT DO.
 *
 *  * It stands its goods on the TERRAIN, not on a building's wall base. A
 *    barrel on a footway rests on the ground it is standing on, so each object
 *    samples `terrain.surfaceHeight` at its own point — which is the opposite
 *    of `signage.js`, where a board must hang off the same datum as the wall it
 *    is bolted to or it floats. Two layers, two right answers.
 *  * It draws no mark, brand, stencil or label. Not on any barrel or case,
 *    ever. L25 decided that for the one documented sign in this town, L130
 *    generalised it to two dozen boards, and it generalises again with force:
 *    nothing this project holds says what was in any barrel in Chicago on this
 *    date, still less whose it was.
 *  * It is ONE draw call for the whole layer, like the fences and the boards.
 *  * It marks itself. Every vertex carries `_confidence` at `reconstructed`,
 *    because the FACT of goods on these frontages is reconstructed — the
 *    weakest thing deciding that the vertex exists at all. So the whole layer
 *    disappears when a visitor hides `reconstructed`, and the town goes back to
 *    standing on swept ground. That is the truthful behaviour.
 *  * It answers a pick. A barrel belongs to the business whose door it stands
 *    at, so clicking it opens that business's card — the same contract the
 *    signboards keep.
 *  * It draws NO PEOPLE, and the bench at the Green Tree is where that bites.
 *    The Trowbridge view of that inn shows a bench of SITTERS against its front
 *    wall; AGENTS.md's standing constraint is not relaxed by a plate, so what is
 *    taken from the picture is the bench and the sitters stay reference. A bench
 *    with nobody on it is the honest half of that image.
 */

import * as THREE from 'three';

/** attested · inferred · reconstructed, as the confidence view reads them. */
const LEVEL = { attested: 0, documented: 0, inferred: 0.5, reconstructed: 1 };

/**
 * THE OBJECTS' SECTIONS, AND WHY THESE NUMBERS ARE SPLIT THE WAY THEY ARE. The
 * record owns everything that is a CLAIM — a barrel's height and girth, a case's
 * size, the wagon's body and wheels are all in `form`, graded and noted there,
 * because they are inventions about the town. What is here is only how those
 * numbers are turned into triangles: how many staves a barrel is drawn with, how
 * many spokes a wheel gets, how thick a rim is. Those are the renderer's, the
 * same division `enclosures.js` makes between a fence's line and a rail's
 * thickness, and a visitor who hides `reconstructed` loses all of it either way.
 */
const BARREL_SIDES = 10;
const WHEEL_SIDES = 12;
const WHEEL_SPOKES = 6;
const WHEEL_RIM_M = 0.09;    // the felloe's radial depth
const WHEEL_T_M = 0.07;      // the tyre's width
const HUB_R_M = 0.09;
const SPOKE_T_M = 0.032;
const AXLE_T_M = 0.05;
const TONGUE_T_M = 0.055;

/**
 * The layer's own timber tone, and it is deliberately NOT the fence's. The
 * enclosures are weathered post-and-rail at 0x8d8272 and the boards are the
 * archetype's silvered plank; a cask and a packing case are newer wood, out of a
 * cooperage or off a schooner, so they read a shade warmer and darker. Like
 * `signage.js`'s note: `ColorManagement.enabled` is true and `setHex` reads
 * sRGB, so this is the hex, not a linear triple copied from a generator.
 */
const GOODS_COLOUR = 0x8a7a5f;

/* -------------------------------------------------------------------------- */
/* primitives                                                                  */
/* -------------------------------------------------------------------------- */

/**
 * One box, 12 triangles, flat-shaded from its own face normals. `u` is the
 * horizontal unit vector along the box's length; up is world Y always.
 * Deliberately the same helper shape as the enclosure and signage layers' —
 * three layers drawing small timber the same way is one thing to reason about.
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

function tri(buf, a, b, c, n, level) {
  for (const p of [a, b, c]) {
    buf.pos.push(p[0], p[1], p[2]);
    buf.nrm.push(n[0], n[1], n[2]);
    buf.conf.push(level);
  }
}

/**
 * A barrel: two frusta belly to belly, so the staves bow the way a coopered cask
 * has to bow, plus its two heads. `axis` is a unit vector — up for a barrel
 * standing on its head, horizontal for one laid on its side — and `right` is any
 * unit vector across it.
 *
 * `sides` staves gives 4·sides side triangles and 2·(sides−2) head triangles;
 * at 10 that is 56 for a whole barrel, which is what lets a hundred and fifty of
 * them cost less than one building.
 */
function pushBarrel(buf, cx, cy, cz, axis, right, len, bellyR, headR, level) {
  const [ax, ay, az] = axis;
  const [rx, ry, rz] = right;
  // the third axis of the frame, right × axis
  const sx = ry * az - rz * ay;
  const sy = rz * ax - rx * az;
  const sz = rx * ay - ry * ax;
  const at = (t, r, k) => [
    cx + ax * t + (rx * Math.cos(k) + sx * Math.sin(k)) * r,
    cy + ay * t + (ry * Math.cos(k) + sy * Math.sin(k)) * r,
    cz + az * t + (rz * Math.cos(k) + sz * Math.sin(k)) * r,
  ];
  const half = len / 2;
  const ring = (t, r) => {
    const out = [];
    for (let i = 0; i < BARREL_SIDES; i += 1) {
      out.push(at(t, r, (i / BARREL_SIDES) * Math.PI * 2));
    }
    return out;
  };
  const lo = ring(-half, headR);
  const mid = ring(0, bellyR);
  const hi = ring(half, headR);
  const nOf = (p, t) => {
    const dx = p[0] - (cx + ax * t);
    const dy = p[1] - (cy + ay * t);
    const dz = p[2] - (cz + az * t);
    const L = Math.hypot(dx, dy, dz) || 1;
    return [dx / L, dy / L, dz / L];
  };
  for (let i = 0; i < BARREL_SIDES; i += 1) {
    const j = (i + 1) % BARREL_SIDES;
    for (const [a, b] of [[lo, mid], [mid, hi]]) {
      tri(buf, a[i], b[i], b[j], nOf(b[i], 0), level);
      tri(buf, a[i], b[j], a[j], nOf(a[i], 0), level);
    }
  }
  for (const [ringPts, sign] of [[lo, -1], [hi, 1]]) {
    const n = [ax * sign, ay * sign, az * sign];
    for (let i = 1; i < BARREL_SIDES - 1; i += 1) {
      if (sign > 0) tri(buf, ringPts[0], ringPts[i], ringPts[i + 1], n, level);
      else tri(buf, ringPts[0], ringPts[i + 1], ringPts[i], n, level);
    }
  }
}

/**
 * A cart wheel, standing in the plane across `axle` (a unit vector along the
 * hub). It is drawn as a RIM — an annulus you can see through — plus spokes and
 * a hub, and the see-through is the whole point: a solid disc reads as a
 * millstone, and the one wagon in this town should not be the object a visitor
 * remembers for being wrong.
 */
function pushWheel(buf, cx, cy, cz, axle, radius, level) {
  const [ax, ay, az] = axle;
  // a frame across the axle; the wheel stands upright, so up is one of its axes
  const ux = -az;
  const uz = ax;
  const uL = Math.hypot(ux, uz) || 1;
  const rx = ux / uL;
  const rz = uz / uL;
  const at = (r, k, t) => [
    cx + rx * Math.cos(k) * r + ax * t,
    cy + Math.sin(k) * r + ay * t,
    cz + rz * Math.cos(k) * r + az * t,
  ];
  const half = WHEEL_T_M / 2;
  const inner = radius - WHEEL_RIM_M;
  for (let i = 0; i < WHEEL_SIDES; i += 1) {
    const k0 = (i / WHEEL_SIDES) * Math.PI * 2;
    const k1 = ((i + 1) / WHEEL_SIDES) * Math.PI * 2;
    const nOut = [rx * Math.cos((k0 + k1) / 2), Math.sin((k0 + k1) / 2),
      rz * Math.cos((k0 + k1) / 2)];
    const nIn = [-nOut[0], -nOut[1], -nOut[2]];
    // tyre
    tri(buf, at(radius, k0, -half), at(radius, k0, half), at(radius, k1, half), nOut, level);
    tri(buf, at(radius, k0, -half), at(radius, k1, half), at(radius, k1, -half), nOut, level);
    // the felloe's inside face
    tri(buf, at(inner, k0, -half), at(inner, k1, half), at(inner, k0, half), nIn, level);
    tri(buf, at(inner, k0, -half), at(inner, k1, -half), at(inner, k1, half), nIn, level);
    // the two side rings
    for (const [t, n] of [[half, [ax, ay, az]], [-half, [-ax, -ay, -az]]]) {
      const a = at(inner, k0, t);
      const b = at(radius, k0, t);
      const c = at(radius, k1, t);
      const d = at(inner, k1, t);
      if (t > 0) { tri(buf, a, b, c, n, level); tri(buf, a, c, d, n, level); } else {
        tri(buf, a, c, b, n, level); tri(buf, a, d, c, n, level);
      }
    }
  }
  // ONE SPOKE BOX SPANS THE WHEEL, so six boxes give twelve spokes' worth of
  // timber for half the triangles — a wheel is symmetrical and nobody counts.
  // Built by hand rather than with `pushBox`: a spoke's long axis is not
  // horizontal and `pushBox`'s `u` is.
  for (let i = 0; i < WHEEL_SPOKES; i += 1) {
    const k = (i / WHEEL_SPOKES) * Math.PI;
    const ck = Math.cos(k);
    const sk = Math.sin(k);
    const d = [rx * ck, sk, rz * ck];              // along the spoke, unit
    const q = [-rx * sk, ck, -rz * sk];            // across it, in the wheel plane
    const half3 = SPOKE_T_M / 2;
    const L = inner;
    const corners = [];
    for (const s of [-1, 1]) {
      for (const a2 of [-1, 1]) {
        for (const b2 of [-1, 1]) {
          corners.push([
            cx + d[0] * s * L + q[0] * a2 * half3 + ax * b2 * half3,
            cy + d[1] * s * L + q[1] * a2 * half3 + ay * b2 * half3,
            cz + d[2] * s * L + q[2] * a2 * half3 + az * b2 * half3,
          ]);
        }
      }
    }
    const face = (i0, i1, i2, i3, n) => {
      tri(buf, corners[i0], corners[i1], corners[i2], n, level);
      tri(buf, corners[i0], corners[i2], corners[i3], n, level);
    };
    face(0, 1, 3, 2, [-q[0], -q[1], -q[2]]);
    face(4, 6, 7, 5, q);
    face(0, 4, 5, 1, [-d[0], -d[1], -d[2]]);
    face(2, 3, 7, 6, d);
  }
  // the hub
  pushBarrel(buf, cx, cy, cz, axle, [rx, 0, rz], WHEEL_T_M * 2.2, HUB_R_M, HUB_R_M * 0.8,
    level);
}

/* -------------------------------------------------------------------------- */
/* the objects                                                                 */
/* -------------------------------------------------------------------------- */

/** The ground under a point, or null when the terrain has nothing there. */
function groundAt(terrain, e, n) {
  const y = terrain.surfaceHeight(e, n);
  return Number.isFinite(y) ? y : null;
}

function buildItem(buf, item, form, terrain, level, problems, who) {
  const at = item.at_local_enu_m;
  if (!Array.isArray(at) || at.length !== 2) return false;
  const base = groundAt(terrain, at[0], at[1]);
  if (base === null) {
    problems.push(`yard: ${who} has no ground under its ${item.kind} — it is not drawn`);
    return false;
  }
  // world is (E, up, -N); the record's bearing is a compass bearing, so along the
  // wall is (cos b, -sin b) in ENU and out of it is (sin b, cos b).
  const b = ((item.bearing_deg ?? 0) * Math.PI) / 180;
  const wx = Math.cos(b);
  const wz = Math.sin(b);
  const x = at[0];
  const z = -at[1];

  if (item.kind === 'barrel') {
    const h = form.barrelHeight;
    const belly = form.barrelBelly / 2;
    const head = form.barrelHead / 2;
    if (item.pose === 'laid') {
      // an empty put back out, lying ALONG the wall and out of the way rather
      // than across the footway: the axis is the along-wall direction.
      pushBarrel(buf, x, base + belly, z, [wx, 0, wz], [0, 1, 0], h, belly, head, level);
    } else {
      pushBarrel(buf, x, base + h / 2, z, [0, 1, 0], [wx, 0, wz], h, belly, head, level);
    }
    return true;
  }
  if (item.kind === 'bench') {
    // A backless plank bench standing against a wall: a seat plank on two plank
    // ends. `at` is its centre and the record puts that half the seat's depth off
    // the wall plane, so the back edge touches the boards.
    const [L, D, H] = form.bench;
    const t = form.benchPlank;
    pushBox(buf, x, base + H - t / 2, z, wx, wz, L / 2, D / 2, t / 2, level);
    // the two ends, inset so the seat overhangs them the way a bench's does
    const endInset = Math.min(0.14, L / 8);
    for (const s2 of [-1, 1]) {
      pushBox(buf, x + wx * s2 * (L / 2 - endInset), base + (H - t) / 2,
        z + wz * s2 * (L / 2 - endInset), wx, wz, t / 2, (D * 0.82) / 2, (H - t) / 2,
        level);
    }
    return true;
  }
  if (item.kind === 'crate') {
    const [l, w, hh] = form.crate;
    const tier = item.tier || 0;
    const s = tier === 0 ? 1 : form.crate2Scale;
    const y = base + (tier === 0 ? hh / 2 : hh + (hh * s) / 2);
    pushBox(buf, x, y, z, wx, wz, (l * s) / 2, (w * s) / 2, (hh * s) / 2, level);
    return true;
  }
  return false;
}

function buildWagon(buf, wagon, form, terrain, level, problems) {
  const at = wagon.at_local_enu_m;
  if (!Array.isArray(at) || at.length !== 2) return false;
  const base = groundAt(terrain, at[0], at[1]);
  if (base === null) {
    problems.push(`yard: ${wagon.id} has no ground under it — no wagon is drawn`);
    return false;
  }
  const b = ((wagon.bearing_deg ?? 0) * Math.PI) / 180;
  // along the wagon, and across it, in the renderer's world axes
  const fx = Math.sin(b);
  const fz = -Math.cos(b);
  const sx = Math.cos(b);
  const sz = Math.sin(b);
  const x = at[0];
  const z = -at[1];
  const [L, W, H] = form.wagonBody;
  const bed = base + form.wagonBedY;

  // the body: a plank floor and four sides, so a visitor looking down into it
  // sees a wagon box and not a solid block.
  pushBox(buf, x, bed, z, fx, fz, L / 2, W / 2, 0.035, level);
  for (const s of [-1, 1]) {
    pushBox(buf, x + sx * s * (W / 2), bed + H / 2, z + sz * s * (W / 2),
      fx, fz, L / 2, 0.03, H / 2, level);
    pushBox(buf, x + fx * s * (L / 2), bed + H / 2, z + fz * s * (L / 2),
      sx, sz, W / 2, 0.03, H / 2, level);
  }
  // the two axles and their wheels
  const pairs = [
    [-L / 2 + 0.35, form.wagonRearWheel / 2],
    [L / 2 - 0.35, form.wagonFrontWheel / 2],
  ];
  for (const [along, r] of pairs) {
    const axY = base + r;
    pushBox(buf, x + fx * along, axY, z + fz * along, sx, sz,
      W / 2 + WHEEL_T_M, AXLE_T_M / 2, AXLE_T_M / 2, level);
    for (const s of [-1, 1]) {
      pushWheel(buf,
        x + fx * along + sx * s * (W / 2 + WHEEL_T_M),
        axY,
        z + fz * along + sz * s * (W / 2 + WHEEL_T_M),
        [sx * s, 0, sz * s], r, level);
    }
  }
  // the tongue, down to the ground at its far end because nothing is hitched to it
  const tipAlong = L / 2 + form.wagonTongue;
  const tipY = base + 0.06;
  const rootY = base + form.wagonFrontWheel / 2;
  const midAlong = (L / 2 + tipAlong) / 2;
  const midY = (tipY + rootY) / 2;
  // Drawn as a box along the horizontal projection, deep enough to span the drop
  // from the front axle to the ground: a tongue is a stick, and a stick's exact
  // inclination is not a claim this record makes.
  pushBox(buf, x + fx * midAlong, midY, z + fz * midAlong, fx, fz,
    form.wagonTongue / 2, TONGUE_T_M / 2,
    Math.max(TONGUE_T_M / 2, (rootY - tipY) / 2), level);
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

/** The record's `form` block, read once so no draw reaches into the JSON. */
function readForm(record) {
  const f = record?.form ?? {};
  const v = (k, fallback) => (f[k]?.value ?? fallback);
  const crate = v('crate_size_m', [1.05, 0.72, 0.62]);
  const body = v('wagon_body_m', [3.05, 1.07, 0.55]);
  return {
    barrelHeight: v('barrel_height_m', 0.84),
    barrelBelly: v('barrel_belly_diameter_m', 0.53),
    barrelHead: v('barrel_head_diameter_m', 0.45),
    crate,
    crate2Scale: 0.72,
    wagonBody: body,
    wagonBedY: 0.95,
    wagonRearWheel: 1.37,
    wagonFrontWheel: 1.07,
    wagonTongue: 2.75,
    bench: v('bench_size_m', [1.83, 0.36, 0.46]),
    benchPlank: v('bench_plank_m', 0.045),
  };
}

/**
 * @param {object} o dataBase (data/ root) · terrain · confidence · problems
 * @returns {Promise<{group: THREE.Group, records: object[], census: object,
 *                    pickAt: function, dispose: function}>}
 */
export async function createYardGoods({
  dataBase, terrain, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'yard';
  const out = {
    group,
    records: [],
    frontages: [],
    wagons: [],
    benches: [],
    census: { records: 0, frontages: 0, objects: 0, barrels: 0, crates: 0, wagons: 0,
      benches: 0, refused: 0 },
    pickAt: () => null,
    dispose: () => {},
  };

  if (!dataBase || !terrain) {
    problems.push('yard: no data base or no terrain — nothing is stood out');
    return out;
  }
  let index;
  try {
    index = await getJSON(new URL('yard/index.json', dataBase));
  } catch (err) {
    // Degrade to NOTHING drawn plus a recorded problem, never to an invented
    // barrel: the same contract the enclosure, signage and vegetation layers keep.
    problems.push(`yard: ${err.message} — no goods are stood out`);
    return out;
  }
  const wanted = Array.isArray(index.yard) ? index.yard : [];
  const loaded = await Promise.all(wanted.map(async (y) => {
    if (!y.file) return [y.id, null, 'the manifest gave no file'];
    try {
      return [y.id, await getJSON(new URL(`yard/${y.file}`, dataBase)), null];
    } catch (err) { return [y.id, null, err.message]; }
  }));

  const buf = { pos: [], nrm: [], conf: [] };
  /**
   * WHICH BUSINESS A TRIANGLE BELONGS TO. The layer is one draw call, so a hit
   * on the mesh knows nothing about which barrel it landed on unless each
   * frontage banks the half-open range of triangles it emitted — the same span
   * table `signage.js` keeps, and for the same reason.
   */
  const spans = [];
  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`yard: ${id} — ${why}`); continue; }
    out.records.push(record);
    out.census.records += 1;
    out.census.refused += (record.refused ?? []).length;
    const form = readForm(record);
    const level = LEVEL[record.existence?.confidence] ?? 1;
    for (const frontage of record.frontages ?? []) {
      const from = buf.pos.length / 9;
      let drew = 0;
      for (const item of frontage.items ?? []) {
        if (!buildItem(buf, item, form, terrain, LEVEL[frontage.confidence] ?? level,
          problems, frontage.structure_id)) continue;
        drew += 1;
        out.census.objects += 1;
        if (item.kind === 'barrel') out.census.barrels += 1;
        if (item.kind === 'crate') out.census.crates += 1;
      }
      if (!drew) continue;
      spans.push({ id: frontage.structure_id, from, to: buf.pos.length / 9 });
      out.frontages.push(frontage);
      out.census.frontages += 1;
    }
    for (const wagon of record.wagons ?? []) {
      const from = buf.pos.length / 9;
      if (!buildWagon(buf, wagon, form, terrain, LEVEL[wagon.confidence] ?? level,
        problems)) continue;
      // A wagon standing in a yard belongs to the building whose yard it is, so a
      // pick on it opens that card. `belongs_to` names it; without one the wagon
      // is unpickable and the aim falls through, which is the fences' behaviour.
      if (wagon.belongs_to) {
        spans.push({ id: wagon.belongs_to, from, to: buf.pos.length / 9 });
      }
      out.wagons.push(wagon);
      out.census.wagons += 1;
      out.census.objects += 1;
    }
    for (const bench of record.benches ?? []) {
      const from = buf.pos.length / 9;
      if (!buildItem(buf, bench, form, terrain, LEVEL[bench.confidence] ?? level,
        problems, bench.belongs_to ?? bench.id)) continue;
      // Same pick contract as the wagons: a bench against an inn's front wall
      // belongs to that inn, so aiming at it opens the inn's card.
      if (bench.belongs_to) {
        spans.push({ id: bench.belongs_to, from, to: buf.pos.length / 9 });
      }
      out.benches.push(bench);
      out.census.benches += 1;
      out.census.objects += 1;
    }
  }
  if (!buf.pos.length) {
    if (out.census.records) {
      problems.push('yard: the records loaded and not one object was stood out');
    }
    return out;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(buf.nrm, 3));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.computeBoundingSphere();

  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(GOODS_COLOUR), roughness: 0.88, metalness: 0.0,
  });
  mat.name = 'yard-goods-timber';
  confidence?.patch(mat);
  /**
   * ITS OWN PROGRAM CACHE KEY, AND WHY THIS LINE IS NOT OPTIONAL. three caches a
   * compiled program under a key ending in `material.customProgramCacheKey()`,
   * whose default is the SOURCE TEXT of `onBeforeCompile` — so every material
   * `confidence.patch()` touches reports the same key, and two patched materials
   * that agree on their other program parameters share one program. The
   * enclosure layer was drawn in solid black by a building's shader that way,
   * with no page error and no warning. This layer is the same shape of material
   * and would walk into the same collision; ticket T-0053 is the general fix.
   */
  mat.customProgramCacheKey = () => 'chicago4d-yard-goods-timber';

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'yard';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  group.userData.census = out.census;

  const raycaster = new THREE.Raycaster();
  /** The business these goods stand at, or null. Same ray budget as the boards. */
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
