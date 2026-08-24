/**
 * wharves.js — the river docks and the South Water landings.
 *
 * Since T-0062 the record carries more than the two warehouse docks T-0041
 * derived: the owner's 2026-08-18 ruling ("you can add more docks!") added
 * reconstructed South Water merchant landings, stated per record and drawn by
 * this same layer wherever the traced 1834 bank reaches them. Nothing below
 * changed for it — the record grew, the drawing didn't.
 *
 * WHY THIS FILE EXISTS. `docs/ROADMAP.md` K5 (e) asks for *"docks/wharves at the
 * forwarding houses"*, and ticket T-0041 is that clause. Two records in this
 * dataset state a dock and both state it in the same sentence — *"Kinzie &
 * Hunter and Dole & Newberry each had a warehouse with its dock along the river
 * front"* — and until this layer existed both carried `geometry: "absent"` over
 * it: the strongest confidence chip the project hands out, in front of a bare
 * bank. `tools/generate_river_wharves.py` answers "which frontage" with a rule
 * and derives the outline from the traced bank, the committed footprint and the
 * committed heightfield; `tools/check.sh` re-derives its record byte for byte;
 * and this file only draws what that record says.
 *
 * WHAT IT WILL AND WILL NOT DO.
 *
 *  * THE DECK'S HEIGHT IS THE TERRAIN'S, NOT THE RECORD'S. It is sampled along
 *    the landward edge at load — the bridge's lesson (T-0001), where a deck
 *    height authored beside the mesh instead of taken from it stood a walker
 *    1.8 m over the planks. Where the bank is lower than the record's freeboard
 *    floor above the water plane, the deck holds the floor instead, because a
 *    working deck stands clear of its own river.
 *  * IT STANDS ON THE BED IT IS OVER. Each crib bent is stepped down to
 *    `terrain.surfaceHeight` at its own point, so the crib meets the channel
 *    floor the heightfield draws rather than a flat guess — which is the only
 *    reason a structure standing in water can be drawn honestly at all.
 *  * IT IS A WALK SURFACE (T-0058), and the route is the one the plank walks
 *    already take. `walkHeight()` puts a wading barrier over open water, so
 *    until now a visitor saw the wharf from the bank and could not step onto
 *    it. A deck does not need a structure record to be stood on — since T-0119
 *    a layer publishes `{ id, y, pts }` and `main.js` appends it to the same
 *    registry the bridges use, which is the one mechanism in this project for
 *    "the visitor is standing on something that is not the heightfield".
 *  * AND THE LANDWARD BAND IS AN APRON, not a slab hanging over the bank. The
 *    record already ties the deck `heel_in_m` back into the bank; what was
 *    drawn there was a level platform, so its landward edge stood 0.32-0.71 m
 *    clear of the ground with daylight under it, and the walker's 0.35 m
 *    step-up rule refused to board FIVE of the seven. That band now ramps from
 *    the bank up to the platform. It invents NO new number — the run is the
 *    record's own `heel_in_m` and the rise is whatever the terrain leaves under
 *    it — and it is the same crib timber below. docs/LIBERTIES.md L182.
 *  * NO VESSEL, NO CARGO, NO CRANE, NO GANGWAY, NO NAME. The record says so and
 *    this file keeps it: the schooner cheered at one of these two wharves in
 *    1834 is not drawn, because a hull would be a larger invention than the
 *    deck it lay at.
 *  * It is ONE draw call for the whole layer, like the fences, the boards and
 *    the goods.
 *  * It marks itself. Every vertex carries `_confidence` at `reconstructed`,
 *    because the SIZE of these docks is invented — the weakest thing deciding
 *    that the vertex exists at all. So the whole layer disappears when a visitor
 *    hides `reconstructed`, and the warehouses go back to standing at an empty
 *    bank. That is the truthful behaviour.
 *  * It answers a pick. A wharf belongs to the warehouse it serves, so clicking
 *    it opens that building's card — the same contract the boards and the goods
 *    keep.
 */

import * as THREE from 'three';

