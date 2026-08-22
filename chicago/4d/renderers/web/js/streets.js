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
// R-BUG4. Bisection steps used to find how far a panel's dry ground reaches
// before the water mask starts. Six halvings of a 5.25 m half-width settle to
// ~8 cm, which is finer than the heightfield the mask is sampled from, so more
// steps would be reporting precision the mask does not have.
const CLIP_STEPS = 6;
// A trimmed panel narrower than this is dropped rather than drawn: below about
// a metre it is no longer a road anybody could walk down, and a sliver at the
// waterline would be a claim rather than a rendering.
const MIN_PANEL_W_M = 1.0;
// T-0110. A panel is allowed to miss the ground between its own vertices by
// this much before it is subdivided; each subdivision halves the panel both
// ways, to at most 2^MAX_DRAPE_LEVEL pieces per axis (0.28 m along a 2.25 m
// step). The tolerance is the LIFT_M scale on purpose: a miss under it stays
// inside what the polygon offset already absorbs, so refining past it would
// spend triangles the picture cannot show. Measured on the shipped field, the
// whole town settles for +9k triangles (~1.5 % of the 'light' ceiling) and
// only bridge-approach and bank panels refine at all.
const DRAPE_TOL_M = 0.03;
const MAX_DRAPE_LEVEL = 3;
const LEVEL = { attested: 0, inferred: 0.5, reconstructed: 1 };

