// -----------------------------------------------------------------------
// app.js — the family album. Hash routes, so the browser's Back button
// always does what a grandparent expects:
//   #/                      home
//   #/chapter/<id>          one chapter
//   #/years  #/years/1950   by decade
//   #/search?q=lake         search
//   #/loved                 photos this visitor loved
//   …/p/<photoId>           the viewer, open on top of any of the above
// -----------------------------------------------------------------------
import { CONFIG } from './config.js';
import { loadLibrary, yearLabel } from './library.js';
import { SKINS, THEME_COLOR } from './skins.js';
import { makeZip } from './zip.js';
import { icon, registerIcons } from '../vendor/polecat-shell/icons.js';

registerIcons({
  heart: '<path d="M12 20s-7.5-4.6-9.2-9.4C1.6 7 3.9 4 7.2 4c2 0 3.6 1.1 4.8 2.8C13.2 5.1 14.8 4 16.8 4c3.3 0 5.6 3 4.4 6.6C19.5 15.4 12 20 12 20z"/>',
  share: '<path d="M12 3v12M8 7l4-4 4 4"/><path d="M5 12v7a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-7"/>',
  pause: '<path d="M8 5v14M16 5v14"/>',
  zoom: '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3M11 8v6M8 11h6"/>',
  shuffle: '<path d="M3 7h3.5c2 0 3.2 1 4.2 2.6l2.6 4.8c.9 1.6 2.2 2.6 4.2 2.6H21"/><path d="M3 17h3.5c1.5 0 2.6-.6 3.4-1.6M14.1 8.6c.8-1 1.9-1.6 3.4-1.6H21M18 4l3 3-3 3M18 14l3 3-3 3"/>',
  frame: '<rect x="3.5" y="4.5" width="17" height="15" rx="1.5"/><path d="m3.5 16 5-5 4 4 3-3 4.5 4.5"/><circle cx="15.5" cy="8.5" r="1.4"/>',
  boxes: '<path d="M3 8l9-4 9 4-9 4-9-4z"/><path d="M3 8v8l9 4 9-4V8M12 12v8"/>',
});

const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const P = CONFIG.access?.prefix || 'memories';

// ---- prefs (look & feel) + loved photos, per device ---------------------
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(`${P}.${k}`)) ?? d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem(`${P}.${k}`, JSON.stringify(v)); } catch {} },
};
const prefs = Object.assign({ skin: CONFIG.defaultSkin || 'heirloom', mode: 'auto', text: 'regular' }, store.get('prefs', {}));
let loved = new Set(store.get('loved', []));

function applyPrefs() {
  const d = document.documentElement;
  d.dataset.skin = prefs.skin; d.dataset.mode = prefs.mode; d.dataset.text = prefs.text;
  const dark = prefs.mode === 'dark' || (prefs.mode === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
  d.dataset.scheme = dark ? 'dark' : 'light';
  const tc = THEME_COLOR[prefs.skin]?.[d.dataset.scheme];
  if (tc) $('meta[name="theme-color"]').setAttribute('content', tc);
  store.set('prefs', prefs);
}
matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', () => prefs.mode === 'auto' && applyPrefs());

function hydrateIcons(root = document) {
  $$('.ic-slot[data-icon]', root).forEach((el) => { if (!el.firstChild) el.innerHTML = icon(el.dataset.icon, 22); });
}

let toastTimer;
function toast(msg, ms = 2600) {
  const t = $('#toast'); t.textContent = msg; t.hidden = false;
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, ms);
}

// ---- state ----------------------------------------------------------------
let LIB = null;            // normalized library
let byId = new Map();
let chapterById = new Map();
let guestLabel = '';
let isKeeper = false;
let currentBase = null;    // the route under the viewer
let currentList = [];      // photos the viewer pages through

// ---- boot -----------------------------------------------------------------
applyPrefs();
hydrateIcons();
boot();

async function boot() {
  const main = $('#main');
  document.title = CONFIG.title;
  let gate = { granted: true, label: '' };
  if (CONFIG.access?.enabled) {
    try {
      const { runGate } = await import('./gate.js');
      gate = await runGate(CONFIG, main);
    } catch (err) {
      console.warn('Gate unavailable', err);
    }
  }
  if (!gate.granted) return;
  guestLabel = gate.label || '';
  isKeeper = !!gate.isAdmin;
  if (gate.keeperUnlocked) setTimeout(() => toast(`That was the keeper's key — you're in, and you can make invite links on the Keeper's page.`, 6500), 600);
  showChrome();
  main.innerHTML = `<div class="loading"><div><div class="ring"></div><p>Opening the album…</p></div></div>`;
  try {
    LIB = await loadLibrary(CONFIG);
  } catch (err) {
    main.innerHTML = `<div class="error-card"><h2>The album didn't open</h2><p>${esc(err.message || err)}</p>
      <p>Check your internet connection and try again. If it keeps happening, let ${esc(CONFIG.keeper)} know.</p>
      <button class="btn btn-primary" type="button" onclick="location.reload()">Try again</button></div>`;
    return;
  }
  byId = new Map(LIB.photos.map((p) => [p.id, p]));
  chapterById = new Map(LIB.chapters.map((c) => [c.id, c]));
  if (LIB.stale) toast('Showing the copy saved on this device — the internet seems to be off.', 4500);
  window.addEventListener('hashchange', route);
  route();
  registerSW();
}

