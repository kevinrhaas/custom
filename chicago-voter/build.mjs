// Builds site/chicago-voter/js/data.js from the cited research in research/*.json
// plus the ballot layout below (races in ballot order, names as printed, ballot
// line numbers, and which survey axes each office actually touches).
//
//   node chicago-voter/build.mjs
//
// The research files carry every source URL; nothing here adds a claim about a
// candidate. What this file adds is editorial and says so: the axis weights per
// office, and the judge flag tiers (see JUDGE_FLAGS).

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const R = (f) => JSON.parse(readFileSync(join(here, 'research', f), 'utf8'));
const statewide = R('statewide.json');
const county = R('county.json');
const cps = R('cps_refs.json');
const judgesA = R('judges_a.json');
const judgesB = R('judges_b.json');

export const ELECTION = {
  dateLabel: 'Tuesday, November 3, 2026',
  precinct: 'Ward 30 · Precinct 04',
  ballotStyle: 'Ballot style 124 (English/Spanish)',
  districts: '3rd Congressional · 2nd Legislative · 3rd Representative · 8th County Board · Board of Review 2nd · Judicial Subcircuit 6 · Board of Education Subdistrict 1B',
  asOf: 'October 28, 2026',
};

export const AXES = {
  econ: { name: 'Taxes & spending', lo: 'Raise revenue, expand programs', hi: 'Cut taxes and spending' },
  safety: { name: 'Public safety', lo: 'Reform and prevention first', hi: 'Enforcement first' },
  federal: { name: 'Immigration & Washington', lo: 'Resist federal immigration enforcement', hi: 'Cooperate with ICE' },
  social: { name: 'Rights & guns', lo: 'Progressive on abortion, LGBTQ rights, guns', hi: 'Conservative on them' },
  change: { name: 'Experience vs. shake-up', lo: 'Continuity and experience', hi: 'Outsider, shake things up' },
  taxfair: { name: 'Property taxes', lo: 'Big commercial property pays full share', hi: 'Ease business taxes, easier appeals' },
  green: { name: 'Water & climate', lo: 'Lowest cost, hold the levy', hi: 'Aggressive green infrastructure' },
  union: { name: 'Schools', lo: 'Aligned with the teachers union, fund through borrowing', hi: 'Independent, fiscal discipline, choice' },
};

const PARTY = { Democratic: 'D', Republican: 'R', Libertarian: 'L', 'American Center Party': 'ACP', Independent: 'I' };