/**
 * WHY A ROAD READS AT ALL — R-BUG2, and the two separate faults behind it.
 *
 * The owner reported roads that "disappear in places, and when you fly over
 * them you lose them". Three mechanisms were proposed; the harness measured
 * them at unoccluded road pixels (see `roadContrast()` in
 * `tools/smoke_renderer.mjs`), and only two of the three are real.
 *
 * REFUTED — mip-averaged alpha falling under `alphaTest`. Plausible, and the
 * shape of the v74 treeline bug, but turning mipmaps OFF made every band WORSE
 * (south_water 250-600 m: 22 % of probes reached the screen with mips, 6 %
 * without). The mip chain is holding a sub-pixel ribbon together, not erasing
 * it. `minFilter` is left alone.
 *
 * FAULT 1, at eye level and at range — THE DEPTH FIGHT. A road 250-600 m out
 * along South Water Street was unoccluded, in front of the camera, and changed
 * the picture by **0.3 L\*** (14 % of probes perceptible). One unit of polygon
 * offset is nothing once depth precision has degraded that far, so the coplanar
 * terrain won the test in patches — the reported "in places". Deepening the
 * offset alone took that band to **3.3 L\* / 71 %**.
 *
 * FAULT 2, from the air — THE ROAD IS 4 % OPAQUE. From `from_above` the ribbon
 * is many pixels wide, unoccluded, and wins the depth test, and it still moved
 * the picture by **1.1 L\*** with ZERO probes perceptible at 100-250 m. The
 * cause is the authored alpha: for a lightly worn track `body` was
 * `0.08 + ruts*0.54 - crown*0.04`, so away from the two wheel ruts the surface
 * was 8 % earth over 92 % prairie, and at the crown 4 %. A road nobody can see
 * is not a subtle road. The baselines below are raised so the FAINTEST surface
 * still reads, while the ordering graded > worn > light — which is a modelled
 * attribute with its own confidence — is preserved. Recorded in
 * `docs/LIBERTIES.md`.
 *
 * FLOOR, for the thin end — a ribbon narrower than this many screen pixels has
 * its alpha scaled up in proportion, capped, so that a track receding to the
 * horizon fades rather than dropping out. Same principle as the
 * `MIN_SILHOUETTE_PX` floor in `trees.js`: never let a feature fall below the
 * pixel it needs to be seen at all. It binds only where the ribbon is thin —
 * from the air 0.02 of a wide road is nothing, so this is not what fixed
 * fault 2.
 *
 * ---------------------------------------------------------------------------
 * R-BUG3 — AND THE ROAD AT YOUR FEET. The owner reported, on the dev preview
 * with both fixes above already in, that the ruts read in the mid-distance and
 * the road is simply not there in the near field. Measured at a station
 * standing on a crossing (`roadContrast()` gained one, because neither gated
 * station stood on a road at all): 2-40 m scored **1.5 L\* with 30 % of probes
 * perceptible**, against 3.4 / 87 % in the very next band out. It now reads
 * **3.1 / 80 % on mobile and 3.2 / 60 % on desktop**, measured on the published
 * mirror.
 *
 * REFUTED — near-field sward occlusion, the parcel's prime suspect. Every one
 * of the near probes was UNOCCLUDED: the harness re-shoots its road markers
 * with the sward and the trees hidden, and the near band's marked count does
 * not move. No grass is hiding this road; the road is painting almost nothing.
 * The clearing corridor is therefore not the fault either, and neither is
 * touched here — widening one to win a contrast score would falsify a recorded
 * ground cover, which the parcel forbids and this fix does not need.
 *
 * FAULT — ALPHA IS A COVERAGE FRACTION, AND COVERAGE ONLY AVERAGES AT RANGE.
 * The authored alpha says what share of the ground is bare earth: 0.46 at the
 * crown of a graded track, 0.30 for a lightly worn one. Far off, one pixel
 * spans many patches and a blend is the right picture of that mixture. At your
 * feet one pixel spans ONE patch, which in life is either earth or grass, and
 * the blend instead paints a uniform wash of grass-with-a-hint-of-dirt. The
 * harness measures both ends of it: the same near probes rendered fully opaque
 * score **3.4 L\*** (4.3 desktop), so the contrast is there in the ribbon's own
 * colour and the shipped alpha was throwing well over half of it away. (The ground is genuinely darker
 * underfoot than at range — L\* 51.0 against 52.7-56.3 — so the near field has
 * less contrast to spend, which is why spending it all matters here.)
 *
 * THE LIFT, and what it does not do. Inside `NEAR_FULL_M` the alpha is scaled
 * by `NEAR_GAIN`, fading back to unity by `NEAR_FADE_M` — which is the outer
 * edge of the band the report is about, so every band the earlier gates hold
 * is arithmetically untouched. It is a GAIN, not a floor: graded > worn >
 * light is a modelled attribute with its own confidence and it survives
 * scaling. Nothing in `data/` moves, no recorded cover changes, and the mean
 * coverage the record states is still what the picture shows at the distance
 * where a mixture is what a pixel means. Recorded in `docs/LIBERTIES.md`.
 *
 * ---------------------------------------------------------------------------
 * R-A1 — THE ACCESSIBILITY AID, AND WHY IT IS ALLOWED TO EXIST.
 *
 * A user control that boosts road contrast converts a defect into a preference
 * and takes the pressure off fixing the default, which is why this was
 * deliberately deferred on 2026-08-14. It ships now because R-BUG3 made the
 * default correct on 2026-08-15: the near band scores 3.1 L\* of a measured
 * ceiling of 3.4 on mobile. The aid is layered ON a correct default; it is not
 * a substitute for one, and it must never be allowed to retire R-W2's textured
 * coverage, which is the honest fix for the ceiling itself.
 *
 * What it is: a viewing accommodation, like the units toggle. Contrast
 * sensitivity varies and a phone screen in sunlight is brutal — which is the
 * exact condition R-BUG3 was reported from. It is NOT a claim about how visible
 * an 1835 street was, and nothing in `data/` moves when it is used.
 *
 * THE DEFAULT IS OFF AND OFF IS ARITHMETICALLY THE OLD SHADER. `uRoadAid` is 0
 * unless a visitor moves the slider, and at 0 the two lines below reduce to
 * `min(a * 1.0, MAX_ALPHA)` — which is the statement that was already there.
 * That is the K24 constraint inherited whole: `tools/critic_shots.mjs`,
 * `tools/light_probe.mjs` and every band in `smoke_renderer.mjs` measure the
 * default, so a gate must not be passable by moving this control. The smoke
 * asserts all three halves of that — the uniform reads 0 with no stored
 * preference, raising it CHANGES the frame, and dropping it back restores the
 * frame — because a control that does not reach the render reports "no effect"
 * for the same reason a broken thermometer reports a steady temperature
 * (R-BUG1's `--no-sun-shadow`).
 *
 * WHAT IT COSTS AT MAXIMUM, stated rather than buried. `AID_GAIN` is
 * `1 / 0.24`: 0.24 is the faintest body alpha any surface authors (a lightly
 * worn track at its crown), so at full aid the faintest road reaches opaque —
 * which is exactly the ceiling R-BUG3 measured by forcing the near probes
 * opaque. Below maximum the gain is a scale and the graded > worn > light
 * ordering survives it, the same way it survives `NEAR_GAIN`. AT maximum every
 * surface saturates and that ordering is gone: the aid has stopped depicting a
 * modelled attribute and is drawing a road you can follow. That is the point of
 * it, and it is why the readout names the default rather than only a number.
 */
