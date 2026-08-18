/**
 * frontage.js — the plank walks, the board crossings, the hitching posts and the
 * named boards on posts that stand between a building and the street it fronts
 * on. Written for the Green Tree Tavern (T-0082) and made a town layer by the
 * Sauganash Hotel (T-0086), which brought the second record and the first post
 * with nothing hanging on it.
 *
 * WHY THIS IS A LAYER AND NOT MORE YARD GOODS. A barrel or a wagon stands on a
 * building's own ground and is derived from its walls alone, which is what
 * `yard.js` draws. A walk and a crossing stand in the STREET, and the number
 * that decides where they may lie belongs to the street — the travelled track's
 * own half-width out of `data/streets/1835.json`. This is the first thing in
 * the project derived from a building and a street at once.
 *
 * WHAT IT WILL AND WILL NOT DO.
 *
 *  * Every board sits on the TERRAIN, sampled under its own centre, exactly as
 *    a barrel does. A walk laid on one height would float at one end of a
 *    frontage and be buried at the other, and this ground is not flat.
 *  * It draws LETTERING, and it is the only thing in this renderer that does.
 *    `docs/LIBERTIES.md` L25 leaves the town's one documented board blank
 *    because nobody described the painting on it; this board's subject is a
 *    NAME that the reference view states in as many words, so the wording is
 *    the plate's and only the letterform is invented (L135). The record carries
 *    the text and the argument; this file only draws what the record says, and
 *    a record with no `text` gets a blank board.
 *  * The timber is ONE draw call for the whole layer, the way the fences and
 *    the signboards are. The lettering is a second, because a painted name is a
 *    texture and timber is not — and it exists only when a board carries text.
 *  * It marks itself. Every vertex carries `_confidence`, so the whole layer
 *    disappears when a visitor hides `reconstructed` and the frontage goes back
 *    to bare ground. That is the truthful behaviour: no source record in this
 *    repository states that a walk stood here on 1 July 1835.
 *  * It answers a pick. A walk, a crossing and a post all belong to the building
 *    they were derived from, so aiming at any of them opens that building's card
 *    — which is what a sign is FOR.
 *  * A post carries a board only where the building's own reference views show
 *    one. The Sauganash's posts are hitching posts: chest-high timber under a
 *    capped head, no arm, no board and nothing lettered, because none of its
 *    three views shows a name board at this hotel (its record's
 *    `board_on_a_post` block states that reading rather than leaving it silent).
 */

import * as THREE from 'three';

/** attested · inferred · reconstructed, as the confidence view reads them. */
const LEVEL = { attested: 0, documented: 0, inferred: 0.5, reconstructed: 1 };

/**
 * The two tones this layer needs, and why they are converted rather than picked.
 * `THREE.Color.setHex` reads sRGB with `ColorManagement.enabled` on, so these are
 * the sRGB hexes that land on the weathered-board linear triples the signage
 * layer and the yard already use — copying a glTF `baseColorFactor` straight
 * across would draw this walk two stops darker than the boards beside it.
 */
const TIMBER = 0xcbc2b1;        // sawn board, weathered — the signboard's own tone
const PAINT = '#2f2013';        // the letterform's paint: L135 claims the colour

/** How far a plank's box reaches below the deck: enough to meet the ground. */
const SKIRT_M = 0.02;
/** Daylight between two boards — a plank walk is not a slab. */
const PLANK_GAP_M = 0.02;
/** A crossing is subdivided this often ALONG its run so it follows the ground. */
const CROSSING_STEP_M = 0.9;

/**
 * One box, 12 triangles, flat-shaded from its own face normals. `u` is the
 * horizontal unit vector along the box's length; up is world Y always.
 * Deliberately the same helper shape as `signage.js` and `enclosures.js` — three
 * layers drawing small timber the same way is one thing to reason about.
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

/** The ground under a point, or null where the heightfield has nothing to say. */
function groundAt(terrain, e, n) {
  const y = terrain.surfaceHeight(e, n);
  return Number.isFinite(y) ? y : null;
}

/**
 * A run of boards laid ACROSS the way a foot travels — an ordinary plank walk.
 * Each board samples the terrain under its own centre, and two short stringers
 * under its edges close the gap to the ground so the deck never reads as
 * floating over a fall it does not follow.
 */
