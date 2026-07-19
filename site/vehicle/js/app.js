/* Vehicle Finder — render + score + filter, multi-search.
   Data facts live in js/data.js (window.FINDER_DATA.searches[]); all ranking
   logic is here so the data stays purely factual. Two searches today:
   - corsair:  Pat's 2026 Lincoln Corsair (Red Carpet Metallic + light seats,
               Reserve/Premiere, AWD preferred, never the Grand Touring PHEV)
   - forester: 2026 Subaru Forester Touring Hybrid (Crimson Red Pearl +
               Touring Brown leather), availability centered on Crystal Lake */

const D = window.FINDER_DATA || { searches: [], generated: '' };
const CRYSTAL_LAKE = { lat: 42.2411, lon: -88.3162 };

/* ---- corsair interior classification -------------------------------- */
function interiorClass(v) {
  const s = (v.interior_color || '').toLowerCase();
  if (s.includes('light smoked truffle')) return { rank: 5, label: 'Light Smoked Truffle', light: true };
  if (s.includes('medium smoked truffle')) return { rank: 3, label: v.interior_color, light: false };
  if (s.includes('smoked truffle')) return { rank: 3, label: v.interior_color, light: false };
  if (/(light gr[ae]y|grey|gray|sandstone|ceramic|dune|light|smoke)/.test(s)) return { rank: 4, label: v.interior_color, light: true };
  if (s.includes('eternal red')) return { rank: 2, label: 'Eternal Red', light: false };
  if (s.includes('ebony') || s.includes('black')) return { rank: 1, label: v.interior_color, light: false };
  return { rank: 1, label: v.interior_color || 'Unknown', light: false };
}

/* swatch color for known color names (both vehicles) */
function swatch(name) {
  const s = (name || '').toLowerCase();
  if (s.includes('red carpet')) return '#8e1425';
  if (s.includes('crimson red')) return '#8c1c2c';
  if (s.includes('light smoked truffle')) return '#c9b79a';
  if (s.includes('medium smoked truffle')) return '#8a6f52';
  if (s.includes('smoked truffle')) return '#9c7f5e';
  if (s.includes('touring brown') || s.includes('brown')) return '#6b4a35';
  if (s.includes('eternal red')) return '#6e1420';
  if (s.includes('ebony') || s.includes('black')) return '#20211f';
  if (/(sandstone|ceramic|dune)/.test(s)) return '#c3c1bb';
  if (s.includes('sand')) return '#cbb99a';
  if (s.includes('white') || s.includes('pearl') && s.includes('crystal')) return '#e9e9e6';
  if (s.includes('blue')) return '#26374d';
  if (s.includes('green')) return '#42513f';
  if (s.includes('bronze')) return '#7a5c3e';
  if (s.includes('silver')) return '#c2c6c9';
  if (/(gr[ae]y|magnetite|graphite)/.test(s)) return '#5c6166';
  if (s.includes('red')) return '#8c1c2c';
  return '#9a9284';
}

/* ---- per-search scoring + tier --------------------------------------- */
function evaluateCorsair(v) {
  const ic = interiorClass(v);
  const red = /red carpet/.test((v.exterior_color || '').toLowerCase());
  let score = 0;
  score += red ? 60 : 10;
  score += ic.rank * 10;
  score += /reserve/i.test(v.trim) ? 14 : /premiere/i.test(v.trim) ? 8 : 0;
  score += v.drivetrain === 'AWD' ? 10 : v.drivetrain === 'FWD' ? 2 : 5;
  score += v.panoramic_roof ? 6 : 0;
  score += Math.max(0, (v.condition === 'new' ? 8 : 5) - (v.mileage || 0) / 1200);
  score += Math.min(6, (v.packages || []).length * 2);
  if (typeof v.distance_mi === 'number') score += Math.max(0, 6 - v.distance_mi / 150);
  if (v.human_verified) score += 15;   // personally confirmed live — trust boost
  let tier;
  if (red && ic.rank === 5) tier = 'exact';
  else if (red && (ic.light || ic.rank >= 3)) tier = 'strong';
  else if (red || ic.rank === 5) tier = 'backup';
  else tier = 'stretch';
  return { ...v, _ic: ic, _target: red, _score: score, _tier: tier };
}

