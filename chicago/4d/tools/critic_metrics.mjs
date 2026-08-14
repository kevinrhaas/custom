/**
 * critic_metrics.mjs — the measurement half of the critic harness (RENDERING G0).
 *
 *   node tools/critic_metrics.mjs <file.png|dir> [...]     print JSON for each frame
 *
 * `tools/critic_shots.mjs` captures frames; this file turns them into the
 * numbers `docs/RENDERING.md` § 5 argues about, so a phase can prove its delta
 * instead of describing it. It reads PNGs and nothing else — which means the
 * SAME code measures a reference photograph and one of our frames. That matters
 * more than it sounds: every number in the 2026-08-10 prairie sweep came out of
 * a harness that no longer exists, so our figures and its reference figures were
 * never once produced by one implementation. Point this at a reference JPEG-
 * turned-PNG and the comparison is finally like for like.
 *
 * NO DEPENDENCIES, deliberately. The PNG decoder below is forty lines over
 * node:zlib, which is cheaper than owning an image library on a gate that has to
 * run in every sandbox.
 *
 * WHAT EACH NUMBER MEANS — the recipes are RENDERING Appendix B; the exact
 * thresholds are this file's, because Appendix B states the shape of each
 * measurement and not its constants. They are stated here rather than tuned per
 * call so that two runs, two phases and two years are comparable:
 *
 *   land/sky boundary   per column, the first row from the top whose next
 *                       `runPx` rows are ALL non-sky. Sky is blue-dominant
 *                       (B > R and B > G); ground is not, at any fog level this
 *                       renderer reaches. The sustained run is what separates
 *                       the GROUND line from the top of a tree: horizon timber
 *                       is two to four pixels tall and never satisfies it.
 *   horizon timber      in the band immediately above that line, a column counts
 *                       as timbered if a pixel there falls at least 3 luma below
 *                       — or 3 G−B above — the sky's own gradient EXTRAPOLATED
 *                       into the band from the twenty rows over it. A constant
 *                       sky reference does not work: the haze brightens steeply
 *                       toward the horizon and reports the air itself as trees.
 *   depth-band RMS      5x5 high-pass on Rec.709 luma over sRGB 0-255, in three
 *                       equal bands down from the median boundary. Collapse
 *                       toward the far band is the tell (§ 1 item 4).
 *   crown fine detail   over crown pixels (above the boundary, non-sky, and
 *                       G >= R so a clapboard gable is not a canopy):
 *                       RMS(I - blur3) / RMS(blur3 - blur9).
 *   shadow decile       mean CIE L* of the darkest tenth of ground pixels, plus
 *                       a count of literal (0,0,0) anywhere in frame.
 *   crown G-B           mean G-B over the brightest third of crown pixels, in
 *                       sRGB units, which is how § 1 item 8 is quoted.
 *   flower load         flower-hued / (plant-hued + flower-hued) over ground
 *                       pixels. Bright and saturated off-green, or near-white
 *                       and bright. HONEST LIMIT: a frame containing streets,
 *                       walls or roofs feeds them into the denominator or worse,
 *                       so this figure is only meaningful at the open-prairie
 *                       stations. It is reported everywhere and quoted there.
 *
 * Every threshold above is a measurement convention, not a claim about 1835.
 */

import zlib from 'node:zlib';
import fs from 'node:fs';
import path from 'node:path';

// ---- PNG ----------------------------------------------------------------- //

