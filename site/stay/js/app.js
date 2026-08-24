/* Stay Finder — render + fit scoring + filters + the Gulf Coast map.
   Facts live in js/data.js (window.STAY_DATA, compiled by build_data.mjs from
   the per-region research files); map geometry lives in js/geo.js. All ranking
   logic is here so the data stays purely factual — same split as the Vehicle
   Finder next door.

   The search: 6-8 bedrooms, king beds in as many of them as possible, Dec 19-27
   2026, anywhere from Cedar Key down to Siesta Key and inland to Crystal
   Springs. Nobody's live calendar was reachable, so availability is reported as
   what we actually saw, never as a promise. */

const D = window.STAY_DATA || { properties: [], regions: [], generated: '' };
const GEO = window.STAY_GEO || null;
const TPA = { lat: 27.9755, lon: -82.5332 };          // Tampa International

const $ = s => document.querySelector(s);
const $$ = s => Array.from(document.querySelectorAll(s));
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const money = n => n == null ? null : '$' + Number(n).toLocaleString('en-US');

/* ---- beds ------------------------------------------------------------- */
/* A listing that never published its bed layout is not the same as one that
   published "no kings" — the first stays unknown and is never scored as zero. */
function bedInfo(p) {
  const b = p.beds || {};
  const known = ['king', 'queen', 'full', 'twin', 'sofa', 'bunk'].some(k => typeof b[k] === 'number');
  const king = typeof b.king === 'number' ? b.king : null;
  const total = known ? ['king', 'queen', 'full', 'twin', 'bunk'].reduce((s, k) => s + (b[k] || 0), 0) : null;
  const ratio = (king != null && p.bedrooms) ? king / p.bedrooms : null;
  return { known, king, total, ratio, b };
}

/* ---- fit score + tier -------------------------------------------------- */
/* The party: three couples — the parents, a brother and his partner, the host
   couple — plus three adult children in their twenties. Nine people, five or
   six rooms, and exactly THREE kings, one per couple. A fourth king earns
   nothing: the twenty-somethings want a decent queen, not another master. And
   a house built for eighteen is the wrong house even when the bedroom count
   fits, so capacity well past the group is a penalty, not a feature. */
const GROUP = 9, KINGS_WANTED = 3;

function evaluate(p) {
  const bi = bedInfo(p);
  const inRange = p.bedrooms >= 5 && p.bedrooms <= 6;
  let score = 0;

  score += inRange ? 40 : (p.bedrooms === 4 || p.bedrooms === 7) ? 15 : 4;

  // Kings score toward three and then stop. Nothing above KINGS_WANTED counts.
  if (bi.king != null) {
    const got = Math.min(bi.king, KINGS_WANTED);
    score += got === 3 ? 26 : got === 2 ? 18 : got === 1 ? 10 : 3;
  } else {
    score += 8;                                     // unstated — mildly penalised, not zeroed
  }

  const sl = p.sleeps || 0;
  if (sl === 0) score += 0;                         // capacity not published
  else if (sl < GROUP) score -= 14;                 // cannot fit everyone
  else if (sl <= 12) score += 12;                   // right-sized for nine
  else if (sl <= 15) score += 4;
  else score -= 8;                                  // built for a much bigger group
  if (p.bedrooms >= 8) score -= 6;                  // more house than this trip needs

  const am = (p.amenities || []).join(' ').toLowerCase();
  const tg = (p.tags || []).join(' ').toLowerCase();
  const heated = /heated (pool|spa)/.test(am);
  const pool = /pool/.test(am) || /pool/.test(tg);
  score += heated ? 11 : pool ? 8 : 0;              // December in Florida: an unheated pool is decor
  if (/hot tub|spa/.test(am)) score += 3;
  if (/fireplace/.test(am + ' ' + tg)) score += 4;  // Christmas week, and inland nights get cool
  if (/waterfront|beachfront|gulf front|bayfront|riverfront|dock|lakefront/.test(am + ' ' + tg)) score += 7;
  if (/elevator/.test(am)) score += 3;              // the parents, and eight days of stairs
  if (/bunk/.test(am + ' ' + tg) || (bi.b && bi.b.bunk > 0)) score -= 4;   // nine adults, no children

  score += p.availability === 'confirmed_open' ? 12
         : p.availability === 'search_listed' ? (p.total_est != null ? 10 : 6) : 0;
  if ((p.images || []).length || p.photo) score += 3;
  if (p.nightly_est != null || p.total_est != null) score += 2;
  if (p.compound) score -= 5;                       // several keys, several contracts

  const d = distanceMi(p);
  if (d != null) score += Math.max(0, 7 - d / 22);

  let tier;
  const kings = bi.king;
  if (inRange && kings >= KINGS_WANTED) tier = 'exact';
  else if (inRange && (kings > 0 || kings == null)) tier = 'strong';
  else if (inRange) tier = 'backup';
  else tier = 'stretch';

  return { ...p, _bi: bi, _score: score, _tier: tier, _dist: d,
           _oversized: sl >= 16 || p.bedrooms >= 8 };
}

