/**
 * flagstaff.js — the mast over Fort Dearborn, and the colours it flew.
 *
 * WHY THIS FILE EXISTS, AND WHY IT DID NOT EXIST BEFORE. This project refused a
 * flagstaff at Fort Dearborn twice, and both refusals were right. `p4_0` — the
 * retrospective plate of the fort — draws a staff with a flag flying, and it is
 * the most conspicuous single feature of that sheet; T-0044's image-accuracy
 * pass refused it because a retrospective engraving conflates the two forts, and
 * `data/exclusions.json` already excludes a flagstaff, the one in the parade of
 * Captain Whistler's FIRST fort, in the 1808 passage that closes "Such was the
 * old Fort previous to 1812" and whose exclusion says in terms that "none of it
 * may be borrowed for the second fort's records". The changelog said so out
 * loud: "The flagstaff in the plate is a trap, and it stays out."
 *
 * T-0096 asked the question the refusals left open — can anything BUT a
 * retrospective plate say so — and the answer turned out to be yes, in a book
 * this project has cited eleven times for other things. Andreas, vol. 1 p. 128,
 * under the running head "CHICAGO IN 1833-37" and in the section headed
 * "Chicago from 1833 to 1837":
 *
 *     "A flagstaff at the fort, some fifty feet high, flaunted, in pleasant
 *      weather and on holidays — a weather-beaten flag …"
 *
 * and, five sentences later, the same mast from the southern approach: "a line
 * of almost indefinable structures, and the flag over the fort, if perchance it
 * was flying." That is the SECOND fort, dated by its own section heading, in a
 * town description that never mentions the first one. So the staff is built —
 * and the plate is still not what built it, and the exclusion still stands.
 *
 * WHAT IT WILL AND WILL NOT DO.
 *
 *  * It stands the mast on the TERRAIN, sampled under its own foot, like the
 *    yard goods and unlike `signage.js` — a spar is stepped into the ground, not
 *    bolted to a wall. The butt is sunk `BUTT_SINK_M` below that sample so the
 *    foot beds into the parade rather than resting on it: if the drawn ground
 *    and the sampled heightfield disagree by a centimetre, a buried butt hides
 *    it and a flush one shows a gap.
 *  * IT SPLITS ITS OWN CONFIDENCE DOWN THE MIDDLE, and this is the whole point
 *    of the layer. The MAST carries `attested` at every vertex — Andreas states
 *    it and states its height. The FLAG carries `reconstructed`, because Andreas
 *    makes it conditional ("in pleasant weather and on holidays", "if perchance
 *    it was flying") and nothing says what was aloft at noon on 1 July 1835. So
 *    a visitor who hides reconstructed geometry strikes the colours and leaves
 *    the staff standing — which is exactly the partition the sources make.
 *  * It claims NO STAR COUNT. The canton is drawn plain. The count is derivable
 *    in principle from the Flag Act of 1818 (twenty-four stars from 1822 until
 *    Arkansas moves it to twenty-five on 4 July 1836) and this project holds no
 *    source record for that act — and a star of that canton is far under a pixel
 *    at both release viewports from any point a visitor may stand, so drawing
 *    one would be asserting a number nobody could read. See L200.
 *  * It is ONE draw call and ONE material, like the fences and the boards: the
 *    timber and the bunting are two cells of a single small canvas atlas, so the
 *    flag costs no second program and no second batch.
 *  * It answers a pick. The mast carries a card, because an object a visitor can
 *    see from across the river ought to be able to say what stood it up.
 */

import * as THREE from 'three';

/** attested · inferred · reconstructed, as the confidence view reads them. */
const LEVEL = { attested: 0, documented: 0, inferred: 0.5, reconstructed: 1 };

/**
 * THE DRAWING'S OWN GRAIN — not claims about 1835. The record owns the height,
 * the flag's size and every confidence; these are how a claim becomes triangles,
 * the division `boats.js` draws between a hull's dimensions and its loft
 * stations.
 */
const SIDES = 8;             // the mast is drawn as an octagonal prism
const BUTT_SINK_M = 0.6;     // how far the butt is stepped into the ground
const TRUCK_DROP_M = 0.35;   // the flag's head hangs this far below the truck
const FLY_SEGMENTS = 10;     // panels along the fly, which is what waves it
const WAVE_AMP_M = 0.30;     // the wave's amplitude at the free leech
const WAVE_TURNS = 1.35;     // how many times the sheet crosses itself, fly-wise

