/**
 * enclosures.js — the town's fence lines, drawn from a perimeter instead of a
 * footprint.
 *
 * WHY THIS FILE EXISTS. Two liberties in docs/LIBERTIES.md have been waiting on
 * the same missing thing, and both name it in the same words. L10, the Western
 * Hotel: *"A yard is an enclosure — a fence line, two gateways and the ground
 * between them — and `outbuilding` builds a building; using it here would mean
 * calling a fence a building, which is a worse claim than the omission."* L60,
 * the estray pen: *"an enclosure archetype — post-and-rail or notched log,
 * ROOFLESS, gated, taking a perimeter rather than a footprint … it is the honest
 * fix."* Chicago's first public building was a fence, and this project could not
 * build one.
 *
 * The generator half of that fix is a Blender archetype and is not this. This is
 * the RENDERER half, and it needs no bake: an enclosure carries a polyline, a
 * fence type, a height and its gateways, so the same argument that lets
 * `streets.js` draw a wagon track and `flora.js` plant a prairie from committed
 * numbers at load lets this draw a fence. No GLB, no `assets/`, no nightly.
 *
 * WHAT IT WILL AND WILL NOT DO.
 *
 *  * It drapes. Every post samples `terrain.surfaceHeight()` at its own foot, so
 *    a fence crossing a slope steps down it. Nothing here regrades the ground
 *    and nothing here is a collision surface — the walker stands on the same
 *    heightfield it always did and walks THROUGH a fence, which is a stated
 *    shortcoming rather than an oversight (see the note in the changelog).
 *  * It refuses water. A post whose foot is in the river mask is dropped, the
 *    way `trees.js` refuses a stem below the waterline. A fence marching into
 *    the water would be a claim about a shoreline this layer knows nothing of.
 *  * It is ONE draw call for the whole layer. Posts and rails are emitted into
 *    a single non-indexed buffer, because a fence is a lot of very small boxes
 *    and eighty draw calls for eighty sticks is how a phone loses its frame.
 *  * It marks itself. Every vertex carries `_confidence`, and it carries the
 *    grade of the WEAKEST thing that decides where that vertex is — which for
 *    every fence in this dataset is the fence type, and every fence type here is
 *    invented. So the whole layer disappears when a visitor hides
 *    `reconstructed`, which is the truthful behaviour: nobody wrote down what
 *    this fence looked like.
 */

import * as THREE from 'three';

/** attested · inferred · reconstructed, as the confidence view reads them. */
const LEVEL = { attested: 0, inferred: 0.5, reconstructed: 1 };

/** Rail stock, in metres. Not a record's numbers — see the note on WOOD below. */
const RAIL_W_M = 0.09;
const RAIL_H_M = 0.13;

/**
 * THE WOOD, AND WHY IT IS NOT IN THE DATA FILE. A rail's own thickness and the
 * colour of weathered oak are the renderer's business in exactly the way a
 * building's shingle colour is the archetype's: they are how a stick is DRAWN,
 * not a claim about the yard. What the record owns — the line, the height, the
 * course count, the post rhythm, the gateways — is read from the file and
 * nothing here overrides it. The tone is the silvered end of the facade palette
 * this project already uses for unpainted board (T-0002), because a yard fence
 * is the least maintained timber on a lot.
 */
const WOOD = 0x8d8272;

/** A drop this steep between neighbouring posts is a bank, not a yard. */
const MAX_STEP_M = 1.5;

/* -------------------------------------------------------------------------- */
/* geometry                                                                    */
/* -------------------------------------------------------------------------- */

