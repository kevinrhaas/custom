/* Stay Finder data compiler.
 *
 * Reads the per-region research files (raw-<region>.json) that live beside this
 * script, normalises them into one factual dataset and writes the app's
 * js/data.js over in site/stay/. Facts only: no scoring, no tiers, no "best
 * value" — all of that lives in the app's js/app.js so the data file stays
 * something you can diff against the listings themselves.
 *
 * Run: node build-data.mjs
 */
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));      // stay/ — research + tooling
const APP = join(HERE, '..', 'site', 'stay');              // site/stay/ — the published app

/* The trip. Dec 19 2026 is a Saturday, which matters more than it looks: the
 * beach PMs run Saturday-to-Saturday turnover in peak weeks and Anna Maria has
 * a 7-night minimum by ordinance, so an 8-night Sat->Sun stay clears both. */
const DATES = { checkin: '2026-12-19', checkout: '2026-12-27', nights: 8, guests: 16 };

const REGIONS = [
  { id: 'tampa-metro',  short: 'Tampa Bay',   label: 'Tampa / St. Pete / Clearwater metro' },
  { id: 'gulf-beaches', short: 'Beaches',     label: 'Gulf beaches & barrier islands' },
  { id: 'nature-coast', short: 'Nature Coast',label: 'Cedar Key, Crystal River, Homosassa' },
  { id: 'inland-east',  short: 'Inland',      label: 'Crystal Springs, Dade City, Lakeland, Ocala' },
  { id: 'unique-stays', short: 'Unusual',     label: 'Estates, inn buyouts and compounds' }
];

const num = v => (typeof v === 'number' && Number.isFinite(v)) ? v : null;
const str = v => (typeof v === 'string' && v.trim() && !/^not stated$/i.test(v.trim())) ? v.trim() : null;
const arr = v => Array.isArray(v) ? v.filter(x => typeof x === 'string' && x.trim()) : [];

/* A bed count is only reported when the listing actually published one.
 * Coercing a missing layout to zero would quietly turn "we don't know" into
 * "no kings", and the king preference is the whole point of this search. */
function beds(b) {
  if (!b || typeof b !== 'object') return null;
  const out = {};
  let any = 0;
  for (const k of ['king', 'queen', 'full', 'twin', 'sofa', 'bunk']) {
    const n = num(b[k]);
    if (n !== null) { out[k] = n; any += n; }
  }
  // all zeros is not a bed layout — it is an unfilled template, and letting it
  // through would read on the card as "we checked: no kings"
  return (Object.keys(out).length && any > 0) ? out : null;
}

const problems = [];
function load() {
  const files = readdirSync(HERE).filter(f => /^raw-.*\.json$/.test(f)).sort();
  const out = [];
  for (const f of files) {
    const doc = JSON.parse(readFileSync(join(HERE, f), 'utf8'));
    const region = doc.region;
    if (!REGIONS.some(r => r.id === region)) problems.push(`${f}: unknown region "${region}"`);
    for (const p of doc.properties || []) {
      const id = str(p.id);
      if (!id) { problems.push(`${f}: a property has no id`); continue; }
      if (!num(p.lat) || !num(p.lon)) { problems.push(`${id}: missing coordinates — dropped (it could not be mapped)`); continue; }
      if (!num(p.bedrooms)) { problems.push(`${id}: no bedroom count — dropped`); continue; }

      // path is relative to the app, but the file lives under site/stay/
      const photo = existsSync(join(APP, 'photos', id + '.jpg')) ? `photos/${id}.jpg` : null;
      out.push({
        id, region,
        name: str(p.name) || id,
        source: str(p.source),
        url: str(p.url),
        city: str(p.city), neighborhood: str(p.neighborhood),
        lat: num(p.lat), lon: num(p.lon), coords_approx: p.coords_approx !== false,
        bedrooms: num(p.bedrooms), bathrooms: num(p.bathrooms), sleeps: num(p.sleeps),
        compound: !!p.compound, compound_note: str(p.compound_note),
        kind: str(p.kind), acreage: str(p.acreage),
        beds: beds(p.beds), beds_note: str(p.beds_note),
        nightly_est: num(p.nightly_est), total_est: num(p.total_est), price_note: str(p.price_note),
        amenities: arr(p.amenities), tags: arr(p.tags),
        photo, images: arr(p.images),
        why: str(p.why), cons: str(p.cons),
        drive_note: str(p.drive_note), min_stay_note: str(p.min_stay_note),
        availability: ['confirmed_open', 'search_listed', 'unknown'].includes(p.availability) ? p.availability : 'unknown',
        availability_note: str(p.availability_note),
        phone: str(p.phone), checked: str(p.checked)
      });
    }
  }
  return dedupe(out);
}

/* Two regional passes can legitimately find the same place — a hilltop retreat
 * is both "inland" and "unusual". Match on listing id, on URL, and on
 * name-in-town, then keep whichever record the researcher filled in more
 * fully rather than whichever happened to be read first. */