function showChrome() {
  $('#brandTitle').textContent = CONFIG.title;
  $('#brandSub').textContent = CONFIG.honorees.map((h) => h.name.split(' ')[0]).join(' & ');
  $('.brand-mark').innerHTML = icon('heart', 20);
  $('#footKeeper').innerHTML = `This album is kept by ${esc(CONFIG.keeper)}. <a href="admin/">Keeper's page</a>`;
  ['#topbar', '#tabbar', '#foot'].forEach((s) => { $(s).hidden = false; });
  document.body.classList.add('has-tabbar');
  // The top bar grows with the text size; sticky things sit just under it.
  const bar = $('#topbar');
  const setBarH = () => document.documentElement.style.setProperty('--topbar-h', `${bar.offsetHeight}px`);
  setBarH(); new ResizeObserver(setBarH).observe(bar);
  $('#lookButton').addEventListener('click', openLook);
  $('[data-look]').addEventListener('click', openLook);
}

// ---- router ---------------------------------------------------------------
function parseHash() {
  let h = location.hash.replace(/^#/, '') || '/';
  let photo = null;
  const m = h.match(/^(.*?)\/p\/([^/?]+)(\?.*)?$/);
  if (m) { photo = decodeURIComponent(m[2]); h = (m[1] || '/') + (m[3] || ''); }
  const [path, qs] = h.split('?');
  const parts = path.split('/').filter(Boolean);
  return { base: h, parts, q: new URLSearchParams(qs || ''), photo };
}

function route() {
  const r = parseHash();
  const fromApp = navFromApp; navFromApp = false;
  if (r.base !== currentBase) {
    const prev = currentBase;
    currentBase = r.base;
    closeViewer(true);
    // Decade to decade on the years page: just glide there, no re-render.
    if (r.parts[0] === 'years' && prev?.startsWith('/years') && $('#main .decade-bar')) focusDecade($('#main'), r.parts[1]);
    else renderBase(r);
  }
  if (r.photo && byId.has(r.photo)) { if (!V.open) V.cameFromApp = fromApp; openViewer(r.photo); }
  else if (!r.photo) closeViewer(true);
}

function setNav(name) {
  $$('[data-nav]').forEach((a) => { if (a.dataset.nav === name) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
}

function renderBase(r) {
  const main = $('#main');
  const [v, arg] = r.parts;
  let html; let after;
  if (v === 'chapter' && chapterById.has(arg)) ({ html, after } = viewChapter(arg));
  else if (v === 'years') ({ html, after } = viewYears(arg));
  else if (v === 'search') ({ html, after } = viewSearch(r.q.get('q') || ''));
  else if (v === 'loved') ({ html, after } = viewLoved());
  else ({ html, after } = viewHome());
  main.innerHTML = `<div class="view">${html}</div>`;
  hydrateIcons(main);
  after?.(main);
  if (!(v === 'years' && arg)) window.scrollTo({ top: 0, behavior: 'instant' });
}

// a link that opens a photo on top of the current page
const photoHref = (id) => `#${(currentBase === '/' ? '' : currentBase.split('?')[0])}/p/${encodeURIComponent(id)}${currentBase.includes('?') ? '?' + currentBase.split('?')[1] : ''}`;

// ---- views ----------------------------------------------------------------
function viewHome() {
  setNav('home');
  document.title = CONFIG.title;
  const H = CONFIG.honorees;
  const names = H.length === 2
    ? `${esc(firstNames(H[0].name))}<span class="amp">&amp;</span>${esc(firstNames(H[1].name))}`
    : H.map((h) => esc(h.name)).join(', ');
  const picks = pickStack();
  const decades = decadeCounts();
  const lovedList = LIB.photos.filter((p) => loved.has(p.id));
  const greet = guestLabel && !sessionStorage.getItem(`${P}.greeted`) ? `<p class="greeting">Welcome, ${esc(guestLabel)}.</p>` : '';
  if (greet) sessionStorage.setItem(`${P}.greeted`, '1');
  const html = `
    <div class="note-row">
      ${CONFIG.sample ? `<p class="sample-note">${icon('boxes', 18)} Sample photos — the real album is on its way</p>` : ''}
      ${isKeeper ? `<a class="sample-note keeper-note" href="admin/">${icon('link', 18)} Make an invite link</a>` : ''}
    </div>
    <section class="hero">
      <div>
        ${greet}
        <p class="kicker">${esc(CONFIG.title)}</p>
        <h1 class="hero-names">${names}</h1>
        <p class="hero-years">${H.map((h) => `<span>${esc(h.name.split(' ')[0])} · ${esc(h.years)}</span>`).join('')}</p>
        <p class="hero-dedication">${esc(CONFIG.dedication)}</p>
        <div class="hero-ctas">
          <button class="btn btn-primary" type="button" data-play="all">${icon('play', 22)} Watch the slideshow</button>
          <a class="btn btn-ghost" href="#chapters" data-scroll="chapters">${icon('book', 22)} Look through the album</a>
        </div>
      </div>
      <div class="stack" aria-label="A few favorite photos">
        ${picks.map((p) => `<button class="print" type="button" data-open="${esc(p.id)}" aria-label="Open ${esc(p.title)}"><img src="${esc(p.thumb)}" alt="" ${fallbackAttr(p, true)}></button>`).join('')}
      </div>
    </section>

    <section class="section" aria-labelledby="momentTitle">
      <div class="section-head"><h2 id="momentTitle">A memory for today</h2></div>
      <div class="moment" id="moment"></div>
    </section>

    <section class="section" id="chapters" aria-labelledby="chTitle">
      <div class="section-head"><h2 id="chTitle">The chapters</h2><span class="lede">${LIB.photos.length} photos and keepsakes</span></div>
      <div class="chapters">
        ${LIB.chapters.map((c, i) => chapterCard(c, i)).join('')}
      </div>
    </section>

    <section class="section" aria-labelledby="yrTitle">
      <div class="section-head"><h2 id="yrTitle">Look by year</h2></div>
      <div class="chips">
        ${decades.map(([d, n]) => `<a class="chip" href="#/years/${d}">${d === 'unknown' ? 'Date unknown' : `${d}s`} <small>${n}</small></a>`).join('')}
      </div>
    </section>

    ${lovedList.length ? `
    <section class="section" aria-labelledby="lvTitle">
      <div class="section-head"><h2 id="lvTitle">Photos you loved</h2><a class="btn btn-quiet" href="#/loved">See all ${lovedList.length}</a></div>
      <div class="jgrid" id="lovedGrid"></div>
    </section>` : ''}
  `;
  return {
    html,
    after(main) {
      currentList = LIB.photos;
      wireCommon(main, LIB.photos);
      renderMoment();
      if (lovedList.length) renderGrid($('#lovedGrid', main), lovedList.slice(0, 8));
    },
  };
}

function chapterCard(c, i) {
  const cover = byId.get(c.cover);
  return `<a class="chapter-card" href="#/chapter/${esc(c.id)}">
    <div class="chapter-cover">${cover ? `<img src="${esc(cover.thumb)}" alt="" loading="lazy" ${fallbackAttr(cover, true)}>` : ''}</div>
    <div class="chapter-body">
      <span class="chapter-num">Chapter ${i + 1}</span>
      <h3>${esc(c.title)}</h3>
      <span class="chapter-meta">${c.count} ${c.count === 1 ? 'photo' : 'photos'}${c.span ? ` · ${spanLabel(c.span)}` : ''}</span>
    </div></a>`;
}

let momentIdx = -1;
function renderMoment(step = 0) {
  const el = $('#moment'); if (!el) return;
  const pool = LIB.photos.filter((p) => p.kind === 'photo' || p.caption);
  if (momentIdx < 0) {
    const day = Math.floor(Date.now() / 86400000);
    momentIdx = day % pool.length;
  }
  momentIdx = (momentIdx + step + pool.length) % pool.length;
  const p = pool[momentIdx];
  el.innerHTML = `
    <button class="moment-img" type="button" data-open="${esc(p.id)}" aria-label="Open ${esc(p.title)} larger"><img src="${esc(p.src)}" alt="${esc(p.title)}" ${fallbackAttr(p)}></button>
    <div class="moment-body">
      <span class="kicker">${esc(chapterById.get(p.chapter)?.title || '')}</span>
      <h3>${esc(p.title)}</h3>
      <p class="moment-meta">${esc([yearLabel(p), p.place].filter(Boolean).join(' · '))}</p>
      ${p.caption ? `<p>${esc(p.caption)}</p>` : ''}
      <div class="moment-actions">
        <button class="btn btn-ghost" type="button" data-moment="next">${icon('shuffle', 22)} Show me another</button>
        <a class="btn btn-quiet" href="${photoHref(p.id)}">Open it</a>
      </div>
    </div>`;
  $('[data-moment="next"]', el).addEventListener('click', () => {
    renderMoment(1 + Math.floor(Math.random() * 3));
    $('[data-moment="next"]', el)?.focus({ preventScroll: true }); // the card was rebuilt; keep focus on the button
  });
  const openIt = (e) => { e.preventDefault(); currentList = LIB.photos; go(photoHref(p.id)); };
  $('[data-open]', el).addEventListener('click', openIt);
  $('a.btn-quiet', el).addEventListener('click', openIt); // same path as the picture, so Back works the same
  if (step) el.querySelector('.moment-img img')?.animate?.([{ opacity: 0 }, { opacity: 1 }], { duration: reduceMotion() ? 0 : 450, easing: 'ease-out' });
}

function viewChapter(id) {
  setNav('home');
  const c = chapterById.get(id);
  const idx = LIB.chapters.indexOf(c);
  const list = LIB.photos.filter((p) => p.chapter === id);
  const next = LIB.chapters[idx + 1];
  document.title = `${c.title} · ${CONFIG.title}`;
  const html = `
    <header class="page-head">
      <a class="back-link" href="#/">${icon('back', 20)} Album home</a>
      <span class="kicker">Chapter ${idx + 1} of ${LIB.chapters.length}${c.span ? ` · ${spanLabel(c.span)}` : ''}</span>
      <h1>${esc(c.title)}</h1>
      ${c.blurb ? `<p class="lede">${esc(c.blurb)}</p>` : ''}
      <div class="row">
        <button class="btn btn-primary" type="button" data-play="chapter">${icon('play', 22)} Slideshow</button>
        <button class="btn btn-ghost" type="button" data-zip="chapter">${icon('download', 22)} Save all ${list.length}</button>
      </div>
    </header>
    <div class="jgrid" id="grid"></div>
    ${next ? `<a class="next-chapter" href="#/chapter/${esc(next.id)}"><span><span class="kicker">Next chapter</span><b>${esc(next.title)}</b></span>${icon('chevron', 28)}</a>`
      : `<a class="next-chapter" href="#/"><span><span class="kicker">That's every chapter</span><b>Back to the album home</b></span>${icon('home', 28)}</a>`}`;
  return {
    html,
    after(main) {
      currentList = list;
      renderGrid($('#grid', main), list);
      wireCommon(main, list, c.title);
    },
  };
}

function viewYears(focus) {
  setNav('years');
  document.title = `By year · ${CONFIG.title}`;
  const groups = new Map();
  LIB.photos.slice().sort((a, b) => (a.year ?? 99999) - (b.year ?? 99999)).forEach((p) => {
    const k = p.decade ?? 'unknown';
    if (!groups.has(k)) groups.set(k, []);
    groups.get(k).push(p);
  });
  const keys = [...groups.keys()];
  const html = `
    <header class="page-head">
      <span class="kicker">The whole album, oldest first</span>
      <h1>By year</h1>
      <p class="lede">Tap a decade to jump straight to it.</p>
    </header>
    <div class="decade-bar"><div class="chips" role="list">
      ${keys.map((k) => `<a role="listitem" class="chip" href="#/years/${k}" data-decade="${k}">${k === 'unknown' ? 'Date unknown' : `${k}s`} <small>${groups.get(k).length}</small></a>`).join('')}
    </div></div>
    ${keys.map((k) => {
      const list = groups.get(k);
      const ys = list.map((p) => p.year).filter(Boolean);
      return `<section class="year-block" id="decade-${k}">
        <h2>${k === 'unknown' ? 'Date unknown' : `The ${k}s`}</h2>
        <p class="sub">${list.length} ${list.length === 1 ? 'photo' : 'photos'}${ys.length ? ` · ${spanLabel([Math.min(...ys), Math.max(...ys)])}` : ''}</p>
        <div class="jgrid" data-decade-grid="${k}"></div></section>`;
    }).join('')}`;
  return {
    html,
    after(main) {
      const all = keys.flatMap((k) => groups.get(k));
      currentList = all;
      keys.forEach((k) => renderGrid($(`[data-decade-grid="${k}"]`, main), groups.get(k), all));
      wireCommon(main, all);
      if (focus) focusDecade(main, focus);
    },
  };
}

function focusDecade(main, focus) {
  $$('[data-decade]', main).forEach((a) => { if (a.dataset.decade === focus) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
  const smooth = reduceMotion() ? 'auto' : 'smooth';
  const target = focus && $(`#decade-${CSS.escape(focus)}`, main);
  requestAnimationFrame(() => (target ? target.scrollIntoView({ behavior: smooth, block: 'start' }) : window.scrollTo({ top: 0, behavior: smooth })));
  if (focus) $(`[data-decade="${CSS.escape(focus)}"]`, main)?.scrollIntoView({ inline: 'center', block: 'nearest', behavior: smooth });
}

function viewSearch(q) {
  setNav('search');
  document.title = `Search · ${CONFIG.title}`;
  const people = [...new Set(LIB.photos.flatMap((p) => p.people))];
  const placeCounts = {};
  LIB.photos.forEach((p) => { if (p.place) { const k = p.place.split(',')[0].trim(); placeCounts[k] = (placeCounts[k] || 0) + 1; } });
  const places = Object.entries(placeCounts).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k]) => k);
  const html = `
    <header class="page-head">
      <span class="kicker">Find a photo</span>
      <h1>Search the album</h1>
    </header>
    <form class="search-box" role="search" id="searchForm">
      ${icon('search', 24)}
      <label class="sr" for="q">Search for a name, place, year or thing</label>
      <input id="q" type="search" autocomplete="off" enterkeyhint="search" placeholder="A name, a place, a year…" value="${esc(q)}">
      <button class="clear" type="button" aria-label="Clear search" ${q ? '' : 'hidden'}>${icon('close', 20)}</button>
    </form>
    <div class="search-hints">
      ${people.length ? `<div><span class="kicker">People</span><div class="chips" style="margin-top:.5rem">${people.map((n) => `<button class="chip" type="button" data-q="${esc(n)}">${esc(n)}</button>`).join('')}</div></div>` : ''}
      ${places.length ? `<div><span class="kicker">Places</span><div class="chips" style="margin-top:.5rem">${places.map((n) => `<button class="chip" type="button" data-q="${esc(n)}">${esc(n)}</button>`).join('')}</div></div>` : ''}
      <div><span class="kicker">Try</span><div class="chips" style="margin-top:.5rem">${['wedding', 'Christmas', 'lake', 'horse', 'car', 'letter'].map((n) => `<button class="chip" type="button" data-q="${n}">${n}</button>`).join('')}</div></div>
    </div>
    <p class="result-count" id="resultCount" aria-live="polite"></p>
    <div class="jgrid" id="results"></div>`;
  return {
    html,
    after(main) {
      const input = $('#q', main); const clear = $('.clear', main);
      let t;
      const run = (val, push) => {
        const v = val.trim();
        clear.hidden = !v;
        $$('[data-q]', main).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.q.toLowerCase() === v.toLowerCase())));
        const res = searchPhotos(v);
        currentList = res;
        const count = $('#resultCount', main);
        const grid = $('#results', main);
        if (!v) { count.textContent = ''; grid.innerHTML = ''; }
        else if (!res.length) {
          count.textContent = '';
          grid.innerHTML = `<div class="empty"><h3>Nothing found for "${esc(v)}"</h3><p>Try a first name, a place, or a year like 1965.</p></div>`;
        } else {
          count.textContent = `${res.length} ${res.length === 1 ? 'photo' : 'photos'} for "${v}"`;
          renderGrid(grid, res);
        }
        const target = `#/search${v ? `?q=${encodeURIComponent(v)}` : ''}`;
        currentBase = target.slice(1);
        if (push) history.pushState(null, '', target); else history.replaceState(null, '', target);
      };
      input.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => run(input.value, false), 180); });
      $('#searchForm', main).addEventListener('submit', (e) => { e.preventDefault(); input.blur(); run(input.value, false); });
      clear.addEventListener('click', () => { input.value = ''; run('', false); input.focus(); });
      $$('[data-q]', main).forEach((b) => b.addEventListener('click', () => { input.value = b.dataset.q; run(b.dataset.q, true); }));
      wireCommon(main, () => currentList);
      if (q) run(q, false); else if (matchMedia('(hover: hover)').matches) input.focus();
    },
  };
}