/** One box, 12 triangles, flat-shaded from its own face normals. */
function pushBox(buf, cx, cy, cz, ux, uz, halfLen, halfW, halfH, level) {
  // `u` is the horizontal unit vector along the box; `v` is horizontal and
  // perpendicular to it. Up is world Y, always: a leaning fence post is a
  // claim about ground this layer does not make.
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

/** Cumulative arc length along a local-ENU polyline. */
function measure(path) {
  const s = [0];
  for (let i = 1; i < path.length; i++) {
    const de = path[i][0] - path[i - 1][0];
    const dn = path[i][1] - path[i - 1][1];
    s.push(s[i - 1] + Math.hypot(de, dn));
  }
  return s;
}

/** The point at arc length `d` along the polyline, in local ENU. */
function at(path, s, d) {
  const t = Math.min(Math.max(d, 0), s[s.length - 1]);
  let i = 1;
  while (i < s.length - 1 && s[i] < t) i++;
  const span = s[i] - s[i - 1] || 1;
  const f = (t - s[i - 1]) / span;
  return [
    path[i - 1][0] + (path[i][0] - path[i - 1][0]) * f,
    path[i - 1][1] + (path[i][1] - path[i - 1][1]) * f,
  ];
}

/** Where along the polyline a gateway's stated centre falls. */
function arcOf(path, s, point) {
  let best = { d: 0, dist: Infinity };
  for (let i = 1; i < path.length; i++) {
    const ex = path[i - 1][0];
    const ny = path[i - 1][1];
    const dx = path[i][0] - ex;
    const dy = path[i][1] - ny;
    const len2 = dx * dx + dy * dy || 1;
    let t = ((point[0] - ex) * dx + (point[1] - ny) * dy) / len2;
    t = Math.min(Math.max(t, 0), 1);
    const dist = Math.hypot(ex + dx * t - point[0], ny + dy * t - point[1]);
    if (dist < best.dist) best = { d: s[i - 1] + t * Math.sqrt(len2), dist };
  }
  return best.d;
}

/**
 * The stretches of a run that carry fence: its whole length, minus a gap for
 * every gateway that lands on it. A gateway is a HOLE, deliberately — this
 * layer hangs no gate leaf, because no source describes one and a drawn gate
 * would be an invention on top of an invention.
 */
function stretches(path, s, gaps) {
  let spans = [[0, s[s.length - 1]]];
  for (const g of gaps) {
    const a = g.d - g.width / 2;
    const b = g.d + g.width / 2;
    const next = [];
    for (const [lo, hi] of spans) {
      if (b <= lo || a >= hi) { next.push([lo, hi]); continue; }
      if (a > lo) next.push([lo, a]);
      if (b < hi) next.push([b, hi]);
    }
    spans = next;
  }
  return spans.filter(([lo, hi]) => hi - lo > 0.2);
}

/* -------------------------------------------------------------------------- */
/* building one enclosure                                                      */
/* -------------------------------------------------------------------------- */

function buildRecord(buf, record, terrain, problems) {
  const form = record.form ?? {};
  const height = form.height_m?.value ?? 1.37;
  const courses = Math.max(1, Math.round(form.rail_courses?.value ?? 3));
  const spacing = Math.max(1, form.post_spacing_m?.value ?? 2.9);
  const postHalf = (form.post_size_m?.value ?? 0.14) / 2;
  // The weakest grade on anything that decides where a stick of this fence is.
  // In practice that is the fence type, and no fence type in this dataset is
  // anything but invented; the max is here so the day a source describes one,
  // the geometry stops claiming to be a guess.
  const level = Math.max(
    LEVEL[form.fence_type?.confidence] ?? 1,
    LEVEL[form.height_m?.confidence] ?? 1,
  );

  let posts = 0;
  let dropped = 0;
  for (const run of record.runs ?? []) {
    const path = run.path_local_enu_m;
    if (!Array.isArray(path) || path.length < 2) continue;
    const s = measure(path);
    const gaps = (record.openings ?? [])
      .map((o) => ({ d: arcOf(path, s, o.at_local_enu_m), width: o.width_m ?? 4.27, o }))
      // A gateway belongs to whichever run it actually stands on: the record
      // states a point, not a run id, so a gate that is 6 m from this line is
      // the other frontage's and must not punch a hole here.
      .filter((g) => {
        const p = at(path, s, g.d);
        return Math.hypot(p[0] - g.o.at_local_enu_m[0], p[1] - g.o.at_local_enu_m[1]) < 1.0;
      });

    for (const [lo, hi] of stretches(path, s, gaps)) {
      const n = Math.max(1, Math.round((hi - lo) / spacing));
      const step = (hi - lo) / n;
      // Post feet first, so a rail can be hung between two known heights and a
      // post standing in the river takes its rails with it.
      const feet = [];
      for (let i = 0; i <= n; i++) {
        const [e, north] = at(path, s, lo + i * step);
        if (terrain.isWater?.(e, north)) { feet.push(null); dropped++; continue; }
        feet.push({ e, n: north, y: terrain.surfaceHeight(e, north) });
      }
      for (const f of feet) {
        if (!f) continue;
        pushBox(buf, f.e, f.y + height / 2, -f.n, 1, 0,
          postHalf, postHalf, height / 2, level);
        posts++;
      }
      for (let i = 0; i < n; i++) {
        const a = feet[i];
        const b = feet[i + 1];
        if (!a || !b) continue;
        if (Math.abs(a.y - b.y) > MAX_STEP_M) { dropped++; continue; }
        const de = b.e - a.e;
        const dn = b.n - a.n;
        const len = Math.hypot(de, dn);
        if (len < 0.05) continue;
        // The renderer's world is (E, up, -N), so the along-run unit vector
        // has its north component negated with the position.
        const ux = de / len;
        const uz = -dn / len;
        for (let c = 1; c <= courses; c++) {
          const h = height * (c / courses) - RAIL_H_M / 2;
          pushBox(buf,
            (a.e + b.e) / 2, (a.y + b.y) / 2 + h, -(a.n + b.n) / 2,
            ux, uz, len / 2, RAIL_W_M / 2, RAIL_H_M / 2, level);
        }
      }
    }
  }
  if (!posts) {
    problems.push(`enclosures: ${record.id} drew nothing — every post stood in water `
      + 'or the record carries no run with two points');
  }
  return { posts, dropped };
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
 *                    dispose: function}>}
 */