/**
 * THE WIND IS A DRAWING DECISION AND IS DECLARED AS ONE (L200). No source says
 * which way the flag blew, and a flag has to blow somewhere or hang as a
 * vertical rag that reads as a fault in the model. It streams to the
 * east-north-east — off the land and out over the lake, the quarter a summer
 * afternoon at this shore most often takes — measured here as a bearing in
 * local ENU, degrees counter-clockwise from local east.
 */
const WIND_BEARING_DEG = 22;

/** The atlas: one cell of weathered timber, one of weather-beaten bunting. */
const ATLAS_W = 512;
const ATLAS_H = 256;
const TIMBER_COLOUR = '#8a7f6b';
/** Andreas's own adjective is "weather-beaten", so nothing here is fresh. */
const BUNTING_RED = '#9c5a52';
const BUNTING_WHITE = '#ded6c6';
const BUNTING_BLUE = '#3b4a63';
const STRIPES = 13;

/* -------------------------------------------------------------------------- */
/* primitives                                                                  */
/* -------------------------------------------------------------------------- */

/** One triangle with its own face normal, a uv per corner and a confidence. */
function pushTri(buf, a, b, c, uvA, uvB, uvC, level) {
  const ux = b[0] - a[0]; const uy = b[1] - a[1]; const uz = b[2] - a[2];
  const vx = c[0] - a[0]; const vy = c[1] - a[1]; const vz = c[2] - a[2];
  let nx = uy * vz - uz * vy;
  let ny = uz * vx - ux * vz;
  let nz = ux * vy - uy * vx;
  const len = Math.hypot(nx, ny, nz);
  if (len < 1e-9) return;
  nx /= len; ny /= len; nz /= len;
  const pts = [a, b, c];
  const uvs = [uvA, uvB, uvC];
  for (let i = 0; i < 3; i += 1) {
    buf.pos.push(pts[i][0], pts[i][1], pts[i][2]);
    buf.nrm.push(nx, ny, nz);
    buf.uv.push(uvs[i][0], uvs[i][1]);
    buf.conf.push(level);
  }
}

function pushQuad(buf, a, b, c, d, uvA, uvB, uvC, uvD, level) {
  pushTri(buf, a, b, c, uvA, uvB, uvC, level);
  pushTri(buf, a, c, d, uvA, uvC, uvD, level);
}

/* -------------------------------------------------------------------------- */
/* the atlas                                                                   */
/* -------------------------------------------------------------------------- */

/** Cell 0 is timber (u 0…0.5), cell 1 the ensign (u 0.5…1). */
const TIMBER_UV = [0.25, 0.5];
const FLAG_U0 = 0.52;
const FLAG_U1 = 0.98;
const FLAG_V0 = 0.04;
const FLAG_V1 = 0.96;

/**
 * The ensign, painted once at load. Stripes and canton only: the canton is left
 * PLAIN on purpose — see the header, and L200.
 */
function paintAtlas() {
  const canvas = document.createElement('canvas');
  canvas.width = ATLAS_W;
  canvas.height = ATLAS_H;
  const g = canvas.getContext('2d');

  g.fillStyle = TIMBER_COLOUR;
  g.fillRect(0, 0, ATLAS_W / 2, ATLAS_H);

  const x0 = ATLAS_W / 2;
  const w = ATLAS_W / 2;
  for (let i = 0; i < STRIPES; i += 1) {
    g.fillStyle = i % 2 === 0 ? BUNTING_RED : BUNTING_WHITE;
    const y = Math.round((i * ATLAS_H) / STRIPES);
    const y2 = Math.round(((i + 1) * ATLAS_H) / STRIPES);
    g.fillRect(x0, y, w, y2 - y);
  }
  // The canton: seven stripes deep and two fifths of the fly, as an ensign of
  // this period is built. No stars — the count is not this project's to assert.
  g.fillStyle = BUNTING_BLUE;
  g.fillRect(x0, 0, Math.round(w * 0.4), Math.round((ATLAS_H * 7) / STRIPES));

  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 4;
  tex.needsUpdate = true;
  return tex;
}

/* -------------------------------------------------------------------------- */
/* the mast and the colours                                                    */
/* -------------------------------------------------------------------------- */

