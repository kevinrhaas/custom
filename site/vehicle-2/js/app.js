/* Corsair Finder — render + score + filter.
   Data facts live in js/data.js (window.CORSAIR_DATA). All ranking logic is
   here so the data file stays purely factual. Priority order (from Pat):
     1) Red Carpet Metallic exterior            (utmost)
     2) LIGHT seats — Light Smoked Truffle best (utmost); light grey / other
        light faux-leather also welcome; then Medium Smoked Truffle; darker
        (Eternal Red, Ebony) only reluctantly
     3) Reserve or Premiere (never Grand Touring / PHEV)
     4) AWD preferred (FWD tolerated)
     5) panoramic roof + nicer packages preferred
     6) new, or essentially new (lightly used) */

const D = window.CORSAIR_DATA || { vehicles: [], generated: '', spec: {} };
const CRYSTAL_LAKE = { lat: 42.2411, lon: -88.3162 };

/* ---- interior classification ---------------------------------------- */
function interiorClass(v) {
  const s = (v.interior_color || '').toLowerCase();
  if (s.includes('light smoked truffle')) return { rank: 5, label: 'Light Smoked Truffle', light: true };
  if (s.includes('medium smoked truffle')) return { rank: 3, label: 'Medium Smoked Truffle', light: false };
  if (s.includes('smoked truffle')) return { rank: 3, label: v.interior_color, light: false };
  if (/(light gr[ae]y|grey|gray|sandstone|ceramic|dune|light|smoke)/.test(s)) return { rank: 4, label: v.interior_color, light: true };
  if (s.includes('eternal red')) return { rank: 2, label: 'Eternal Red', light: false };
  if (s.includes('ebony') || s.includes('black')) return { rank: 1, label: v.interior_color, light: false };
  return { rank: 1, label: v.interior_color || 'Unknown', light: false };
}
function isRedCarpet(v) { return /red carpet/.test((v.exterior_color || '').toLowerCase()); }

/* swatch color for known interior/exterior names */
function swatch(name) {
  const s = (name || '').toLowerCase();
  if (s.includes('red carpet')) return '#8e1425';
  if (s.includes('light smoked truffle')) return '#c9b79a';
  if (s.includes('medium smoked truffle')) return '#8a6f52';
  if (s.includes('smoked truffle')) return '#9c7f5e';
  if (s.includes('eternal red')) return '#6e1420';
  if (s.includes('ebony') || s.includes('black')) return '#20211f';
  if (/(gr[ae]y|sandstone|ceramic|dune|light)/.test(s)) return '#c3c1bb';
  if (s.includes('white')) return '#eee';
  if (s.includes('blue')) return '#26374d';
  if (s.includes('silver') || s.includes('grey')) return '#b8bcc0';
  return '#9a9284';
}

/* ---- scoring + tier -------------------------------------------------- */
function evaluate(v) {
  const ic = interiorClass(v);
  const red = isRedCarpet(v);
  let score = 0;
  score += red ? 60 : 10;
  score += ic.rank * 10;                         // 10..50
  score += /reserve/i.test(v.trim) ? 14 : /premiere/i.test(v.trim) ? 8 : 0;
  score += v.drivetrain === 'AWD' ? 10 : v.drivetrain === 'FWD' ? 2 : 5;
  score += v.panoramic_roof ? 6 : 0;
  score += Math.max(0, (v.condition === 'new' ? 8 : 5) - (v.mileage || 0) / 1200);
  score += Math.min(6, (v.packages || []).length * 2);
  if (typeof v.distance_mi === 'number') score += Math.max(0, 6 - v.distance_mi / 150); // proximity tiebreaker

  // headline tier keys off the two "utmost" prefs: exterior + light seats
  let tier;
  if (red && ic.rank === 5) tier = 'exact';
  else if (red && (ic.light || ic.rank >= 3)) tier = 'strong';
  else if (red || ic.rank === 5) tier = 'backup';
  else tier = 'stretch';
  return { ...v, _ic: ic, _red: red, _score: score, _tier: tier };
}

