// build-draw.mjs — derive a "draw" score (how much of a footprint an act has)
// from evidence already in profiles.merged.json + lineup.json. Writes draw.json,
// which build-data.mjs folds into the payload as each band's `dw`.
//
// There is no attendance or streaming data for a porchfest, so "popular" here
// is an EVIDENCE score, not a measurement: the rooms an act has played, who
// they have opened for, releases, curation/press, and how much of a web
// presence the research could actually verify. It is deliberately conservative
// and it is checked in three ways, because a naive keyword sweep gets this
// wrong in ways that libel real musicians:
//
//   1. NEGATION GUARD. "rather than a road-hardened touring act" is not a
//      touring credit. A negation cue in the words just before a match voids it.
//   2. CONFIDENCE GATING. When the researchers marked an act low-confidence
//      they are saying the text is self-description from a festival bio with
//      nothing to verify it. Text-derived credit is scaled down accordingly,
//      so "this profile rests on their own festival bio" cannot score as a
//      festival booking.
//   3. PRECISE PATTERNS. "aimed at the headlines" is not a headline slot;
//      "the current lineup" is not the radio station; an act that "runs the
//      We Love Fiesta label" is not signed to one; "RADIO BABY" is an album
//      title, not airplay.
//
//   node build-draw.mjs --report
import fs from 'node:fs';

const profs = JSON.parse(fs.readFileSync('profiles.merged.json', 'utf8'));
const lineup = JSON.parse(fs.readFileSync('lineup.json', 'utf8'));
const byName = new Map(lineup.map(b => [b.band_name, b]));

// Rooms, weighted by what playing them actually signals in the Twin Cities.
// A First Avenue booking is a different order of thing from a coffee shop.
const VENUES = [
  [/first\s*ave(nue)?\b/i, 10, 'First Avenue'],
  [/palace theat/i, 9, 'Palace Theatre'],
  [/\bfine line\b/i, 8, 'Fine Line'],
  [/cedar cultural/i, 8, 'Cedar Cultural Center'],
  [/7th st(reet)? entry|seventh street entry/i, 7, '7th St Entry'],
  [/\bturf club\b/i, 7, 'Turf Club'],
  [/\bicehouse\b/i, 6, 'Icehouse'],
  [/varsity theat/i, 6, 'Varsity Theater'],
  [/parkway theat/i, 5, 'Parkway Theater'],
  [/hook (and|&) ladder/i, 5, 'Hook and Ladder'],
  [/\bwhite squirrel\b/i, 4, 'White Squirrel'],
  [/uptown vfw|\bvfw\b/i, 4, 'Uptown VFW'],
  [/\bgreen room\b/i, 4, 'Green Room'],
  [/\baster cafe\b/i, 3, 'Aster Cafe'],
  [/\b331 club\b/i, 3, '331 Club'],
  [/\bday block\b/i, 3, 'Day Block'],
];