// Ballot layout, in ballot order. `nums` are the line numbers printed beside the ovals.
const LAYOUT = [
  // ---- side A, front
  { id: 'us-senate', group: 'Federal & statewide', title: 'United States Senator', short: 'U.S. Senate', es: 'Senador de los Estados Unidos', src: statewide, nums: [1, 2, 3], writeIn: true,
    weights: { econ: 1, social: 1, federal: 0.8, safety: 0.5, change: 0.3 }, partyWeight: 0.6, importance: 1.3 },
  { id: 'governor', group: 'Federal & statewide', title: 'Governor & Lieutenant Governor', short: 'Governor', es: 'Gobernador y Vicegobernador', src: statewide, nums: [4, 5, 6], writeIn: true,
    weights: { econ: 1, safety: 0.8, federal: 0.8, social: 0.7, change: 0.4 }, partyWeight: 0.6, importance: 1.3 },
  { id: 'attorney-general', group: 'Federal & statewide', title: 'Attorney General', short: 'Attorney General', es: 'Fiscal General', src: statewide, nums: [7, 8],
    weights: { safety: 1, federal: 1, social: 0.5, change: 0.4 }, partyWeight: 0.6 },
  { id: 'secretary-of-state', group: 'Federal & statewide', title: 'Secretary of State', short: 'Secretary of State', es: 'Secretario del Estado', src: statewide, nums: [9, 10], writeIn: true,
    weights: { change: 0.7, econ: 0.4, federal: 0.4, social: 0.3 }, partyWeight: 0.6 },
  { id: 'comptroller', group: 'Federal & statewide', title: 'Comptroller', short: 'Comptroller', es: 'Contralor', src: statewide, nums: [11, 12], writeIn: true,
    weights: { econ: 1, change: 0.6 }, partyWeight: 0.6 },
  { id: 'treasurer', group: 'Federal & statewide', title: 'Treasurer', short: 'State Treasurer', es: 'Tesorero', src: statewide, nums: [13, 14], writeIn: true,
    weights: { econ: 1, change: 0.6, social: 0.2 }, partyWeight: 0.6 },
  { id: 'us-house-3', group: 'Congress & Springfield', title: 'U.S. Representative, 3rd District', short: 'U.S. House (IL-3)', es: 'Representante de los EE. UU., Distrito 3', src: county, nums: [21, 22],
    weights: { econ: 1, federal: 1, social: 0.8, safety: 0.5, change: 0.3 }, partyWeight: 0.6 },
  { id: 'state-senate-2', group: 'Congress & Springfield', title: 'State Senator, 2nd District', short: 'State Senate (2nd)', es: 'Senador Estatal, Distrito 2', src: county, nums: [32],
    weights: { econ: 1, safety: 0.6, federal: 0.6, social: 0.6 } },
  { id: 'state-rep-3', group: 'Congress & Springfield', title: 'State Representative, 3rd District', short: 'State House (3rd)', es: 'Representante Estatal, Distrito 3', src: county, nums: [42],
    weights: { econ: 1, safety: 0.6, federal: 0.6, social: 0.6 } },
  { id: 'mwrd-6yr', group: 'Water Reclamation District', title: 'MWRD Commissioners, full 6-year term', short: 'Water District (pick 3)', es: 'Comisionados del Distrito Metropolitano de Reclamación de Aguas', src: county, nums: [51, 52, 53, 54, 55, 56], voteFor: 3,
    weights: { green: 1, econ: 0.5, change: 0.5 }, partyWeight: 0.5 },
  { id: 'mwrd-2yr', group: 'Water Reclamation District', title: 'MWRD Commissioner, unexpired 2-year term', short: 'Water District (2-yr)', src: county, nums: [57],
    weights: { green: 1, econ: 0.5, change: 0.4 } },
  { id: 'county-board-president', group: 'Cook County', title: 'President of the Cook County Board', short: 'County Board President', es: 'Presidente de la Junta del Condado', src: county, nums: [62, 63],
    weights: { econ: 1, change: 0.7, safety: 0.5, federal: 0.4, taxfair: 0.4 }, partyWeight: 0.6 },
  { id: 'county-clerk', group: 'Cook County', title: 'Cook County Clerk', short: 'County Clerk', es: 'Secretario del Condado', src: county, nums: [64], writeIn: true,
    weights: { change: 0.6, federal: 0.3 } },
  { id: 'sheriff', group: 'Cook County', title: 'Cook County Sheriff', short: 'Sheriff', es: 'Alguacil del Condado', src: county, nums: [65, 66],
    weights: { safety: 1, federal: 0.8, change: 0.6, econ: 0.3 }, partyWeight: 0.6 },
  { id: 'county-treasurer', group: 'Cook County', title: 'Cook County Treasurer', short: 'County Treasurer', es: 'Tesorero del Condado', src: county, nums: [67],
    weights: { taxfair: 0.6, change: 0.6 } },
  { id: 'assessor', group: 'Cook County', title: 'Cook County Assessor', short: 'Assessor', es: 'Asesor del Condado', src: county, nums: [68, 69],
    weights: { taxfair: 1, change: 0.6, econ: 0.4 }, partyWeight: 0.5 },
  { id: 'commissioner-8', group: 'Cook County', title: 'Cook County Commissioner, 8th District', short: 'County Commissioner (8th)', es: 'Comisionado del Condado, Distrito 8', src: county, nums: [71, 72],
    weights: { econ: 1, safety: 0.6, federal: 0.6, change: 0.4, social: 0.3 }, partyWeight: 0.6 },
  { id: 'board-of-review-2', group: 'Cook County', title: 'Board of Review, 2nd District', short: 'Board of Review (2nd)', es: 'Junta de Revisión, Distrito 2', src: county, nums: [82],
    weights: { taxfair: 1, change: 0.5 } },
  { id: 'judges-new', group: 'Judges: open seats', title: 'Appellate & Circuit Court vacancies', short: 'Six open judgeships', kind: 'judge', nums: [102, 103, 104, 105, 106, 107],
    note: 'Each of these six seats has a single candidate, the Democrat who won the March primary. You can vote for them or leave the oval blank.' },
  // ---- side A, back
  { id: 'cps-president', group: 'Board of Education', title: 'President of the Chicago Board of Education', short: 'School Board President', es: 'Presidente de la Junta de Educación de Chicago', src: cps, nums: [121, 122, 123, 124], writeIn: true,
    weights: { union: 1, change: 0.6, econ: 0.4 }, importance: 1.2 },
  { id: 'cps-1b', group: 'Board of Education', title: 'Member, Chicago Board of Education, Subdistrict 1B', short: 'School Board (1B)', es: 'Miembro de la Junta de Educación, Subdistrito 1B', src: cps, nums: [131, 132], writeIn: true,
    weights: { union: 1, change: 0.6, econ: 0.4 } },
  // measures: order on the ballot
  // `yes` (editorial) says how a Yes vote reads on the survey axes; it replaces the
  // researcher's scores so the reason line under each pick reads as plain English.
  { id: 'q-millionaire-county', group: 'Public questions', short: 'Millionaire Amendment (county)', measureIndex: 0,
    yes: { econ: { v: -2, why: 'A Yes backs a 3% surcharge on income over $1 million, split between property-tax relief and schools.' } } },
  { id: 'q-shotspotter', group: 'Public questions', short: 'Restart gunshot detection', measureIndex: 1,
    yes: { safety: { v: 1.8, why: 'A Yes asks the city to bring back gunshot-detection sensors, the police technology Mayor Johnson ended in 2024.' } } },
  { id: 'q-festival', group: 'Public questions', short: 'Permanent festival space', measureIndex: 2, lightning: true,
    lightningAsk: 'Should Chicago build a permanent festival grounds for big outdoor events? (Advisory; no site or budget named.)' },
  { id: 'q-midway-blitz', group: 'Public questions', short: 'Midway Blitz cost recovery', measureIndex: 3,
    yes: { federal: { v: -2, why: 'A Yes tells the city to pursue the federal government for the costs of the 2025 Midway Blitz ICE surge.' },
      safety: { v: -0.6, why: 'Supporters frame the surge’s militarized tactics as harmful to public safety.' } } },
  { id: 'q-cps-millionaire', group: 'Public questions', short: 'Millionaire surcharge for schools (CPS)', measureIndex: 4,
    yes: { econ: { v: -2, why: 'A Yes asks Springfield to tax millionaires more and send the money to public schools.' } } },
  { id: 'q-vacant-land', group: 'Public questions', short: 'Vacant-land charge for CPS', measureIndex: 5,
    yes: { econ: { v: -1.6, why: 'A Yes backs a new yearly charge on long-vacant commercial and investment land, paid to CPS.' },
      taxfair: { v: -1.2, why: 'It puts more of the load on commercial and investment property owners.' } } },
  // ---- side B
  { id: 'retain-appellate', group: 'Judges: retention', title: 'Retention, Appellate Court (First District)', short: 'Appellate retention', kind: 'retention', yesNums: [201] },
  { id: 'retain-circuit', group: 'Judges: retention', title: 'Retention, Circuit Court of Cook County', short: 'Circuit retention', kind: 'retention', yesFrom: 203 },
];

