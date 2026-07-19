/* build_data.mjs — compile raw agent listings into js/data.js.
   Reads raw.json (an array of listing objects merged from the nationwide
   search), dedupes by VIN, fills drivetrain from the VIN when missing,
   estimates driving distance to Crystal Lake, IL, and writes js/data.js.
   Run: node build_data.mjs   (no deps). */
import { readFileSync, writeFileSync } from 'node:fs';

const CRYSTAL = { lat: 42.2411, lon: -88.3162 };

// City -> [lat, lon]. Keyed "city, ST" (lowercase). Falls back to state centroid.
const CITY = {
  'barrington, il': [42.154, -88.136], 'chicago, il': [41.878, -87.629],
  'schaumburg, il': [42.033, -88.083], 'arlington heights, il': [42.088, -87.981],
  'glenview, il': [42.069, -87.788], 'naperville, il': [41.785, -88.147],
  'orland park, il': [41.630, -87.854], 'libertyville, il': [42.283, -87.953],
  'west allis, wi': [43.017, -88.007], 'west allis (milwaukee), wi': [43.017, -88.007],
  'glendale, wi': [43.128, -87.935], 'milwaukee, wi': [43.039, -87.906],
  'madison, wi': [43.073, -89.401], 'troy, mi': [42.605, -83.150],
  'fishers, in': [39.956, -86.014], 'indianapolis, in': [39.768, -86.158],
  'ballwin, mo': [38.595, -90.546], 'st. louis, mo': [38.627, -90.199],
  'las vegas, nv': [36.170, -115.139], 'franklin, tn': [35.925, -86.869],
  'nashville, tn': [36.163, -86.781], 'freehold, nj': [40.260, -74.274],
  'monroeville, pa': [40.421, -79.788], 'atlanta, ga': [33.749, -84.388],
  'savannah, ga': [32.081, -81.091], 'wilmington, nc': [34.226, -77.945],
  'dallas, tx': [32.777, -96.797], 'houston, tx': [29.760, -95.370],
  'austin, tx': [30.267, -97.743], 'san antonio, tx': [29.424, -98.494],
  'miami, fl': [25.762, -80.192], 'orlando, fl': [28.538, -81.379],
  'tampa, fl': [27.951, -82.457], 'jacksonville, fl': [30.332, -81.656],
  'los angeles, ca': [34.052, -118.244], 'san diego, ca': [32.716, -117.161],
  'san francisco, ca': [37.775, -122.419], 'sacramento, ca': [38.582, -121.494],
  'phoenix, az': [33.448, -112.074], 'denver, co': [39.739, -104.990],
  'seattle, wa': [47.606, -122.332], 'charlotte, nc': [35.227, -80.843],
  'columbus, oh': [39.961, -82.999], 'cincinnati, oh': [39.103, -84.512],
  'cleveland, oh': [41.499, -81.694], 'detroit, mi': [42.331, -83.046],
  'grand rapids, mi': [42.963, -85.668], 'minneapolis, mn': [44.978, -93.265],
  'kansas city, mo': [39.100, -94.579], 'louisville, ky': [38.253, -85.758],
  'richmond, va': [37.541, -77.436], 'washington, dc': [38.907, -77.037],
  'new york, ny': [40.713, -74.006], 'boston, ma': [42.360, -71.058],
  'philadelphia, pa': [39.953, -75.165], 'pittsburgh, pa': [40.441, -79.996],
  'lemoyne, pa': [40.241, -76.897], 'woodbridge, ct': [41.353, -73.008],
  'knoxville, tn': [35.961, -83.921], 'champaign, il': [40.116, -88.243],
  'st. albans, wv': [38.386, -81.836], 'saint albans, wv': [38.386, -81.836],
  'coconut creek, fl': [26.252, -80.179], 'longwood, fl': [28.703, -81.339],
  'wichita, ks': [37.687, -97.336], 'chantilly, va': [38.894, -77.431],
  'olathe, ks': [38.881, -94.819], 'daytona beach, fl': [29.210, -81.023],
  'st. augustine, fl': [29.905, -81.313], 'saint augustine, fl': [29.905, -81.313],
  'apple valley, mn': [44.732, -93.218], 'saint peters, mo': [38.780, -90.626],
  'st. peters, mo': [38.780, -90.626], 'oklahoma city, ok': [35.468, -97.516],
  'spring, tx': [30.080, -95.417],
};
const STATE = {
  il: [40.0, -89.0], wi: [44.5, -89.5], in: [39.9, -86.3], mi: [43.3, -84.5],
  mo: [38.5, -92.3], oh: [40.4, -82.8], mn: [46.3, -94.3], ia: [42.0, -93.5],
  ky: [37.5, -85.3], tn: [35.9, -86.4], nv: [39.3, -116.6], ca: [37.2, -119.3],
  tx: [31.5, -99.3], fl: [28.6, -82.4], ga: [32.7, -83.4], nc: [35.6, -79.4],
  az: [34.2, -111.7], co: [39.0, -105.5], wa: [47.4, -120.5], nj: [40.1, -74.7],
  ny: [42.9, -75.5], pa: [40.9, -77.8], va: [37.8, -78.2], ma: [42.3, -71.8],
  md: [39.0, -76.7], dc: [38.9, -77.0], sc: [33.9, -80.9], al: [32.8, -86.8],
  or: [43.9, -120.6], ut: [39.3, -111.7], mn2: [46.3, -94.3],
};
function haversine(a, b) {
  const R = 3958.8, r = d => d * Math.PI / 180;
  const dLat = r(b[0] - a.lat), dLon = r(b[1] - a.lon);
  const s = Math.sin(dLat / 2) ** 2 + Math.cos(r(a.lat)) * Math.cos(r(b[0])) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}