function evaluateForester(v) {
  const ext = (v.exterior_color || '').toLowerCase();
  const trim = (v.trim || '').toLowerCase();
  const crimson = /crimson red/.test(ext);
  const touring = /touring/.test(trim);
  const hybrid = /hybrid/.test(trim);
  const brown = /brown/.test((v.interior_color || '').toLowerCase());
  let score = 0;
  score += crimson ? 60 : 10;
  score += touring ? 30 : /limited/.test(trim) ? 15 : /sport/.test(trim) ? 10 : /premium/.test(trim) ? 8 : 4;
  score += hybrid ? 10 : 0;
  score += brown ? 4 : 0;
  score += Math.max(0, (v.condition === 'new' ? 8 : 5) - (v.mileage || 0) / 1200);
  score += v.panoramic_roof ? 4 : 0;
  if (typeof v.distance_mi === 'number') score += Math.max(0, 12 - v.distance_mi / 60); // proximity weighs more here
  if (v.human_verified) score += 15;
  let tier;
  if (crimson && touring && hybrid) tier = 'exact';
  else if (crimson && hybrid) tier = 'strong';
  else if (touring && hybrid) tier = 'backup';
  else tier = 'stretch';
  return { ...v, _ic: { label: v.interior_color || '—' }, _target: crimson, _score: score, _tier: tier };
}

const EVALUATORS = { corsair: evaluateCorsair, forester: evaluateForester };

/* ---- distance --------------------------------------------------------- */
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

/* ---- helpers ---------------------------------------------------------- */
const TIER_LABEL = { exact: 'Exact match', strong: 'Strong match', backup: 'Backup', stretch: 'For reference' };
const $ = s => document.querySelector(s);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const money = n => n == null ? '—' : '$' + Number(n).toLocaleString('en-US');
const isGone = v => v.available === false;

/* Clean line-art SUV glyph (from the AutoSelector icon family), tinted in the
   car's exterior paint colour — single-colour currentColor icon, fleet style. */
function carSVG(v) {
  const unknown = /not published|unconfirmed/i.test(v.exterior_color || '');
  const c = unknown ? 'var(--text-3)' : swatch(v.exterior_color);
  return `<svg class="car-icon" viewBox="1 4 22 15" style="color:${c}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="${esc(v.exterior_color)}">
    <path d="M3 15v-4l1.5-3.5A1.6 1.6 0 0 1 6 6.5h8l4 4.5h3V15" fill="currentColor" fill-opacity="0.16"/>
    <circle cx="7.5" cy="16" r="1.8"/><circle cx="17" cy="16" r="1.8"/><path d="M9.3 16h5.9"/>
  </svg>${unknown ? '<div class="color-tbd">color TBD — call dealer</div>' : ''}`;
}

/* Value rating + fair-price estimate.
   Corsair: final model year — verified market discounts in this dataset run
   ~5-8% off MSRP on clean new cars and 8-16% off on demo/aged units, so fair
   is anchored there. Forester hybrid: in-demand, observed discounts 0-6%;
   Touring Hybrids without a known MSRP rate against the verified market floor
   (~$41.5-42.4k) and the $42,995 as-configured reference. */
function valueInfo(v, searchId) {
  if (v.price == null) return null;
  const demo = v.condition === 'used' || (v.mileage || 0) > 500;
  let fair = null;
  if (v.msrp) fair = Math.round(v.msrp * (searchId === 'corsair' ? (demo ? 0.87 : 0.93) : (demo ? 0.94 : 0.955)) / 100) * 100;
  else if (searchId === 'forester' && /touring hybrid/i.test(v.trim || '')) fair = 42500;
  if (!fair) return null;
  const rel = (v.price - fair) / fair;
  const rating = rel <= -0.02 ? ['great', 'Great deal'] : rel <= 0.02 ? ['good', 'Good deal'] : rel <= 0.06 ? ['fair', 'Fair price'] : ['high', 'Above market'];
  return { cls: rating[0], label: rating[1], fair, msrp: v.msrp || null };
}

function condLabel(v) {
  const mi = v.mileage;
  if (v.condition === 'used') return `<span class="used">used · ${mi != null ? Number(mi).toLocaleString() + ' mi' : 'lightly used'}</span>`;
  if (mi != null && mi > 50) return `<span class="used">new · demo, ${Number(mi).toLocaleString()} mi</span>`;
  return '<span class="used" style="color:var(--ok)">new</span>';
}
function attr(k, v, extra = '') { return `<div class="attr"><span class="k">${k}</span><span class="v">${extra}${esc(v)}</span></div>`; }
function sw(name) { return `<span class="swatch" style="background:${swatch(name)}"></span>`; }