function viewLoved() {
  setNav('home');
  document.title = `Photos you loved · ${CONFIG.title}`;
  const list = LIB.photos.filter((p) => loved.has(p.id));
  const html = `
    <header class="page-head">
      <a class="back-link" href="#/">${icon('back', 20)} Album home</a>
      <h1>Photos you loved</h1>
      <p class="lede">Tap the heart on any photo to keep it here. Only you see this list, on this device.</p>
      ${list.length ? `<div class="row"><button class="btn btn-primary" type="button" data-play="loved">${icon('play', 22)} Slideshow</button></div>` : ''}
    </header>
    ${list.length ? '<div class="jgrid" id="grid"></div>' : `<div class="empty"><h3>No favorites yet</h3><p>When a photo makes you smile, tap “Love it” and it will wait for you here.</p></div>`}`;
  return { html, after(main) { currentList = list; if (list.length) renderGrid($('#grid', main), list); wireCommon(main, list, 'Photos you loved'); } };
}

// shared wiring for any view: open photos, slideshows, zips, smooth scroll.
// #main outlives every view, so it gets ONE listener; each view just swaps
// in its own list/label (adding a listener per view stacked them up, so
// "Save all" ran once for every page visited).
let common = { getList: () => [], label: '' };
function wireCommon(main, list, label) {
  common = { getList: typeof list === 'function' ? list : () => list, label };
  if (main._wired) return;
  main._wired = true;
  main.addEventListener('click', (e) => {
    const { getList, label } = common;
    const open = e.target.closest('[data-open]');
    if (open && !open.closest('#moment')) {
      e.preventDefault();
      const tileList = open.closest('.jgrid')?._ctx; // a grid knows which photos it pages through
      currentList = tileList || getList();
      go(photoHref(open.dataset.open)); return;
    }
    const play = e.target.closest('[data-play]');
    if (play) { startShow(play.dataset.play === 'all' ? LIB.photos : getList()); return; }
    const zip = e.target.closest('[data-zip]');
    if (zip) { if (!zip.disabled) saveAll(getList(), label || CONFIG.title, zip); return; }
    const sc = e.target.closest('[data-scroll]');
    if (sc) { e.preventDefault(); $(`#${sc.dataset.scroll}`)?.scrollIntoView({ behavior: reduceMotion() ? 'auto' : 'smooth' }); }
  });
}