const MIN_TRACK_PX = 2.0;
const MAX_THIN_BOOST = 6.0;
const MAX_ALPHA = 0.92;
const NEAR_FULL_M = 15.0;
const NEAR_FADE_M = 40.0;
const NEAR_GAIN = 2.4;
// R-A1. The faintest authored body alpha is 0.28 - 0.04 = 0.24 (light worn
// earth at the crown); this takes that one surface to opaque at full aid.
const AID_GAIN = 1 / 0.24;

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

/**
 * T-0110 — THE ROAD MUST FOLLOW THE GROUND IT CLAIMS TO LIE ON.
 *
 * The owner reported, walking Kinzie Street onto the North Branch bridge an
 * hour after T-0046 raised its approach earthworks: the track "gets pixely and
 * you can see grass triangles and it ends with a black line and more grass."
 * Replayed against the committed heightfield, the mechanism is not the water
 * trim the ticket first suspected — the trims hold full width up both ramps —
 * it is that a panel was ONE planar quad, 2.25 m long and two vertices wide,
 * and an embankment is not planar. Between the corners the fill's crest rose
 * through the ribbon by up to **1.49 m** (west approach nose; 1.41 m east,
 * 1.09 m at the Dearborn drawbridge approach on North Water). The terrain is
 * opaque and wins the depth test, so everywhere it broke the surface the road
 * simply was not drawn: his green wedges, and his road ending short of the
 * deck. The smoke's `worstDrape` gate never saw it because it samples
 * VERTICES, and every vertex was perfectly draped.
 *
 * The fix is refinement, not flattening: where a panel's own vertices miss the
 * field between themselves by more than DRAPE_TOL_M, the panel subdivides —
 * halving both axes per level — and every new vertex samples
 * `terrain.surfaceHeight()` exactly as the corners always have. The module's
 * standing contract is untouched: the terrain is never edited, the walker
 * still stands on the same heightfield, and a level-0 panel emits byte-for-byte
 * the geometry this function always emitted, so the flat town (94 % of panels)
 * is arithmetically unchanged.
 *
 * Three refusals, all deliberate:
 * - A level is REJECTED if any of its new row centres or vertices lands on
 *   water. The R-BUG4 rule ("clip, don't paint a ford") binds interior
 *   vertices the same as corners, and the smoke's wet-vertex gate counts
 *   positions, not heights.
 * - A panel that touches ground OFF the heightfield grid stays at level 0.
 *   Out there `surfaceHeight()` answers a fallback constant, not a
 *   measurement, and refining against a constant would manufacture cliffs at
 *   the map border.
 * - Interior rows re-run the SAME dryReach trim as panel ends, so the drawn
 *   edge follows the waterline at the refined resolution instead of
 *   interpolating across it.
 *
 * Neighbouring panels can settle on different levels; the shared row's edge
 * vertices coincide exactly (same centreline point, same trim), and any
 * T-junction gap between interior columns is bounded by DRAPE_TOL_M — the
 * coarser panel's own acceptance test ran on that very row.
 */
