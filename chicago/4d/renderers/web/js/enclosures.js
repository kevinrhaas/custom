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
 *  * It knows three fences. `post_and_rail` is the open horizontal thing the wagon
 *    yard and the pound are built from: posts, and courses spanning between them.
 *    `picket` is the Kinzie-view plate's garden fence — the same posts and two
 *    stringers, closed with a run of vertical pales at the record's own pale width
 *    and gap. `board` is the Sauganash's yard fence: the same construction again,
 *    at the record's own board width and a butted gap, and tall. The difference is
 *    not decoration and it is the whole of what each one says: a rail fence turns a
 *    team and you see the yard through it, a picket fence keeps poultry out of the
 *    vegetables, and a board fence is a wall — it says the ground behind it was
 *    private, which is exactly what the three views of that hotel show.
 *  * It refuses water. A post whose foot is in the river mask is dropped, the
 *    way `trees.js` refuses a stem below the waterline. A fence marching into
 *    the water would be a claim about a shoreline this layer knows nothing of.
 *  * It draws in CULLING-SIZED CHUNKS. It used to be one draw call for the whole
 *    layer — posts and rails emitted into a single non-indexed buffer, because a
 *    fence is a lot of very small boxes and eighty draw calls for eighty sticks
 *    is how a phone loses its frame. That was right while the only enclosures
 *    were one yard and one pound, and it stopped being right the moment the
 *    dooryard pickets put fifteen plots across the whole South Division: one
 *    geometry spanning the town has a bounding sphere no frustum ever culls, so
 *    every fence in Chicago was drawn in every frame including the ones behind
 *    the camera — 33,166 triangles, everywhere, forever. T-0115 measured that
 *    and named it the largest free saving left in the scene, and T-0119 had
 *    already solved the same problem one layer over (`frontage.js` builds the
 *    river walk as one mesh per segment). So a run — or a piece of a run no
 *    longer than `CHUNK_M` across — is its own mesh with its own bounding
 *    sphere, on the SAME material, and the draw-call principle bends exactly as
 *    far as culling needs it to and no further.
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

/**
 * Pale stock, in metres. Same argument as the rail above: a pale's THICKNESS is how a
 * stick is drawn, where its WIDTH and the gap beside it are the fence's rhythm and
 * belong to the record — `picket_width_m` / `picket_gap_m` and `board_width_m` /
 * `board_gap_m` — because they are what decides whether a visitor is looking at a
 * fence or at a wall. The THICKNESS is shared: a pale and a fence board are the same
 * sawn stuff, and nothing in any record here distinguishes them.
 */
const PALE_T_M = 0.022;

/** A drop this steep between neighbouring posts is a bank, not a yard. */
const MAX_STEP_M = 1.5;

/**
 * How far a chunk is allowed to reach before the layer starts a new one, in
 * metres of bounding-box diagonal. The number is a culling decision and nothing
 * else: small enough that a mesh's bounding sphere is local to the fence it
 * draws (a dooryard plot is 10.5 m corner to corner and is always one chunk),
 * large enough that a town's worth of fence is tens of meshes rather than
 * hundreds. A chunk boundary can only fall between two bays, so no member is
 * ever split.
 */
const CHUNK_M = 30;

/* -------------------------------------------------------------------------- */
/* geometry                                                                    */
/* -------------------------------------------------------------------------- */

/**
 * One box, 12 triangles, flat-shaded from its own face normals — or 10 with
 * `skipUnderside`, which is what a pale takes. A picket fence is thousands of very
 * small boxes and the underside of every one of them is buried in the ground it
 * stands on; at 3 500 pales that face is 7 000 triangles nobody can ever see, and
 * the scene's `light` detail ceiling is the tightest of the three.
 *
 * ...or **4, with `plank`**, which is what a pale takes at `light` (T-0067,
 * costed by T-0115). A pale is a 22 mm-thick prism, and of its ten triangles SIX
 * are the two 22 mm edge faces and the 22 mm top cap — three quarters of the
 * geometry for one fortieth of the silhouette. At `light` a pale is drawn as a
 * zero-thickness double-sided plank instead: the two broad faces only, each with
 * its own outward normal so it lights correctly from either side of the fence
 * without a second material. The pale keeps its width, its height, its position
 * and its rhythm; what it loses is a thickness you cannot see from more than a
 * metre away and could never see at all from the side the fence is meant to be
 * read from. Measured on the 2,335 pales standing today: ~14,000 triangles, and
 * every pale the fence tickets add after this costs 4 at `light` instead of 10.
 * `full` and `balanced` draw the prism, unchanged.
 */
