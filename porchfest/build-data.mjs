// Merge scraped lineup + researched profiles + geocoding + street network
// into the single payload the app ships with.
import fs from 'node:fs';

const raw = JSON.parse(fs.readFileSync('lineup.json', 'utf8'));
const profs = JSON.parse(fs.readFileSync('profiles.merged.json', 'utf8'));
const geo = JSON.parse(fs.readFileSync('geocode.json', 'utf8'));
const corners = JSON.parse(fs.readFileSync('intersections.json', 'utf8'));
const streets = JSON.parse(fs.readFileSync('streets.json', 'utf8'));

const byName = new Map(profs.map(p => [p.band_name, p]));

// "2:00 PM - 3:00 PM" -> [840, 900] minutes past midnight
function parseWindow(s) {
  const m = String(s || '').match(/(\d{1,2}):(\d{2})\s*(AM|PM)\s*-\s*(\d{1,2}):(\d{2})\s*(AM|PM)/i);
  if (!m) return null;
  const to = (h, mi, ap) => ((+h % 12) + (/pm/i.test(ap) ? 12 : 0)) * 60 + +mi;
  return [to(m[1], m[2], m[3]), to(m[4], m[5], m[6])];
}

const porchList = Object.keys(geo);
const porchIdx = new Map(porchList.map((a, i) => [a, i]));
const porches = porchList.map(a => ({ a, lat: +geo[a].lat.toFixed(6), lon: +geo[a].lon.toFixed(6) }));

const slug = (s) => s.toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const seen = new Set();
const DIMS = ['energy', 'loudness', 'tempo', 'electronic', 'vocal_forward',
  'danceability', 'experimental', 'brightness', 'grit', 'kid_friendly'];

const bands = [];
const problems = [];
for (const b of raw) {
  const p = byName.get(b.band_name);
  if (!p) { problems.push(`no profile: ${b.band_name}`); continue; }
  const win = parseWindow(b.time);
  if (!win) { problems.push(`unparsable time "${b.time}": ${b.band_name}`); continue; }
  let id = slug(b.band_name), n = 2;
  while (seen.has(id)) id = slug(b.band_name) + '-' + n++;
  seen.add(id);
  const links = {};
  for (const [k, v] of Object.entries({ web: b.website_link, bc: b.bandcamp_link, sp: b.spotify_link,
    sc: b.soundcloud_link, ig: b.instagram_link, fb: b.facebook_link })) {
    if (v && /^https?:\/\//i.test(v)) links[k] = v;
  }
  bands.push({
    id, n: b.band_name, g: b.genre || '', t: win, p: porchIdx.get(b.porch_address),
    one: p.one_liner, pr: p.profile, sl: p.sounds_like || [], tg: p.genre_tags || [],
    d: DIMS.map(k => p.dims[k]), cf: { high: 2, medium: 1, low: 0 }[p.confidence] ?? 1,
    bio: b.bio || '', img: b.img_url || '', l: links,
  });
}

bands.sort((a, b) => a.t[0] - b.t[0] || a.n.localeCompare(b.n));
console.log(`bands: ${bands.length}/${raw.length}`);
if (problems.length) console.log('PROBLEMS:\n' + problems.join('\n'));

const starts = bands.map(b => b.t[0]), ends = bands.map(b => b.t[1]);
console.log(`window: ${Math.min(...starts)}–${Math.max(...ends)} min ` +
  `(${Math.floor(Math.min(...starts) / 60)}:00 – ${Math.floor(Math.max(...ends) / 60)}:00)`);
console.log(`sets per porch: min=${Math.min(...porches.map((_, i) => bands.filter(b => b.p === i).length))} ` +
  `max=${Math.max(...porches.map((_, i) => bands.filter(b => b.p === i).length))}`);
console.log(`with photos: ${bands.filter(b => b.img).length}, with links: ${bands.filter(b => Object.keys(b.l).length).length}`);

const data = {
  fest: { name: 'Uptown Porchfest', year: 2026, date: '2026-08-15',
          city: 'Lowry Hill East (The Wedge), Minneapolis', src: 'https://uptownporchfest.com/bands' },
  dims: DIMS,
  bands, porches,
  corners: corners.map(c => ({ a: c.label, lat: +c.lat.toFixed(6), lon: +c.lon.toFixed(6) })),
  streets,
};
fs.writeFileSync('data.json', JSON.stringify(data));
console.log('wrote data.json', (fs.statSync('data.json').size / 1024).toFixed(1) + ' KB');
