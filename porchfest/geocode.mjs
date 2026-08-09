// Geocode the 33 unique porch addresses via Nominatim (free, no key).
// Rate-limited to 1 req / 1.2s per the OSM usage policy.
import fs from 'node:fs';

const UA = 'UptownPorchfestPlanner/1.0 (kevinroberthaas@gmail.com)';
const bands = JSON.parse(fs.readFileSync('lineup.json', 'utf8'));
const addrs = [...new Set(bands.map(b => b.porch_address))];

// Normalize the messy ones into something Nominatim resolves cleanly.
const normalize = (a) => {
  let s = a.trim();
  if (s === '2840 Bryant/2845 Colfax Avenue') s = '2840 Bryant Ave S';
  if (/^900 W 22nd/i.test(s)) return '900 West 22nd Street, Minneapolis, MN 55405';
  s = s.replace(/\bAve S\b/i, 'Avenue South');
  if (!/minneapolis/i.test(s)) s += ', Minneapolis, MN';
  return s;
};

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const out = {};

for (const raw of addrs) {
  const q = normalize(raw);
  let rec = null;
  for (const attempt of [q, q.replace(/, Minneapolis, MN$/, ', Minneapolis, Minnesota, USA')]) {
    const url = 'https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q='
      + encodeURIComponent(attempt);
    try {
      const res = await fetch(url, { headers: { 'User-Agent': UA, 'Accept-Language': 'en' } });
      const j = await res.json();
      if (Array.isArray(j) && j.length) {
        rec = { lat: +j[0].lat, lon: +j[0].lon, display: j[0].display_name, query: attempt };
        break;
      }
    } catch (e) {
      console.error('ERR', raw, e.message);
    }
    await sleep(1200);
  }
  out[raw] = rec;
  console.log(rec ? `OK   ${raw}  ->  ${rec.lat},${rec.lon}` : `MISS ${raw}`);
  await sleep(1200);
}

fs.writeFileSync('geocode.json', JSON.stringify(out, null, 2));
const miss = Object.entries(out).filter(([, v]) => !v).map(([k]) => k);
console.log(`\ndone: ${addrs.length - miss.length}/${addrs.length} geocoded`);
if (miss.length) console.log('MISSING:\n' + miss.join('\n'));
