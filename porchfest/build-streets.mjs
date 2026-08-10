// Bake the street network for the festival area: the app draws its own map and
// computes its own walking paths — no tile server, no CDN, no runtime network.
// Street centrelines only; OSM's per-sidewalk footways are dropped (noisy to
// draw, and pedestrians here just walk the street grid).
import fs from 'node:fs';

const UA = 'UptownPorchfestPlanner/1.0 (+https://polecat.live)';
const BBOX = '44.9468,-93.2975,44.9640,-93.2852';
const QUERY = `[out:json][timeout:120];
(
  way["highway"~"^(residential|living_street|tertiary|secondary|primary|unclassified|service|footway|path|pedestrian|steps|cycleway|track)$"](${BBOX});
);
out body;
>;
out skel qt;`;

// GET, not POST — some proxies refuse POST to Overpass. Overpass also sheds
// load under contention, so back off and retry rather than failing the build.
const MIRRORS = ['https://overpass-api.de/api/interpreter', 'https://overpass.osm.ch/api/interpreter'];
async function overpass(query) {
  let last;
  for (let attempt = 0; attempt < 6; attempt++) {
    const url = MIRRORS[attempt % MIRRORS.length] + '?data=' + encodeURIComponent(query);
    try {
      const res = await fetch(url, { headers: { 'User-Agent': UA } });
      const text = await res.text();
      if (res.ok && text.startsWith('{')) return JSON.parse(text);
      last = `${res.status} ${text.slice(0, 90)}`;
    } catch (e) { last = e.message; }
    const wait = 2000 * 2 ** attempt;
    console.log(`  attempt ${attempt + 1} failed (${last}) — retrying in ${wait / 1000}s`);
    await new Promise(r => setTimeout(r, wait));
  }
  throw new Error(`Overpass unreachable: ${last}`);
}

console.log('fetching street network…');
const osm = await overpass(QUERY);
const nodeLL = new Map();
for (const el of osm.elements) if (el.type === 'node') nodeLL.set(el.id, [el.lat, el.lon]);
const ways = osm.elements.filter(el => el.type === 'way' && el.nodes?.length > 1);
console.log(`raw: ${ways.length} ways, ${nodeLL.size} nodes`);

const CLS = {
  primary: 'major', secondary: 'major', tertiary: 'mid',
  residential: 'minor', living_street: 'minor', unclassified: 'minor', pedestrian: 'minor',
};
const blocked = (t) => t.foot === 'no' || t.access === 'private' || t.access === 'no';

const kept = [];
for (const w of ways) {
  const t = w.tags || {};
  const cls = CLS[t.highway];
  if (!cls || blocked(t)) continue;
  const ns = w.nodes.filter(n => nodeLL.has(n));
  if (ns.length < 2) continue;
  kept.push({ ns, cls, name: t.name || '' });
}
console.log(`street ways: ${kept.length}`);

// --- drop near-collinear intermediate points (grid streets are mostly straight)
const M_PER_DEG_LAT = 111320, M_PER_DEG_LON = 78700;  // ~45°N
const toM = ([la, lo]) => [la * M_PER_DEG_LAT, lo * M_PER_DEG_LON];
function simplify(coords, tolM = 3) {
  if (coords.length < 3) return coords;
  const keep = new Array(coords.length).fill(false);
  keep[0] = keep[coords.length - 1] = true;
  (function dp(lo, hi) {
    if (hi <= lo + 1) return;
    const [ax, ay] = toM(coords[lo]), [bx, by] = toM(coords[hi]);
    const dx = bx - ax, dy = by - ay, len2 = dx * dx + dy * dy;
    let best = -1, bi = -1;
    for (let i = lo + 1; i < hi; i++) {
      const [px, py] = toM(coords[i]);
      let d;
      if (len2 === 0) d = Math.hypot(px - ax, py - ay);
      else {
        const t = Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / len2));
        d = Math.hypot(px - (ax + t * dx), py - (ay + t * dy));
      }
      if (d > best) { best = d; bi = i; }
    }
    if (best > tolM) { keep[bi] = true; dp(lo, bi); dp(bi, hi); }
  })(0, coords.length - 1);
  return coords.filter((_, i) => keep[i]);
}

// Junction nodes must survive simplification or the routing graph falls apart.
const useCount = new Map();
for (const w of kept) for (const n of w.ns) useCount.set(n, (useCount.get(n) || 0) + 1);

const used = new Set();
const simplified = [];
for (const w of kept) {
  // split into runs between junctions, simplify each run, stitch back
  const out = [w.ns[0]];
  let run = [w.ns[0]];
  for (let i = 1; i < w.ns.length; i++) {
    run.push(w.ns[i]);
    const isJunction = (useCount.get(w.ns[i]) || 0) > 1 || i === w.ns.length - 1;
    if (isJunction) {
      const simp = simplify(run.map(n => nodeLL.get(n)));
      const idsOfRun = run.filter((n, k) => simp.some(c => {
        const [la, lo] = nodeLL.get(n); return c[0] === la && c[1] === lo;
      }) && k > 0);
      out.push(...idsOfRun);
      run = [w.ns[i]];
    }
  }
  const ns = out.filter((n, i) => i === 0 || n !== out[i - 1]);
  if (ns.length < 2) continue;
  simplified.push({ ns, cls: w.cls, name: w.name });
  ns.forEach(n => used.add(n));
}

const ids = [...used];
const idx = new Map(ids.map((id, i) => [id, i]));
const pts = ids.map(id => { const [la, lo] = nodeLL.get(id); return [+la.toFixed(5), +lo.toFixed(5)]; });
const outWays = simplified.map(w => ({ n: w.ns.map(n => idx.get(n)), c: w.cls, s: w.name }));

const before = kept.reduce((a, w) => a + w.ns.length, 0);
const after = outWays.reduce((a, w) => a + w.n.length, 0);
console.log(`nodes ${pts.length}, way-points ${before} -> ${after}`);
console.log(`classes: ${['major','mid','minor'].map(c => c + '=' + outWays.filter(w => w.c === c).length).join(' ')}`);

// one label anchor per street name, on its longest way
const byName = new Map();
for (const w of outWays) {
  if (!w.s) continue;
  const p = byName.get(w.s);
  if (!p || w.n.length > p.n.length) byName.set(w.s, w);
}
const labels = [...byName.entries()].map(([s, w]) => {
  const a = pts[w.n[0]], b = pts[w.n[w.n.length - 1]];
  return { s, p: w.n[Math.floor(w.n.length / 2)], v: Math.abs(b[0] - a[0]) > Math.abs(b[1] - a[1]) };
});
console.log(`labels: ${labels.length}`);

fs.writeFileSync('streets.json', JSON.stringify({ pts, ways: outWays, labels }));
console.log('wrote streets.json', (fs.statSync('streets.json').size / 1024).toFixed(1) + ' KB');