/** attested · inferred · reconstructed, as the confidence view reads them. */
const LEVEL = { attested: 0, documented: 0, inferred: 0.5, reconstructed: 1 };

/** The vertical datum: the summer-1835 water surface, the same zero terrain.js
 *  draws the river plane at. Imported as a literal rather than from terrain.js
 *  so this layer keeps working if it is ever mounted without one. */
const WATER_Y = 0;

/**
 * HOW THE OUTLINE BECOMES TRIANGLES, and why these numbers are not the record's.
 * The record owns everything that is a CLAIM about the town — where the deck
 * stands, how far out its face reaches, how thick the planks are, how high it
 * holds above the water. What is here is only the grain of the drawing: how many
 * bents the crib is stepped into, how many posts stand on it, how far the crib
 * is inset under the deck it carries. Same division `yard.js` makes between a
 * barrel's girth and the number of staves it is drawn with.
 */
const BENT_M = 2.5;          // the crib is stepped at this spacing, along its run
const CRIB_INSET_M = 0.10;   // the crib sits this far in under the deck's edge
const CRIB_FOOT_M = 0.35;    // and is buried this far into the bed it stands on
const POSTS = 3;             // snubbing posts along the face
const POST_INSET_M = 0.45;   // set back this far from the face's own edge

/**
 * The layer's timber tone. Deliberately NOT the goods' warm cooperage colour and
 * not the fences' weathered grey: a dock is heavy structural timber standing in
 * water, wet at the foot and silvered on the deck, so it reads darker and cooler
 * than both. As in `signage.js`: `ColorManagement.enabled` is true and `setHex`
 * reads sRGB, so this is the hex, not a linear triple copied from a generator.
 */
const WHARF_COLOUR = 0x6f6a5e;

/* -------------------------------------------------------------------------- */
/* primitives                                                                  */
/* -------------------------------------------------------------------------- */

/**
 * One box, 12 triangles, flat-shaded from its own face normals. `u` is the
 * horizontal unit vector along the box's length; up is world Y always.
 * Deliberately the same helper shape as the enclosure, signage and yard layers'
 * — four layers drawing timber the same way is one thing to reason about.
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
 * One triangle with the normal its own three vertices imply.
 *
 * `pushBox` above can take a face normal as a constant because every box it
 * draws is axis-true in its own frame. The deck is not: its landward band is
 * inclined by whatever the terrain leaves under it, so a constant normal would
 * light the apron as though it were flat. Points are world `[x, y, z]`.
 */
function pushTri(buf, a, b, c, level) {
  const ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2];
  const vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
  let nx = uy * vz - uz * vy;
  let ny = uz * vx - ux * vz;
  let nz = ux * vy - uy * vx;
  const len = Math.hypot(nx, ny, nz) || 1;
  nx /= len; ny /= len; nz /= len;
  for (const p of [a, b, c]) {
    buf.pos.push(p[0], p[1], p[2]);
    buf.nrm.push(nx, ny, nz);
    buf.conf.push(level);
  }
}

/**
 * A four-cornered slab of a stated thickness whose TOP may be a warped plane —
 * each corner carries its own height. Used for the deck, which is level over
 * the water and inclined over the bank.
 *
 * `corners` are local ENU `[e, n]` in ring order and `tops` their heights; the
 * ring is reversed if it is not counter-clockwise in (e, n), which is what puts
 * the top face's normal up in a world of (E, up, −N).
 */
function pushSlab(buf, corners, tops, thickness, level) {
  let ring = corners.map((p, i) => [p[0], p[1], tops[i]]);
  let area = 0;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    area += (ring[j][0] * ring[i][1]) - (ring[i][0] * ring[j][1]);
  }
  if (area < 0) ring = ring.slice().reverse();
  const top = ring.map((p) => [wx(p[0]), p[2], wz(p[1])]);
  const bot = top.map((p) => [p[0], p[1] - thickness, p[2]]);
  for (let i = 2; i < top.length; i += 1) {
    pushTri(buf, top[0], top[i - 1], top[i], level);
    pushTri(buf, bot[0], bot[i], bot[i - 1], level);
  }
  for (let i = 0; i < top.length; i += 1) {
    const j = (i + 1) % top.length;
    pushTri(buf, top[i], bot[i], bot[j], level);
    pushTri(buf, top[i], bot[j], top[j], level);
  }
}