/* ---- distance to TPA --------------------------------------------------- */
function haversine(a, b) {
  const R = 3958.8, toRad = x => x * Math.PI / 180;
  const dLat = toRad(b.lat - a.lat), dLon = toRad(b.lon - a.lon);
  const s = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}
function distanceMi(p) {
  if (typeof p.lat !== 'number' || typeof p.lon !== 'number') return null;
  return Math.round(haversine(TPA, { lat: p.lat, lon: p.lon }) * 1.2);   // straight line -> road-ish
}

/* ---- booking link with our dates already in it ------------------------- */
/* Airbnb and Vrbo both read check-in/check-out off the query string, so the
   host's calendar opens on Dec 19-27 instead of today. Anything else is left
   exactly as found — inventing query params for a PM site's booking engine
   would just produce a broken link. */
function datedUrl(p) {
  const u = p.url || '';
  const { checkin, checkout, guests } = D.dates || {};
  if (!u || !checkin) return u;
  try {
    const url = new URL(u);
    const h = url.hostname.replace(/^www\./, '');
    if (h.endsWith('airbnb.com')) {
      url.searchParams.set('check_in', checkin);
      url.searchParams.set('check_out', checkout);
      if (guests) url.searchParams.set('adults', guests);
    } else if (h.endsWith('vrbo.com') || h.endsWith('homeaway.com')) {
      url.searchParams.set('startDate', checkin);
      url.searchParams.set('endDate', checkout);
      if (guests) url.searchParams.set('adults', guests);
    } else {
      return u;
    }
    return url.toString();
  } catch (e) { return u; }
}

/* ====================== the map =======================================
   Plain SVG, no tile server and no map library — same approach as the
   Porchfest route map. Geometry is baked into js/geo.js at build time and
   projected here; panning and zooming just move the viewBox, clamped so the
   view can never wander off the edge of the data into blank water. */

const MAP = (() => {
  if (!GEO) return null;
  const [W, S, E, N] = GEO.bbox;
  const SCALE = 1000 / (E - W);
  const mercY = lat => (180 / Math.PI) * Math.log(Math.tan(Math.PI / 4 + lat * Math.PI / 360));
  const Y0 = mercY(N), H = (Y0 - mercY(S)) * SCALE;
  const px = lon => (lon - W) * SCALE;
  const py = lat => (Y0 - mercY(lat)) * SCALE;
  const FRAME = { x: 0, y: 0, w: 1000, h: H };
  const d = pts => pts.map((p, i) => (i ? 'L' : 'M') + px(p[0]).toFixed(1) + ' ' + py(p[1]).toFixed(1)).join('');
  const dz = pts => d(pts) + 'Z';
  return { W, S, E, N, H, px, py, d, dz, FRAME };
})();

/* Towns worth a label — enough to orient without turning the map into a
   gazetteer. Coordinates are the town centres. */
const TOWNS = [
  { n: 'Tampa', lat: 27.951, lon: -82.457, big: 1 },
  { n: 'St. Petersburg', lat: 27.771, lon: -82.640, big: 1 },
  { n: 'Clearwater', lat: 27.966, lon: -82.800 },
  { n: 'Sarasota', lat: 27.337, lon: -82.531, big: 1 },
  { n: 'Bradenton', lat: 27.499, lon: -82.575 },
  { n: 'Lakeland', lat: 28.039, lon: -81.950 },
  { n: 'Ocala', lat: 29.187, lon: -82.140, big: 1 },
  { n: 'Brooksville', lat: 28.555, lon: -82.388 },
  { n: 'Dade City', lat: 28.365, lon: -82.196 },
  { n: 'Crystal Springs', lat: 28.180, lon: -82.140, star: 1 },
  { n: 'Zephyrhills', lat: 28.234, lon: -82.181 },
  { n: 'Plant City', lat: 28.019, lon: -82.114 },
  { n: 'Crystal River', lat: 28.902, lon: -82.593, star: 1 },
  { n: 'Homosassa', lat: 28.781, lon: -82.613 },
  { n: 'Cedar Key', lat: 29.136, lon: -83.033, star: 1 },
  { n: 'Chiefland', lat: 29.474, lon: -82.859 },
  { n: 'Dunnellon', lat: 29.049, lon: -82.461 },
  { n: 'Tarpon Springs', lat: 28.146, lon: -82.757 },
  { n: 'Winter Haven', lat: 28.022, lon: -81.733 },
  { n: 'Anna Maria Is.', lat: 27.531, lon: -82.735 },
  { n: 'Siesta Key', lat: 27.266, lon: -82.552 },
  { n: 'Weeki Wachee', lat: 28.517, lon: -82.573 },
  { n: 'Steinhatchee', lat: 29.671, lon: -83.389 },
  { n: 'Suwannee', lat: 29.328, lon: -83.140 },
  { n: 'Inverness', lat: 28.836, lon: -82.330 },
  { n: 'Venice', lat: 27.100, lon: -82.454 },
  { n: 'Boca Grande', lat: 26.749, lon: -82.263 },
  { n: 'Punta Gorda', lat: 26.930, lon: -82.045 },
  { n: 'Lake Wales', lat: 27.901, lon: -81.586 },
  { n: 'TPA', lat: 27.9755, lon: -82.5332, air: 1 }
];