/* ---- state ------------------------------------------------------------ */
let SEARCH = null;           // active search object from data.js
let VEHICLES = [];           // evaluated vehicles of the active search
let state = { tier: 'all', sort: 'match', awdOnly: false, targetOnly: true, showUnavail: false, hvOnly: false };

function selectSearch(id) {
  SEARCH = D.searches.find(s => s.id === id) || D.searches[0];
  if (!SEARCH) return;
  VEHICLES = (SEARCH.vehicles || []).map(EVALUATORS[SEARCH.id] || evaluateCorsair);
  document.querySelectorAll('[data-search-btn]').forEach(b => b.classList.toggle('on', b.dataset.searchBtn === SEARCH.id));
  $('#heroTitle').innerHTML = esc(SEARCH.title).replace(/(Lincoln Corsair|Forester Touring Hybrid)/, '<span class="grad">$1</span>');
  $('#heroSub').textContent = SEARCH.subtitle;
  $('#specStrip').innerHTML = (SEARCH.spec_chips || []).map(c =>
    `<span class="spec-chip">${c.dot ? `<span class="dot" style="background:${c.dot}"></span> ` : ''}${c.text}</span>`).join('');
  $('#targetLabel').textContent = `${SEARCH.target_color} only`;
  const t = SEARCH.tiers || {};
  $('#legend').innerHTML = ['exact', 'strong', 'backup', 'stretch'].map(k =>
    `<span class="item"><span class="sw" style="background:var(--${k})"></span> ${esc(t[k] || k)}</span>`).join('');
  try { history.replaceState(null, '', '#' + SEARCH.id); } catch (e) {}
  stats(); apply();
}