function completeness(p) {
  let n = 0;
  for (const [k, v] of Object.entries(p)) {
    if (v === null || v === false) continue;
    if (Array.isArray(v)) { n += v.length ? 2 : 0; continue; }
    if (typeof v === 'object') { n += 2; continue; }
    n += 1;
  }
  return n;
}
function dedupe(list) {
  const keysOf = p => [
    'id:' + p.id,
    p.url ? 'url:' + p.url.replace(/[?#].*$/, '').replace(/\/$/, '') : null,
    `nm:${p.name.toLowerCase()}|${(p.city || '').toLowerCase()}`
  ].filter(Boolean);

  const owner = new Map(), kept = new Map();
  for (const p of list) {
    const hit = keysOf(p).map(k => owner.get(k)).find(Boolean);
    if (!hit) {
      kept.set(p.id, p);
      keysOf(p).forEach(k => owner.set(k, p.id));
      continue;
    }
    const prev = kept.get(hit);
    if (completeness(p) > completeness(prev)) {
      kept.set(hit, { ...p, id: prev.id });      // keep the id already registered
      problems.push(`${p.name}: found twice (${prev.region} + ${p.region}) — kept the fuller ${p.region} record`);
    } else {
      problems.push(`${p.name}: found twice (${prev.region} + ${p.region}) — kept the fuller ${prev.region} record`);
    }
    keysOf(p).forEach(k => { if (!owner.has(k)) owner.set(k, hit); });
  }
  return [...kept.values()];
}

const properties = load();

// every pin has to land inside the map frame or it silently vanishes off-canvas
const FRAME = { W: -83.85, E: -81.10, S: 26.50, N: 29.95 };
for (const p of properties) {
  if (p.lon < FRAME.W || p.lon > FRAME.E || p.lat < FRAME.S || p.lat > FRAME.N)
    problems.push(`${p.id}: ${p.lat},${p.lon} falls outside the map frame`);
}

const DATA = {
  generated: 'August 23, 2026',
  dates: DATES,
  regions: REGIONS,
  tiers: {
    exact:   'Best fit — 6–8 bedrooms with kings in most of them',
    strong:  'Strong — right size, kings partly or not yet confirmed',
    backup:  'Worth a look — right size, but the beds are not kings',
    stretch: 'Stretch — outside 6–8 bedrooms, or several keys'
  },
  spec_chips: [
    { dot: '#0e7c8a', text: '<b>1.</b>&nbsp;6–8 bedrooms' },
    { dot: '#d4614a', text: '<b>2.</b>&nbsp;King beds in most of them' },
    { text: '<b>3.</b>&nbsp;Dec 19–27, 2026 · 8 nights' },
    { text: '<b>4.</b>&nbsp;Room for 12–18' },
    { text: '<b>5.</b>&nbsp;Pool, water or real character' }
  ],
  disclaimer:
    'Nothing here is a booking, and no listing calendar could be read directly — every rental platform blocks automated checks. ' +
    'Availability is reported as exactly what was seen: “Dec 19–27 showed open” only where a dated search returned the house, ' +
    '“came back in a Dec 19–27 search” where it appeared in dated results, and “unknown” for everything else, which is most of them. ' +
    'Confirm dates, the bed layout and the real holiday rate with the host or manager before counting on any of it. ' +
    'Prices are whatever the source published — often a shoulder-season nightly rate or a range, not a Christmas-week quote, which will usually be higher. ' +
    'Bed counts are the listing’s own; where a host never published a layout the card says so rather than guessing. ' +
    'Pins sit at each listing’s stated area, not its street address. Fit ranking is our own opinion, not the platforms’.',
  properties
};

writeFileSync(join(APP, 'js', 'data.js'),
  '/* Stay Finder data — FACTS ONLY (ranking lives in js/app.js). Generated by\n' +
  '   build-data.mjs in stay/, from the raw-<region>.json research files. Every\n' +
  '   real listing that was found and read on the "generated" date. */\n' +
  'window.STAY_DATA = ' + JSON.stringify(DATA, null, 1) + ';\n');

const byRegion = {};
for (const p of properties) byRegion[p.region] = (byRegion[p.region] || 0) + 1;
const kings = properties.filter(p => p.beds && p.beds.king > 0).length;
const photos = properties.filter(p => p.photo).length;
console.log(`wrote site/stay/js/data.js — ${properties.length} properties`);
for (const r of REGIONS) console.log(`  ${String(byRegion[r.id] || 0).padStart(3)}  ${r.label}`);
console.log(`  ${kings} with a published king count · ${photos} with a local photo`);
console.log(`  ${properties.filter(p => p.bedrooms >= 6 && p.bedrooms <= 8).length} inside the 6–8 bedroom brief`);
if (problems.length) { console.log('\nnotes:'); problems.forEach(p => console.log('  - ' + p)); }