/* ---- distance -------------------------------------------------------- */
function haversine(a, b) {
  const R = 3958.8, toRad = d => d * Math.PI / 180;
  const dLat = toRad(b.lat - a.lat), dLon = toRad(b.lon - a.lon);
  const s = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}
function distanceMi(v) {
  if (typeof v.distance_mi === 'number') return v.distance_mi;
  if (typeof v.lat === 'number' && typeof v.lon === 'number')
    return Math.round(haversine(CRYSTAL_LAKE, { lat: v.lat, lon: v.lon }) * 1.18);
  return null;
}

/* ---- rendering ------------------------------------------------------- */
const TIER_LABEL = { exact: 'Exact match', strong: 'Strong match', backup: 'Backup', stretch: 'For reference' };
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const money = n => n == null ? '—' : '$' + Number(n).toLocaleString('en-US');

let VEHICLES = (D.vehicles || []).map(evaluate);
let state = { tier: 'all', sort: 'match', awdOnly: false, redOnly: false, showUnavail: false };
const isGone = v => v.available === false;

/* hex helpers for painting the illustration */
function hexToRgb(h) { const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(h || ''); return m ? [1, 2, 3].map(i => parseInt(m[i], 16)) : [154, 146, 132]; }
function rgbToHex(r) { return '#' + r.map(x => Math.max(0, Math.min(255, Math.round(x))).toString(16).padStart(2, '0')).join(''); }
function shade(hex, amt) { const [r, g, b] = hexToRgb(hex); const f = amt < 0 ? 0 : 255, t = Math.abs(amt); return rgbToHex([r + (f - r) * t, g + (f - g) * t, b + (f - b) * t]); }

/* A clean side-profile crossover, painted in the car's real exterior colour,
   with an interior-colour cabin. Self-contained SVG — no external images. */
let _svgId = 0;
function carSVG(v) {
  const ext = swatch(v.exterior_color), intc = swatch(v.interior_color);
  const light = shade(ext, 0.28), dark = shade(ext, -0.34), rim = shade(ext, -0.5);
  const id = 'g' + (_svgId++);
  const unknown = /unconfirmed/i.test(v.exterior_color || '');
  return `<svg viewBox="0 0 320 150" role="img" aria-label="${esc(v.exterior_color)} Lincoln Corsair">
    <defs>
      <linearGradient id="body${id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="${light}"/><stop offset="0.5" stop-color="${ext}"/><stop offset="1" stop-color="${dark}"/>
      </linearGradient>
      <linearGradient id="glass${id}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#cfe4f2" stop-opacity="0.95"/><stop offset="1" stop-color="#5b7488" stop-opacity="0.95"/>
      </linearGradient>
    </defs>
    <ellipse cx="160" cy="130" rx="118" ry="9" fill="rgba(0,0,0,0.16)"/>
    <!-- body -->
    <path d="M26,112 L28,96 Q30,86 42,83 L70,80 Q92,58 120,54 L206,52 Q236,54 256,78 L286,86 Q294,90 294,102 L294,112 Q294,116 288,116 L32,116 Q26,116 26,112 Z" fill="url(#body${id})" stroke="${rim}" stroke-width="1.5"/>
    <!-- cabin / interior colour showing through glass -->
    <path d="M78,80 Q96,60 121,57 L162,56 L162,80 Z" fill="${intc}"/>
    <path d="M170,56 L204,57 Q230,59 246,79 L170,80 Z" fill="${intc}"/>
    <!-- glass overlay -->
    <path d="M78,80 Q96,60 121,57 L162,56 L162,80 Z" fill="url(#glass${id})" opacity="0.72"/>
    <path d="M170,56 L204,57 Q230,59 246,79 L170,80 Z" fill="url(#glass${id})" opacity="0.72"/>
    <rect x="163" y="56" width="5" height="24" fill="${dark}"/>
    <!-- beltline + rocker -->
    <path d="M42,83 L256,78" fill="none" stroke="${light}" stroke-width="1.4" opacity="0.7"/>
    <rect x="34" y="108" width="256" height="5" rx="2" fill="${rim}" opacity="0.7"/>
    <!-- lights -->
    <rect x="286" y="88" width="7" height="9" rx="2" fill="#c9433f"/>
    <path d="M27,95 L37,93 L37,99 L28,100 Z" fill="#f3f0e2"/>
    <!-- wheels -->
    ${[92, 232].map(cx => `<g><circle cx="${cx}" cy="112" r="20" fill="#15161a"/><circle cx="${cx}" cy="112" r="19" fill="none" stroke="#0a0a0c" stroke-width="2"/><circle cx="${cx}" cy="112" r="10" fill="#c9ccd1"/><circle cx="${cx}" cy="112" r="9" fill="none" stroke="#8a8f96" stroke-width="1"/><circle cx="${cx}" cy="112" r="3" fill="#6b7078"/></g>`).join('')}
    ${unknown ? '<text x="160" y="40" text-anchor="middle" font-size="13" font-family="system-ui" fill="#fff" opacity="0.9">color TBD — call dealer</text>' : ''}
  </svg>`;
}