/* -------------------------------------------------------------------------- */
/* the wharf                                                                   */
/* -------------------------------------------------------------------------- */

/** Local ENU (e, n) to the renderer's world (x, z). World is (E, up, −N). */
const wx = (e) => e;
const wz = (n) => -n;

function groundAt(terrain, e, n) {
  const y = terrain.surfaceHeight(e, n);
  return Number.isFinite(y) ? y : null;
}

/**
 * A run of crib wall, stepped into bents that each reach the bed under them.
 *
 * `a` and `b` are the run's two ends in local ENU, on the CENTRELINE of the
 * wall; the wall is `width` across and hangs from `topAt(e, n)` down to the
 * bed. A bent whose bed sample is above the deck is skipped rather than drawn
 * inside out — over dry ground the deck sits on the ground and needs no crib.
 *
 * `topAt` is a FUNCTION rather than a height because the deck's landward band
 * is inclined (T-0058): a constant top would leave the crib standing proud of
 * the apron it carries, which is the same class of fault as a deck floating
 * over its own bank.
 */
function pushCribRun(buf, a, b, width, topAt, terrain, level) {
  const de = b[0] - a[0];
  const dn = b[1] - a[1];
  const run = Math.hypot(de, dn);
  if (run < 0.05) return 0;
  const ue = de / run;
  const un = dn / run;
  const bents = Math.max(1, Math.round(run / BENT_M));
  const step = run / bents;
  let drawn = 0;
  for (let i = 0; i < bents; i += 1) {
    const t = (i + 0.5) * step;
    const e = a[0] + ue * t;
    const n = a[1] + un * t;
    const bed = groundAt(terrain, e, n);
    if (bed === null) continue;
    const deckY = topAt(e, n);
    const foot = Math.min(bed - CRIB_FOOT_M, deckY - 0.25);
    const h = deckY - foot;
    if (h <= 0.05) continue;
    pushBox(buf, wx(e), foot + h / 2, wz(n), ue, -un,
      step / 2, width / 2, h / 2, level);
    drawn += 1;
  }
  return drawn;
}

/**
 * One wharf: the deck slab, the crib under its face and its two ends, and the
 * snubbing posts. Returns the number of vertices it emitted, or 0 if the record
 * could not be stood anywhere — which is always a recorded problem and never a
 * silently invented dock.
 */