let navFromApp = false;
function go(hash) { navFromApp = true; if (location.hash !== hash) location.hash = hash; else route(); }

// ---- helpers --------------------------------------------------------------
function firstNames(n) { return n.split(' ')[0]; }
function spanLabel([a, b]) { return a === b ? `${a}` : `${a}–${b}`; }
function decadeCounts() {
  const m = new Map();
  LIB.photos.forEach((p) => m.set(p.decade, (m.get(p.decade) || 0) + 1));
  return [...m.entries()].sort((a, b) => (a[0] ?? 99999) - (b[0] ?? 99999)).map(([d, n]) => [d ?? 'unknown', n]);
}
function pickStack() {
  const covers = LIB.chapters.map((c) => byId.get(c.cover)).filter(Boolean);
  const photos = covers.filter((p) => p.kind === 'photo');
  const pool = photos.length >= 3 ? photos : LIB.photos;
  return [pool[0], pool[Math.floor(pool.length / 2)], pool[pool.length - 1]].filter(Boolean)
    .filter((p, i, a) => a.indexOf(p) === i);
}
function searchPhotos(q) {
  if (!q) return [];
  const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
  const singular = (t) => t.replace(/(es|s)$/, '');
  return LIB.photos.filter((p) => terms.every((t) => p.search.includes(t) || (t.length > 3 && p.search.includes(singular(t)))));
}
function fallbackAttr(p, thumb) {
  const f = thumb ? (p.thumbFallback || p.fallback) : p.fallback;
  return f ? `data-fallback="${esc(f)}" onerror="if(this.dataset.fallback&&this.src!==this.dataset.fallback){this.src=this.dataset.fallback}"` : '';
}