/** Decode an 8-bit non-interlaced PNG to `{ width, height, data }` RGBA. */
export function decodePng(buf) {
  if (buf.readUInt32BE(0) !== 0x89504e47) throw new Error('not a PNG');
  let pos = 8;
  let hdr = null;
  const idat = [];
  while (pos + 8 <= buf.length) {
    const len = buf.readUInt32BE(pos);
    const type = buf.toString('ascii', pos + 4, pos + 8);
    const body = buf.subarray(pos + 8, pos + 8 + len);
    if (type === 'IHDR') {
      hdr = {
        width: body.readUInt32BE(0),
        height: body.readUInt32BE(4),
        depth: body[8],
        color: body[9],
        interlace: body[12],
      };
    } else if (type === 'IDAT') idat.push(Buffer.from(body));
    else if (type === 'IEND') break;
    pos += 12 + len;
  }
  if (!hdr) throw new Error('no IHDR');
  if (hdr.depth !== 8 || hdr.interlace !== 0) {
    throw new Error(`unsupported PNG: depth ${hdr.depth}, interlace ${hdr.interlace}`);
  }
  const channels = { 0: 1, 2: 3, 4: 2, 6: 4 }[hdr.color];
  if (!channels) throw new Error(`unsupported PNG colour type ${hdr.color}`);

  const raw = zlib.inflateSync(Buffer.concat(idat));
  const { width: W, height: H } = hdr;
  const stride = W * channels;
  const out = new Uint8Array(W * H * 4);
  let prev = new Uint8Array(stride);
  let line = new Uint8Array(stride);
  let p = 0;
  for (let y = 0; y < H; y++) {
    const filter = raw[p++];
    for (let i = 0; i < stride; i++) {
      const x = raw[p + i];
      const a = i >= channels ? line[i - channels] : 0;
      const b = prev[i];
      const c = i >= channels ? prev[i - channels] : 0;
      let v;
      switch (filter) {
        case 0: v = x; break;
        case 1: v = x + a; break;
        case 2: v = x + b; break;
        case 3: v = x + ((a + b) >> 1); break;
        case 4: {
          const pa = Math.abs(b - c);
          const pb = Math.abs(a - c);
          const pc = Math.abs(a + b - 2 * c);
          v = x + (pa <= pb && pa <= pc ? a : pb <= pc ? b : c);
          break;
        }
        default: throw new Error(`bad PNG filter ${filter}`);
      }
      line[i] = v & 0xff;
    }
    p += stride;
    for (let x = 0; x < W; x++) {
      const s = x * channels;
      const d = (y * W + x) * 4;
      if (channels >= 3) {
        out[d] = line[s]; out[d + 1] = line[s + 1]; out[d + 2] = line[s + 2];
        out[d + 3] = channels === 4 ? line[s + 3] : 255;
      } else {
        out[d] = out[d + 1] = out[d + 2] = line[s];
        out[d + 3] = channels === 2 ? line[s + 1] : 255;
      }
    }
    const swap = prev; prev = line; line = swap;
  }
  return { width: W, height: H, data: out };
}

// ---- colour -------------------------------------------------------------- //

const SRGB_LIN = new Float32Array(256);
for (let i = 0; i < 256; i++) {
  const c = i / 255;
  SRGB_LIN[i] = c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
}

/** CIE L* (D65), 0..100. Lightness only — hue lives in the raw channels. */
export function labL(r, g, b) {
  const Y = 0.2126 * SRGB_LIN[r] + 0.7152 * SRGB_LIN[g] + 0.0722 * SRGB_LIN[b];
  const f = Y > 0.008856 ? Math.cbrt(Y) : 7.787 * Y + 16 / 116;
  return 116 * f - 16;
}

/** Hue in degrees and HSL-style saturation, from gamma-encoded sRGB. */
function hueSat(r, g, b) {
  const mx = Math.max(r, g, b);
  const mn = Math.min(r, g, b);
  const d = mx - mn;
  if (d === 0) return { hue: 0, sat: 0 };
  let h;
  if (mx === r) h = 60 * (((g - b) / d) % 6);
  else if (mx === g) h = 60 * ((b - r) / d + 2);
  else h = 60 * ((r - g) / d + 4);
  if (h < 0) h += 360;
  const l = (mx + mn) / 2 / 255;
  return { hue: h, sat: d / 255 / (1 - Math.abs(2 * l - 1) || 1) };
}

// ---- small array helpers ------------------------------------------------- //

/** Separable box blur of radius r over a W x H Float32Array. */
function boxBlur(src, W, H, r) {
  const tmp = new Float32Array(W * H);
  const out = new Float32Array(W * H);
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      let s = 0; let n = 0;
      for (let i = -r; i <= r; i++) {
        const xx = x + i;
        if (xx < 0 || xx >= W) continue;
        s += src[y * W + xx]; n++;
      }
      tmp[y * W + x] = s / n;
    }
  }
  for (let y = 0; y < H; y++) {
    for (let x = 0; x < W; x++) {
      let s = 0; let n = 0;
      for (let i = -r; i <= r; i++) {
        const yy = y + i;
        if (yy < 0 || yy >= H) continue;
        s += tmp[yy * W + x]; n++;
      }
      out[y * W + x] = s / n;
    }
  }
  return out;
}

function rms(values) {
  if (!values.length) return null;
  let s = 0;
  for (const v of values) s += v * v;
  return Math.sqrt(s / values.length);
}

function round(v, places = 3) {
  return v === null || !Number.isFinite(v) ? null : Number(v.toFixed(places));
}

// ---- the measurements ---------------------------------------------------- //

/**
 * Per-column land/sky boundary. Returns an Int32Array of row indices; `H` means
 * the column never reaches sustained ground (all sky, or a frame that is all
 * ground has boundary 0).
 */