export async function createEnclosures({
  dataBase, terrain, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'enclosures';
  const out = { group, records: [], census: { enclosures: 0, posts: 0, dropped: 0 },
    dispose: () => {} };

  if (!dataBase || !terrain) {
    problems.push('enclosures: no data base or no terrain — no fence is drawn');
    return out;
  }
  let index;
  try {
    index = await getJSON(new URL('enclosures/index.json', dataBase));
  } catch (err) {
    // Degrade to NOTHING drawn plus a recorded problem, never to an invented
    // fence: the same contract the vegetation layers keep.
    problems.push(`enclosures: ${err.message} — no fence, yard or pen is drawn`);
    return out;
  }
  const wanted = Array.isArray(index.enclosures) ? index.enclosures : [];
  const loaded = await Promise.all(wanted.map(async (e) => {
    if (!e.file) return [e.id, null, 'the manifest gave no file'];
    try {
      return [e.id, await getJSON(new URL(`enclosures/${e.file}`, dataBase)), null];
    } catch (err) { return [e.id, null, err.message]; }
  }));

  const buf = { pos: [], nrm: [], conf: [] };
  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`enclosures: ${id} — ${why}`); continue; }
    const { posts, dropped } = buildRecord(buf, record, terrain, problems);
    out.records.push(record);
    out.census.enclosures++;
    out.census.posts += posts;
    out.census.dropped += dropped;
  }
  if (!buf.pos.length) return out;

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(buf.nrm, 3));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.computeBoundingSphere();

  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(WOOD), roughness: 0.92, metalness: 0.0,
  });
  mat.name = 'enclosure-timber';
  confidence?.patch(mat);
  /**
   * THE PROGRAM CACHE KEY, AND WHY THIS ONE LINE IS NOT OPTIONAL.
   *
   * three caches a compiled program under a key that ends in
   * `material.customProgramCacheKey()`, whose default is
   * `this.onBeforeCompile.toString()` — the SOURCE TEXT of the hook, not the
   * closure. Every material `confidence.patch()` touches therefore reports the
   * same key text, so two patched materials that agree on every other program
   * parameter share one compiled program, and the one that compiles first wins.
   *
   * Measured on the first build of this layer: a plain patched
   * MeshStandardMaterial with no map, opaque, is parameter-for-parameter the
   * twin of a mapless building material out of `buildings.js`, which chains a
   * SECOND hook reading the per-vertex `_roughness` and facade-tone attributes
   * this geometry does not have. The fence drew in the right place, in the right
   * shape, casting the right shadow, in SOLID BLACK, at both viewports, with no
   * page error and no shader warning — because it was being drawn by another
   * layer's program against attributes it never bound. Unpatching the material
   * lit it perfectly, which is what made the cause so hard to see.
   *
   * The key below is this layer's own, so the fence gets its own program. The
   * general trap is not fixed here — any future layer that patches a plain lit
   * material walks into the same collision — and is filed as its own ticket.
   */
  mat.customProgramCacheKey = () => 'chicago4d-enclosure-timber';

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'enclosures';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  group.userData.census = out.census;

  out.dispose = () => { geo.dispose(); mat.dispose(); };
  return out;
}