// Judge flag tiers (editorial, from the cited ratings):
//   concern  = a major bar (CBA, Chicago Council of Lawyers, ISBA) rated them Not Recommended / Not Qualified
//   caution  = only an Alliance member bar said No, or Injustice Watch documents a notable controversy
//   clean    = positive across every group found
const JUDGE_FLAGS = {
  'lorraine-mary-murphy': 'concern', 'tiesha-l-smith': 'concern',
  'ursula-walowski': 'caution', 'maritza-martinez': 'caution', 'erin-haggerty-antonietti': 'caution',
  'teresa-molina-gonzalez': 'caution', 'gerardo-tristan-jr': 'caution', 'chris-stacey': 'caution',
  'ashonta-c-rice': 'caution', 'steven-q-mckenzie': 'caution',
};
const judgeFlag = (id) => JUDGE_FLAGS[id] || 'clean';

const slug = (s) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

function findByBallot(src, n) {
  for (const race of src.races) for (const c of race.candidates || []) if (Number(c.ballot) === n) return { race, c };
  return null;
}

function axes(a) {
  const out = {};
  for (const [k, v] of Object.entries(a || {})) {
    if (v == null) continue;
    const val = typeof v === 'object' ? v.v : v;
    if (val == null || Number.isNaN(Number(val))) continue;
    out[k] = { v: Number(val), why: (typeof v === 'object' && v.why) || '' };
  }
  return out;
}

function cleanPositions(p) {
  const out = {};
  for (const [k, v] of Object.entries(p || {})) {
    if (!v || /^not found\.?$/i.test(String(v).trim())) continue;
    out[k.replace(/_/g, ' ')] = String(v);
  }
  return out;
}

const arr = (x) => (Array.isArray(x) ? x : x ? [x] : []).filter((s) => s && !/^not found\.?$/i.test(String(s).trim()));
const srcs = (x) => arr(x).filter((s) => s.url && /^https?:/.test(s.url)).map((s) => ({ title: s.title || '', url: s.url }));

const SHORT = { 'Whitfield Harrington Jr': 'Harrington', 'Eira Lizeth Corral Sepúlveda': 'Corral Sepúlveda', 'Elizabeth "Liz" Nicholson': 'Nicholson',
  'Cameron "Cam" Davis': 'Davis', 'JB Pritzker': 'Pritzker' };