function buildBasemap() {
  if (!MAP) return '';
  const g = GEO, out = [];
  out.push(`<rect x="0" y="0" width="1000" height="${MAP.H.toFixed(1)}" fill="var(--water)"/>`);
  // land first, then bays and passes carved back out of it
  for (const f of g.land) out.push(`<path class="land" fill-rule="evenodd" d="${f.p.map(MAP.dz).join('')}"/>`);
  for (const f of g.water) out.push(`<path class="bay" fill-rule="evenodd" d="${f.p.map(MAP.dz).join('')}"/>`);
  for (const f of g.rivers) out.push(`<path class="river${f.m ? ' major' : ''}" d="${MAP.d(f.l)}"/>`);
  for (const f of g.lakes) out.push(`<path class="lake" fill-rule="evenodd" d="${f.p.map(MAP.dz).join('')}"/>`);
  out.push(`<text class="arealbl" x="${MAP.px(-83.62).toFixed(1)}" y="${MAP.py(28.55).toFixed(1)}" transform="rotate(-64 ${MAP.px(-83.62).toFixed(1)} ${MAP.py(28.55).toFixed(1)})">The Gulf</text>`);
  for (const t of TOWNS) {
    const x = MAP.px(t.lon), y = MAP.py(t.lat);
    const tf = `translate(${x.toFixed(1)} ${y.toFixed(1)})`;
    if (t.air) {
      out.push(`<g class="town" data-tf="${tf}" transform="${tf}"><path class="citydot" transform="rotate(45) scale(.4) translate(-10 -10)" d="M10 0l-2 6-8 3v2l8-1 1 5-3 2v2l4-1 4 1v-2l-3-2 1-5 8 1v-2l-8-3z"/><text class="citylbl" x="6" y="3">TPA</text></g>`);
    } else {
      const r = t.big ? 2.6 : t.star ? 2.4 : 1.8;
      out.push(`<g class="town" data-tf="${tf}" transform="${tf}"><circle class="citydot" cx="0" cy="0" r="${r}"${t.star ? ' style="fill:var(--coral)"' : ''}/><text class="citylbl" x="${(r + 2.5).toFixed(1)}" y="3"${t.big ? ' style="font-size:10.5px;font-weight:700"' : ''}>${esc(t.n)}</text></g>`);
    }
  }
  return out.join('');
}

/* ---- map view state ---------------------------------------------------- */
let view = null, mapReady = false;

function clampView(v) {
  const F = MAP.FRAME;
  v.w = Math.min(v.w, F.w); v.h = Math.min(v.h, F.h);
  v.x = Math.max(F.x, Math.min(v.x, F.x + F.w - v.w));
  v.y = Math.max(F.y, Math.min(v.y, F.y + F.h - v.h));
  return v;
}
function applyView() {
  const svg = $('#map');
  svg.setAttribute('viewBox', `${view.x.toFixed(1)} ${view.y.toFixed(1)} ${view.w.toFixed(1)} ${view.h.toFixed(1)}`);
  /* Everything that should stay the same size on screen — pins, town markers,
     labels — is drawn in user units, so it has to shrink as the view zooms in.
     k is exactly the view's share of the full frame, so scaling by k holds
     screen size constant. Strokes use non-scaling-stroke and need no help. */
  const k = view.w / MAP.FRAME.w;
  svg.style.setProperty('--k', k.toFixed(4));
  $$('#map .pin, #map .town').forEach(el => el.setAttribute('transform', el.dataset.tf + ` scale(${k.toFixed(4)})`));
}
function fitToPins(list) {
  const pts = list.filter(p => typeof p.lat === 'number' && typeof p.lon === 'number');
  const F = MAP.FRAME;
  if (!pts.length) { view = { ...F }; return applyView(); }
  let x1 = Infinity, y1 = Infinity, x2 = -Infinity, y2 = -Infinity;
  for (const p of pts) {
    const x = MAP.px(p.lon), y = MAP.py(p.lat);
    x1 = Math.min(x1, x); x2 = Math.max(x2, x); y1 = Math.min(y1, y); y2 = Math.max(y2, y);
  }
  const padX = Math.max(70, (x2 - x1) * 0.14), padY = Math.max(70, (y2 - y1) * 0.14);
  x1 -= padX; x2 += padX; y1 -= padY; y2 += padY;
  // grow the short side so the view keeps the viewport's aspect ratio
  const box = $('#map').getBoundingClientRect();
  const aspect = (box.width || 520) / (box.height || 640);
  let w = x2 - x1, h = y2 - y1;
  if (w / h < aspect) { const nw = h * aspect; x1 -= (nw - w) / 2; w = nw; }
  else { const nh = w / aspect; y1 -= (nh - h) / 2; h = nh; }
  view = clampView({ x: x1, y: y1, w, h });
  applyView();
}
function zoomBy(f, cx, cy) {
  const nx = cx == null ? view.x + view.w / 2 : cx, ny = cy == null ? view.y + view.h / 2 : cy;
  const w = view.w * f, h = view.h * f;
  view = clampView({ x: nx - (nx - view.x) * f, y: ny - (ny - view.y) * f, w, h });
  applyView();
}