function card(v) {
  const dist = distanceMi(v);
  const opts = [...(v.packages || []), ...(v.options || [])];
  const contact = [];
  if (v.dealer_phone) contact.push(`<a class="btn btn-ghost" href="tel:${esc(v.dealer_phone.replace(/[^0-9+]/g, ''))}">☎ ${esc(v.dealer_phone)}</a>`);
  if (v.dealer_email) contact.push(`<a class="btn btn-ghost" href="mailto:${esc(v.dealer_email)}">✉ Email</a>`);
  // hosted Monroney PDF (fetched from FordDirect and link-verified at build time)
  if (v.sticker) contact.push(`<a class="btn btn-ghost" href="${esc(v.sticker)}" target="_blank" rel="noopener">📄 Window sticker</a>`);
  return `
  <article class="card${isGone(v) ? ' gone' : ''}" data-tier="${v._tier}">
    ${isGone(v) ? '<div class="gone-ribbon">Sold / removed</div>' : ''}
    <div class="card-photo">
      ${carSVG(v)}
      ${v.photo ? `<button class="photo-thumb" type="button" data-photo="${esc(v.photo)}" aria-label="View dealer photo"><img src="${esc(v.photo)}" alt="" loading="lazy"><span>📷 photo</span></button>` : ''}
      <div class="photo-badges">
        <span class="pb"><span class="swatch" style="background:${swatch(v.exterior_color)}"></span>${esc(v.exterior_color)}</span>
        <span class="pb"><span class="swatch" style="background:${swatch(v.interior_color)}"></span>${esc(v._ic.label)}</span>
      </div>
    </div>
    <div class="card-head">
      <div class="card-title">
        <h3>${esc(v.year)} ${esc(SEARCH.id === 'forester' ? 'Subaru Forester' : 'Lincoln Corsair')} ${esc(v.trim)}</h3>
        <div class="sub">${esc(v.exterior_color)} · ${esc(v._ic.label)} interior${v.interior_material ? ' · ' + esc(v.interior_material) : ''}</div>
      </div>
      <div style="text-align:right">
        ${v.human_verified
          ? '<span class="hv-badge" title="Personally confirmed live on the dealer site">✓ human-verified</span> '
          : '<span class="rv-badge" title="Found and checked automatically — not yet clicked by a human. Confirm with the dealer before acting.">🤖 robot-found</span> '}<span class="tier-badge ${v._tier}">${TIER_LABEL[v._tier]}</span>
        <div class="price" style="margin-top:8px">${money(v.price)}${condLabel(v)}</div>
        ${(() => { const vi = valueInfo(v, SEARCH.id); return vi ? `<div class="value-line"><span class="val val-${vi.cls}">${vi.label}</span><span class="fair">fair ≈ ${money(vi.fair)}${vi.msrp ? ' · MSRP ' + money(vi.msrp) : ''}</span></div>` : (v.msrp ? `<div class="value-line"><span class="fair">MSRP ${money(v.msrp)} · call for price</span></div>` : ''); })()}
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
  if (state.hvOnly) rows = rows.filter(v => v.human_verified);
  if (state.targetOnly) rows = rows.filter(v => v._target);
  const sorters = {
    match: (a, b) => b._score - a._score,
    distance: (a, b) => (distanceMi(a) ?? 1e9) - (distanceMi(b) ?? 1e9),
    price: (a, b) => (a.price ?? 1e9) - (b.price ?? 1e9),
  };
  rows.sort(sorters[state.sort]);
  $('#list').innerHTML = rows.length ? rows.map(card).join('') : `<div class="empty">No vehicles match these filters. Loosen them to see more of the ${VEHICLES.length} found.</div>`;
  $('#count').textContent = rows.length;
  const removed = VEHICLES.filter(isGone).length;
  const notes = [];
  if (removed && !state.showUnavail) notes.push(`${removed} sold/removed hidden`);
  if (state.targetOnly) notes.push(`non–${SEARCH.target_color} hidden (uncheck to see all)`);
  $('#removedNote').textContent = notes.length ? ' · ' + notes.join(' · ') : '';
}

function stats() {
  const pool = state.showUnavail ? VEHICLES : VEHICLES.filter(v => !isGone(v));
  const by = t => pool.filter(v => v._tier === t).length;
  $('#s-total').textContent = pool.length;
  $('#s-exact').textContent = by('exact');
  $('#s-strong').textContent = by('strong');
  $('#s-backup').textContent = by('backup') + by('stretch');
}

/* lightbox for real dealer photos */
function openLightbox(src) {
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = `<img src="${esc(src)}" alt="Dealer photo"><span class="lb-hint">click anywhere to close</span>`;
  lb.addEventListener('click', () => lb.remove());
  document.addEventListener('keydown', function onEsc(e) { if (e.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', onEsc); } });
  document.body.appendChild(lb);
}

function wire() {
  document.addEventListener('click', e => {
    const t = e.target.closest('.photo-thumb');
    if (t) openLightbox(t.dataset.photo);
  });
  document.querySelectorAll('[data-search-btn]').forEach(b => b.addEventListener('click', () => selectSearch(b.dataset.searchBtn)));
  document.querySelectorAll('[data-tier-btn]').forEach(b => b.addEventListener('click', () => {
    state.tier = b.dataset.tierBtn;
    document.querySelectorAll('[data-tier-btn]').forEach(x => x.classList.toggle('on', x === b));
    apply();
  }));
  document.querySelectorAll('[data-sort-btn]').forEach(b => b.addEventListener('click', () => {
    state.sort = b.dataset.sortBtn;
    document.querySelectorAll('[data-sort-btn]').forEach(x => x.classList.toggle('on', x === b));
    apply();
  }));
  $('#awdOnly').addEventListener('change', e => { state.awdOnly = e.target.checked; apply(); });
  $('#hvOnly').addEventListener('change', e => { state.hvOnly = e.target.checked; apply(); });
  $('#targetOnly').addEventListener('change', e => { state.targetOnly = e.target.checked; apply(); });
  $('#showUnavail').addEventListener('change', e => { state.showUnavail = e.target.checked; stats(); apply(); });
  const t = $('#themeToggle');
  const setT = m => { document.documentElement.setAttribute('data-theme', m); t.textContent = m === 'dark' ? '☀️' : '🌙'; try { localStorage.setItem('finder.theme', m); } catch (e) {} };
  t.addEventListener('click', () => setT(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'));
  if ($('#genDate') && D.generated) $('#genDate').textContent = D.generated;
}

document.addEventListener('DOMContentLoaded', () => {
  wire();
  const hash = (location.hash || '').replace('#', '');
  selectSearch(D.searches.some(s => s.id === hash) ? hash : 'corsair');
});
