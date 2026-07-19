/* build_data.mjs — compile raw listings into js/data.js for the Vehicle Finder.
   Reads raw-corsair.json + raw-forester.json (arrays of listing objects from
   the nationwide searches), dedupes by VIN, fills drivetrain/trim from the VIN
   where decodable, estimates driving distance to Crystal Lake, IL, and writes
   js/data.js with both searches. Run: node build_data.mjs  (no deps). */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';

// attach hosted window-sticker / photo paths when the files exist on disk
function attachAssets(v) {
  if (v.vin) {
    const vin = v.vin.toUpperCase();
    if (existsSync(new URL(`./stickers/${vin}.pdf`, import.meta.url))) v.sticker = `stickers/${vin}.pdf`;
    for (const ext of ['jpg', 'webp', 'png']) {
      if (existsSync(new URL(`./photos/${vin}.${ext}`, import.meta.url))) { v.photo = `photos/${vin}.${ext}`; break; }
    }
  }
  return v;
}

const CRYSTAL = { lat: 42.2411, lon: -88.3162 };

// City -> [lat, lon]. Keyed "city, ST" (lowercase). Falls back to state centroid.
const CITY = {
  'barrington, il': [42.154, -88.136], 'chicago, il': [41.878, -87.629],
  'schaumburg, il': [42.033, -88.083], 'arlington heights, il': [42.088, -87.981],
  'glenview, il': [42.069, -87.788], 'naperville, il': [41.785, -88.147],
  'orland park, il': [41.630, -87.854], 'libertyville, il': [42.283, -87.953],
  'skokie, il': [42.032, -87.732], 'evanston, il': [42.045, -87.688],
  'bensenville, il': [41.955, -87.940], 'north aurora, il': [41.806, -88.327],
  'hoffman estates, il': [42.043, -88.080], 'elgin, il': [42.037, -88.281],
  'crystal lake, il': [42.241, -88.316], 'gurnee, il': [42.370, -87.902],
  'highland park, il': [42.182, -87.800], 'countryside, il': [41.783, -87.878],
  'rockford, il': [42.271, -89.094], 'peoria, il': [40.694, -89.589],
  'springfield, il': [39.782, -89.651], 'champaign, il': [40.116, -88.243],
  'west allis, wi': [43.017, -88.007], 'west allis (milwaukee), wi': [43.017, -88.007],
  'glendale, wi': [43.128, -87.935], 'milwaukee, wi': [43.039, -87.906],
  'madison, wi': [43.073, -89.401], 'mequon, wi': [43.223, -87.984],
  'waukesha, wi': [43.012, -88.231], 'green bay, wi': [44.513, -88.013],
  'kenosha, wi': [42.585, -87.821], 'racine, wi': [42.726, -87.783],
  'troy, mi': [42.605, -83.150], 'sterling heights, mi': [42.580, -83.030],
  'detroit, mi': [42.331, -83.046], 'grand rapids, mi': [42.963, -85.668],
  'fishers, in': [39.956, -86.014], 'indianapolis, in': [39.768, -86.158],
  'merrillville, in': [41.483, -87.333], 'fort wayne, in': [41.079, -85.139],
  'schererville, in': [41.479, -87.455], 'mishawaka, in': [41.661, -86.158],
  'palatine, il': [42.110, -88.034], 'mequon, wi': [43.223, -87.984],
  'urbandale, ia': [41.627, -93.712], 'dubuque, ia': [42.500, -90.665],
  "o'fallon, mo": [38.811, -90.700], 'st. cloud, mn': [45.560, -94.162],
  'ballwin, mo': [38.595, -90.546], 'st. louis, mo': [38.627, -90.199],
  'saint peters, mo': [38.780, -90.626], 'st. peters, mo': [38.780, -90.626],
  'las vegas, nv': [36.170, -115.139], 'franklin, tn': [35.925, -86.869],
  'nashville, tn': [36.163, -86.781], 'knoxville, tn': [35.961, -83.921],
  'freehold, nj': [40.260, -74.274], 'monroeville, pa': [40.421, -79.788],
  'lemoyne, pa': [40.241, -76.897], 'woodbridge, ct': [41.353, -73.008],
  'st. albans, wv': [38.386, -81.836], 'saint albans, wv': [38.386, -81.836],
  'atlanta, ga': [33.749, -84.388], 'savannah, ga': [32.081, -81.091],
  'coconut creek, fl': [26.252, -80.179], 'longwood, fl': [28.703, -81.339],
  'daytona beach, fl': [29.210, -81.023], 'tampa, fl': [27.951, -82.457],
  'wesley chapel, fl': [28.240, -82.328], 'miami, fl': [25.762, -80.192],
  'orlando, fl': [28.538, -81.379], 'st. augustine, fl': [29.905, -81.313],
  'saint augustine, fl': [29.905, -81.313],
  'wichita, ks': [37.687, -97.336], 'olathe, ks': [38.881, -94.819],
  'chantilly, va': [38.894, -77.431], 'alexandria, va': [38.805, -77.047],
  'apple valley, mn': [44.732, -93.218], 'minneapolis, mn': [44.978, -93.265],
  'oklahoma city, ok': [35.468, -97.516], 'el reno, ok': [35.532, -97.955],
  'spring, tx': [30.080, -95.417], 'dallas, tx': [32.777, -96.797],
  'houston, tx': [29.760, -95.370], 'phoenix, az': [33.448, -112.074],
  'denver, co': [39.739, -104.990], 'columbus, oh': [39.961, -82.999],
  'cincinnati, oh': [39.103, -84.512], 'cleveland, oh': [41.499, -81.694],
  'cedar rapids, ia': [41.978, -91.665], 'des moines, ia': [41.587, -93.625],
  'davenport, ia': [41.524, -90.578], 'dubuque, ia': [42.500, -90.665],
  'louisville, ky': [38.253, -85.758], 'charlotte, nc': [35.227, -80.843],
  'waukesha, wi': [43.012, -88.231], 'appleton, wi': [44.262, -88.415],
  'highland park, il': [42.182, -87.800], 'portage, in': [41.576, -87.176],
  'cuyahoga falls, oh': [41.134, -81.485], 'spokane valley, wa': [47.673, -117.239],
  'aurora, co': [39.729, -104.832], 'emerson, nj': [40.976, -74.026],
  'plano, tx': [33.020, -96.699],
};
const STATE = {
  il: [40.0, -89.0], wi: [44.5, -89.5], in: [39.9, -86.3], mi: [43.3, -84.5],
  mo: [38.5, -92.3], oh: [40.4, -82.8], mn: [46.3, -94.3], ia: [42.0, -93.5],
  ky: [37.5, -85.3], tn: [35.9, -86.4], nv: [39.3, -116.6], ks: [38.5, -98.0],
  tx: [31.5, -99.3], fl: [28.6, -82.4], ga: [32.7, -83.4], nc: [35.6, -79.4],
  az: [34.2, -111.7], co: [39.0, -105.5], nj: [40.1, -74.7], ok: [35.6, -97.5],
  ny: [42.9, -75.5], pa: [40.9, -77.8], va: [37.8, -78.2], ct: [41.6, -72.7],
  md: [39.0, -76.7], dc: [38.9, -77.0], sc: [33.9, -80.9], al: [32.8, -86.8],
  wv: [38.6, -80.6], ne: [41.5, -99.8], ar: [34.9, -92.4], la: [31.1, -92.0],
  ms: [32.7, -89.7], ut: [39.3, -111.7], nm: [34.4, -106.1], sd: [44.4, -100.2],
  nd: [47.5, -100.5], mt: [47.1, -109.6], wy: [43.0, -107.6], id: [44.4, -114.6],
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
// VIN decode, 2026 Corsair: 5LMCJ{1|2}{C|D}A -> 1=Premiere/2=Reserve, C=FWD/D=AWD
function decodeCorsair(vin) {
  const m = /^5LMCJ([12])([CD])A/i.exec(vin || '');
  if (!m) return {};
  return { trim: m[1] === '2' ? 'Reserve' : 'Premiere', drivetrain: m[2].toUpperCase() === 'D' ? 'AWD' : 'FWD' };
}

function clean(o) { const r = {}; for (const k in o) if (o[k] !== null && o[k] !== '' && !(Array.isArray(o[k]) && !o[k].length)) r[k] = o[k]; return r; }

function compile(file, decode) {
  if (!existsSync(new URL(file, import.meta.url))) return [];
  const raw = JSON.parse(readFileSync(new URL(file, import.meta.url)));
  const byVin = new Map(); const noVin = [];
  for (const v of raw) {
    const dec = decode ? decode(v.vin) : {};
    if (!v.drivetrain && dec.drivetrain) v.drivetrain = dec.drivetrain;
    if (dec.trim && !/grand touring/i.test(v.trim || '')) v.trim = dec.trim;
    if (v.distance_mi == null) v.distance_mi = distFor(v.dealer_city, v.dealer_state);
    if (!v.vin) { noVin.push(v); continue; }
    const key = v.vin.toUpperCase();
    const prev = byVin.get(key);
    if (!prev) { byVin.set(key, v); continue; }
    const score = x => (x.price ? 2 : 0) + (x.dealer_phone ? 1 : 0) + Object.values(x).filter(Boolean).length * 0.1;
    byVin.set(key, score(v) > score(prev) ? { ...prev, ...clean(v) } : { ...v, ...clean(prev) });
  }
  return [...byVin.values(), ...noVin].map(attachAssets);
}

const corsair = compile('./raw-corsair.json', decodeCorsair);
const forester = compile('./raw-forester.json', null);

const out = {
  generated: process.env.GEN_DATE || 'July 19, 2026',
  searches: [
    {
      id: 'corsair',
      label: 'Lincoln Corsair',
      title: "Pat's 2026 Lincoln Corsair",
      subtitle: 'The Corsair is in its final model year. Ranked nationwide shortlist for Pat: Red Carpet Metallic, light Smoked Truffle seats, Reserve or Premiere, AWD preferred — never the Grand Touring PHEV.',
      target_color: 'Red Carpet Metallic',
      spec_chips: [
        { dot: '#8e1425', text: '<b>1.</b>&nbsp;Red Carpet Metallic' },
        { dot: '#c9b79a', text: '<b>2.</b>&nbsp;Light seats — Light Smoked Truffle' },
        { text: '<b>3.</b>&nbsp;Reserve or Premiere' },
        { text: '<b>4.</b>&nbsp;AWD preferred' },
        { text: '<b>5.</b>&nbsp;Panoramic roof · nicer packages' },
        { text: '<b>6.</b>&nbsp;New or essentially new' },
      ],
      tiers: {
        exact: 'Exact — Red Carpet Metallic + Light Smoked Truffle',
        strong: 'Strong — Red Carpet + a light interior',
        backup: 'Backup — one utmost pref met',
        stretch: 'Reference — nearby / notable',
      },
      vehicles: corsair,
    },
    {
      id: 'forester',
      label: 'Subaru Forester',
      title: '2026 Subaru Forester Touring Hybrid',
      subtitle: 'Per the build sheet: Forester Touring Hybrid in Crimson Red Pearl with Touring Brown leather — $42,995 as configured with destination. Availability centered on Crystal Lake, IL.',
      target_color: 'Crimson Red Pearl',
      spec_chips: [
        { dot: '#8c1c2c', text: '<b>1.</b>&nbsp;Crimson Red Pearl' },
        { dot: '#6b4a35', text: '<b>2.</b>&nbsp;Touring Brown leather' },
        { text: '<b>3.</b>&nbsp;Touring Hybrid trim' },
        { text: '<b>4.</b>&nbsp;AWD standard · panoramic moonroof' },
        { text: '<b>5.</b>&nbsp;$42,995 as configured' },
        { text: '<b>6.</b>&nbsp;Near Crystal Lake preferred' },
      ],
      tiers: {
        exact: 'Exact — Crimson Red Pearl + Touring Hybrid',
        strong: 'Strong — Crimson Red on another hybrid trim',
        backup: 'Backup — Touring Hybrid, other color',
        stretch: 'Reference — other relevant Foresters',
      },
      vehicles: forester,
    },
  ],
};

writeFileSync(new URL('./js/data.js', import.meta.url),
  '/* Vehicle Finder data — FACTS ONLY (ranking logic in app.js). Auto-generated\n   by build_data.mjs from nationwide dealer searches. Each record is a real\n   listing; distance_mi = est. driving miles to Crystal Lake, IL. */\nwindow.FINDER_DATA = ' +
  JSON.stringify(out, null, 2) + ';\n');
console.log(`Wrote data.js — corsair: ${corsair.length}, forester: ${forester.length}`);