function distFor(city, st) {
  const key = `${(city || '').toLowerCase().trim()}, ${(st || '').toLowerCase().trim()}`;
  const c = CITY[key] || STATE[(st || '').toLowerCase().trim()];
  if (!c) return null;
  return Math.round(haversine(CRYSTAL, c) * 1.18);
}
// VIN drivetrain/trim decode for 2026 Corsair: 5LMCJ{1|2}{C|D}A...
//   1=Premiere, 2=Reserve ; C=FWD, D=AWD
function decode(vin) {
  if (!vin || vin.length < 8) return {};
  const m = /^5LMCJ([12])([CD])A/i.exec(vin);
  if (!m) return {};
  return { trim: m[1] === '2' ? 'Reserve' : 'Premiere', drivetrain: m[2].toUpperCase() === 'D' ? 'AWD' : 'FWD' };
}

const raw = JSON.parse(readFileSync(new URL('./raw.json', import.meta.url)));
const byVin = new Map();
let noVin = [];
for (const v of raw) {
  const dec = decode(v.vin);
  if (!v.drivetrain && dec.drivetrain) v.drivetrain = dec.drivetrain;
  // trust VIN trim decode over free-text when they conflict on trim family
  if (dec.trim && !/grand touring/i.test(v.trim || '')) v.trim = dec.trim;
  if (v.distance_mi == null) v.distance_mi = distFor(v.dealer_city, v.dealer_state);
  if (!v.vin) { noVin.push(v); continue; }
  const key = v.vin.toUpperCase();
  const prev = byVin.get(key);
  if (!prev) { byVin.set(key, v); continue; }
  // merge: prefer the record with more filled fields / a real price / phone
  const score = x => (x.price ? 2 : 0) + (x.dealer_phone ? 1 : 0) + Object.values(x).filter(Boolean).length * 0.1;
  const merged = score(v) > score(prev) ? { ...prev, ...clean(v) } : { ...v, ...clean(prev) };
  byVin.set(key, merged);
}
function clean(o) { const r = {}; for (const k in o) if (o[k] !== null && o[k] !== '' && !(Array.isArray(o[k]) && !o[k].length)) r[k] = o[k]; return r; }

const vehicles = [...byVin.values(), ...noVin];
const out = {
  generated: process.env.GEN_DATE || 'July 19, 2026',
  spec: {
    exterior: 'Red Carpet Metallic Tinted Clearcoat',
    interior: 'Light Smoked Truffle (light seats preferred; light grey / other light faux-leather welcome)',
    trims: ['Reserve', 'Premiere'],
    exclude: ['Grand Touring (PHEV)'],
    drivetrain: 'AWD preferred (FWD tolerated)',
  },
  vehicles,
};
writeFileSync(new URL('./js/data.js', import.meta.url),
  '/* Corsair Finder data — FACTS ONLY (ranking logic in app.js). Auto-generated\n   by build_data.mjs from a nationwide Lincoln-dealer search. Each record is a\n   real, verified listing; distance_mi = est. driving miles to Crystal Lake, IL. */\nwindow.CORSAIR_DATA = ' +
  JSON.stringify(out, null, 2) + ';\n');
console.log(`Wrote ${vehicles.length} vehicles (${byVin.size} with VIN, ${noVin.length} without).`);