function buildWharf(buf, w, form, terrain, level, problems) {
  const quad = w.deck_quad_local_enu_m;
  if (!Array.isArray(quad) || quad.length !== 4) {
    problems.push(`wharves: ${w.structure_id} has no deck outline — nothing is drawn`);
    return 0;
  }
  const [heelL, heelR, faceR, faceL] = quad;
  // The deck's own axes, taken from the outline rather than from the record's
  // tangent: if the two ever disagreed the outline is what a visitor sees.
  const alongE = heelR[0] - heelL[0];
  const alongN = heelR[1] - heelL[1];
  const length = Math.hypot(alongE, alongN);
  const ue = alongE / (length || 1);
  const un = alongN / (length || 1);
  const outE = faceL[0] - heelL[0];
  const outN = faceL[1] - heelL[1];
  const width = Math.hypot(outE, outN);
  if (!(length > 0.5 && width > 0.5)) {
    problems.push(`wharves: ${w.structure_id}'s deck outline is degenerate — nothing is drawn`);
    return 0;
  }
  const oe = outE / width;
  const on = outN / width;

  // THE DECK TOP IS THE GROUND'S. Sampled at both heel corners and at the middle
  // of the landward edge, so a deck tying into a bank that falls away along its
  // length still meets the highest ground it touches rather than floating over
  // the rest of it. Never below the record's freeboard floor over the water.
  const heelMid = [(heelL[0] + heelR[0]) / 2, (heelL[1] + heelR[1]) / 2];
  const samples = [heelL, heelMid, heelR]
    .map((p) => groundAt(terrain, p[0], p[1]))
    .filter((y) => y !== null);
  if (!samples.length) {
    problems.push(`wharves: ${w.structure_id} has no ground under its landward edge `
      + '— no wharf is drawn');
    return 0;
  }
  const deckY = Math.max(...samples, WATER_Y + form.freeboard);

  /**
   * THE BOARDING APRON (T-0058). The deck top is the freeboard floor at all
   * seven landings, because the 1834 bank is 0.17-0.58 m above the water at
   * every one of them — so a level slab across the whole outline stands
   * 0.32-0.71 m clear of the ground its landward band is supposed to tie into.
   * That is a step nobody can take (WALK.stepUp is 0.35 m) and a slab with
   * daylight under it.
   *
   * So the landward `heel_in_m` of the deck is drawn as an inclined apron,
   * running from the ground at its own landward lip up to the platform at the
   * bank foot. NOTHING NEW IS INVENTED: the run is the record's own heel, the
   * rise is whatever the terrain leaves under it, and the lip takes the LOWEST
   * of the three ground samples along that edge so the apron never rises to
   * meet a visitor — where the bank is higher the ground simply wins, which is
   * what `surfaceAt()` already does over land.
   */
  const lipY = Math.min(deckY - form.deckT, ...samples);
  const rise = deckY - lipY;
  const heelIn = Math.min(form.heelIn, width);
  const apron = rise > 0.02 && heelIn > 0.05;
  /** The deck top at a point, in metres landward-to-waterward across the band.
   *  Clamped at both ends: every caller today asks inside the outline, and a
   *  caller that ever asks outside it should get the deck's own edge rather
   *  than an extrapolated plane running off under the prairie. */
  const topAtS = (s) => (apron && s < heelIn
    ? lipY + rise * (Math.max(0, s) / heelIn) : deckY);
  /** How far (e, n) stands out from the landward edge, along the deck's normal. */
  const across = (e, n) => (e - heelL[0]) * oe + (n - heelL[1]) * on;
  const topAt = (e, n) => topAtS(across(e, n));
  const before = buf.pos.length;

  // the deck: the level platform over the water, and — where the bank is lower
  // than the platform — the apron that ties it into the ground behind it.
  const foot = (p) => [p[0] + oe * heelIn, p[1] + on * heelIn];
  const cx = (heelL[0] + heelR[0] + faceL[0] + faceR[0]) / 4;
  const cn = (heelL[1] + heelR[1] + faceL[1] + faceR[1]) / 4;
  if (apron) {
    const footL = foot(heelL);
    const footR = foot(heelR);
    pushSlab(buf, [heelL, heelR, footR, footL], [lipY, lipY, deckY, deckY],
      form.deckT, level);
    pushSlab(buf, [footL, footR, faceR, faceL], [deckY, deckY, deckY, deckY],
      form.deckT, level);
  } else {
    pushBox(buf, wx(cx), deckY - form.deckT / 2, wz(cn), ue, -un,
      length / 2, width / 2, form.deckT / 2, level);
  }

  // the crib: under the outer face and under both ends, inset so the deck
  // oversails it the way a planked deck oversails the timber carrying it. The
  // end runs start at the landward lip, so the apron is carried by the same
  // timber the platform is rather than resting on nothing.
  const inset = (p, de, dn) => [p[0] + de, p[1] + dn];
  const halfCrib = form.cribW / 2 + CRIB_INSET_M;
  const faceCentreL = inset(faceL, -oe * halfCrib, -on * halfCrib);
  const faceCentreR = inset(faceR, -oe * halfCrib, -on * halfCrib);
  const cribTop = (e, n) => topAt(e, n) - form.deckT;
  let bents = pushCribRun(buf, faceCentreL, faceCentreR, form.cribW,
    cribTop, terrain, level);
  bents += pushCribRun(buf,
    inset(heelL, ue * halfCrib + oe * halfCrib, un * halfCrib + on * halfCrib),
    inset(faceCentreL, ue * halfCrib, un * halfCrib),
    form.cribW, cribTop, terrain, level);
  bents += pushCribRun(buf,
    inset(heelR, -ue * halfCrib + oe * halfCrib, -un * halfCrib + on * halfCrib),
    inset(faceCentreR, -ue * halfCrib, -un * halfCrib),
    form.cribW, cribTop, terrain, level);
  if (!bents) {
    problems.push(`wharves: ${w.structure_id}'s deck stands on no crib — the bed `
      + 'under it could not be sampled');
  }

  // the snubbing posts, along the face
  for (let i = 0; i < POSTS; i += 1) {
    const t = ((i + 1) / (POSTS + 1) - 0.5) * (length - 2 * POST_INSET_M);
    const e = cx + ue * t + oe * (width / 2 - POST_INSET_M);
    const n = cn + un * t + on * (width / 2 - POST_INSET_M);
    pushBox(buf, wx(e), deckY + form.postH / 2, wz(n), ue, -un,
      form.postSide / 2, form.postSide / 2, form.postH / 2, level);
  }

  w._drawn = {
    deck_top_m: deckY,
    from_terrain: deckY > WATER_Y + form.freeboard + 1e-6,
    bents,
    /** The apron, or null where the bank already stood at the platform. */
    apron: apron ? {
      lip_m: lipY,
      rise_m: rise,
      run_m: heelIn,
      slope_deg: Math.atan2(rise, heelIn) * 180 / Math.PI,
    } : null,
    /** The step a visitor takes to board, measured at the landward lip. */
    board_step_m: Math.max(0, (apron ? lipY : deckY) - Math.min(...samples)),
    vertices: (buf.pos.length - before) / 3,
  };
  /**
   * THE SURFACE, in `decksFrom()`'s own shape plus a height function.
   *
   * `y` is the platform — the highest the deck reaches, which is what a deck
   * registry that only understands flat surfaces should be told. `heightAt` is
   * the whole truth, and it is the SAME `topAt` the slab above was drawn from,
   * so the plank a boot is on and the plank the mesh draws are one number
   * rather than two that agree until they do not. That is T-0001's finding,
   * which this layer's header has cited since it had no walk surface at all.
   */
  w._deck = {
    id: `${w.structure_id}__wharf`,
    y: deckY,
    pts: quad,
    heightAt: topAt,
  };
  return (buf.pos.length - before) / 3;
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
  return {
    deckT: v('deck_thickness_m', 0.14),
    freeboard: v('freeboard_m', 0.9),
    cribW: v('crib_width_m', 1.2),
    postSide: v('post_side_m', 0.22),
    postH: v('post_height_m', 0.75),
    // How far the deck ties back into the bank. Read here since T-0058 because
    // that band is the boarding apron, and its run is the record's number.
    heelIn: v('heel_in_m', 2.0),
  };
}

