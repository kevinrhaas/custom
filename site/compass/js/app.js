/* Compass — passcode gate + private research console on the Polecat Shell.
   The opportunity data ships AES-GCM-encrypted in js/payload.js (built by
   tools/encrypt.mjs); decryption is local (WebCrypto). After unlock the app
   boots the vendored shell frame: rail + topbar + three sections —
   Home (overview + sync), Opportunities (the console), Lists (saved lists,
   manual reorder, pairwise ranking, CSV export). Favorites and lists are
   local-first and sync to Supabase when connected. */

import { configure as configureTheme, applyTheme, toggleMode } from '../vendor/polecat-shell/theme.js';
import { initShell, appSwitcher } from '../vendor/polecat-shell/shell.js';
import { icon } from '../vendor/polecat-shell/icons.js';
import { el, escapeHtml as esc, toast, confirmDialog, promptDialog, download, uuid, relTime } from '../vendor/polecat-shell/ui.js';
import { FLEET } from '../vendor/polecat-shell/catalog.js';

configureTheme({
  storageKey: 'compass.theme', defaultTheme: 'ink:dark',
  palettes: [{ key: 'ink', label: 'Ink & Chalk', hint: 'Night-class navy, teal & amber' }],
});
applyTheme();

/* ================= crypto + gate ================= */
function b64ToBytes(b64) {
  const bin = atob(b64), out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
/* Forgiving normalization: only letters and digits count. */
const normalizePass = (p) => (p || '').toLowerCase().replace(/[^a-z0-9]/g, '');

async function decryptPayload(pass) {
  const P = window.COMPASS_PAYLOAD;
  if (!P || !P.ct) throw new Error('no payload');
  const enc = new TextEncoder();
  const km = await crypto.subtle.importKey('raw', enc.encode(normalizePass(pass)), { name: 'PBKDF2' }, false, ['deriveKey']);
  const key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt: b64ToBytes(P.salt), iterations: 310000, hash: 'SHA-256' },
    km, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
  const plain = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: b64ToBytes(P.iv) }, key, b64ToBytes(P.ct));
  return JSON.parse(new TextDecoder().decode(plain));
}

let DATA = null;
const byUrl = new Map();

(function gate() {
  const form = document.getElementById('gateForm');
  const card = document.getElementById('gateCard');
  const input = document.getElementById('passInput');
  const btn = document.getElementById('unlockBtn');

  async function attempt(pass, silent) {
    btn.disabled = true;
    try {
      DATA = await decryptPayload(pass);
      try { sessionStorage.setItem('compass.k', pass); } catch (e) {}
      boot();
    } catch (e) {
      DATA = null;
      if (!silent) {
        card.classList.remove('wrong');
        void card.offsetWidth;
        card.classList.add('wrong');
        input.select();
      }
    }
    btn.disabled = false;
  }
  form.addEventListener('submit', (ev) => { ev.preventDefault(); attempt(input.value, false); });
  let saved = null;
  try { saved = sessionStorage.getItem('compass.k'); } catch (e) {}
  if (saved) attempt(saved, true);
})();

/* ================= local stores ================= */
let FAVS = new Set();
try { FAVS = new Set(JSON.parse(localStorage.getItem('compass.favs.v1') || '[]')); } catch (e) {}
const saveFavs = () => { try { localStorage.setItem('compass.favs.v1', JSON.stringify([...FAVS])); } catch (e) {} };

let LISTS = [];
try { LISTS = JSON.parse(localStorage.getItem('compass.lists.v1') || '[]'); } catch (e) {}
let TOMB = {};
try { TOMB = JSON.parse(localStorage.getItem('compass.lists.tomb') || '{}'); } catch (e) {}
const saveLists = () => {
  try {
    localStorage.setItem('compass.lists.v1', JSON.stringify(LISTS));
    localStorage.setItem('compass.lists.tomb', JSON.stringify(TOMB));
  } catch (e) {}
};
const getList = (id) => LISTS.find((l) => l.id === id);

/* ================= supabase sync ================= */
const SB_SQL = [
  'CREATE TABLE IF NOT EXISTS "compass_favorites" (',
  '  item_url   TEXT PRIMARY KEY,',
  '  starred_at TIMESTAMPTZ NOT NULL DEFAULT now()',
  ');',
  'CREATE TABLE IF NOT EXISTS "compass_lists" (',
  '  id TEXT PRIMARY KEY,',
  '  name TEXT,',
  '  "updatedAt" BIGINT,',
  '  data TEXT',
  ');',
  'GRANT SELECT, INSERT, UPDATE, DELETE ON "compass_favorites", "compass_lists" TO anon, authenticated, service_role;',
  'ALTER TABLE "compass_favorites" ENABLE ROW LEVEL SECURITY;',
  'ALTER TABLE "compass_lists" ENABLE ROW LEVEL SECURITY;',
  'DROP POLICY IF EXISTS compass_anon_all ON "compass_favorites";',
  'CREATE POLICY compass_anon_all ON "compass_favorites" FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);',
  'DROP POLICY IF EXISTS compass_anon_all_lists ON "compass_lists";',
  'CREATE POLICY compass_anon_all_lists ON "compass_lists" FOR ALL TO anon, authenticated USING (true) WITH CHECK (true);',
  "NOTIFY pgrst, 'reload schema';",
].join('\n');