function condLabel(v) {
  const mi = v.mileage;
  if (v.condition === 'used') return `<span class="used">used · ${mi != null ? Number(mi).toLocaleString() + ' mi' : 'lightly used'}</span>`;
  if (mi != null && mi > 50) return `<span class="used">new · demo, ${Number(mi).toLocaleString()} mi</span>`;
  return '<span class="used" style="color:var(--ok)">new</span>';
}
function attr(k, v, extra = '') { return `<div class="attr"><span class="k">${k}</span><span class="v">${extra}${esc(v)}</span></div>`; }
function sw(name) { return `<span class="swatch" style="background:${swatch(name)}"></span>`; }

function card(v) {
  const dist = distanceMi(v);
  const opts = [...(v.packages || []), ...(v.options || [])];
  const contact = [];
  if (v.dealer_phone) contact.push(`<a class="btn btn-ghost" href="tel:${esc(v.dealer_phone.replace(/[^0-9+]/g, ''))}">☎ ${esc(v.dealer_phone)}</a>`);
  if (v.dealer_email) contact.push(`<a class="btn btn-ghost" href="mailto:${esc(v.dealer_email)}">✉ Email</a>`);
  return `
  <article class="card${isGone(v) ? ' gone' : ''}" data-tier="${v._tier}">
    ${isGone(v) ? '<div class="gone-ribbon">Sold / removed</div>' : ''}
    <div class="card-photo">
      ${carSVG(v)}
      <div class="photo-badges">
        <span class="pb"><span class="swatch" style="background:${swatch(v.exterior_color)}"></span>${esc(v.exterior_color)}</span>
        <span class="pb"><span class="swatch" style="background:${swatch(v.interior_color)}"></span>${esc(v._ic.label)}</span>
      </div>
    </div>
    <div class="card-head">
      <div class="card-title">
        <h3>${esc(v.year)} Lincoln Corsair ${esc(v.trim)}</h3>
        <div class="sub">${esc(v.exterior_color)} · ${esc(v._ic.label)} interior${v.interior_material ? ' · ' + esc(v.interior_material) : ''}</div>
      </div>
      <div style="text-align:right">
        <span class="tier-badge ${v._tier}">${TIER_LABEL[v._tier]}</span>
        <div class="price" style="margin-top:8px">${money(v.price)}${condLabel(v)}</div>
      </div>
    </div>
    <div class="attrs">
      ${attr('Exterior', v.exterior_color, sw(v.exterior_color))}
      ${attr('Interior', v._ic.label, sw(v.interior_color))}
      ${attr('Drivetrain', v.drivetrain || '—')}
      ${attr('Pano roof', v.panoramic_roof ? 'Yes' : (v.panoramic_roof === false ? 'No' : '—'), v.panoramic_roof ? '<span class="chk">✓ </span>' : '')}
      ${attr('Condition', v.condition === 'new' ? 'New' : 'Used')}
      ${attr('Distance', dist != null ? '~' + dist + ' mi' : '—')}
    </div>
    ${opts.length ? `<details class="opts"><summary>Options & packages (${opts.length})</summary><ul>${opts.map(o => `<li>${esc(o)}</li>`).join('')}</ul></details>` : ''}
    ${v.match_notes ? `<div class="note">${esc(v.match_notes)}</div>` : ''}
    <div class="card-foot">
      <div class="dealer">
        <b>${esc(v.dealer_name || 'Dealer')}</b> · <span class="loc">${esc([v.dealer_city, v.dealer_state].filter(Boolean).join(', '))}</span>
        ${dist != null ? ` · <span class="dist">~${dist} mi to Crystal Lake</span>` : ''}
        <div class="vin">VIN ${esc(v.vin || 'n/a')}</div>
      </div>
      <div class="foot-actions">
        ${contact.join('')}
        ${v.listing_url ? `<a class="btn btn-primary" href="${esc(v.listing_url)}" target="_blank" rel="noopener">View listing ↗</a>` : ''}
      </div>
    </div>
  </article>`;
}

