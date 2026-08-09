// Pull the lineup from uptownporchfest.com.
//
// The site is a React SPA with no public API, but its bundle ships the whole
// band list inline as a JSON.parse('…') literal — name, genre, bio, porch
// address, set time, photo and social links for all 91 acts. We locate the
// bundle from the page, extract that literal and unescape it back to JSON.
//
//   node build/scrape.mjs   ->  build/lineup.json
import fs from 'node:fs';
import path from 'node:path';

const UA = 'UptownPorchfestPlanner/1.0 (+https://polecat.live)';
const here = path.dirname(new URL(import.meta.url).pathname);
const get = async (url) => {
  const r = await fetch(url, { headers: { 'User-Agent': UA } });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.text();
};

const html = await get('https://uptownporchfest.com/bands');
const m = html.match(/src="(\/static\/js\/main\.[a-z0-9]+\.js)"/i);
if (!m) throw new Error('could not find the main bundle in the page');
console.log('bundle:', m[1]);
const js = await get('https://uptownporchfest.com' + m[1]);

// Walk every JSON.parse('…') literal and keep the one that looks like the lineup.
const MARK = "JSON.parse('";
let idx = 0, found = null;
while ((idx = js.indexOf(MARK, idx)) !== -1) {
  const start = idx + MARK.length;
  let p = start, esc = false, end = -1;
  for (; p < js.length; p++) {
    const c = js[p];
    if (esc) { esc = false; continue; }
    if (c === '\\') { esc = true; continue; }
    if (c === "'") { end = p; break; }
  }
  if (end === -1) break;
  try {
    // The literal is a JS string; turn it back into its runtime value first.
    const data = JSON.parse(JSON.parse('"' + js.slice(start, end).replace(/"/g, '\\"') + '"'));
    if (Array.isArray(data) && data[0]?.band_name) { found = data; break; }
  } catch { /* not this one */ }
  idx = end + 1;
}
if (!found) throw new Error('no band array found in the bundle — the site changed shape');

const need = ['band_name', 'porch_address', 'time', 'genre', 'bio'];
const bad = found.filter(b => need.some(k => !(k in b)));
if (bad.length) throw new Error(`${bad.length} record(s) missing expected fields`);

fs.writeFileSync(path.join(here, 'lineup.json'), JSON.stringify(found, null, 2));
console.log(`wrote lineup.json — ${found.length} bands, ` +
  `${new Set(found.map(b => b.porch_address)).size} porches`);