/** The tapered octagonal spar, from its buried butt to its truck. */
function pushMast(buf, cx, cz, footY, headY, butt, truck, level) {
  const ring = (y, r) => {
    const out = [];
    for (let i = 0; i < SIDES; i += 1) {
      const a = (i / SIDES) * Math.PI * 2;
      out.push([cx + Math.cos(a) * r, y, cz + Math.sin(a) * r]);
    }
    return out;
  };
  const lo = ring(footY, butt / 2);
  const hi = ring(headY, truck / 2);
  for (let i = 0; i < SIDES; i += 1) {
    const j = (i + 1) % SIDES;
    pushQuad(buf, lo[i], lo[j], hi[j], hi[i],
      TIMBER_UV, TIMBER_UV, TIMBER_UV, TIMBER_UV, level);
  }
  // The truck, closed so the spar does not read as a pipe from the bank above.
  for (let i = 1; i < SIDES - 1; i += 1) {
    pushTri(buf, hi[0], hi[i], hi[i + 1], TIMBER_UV, TIMBER_UV, TIMBER_UV, level);
  }
}

/**
 * The ensign, streaming from the hoist. The sheet is waved along the fly rather
 * than left flat: a rectangle hanging dead straight off a mast reads as a decal,
 * and the wave is the cheapest honest way to say "cloth".
 */
function pushFlag(buf, cx, cz, headY, hoist, fly, mastR, level) {
  const th = (WIND_BEARING_DEG * Math.PI) / 180;
  const fx = Math.cos(th);
  const fz = -Math.sin(th);      // local ENU east/north into world x/z
  const px = -fz;                // across the fly, horizontally
  const pz = fx;

  const at = (t, s) => {
    // t: 0 at the hoist, 1 at the leech. s: 0 at the head, 1 at the foot.
    const d = mastR + t * fly;
    const wave = Math.sin(t * Math.PI * WAVE_TURNS) * WAVE_AMP_M * t;
    // The foot lifts a little as the sheet streams, which is what cloth does.
    const y = headY - s * hoist + t * 0.18 * hoist;
    return [cx + fx * d + px * wave, y, cz + fz * d + pz * wave];
  };
  const uv = (t, s) => [
    FLAG_U0 + (FLAG_U1 - FLAG_U0) * t,
    FLAG_V1 - (FLAG_V1 - FLAG_V0) * s,
  ];

  for (let i = 0; i < FLY_SEGMENTS; i += 1) {
    const t0 = i / FLY_SEGMENTS;
    const t1 = (i + 1) / FLY_SEGMENTS;
    pushQuad(buf, at(t0, 0), at(t1, 0), at(t1, 1), at(t0, 1),
      uv(t0, 0), uv(t1, 0), uv(t1, 1), uv(t0, 1), level);
  }
}

/* -------------------------------------------------------------------------- */
/* the card — a flagstaff is not a structure, so it carries its own            */
/* -------------------------------------------------------------------------- */