function apply() {
  let rows = VEHICLES.slice();
  if (!state.showUnavail) rows = rows.filter(v => !isGone(v));
  if (state.tier !== 'all') rows = rows.filter(v => v._tier === state.tier);
  if (state.awdOnly) rows = rows.filter(v => v.drivetrain === 'AWD');
  if (state.redOnly) rows = rows.filter(v => v._red);
  const sorters = {
    match: (a, b) => b._score - a._score,
    distance: (a, b) => (distanceMi(a) ?? 1e9) - (distanceMi(b) ?? 1e9),
    price: (a, b) => (a.price ?? 1e9) - (b.price ?? 1e9),
  };
  rows.sort(sorters[state.sort]);
  $('#list').innerHTML = rows.length ? rows.map(card).join('') : `<div class="empty">No vehicles match these filters. Loosen them to see more of the ${VEHICLES.length} found.</div>`;
  $('#count').textContent = rows.length;
  const removed = VEHICLES.filter(isGone).length;
  $('#removedNote').textContent = (removed && !state.showUnavail) ? ` · ${removed} sold/removed hidden` : '';
}

function stats() {
  const pool = state.showUnavail ? VEHICLES : VEHICLES.filter(v => !isGone(v));
  const by = t => pool.filter(v => v._tier === t).length;
  $('#s-total').textContent = pool.length;
  $('#s-exact').textContent = by('exact');
  $('#s-strong').textContent = by('strong');
  $('#s-backup').textContent = by('backup') + by('stretch');
  const nearest = VEHICLES.map(distanceMi).filter(d => d != null).sort((a, b) => a - b)[0];
  if (nearest != null) $('#s-nearest') && ($('#s-nearest').textContent = '~' + nearest + ' mi');
}

function wire() {
  document.querySelectorAll('[data-tier-btn]').forEach(b => b.addEventListener('click', () => {
    state.tier = b.dataset.tierBtn;
    document.querySelectorAll('[data-tier-btn]').forEach(x => x.classList.toggle('on', x === b));
    apply();
  }));
  $('#sort').addEventListener('change', e => { state.sort = e.target.value; apply(); });
  $('#awdOnly').addEventListener('change', e => { state.awdOnly = e.target.checked; apply(); });
  $('#redOnly').addEventListener('change', e => { state.redOnly = e.target.checked; apply(); });
  $('#showUnavail').addEventListener('change', e => { state.showUnavail = e.target.checked; stats(); apply(); });
  const t = $('#themeToggle');
  const setT = m => { document.documentElement.setAttribute('data-theme', m); t.textContent = m === 'dark' ? '☀️' : '🌙'; try { localStorage.setItem('corsair.theme', m); } catch (e) {} };
  t.addEventListener('click', () => setT(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));
  if ($('#genDate') && D.generated) $('#genDate').textContent = D.generated;
}

document.addEventListener('DOMContentLoaded', () => { stats(); wire(); apply(); });