function pinColor(p) { return `var(--${p._tier})`; }

/* Several houses can sit on the same beach block, and stacked pins are
   unclickable. Fan any exact-ish coincidence out around a small circle —
   deterministic, so pins don't jump between renders. */
function spread(pts) {
  const NEAR = 11;                                   // pin radius plus a gap
  const sorted = pts.slice().sort((a, b) => a.id < b.id ? -1 : 1);   // stable clusters
  const clusters = [];
  for (const p of sorted) {
    const x = MAP.px(p.lon), y = MAP.py(p.lat);
    const c = clusters.find(c => Math.hypot(c.x - x, c.y - y) < NEAR);
    if (c) c.members.push(p); else clusters.push({ x, y, members: [p] });
  }
  const off = {};
  for (const c of clusters) {
    const n = c.members.length;
    if (n === 1) { off[c.members[0].id] = [0, 0]; continue; }
    // fan out on a ring big enough that neighbours clear each other
    const r = Math.max(10, (NEAR * n) / (2 * Math.PI) + 4);
    c.members.forEach((p, i) => {
      const a = (i / n) * Math.PI * 2 - Math.PI / 2;
      off[p.id] = [c.x - MAP.px(p.lon) + Math.cos(a) * r, c.y - MAP.py(p.lat) + Math.sin(a) * r];
    });
  }
  return off;
}

function renderPins(list, allList) {
  if (!MAP) return;
  const g = $('#pins');
  const shown = new Set(list.map(p => p.id));
  const placed = allList.filter(p => typeof p.lat === 'number' && typeof p.lon === 'number');
  const off = spread(placed);
  g.innerHTML = placed
    .map(p => {
      const o = off[p.id] || [0, 0];
      const x = MAP.px(p.lon) + o[0], y = MAP.py(p.lat) + o[1];
      const idx = p._idx;
      const tf = `translate(${x.toFixed(1)} ${y.toFixed(1)})`;
      return `<g class="pin${shown.has(p.id) ? '' : ' dim'}" data-id="${esc(p.id)}" data-tf="${tf}" transform="${tf}" style="color:${pinColor(p)}" tabindex="0" role="button" aria-label="${esc(p.name)}">
        <circle class="halo" r="17"/>
        <circle class="dot" r="10"/>
        <text y="3">${idx != null ? idx : ''}</text>
      </g>`;
    }).join('');
}

function initMap(all) {
  if (!MAP) return;
  const svg = $('#map');
  svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
  svg.innerHTML = `<g id="basemap">${buildBasemap()}</g><g id="pins"></g>`;
  view = { ...MAP.FRAME };
  mapReady = true;

  // drag to pan
  let drag = null;
  const toUser = e => {
    const r = svg.getBoundingClientRect();
    const k = Math.max(view.w / r.width, view.h / r.height);           // 'meet' scale
    const offX = (r.width - view.w / k) / 2, offY = (r.height - view.h / k) / 2;
    return { x: view.x + (e.clientX - r.left - offX) * k, y: view.y + (e.clientY - r.top - offY) * k, k };
  };
  svg.addEventListener('pointerdown', e => {
    if (e.target.closest('.pin')) return;
    drag = { ...toUser(e), vx: view.x, vy: view.y, moved: false };
    svg.setPointerCapture(e.pointerId); svg.classList.add('dragging');
  });
  svg.addEventListener('pointermove', e => {
    if (!drag) return;
    const r = svg.getBoundingClientRect();
    const k = Math.max(view.w / r.width, view.h / r.height);
    const dx = (e.clientX - (drag.cx0 ?? e.clientX));
    if (!drag.cx0) { drag.cx0 = e.clientX; drag.cy0 = e.clientY; return; }
    drag.moved = true;
    view = clampView({ x: drag.vx - (e.clientX - drag.cx0) * k, y: drag.vy - (e.clientY - drag.cy0) * k, w: view.w, h: view.h });
    applyView();
  });
  const endDrag = e => { if (drag) { svg.classList.remove('dragging'); drag = null; } };
  svg.addEventListener('pointerup', endDrag);
  svg.addEventListener('pointercancel', endDrag);

  svg.addEventListener('wheel', e => {
    e.preventDefault();
    const u = toUser(e);
    zoomBy(e.deltaY > 0 ? 1.18 : 1 / 1.18, u.x, u.y);
  }, { passive: false });

  $('#zIn').onclick = () => zoomBy(1 / 1.35);
  $('#zOut').onclick = () => zoomBy(1.35);
  $('#zFit').onclick = () => fitToPins(shownList);

  // pin -> card
  const tip = $('#maptip');
  svg.addEventListener('click', e => {
    const pin = e.target.closest('.pin'); if (!pin) return;
    selectCard(pin.dataset.id, true);
  });
  svg.addEventListener('keydown', e => {
    const pin = e.target.closest('.pin');
    if (pin && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); selectCard(pin.dataset.id, true); }
  });
  svg.addEventListener('pointerover', e => {
    const pin = e.target.closest('.pin'); if (!pin) return;
    const p = BY_ID[pin.dataset.id]; if (!p) return;
    const bi = p._bi;
    tip.innerHTML = `<b>${esc(p.name)}</b><span class="m">${esc(p.city || '')}${p.neighborhood ? ' · ' + esc(p.neighborhood) : ''}<br>${p.bedrooms} BR${bi.king ? ` · ${bi.king} king${bi.king > 1 ? 's' : ''}` : ''}${p.sleeps ? ` · sleeps ${p.sleeps}` : ''}</span>`;
    tip.classList.add('on');
  });
  svg.addEventListener('pointermove', e => {
    if (!tip.classList.contains('on')) return;
    const r = $('.mapbody').getBoundingClientRect();
    let x = e.clientX - r.left + 14, y = e.clientY - r.top + 14;
    if (x + 240 > r.width) x = e.clientX - r.left - 246;
    if (y + 90 > r.height) y = e.clientY - r.top - 96;
    tip.style.left = x + 'px'; tip.style.top = y + 'px';
  });
  svg.addEventListener('pointerout', e => {
    if (!e.relatedTarget || !e.relatedTarget.closest || !e.relatedTarget.closest('.pin')) tip.classList.remove('on');
  });
}