function buildWalk(buf, walk, terrain, level, problems) {
  const line = walk.centreline_local_enu_m;
  if (!Array.isArray(line) || line.length < 2) {
    problems.push(`frontage: ${walk.id} carries no centreline — nothing is laid`);
    return false;
  }
  const [a, b] = line;
  // Local ENU (E, N) to the renderer's world (E, up, -N).
  const ax = a[0];
  const az = -a[1];
  const bx = b[0];
  const bz = -b[1];
  const dx = bx - ax;
  const dz = bz - az;
  const len = Math.hypot(dx, dz);
  if (len < 0.5) {
    problems.push(`frontage: ${walk.id} is ${len.toFixed(2)} m long — nothing is laid`);
    return false;
  }
  const rx = dx / len;
  const rz = dz / len;            // along the run
  const wx = -rz;
  const wz = rx;                  // across it
  const halfW = (walk.width_m ?? 1.83) / 2;
  const rise = walk.rise_m ?? 0.11;
  const thick = walk.plank_thickness_m ?? 0.055;
  const pitch = walk.plank_pitch_m ?? 0.26;
  const n = Math.max(1, Math.round(len / pitch));
  const step = len / n;
  let drawn = 0;
  for (let i = 0; i < n; i += 1) {
    const t = (i + 0.5) * step;
    const cx = ax + rx * t;
    const cz = az + rz * t;
    const g = groundAt(terrain, cx, -cz);
    if (g === null) continue;
    const top = g + rise;
    // The board itself, its long axis ACROSS the run.
    pushBox(buf, cx, top - thick / 2, cz, wx, wz,
      halfW, Math.max(0.02, (step - PLANK_GAP_M) / 2), thick / 2, level);
    // Two stringers under its edges, from the ground to the underside.
    const under = Math.max(0.01, rise - thick + SKIRT_M);
    for (const s of [-1, 1]) {
      pushBox(buf,
        cx + wx * s * (halfW - 0.09), top - thick - under / 2 + SKIRT_M / 2, cz + wz * s * (halfW - 0.09),
        rx, rz, step / 2, 0.045, under / 2, level);
    }
    drawn += 1;
  }
  if (!drawn) {
    problems.push(`frontage: ${walk.id} found no ground under any board — nothing is laid`);
    return false;
  }
  return true;
}

/**
 * A crossing: boards laid ALONG the way a foot travels, which is what a crossing
 * is FOR — it spans the ruts instead of lying in them. Subdivided along the run
 * so that a board fifteen metres long still follows the camber of the road it
 * crosses.
 */
function buildCrossing(buf, walk, terrain, level, problems) {
  const line = walk.centreline_local_enu_m;
  if (!Array.isArray(line) || line.length < 2) {
    problems.push(`frontage: ${walk.id} carries no centreline — nothing is laid`);
    return false;
  }
  const [a, b] = line;
  const ax = a[0];
  const az = -a[1];
  const dx = b[0] - ax;
  const dz = -b[1] - az;
  const len = Math.hypot(dx, dz);
  if (len < 0.5) {
    problems.push(`frontage: ${walk.id} is ${len.toFixed(2)} m long — nothing is laid`);
    return false;
  }
  const rx = dx / len;
  const rz = dz / len;
  const wx = -rz;
  const wz = rx;
  const width = walk.width_m ?? 1.22;
  const boards = Math.max(1, walk.plank_count ?? 4);
  const bw = width / boards;
  const rise = walk.rise_m ?? 0.06;
  const thick = walk.plank_thickness_m ?? 0.055;
  const segs = Math.max(1, Math.round(len / CROSSING_STEP_M));
  const step = len / segs;
  let drawn = 0;
  for (let i = 0; i < segs; i += 1) {
    const t = (i + 0.5) * step;
    const cx = ax + rx * t;
    const cz = az + rz * t;
    const g = groundAt(terrain, cx, -cz);
    if (g === null) continue;
    const top = g + rise;
    for (let j = 0; j < boards; j += 1) {
      const off = (j + 0.5) * bw - width / 2;
      pushBox(buf, cx + wx * off, top - thick / 2, cz + wz * off, rx, rz,
        step / 2, Math.max(0.02, (bw - PLANK_GAP_M) / 2), thick / 2, level);
    }
    drawn += 1;
  }
  if (!drawn) {
    problems.push(`frontage: ${walk.id} found no ground under any board — nothing is laid`);
    return false;
  }
  return true;
}