export function landSkyBoundary(img, runPx) {
  const { width: W, height: H, data } = img;
  const run = runPx ?? Math.max(8, Math.round(H / 33));
  const boundary = new Int32Array(W).fill(H);
  const sky = new Uint8Array(W * H);
  for (let i = 0, p = 0; i < W * H; i++, p += 4) {
    sky[i] = data[p + 2] > data[p] && data[p + 2] > data[p + 1] ? 1 : 0;
  }
  for (let x = 0; x < W; x++) {
    let streak = 0;
    for (let y = H - 1; y >= 0; y--) {
      if (sky[y * W + x]) streak = 0;
      else {
        streak++;
        if (streak >= run) boundary[x] = y;
      }
    }
  }
  return { boundary, sky, run };
}

/**
 * Every § 1 / § 5 metric for one frame. `opts.horizonBandPx` and `opts.runPx`
 * exist for experiments; the gate quotes the defaults.
 */
export function measure(img, opts = {}) {
  const { width: W, height: H, data } = img;
  const { boundary, sky, run } = landSkyBoundary(img, opts.runPx);

  const luma = new Float32Array(W * H);
  const gb = new Float32Array(W * H);
  for (let i = 0, p = 0; i < W * H; i++, p += 4) {
    luma[i] = 0.2126 * data[p] + 0.7152 * data[p + 1] + 0.0722 * data[p + 2];
    gb[i] = data[p + 1] - data[p + 2];
  }

  // --- where the ground line sits, as one number for the banding ---------- //
  const sorted = [...boundary].sort((a, b) => a - b);
  const medianBoundary = sorted[Math.floor(sorted.length / 2)];
  const skyFraction = boundary.reduce((s, b) => s + Math.min(b, H), 0) / (W * H);

  // --- horizon timber ----------------------------------------------------- //
  const bandPx = opts.horizonBandPx ?? Math.max(3, Math.round(H / 100));
  const fitRows = 20;
  let timbered = 0; let measurable = 0;
  let timberedCentre = 0; let measurableCentre = 0;
  const c0 = Math.floor(W / 6);
  const c1 = Math.ceil(W * 5 / 6);
  for (let x = 0; x < W; x++) {
    const b = boundary[x];
    const bandTop = b - bandPx;
    if (b >= H || bandTop - fitRows < 0) continue;
    // Least squares on the sky ABOVE the band, extrapolated down into it: the
    // haze gradient is steep enough near the horizon that a flat reference
    // reports the air as timber.
    let sx = 0; let sy = 0; let sxx = 0; let sxyL = 0; let syG = 0; let sxyG = 0;
    for (let i = 0; i < fitRows; i++) {
      const y = bandTop - fitRows + i;
      const vL = luma[y * W + x];
      const vG = gb[y * W + x];
      sx += i; sxx += i * i; sy += vL; sxyL += i * vL; syG += vG; sxyG += i * vG;
    }
    const denom = fitRows * sxx - sx * sx;
    const slopeL = (fitRows * sxyL - sx * sy) / denom;
    const interceptL = (sy - slopeL * sx) / fitRows;
    const slopeG = (fitRows * sxyG - sx * syG) / denom;
    const interceptG = (syG - slopeG * sx) / fitRows;

    let hit = false;
    for (let y = bandTop; y < b; y++) {
      const t = y - (bandTop - fitRows);
      const predL = interceptL + slopeL * t;
      const predG = interceptG + slopeG * t;
      if (luma[y * W + x] <= predL - 3 || gb[y * W + x] >= predG + 3) { hit = true; break; }
    }
    measurable++;
    if (hit) timbered++;
    if (x >= c0 && x < c1) { measurableCentre++; if (hit) timberedCentre++; }
  }

  // --- depth-band high-pass RMS ------------------------------------------- //
  const blur5 = boxBlur(luma, W, H, 2);
  const bands = { far: [], mid: [], near: [] };
  const groundRows = H - medianBoundary;
  const bandH = Math.floor(groundRows / 3);
  if (bandH > 0) {
    const names = ['far', 'mid', 'near'];
    for (let k = 0; k < 3; k++) {
      const y0 = medianBoundary + k * bandH;
      const y1 = y0 + bandH;
      for (let y = y0; y < y1; y++) {
        for (let x = 0; x < W; x++) {
          const i = y * W + x;
          bands[names[k]].push(luma[i] - blur5[i]);
        }
      }
    }
  }

  // --- crowns ------------------------------------------------------------- //
  const crown = [];
  for (let x = 0; x < W; x++) {
    for (let y = 0; y < Math.min(boundary[x], H); y++) {
      const i = y * W + x;
      if (sky[i]) continue;
      const p = i * 4;
      if (data[p + 1] < data[p]) continue;   // foliage is never red-dominant
      crown.push(i);
    }
  }
  const blur3 = boxBlur(luma, W, H, 1);
  const blur9 = boxBlur(luma, W, H, 4);
  const fine = rms(crown.map((i) => luma[i] - blur3[i]));
  const coarse = rms(crown.map((i) => blur3[i] - blur9[i]));

  let crownGB = null;
  if (crown.length) {
    const lums = crown.map((i) => luma[i]).sort((a, b) => a - b);
    const cut = lums[Math.floor(lums.length * 2 / 3)];
    const lit = crown.filter((i) => luma[i] >= cut);
    crownGB = lit.reduce((s, i) => s + gb[i], 0) / (lit.length || 1);
  }

  // --- shadows ------------------------------------------------------------ //
  const groundL = [];
  let literalBlack = 0;
  for (let x = 0; x < W; x++) {
    for (let y = Math.min(boundary[x], H); y < H; y++) {
      const p = (y * W + x) * 4;
      groundL.push(labL(data[p], data[p + 1], data[p + 2]));
    }
  }
  for (let p = 0; p < W * H * 4; p += 4) {
    if (data[p] === 0 && data[p + 1] === 0 && data[p + 2] === 0) literalBlack++;
  }
  groundL.sort((a, b) => a - b);
  const decile = groundL.slice(0, Math.max(1, Math.floor(groundL.length / 10)));
  const darkestDecileL = decile.length
    ? decile.reduce((s, v) => s + v, 0) / decile.length : null;

  // --- flower load -------------------------------------------------------- //
  let plantHued = 0; let flowerHued = 0;
  for (let x = 0; x < W; x++) {
    for (let y = Math.min(boundary[x], H); y < H; y++) {
      const p = (y * W + x) * 4;
      const { hue, sat } = hueSat(data[p], data[p + 1], data[p + 2]);
      const L = labL(data[p], data[p + 1], data[p + 2]);
      if (hue >= 50 && hue < 180 && sat >= 0.08) { plantHued++; continue; }
      const chromatic = sat >= 0.25 && L >= 60;
      const white = sat <= 0.12 && L >= 75;
      if (chromatic || white) flowerHued++;
    }
  }

  return {
    width: W,
    height: H,
    conventions: { runPx: run, horizonBandPx: bandPx, fitRows },
    landSky: {
      medianBoundaryRow: medianBoundary,
      skyFraction: round(skyFraction, 4),
    },
    horizonTimber: {
      columnsMeasured: measurable,
      coverageAll: measurable ? round(timbered / measurable, 4) : null,
      coverageCentralTwoThirds: measurableCentre
        ? round(timberedCentre / measurableCentre, 4) : null,
    },
    depthBandHighPassRms: {
      far: round(rms(bands.far), 2),
      mid: round(rms(bands.mid), 2),
      near: round(rms(bands.near), 2),
      bandHeightPx: bandH,
    },
    crown: {
      pixels: crown.length,
      fineDetailRatio: fine !== null && coarse ? round(fine / coarse, 3) : null,
      fineRms: round(fine, 2),
      coarseRms: round(coarse, 2),
      sunlitGminusB: round(crownGB, 2),
    },
    shadow: {
      darkestDecileL: round(darkestDecileL, 2),
      literalBlackPixels: literalBlack,
    },
    flower: {
      plantHuedPixels: plantHued,
      flowerHuedPixels: flowerHued,
      load: plantHued + flowerHued ? round(flowerHued / (plantHued + flowerHued), 4) : null,
    },
  };
}

/** Measure one PNG on disk. */
export function measureFile(file, opts) {
  return measure(decodePng(fs.readFileSync(file)), opts);
}

// ---- CLI ----------------------------------------------------------------- //

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  if (!args.length) {
    console.error('usage: node tools/critic_metrics.mjs <file.png|dir> [...]');
    process.exit(2);
  }
  const files = [];
  for (const a of args) {
    const st = fs.statSync(a);
    if (st.isDirectory()) {
      for (const f of fs.readdirSync(a).sort()) {
        if (f.endsWith('.png')) files.push(path.join(a, f));
      }
    } else files.push(a);
  }
  const out = {};
  for (const f of files) out[path.basename(f, '.png')] = measureFile(f);
  console.log(JSON.stringify(out, null, 2));
}