/* ====================== cards ========================================== */
const ICON = {
  bed: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18V7M3 12h18v6"/><path d="M21 18v-4a2 2 0 00-2-2H7"/><circle cx="7" cy="9.5" r="1.6"/></svg>',
  bath: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16v3a4 4 0 01-4 4H8a4 4 0 01-4-4z"/><path d="M6 12V6a2 2 0 013.4-1.4"/><path d="M7 19l-1 2M17 19l1 2"/></svg>',
  people: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5 6-5s6 1.7 6 5"/><circle cx="17.5" cy="8.5" r="2.6"/><path d="M16 15c3 0 5 1.7 5 5"/></svg>',
  pin: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-6.2 7-11a7 7 0 10-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
  house: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10.5V20h13v-9.5"/><path d="M9.5 20v-5.5h5V20"/></svg>',
  ext: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M18 14v5a1 1 0 01-1 1H5a1 1 0 01-1-1V7a1 1 0 011-1h5"/></svg>',
  phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M5 3h4l2 5-2.5 1.5a12 12 0 006 6L16 13l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z"/></svg>'
};
const TIER_LABEL = { exact: 'Best fit', strong: 'Strong', backup: 'Worth a look', stretch: 'Stretch' };
/* A dated search that came back with a priced eight-night total is much
   stronger evidence than merely appearing in a list: the platform's own engine
   costed Dec 19-27 for that house. Say so, rather than flattening it into the
   same "listed" bucket as a listing we only glimpsed. */
function availInfo(p) {
  if (p.availability === 'confirmed_open') return ['confirmed', '✓', 'Dec 19–27 showed open'];
  if (p.availability === 'search_listed') {
    return p.total_est != null
      ? ['confirmed', '✓', 'Priced for Dec 19–27 — all 8 nights quoted']
      : ['listed', '◐', 'Came back in a Dec 19–27 search'];
  }
  return ['unknown', '?', 'Dates not checkable — ask the host'];
}

function bedsLine(p) {
  const bi = p._bi, b = bi.b;
  if (!bi.known) return `<div class="beds-line"><span class="unk">Bed layout not published — worth asking, since the kings matter.</span></div>`;
  const parts = [];
  const push = (k, label) => { if (b[k]) parts.push(`<b>${b[k]}</b> ${label}${b[k] > 1 ? 's' : ''}`); };
  push('king', 'king'); push('queen', 'queen'); push('full', 'full');
  push('twin', 'twin'); push('bunk', 'bunk'); push('sofa', 'sofa bed');
  return `<div class="beds-line">${parts.join(' · ') || '<span class="unk">Bed layout not published</span>'}</div>`;
}

function priceBlock(p) {
  const n = p.nightly_est, t = p.total_est;
  if (n == null && t == null) return `<div class="price"><span class="none">No public rate — ask for a Christmas-week quote</span></div>`;
  const bits = [];
  if (n != null) bits.push(`<span class="n">${money(n)}</span><span class="per">/night</span>`);
  if (t != null) bits.push(`<span class="tot">${n != null ? '· ' : '<span class="n">'}${money(t)}${n == null ? '</span>' : ''} for the 8 nights</span>`);
  return `<div class="price">${bits.join(' ')}</div>${p.price_note ? `<div class="price"><span class="est">${esc(p.price_note)}</span></div>` : ''}`;
}