// ---- justified grid -------------------------------------------------------
const gridObservers = new WeakMap();
function renderGrid(el, list, contextList) {
  if (!el) return;
  el.innerHTML = '';
  el._list = list;
  el._ctx = contextList || list;
  layoutGrid(el);
  if (!gridObservers.has(el)) {
    let lastW = el.clientWidth;
    const ro = new ResizeObserver(() => { if (Math.abs(el.clientWidth - lastW) > 4) { lastW = el.clientWidth; layoutGrid(el); } });
    ro.observe(el); gridObservers.set(el, ro);
  }
}
function layoutGrid(el) {
  const list = el._list || [];
  const W = el.clientWidth || 320;
  const pad = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--print-pad')) || 0;
  const gap = W < 520 ? 8 : 12;
  const target = W < 520 ? 138 : W < 900 ? 190 : 235;
  el.style.setProperty('--gap', `${gap}px`);
  const rows = []; let row = []; let sumAr = 0;
  for (const p of list) {
    const ar = p.w && p.h ? p.w / p.h : 4 / 3;
    row.push({ p, ar }); sumAr += ar;
    const h = (W - gap * (row.length - 1) - pad * 2 * row.length) / sumAr;
    if (h <= target) { rows.push({ items: row, h }); row = []; sumAr = 0; }
  }
  if (row.length) {
    const h = (W - gap * (row.length - 1) - pad * 2 * row.length) / sumAr;
    rows.push({ items: row, h: Math.min(h, target * 1.15) });
  }
  const frag = document.createDocumentFragment();
  for (const r of rows) {
    const rowEl = document.createElement('div'); rowEl.className = 'jrow';
    for (const { p, ar } of r.items) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'tile'; b.dataset.open = p.id;
      b.style.width = `${Math.floor(r.h * ar + pad * 2)}px`; b.style.height = `${Math.floor(r.h + pad * 2)}px`;
      b.setAttribute('aria-label', `${p.title}${p.year ? `, ${yearLabel(p)}` : ''}`);
      b.innerHTML = `<img src="${esc(p.thumb)}" alt="" loading="lazy" decoding="async" ${fallbackAttr(p, true)}>
        <span class="tile-label">${esc(p.title)}</span>${loved.has(p.id) ? `<span class="fav-dot" aria-hidden="true">${icon('heart', 16)}</span>` : ''}`;
      const img = b.firstElementChild;
      if (img.complete && img.naturalWidth) img.classList.add('loaded');
      else img.addEventListener('load', () => img.classList.add('loaded'), { once: true });
      img.addEventListener('error', () => img.classList.add('loaded'));
      b.addEventListener('click', () => { currentList = el._ctx; });
      rowEl.appendChild(b);
    }
    frag.appendChild(rowEl);
  }
  el.replaceChildren(frag);
}