/**
 * The post, its cross-arm, two hangers and the board hanging under them. Returns
 * the board's own frame so the lettering can be laid on its two faces without
 * re-deriving any of this arithmetic.
 *
 * The frame, against docs/GLB-CONTRACT.md: `facade_bearing_deg` is a compass
 * bearing, so the outward normal is (sin b, cos b) in ENU and the along-wall
 * direction is (cos b, −sin b). The renderer's world is (E, up, −N), which is
 * where every negated north below comes from — the same three lines
 * `signage.js` composes.
 */
function buildPost(buf, post, terrain, level, problems) {
  const at = post.at_local_enu_m;
  if (!Array.isArray(at) || at.length !== 2) {
    problems.push(`frontage: ${post.id} carries no stand — no post is set`);
    return null;
  }
  const g = groundAt(terrain, at[0], at[1]);
  if (g === null) {
    problems.push(`frontage: ${post.id} has no ground under it — no post is set`);
    return null;
  }
  const b = ((post.facade_bearing_deg ?? 0) * Math.PI) / 180;
  const ox = Math.sin(b);
  const oz = -Math.cos(b);       // out of the facade, toward the street
  const wx = Math.cos(b);
  const wz = Math.sin(b);        // along the wall, away from the corner
  const px = at[0];
  const pz = -at[1];
  const h = post.post_height_m ?? 3.6;
  const sq = (post.post_square_m ?? 0.18) / 2;

  // A HITCHING POST IS A POST AND NOTHING ELSE (T-0086). The Sauganash's three
  // views put posts at its road edge and a horse tied to one; none of them puts
  // a board on any of them, so this branch draws chest-high timber under a
  // capped head and returns a frame carrying no text — the lettering pass never
  // sees it, and the record says in as many words why there is nothing to letter.
  if (post.kind === 'hitching_post') {
    const cap = (post.cap_square_m ?? 0.22) / 2;
    const capT = post.cap_thickness_m ?? 0.07;
    pushBox(buf, px, g + (h - capT) / 2, pz, wx, wz, sq, sq, (h - capT) / 2, level);
    pushBox(buf, px, g + h - capT / 2, pz, wx, wz, cap, cap, capT / 2, level);
    return { cx: px, cy: g + h, cz: pz, ox, oz, wx, wz, bw: 0, bh: 0, bt: 0, text: '' };
  }
  const arm = post.arm_m ?? 1.55;
  const armT = 0.09;
  const drop = post.hanger_drop_m ?? 0.18;
  const bw = post.board_w_m ?? 1.3;
  const bh = post.board_h_m ?? 0.55;
  const bt = post.board_thickness_m ?? 0.055;

  // The pole. One box standing on the ground the record's stand samples.
  pushBox(buf, px, g + h / 2, pz, wx, wz, sq, sq, h / 2, level);
  // The cross-arm at its head, running along the wall away from the corner.
  const armY = g + h - armT;
  pushBox(buf, px + wx * (arm / 2), armY, pz + wz * (arm / 2), wx, wz,
    arm / 2, armT / 2, armT / 2, level);
  // A knee brace under it, so the arm reads as carried rather than glued.
  pushBox(buf, px + wx * 0.30, armY - 0.30, pz + wz * 0.30, wx, wz,
    0.30, armT * 0.35, armT * 0.35, level);
  // Two hangers dropping from the arm, and the board under them. The board's
  // long axis runs along the arm and its face looks out of the facade, which is
  // how it is read from the street the inn fronts on.
  const hang = arm * 0.55;
  for (const s of [-1, 1]) {
    pushBox(buf,
      px + wx * (hang + s * bw * 0.36), armY - drop / 2, pz + wz * (hang + s * bw * 0.36),
      ox, oz, 0.022, 0.018, drop / 2, level);
  }
  const cy = armY - drop - bh / 2;
  const cx = px + wx * hang;
  const cz = pz + wz * hang;
  pushBox(buf, cx, cy, cz, wx, wz, bw / 2, bt / 2, bh / 2, level);
  return { cx, cy, cz, ox, oz, wx, wz, bw, bh, bt, text: post.text || '' };
}

