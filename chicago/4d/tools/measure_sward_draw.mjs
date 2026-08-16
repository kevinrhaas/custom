/**
 * ROADMAP K49(a) — THE SWARD'S DRAWN CENSUS, ACROSS EVERY COMMUNITY.
 *
 *   node tools/measure_sward_draw.mjs [--source]
 *
 * `flora.js` keeps the census (`stats.draws`); the release smoke reads it at
 * whatever station the gate happens to be standing in, and that is one
 * community out of ten. This stands the placer in EVERY community in turn and
 * asks the same question of each: which species does a list owe a whole plant
 * to, and draw nowhere?
 *
 * Why a separate tool rather than another smoke assertion. The smoke is a gate
 * and costs ~13 minutes a viewport; this is a measurement and costs about one,
 * because it never renders a frame it does not need. It re-deals the sward by
 * handing `flora.update` a synthetic camera at a plantable point inside each
 * community — the same entry point the render loop uses, so it measures the
 * placer rather than a re-implementation of it.
 *
 * The single-station figure the smoke prints is not wrong, it is SMALL: 68
 * slots in the settled town, where this reports 6,780 across sixteen populated
 * lists. Quote this one for a claim about the dataset, and the smoke's for a
 * claim about the frame the gate stood in.
 *
 * Defaults to the PUBLISHED mirror, for the reason the smoke does: the source
 * tree and the site do not load the same geometry, and the ground a plant is
 * stationed on comes off it. `--source` measures the working tree instead.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// Playwright is installed globally on the runner, and ESM does not honour
// NODE_PATH, so resolve it the way tools/smoke_renderer.mjs does.
async function loadPlaywright() {
  let ns;
  try {
    ns = await import('playwright');
  } catch {
    const root = (process.env.NODE_PATH
      || execSync('npm root -g', { encoding: 'utf8' })).trim().split(path.delimiter)[0];
    ns = await import(path.join(root, 'playwright', 'index.js'));
  }
  return ns.chromium ? ns : ns.default;
}
const { chromium } = await loadPlaywright();

const HERE = path.dirname(fileURLToPath(import.meta.url));
const wantSource = process.argv.includes('--source');
const ROOT = wantSource
  ? path.resolve(HERE, '..')
  : path.resolve(HERE, '../../../site/chicago/4d');
const ENTRY = wantSource ? '/renderers/web/index.html' : '/walk/';
const PORT = Number(process.env.SWARD_PORT || 4191);
const YEAR = process.env.SWARD_YEAR || '1835';

const TYPES = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.glb': 'model/gltf-binary',
  '.bin': 'application/octet-stream', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.wasm': 'application/wasm', '.md': 'text/markdown',
};
const server = http.createServer((req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  let file = path.join(ROOT, url);
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
  if (!file.startsWith(ROOT) || !fs.existsSync(file)) {
    res.writeHead(404, { 'content-type': 'text/plain' });
    res.end(`not found: ${url}`);
    return;
  }
  res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});
await new Promise((r) => server.listen(PORT, r));
if (!wantSource && !fs.existsSync(path.join(ROOT, 'walk', 'index.html'))) {
  console.error(`no published mirror at ${ROOT} — run tools/publish.sh first`);
  process.exit(2);
}
console.log(`serving ${ROOT} — ${wantSource ? 'source tree' : 'PUBLISHED mirror'}\n`);

const browser = await chromium.launch({ args: ['--enable-unsafe-swiftshader'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
const errors = [];
page.on('pageerror', (e) => errors.push(String(e)));
await page.goto(`http://127.0.0.1:${PORT}${ENTRY}?year=${YEAR}`, { waitUntil: 'load' });
await page.waitForFunction(() => window.__chicago4d?.ready === true, null, { timeout: 240000 });

const measured = await page.evaluate(() => {
  const a = window.__chicago4d;
  const wanted = a.flora.substrates().map((z) => z.id);
  // One plantable point per community, found through the placer's OWN zone
  // finder and its own plantability rule rather than off the extents: a point
  // this project would refuse to plant answers for nothing.
  const spots = {};
  for (let e = -900; e <= 1200 && Object.keys(spots).length < wanted.length; e += 6) {
    for (let n = -700; n <= 700; n += 6) {
      const z = a.flora.zoneAt(e, n);
      if (z && !spots[z] && a.flora.plantableAt(e, n)) spots[z] = [e, n];
    }
  }
  const rows = [];
  for (const [zone, [e, n]] of Object.entries(spots)) {
    // The rig re-deals when the camera has moved, so hand it a camera. It reads
    // exactly two things off one, and a duck answers both.
    const camera = {
      getWorldPosition: (v) => { v.set(e, 1.7, -n); return v; },
      getWorldDirection: (v) => { v.set(0, 0, -1); return v; },
    };
    a.flora.update(0.016, camera);
    a.flora.update(0.016, camera);
    for (const d of a.flora.stats.draws) {
      if (d.drawn <= 0) continue;
      rows.push({
        at: zone,
        community: d.community,
        list: d.list,
        drawn: d.drawn,
        species: d.species.length,
        worstShortfall: Math.max(0, ...d.species.map((s) => s.expected - s.drawn)),
        // ROADMAP K49(d). The worst shortfall is a max of a max, so it moves on
        // one species in one list and is the noisiest thing this tool prints —
        // it named the fault, but it cannot rank two candidate repairs. This is
        // the whole list's disagreement with its own record, summed over every
        // species and both signs, and it is the figure to compare draws on.
        deviation: d.species.reduce((t, s) => t + Math.abs(s.expected - s.drawn), 0),
        absent: d.species.filter((s) => s.drawn === 0 && s.expected >= 1)
          .map((s) => ({ id: s.id, owed: s.expected, unit: s.unit })),
      });
    }
  }
  return { spots: Object.keys(spots), rows, abundance: a.flora.stats.abundance };
});

const slots = measured.rows.reduce((t, r) => t + r.drawn, 0);
const lists = new Set(measured.rows.map((r) => `${r.community}.${r.list}`));
const absent = measured.rows.flatMap((r) => r.absent.map(
  (s) => `${r.community}.${r.list}.${s.id} owed ${s.owed.toFixed(2)} (${s.unit}), standing at `
    + `${r.at}`));
const worst = Math.max(0, ...measured.rows.map((r) => r.worstShortfall));
const devOf = (list) => measured.rows.filter((r) => r.list === list)
  .reduce((t, r) => t + r.deviation, 0);

for (const r of measured.rows) {
  console.log(`  at ${r.at.padEnd(22)} ${r.community.padEnd(22)} ${r.list.padEnd(6)} `
    + `drawn ${String(r.drawn).padStart(5)}  of ${String(r.species).padStart(2)} species  `
    + `worst shortfall ${r.worstShortfall.toFixed(2)}  dev ${r.deviation.toFixed(2)}`
    + `${r.absent.length ? `  ABSENT ${r.absent.map((s) => s.id).join(', ')}` : ''}`);
}
const ab = measured.abundance ?? { lists: 0, mixed: [], unconvertible: [] };
console.log(`\n${measured.spots.length} communities stood in · ${lists.size} populated list(s) · `
  + `${slots} slots dealt · worst shortfall ${worst.toFixed(2)} slot(s)`);
console.log(`deviation from the recorded cover, summed over every species and both signs: `
  + `matrix ${devOf('matrix').toFixed(2)} · forb ${devOf('forb').toFixed(2)} slot(s)`);
console.log(`${absent.length} species owed a whole slot and drawn nowhere:`);
for (const s of absent) console.log(`  - ${s}`);
console.log(`\nabundance units: ${ab.mixed.length} of ${ab.lists} lists mix an area with a count; `
  + `${ab.unconvertible.length} record(s) give cover with no width_m`);
for (const m of ab.mixed) {
  console.log(`  - ${m.zone}.${m.list}: ${(m.countedShare * 100).toFixed(1)}% of slots dealt off `
    + `counts, against ${m.area} species recorded as an area`);
}
if (errors.length) console.log(`\npage errors: ${errors.length}\n  ${errors.join('\n  ')}`);

await browser.close();
server.close();
process.exit(errors.length ? 1 : 0);