const shortName = (n) => SHORT[n] || n.replace(/,?\s+(Jr\.?|Sr\.?|II|III)$/, '').split(' ').slice(-1)[0];
function candidate(c, n, race) {
  const party = c.party || '';
  const pkey = PARTY[party] || (party ? party.slice(0, 3).toUpperCase() : 'NP');
  return {
    id: slug(c.name), name: c.name, short: shortName(c.name),
    ballot: n, party: pkey, partyName: party, incumbent: !!c.incumbent, runningMate: c.running_mate || undefined,
    bio: c.bio || '', quals: c.qualifications || '', positions: cleanPositions(c.positions),
    endorse: arr(c.endorsements), gaps: arr(c.gaps), axes: axes(c.axes), sources: srcs(c.sources),
    withdrawn: c.withdrawn || undefined,
  };
}

function judgeFromResearch(j, extra = {}) {
  const name = j.name;
  return {
    id: slug(name), name, yes: j.yes, no: j.no, ballot: j.ballot, seat: j.seat || '',
    assignment: [j.assignment, j.served_since ? `on the bench since ${j.served_since}` : ''].filter(Boolean).join(' · '),
    bio: j.bio || '', ratings: Object.fromEntries(Object.entries(j.ratings || {}).filter(([, v]) => v)),
    flag: j.flag === 'unknown' ? 'unknown' : judgeFlag(slug(name)), why: j.why || '', iw: j.injustice_watch || '',
    sources: srcs(j.sources), ...extra,
  };
}

const RACES = [];
for (const L of LAYOUT) {
  const base = { id: L.id, group: L.group, title: L.title, short: L.short, es: L.es };
  if (L.measureIndex != null) {
    const m = cps.questions[L.measureIndex];
    RACES.push({ ...base, kind: 'measure', title: m.title, jurisdiction: m.jurisdiction, wording: m.wording, binding: !!m.binding,
      sponsor: m.sponsor, yesMeans: m.yes_means, noMeans: m.no_means, for: arr(m.for), against: arr(m.against), facts: arr(m.facts),
      yes: L.yes || (L.lightning ? {} : axes(m.yes_axes)), lightning: !!L.lightning, lightningAsk: L.lightningAsk || m.wording, sources: srcs(m.sources) });
    continue;
  }
  if (L.kind === 'judge') {
    const list = L.nums.map((n) => {
      const j = judgesA.new_judges.find((x) => Number(x.ballot) === n);
      if (!j) throw new Error(`no research for judge ballot ${n}`);
      return judgeFromResearch(j, { ballot: n });
    });
    RACES.push({ ...base, kind: 'judge', note: L.note, candidates: list });
    continue;
  }
  if (L.kind === 'retention') {
    const all = [...judgesA.retention, ...judgesB.retention];
    const seen = new Set(); const list = [];
    for (const j of all.sort((a, b) => a.yes - b.yes)) {
      if (seen.has(j.yes)) continue; seen.add(j.yes);
      if (L.yesNums ? L.yesNums.includes(j.yes) : j.yes >= L.yesFrom) list.push(judgeFromResearch(j));
    }
    RACES.push({ ...base, kind: 'retention', judges: list, note: judgesB.retention_rule });
    continue;
  }
  const found = L.nums.map((n) => findByBallot(L.src, n));
  const miss = L.nums.filter((n, i) => !found[i]);
  if (miss.length) throw new Error(`${L.id}: no research for ballot numbers ${miss.join(', ')}`);
  const ctxRace = found[0].race;
  RACES.push({ ...base, kind: 'pick', voteFor: L.voteFor || 1, context: ctxRace.context || '', writeIn: !!L.writeIn,
    weights: L.weights, partyWeight: L.partyWeight || 0, importance: L.importance || 1,
    candidates: found.map(({ c }, i) => candidate(c, L.nums[i])) });
}

const out = `// GENERATED by chicago-voter/build.mjs from chicago-voter/research/*.json. Do not edit by hand.
export const ELECTION = ${JSON.stringify(ELECTION, null, 1)};
export const AXES = ${JSON.stringify(AXES, null, 1)};
export const RACES = ${JSON.stringify(RACES)};
`;
const target = join(here, '..', 'site', 'chicago-voter', 'js', 'data.js');
writeFileSync(target, out);
const nJ = RACES.filter((r) => r.kind === 'retention').reduce((a, r) => a + r.judges.length, 0);
console.log(`wrote ${target}: ${RACES.length} races, ${nJ} retention judges, ${(out.length / 1024).toFixed(0)} KB`);