function refinedPanel(terrain, a, b, ue, un, ends, dryReach) {
  const build = (level) => {
    const R = 1 << level;
    const rows = [];
    for (let r = 0; r <= R; r++) {
      const t = r / R;
      const pe = a[0] + (b[0] - a[0]) * t;
      const pn = a[1] + (b[1] - a[1]) * t;
      if (r > 0 && r < R && terrain.isWater(pe, pn)) return null;
      const reachL = r === 0 ? ends.aL : r === R ? ends.bL : dryReach(pe, pn, ue, un);
      const reachR = r === 0 ? ends.aR : r === R ? ends.bR : dryReach(pe, pn, -ue, -un);
      const row = [];
      for (let c = 0; c <= R; c++) {
        const f = c / R;
        // Rounded to the float32 the position buffer will store, and sampled
        // AT that value: on the ~1:1 ramp flanks the double-precision position
        // and its stored float32 stand on ground ~1e-5 m apart, which is
        // exactly the drape budget the smoke holds vertices to.
        const e = Math.fround((pe + ue * reachL) * (1 - f) + (pe - ue * reachR) * f);
        const n = Math.fround((pn + un * reachL) * (1 - f) + (pn - un * reachR) * f);
        const interior = (r > 0 && r < R) || (c > 0 && c < R);
        if (interior && terrain.isWater(e, n)) return null;
        row.push([e, n, terrain.surfaceHeight(e, n) + LIFT_M]);
      }
      rows.push(row);
    }
    return rows;
  };
  // Worst |field − ribbon| between the grid's own vertices, probed at the
  // half-points of every sub-quad. Off-grid probes are skipped: no measurement,
  // no verdict.
  const residual = (rows) => {
    let worst = 0;
    for (let r = 0; r < rows.length - 1; r++) {
      for (let c = 0; c < rows[r].length - 1; c++) {
        const q = [rows[r][c], rows[r][c + 1], rows[r + 1][c], rows[r + 1][c + 1]];
        for (let i = 0; i <= 2; i++) {
          for (let j = 0; j <= 2; j++) {
            const ft = i / 2;
            const fs = j / 2;
            const e = (q[0][0] * (1 - fs) + q[1][0] * fs) * (1 - ft)
              + (q[2][0] * (1 - fs) + q[3][0] * fs) * ft;
            const n = (q[0][1] * (1 - fs) + q[1][1] * fs) * (1 - ft)
              + (q[2][1] * (1 - fs) + q[3][1] * fs) * ft;
            if (!terrain.inBounds(e, n)) continue;
            const y = (q[0][2] * (1 - fs) + q[1][2] * fs) * (1 - ft)
              + (q[2][2] * (1 - fs) + q[3][2] * fs) * ft;
            worst = Math.max(worst, Math.abs(terrain.surfaceHeight(e, n) + LIFT_M - y));
          }
        }
      }
    }
    return worst;
  };
  let grid = build(0);
  if (grid.some((row) => row.some(([e, n]) => !terrain.inBounds(e, n)))) return grid;
  let level = 0;
  let miss = residual(grid);
  while (miss > DRAPE_TOL_M && level < MAX_DRAPE_LEVEL) {
    const next = build(level + 1);
    if (!next) break;
    grid = next;
    level += 1;
    miss = residual(grid);
  }
  return grid;
}