/**
 * The painted name, as a canvas texture on a plane just proud of each board
 * face. Drawn rather than left blank because the wording is evidence this
 * project holds and the letterform is the only invented part — see
 * docs/LIBERTIES.md L135 and the record's own `lettering` block.
 */
function makeLettering(boards) {
  const lettered = boards.filter((b) => b && b.text);
  if (!lettered.length) return null;
  const pos = [];
  const nrm = [];
  const uv = [];
  const conf = [];
  // Only one texture is supported per draw call, so the layer draws the first
  // wording it meets and says so if a second ever appears. One board today.
  const first = lettered[0];
  for (const board of lettered) {
    if (board.text !== first.text) continue;
    const { cx, cy, cz, ox, oz, wx, wz, bw, bh, bt } = board;
    const mx = bw * 0.5 - 0.07;
    const my = bh * 0.5 - 0.07;
    const proud = bt / 2 + 0.006;
    for (const side of [1, -1]) {
      const nx = ox * side;
      const nz = oz * side;
      // WHICH WAY THE NAME RUNS. A reader standing off the face has the board's
      // along-wall axis on their LEFT when they look at the near face and on
      // their right at the far one, so the horizontal axis flips with the face
      // — and it is the NEAR face that takes the minus. Getting this backwards
      // draws a perfectly lit board with the name mirrored on both sides, which
      // is what the first build of this layer did.
      const ux = -wx * side;
      const uz = -wz * side;
      const P = (s, t) => [cx + nx * proud + ux * s * mx, cy + t * my, cz + nz * proud + uz * s * mx];
      const quad = [P(-1, -1), P(1, -1), P(1, 1), P(-1, 1)];
      const uvs = [[0, 0], [1, 0], [1, 1], [0, 1]];
      for (const [i, j, k] of [[0, 1, 2], [0, 2, 3]]) {
        for (const idx of [i, j, k]) {
          pos.push(quad[idx][0], quad[idx][1], quad[idx][2]);
          nrm.push(nx, 0, nz);
          uv.push(uvs[idx][0], uvs[idx][1]);
          conf.push(board.level ?? 1);
        }
      }
    }
  }
  if (!pos.length) return null;

  const W = 1024;
  const H = Math.round(W * (first.bh / first.bw));
  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;
  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = PAINT;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  // Fit the wording to the board rather than choosing a size: the board is a
  // derived width and the name is a given, so the type is what gives way.
  let size = Math.round(H * 0.52);
  const face = (px) => `600 ${px}px Georgia, "Times New Roman", Times, serif`;
  ctx.font = face(size);
  const limit = W * 0.86;
  while (size > 8 && ctx.measureText(first.text).width > limit) {
    size -= 4;
    ctx.font = face(size);
  }
  ctx.fillText(first.text, W / 2, H / 2 + size * 0.03);

  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 4;
  texture.needsUpdate = true;
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(nrm, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(conf, 1));
  geo.computeBoundingSphere();
  return { geo, texture, text: first.text };
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
export async function createFrontage({
  dataBase, terrain, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'frontage';
  const out = {
    group,
    records: [],
    walks: [],
    posts: [],
    census: {
      records: 0, walks: 0, crossings: 0, posts: 0, hitching: 0, lettered: 0,
      refused: 0, meshes: 0,
    },
    pickAt: () => null,
    dispose: () => {},
  };

  if (!dataBase || !terrain) {
    problems.push('frontage: no data base or no terrain — no walk is laid');
    return out;
  }
  let index;
  try {
    index = await getJSON(new URL('frontage/index.json', dataBase));
  } catch (err) {
    // Degrade to NOTHING drawn plus a recorded problem, never to an invented
    // walk: the same contract the enclosure, signage and yard layers keep.
    problems.push(`frontage: ${err.message} — no walk is laid`);
    return out;
  }
  const wanted = Array.isArray(index.frontage) ? index.frontage : [];
  const loaded = await Promise.all(wanted.map(async (f) => {
    if (!f.file) return [f.id, null, 'the manifest gave no file'];
    try {
      return [f.id, await getJSON(new URL(`frontage/${f.file}`, dataBase)), null];
    } catch (err) { return [f.id, null, err.message]; }
  }));

  const buf = { pos: [], nrm: [], conf: [] };
  const spans = [];
  const boards = [];
  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`frontage: ${id} — ${why}`); continue; }
    out.records.push(record);
    out.census.records += 1;
    out.census.refused += (record.refused ?? []).length;
    for (const walk of record.walks ?? []) {
      const level = LEVEL[walk.confidence] ?? 1;
      const from = buf.pos.length / 9;
      const crossing = walk.kind === 'board_crossing';
      const ok = crossing
        ? buildCrossing(buf, walk, terrain, level, problems)
        : buildWalk(buf, walk, terrain, level, problems);
      if (!ok) continue;
      spans.push({ id: walk.belongs_to, from, to: buf.pos.length / 9 });
      out.walks.push(walk);
      out.census[crossing ? 'crossings' : 'walks'] += 1;
    }
    for (const post of record.posts ?? []) {
      const level = LEVEL[post.confidence] ?? 1;
      const from = buf.pos.length / 9;
      const board = buildPost(buf, post, terrain, level, problems);
      if (!board) continue;
      spans.push({ id: post.belongs_to, from, to: buf.pos.length / 9 });
      out.posts.push(post);
      out.census.posts += 1;
      if (post.kind === 'hitching_post') out.census.hitching += 1;
      if (board.text) out.census.lettered += 1;
      boards.push({ ...board, level });
    }
  }
  if (!buf.pos.length) {
    if (out.census.records) {
      problems.push('frontage: the records loaded and not one board was laid');
    }
    return out;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(buf.nrm, 3));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.computeBoundingSphere();

  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(TIMBER), roughness: 0.9, metalness: 0.0,
  });
  mat.name = 'frontage-timber';
  confidence?.patch(mat);
  /**
   * ITS OWN PROGRAM CACHE KEY. three caches a compiled program under a key
   * ending in `customProgramCacheKey()`, whose default is the SOURCE TEXT of
   * `onBeforeCompile` — so every material `confidence.patch()` touches reports
   * the same key and two of them can silently share one program. That drew a
   * whole layer in another layer's shader once already; ticket T-0053 is the
   * general fix and this is the local guard every derived layer carries.
   */
  mat.customProgramCacheKey = () => 'chicago4d-frontage-timber';

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'frontage';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  out.census.meshes = 1;

  const letters = makeLettering(boards);
  let letterMat = null;
  if (letters) {
    letterMat = new THREE.MeshStandardMaterial({
      map: letters.texture,
      color: new THREE.Color(0xffffff),
      roughness: 0.95,
      metalness: 0.0,
      transparent: false,
      alphaTest: 0.5,
      /**
       * DOUBLE-SIDED, and it is not laziness. Each face's quad is wound from the
       * board's own axes rather than from a camera, so one of the two comes out
       * back-facing — and under `FrontSide` the name simply did not draw, on a
       * board that looked perfectly finished. Four triangles is not worth a
       * winding rule that has to be right twice.
       */
      side: THREE.DoubleSide,
    });
    letterMat.name = 'frontage-lettering';
    confidence?.patch(letterMat);
    letterMat.customProgramCacheKey = () => 'chicago4d-frontage-lettering';
    const letterMesh = new THREE.Mesh(letters.geo, letterMat);
    letterMesh.name = 'frontage-lettering';
    letterMesh.castShadow = false;
    letterMesh.receiveShadow = false;
    group.add(letterMesh);
    out.census.meshes = 2;
    out.lettering = letters.text;
  }
  group.userData.census = out.census;

  const raycaster = new THREE.Raycaster();
  /** The building this walk or post belongs to, or null. */
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

  out.dispose = () => {
    geo.dispose();
    mat.dispose();
    if (letters) { letters.geo.dispose(); letters.texture.dispose(); }
    if (letterMat) letterMat.dispose();
  };
  return out;
}