/**
 * @param {object} o dataBase (data/ root) · terrain · confidence · problems
 * @returns {Promise<{group: THREE.Group, records: object[], wharves: object[],
 *                    census: object, pickAt: function, dispose: function}>}
 */
export async function createWharves({
  dataBase, terrain, confidence = null, problems = [],
} = {}) {
  const group = new THREE.Group();
  group.name = 'wharves';
  const out = {
    group,
    records: [],
    wharves: [],
    /**
     * The decks as planting keep-outs, in `footprintsFrom()`'s own shape.
     * `flora.js` and `trees.js` refuse to plant inside a footprint plus a metre,
     * and a deck is a floor: a prairie dock growing up through the planks reads
     * as a hole in the model rather than as a wharf. Handed to the planters
     * ALONGSIDE the buildings' footprints and never merged into them — the
     * walker and the picker resolve a footprint by structure id, and a second
     * polygon under the same id would answer for the building.
     */
    keepOut: [],
    /**
     * THE DECKS A VISITOR STANDS ON (T-0058), in `decksFrom()`'s `{ id, y, pts }`
     * shape with a `heightAt` for the inclined landward band. `main.js` appends
     * them to the walker's registry — the same route the plank walks take
     * (T-0119), because there is exactly one mechanism in this project for
     * "the visitor is standing on something that is not the heightfield".
     */
    decks: [],
    census: { records: 0, wharves: 0, bents: 0, aprons: 0, refused: 0 },
    pickAt: () => null,
    dispose: () => {},
  };

  if (!dataBase || !terrain) {
    problems.push('wharves: no data base or no terrain — no dock is drawn');
    return out;
  }
  let index;
  try {
    index = await getJSON(new URL('wharves/index.json', dataBase));
  } catch (err) {
    // Degrade to NOTHING drawn plus a recorded problem, never to an invented
    // dock: the same contract the enclosure, signage, yard and vegetation
    // layers keep.
    problems.push(`wharves: ${err.message} — no dock is drawn`);
    return out;
  }
  const wanted = Array.isArray(index.wharves) ? index.wharves : [];
  const loaded = await Promise.all(wanted.map(async (w) => {
    if (!w.file) return [w.id, null, 'the manifest gave no file'];
    try {
      return [w.id, await getJSON(new URL(`wharves/${w.file}`, dataBase)), null];
    } catch (err) { return [w.id, null, err.message]; }
  }));

  const buf = { pos: [], nrm: [], conf: [] };
  /**
   * WHICH WAREHOUSE A TRIANGLE BELONGS TO. The layer is one draw call, so a hit
   * on the mesh knows nothing about which wharf it landed on unless each banks
   * the half-open range of triangles it emitted — the same span table
   * `signage.js` and `yard.js` keep, and for the same reason.
   */
  const spans = [];
  for (const [id, record, why] of loaded) {
    if (!record) { problems.push(`wharves: ${id} — ${why}`); continue; }
    out.records.push(record);
    out.census.records += 1;
    out.census.refused += (record.refused ?? []).length;
    const form = readForm(record);
    const level = LEVEL[record.existence?.confidence] ?? 1;
    for (const w of record.wharves ?? []) {
      const from = buf.pos.length / 9;
      if (!buildWharf(buf, w, form, terrain, LEVEL[w.confidence] ?? level, problems)) {
        continue;
      }
      spans.push({ id: w.structure_id, from, to: buf.pos.length / 9 });
      out.keepOut.push({ id: `${w.structure_id}__wharf`, pts: w.deck_quad_local_enu_m });
      if (w._deck) out.decks.push(w._deck);
      out.wharves.push(w);
      out.census.wharves += 1;
      out.census.bents += w._drawn?.bents ?? 0;
      out.census.aprons += w._drawn?.apron ? 1 : 0;
    }
  }
  if (!buf.pos.length) {
    if (out.census.records) {
      problems.push('wharves: the record loaded and not one dock was drawn');
    }
    return out;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(buf.pos, 3));
  geo.setAttribute('normal', new THREE.Float32BufferAttribute(buf.nrm, 3));
  geo.setAttribute('_confidence', new THREE.Float32BufferAttribute(buf.conf, 1));
  geo.computeBoundingSphere();

  const mat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(WHARF_COLOUR), roughness: 0.92, metalness: 0.0,
  });
  mat.name = 'wharf-timber';
  confidence?.patch(mat);
  /**
   * ITS OWN PROGRAM CACHE KEY, AND WHY THIS LINE IS NOT OPTIONAL. three caches a
   * compiled program under a key ending in `material.customProgramCacheKey()`,
   * whose default is the SOURCE TEXT of `onBeforeCompile` — so every material
   * `confidence.patch()` touches reports the same key, and two patched materials
   * that agree on their other program parameters share one program. The
   * enclosure layer was drawn in solid black by a building's shader that way,
   * with no page error and no warning; ticket T-0053 is the general fix.
   */
  mat.customProgramCacheKey = () => 'chicago4d-wharf-timber';

  const mesh = new THREE.Mesh(geo, mat);
  mesh.name = 'wharves';
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  group.add(mesh);
  group.userData.census = out.census;

  const raycaster = new THREE.Raycaster();
  /** The warehouse this dock belongs to, or null. Same ray budget as the boards. */
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