function addRecord(buffers, record, terrain, stats) {
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
    const ue = -dn / length;
    const un = de / length;

    // R-BUG4. The CENTRELINE test still drops the panel: a road whose centre is
    // in the river is a crossing, and a crossing is a bridge's job, not a
    // ribbon's.
    if (terrain.isWater(a[0], a[1]) || terrain.isWater(b[0], b[1])) {
      along += length;
      continue;
    }
    // But the EDGE test used to drop it too, and that was the wrong instrument
    // for the right aim. Its comment said it kept a bank road from painting
    // over water just because its legal corridor reached it — true, and the
    // remedy for "do not paint over water" is to CLIP the panel at the
    // waterline, not to delete it, because deleting takes the DRY HALF with it.
    // Owner-reported from South Water Street as a clean-edged green hole
    // punched through the roadway; replayed against the shipped mask it was
    // 13 panels and ~30 m of roadway removed while the centreline was dry land
    // a visitor can stand on, and 14.2 % of Kinzie Street.
    //
    // So each end is trimmed on each side INDEPENDENTLY: walk out from the dry
    // centreline to the recorded half-width and keep the furthest dry reach.
    // Asymmetric on purpose — a bank road is wet on one side only, and
    // shrinking it symmetrically would throw away the dry verge as well.
    const dryReach = (e0, n0, se, sn) => {
      if (!terrain.isWater(e0 + se * half, n0 + sn * half)) return half;
      let lo = 0;
      let hi = half;
      for (let k = 0; k < CLIP_STEPS; k++) {
        const mid = (lo + hi) * 0.5;
        if (terrain.isWater(e0 + se * mid, n0 + sn * mid)) hi = mid;
        else lo = mid;
      }
      return lo;
    };
    const aL = dryReach(a[0], a[1], ue, un);
    const aR = dryReach(a[0], a[1], -ue, -un);
    const bL = dryReach(b[0], b[1], ue, un);
    const bR = dryReach(b[0], b[1], -ue, -un);
    // A panel trimmed to nothing is a panel whose centreline is dry by a hair
    // and whose surroundings are not. Drawing a sliver there would be a claim
    // about a road too narrow to walk on, so it is dropped and counted.
    if (aL + aR < MIN_PANEL_W_M || bL + bR < MIN_PANEL_W_M) {
      along += length;
      continue;
    }
    // T-0110: a grid of (level+1)² draped vertices — one quad at level 0,
    // which is this function's historical output exactly.
    const grid = refinedPanel(terrain, a, b, ue, un, { aL, aR, bL, bR }, dryReach);
    const rows = grid.length - 1;
    const cols = grid[0].length - 1;
    const base = buf.pos.length / 3;
    for (let r = 0; r <= rows; r++) {
      // Across first, distance along second. The texture repeats every eight
      // metres, long enough that its ruts read as travel rather than corduroy.
      const v = (along + (length * r) / rows) / 8;
      for (let c = 0; c <= cols; c++) {
        const [e, n, y] = grid[r][c];
        buf.pos.push(e, y, -n);
        buf.conf.push(confidence);
        buf.uv.push(c / cols, v);
      }
    }
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const i00 = base + r * (cols + 1) + c;
        const i10 = i00 + cols + 1;
        buf.idx.push(i00, i10, i00 + 1, i00 + 1, i10, i10 + 1);
      }
    }
    stats.panels += 1;
    if (rows > 1) stats.refinedPanels += 1;
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
      // Baselines raised for R-BUG2 fault 2 — see the note at the top of the
      // file. The modulation shape (ruts up, crown down) and the graded > worn
      // > light ordering are unchanged; only the floor each surface starts
      // from moved, from 0.54/0.20/0.08 to 0.54/0.38/0.28. The faintest
      // surface now bottoms out at 0.24 rather than 0.04.
      const body = graded
        ? 0.54 + ruts * 0.25 - crown * 0.08
        : light ? 0.28 + ruts * 0.54 - crown * 0.04
          : 0.38 + ruts * 0.55 - crown * 0.08;
      image.data[i + 3] = Math.round(255 * edge * Math.max(0, Math.min(MAX_ALPHA, body)));
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

