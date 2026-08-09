// Intersections from Overpass + a real pedestrian walking matrix from the
// OSM.de routed-foot OSRM instance. Both baked into the app so the planner's
// routing math needs zero network at runtime.
import fs from 'node:fs';

const UA = 'UptownPorchfestPlanner/1.0 (kevinroberthaas@gmail.com)';
const BBOX = '44.9460,-93.3030,44.9660,-93.2840';
const AVENUES = ['Lyndale Avenue South', 'Aldrich Avenue South', 'Bryant Avenue South',
  'Colfax Avenue South', 'Dupont Avenue South', 'Emerson Avenue South', 'Hennepin Avenue'];
const CROSS = ['West Lake Street', 'West Franklin Avenue', 'West 22nd Street',
  'West 24th Street', 'West 25th Street', 'West 26th Street', 'West 27th Street',
  'West 28th Street'];

const q = `[out:json][timeout:90];
(
${[...AVENUES, ...CROSS].map(n => `  way["name"="${n}"]["highway"](${BBOX});`).join('\n')}
);
out body;
>;
out skel qt;`;

console.log('querying Overpass…');
// GET, not POST — the agent proxy refuses POST to this host.
const res = await fetch('https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(q),
  { headers: { 'User-Agent': UA } });
const osm = await res.json();
const nodeLL = new Map();
const ways = [];
for (const el of osm.elements) {
  if (el.type === 'node') nodeLL.set(el.id, [el.lat, el.lon]);
  else if (el.type === 'way' && el.tags?.name) ways.push({ name: el.tags.name, nodes: el.nodes });
}
console.log(`  ways=${ways.length} nodes=${nodeLL.size}`);

// Shared node between an avenue way and a cross-street way == the intersection.
const shortAve = (n) => n.replace(' Avenue South', ' Ave S').replace(' Avenue', ' Ave');
const shortX = (n) => n.replace('West ', 'W ');
const inter = [];
for (const a of AVENUES) {
  const aNodes = new Set(ways.filter(w => w.name === a).flatMap(w => w.nodes));
  for (const c of CROSS) {
    const cNodes = new Set(ways.filter(w => w.name === c).flatMap(w => w.nodes));
    const hit = [...aNodes].find(id => cNodes.has(id));
    if (!hit) continue;
    const [lat, lon] = nodeLL.get(hit);
    inter.push({ kind: 'corner', label: `${shortAve(a)} & ${shortX(c)}`, lat, lon });
  }
}
inter.sort((x, y) => x.label.localeCompare(y.label));
console.log(`intersections resolved: ${inter.length}`);
inter.forEach(i => console.log(`  ${i.label.padEnd(32)} ${i.lat.toFixed(6)},${i.lon.toFixed(6)}`));
fs.writeFileSync('intersections.json', JSON.stringify(inter, null, 2));

// ---- pedestrian matrix over porches + corners ---------------------------
const geo = JSON.parse(fs.readFileSync('geocode.json', 'utf8'));
const porches = Object.entries(geo).map(([address, g]) => ({ kind: 'porch', label: address, lat: g.lat, lon: g.lon }));
const nodes = [...porches, ...inter];
console.log(`\nmatrix nodes: ${nodes.length} (${porches.length} porches + ${inter.length} corners)`);

const coords = nodes.map(n => `${n.lon},${n.lat}`).join(';');
const url = `https://routing.openstreetmap.de/routed-foot/table/v1/driving/${coords}?annotations=duration,distance`;
const t = await (await fetch(url, { headers: { 'User-Agent': UA } })).json();
if (t.code !== 'Ok') { console.error('table failed:', JSON.stringify(t).slice(0, 400)); process.exit(1); }

const durations = t.durations.map(r => r.map(v => v == null ? null : Math.round(v)));
const distances = t.distances.map(r => r.map(v => v == null ? null : Math.round(v)));
const dur = durations.flat().filter(v => v != null);
const dist = distances.flat().filter(v => v != null);
const nulls = durations.flat().filter(v => v == null).length;
console.log(`table OK — ${durations.length}x${durations[0].length}, nulls=${nulls}`);
console.log(`  seconds: max=${Math.max(...dur)} median=${dur.slice().sort((a,b)=>a-b)[dur.length>>1]}`);
console.log(`  metres : max=${Math.max(...dist)}`);
const paceOk = Math.max(...dist) / Math.max(...dur);
console.log(`  implied pace ≈ ${paceOk.toFixed(2)} m/s (walking should be ~1.1-1.4)`);

fs.writeFileSync('matrix.json', JSON.stringify({ nodes, durations, distances }));
console.log('wrote matrix.json', (fs.statSync('matrix.json').size / 1024).toFixed(1) + ' KB');