function card(p) {
  const bi = p._bi;
  /* Prefer the copy saved into photos/ — the remote CDN links are the first
     thing to rot, and some hosts refuse hotlinks outright. Remote is the
     fallback, and a drawn placeholder is the fallback to that. */
  const img = p.photo || (p.images || [])[0];
  const av = availInfo(p);
  const link = datedUrl(p);
  const kbs = [];
  kbs.push(`<span class="kb hero">${ICON.bed} ${p.bedrooms} bedrooms</span>`);
  /* Three kings is the target, so highlight it only when the house hits it.
     Above three the count is reported plainly — extra masters are not a win,
     and colouring them like one is how the last version misled us. */
  if (bi.king >= KINGS_WANTED) kbs.push(`<span class="kb king">👑 ${bi.king} king${bi.king > 1 ? 's' : ''}${bi.king > KINGS_WANTED ? ' <span style="opacity:.6;font-weight:600">· 3 is all we need</span>' : ''}</span>`);
  else if (bi.king > 0) kbs.push(`<span class="kb">👑 ${bi.king} king${bi.king > 1 ? 's' : ''} <span style="opacity:.6;font-weight:600">· short of 3</span></span>`);
  else if (!bi.known) kbs.push(`<span class="kb muted">👑 kings unconfirmed</span>`);
  else kbs.push(`<span class="kb muted">👑 no kings listed</span>`);
  if (p.bathrooms) kbs.push(`<span class="kb">${ICON.bath} ${p.bathrooms} bath</span>`);
  if (p.sleeps) kbs.push(`<span class="kb${p.sleeps < GROUP ? ' under' : p._oversized ? ' over' : ''}">${ICON.people} sleeps ${p.sleeps}${p.sleeps < GROUP ? ' — too few for nine' : p._oversized ? ' — bigger than we need' : ''}</span>`);
  if (p.compound) kbs.push(`<span class="kb">🏘 books as ${p.compound_note ? 'one' : 'a compound'}</span>`);

  return `
  <article class="card" id="card-${esc(p.id)}" data-id="${esc(p.id)}" data-tier="${p._tier}">
    <div class="card-photo">
      ${img ? `<img src="${esc(img)}" alt="${esc(p.name)}" loading="lazy" data-photo="${esc(p.id)}" onerror="this.closest('.card-photo').classList.add('failed');this.remove()">`
            : ''}
      <div class="noimg"${img ? ' style="display:none"' : ''}>${ICON.house}<span>no photo saved</span></div>
      <span class="pin-badge" style="background:var(--${p._tier})">${p._idx}</span>
      <span class="tier-badge" style="background:var(--${p._tier})">${TIER_LABEL[p._tier]}</span>
      ${(p.images || []).length > 1 ? `<span class="photo-count" data-photo="${esc(p.id)}">📷 ${p.images.length}</span>` : ''}
    </div>
    <div class="card-body">
      <h3>${esc(p.name)}</h3>
      <div class="where">${ICON.pin}<span class="addr">${esc(p.city || '')}${p.neighborhood ? ` · ${esc(p.neighborhood)}` : ''}
        ${p._dist != null ? `<span class="src">· ${p._dist} mi from TPA</span>` : ''}
        <span class="src">· ${esc(p.source || 'listing')}</span></span></div>
      <div class="keyrow">${kbs.join('')}</div>
      ${bedsLine(p)}
      ${priceBlock(p)}
      ${(p.tags || []).length ? `<div class="tags">${p.tags.slice(0, 6).map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div>` : ''}
      ${p.why ? `<div class="why">${esc(p.why)}</div>` : ''}
      ${p.cons ? `<div class="cons">${esc(p.cons)}</div>` : ''}
      <span class="avail ${av[0]}" title="${esc(p.availability_note || '')}">${av[1]} ${av[2]}</span>
      <div class="card-actions">
        ${link ? `<a class="btn btn-primary" href="${esc(link)}" target="_blank" rel="noopener">${ICON.ext} Open the listing</a>` : ''}
        ${p.phone ? `<a class="btn btn-ghost" href="tel:${esc(String(p.phone).replace(/[^0-9+]/g, ''))}">${ICON.phone} ${esc(p.phone)}</a>` : ''}
        <button class="btn btn-ghost" type="button" data-locate="${esc(p.id)}">${ICON.pin} Show on map</button>
      </div>
    </div>
  </article>`;
}

/* ====================== state, filters, render ========================== */
let ALL = [], BY_ID = {}, shownList = [], selected = null;
const state = { q: '', region: 'all', king: false, pool: false, water: false, strict: true, sleeps: 'fits', sort: 'match' };

function matches(p) {
  if (state.strict && !(p.bedrooms >= 5 && p.bedrooms <= 6)) return false;
  if (state.region !== 'all' && p.region !== state.region) return false;
  if (state.king && !(p._bi.king >= KINGS_WANTED)) return false;
  const am = ((p.amenities || []).join(' ') + ' ' + (p.tags || []).join(' ')).toLowerCase();
  if (state.pool && !/pool/.test(am)) return false;
  if (state.water && !/waterfront|beachfront|gulf front|gulffront|bayfront|riverfront|lakefront|dock|canal|water/.test(am)) return false;
  /* 'fits' drops only houses we KNOW are too small — an unpublished capacity is
     not evidence against a house. 'right' is the deliberate tight band, so it
     does require a stated number. */
  if (state.sleeps === 'fits' && p.sleeps != null && p.sleeps < GROUP) return false;
  if (state.sleeps === 'right' && !(p.sleeps >= GROUP && p.sleeps <= 12)) return false;
  if (state.q) {
    const hay = [p.name, p.city, p.neighborhood, p.source, p.why, p.cons, (p.amenities || []).join(' '), (p.tags || []).join(' ')].join(' ').toLowerCase();
    if (!state.q.toLowerCase().split(/\s+/).every(w => hay.includes(w))) return false;
  }
  return true;
}

const SORTS = {
  match: (a, b) => b._score - a._score,
  // toward three kings, not away from it — a seven-king house is not "better"
  kings: (a, b) => Math.abs((a._bi.king ?? 99) - KINGS_WANTED) - Math.abs((b._bi.king ?? 99) - KINGS_WANTED) || b._score - a._score,
  near: (a, b) => (a._dist ?? 9e9) - (b._dist ?? 9e9) || b._score - a._score,
  price: (a, b) => {
    const av = a.nightly_est ?? a.total_est / 8 ?? null, bv = b.nightly_est ?? b.total_est / 8 ?? null;
    if (av == null && bv == null) return b._score - a._score;
    if (av == null) return 1; if (bv == null) return -1;
    return av - bv;
  },
  small: (a, b) => (a.sleeps || 99) - (b.sleeps || 99) || b._score - a._score
};

function apply(refit) {
  shownList = ALL.filter(matches).sort(SORTS[state.sort] || SORTS.match);
  shownList.forEach((p, i) => { p._idx = i + 1; });
  ALL.filter(p => !shownList.includes(p)).forEach(p => { p._idx = null; });

  $('#list').innerHTML = shownList.length
    ? shownList.map(card).join('')
    : `<div class="empty">Nothing matches those filters. Try turning off “5–6 bedrooms only” — Cedar Key in particular tops out at four bedrooms, and a good four-bedroom there would mean two of the three kids sharing.</div>`;
  $('#count').textContent = shownList.length;
  const hidden = ALL.length - shownList.length;
  $('#hiddenNote').textContent = hidden ? ` · ${hidden} hidden by filters` : '';

  renderPins(shownList, ALL);
  if (mapReady) { applyView(); if (refit !== false) fitToPins(shownList); }
  if (selected && !shownList.some(p => p.id === selected)) selected = null;
  paintSelection();
}

function stats() {
  $('#s-total').textContent = ALL.length;
  $('#s-exact').textContent = ALL.filter(p => p._tier === 'exact').length;
  $('#s-strong').textContent = ALL.filter(p => p._tier === 'strong').length;
  // right-sized: in the bedroom band AND built for roughly this group, not double it
  $('#s-king').textContent = ALL.filter(p =>
    p.bedrooms >= 5 && p.bedrooms <= 6 && p.sleeps >= GROUP && p.sleeps <= 12).length;
  $('#s-regions').textContent = new Set(ALL.map(p => p.region)).size;
}

/* ---- selection linking card <-> pin ------------------------------------ */
function paintSelection() {
  $$('.card').forEach(c => c.classList.toggle('sel', c.dataset.id === selected));
  $$('#map .pin').forEach(p => p.classList.toggle('sel', p.dataset.id === selected));
}
/* Pins for filtered-out houses stay on the map, dimmed, so you can still see
   what you have ruled out — but clicking one used to select a card that wasn't
   rendered, which read as the map being broken. Say what happened instead. */
let hintTimer = null;
function flashHint(msg) {
  const el = $('#mapHint'); if (!el) return;
  if (!el.dataset.base) el.dataset.base = el.textContent;
  el.textContent = msg;
  el.style.color = 'var(--warn)';
  clearTimeout(hintTimer);
  hintTimer = setTimeout(() => { el.textContent = el.dataset.base; el.style.color = ''; }, 4000);
}

function selectCard(id, fromMap) {
  selected = id;
  paintSelection();
  const el = $('#card-' + CSS.escape(id));
  if (!el) {
    const p = BY_ID[id];
    flashHint(p ? `${p.name} is hidden by your filters — clear them to see it.` : 'That one is hidden by your filters.');
    return;
  }
  if (fromMap) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  if (!fromMap) {
    const p = BY_ID[id];
    if (p && mapReady && typeof p.lat === 'number') {
      const zw = Math.min(view.w, MAP.FRAME.w * 0.34), zh = zw * (view.h / view.w);
      view = clampView({ x: MAP.px(p.lon) - zw / 2, y: MAP.py(p.lat) - zh / 2, w: zw, h: zh });
      applyView();
      $('#mapwrap').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
}

/* ---- lightbox ---------------------------------------------------------- */
let lbShots = [], lbAt = 0, lbLocal = null;
function openLightbox(id, at) {
  const p = BY_ID[id]; if (!p) return;
  // full-resolution originals when we have them, the local copy otherwise
  lbShots = (p.images || []).length ? p.images.slice() : (p.photo ? [p.photo] : []);
  if (!lbShots.length) return;
  lbLocal = p.photo || null;
  lbAt = at || 0;
  $('#lbCap').textContent = p.name;
  $('#lbImg').src = lbShots[lbAt];
  $('#lb').classList.add('on');
  $('#lb').setAttribute('aria-hidden', 'false');
  const many = lbShots.length > 1;
  $('#lbPrev').style.display = $('#lbNext').style.display = many ? '' : 'none';
}
function stepLightbox(n) {
  if (!lbShots.length) return;
  lbAt = (lbAt + n + lbShots.length) % lbShots.length;
  $('#lbImg').src = lbShots[lbAt];
}
/* If the host's CDN refuses the hotlink, drop back to the local copy rather
   than leaving a broken frame on screen. */
window.__lbFallback = el => {
  if (lbLocal && el.getAttribute('src') !== lbLocal) el.src = lbLocal;
};

function closeLightbox() { $('#lb').classList.remove('on'); $('#lb').setAttribute('aria-hidden', 'true'); $('#lbImg').src = ''; }

/* ---- wiring ------------------------------------------------------------ */
function buildRegionSeg() {
  const counts = {};
  ALL.forEach(p => { counts[p.region] = (counts[p.region] || 0) + 1; });
  const btns = [`<button data-region-btn="all" class="on">All areas <span style="opacity:.7">${ALL.length}</span></button>`];
  for (const r of D.regions || []) {
    if (!counts[r.id]) continue;
    btns.push(`<button data-region-btn="${esc(r.id)}">${esc(r.short || r.label)} <span style="opacity:.7">${counts[r.id]}</span></button>`);
  }
  $('#regionSeg').innerHTML = btns.join('');
  $$('#regionSeg button').forEach(b => b.onclick = () => {
    state.region = b.dataset.regionBtn;
    $$('#regionSeg button').forEach(x => x.classList.toggle('on', x === b));
    apply();
  });
}

function wire() {
  $('#themeToggle').onclick = () => {
    const cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', cur);
    try { localStorage.setItem('stay.theme', cur); } catch (e) {}
    $('#themeToggle').textContent = cur === 'dark' ? '☀️' : '🌙';
  };
  $('#themeToggle').textContent = document.documentElement.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';

  $('#q').oninput = e => { state.q = e.target.value.trim(); apply(false); };
  $('#fKing').onchange = e => { state.king = e.target.checked; apply(); };
  $('#fPool').onchange = e => { state.pool = e.target.checked; apply(); };
  $('#fWater').onchange = e => { state.water = e.target.checked; apply(); };
  $('#fStrict').onchange = e => { state.strict = e.target.checked; apply(); };
  $$('[data-sort-btn]').forEach(b => b.onclick = () => {
    state.sort = b.dataset.sortBtn;
    $$('[data-sort-btn]').forEach(x => x.classList.toggle('on', x === b));
    apply(false);
  });
  $$('[data-sleeps-btn]').forEach(b => b.onclick = () => {
    state.sleeps = b.dataset.sleepsBtn;
    $$('[data-sleeps-btn]').forEach(x => x.classList.toggle('on', x === b));
    apply();
  });
  $('#mapToggle').onclick = () => {
    const w = $('#mapwrap'); w.classList.toggle('collapsed');
    $('#mapToggle').textContent = w.classList.contains('collapsed') ? 'Show map' : 'Hide map';
    if (!w.classList.contains('collapsed')) fitToPins(shownList);
  };

  $('#list').addEventListener('click', e => {
    const loc = e.target.closest('[data-locate]');
    if (loc) { selectCard(loc.dataset.locate, false); return; }
    const ph = e.target.closest('[data-photo]');
    if (ph) { openLightbox(ph.dataset.photo, 0); return; }
    const c = e.target.closest('.card');
    if (c && !e.target.closest('a')) selectCard(c.dataset.id, false);
  });

  $('#lbX').onclick = closeLightbox;
  $('#lbPrev').onclick = e => { e.stopPropagation(); stepLightbox(-1); };
  $('#lbNext').onclick = e => { e.stopPropagation(); stepLightbox(1); };
  $('#lb').onclick = e => { if (e.target.id === 'lb') closeLightbox(); };
  document.addEventListener('keydown', e => {
    if (!$('#lb').classList.contains('on')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') stepLightbox(-1);
    if (e.key === 'ArrowRight') stepLightbox(1);
  });
  let rz;
  addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(() => mapReady && fitToPins(shownList), 200); });
}

function boot() {
  ALL = (D.properties || []).map(evaluate);
  ALL.forEach(p => { BY_ID[p.id] = p; });
  $('#genDate').textContent = D.generated || '—';
  if (D.disclaimer) $('#disclaimer').textContent = D.disclaimer;
  if (D.spec_chips) $('#specStrip').innerHTML = D.spec_chips.map(c =>
    `<span class="spec-chip">${c.dot ? `<span class="dot" style="background:${c.dot}"></span> ` : ''}${c.text}</span>`).join('');
  $('#legend').innerHTML = ['exact', 'strong', 'backup', 'stretch'].map(k =>
    `<span class="item"><span class="sw" style="background:var(--${k})"></span> ${esc((D.tiers || {})[k] || TIER_LABEL[k])}</span>`).join('');
  buildRegionSeg();
  stats();
  wire();
  initMap(ALL);
  apply();
}
document.addEventListener('DOMContentLoaded', boot);