// ---- viewer ---------------------------------------------------------------
const V = { el: $('#viewer'), img: $('#vImg'), stage: $('#vStage'), idx: 0, list: [], lastFocus: null, open: false };

function openViewer(id) {
  const list = currentList.length && currentList.some((p) => p.id === id) ? currentList : LIB.photos;
  V.list = list; V.idx = list.findIndex((p) => p.id === id);
  if (!V.open) {
    V.lastFocus = document.activeElement;
    V.el.hidden = false; V.open = true;
    document.body.style.overflow = 'hidden';
    hydrateIcons(V.el);
    $('[data-v="close"]', V.el).focus({ preventScroll: true });
  }
  showPhoto();
}

function closeViewer(silent) {
  if (!V.open) return;
  V.el.hidden = true; V.open = false;
  document.body.style.overflow = '';
  setZoom(false);
  if (V.lastFocus?.isConnected) V.lastFocus.focus({ preventScroll: true });
  else {
    const tile = $(`[data-open="${CSS.escape(V.list[V.idx]?.id || '')}"]`);
    tile?.focus({ preventScroll: true });
  }
  if (!silent) {
    if (V.cameFromApp) history.back();
    else { history.replaceState(null, '', `#${currentBase}`); }
  }
}

function showPhoto() {
  const p = V.list[V.idx]; if (!p) return;
  setZoom(false);
  V.img.classList.add('swap');
  const next = new Image();
  next.decoding = 'async';
  const swapIn = (src) => { V.img.src = src; V.img.alt = p.title; requestAnimationFrame(() => V.img.classList.remove('swap')); };
  next.onload = () => swapIn(next.src);
  next.onerror = () => { if (p.fallback && next.src !== p.fallback) next.src = p.fallback; else swapIn(p.thumb); };
  next.src = p.src;
  $('#vTitle').textContent = p.title;
  $('#vMeta').textContent = [yearLabel(p), p.place, chapterById.get(p.chapter)?.title].filter(Boolean).join(' · ');
  $('#vCaption').textContent = p.caption || '';
  $('#vPeople').innerHTML = p.people.map((n) => `<button type="button" data-person="${esc(n)}">More of ${esc(n)}</button>`).join('');
  $('#vCount').textContent = V.list.length > 1 ? `${V.idx + 1} of ${V.list.length}` : '';
  const dl = $('#vDownload'); dl.href = p.download; dl.setAttribute('download', p.downloadName || `${p.title}.jpg`);
  const fav = $('[data-v="fav"]', V.el); const isFav = loved.has(p.id);
  fav.setAttribute('aria-pressed', String(isFav)); $('.fav-label', fav).textContent = isFav ? 'Loved' : 'Love it';
  const single = V.list.length < 2;
  $$('[data-v="prev"], [data-v="next"]', V.el).forEach((b) => { b.disabled = single; b.style.visibility = single ? 'hidden' : ''; });
  // warm the neighbors
  [1, -1].forEach((d) => { const n = V.list[(V.idx + d + V.list.length) % V.list.length]; if (n) { const i = new Image(); i.src = n.src; } });
  const seen = new Set(store.get('seen', [])); seen.add(p.id); store.set('seen', [...seen]);
}

function step(d) {
  if (V.list.length < 2) return;
  V.idx = (V.idx + d + V.list.length) % V.list.length;
  history.replaceState(null, '', photoHref(V.list[V.idx].id));
  showPhoto();
}

function setZoom(on) {
  V.stage.classList.toggle('zoomed', on);
  const b = $('[data-v="zoom"]', V.el);
  b.setAttribute('aria-pressed', String(on)); $('.zoom-label', b).textContent = on ? 'Fit to screen' : 'Zoom in';
  if (on) requestAnimationFrame(() => {
    V.stage.scrollLeft = (V.stage.scrollWidth - V.stage.clientWidth) / 2;
    V.stage.scrollTop = (V.stage.scrollHeight - V.stage.clientHeight) / 2;
  });
}