function pushBox(buf, cx, cy, cz, ux, uz, halfLen, halfW, halfH, level,
                 skipUnderside = false, plank = false) {
  // `u` is the horizontal unit vector along the box; `v` is horizontal and
  // perpendicular to it. Up is world Y, always: a leaning fence post is a
  // claim about ground this layer does not make.
  const vx = -uz;
  const vz = ux;
  // A plank is the same box with its thickness taken out, so the two broad
  // faces below land exactly on the line the pale's centre is authored on —
  // which is where the prism's own centre stood.
  const w = plank ? 0 : halfW;
  const P = (a, b, c) => [
    cx + ux * a * halfLen + vx * b * w,
    cy + c * halfH,
    cz + uz * a * halfLen + vz * b * w,
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
  // `faces` runs +u, -u, +v, -v, top, underside. A plank keeps the two BROAD
  // faces, which for a pale are the ±v pair: `halfLen` is the pale's recorded
  // width along the run and `halfW` its thickness across it, so the faces that
  // carry the fence are the ones perpendicular to v. The six it drops are the
  // two edge faces, the top cap and the buried underside.
  const wanted = plank ? faces.slice(2, 4) : (skipUnderside ? faces.slice(0, 5) : faces);
  for (const [t1, t2, n] of wanted) {
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

/**
 * A chunk under construction: one buffer, and the bounding box of the ground it
 * has covered so far. `reaches` is the diagonal of that box, which is what
 * `CHUNK_M` bounds — a mesh whose bounding sphere is bigger than its own fence
 * is a mesh the frustum cannot cull.
 */
function newChunk() {
  return { pos: [], nrm: [], conf: [],
    minE: Infinity, maxE: -Infinity, minN: Infinity, maxN: -Infinity };
}
function cover(chunk, e, n) {
  if (e < chunk.minE) chunk.minE = e;
  if (e > chunk.maxE) chunk.maxE = e;
  if (n < chunk.minN) chunk.minN = n;
  if (n > chunk.maxN) chunk.maxN = n;
}
function reaches(chunk) {
  if (!Number.isFinite(chunk.minE)) return 0;
  return Math.hypot(chunk.maxE - chunk.minE, chunk.maxN - chunk.minN);
}

function buildRecord(record, terrain, problems, { plankPales = false } = {}) {
  const form = record.form ?? {};
  const height = form.height_m?.value ?? 1.37;
  const courses = Math.max(1, Math.round(form.rail_courses?.value ?? 3));
  const spacing = Math.max(1, form.post_spacing_m?.value ?? 2.9);
  const postHalf = (form.post_size_m?.value ?? 0.14) / 2;
  const kind = form.fence_type?.value ?? 'post_and_rail';
  // TWO CLOSED FENCES AND ONE OPEN ONE. A picket and a board fence are the same
  // construction — posts, stringers behind them, vertical stock nailed across —
  // and they differ in the STOCK, which is the whole of what a visitor reads:
  // a pale is a hand's width with a hand's width of daylight beside it, and a
  // board is butted to its neighbour so there is none. That is why the two are
  // one branch here and two values in the record: the difference between a
  // garden fence you see the garden through and a fence that makes a yard a
  // room is `board_gap_m`, and it belongs to the record for the same reason
  // `picket_gap_m` does.
  const closed = kind === 'picket' || kind === 'board';
  const board = kind === 'board';
  const paleW = Math.max(0.02,
    (board ? form.board_width_m?.value : form.picket_width_m?.value) ?? 0.089);
  // A board fence's gap is allowed to be the shrinkage gap between two butted
  // boards, which is millimetres; a pale's floor stays where it was.
  const palePitch = paleW + Math.max(board ? 0 : 0.01,
    (board ? form.board_gap_m?.value : form.picket_gap_m?.value) ?? 0.089);
  // The weakest grade on anything that decides where a stick of this fence is.
  // In practice that is the fence type, and no fence type in this dataset is
  // anything but invented; the max is here so the day a source describes one,
  // the geometry stops claiming to be a guess.
  const level = Math.max(
    LEVEL[form.fence_type?.confidence] ?? 1,
    LEVEL[form.height_m?.confidence] ?? 1,
  );

  let posts = 0;
  let pales = 0;
  let dropped = 0;
  /**
   * The chunking, and where its boundaries are ALLOWED to fall. A new chunk is
   * opened when the one in hand has reached `CHUNK_M` across, and only ever
   * between two bays — the post, its rails and its pales all go into the same
   * buffer, so no member is ever split across two meshes and nothing moves by a
   * millimetre. The chunks are otherwise exactly the timber the single buffer
   * held: the same boxes, in the same places, on the same material.
   */
  const chunks = [];
  let buf = newChunk();
  const flush = () => {
    if (buf.pos.length) chunks.push(buf);
    buf = newChunk();
  };
  for (const run of record.runs ?? []) {
    const path = run.path_local_enu_m;
    if (!Array.isArray(path) || path.length < 2) continue;
    // A run is its own chunk (or several): two plots on opposite sides of the
    // town share a record and must not share a bounding sphere.
    flush();
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
      const post = (f) => {
        if (!f) return;
        cover(buf, f.e, f.n);
        pushBox(buf, f.e, f.y + height / 2, -f.n, 1, 0,
          postHalf, postHalf, height / 2, level);
        posts++;
      };
      for (let i = 0; i < n; i++) {
        // The bay's own near post, then its timber: one bay is the smallest
        // thing a chunk boundary may fall between, so it is emitted whole.
        if (reaches(buf) > CHUNK_M) flush();
        post(feet[i]);
        const a = feet[i];
        const b = feet[i + 1];
        if (!a || !b) continue;
        if (Math.abs(a.y - b.y) > MAX_STEP_M) { dropped++; continue; }
        cover(buf, b.e, b.n);
        const de = b.e - a.e;
        const dn = b.n - a.n;
        const len = Math.hypot(de, dn);
        if (len < 0.05) continue;
        // The renderer's world is (E, up, -N), so the along-run unit vector
        // has its north component negated with the position.
        const ux = de / len;
        const uz = -dn / len;
        for (let c = 1; c <= courses; c++) {
          // On a rail fence the courses ARE the fence, so the top one is the top of
          // it. On a picket fence they are stringers behind the pales and want to sit
          // inside the height, or the top rail reads as a cap rail nobody described.
          const f = closed
            ? (courses > 1 ? 0.22 + 0.58 * ((c - 1) / (courses - 1)) : 0.55)
            : c / courses;
          const h = height * f - RAIL_H_M / 2;
          pushBox(buf,
            (a.e + b.e) / 2, (a.y + b.y) / 2 + h, -(a.n + b.n) / 2,
            ux, uz, len / 2, RAIL_W_M / 2, RAIL_H_M / 2, level);
        }
        if (closed) {
          // The pales, centred on the run line exactly as the posts and rails are.
          // Nailing them to one face would be more like a real fence and would push
          // timber off the line the record authored, which is the one thing the
          // layer's own gate measures; the interpenetration costs nothing on screen.
          const count = Math.max(1, Math.floor(len / palePitch));
          const first = (len - (count - 1) * palePitch) / 2;
          for (let k = 0; k < count; k++) {
            const f = (first + k * palePitch) / len;
            pushBox(buf,
              a.e + de * f, a.y + (b.y - a.y) * f + height / 2, -(a.n + dn * f),
              ux, uz, paleW / 2, PALE_T_M / 2, height / 2, level, true, plankPales);
            pales++;
          }
        }
      }
      // The stretch's far post: the loop above emits each bay's NEAR post, so
      // the last one would otherwise be left off the end of every run.
      post(feet[n]);
    }
  }
  flush();
  if (!posts) {
    problems.push(`enclosures: ${record.id} drew nothing — every post stood in water `
      + 'or the record carries no run with two points');
  }
  return { chunks, posts, pales, dropped };
}

/* -------------------------------------------------------------------------- */
/* the layer                                                                   */
/* -------------------------------------------------------------------------- */

async function getJSON(url) {
  const res = await fetch(url, { cache: 'no-cache' });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} — ${url}`);
  return res.json();
}

/** The detail levels at which a pale is drawn as a plank rather than a prism.
 *  Named here rather than read out of `main.js` so the layer answers for its own
 *  geometry; `main.js` passes the level and this decides what that level means
 *  to a fence. See the note on `pushBox`. */
const PLANK_LEVELS = new Set(['light']);

/**
 * @param {object} o dataBase (data/ root) · terrain · confidence · problems ·
 *                   detail (the scene-detail level, `full` by default)
 * @returns {Promise<{group: THREE.Group, records: object[], census: object,
 *                    setDetail: function, dispose: function}>}
 */
export async function createEnclosures({
  dataBase, terrain, confidence = null, problems = [], detail = 'full',
} = {}) {
  const group = new THREE.Group();
  group.name = 'enclosures';
  const out = { group, records: [],
    census: { enclosures: 0, posts: 0, pales: 0, dropped: 0, chunks: 0 },
    // Replaced once there is a mesh to raycast; a layer that drew nothing still
    // answers a pick, with nothing.
    pickAt: () => null,
    setDetail: () => false,
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

  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`enclosures: ${id} — ${why}`); continue; }
    out.records.push(record);
  }
  if (!out.records.length) return out;

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

  /**
   * WHICH RECORD A MESH BELONGS TO, and why this layer bothers.
   *
   * A hit on a merged buffer knows nothing about which fence it landed on. That
   * was fine while the only enclosure was a yard nobody could ask a question
   * about. It stopped being fine with the estray pen (T-0051): the pen is a
   * STRUCTURE RECORD whose geometry moved here, its card is still compiled from
   * `data/structures/estray_pen.json`, and a visitor who could click Chicago's
   * first public building while it was a roofed box must not lose the card
   * because the model got more honest about its roof.
   *
   * It used to be answered with banked triangle ranges and a `faceIndex` lookup.
   * Chunking answers it better and for free: a chunk is timber from ONE record,
   * so the owner rides on the mesh (`userData.pickId`) exactly as it does on the
   * chunked plank walks in `frontage.js`. An enclosure with no `structure_id` —
   * the wagon yard, the town's garden pickets — carries null and is not
   * pickable, which is correct: there is no card behind it.
   */
  let meshes = [];

  /**
   * Build (or rebuild) the layer's meshes at the level in hand. Rebuilding is
   * what a change of scene detail costs here, and it costs no fetch: the records
   * are already loaded, and geometry this small is faster to rebuild than a
   * second copy of it is to keep. `problems` is only collected on the FIRST
   * build — a rebuild that re-reported every one of them would grow the panel
   * every time a visitor touched the detail control.
   */
  let level = detail;
  let firstBuild = true;
  function build() {
    for (const m of meshes) { group.remove(m); m.geometry.dispose(); }
    meshes = [];
    const sink = firstBuild ? problems : [];
    const census = { enclosures: 0, posts: 0, pales: 0, dropped: 0, chunks: 0 };
    const plankPales = PLANK_LEVELS.has(level);
    for (const record of out.records) {
      const r = buildRecord(record, terrain, sink, { plankPales });
      for (const chunk of r.chunks) {
        const geo = new THREE.BufferGeometry();
        geo.setAttribute('position', new THREE.Float32BufferAttribute(chunk.pos, 3));
        geo.setAttribute('normal', new THREE.Float32BufferAttribute(chunk.nrm, 3));
        geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(chunk.conf, 1));
        // The whole point of the chunk: its own bounding sphere, around its own
        // fence, so the frustum can leave it out.
        geo.computeBoundingSphere();
        const mesh = new THREE.Mesh(geo, mat);
        mesh.name = 'enclosure-chunk';
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        mesh.userData.pickId = record.structure_id ?? null;
        mesh.userData.recordId = record.id;
        group.add(mesh);
        meshes.push(mesh);
        census.chunks += 1;
      }
      census.enclosures += 1;
      census.posts += r.posts;
      census.pales += r.pales;
      census.dropped += r.dropped;
    }
    firstBuild = false;
    Object.assign(out.census, census);
    group.userData.census = out.census;
  }
  build();
  if (!meshes.length) return out;

  /**
   * A change of scene detail, applied in place. Returns whether anything was
   * rebuilt, so the caller can re-apply the shadow policy only when it has to —
   * every mesh here is new after a rebuild and starts out casting.
   */
  out.setDetail = (next) => {
    if (!next || next === level) return false;
    const was = PLANK_LEVELS.has(level);
    level = next;
    if (PLANK_LEVELS.has(level) === was) return false;
    build();
    return true;
  };

  const raycaster = new THREE.Raycaster();
  /**
   * The structure this fence stands for, or null. Same ray budget as
   * `buildings.pickAt` — as far as you can see, which depends on how high you
   * are — so a fence and a roof answer a click on the same terms.
   */
  out.pickAt = (ndc, camera) => {
    if (!camera) return null;
    raycaster.setFromCamera(ndc ?? new THREE.Vector2(0, 0), camera);
    raycaster.far = Math.max(400, camera.position.y * 4);
    const hits = raycaster.intersectObjects(meshes, false);
    if (!hits.length) return null;
    const hit = hits[0];
    const id = hit.object?.userData?.pickId ?? null;
    if (!id) return null;
    return { id, point: hit.point.clone(), distance: hit.distance };
  };

  out.dispose = () => {
    for (const m of meshes) m.geometry.dispose();
    meshes = [];
    mat.dispose();
  };
  return out;
}