function sbCfg() {
  const cfg = (DATA && DATA.supabase) || {};
  let localKey = '';
  try { localKey = localStorage.getItem('compass.sb.key') || ''; } catch (e) {}
  return {
    url: (cfg.url || '').replace(/\/+$/, ''),
    favTable: cfg.table || 'compass_favorites',
    listTable: 'compass_lists',
    key: localKey || cfg.anonKey || '',
  };
}
const sbHeaders = (key, extra) => ({ apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', ...extra });

let sbConnected = false;
let syncState = { s: 'off', msg: '' };
function setSync(s, msg) {
  syncState = { s, msg };
  document.querySelectorAll('.sync-dot').forEach((d) => { d.className = 'sync-dot ' + s; });
  const st = document.getElementById('syncStatus');
  if (st) st.textContent = msg;
  const sq = document.getElementById('syncSql');
  if (sq) sq.hidden = s !== 'warn';
  const kpi = document.getElementById('kpiSync');
  if (kpi) kpi.textContent = s === 'ok' ? 'On' : s === 'warn' ? 'Setup' : s === 'err' ? 'Error' : 'Off';
}
async function sbGet(cfg, table, sel) {
  const res = await fetch(`${cfg.url}/rest/v1/${table}?select=${sel}`, { headers: sbHeaders(cfg.key) });
  if (res.status === 404 || res.status === 400) return { missing: true };
  if (res.status === 401 || res.status === 403) throw new Error('Supabase rejected the key (401/403).');
  if (!res.ok) throw new Error('HTTP ' + res.status);
  return { rows: await res.json() };
}
const sbUpsert = (cfg, table, rows) =>
  fetch(`${cfg.url}/rest/v1/${table}`, {
    method: 'POST', headers: sbHeaders(cfg.key, { Prefer: 'resolution=merge-duplicates,return=minimal' }),
    body: JSON.stringify(rows),
  }).then((r) => { if (!r.ok) throw new Error('upsert HTTP ' + r.status); });
const sbDelete = (cfg, table, q) =>
  fetch(`${cfg.url}/rest/v1/${table}?${q}`, { method: 'DELETE', headers: sbHeaders(cfg.key) })
    .then((r) => { if (!r.ok) throw new Error('delete HTTP ' + r.status); });

const syncErr = (e) => setSync('err', 'Sync error: ' + e.message + ' Everything still works on this device.');

async function initSync() {
  const cfg = sbCfg();
  sbConnected = false;
  if (!cfg.url) { setSync('off', 'Sync is not configured in this build.'); return; }
  if (!cfg.key) { setSync('off', 'Not connected — favorites and lists live on this device only. Paste your Supabase key below to sync.'); return; }
  setSync('off', 'Connecting…');
  try {
    const favs = await sbGet(cfg, cfg.favTable, 'item_url');
    if (favs.missing) {
      const sq = document.getElementById('sqlText');
      if (sq) sq.textContent = SB_SQL;
      setSync('warn', 'Connected, but the tables do not exist yet — one-time setup below.');
      return;
    }
    // favorites: union merge
    const remoteFavs = new Set(favs.rows.map((r) => r.item_url));
    const pushFavs = [...FAVS].filter((u) => !remoteFavs.has(u));
    if (pushFavs.length) await sbUpsert(cfg, cfg.favTable, pushFavs.map((u) => ({ item_url: u })));
    remoteFavs.forEach((u) => FAVS.add(u));
    saveFavs();

    // lists: last-writer-wins by updatedAt, with local tombstones for deletes
    const lr = await sbGet(cfg, cfg.listTable, 'id,name,updatedAt,data');
    if (!lr.missing) {
      const remote = lr.rows || [];
      const localById = new Map(LISTS.map((l) => [l.id, l]));
      const pushUp = [];
      for (const r of remote) {
        const t = TOMB[r.id];
        if (t && t >= (r.updatedAt || 0)) { sbDelete(cfg, cfg.listTable, 'id=eq.' + encodeURIComponent(r.id)).catch(() => {}); continue; }
        let items = [];
        try { items = JSON.parse(r.data || '[]'); } catch (e) {}
        const loc = localById.get(r.id);
        if (!loc) LISTS.push({ id: r.id, name: r.name || 'List', items, updatedAt: r.updatedAt || 0 });
        else if ((r.updatedAt || 0) > (loc.updatedAt || 0)) { loc.name = r.name || loc.name; loc.items = items; loc.updatedAt = r.updatedAt; }
        else if ((loc.updatedAt || 0) > (r.updatedAt || 0)) pushUp.push(loc);
      }
      const remoteIds = new Set(remote.map((r) => r.id));
      LISTS.forEach((l) => { if (!remoteIds.has(l.id)) pushUp.push(l); });
      if (pushUp.length) await sbUpsert(cfg, cfg.listTable, pushUp.map(listRow));
      saveLists();
    }
    sbConnected = true;
    setSync('ok', `Synced — ${FAVS.size} favorite${FAVS.size === 1 ? '' : 's'} and ${LISTS.length} list${LISTS.length === 1 ? '' : 's'} shared across your devices.`);
    rerender();
  } catch (e) { syncErr(e); }
}
const listRow = (l) => ({ id: l.id, name: l.name, updatedAt: l.updatedAt || Date.now(), data: JSON.stringify(l.items) });
function pushList(l) { if (sbConnected) sbUpsert(sbCfg(), sbCfg().listTable, [listRow(l)]).catch(syncErr); }
function pushListDelete(id) { if (sbConnected) sbDelete(sbCfg(), sbCfg().listTable, 'id=eq.' + encodeURIComponent(id)).catch(syncErr); }

function toggleFav(url) {
  const starred = !FAVS.has(url);
  if (starred) FAVS.add(url); else FAVS.delete(url);
  saveFavs();
  rerender();
  if (sbConnected) {
    const cfg = sbCfg();
    (starred ? sbUpsert(cfg, cfg.favTable, [{ item_url: url }])
             : sbDelete(cfg, cfg.favTable, 'item_url=eq.' + encodeURIComponent(url))).catch(syncErr);
  }
}

/* ================= shell + views ================= */
const CATS = ['Higher Ed', 'Workforce & Nonprofit', 'Youth & Teens', 'Mission & EdTech', 'Corporate Tech'];
const CAT_COLORS = {
  'Higher Ed': 'var(--c-highered)', 'Workforce & Nonprofit': 'var(--c-workforce)',
  'Youth & Teens': 'var(--c-youth)', 'Mission & EdTech': 'var(--c-mission)', 'Corporate Tech': 'var(--c-corp)',
};
const TYPES = [
  { key: 'All', label: 'All types', match: () => true },
  { key: 'full', label: 'Full-time', match: (t) => t === 'full-time' },
  { key: 'part', label: 'Part-time / adjunct', match: (t) => t === 'part-time' || t === 'adjunct' },
  { key: 'contract', label: 'Contract / fractional', match: (t) => t === 'contract' || t === 'fractional' },
  { key: 'vol', label: 'Volunteer / board', match: (t) => t === 'volunteer' || t === 'board' },
];
const MODES = ['All', 'remote', 'hybrid', 'onsite', 'flexible'];
const state = { cat: 'All', type: 'All', mode: 'All', q: '', sort: 'overall', favOnly: false, listId: null, pw: null };
const SECTIONS = [
  { key: 'home', label: 'Home', icon: 'home' },
  { key: 'opps', label: 'Opportunities', icon: 'compass' },
  { key: 'lists', label: 'Lists', icon: 'list' },
];
const TITLE = { home: 'Compass', opps: 'Opportunities', lists: 'Lists' };
let shell, main, titleEl, current = 'home';
const isLight = () => document.documentElement.getAttribute('data-theme') === 'light';

function boot() {
  DATA.items.forEach((it) => byUrl.set(it.url, it));
  document.getElementById('gate').remove();

  titleEl = el('h1', { text: 'Compass', style: 'font-size:16px;font-weight:700;margin:0' });
  const syncBtn = el('button', { class: 'btn icon ghost', title: 'Sync status', 'aria-label': 'Sync status', onclick: () => { go('home'); setTimeout(() => document.getElementById('syncCard')?.scrollIntoView({ behavior: 'smooth' }), 60); } });
  syncBtn.appendChild(el('span', { class: 'sync-dot off' }));
  const themeBtn = el('button', { class: 'btn icon ghost', title: 'Toggle light / dark', 'aria-label': 'Toggle theme', html: icon(isLight() ? 'moon' : 'sun'), onclick: () => { toggleMode(); themeBtn.innerHTML = icon(isLight() ? 'moon' : 'sun'); } });
  const lockBtn = el('button', { class: 'btn icon ghost', title: 'Lock', 'aria-label': 'Lock', html: icon('key'), onclick: () => { try { sessionStorage.removeItem('compass.k'); } catch (e) {} location.reload(); } });

  shell = initShell({
    app: { id: 'compass', name: 'Compass', icon: icon('compass'), wordmark: '🧭' },
    sections: SECTIONS.map((s) => ({ ...s, icon: icon(s.icon) })),
    onNav: (k) => go(k),
    rail: { storageKey: 'compass.rail' },
    topbar: { left: [titleEl], right: [syncBtn, appSwitcher(FLEET, {}), themeBtn, lockBtn] },
  });
  main = shell.els.main;

  for (const s of SECTIONS) {
    main.appendChild(el('section', { 'data-view': s.key, hidden: true }, [el('div', { class: 'cx-wrap', id: 'view-' + s.key })]));
  }
  buildOppsStatic();
  routeFromHash();
  window.addEventListener('hashchange', routeFromHash);
  initSync();
}

function routeFromHash() {
  const k = location.hash.replace(/^#\/?/, '').split('/')[0];
  go(SECTIONS.some((s) => s.key === k) ? k : 'home', true);
}
function go(key, fromHash) {
  current = key;
  main.querySelectorAll('section[data-view]').forEach((s) => { s.hidden = s.dataset.view !== key; });
  titleEl.textContent = TITLE[key];
  shell.setActive(key);
  if (!fromHash) location.hash = key;
  rerender();
  main.scrollTop = 0;
}
function rerender() {
  if (!shell) return;
  if (current === 'home') renderHome();
  if (current === 'opps') renderOppsList();
  if (current === 'lists') renderLists();
  shell.setBadge('lists', LISTS.length || 0);
}

/* ================= shared card pieces ================= */
const dots = (n, cls) => '<span class="dots' + (cls ? ' ' + cls : '') + '">' + Array.from({ length: 5 }, (_, i) => `<i${i < n ? ' class="on"' : ''}></i>`).join('') + '</span>';
function modeBadge(it) {
  let label = it.workMode.charAt(0).toUpperCase() + it.workMode.slice(1);
  if (it.modeNotes) label += ' · ' + it.modeNotes;
  let cls = 'badge';
  if (it.workMode === 'remote') cls += ' mode-remote';
  if (/5 days|five days|fully on.?site/i.test(it.modeNotes || '')) cls += ' mode-onsite5';
  return `<span class="${cls}">${esc(label)}</span>`;
}
function card(it) {
  const r = it.ratings, faved = FAVS.has(it.url);
  let h = `<article class="card" data-cat="${esc(it.category)}">`;
  h += '<div class="card-top"><div>';
  h += `<div class="card-org">${esc(it.org)}</div>`;
  h += `<div class="card-title"><a href="${esc(it.url)}" target="_blank" rel="noopener noreferrer">${esc(it.title)}</a></div>`;
  h += '</div><div class="card-side">';
  h += `<button class="fav-btn${faved ? ' on' : ''}" data-fav="${esc(it.url)}" type="button" aria-pressed="${faved}" title="${faved ? 'Remove favorite' : 'Add favorite'}">★</button>`;
  h += `<div class="overall-chip"><span class="num">${r.overall.toFixed(1)}</span><span class="lbl">Overall</span></div>`;
  h += '</div></div>';
  h += '<div class="badges">';
  h += `<span class="badge"><span class="dot" style="background:${CAT_COLORS[it.category] || 'var(--border-2)'}"></span>${esc(it.category)}</span>`;
  h += `<span class="badge">${esc(it.type.charAt(0).toUpperCase() + it.type.slice(1))}</span>`;
  h += modeBadge(it);
  if (it.area) h += `<span class="badge">📍 ${esc(it.area)}</span>`;
  h += '</div>';
  if (it.orgBlurb) h += `<p class="card-blurb"><b>Who they are:</b> ${esc(it.orgBlurb)}</p>`;
  h += `<p class="card-desc">${esc(it.desc)}</p>`;
  if (it.whyFit) h += `<p class="card-why"><b>Why you:</b> ${esc(it.whyFit)}</p>`;
  h += `<div class="fact-row"><span class="k">Comp</span><span class="v">${esc(it.compText || 'Not listed')}</span></div>`;
  if (it.benefitsText && it.benefitsText !== 'Not listed') h += `<div class="fact-row"><span class="k">Benefits</span><span class="v">${esc(it.benefitsText)}</span></div>`;
  if (it.location) h += `<div class="fact-row"><span class="k">Where</span><span class="v">${esc(it.location)}</span></div>`;
  if (it.contactNote) h += `<div class="fact-row"><span class="k">Contact</span><span class="v">${esc(it.contactNote)}</span></div>`;
  h += '<div class="ratings">';
  h += `<span class="rating"><span class="rl">Mission</span>${dots(r.mission)}</span>`;
  h += `<span class="rating"><span class="rl">Fit</span>${dots(r.fit)}</span>`;
  h += `<span class="rating dim-comp"><span class="rl">Comp</span>${dots(r.comp)}</span>`;
  h += `<span class="rating"><span class="rl">Flex</span>${dots(r.flex)}</span>`;
  h += '</div>';
  h += '<div class="card-foot">';
  h += `<a class="apply-btn" href="${esc(it.url)}" target="_blank" rel="noopener noreferrer">View posting ↗</a>`;
  if (it.verified) h += `<span class="verified-note">✓ ${esc(it.verified)}</span>`;
  h += '</div></article>';
  return h;
}

/* ================= HOME ================= */
function renderHome() {
  const host = document.getElementById('view-home');
  const top5 = [...DATA.items].sort((a, b) => b.ratings.overall - a.ratings.overall).slice(0, 5);
  let h = '';
  h += '<header class="cx-hero">';
  h += '<div class="kicker">Opportunity research</div>';
  h += '<h1>Where to point <span class="grad">what you know.</span></h1>';
  h += `<p class="sub">${esc(DATA.focus || '')}</p>`;
  h += `<p class="gen">Researched & link-verified ${esc(DATA.generated || '')} · every card links to the live posting</p>`;
  h += '</header>';

  h += '<div class="kpis">';
  h += `<button class="kpi" data-go="opps"><span class="n">${DATA.items.length}</span><span class="l">Opportunities</span></button>`;
  h += `<button class="kpi" data-go="favs"><span class="n">${FAVS.size}</span><span class="l">Favorites ★</span></button>`;
  h += `<button class="kpi" data-go="lists"><span class="n">${LISTS.length}</span><span class="l">Saved lists</span></button>`;
  h += `<button class="kpi" data-go="sync"><span class="n" id="kpiSync">—</span><span class="l">Sync</span></button>`;
  h += '</div>';

  h += '<div class="callout"><b>⏰ Time-sensitive:</b> College of DuPage — Director, AI Strategy & Technology Partnerships closes <b>Aug 9, 2026</b>. i.c.stars\' fall facilitator cycle: email dfoye@icstars.org directly.</div>';

  h += '<h2 class="cx-h2">The landscape</h2><div class="stats">';
  for (const c of CATS) {
    const n = DATA.items.filter((it) => it.category === c).length;
    h += `<button class="stat" data-cat-go="${esc(c)}" data-cat="${esc(c)}"><span class="n">${n}</span><span class="l">${esc(c)}</span></button>`;
  }
  h += '</div>';

  h += '<h2 class="cx-h2">Top picks</h2><div class="top-picks">';
  top5.forEach((it, i) => {
    const faved = FAVS.has(it.url);
    h += `<div class="pick"><span class="rank">${i + 1}</span><span class="pick-dot" style="background:${CAT_COLORS[it.category]}"></span>`;
    h += `<span class="pick-main"><b>${esc(it.org)}</b> — ${esc(it.title)}</span>`;
    h += `<span class="pick-overall">${it.ratings.overall.toFixed(1)}</span>`;
    h += `<button class="fav-btn sm${faved ? ' on' : ''}" data-fav="${esc(it.url)}" aria-pressed="${faved}">★</button>`;
    h += `<a class="pick-open" href="${esc(it.url)}" target="_blank" rel="noopener noreferrer" title="Open posting">${icon('external', 15)}</a></div>`;
  });
  h += '</div>';

  h += '<h2 class="cx-h2">Cross-device sync</h2>';
  h += '<div class="sync-panel" id="syncCard">';
  h += `<div class="sync-status" id="syncStatus">${esc(syncState.msg)}</div>`;
  h += '<div class="sync-row">';
  h += '<input type="password" id="sbKey" autocomplete="off" placeholder="Supabase anon / publishable key — paste once">';
  h += '<button id="sbSave" type="button">Connect</button><button id="sbForget" type="button" class="ghost">Disconnect</button>';
  h += '</div>';
  h += `<div class="sync-note">Favorites and lists always work on this device. Connecting syncs them through your Supabase project (${esc(sbCfg().url || 'not configured')}). Keys pasted here stay in this browser only.</div>`;
  h += `<div class="sync-sql" id="syncSql" ${syncState.s === 'warn' ? '' : 'hidden'}><div class="sync-note"><b>One-time setup:</b> paste this into Supabase → SQL Editor → Run, then hit Connect again:</div><pre id="sqlText">${esc(SB_SQL)}</pre><button id="sqlCopy" type="button" class="ghost">Copy SQL</button></div>`;
  h += '</div>';

  host.innerHTML = h;
  setSync(syncState.s, syncState.msg);

  host.querySelectorAll('[data-go]').forEach((b) => b.addEventListener('click', () => {
    const t = b.getAttribute('data-go');
    if (t === 'favs') { state.favOnly = true; go('opps'); }
    else if (t === 'sync') document.getElementById('syncCard').scrollIntoView({ behavior: 'smooth' });
    else go(t);
  }));
  host.querySelectorAll('[data-cat-go]').forEach((b) => b.addEventListener('click', () => { state.cat = b.getAttribute('data-cat-go'); go('opps'); }));
  host.addEventListener('click', (ev) => {
    const f = ev.target.closest('.fav-btn'); if (f) toggleFav(f.getAttribute('data-fav'));
  });
  document.getElementById('sbSave').addEventListener('click', () => {
    const v = document.getElementById('sbKey').value.trim();
    if (v) { try { localStorage.setItem('compass.sb.key', v); } catch (e) {} }
    initSync();
  });
  document.getElementById('sbForget').addEventListener('click', () => {
    try { localStorage.removeItem('compass.sb.key'); } catch (e) {}
    sbConnected = false; initSync();
  });
  document.getElementById('sqlCopy').addEventListener('click', () => { navigator.clipboard?.writeText(SB_SQL); toast('SQL copied'); });
}

/* ================= OPPORTUNITIES ================= */
function segHtml(items, attr, currentVal, labelFn) {
  let h = '<div class="seg">';
  for (const it of items) {
    const key = typeof it === 'string' ? it : it.key;
    const label = labelFn ? labelFn(it) : (typeof it === 'string' ? it : it.label);
    h += `<button data-${attr}="${esc(key)}"${currentVal === key ? ' class="on"' : ''}>${esc(label)}</button>`;
  }
  return h + '</div>';
}
function buildOppsStatic() {
  const host = document.getElementById('view-opps');
  let h = '';
  h += '<div class="legend"><b>Ratings</b> — 1–5 on <b>Mission</b> (giving back), <b>Fit</b> (skills + odds), <b>Comp</b> (as listed), <b>Flex</b> (location/schedule vs Loop-North-NW + ≤2–3 days) · <b>Overall</b> weighted toward mission.</div>';
  h += '<div class="controls" id="controlsCat"></div>';
  h += '<div class="controls">';
  h += '<input type="search" id="q" placeholder="Search org, title, keywords…" aria-label="Search">';
  h += '<button class="fav-toggle" id="favToggle" type="button" aria-pressed="false">☆ Favorites</button>';
  h += '<span class="sort-label">Sort</span><select id="sortSel" aria-label="Sort by">';
  h += '<option value="overall">Overall (best first)</option><option value="mission">Mission</option><option value="fit">Fit</option><option value="comp">Comp</option><option value="flex">Flexibility</option><option value="org">Organization A–Z</option></select>';
  h += '</div>';
  h += '<div class="count-note" id="countNote"></div><div class="list" id="oppList"></div>';
  host.innerHTML = h;

  document.getElementById('q').addEventListener('input', (ev) => { state.q = ev.target.value.toLowerCase(); renderOppsList(); });
  document.getElementById('sortSel').addEventListener('change', (ev) => { state.sort = ev.target.value; renderOppsList(); });
  document.getElementById('favToggle').addEventListener('click', () => { state.favOnly = !state.favOnly; renderOppsList(); });
  document.getElementById('controlsCat').addEventListener('click', (ev) => {
    const b = ev.target.closest('button'); if (!b) return;
    if (b.hasAttribute('data-cat')) state.cat = b.getAttribute('data-cat');
    if (b.hasAttribute('data-type')) state.type = b.getAttribute('data-type');
    if (b.hasAttribute('data-mode')) state.mode = b.getAttribute('data-mode');
    renderOppsList();
  });
  document.getElementById('oppList').addEventListener('click', (ev) => {
    const f = ev.target.closest('.fav-btn');
    if (f) { ev.preventDefault(); toggleFav(f.getAttribute('data-fav')); }
  });
}
const typeMatcher = (key) => (TYPES.find((t) => t.key === key) || TYPES[0]).match;
function filtered() {
  const tm = typeMatcher(state.type);
  return DATA.items.filter((it) => {
    if (state.favOnly && !FAVS.has(it.url)) return false;
    if (state.cat !== 'All' && it.category !== state.cat) return false;
    if (!tm(it.type)) return false;
    if (state.mode !== 'All' && it.workMode !== state.mode) return false;
    if (state.q) {
      const hay = [it.org, it.title, it.desc, it.location, it.area, it.category, it.compText, it.whyFit, it.type, it.modeNotes, it.orgBlurb].join(' ').toLowerCase();
      if (!hay.includes(state.q)) return false;
    }
    return true;
  });
}
function sorted(items) {
  const s = state.sort, arr = [...items];
  if (s === 'org') arr.sort((a, b) => a.org.localeCompare(b.org) || b.ratings.overall - a.ratings.overall);
  else arr.sort((a, b) => (b.ratings[s] || 0) - (a.ratings[s] || 0) || b.ratings.overall - a.ratings.overall || (b.ratings.mission || 0) - (a.ratings.mission || 0));
  return arr;
}
function renderOppsList() {
  const catRow = document.getElementById('controlsCat');
  catRow.innerHTML =
    segHtml(['All', ...CATS], 'cat', state.cat) +
    segHtml(TYPES, 'type', state.type) +
    segHtml(MODES, 'mode', state.mode, (m) => (m === 'All' ? 'Any mode' : m.charAt(0).toUpperCase() + m.slice(1)));
  const ft = document.getElementById('favToggle');
  ft.classList.toggle('on', state.favOnly);
  ft.setAttribute('aria-pressed', String(state.favOnly));
  ft.textContent = (state.favOnly ? '★' : '☆') + ' Favorites';

  const items = sorted(filtered());
  document.getElementById('countNote').textContent = `${items.length} of ${DATA.items.length} opportunities shown · ${FAVS.size} ★`;
  document.getElementById('oppList').innerHTML = items.length ? items.map(card).join('')
    : '<div class="empty">Nothing matches those filters — loosen one and try again.</div>';
}

/* ================= LISTS ================= */
function newListFromFavs() {
  if (!FAVS.size) { toast('No favorites yet', { body: 'Star some opportunities first — then save them as a list.', kind: 'warn' }); return; }
  promptDialog({ title: 'New list from favorites', label: 'List name', placeholder: 'e.g. Fall shortlist', multiline: false, okText: 'Create' }).then((name) => {
    if (name == null) return;
    const items = sorted(DATA.items.filter((it) => FAVS.has(it.url))).map((it) => it.url);
    const l = { id: uuid(), name: name.trim() || 'Shortlist ' + new Date().toLocaleDateString(), items, updatedAt: Date.now() };
    LISTS.push(l); saveLists(); pushList(l);
    state.listId = l.id; rerender();
    toast('List created', { body: `${items.length} favorites saved to “${l.name}”.`, kind: 'success' });
  });
}
function touchList(l) { l.updatedAt = Date.now(); saveLists(); pushList(l); }

function renderLists() {
  const host = document.getElementById('view-lists');
  if (state.pw) return renderPairwise(host);
  const l = state.listId && getList(state.listId);
  if (l) return renderListDetail(host, l);

  let h = '<div class="lists-head"><h2 class="cx-h2" style="margin:0">Saved lists</h2>';
  h += `<button class="btn-primary" id="newFromFavs">${icon('plus', 15)} New list from favorites (${FAVS.size} ★)</button></div>`;
  if (!LISTS.length) {
    h += '<div class="empty">No lists yet. Star opportunities in the console, then save your favorites as a list — from there you can rank them manually or run a pairwise “this or that” ranking, and export everything as a CSV.</div>';
  } else {
    h += '<div class="list-grid">';
    for (const li of [...LISTS].sort((a, b) => (b.updatedAt || 0) - (a.updatedAt || 0))) {
      h += `<button class="list-card" data-open="${esc(li.id)}">`;
      h += `<span class="list-name">${icon('list', 16)} ${esc(li.name)}</span>`;
      h += `<span class="list-meta">${li.items.length} item${li.items.length === 1 ? '' : 's'} · updated ${esc(relTime(li.updatedAt || Date.now()))}</span>`;
      h += '</button>';
    }
    h += '</div>';
  }
  host.innerHTML = h;
  document.getElementById('newFromFavs').addEventListener('click', newListFromFavs);
  host.querySelectorAll('[data-open]').forEach((b) => b.addEventListener('click', () => { state.listId = b.getAttribute('data-open'); rerender(); }));
}

function renderListDetail(host, l) {
  const items = l.items.map((u) => byUrl.get(u)).filter(Boolean);
  let h = `<div class="lists-head"><button class="btn-ghost" id="backLists">${icon('chevron', 15)} All lists</button>`;
  h += `<h2 class="cx-h2 list-title" id="renameList" title="Rename" style="margin:0;cursor:pointer">${esc(l.name)} ✎</h2></div>`;
  h += `<div class="count-note">${items.length} item${items.length === 1 ? '' : 's'} · drag or use ↑↓ to rank manually · updated ${esc(relTime(l.updatedAt || Date.now()))}</div>`;
  h += '<div class="list-actions">';
  h += `<button class="btn-primary" id="pwStart" ${items.length < 2 ? 'disabled' : ''}>${icon('sort', 15)} Pairwise rank</button>`;
  h += `<button class="btn-ghost" id="csvExport">${icon('download', 15)} Export CSV</button>`;
  h += `<button class="btn-ghost" id="addFavs">${icon('star', 15)} Add current favorites</button>`;
  h += `<button class="btn-ghost danger" id="delList">${icon('trash', 15)} Delete list</button>`;
  h += '</div>';
  h += '<div class="rank-rows" id="rankRows">';
  items.forEach((it, i) => {
    h += `<div class="rank-row" draggable="true" data-i="${i}">`;
    h += `<span class="drag-grip">${icon('grip', 16)}</span><span class="rank">${i + 1}</span>`;
    h += `<span class="pick-dot" style="background:${CAT_COLORS[it.category]}"></span>`;
    h += `<span class="pick-main"><b>${esc(it.org)}</b> — ${esc(it.title)}<span class="row-sub">${esc(it.compText || '')}</span></span>`;
    h += `<span class="pick-overall">${it.ratings.overall.toFixed(1)}</span>`;
    h += `<span class="row-btns"><button data-up="${i}" title="Move up" ${i === 0 ? 'disabled' : ''}>↑</button>`;
    h += `<button data-down="${i}" title="Move down" ${i === items.length - 1 ? 'disabled' : ''}>↓</button>`;
    h += `<button data-rm="${i}" title="Remove">${icon('close', 14)}</button></span>`;
    h += `<a class="pick-open" href="${esc(it.url)}" target="_blank" rel="noopener noreferrer">${icon('external', 15)}</a>`;
    h += '</div>';
  });
  h += '</div>';
  if (l.items.length !== items.length) h += `<div class="count-note">${l.items.length - items.length} item(s) reference postings no longer in the dataset and are hidden.</div>`;
  host.innerHTML = h;

  document.getElementById('backLists').addEventListener('click', () => { state.listId = null; rerender(); });
  document.getElementById('renameList').addEventListener('click', () => {
    promptDialog({ title: 'Rename list', label: 'List name', multiline: false, okText: 'Rename' }).then((name) => {
      if (name == null || !name.trim()) return;
      l.name = name.trim(); touchList(l); rerender();
    });
  });
  document.getElementById('pwStart').addEventListener('click', () => startPairwise(l));
  document.getElementById('csvExport').addEventListener('click', () => exportCsv(l.name, items));
  document.getElementById('addFavs').addEventListener('click', () => {
    const before = l.items.length;
    FAVS.forEach((u) => { if (!l.items.includes(u) && byUrl.has(u)) l.items.push(u); });
    touchList(l); rerender();
    toast(l.items.length - before + ' added');
  });
  document.getElementById('delList').addEventListener('click', () => {
    confirmDialog({ title: 'Delete this list?', message: `“${l.name}” will be removed everywhere.`, okText: 'Delete', danger: true }).then((ok) => {
      if (!ok) return;
      LISTS = LISTS.filter((x) => x.id !== l.id);
      TOMB[l.id] = Date.now(); saveLists(); pushListDelete(l.id);
      state.listId = null; rerender();
    });
  });

  const move = (i, j) => {
    const [x] = l.items.splice(i, 1);
    l.items.splice(j, 0, x);
    touchList(l); rerender();
  };
  host.querySelectorAll('[data-up]').forEach((b) => b.addEventListener('click', () => { const i = +b.dataset.up; move(i, i - 1); }));
  host.querySelectorAll('[data-down]').forEach((b) => b.addEventListener('click', () => { const i = +b.dataset.down; move(i, i + 1); }));
  host.querySelectorAll('[data-rm]').forEach((b) => b.addEventListener('click', () => { l.items.splice(+b.dataset.rm, 1); touchList(l); rerender(); }));

  let dragFrom = null;
  host.querySelectorAll('.rank-row').forEach((row) => {
    row.addEventListener('dragstart', () => { dragFrom = +row.dataset.i; row.classList.add('dragging'); });
    row.addEventListener('dragend', () => row.classList.remove('dragging'));
    row.addEventListener('dragover', (ev) => { ev.preventDefault(); row.classList.add('drop-hint'); });
    row.addEventListener('dragleave', () => row.classList.remove('drop-hint'));
    row.addEventListener('drop', (ev) => {
      ev.preventDefault();
      const to = +row.dataset.i;
      if (dragFrom != null && dragFrom !== to) move(dragFrom, to);
      dragFrom = null;
    });
  });
}

/* ------- pairwise ranking (interactive bottom-up merge sort) ------- */
const pwEstimate = (n) => { const c = Math.ceil(Math.log2(n)); return n * c - Math.pow(2, c) + 1; };
function startPairwise(l) {
  const urls = l.items.filter((u) => byUrl.has(u));
  state.pw = {
    listId: l.id, listName: l.name,
    pool: urls.map((u) => [u]), a: null, b: null, ai: 0, bi: 0, out: [],
    count: 0, est: pwEstimate(urls.length), undo: [], result: null,
  };
  pwAdvance();
  rerender();
}
function pwAdvance() {
  const p = state.pw;
  while (!p.result) {
    if (p.a) return; // waiting on a comparison
    if (p.pool.length >= 2) { p.a = p.pool.shift(); p.b = p.pool.shift(); p.ai = 0; p.bi = 0; p.out = []; return; }
    p.result = p.pool[0] || [];
  }
}
function pwPick(which) {
  const p = state.pw;
  p.undo.push(JSON.stringify({ pool: p.pool, a: p.a, b: p.b, ai: p.ai, bi: p.bi, out: p.out, count: p.count }));
  if (p.undo.length > 400) p.undo.shift();
  p.count++;
  if (which === 'a') p.out.push(p.a[p.ai++]); else p.out.push(p.b[p.bi++]);
  if (p.ai >= p.a.length || p.bi >= p.b.length) {
    p.out.push(...p.a.slice(p.ai), ...p.b.slice(p.bi));
    p.pool.push(p.out);
    p.a = p.b = null;
    pwAdvance();
  }
  rerender();
}
function pwUndo() {
  const p = state.pw;
  const snap = p.undo.pop();
  if (!snap) return;
  Object.assign(p, JSON.parse(snap), { result: null });
  rerender();
}
function duelCard(it, side) {
  let h = `<button class="duel" data-pick="${side}">`;
  h += `<span class="duel-org">${esc(it.org)}</span>`;
  h += `<span class="duel-title">${esc(it.title)}</span>`;
  h += `<span class="badges"><span class="badge"><span class="dot" style="background:${CAT_COLORS[it.category]}"></span>${esc(it.category)}</span>${modeBadge(it)}</span>`;
  h += `<span class="duel-comp">${esc(it.compText || 'Comp not listed')}</span>`;
  if (it.orgBlurb) h += `<span class="duel-blurb">${esc(it.orgBlurb)}</span>`;
  if (it.whyFit) h += `<span class="duel-why"><b>Why you:</b> ${esc(it.whyFit)}</span>`;
  h += `<span class="duel-overall">Overall ${it.ratings.overall.toFixed(1)}</span>`;
  h += '</button>';
  return h;
}
function renderPairwise(host) {
  const p = state.pw;
  if (p.result) {
    const items = p.result.map((u) => byUrl.get(u)).filter(Boolean);
    let h = `<div class="lists-head"><h2 class="cx-h2" style="margin:0">Your ranking — ${esc(p.listName)}</h2></div>`;
    h += `<div class="count-note">Built from ${p.count} choices. Save it, apply it to the original list, or export it.</div>`;
    h += '<div class="list-actions">';
    h += `<button class="btn-primary" id="pwSaveNew">${icon('plus', 15)} Save as new list</button>`;
    h += `<button class="btn-ghost" id="pwApply">Apply order to “${esc(p.listName)}”</button>`;
    h += `<button class="btn-ghost" id="pwCsv">${icon('download', 15)} Export CSV</button>`;
    h += `<button class="btn-ghost" id="pwClose">Done</button>`;
    h += '</div><div class="rank-rows">';
    items.forEach((it, i) => {
      h += `<div class="rank-row"><span class="rank">${i + 1}</span><span class="pick-dot" style="background:${CAT_COLORS[it.category]}"></span>`;
      h += `<span class="pick-main"><b>${esc(it.org)}</b> — ${esc(it.title)}<span class="row-sub">${esc(it.compText || '')}</span></span>`;
      h += `<span class="pick-overall">${it.ratings.overall.toFixed(1)}</span>`;
      h += `<a class="pick-open" href="${esc(it.url)}" target="_blank" rel="noopener noreferrer">${icon('external', 15)}</a></div>`;
    });
    h += '</div>';
    host.innerHTML = h;
    document.getElementById('pwSaveNew').addEventListener('click', () => {
      promptDialog({ title: 'Save ranking as a new list', label: 'List name', placeholder: p.listName + ' — ranked', multiline: false, okText: 'Save' }).then((name) => {
        if (name == null) return;
        const nl = { id: uuid(), name: (name.trim() || p.listName + ' — ranked'), items: p.result.slice(), updatedAt: Date.now() };
        LISTS.push(nl); saveLists(); pushList(nl);
        state.pw = null; state.listId = nl.id; rerender();
        toast('Ranking saved', { kind: 'success' });
      });
    });
    document.getElementById('pwApply').addEventListener('click', () => {
      const l = getList(p.listId);
      if (l) { l.items = p.result.slice(); touchList(l); }
      state.pw = null; state.listId = p.listId; rerender();
      toast('Order applied', { kind: 'success' });
    });
    document.getElementById('pwCsv').addEventListener('click', () => exportCsv(p.listName + ' — ranked', items));
    document.getElementById('pwClose').addEventListener('click', () => { state.pw = null; rerender(); });
    return;
  }

  const A = byUrl.get(p.a[p.ai]), B = byUrl.get(p.b[p.bi]);
  const pct = Math.min(99, Math.round((p.count / Math.max(1, p.est)) * 100));
  let h = `<div class="lists-head"><h2 class="cx-h2" style="margin:0">Which would you rather pursue?</h2></div>`;
  h += `<div class="count-note">Ranking “${esc(p.listName)}” · choice ${p.count + 1} of ~${p.est}</div>`;
  h += `<div class="pw-bar"><span style="width:${pct}%"></span></div>`;
  h += `<div class="duel-row">${duelCard(A, 'a')}<span class="duel-vs">vs</span>${duelCard(B, 'b')}</div>`;
  h += `<div class="list-actions"><button class="btn-ghost" id="pwUndo" ${p.undo.length ? '' : 'disabled'}>${icon('undo', 15)} Undo</button>`;
  h += `<button class="btn-ghost danger" id="pwCancel">Cancel</button></div>`;
  host.innerHTML = h;
  host.querySelectorAll('[data-pick]').forEach((b) => b.addEventListener('click', () => pwPick(b.getAttribute('data-pick'))));
  document.getElementById('pwUndo').addEventListener('click', pwUndo);
  document.getElementById('pwCancel').addEventListener('click', () => {
    confirmDialog({ title: 'Stop ranking?', message: 'Progress in this comparison run will be lost.', okText: 'Stop', danger: true }).then((ok) => {
      if (ok) { state.pw = null; rerender(); }
    });
  });
}

/* ================= CSV export ================= */
const csvCell = (s) => '"' + String(s == null ? '' : s).replace(/"/g, '""') + '"';
function exportCsv(name, items) {
  const head = ['Rank', 'Organization', 'Title', 'Category', 'Type', 'Work mode', 'Schedule notes', 'Area', 'Location',
    'Compensation (as listed)', 'Benefits (as listed)', 'About the org', 'Why you fit', 'Contact', 'Apply link',
    'Mission', 'Fit', 'Comp', 'Flex', 'Overall', 'Verified'];
  const rows = items.map((it, i) => [
    i + 1, it.org, it.title, it.category, it.type, it.workMode, it.modeNotes || '', it.area || '', it.location || '',
    it.compText || 'Not listed', it.benefitsText || 'Not listed', it.orgBlurb || '', it.whyFit || '',
    it.contactNote || 'Apply via posting link', it.url,
    it.ratings.mission, it.ratings.fit, it.ratings.comp, it.ratings.flex, it.ratings.overall, it.verified || '',
  ].map(csvCell).join(','));
  const csv = head.map(csvCell).join(',') + '\n' + rows.join('\n');
  const fname = name.replace(/[^\w\s-]+/g, '').trim().replace(/\s+/g, '-').toLowerCase() || 'compass-list';
  download(fname + '.csv', csv, 'text/csv');
  toast('CSV exported', { body: items.length + ' rows with contact info.', kind: 'success' });
}