V.el.addEventListener('click', async (e) => {
  const person = e.target.closest('[data-person]');
  if (person) { V.open = false; V.el.hidden = true; document.body.style.overflow = ''; location.hash = `#/search?q=${encodeURIComponent(person.dataset.person)}`; return; }
  const b = e.target.closest('[data-v]'); if (!b) return;
  const p = V.list[V.idx];
  switch (b.dataset.v) {
    case 'close': closeViewer(false); break;
    case 'prev': step(-1); break;
    case 'next': step(1); break;
    case 'zoom': setZoom(!V.stage.classList.contains('zoomed')); break;
    case 'fav': {
      if (loved.has(p.id)) { loved.delete(p.id); toast('Removed from your loved photos'); }
      else { loved.add(p.id); toast('Saved to “Photos you loved” on the home page'); }
      store.set('loved', [...loved]); showPhoto(); break;
    }
    case 'share': {
      const url = new URL(photoHref(p.id), location.href).href;
      const data = { title: p.title, text: `${p.title}${p.year ? ` (${yearLabel(p)})` : ''} — from ${CONFIG.title}`, url };
      try {
        if (navigator.share) await navigator.share(data);
        else { await navigator.clipboard.writeText(url); toast('Link copied — paste it in a text or email'); }
      } catch (err) { if (err?.name !== 'AbortError') toast('Could not share right now'); }
      break;
    }
  }
});
V.stage.addEventListener('click', (e) => {
  if (e.target === V.img && !V.stage.classList.contains('zoomed') && matchMedia('(hover: hover)').matches) setZoom(true);
  else if (e.target === V.img && V.stage.classList.contains('zoomed')) setZoom(false);
});
// swipe left/right (buttons do the same thing for anyone who prefers them)
let sx = null, sy = null;
V.stage.addEventListener('pointerdown', (e) => { if (!V.stage.classList.contains('zoomed')) { sx = e.clientX; sy = e.clientY; } });
V.stage.addEventListener('pointerup', (e) => {
  if (sx === null) return;
  const dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
  if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.3) step(dx < 0 ? 1 : -1);
});
V.stage.addEventListener('pointercancel', () => { sx = null; });

document.addEventListener('keydown', (e) => {
  if (!$('#show').hidden) return showKey(e);
  if (!$('#lookSheet').hidden) { if (e.key === 'Escape') closeLook(); return trapFocus(e, $('#lookSheet')); }
  if (!V.open) return;
  if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
  else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
  else if (e.key === 'Escape') { e.preventDefault(); if (V.stage.classList.contains('zoomed')) setZoom(false); else closeViewer(false); }
  else trapFocus(e, V.el);
});

function trapFocus(e, root) {
  if (e.key !== 'Tab') return;
  const f = $$('button:not([disabled]), a[href], input, [tabindex]:not([tabindex="-1"])', root).filter((x) => x.offsetParent !== null && x.style.visibility !== 'hidden');
  if (!f.length) return;
  const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
  else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
}

// ---- slideshow ------------------------------------------------------------
const S = { el: $('#show'), list: [], idx: 0, timer: null, playing: false, hideT: null, wake: null, layer: 0, dur: 7000 };
async function startShow(list) {
  if (!list.length) return;
  S.list = list; S.idx = 0; S.layer = 0;
  // Its own history entry, so the phone's Back button stops the show
  // instead of changing the page underneath it.
  if (S.el.hidden && !S.pushed) { history.pushState({ show: 1 }, '', location.href); S.pushed = true; }
  S.lastFocus = document.activeElement;
  S.el.hidden = false; hydrateIcons(S.el);
  document.body.style.overflow = 'hidden';
  try { await S.el.requestFullscreen?.(); } catch {}
  try { S.wake = await navigator.wakeLock?.request('screen'); } catch {}
  showControls();
  S.playing = true; updateToggle();
  $('[data-s="toggle"]', S.el).focus({ preventScroll: true }); // keyboard focus lives in the show, not behind it
  showSlide();
}
function showSlide() {
  const p = S.list[S.idx];
  const imgs = $$('.show-img', S.el);
  const cur = imgs[S.layer], prev = imgs[1 - S.layer];
  const kb = !reduceMotion();
  cur.classList.remove('kb', 'on');
  cur.onload = () => {
    if (kb) { cur.style.setProperty('--kx', `${(Math.random() * 4 - 2).toFixed(2)}%`); cur.style.setProperty('--ky', `${(Math.random() * 4 - 2).toFixed(2)}%`); cur.style.setProperty('--dur', `${S.dur + 1600}ms`); void cur.offsetWidth; cur.classList.add('kb'); }
    cur.classList.add('on'); prev.classList.remove('on');
  };
  cur.onerror = () => { if (p.fallback && cur.src !== p.fallback) cur.src = p.fallback; };
  cur.src = p.src; cur.alt = p.title;
  $('#sCaption').innerHTML = `${esc(p.title)}<small>${esc([yearLabel(p), p.place].filter(Boolean).join(' · '))}</small>`;
  const n = S.list[(S.idx + 1) % S.list.length]; if (n) { const i = new Image(); i.src = n.src; }
  const bar = $('#sProgress');
  bar.style.transition = 'none'; bar.style.width = `${(S.idx / S.list.length) * 100}%`;
  requestAnimationFrame(() => { bar.style.transition = S.playing ? `width ${S.dur}ms linear` : 'none'; bar.style.width = `${((S.idx + 1) / S.list.length) * 100}%`; });
  clearTimeout(S.timer);
  if (S.playing) S.timer = setTimeout(() => advance(1), S.dur);
}
function advance(d) { S.idx = (S.idx + d + S.list.length) % S.list.length; S.layer = 1 - S.layer; showSlide(); }
function updateToggle() {
  const b = $('[data-s="toggle"]', S.el);
  b.querySelector('.ic-slot').innerHTML = icon(S.playing ? 'pause' : 'play', 22);
  $('.s-toggle-label', b).textContent = S.playing ? 'Pause' : 'Play';
}
function togglePlay() { S.playing = !S.playing; updateToggle(); showSlide(); }
async function stopShow(fromHistory) {
  if (S.el.hidden) return;
  clearTimeout(S.timer); S.playing = false; S.el.hidden = true;
  document.body.style.overflow = V.open ? 'hidden' : '';
  if (S.pushed) { S.pushed = false; if (fromHistory !== true) history.back(); }
  try { if (document.fullscreenElement) await document.exitFullscreen(); } catch {}
  if (S.lastFocus?.isConnected) S.lastFocus.focus({ preventScroll: true }); // after fullscreen ends, or it is lost
  try { await S.wake?.release(); } catch {} S.wake = null;
}
function showControls() {
  S.el.classList.add('controls-on'); clearTimeout(S.hideT);
  S.hideT = setTimeout(() => S.el.classList.remove('controls-on'), matchMedia('(hover: none)').matches ? 6000 : 3500);
}
S.el.addEventListener('pointermove', showControls);
S.el.addEventListener('click', (e) => {
  const b = e.target.closest('[data-s]');
  if (!b) { if (!S.el.classList.contains('controls-on')) { showControls(); return; } return; }
  showControls();
  ({ prev: () => advance(-1), next: () => advance(1), toggle: togglePlay, close: stopShow })[b.dataset.s]();
});
function showKey(e) {
  showControls();
  if (e.key === 'Escape') stopShow();
  else if (e.key === 'ArrowRight') advance(1);
  else if (e.key === 'ArrowLeft') advance(-1);
  else if (e.key === ' ') { e.preventDefault(); togglePlay(); }
  else trapFocus(e, S.el);
}
window.addEventListener('popstate', () => { if (!S.el.hidden) { S.pushed = false; stopShow(true); } });
document.addEventListener('fullscreenchange',() => { if (!document.fullscreenElement && !S.el.hidden && S._wasFs) stopShow(); S._wasFs = !!document.fullscreenElement; });
document.addEventListener('visibilitychange', async () => { if (!S.el.hidden && document.visibilityState === 'visible' && !S.wake) { try { S.wake = await navigator.wakeLock?.request('screen'); } catch {} } });