function cardRecordFor(record) {
  const attributes = {};
  attributes.existence = record.existence;
  if (record.form?.height_m) attributes.height_m = record.form.height_m;
  if (record.form?.material) attributes.material = record.form.material;
  if (record.flag?.flying) attributes.flag_flying = record.flag.flying;
  if (record.flag?.condition) attributes.flag_condition = record.flag.condition;
  if (record.flag?.device) attributes.flag_device = record.flag.device;
  if (record.wrong_fort_guard) attributes.wrong_fort_guard = record.wrong_fort_guard;

  return {
    id: record.id,
    sidecar: {
      name: record.name ?? record.id,
      phase: null,
      placement: {
        symbolic_location: 'On the parade ground inside Fort Dearborn',
        position_confidence: record.position?.confidence ?? 'reconstructed',
        position_sources: record.position?.sources ?? [],
        position_note: record.position?.note ?? '',
      },
      attributes,
      citations: [],
      research_note: 'A flagstaff from data/flagstaff/ — not a structure record. '
        + 'The mast and its height are attested at Andreas vol. 1 p. 128, in a '
        + 'passage describing the town of 1833-37; the flag aloft, the mast’s '
        + 'position on the parade and the ensign’s size are reconstructed and '
        + 'claimed at docs/LIBERTIES.md L200. The retrospective plate p4_0 draws a '
        + 'flagstaff too and is NOT what built this one — see '
        + 'docs/RESEARCH/fort_dearborn.md § 10.',
    },
  };
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
 * @returns {Promise<{group: THREE.Group, records: object[], staffs: object[],
 *                    census: object, pickAt: function, dispose: function}>}
 */
export async function createFlagstaff({
  dataBase, terrain, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'flagstaff';
  const out = {
    group,
    records: [],
    staffs: [],
    census: { records: 0, staffs: 0, flags: 0, refused: 0 },
    pickAt: () => null,
    dispose: () => {},
  };

  if (!dataBase || !terrain) {
    problems.push('flagstaff: no data base or no terrain — no mast is drawn');
    return out;
  }
  let index;
  try {
    index = await getJSON(new URL('flagstaff/index.json', dataBase));
  } catch (err) {
    // Degrade to NOTHING drawn plus a recorded problem, never to an invented
    // mast: the same contract every derived layer keeps.
    problems.push(`flagstaff: ${err.message} — no mast is drawn`);
    return out;
  }
  const wanted = Array.isArray(index.flagstaffs) ? index.flagstaffs : [];
  const loaded = await Promise.all(wanted.map(async (s) => {
    if (!s.file) return [s.id, null, 'the manifest gave no file'];
    try {
      return [s.id, await getJSON(new URL(`flagstaff/${s.file}`, dataBase)), null];
    } catch (err) { return [s.id, null, err.message]; }
  }));

  const buf = { pos: [], nrm: [], uv: [], conf: [] };
  /** Which staff a triangle belongs to — the same span table the boat, wharf,
   *  sign and yard layers keep, and for the same reason. */
  const spans = [];
  const cards = new Map();

  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`flagstaff: ${id} — ${why}`); continue; }
    out.records.push(record);
    out.census.records += 1;

    const pos = record.position_local_enu_m;
    const height = record.form?.height_m?.value;
    if (!Array.isArray(pos) || pos.length < 2 || !(height > 0)) {
      problems.push(`flagstaff: ${record.id} has no position or no height — not drawn`);
      out.census.refused += 1;
      continue;
    }
    const [E, N] = pos;
    const ground = terrain.surfaceHeight(E, N);
    if (!Number.isFinite(ground)) {
      problems.push(`flagstaff: ${record.id} stands off the heightfield — not drawn`);
      out.census.refused += 1;
      continue;
    }
    const butt = record.form?.butt_diameter_m?.value ?? 0.34;
    const truck = record.form?.truck_diameter_m?.value ?? 0.16;
    const mastLevel = LEVEL[record.existence?.confidence] ?? 0;

    const from = buf.pos.length / 9;
    pushMast(buf, E, -N, ground - BUTT_SINK_M, ground + height, butt, truck, mastLevel);

    const flag = record.flag ?? {};
    if (flag.flying?.value) {
      const hoist = flag.hoist_m?.value ?? 2.6;
      const fly = flag.fly_m?.value ?? 4.9;
      pushFlag(buf, E, -N, ground + height - TRUCK_DROP_M, hoist, fly, truck / 2,
        LEVEL[flag.flying?.confidence] ?? 1);
      out.census.flags += 1;
    }
    spans.push({ id: record.id, from, to: buf.pos.length / 9 });
    cards.set(record.id, cardRecordFor(record));

    record._drawn = {
      ground_y_m: ground,
      head_y_m: ground + height,
      triangles: buf.pos.length / 9 - from,
    };
    out.staffs.push(record);
    out.census.staffs += 1;
  }

  if (!buf.pos.length) {
    if (out.census.records) {
      problems.push('flagstaff: the record loaded and no mast was drawn');
    }
    return out;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(buf.nrm, 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute(buf.uv, 2));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.computeBoundingSphere();

  const tex = paintAtlas();
  const mat = new THREE.MeshStandardMaterial({
    map: tex,
    roughness: 0.88,
    metalness: 0.0,
    side: THREE.DoubleSide,   // bunting is cloth, and a flag has two faces
  });
  mat.name = 'flagstaff-atlas';
  confidence?.patch(mat);
  // Its own program cache key — the T-0053 hazard: two patched materials that
  // agree on their other parameters share one compiled program, silently.
  mat.customProgramCacheKey = () => 'chicago4d-flagstaff';

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'flagstaff';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  group.userData.census = out.census;

  const raycaster = new THREE.Raycaster();
  /** The mast under the crosshair, with its own card record. */
  out.pickAt = (ndc, camera) => {
    if (!camera) return null;
    raycaster.setFromCamera(ndc ?? new THREE.Vector2(0, 0), camera);
    raycaster.far = Math.max(400, camera.position.y * 4);
    const hits = raycaster.intersectObject(mesh, false);
    if (!hits.length) return null;
    const hit = hits[0];
    const span = spans.find((sp) => hit.faceIndex >= sp.from && hit.faceIndex < sp.to);
    if (!span) return null;
    return {
      id: span.id,
      record: cards.get(span.id) ?? null,
      point: hit.point.clone(),
      distance: hit.distance,
    };
  };

  out.dispose = () => { geo.dispose(); mat.dispose(); tex.dispose(); };
  return out;
}