// Curation, press and reach — someone outside the band vouched for them.
const REACH = [
  // "The Current" the station, not "the current lineup". Requires a possessive,
  // a preposition, or the call sign.
  [/89\.3|\bKCMP\b|(on|at|for|in)\s+The Current\b|The Current'?s\b/, 9, 'The Current'],
  [/\bNPR\b|city pages|star tribune|\bMPR\b|\bRacket\b|conan o'?brien|\bSXSW\b/i, 8, 'press / national TV'],
  [/\bgrammy\b/i, 12, 'Grammy'],
  [/\baward\b|mn music aw|best new band/i, 5, 'award'],
  // Signed to a label, or a discography credit — but NOT merely naming one.
  // "His father ran Kilimanjaro Records" is family history and "plays ...
  // from Caydence Records" is a record shop, so a bare "X Records" is not
  // enough; there has to be a release preposition or a (Label, year) credit.
  // The month guard keeps "(March 6, 2026)" from reading as a label.
  [/\bsigned to\b|\bon\s+[A-Z][\w'& ]*Records\b|\((?!(?:January|February|March|April|May|June|July|August|September|October|November|December)\b)[A-Z][\w'& ]{2,20},\s*(?:19|20)\d\d\)/, 5, 'label'],
  [/opened for|opening for|shared (the )?stages? with|\bsupported\b/i, 5, 'opened for'],
  [/\bheadlin(ed|ing|er)\b/i, 5, 'headlined'],
  [/sold[- ]out/i, 5, 'sold out'],
  [/\btour(ed|ing)\b|\bwarped tour\b/i, 4, 'touring'],
  [/\bfestival\b|\bfest\b/i, 3, 'festival'],
  // Airplay, not the word "radio". Excludes "radio edit" and album titles.
  [/\bRadio K\b|public radio\b|\bairplay\b|in-?studio\b|\bAmpers\/PRX\b/i, 3, 'radio'],
  [/rock the garden|basilica block|soundset|eaux claires/i, 7, 'major festival'],
];

// Releases separate a working band from neighbours who rehearse in a garage.
const OUTPUT = [
  [/\balbum\b|\bLP\b/i, 3, 'album'],
  [/\bEP\b/i, 2, 'EP'],
  [/\bsingles?\b/i, 1, 'single'],
];

// A match inside a negated clause is not a credit. Checks the run-up to the
// match for a cue that flips its meaning.
const NEGATION = /\b(rather than|not a|not an|no |never |isn'?t|aren'?t|without|little|hasn'?t|haven'?t|rests on (their|its) own|nothing to)\b[^.;]{0,60}$/i;

function hits(text, table) {
  const found = [];
  let score = 0;
  for (const [rx, w, label] of table) {
    const m = rx.exec(text);
    if (!m) continue;
    if (NEGATION.test(text.slice(Math.max(0, m.index - 80), m.index))) continue;
    score += w;
    found.push(label);
  }
  return { score, found };
}

const rows = profs.map(p => {
  const lu = byName.get(p.band_name) || {};
  const text = `${p.profile || ''} ${p.one_liner || ''}`;

  const v = hits(text, VENUES);
  const r = hits(text, REACH);
  const o = hits(text, OUTPUT);

  // Venue credit is dominated by the best room played, not the count — three
  // coffee shops do not add up to the Entry.
  const best = v.found.length
    ? Math.max(...VENUES.filter(([, , l]) => v.found.includes(l)).map(([, w]) => w)) : 0;
  const venueScore = best + Math.min(6, (v.score - best) * 0.4);

  // Low confidence means the research found nothing to verify the text
  // against, so anything the text claims about itself is discounted hard.
  const trust = { high: 1, medium: 0.85, low: 0.35 }[p.confidence] ?? 0.85;
  const textScore = (venueScore + r.score + o.score) * trust;

  // Platform presence is weak evidence on its own — anyone can make a
  // Bandcamp — so it is capped low and not confidence-scaled.
  const platScore = ['spotify_link', 'website_link', 'bandcamp_link'].filter(k => lu[k]).length * 1.5;
  const conf = { high: 5, medium: 2, low: 0 }[p.confidence] ?? 2;
  const src = Math.min(4, (p.sources || []).length);

  return {
    band: p.band_name,
    raw: textScore + platScore + conf + src,
    why: [...v.found, ...r.found, ...o.found].slice(0, 6),
    conf: p.confidence,
  };
});

// Normalise against the strongest act in this lineup, so the scale reads
// "relative to this festival" rather than as a false absolute.
const max = Math.max(...rows.map(r => r.raw));
rows.forEach(r => { r.draw = Math.round((r.raw / max) * 100); });
rows.sort((a, b) => b.draw - a.draw || a.band.localeCompare(b.band));

fs.writeFileSync('draw.json', JSON.stringify(
  Object.fromEntries(rows.map(r => [r.band, { d: r.draw, why: r.why }]))));

if (process.argv.includes('--report')) {
  console.log('rank draw  conf    band                             evidence');
  rows.forEach((r, i) => console.log(
    String(i + 1).padStart(4), String(r.draw).padStart(4), ' ', r.conf.padEnd(7),
    r.band.slice(0, 31).padEnd(33), r.why.join(', ') || '—'));
  const b = { '70+': 0, '50-69': 0, '30-49': 0, '<30': 0 };
  rows.forEach(r => b[r.draw >= 70 ? '70+' : r.draw >= 50 ? '50-69' : r.draw >= 30 ? '30-49' : '<30']++);
  console.log('\nbuckets', JSON.stringify(b));
}
console.log(`wrote draw.json (${rows.length} bands)`);