// ---- save a whole chapter -------------------------------------------------
async function saveAll(list, label, btn) {
  if (!list.length) return;
  btn.disabled = true;
  const files = [];
  try {
    for (let i = 0; i < list.length; i++) {
      toast(`Gathering photos… ${i + 1} of ${list.length}`, 60000);
      const p = list[i];
      const res = await fetch(p.download);
      if (!res.ok) throw new Error(String(res.status));
      files.push({ name: p.downloadName || `${p.title}.jpg`, data: new Uint8Array(await res.arrayBuffer()) });
    }
    const blob = makeZip(files);
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = `${label}.zip`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 30000);
    toast(`Saved ${files.length} photos to your downloads`, 4000);
  } catch {
    if (CONFIG.source === 'drive' && CONFIG.drive?.folderId) {
      toast('Opening the Google Drive folder — use “Download all” there', 5000);
      window.open(`https://drive.google.com/drive/folders/${CONFIG.drive.folderId}`, '_blank', 'noopener');
    } else toast('Could not save them all right now. You can save each photo one at a time.', 5000);
  } finally { btn.disabled = false; }
}

// ---- look & feel sheet ----------------------------------------------------
function openLook() {
  const sheet = $('#lookSheet');
  $('#skinGrid').innerHTML = SKINS.map((s) => `
    <button type="button" role="radio" class="skin-card" data-skin="${s.id}" aria-checked="${prefs.skin === s.id}">
      <span class="skin-swatch" style="background:${s.swatch[0]}">
        <i style="background:${s.swatch[1]}"></i><i style="background:${s.swatch[2]}"></i><i style="background:${s.swatch[3]}"></i>
        <b style="color:${s.swatch[2]};font-family:${s.font === 'serif' ? 'var(--serif)' : 'var(--sans)'}">Aa</b>
      </span>
      <span class="skin-name"><strong>${esc(s.name)}</strong><small>${esc(s.note)}</small></span>
    </button>`).join('');
  syncLook();
  $('#lookScrim').hidden = false; sheet.hidden = false; hydrateIcons(sheet);
  $('[data-close-sheet]', sheet).focus();
}
function syncLook() {
  $$('#skinGrid [data-skin]').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.skin === prefs.skin)));
  $$('#textSeg [data-text]').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.text === prefs.text)));
  $$('#modeSeg [data-mode]').forEach((b) => b.setAttribute('aria-checked', String(b.dataset.mode === prefs.mode)));
}
function closeLook() { $('#lookScrim').hidden = true; $('#lookSheet').hidden = true; $('#lookButton').focus({ preventScroll: true }); }
$('#lookScrim').addEventListener('click', closeLook);
$('#lookSheet').addEventListener('click', (e) => {
  if (e.target.closest('[data-close-sheet]')) return closeLook();
  // button[…] only: <html> carries data-skin/data-text/data-mode too, so a bare
  // [data-skin] matched it for EVERY click and text size / dark never applied.
  const sk = e.target.closest('button[data-skin]'); const tx = e.target.closest('button[data-text]'); const md = e.target.closest('button[data-mode]');
  if (sk) { prefs.skin = sk.dataset.skin; const meta = SKINS.find((s) => s.id === prefs.skin); if (meta?.prefers && prefs.mode === 'auto') prefs.mode = meta.prefers; }
  else if (tx) prefs.text = tx.dataset.text;
  else if (md) prefs.mode = md.dataset.mode;
  else return;
  applyPrefs(); syncLook();
  $$('.jgrid').forEach((g) => g._list && layoutGrid(g));
});

// ---- offline-friendly -----------------------------------------------------
function registerSW() {
  if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(() => {});
}