function meshOf(surface, buf, confidence, aidUniform) {
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
    // R-BUG2 fault 1. -1/-1 is a fraction of a depth unit and the terrain won
    // the test in patches beyond ~250 m. Deep enough to hold at the far end of
    // the town, shallow enough that the ribbon never lifts off its own drape —
    // the vertices are untouched, and `worstDrape` still gates them.
    // R-BUG3 deepened it again, and the reason it had to is the same reason
    // R-BUG2's number was too shallow: it was tuned until the bands AT THE TWO
    // STATIONS THEN GATED passed. Standing on Lake Street at Market, desktop,
    // 100-250 m, the ribbon lost the test again — 23 probes where the marker
    // pass is frontmost and the road changes the picture by 0.0 L\*, opaque or
    // not, which is a depth fight and nothing else. These are the marker's own
    // values, so "the road's surface is the frontmost thing here" and "the road
    // is drawn here" now mean the same thing rather than differing by a tuning
    // constant. The vertices are still untouched and `worstDrape` still gates
    // them to 1e-5 m.
    polygonOffsetFactor: -8,
    polygonOffsetUnits: -32,
  });
  mat.name = `street-${surface}`;
  // R-BUG2 floor. `u` runs 0 -> 1 exactly across the track, so 1/fwidth(u) IS
  // the ribbon's width in screen pixels — no uniform, no viewport to keep in
  // sync, and correct under any field of view. Set BEFORE confidence.patch(),
  // which chains whatever it finds here rather than replacing it.
  mat.onBeforeCompile = (shader) => {
    shader.uniforms.uRoadAid = aidUniform;
    shader.fragmentShader = `uniform float uRoadAid;\n${shader.fragmentShader}`.replace(
      '#include <map_fragment>',
      `#include <map_fragment>
      {
        float trackPx = 1.0 / max(fwidth(vMapUv.x), 1e-6);
        float thin = clamp(${MIN_TRACK_PX.toFixed(1)} / trackPx, 1.0, ${MAX_THIN_BOOST.toFixed(1)});
        diffuseColor.a = min(diffuseColor.a * thin, ${MAX_ALPHA.toFixed(2)});
        // R-BUG3. Distance from the eye, not a pixel count: the band this
        // answers is metres from the walker and must not mean something
        // different at 390 px than at 1280.
        float eyeM = length(vViewPosition);
        float near = 1.0 - smoothstep(${NEAR_FULL_M.toFixed(1)}, ${NEAR_FADE_M.toFixed(1)}, eyeM);
        float gain = mix(1.0, ${NEAR_GAIN.toFixed(2)}, near);
        diffuseColor.a = min(diffuseColor.a * gain, ${MAX_ALPHA.toFixed(2)});
        // R-A1, and it is LAST on purpose: the aid scales whatever the
        // recorded surface and the two fixes above arrived at, so it can never
        // change which road is fainter than which. At uRoadAid == 0 this is
        // min(a * 1.0, ${MAX_ALPHA.toFixed(2)}) — the line immediately above,
        // re-applied — so the default frame is the frame that shipped before
        // the control existed.
        diffuseColor.a = min(
          diffuseColor.a * mix(1.0, ${AID_GAIN.toFixed(4)}, uRoadAid),
          mix(${MAX_ALPHA.toFixed(2)}, 1.0, uRoadAid));
      }`,
    );
  };
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
  // T-0110. With refinement a panel is no longer a fixed six indices, so the
  // smoke's panel-accounting gate reads these counters instead of index math.
  const stats = { panels: 0, refinedPanels: 0 };
  for (const record of prepared) addRecord(buffers, record, terrain, stats);
  const resources = [];
  // R-A1. One uniform object shared by every surface's material, so the aid
  // cannot end up applied to the graded tracks and not the worn ones.
  const aidUniform = { value: 0 };
  for (const [surface, buf] of buffers) {
    const built = meshOf(surface, buf, confidence, aidUniform);
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
    stats,
    status,
    hitsAt,
    blocksGrowth,
    /**
     * R-A1. The road-legibility aid, 0 (off, the default) to 1 (the faintest
     * surface opaque). A uniform, so it costs no recompile and takes effect on
     * the next frame; the gates read `legibilityAid` to prove it is 0 when
     * nobody has touched it.
     */
    setLegibilityAid(v) {
      const next = Math.max(0, Math.min(1, Number(v) || 0));
      aidUniform.value = next;
      return next;
    },
    get legibilityAid() { return aidUniform.value; },
    dispose() {
      for (const r of resources) {
        r.geo.dispose();
        r.mat.dispose();
        r.map.dispose();
      }
    },
  };
}
