/* Wau-Bun — an interactive telling.
   No build step, no framework, no dependencies. Reads the data files loaded
   before it (WAUBUN_FACTIONS, WAUBUN_CHARACTERS, WAUBUN_PART1/2/3) and renders
   four views over the same model: the presence chart, the scene-by-scene
   reader, the cast, and a plain table.

   The model: a scene names who is present (`cast`) and who is spoken of
   (`offstage`). Everything else — first appearance, last appearance, arcs,
   counts, the "enters here" badges — is derived, never hand-maintained.

   Navigation is history-driven: every move (view, scene, selection, an open
   panel) is a history entry, so the browser Back button always undoes exactly
   one step and the URL is shareable.

   The full text of each scene lives in js/data-text-part1.js and is fetched
   only when the reader first needs it — first paint stays light. */
(function () {
  'use strict';

  var PARTS = [WAUBUN_PART1, WAUBUN_PART2, WAUBUN_PART3];
  var FAC = {}, FAC_ORDER = WAUBUN_FACTIONS.map(function (f) { return f.id; });
  WAUBUN_FACTIONS.forEach(function (f) { FAC[f.id] = f; });
  var CH = {};
  WAUBUN_CHARACTERS.forEach(function (c) { CH[c.id] = c; });

  var MODES = [
    { id: 'summary',  label: 'Summary',  note: 'What happens, in brief.' },
    { id: 'modern',   label: 'Modern',   note: 'The contemporary-English edition, in full.' },
    { id: 'original', label: '1856',     note: 'Juliette Kinzie\'s original text, in full.' }
  ];

  var state = {
    part: 'part1',
    view: 'chart',
    scene: null,          // scene shown in the reader
    mode: 'summary',      // summary | modern | original
    selected: [],         // scene ids selected in the chart
    panel: null,          // { kind:'scene'|'character', id }
    factions: FAC_ORDER.slice(),
    query: '',
    pivotalOnly: false,
    cell: 22,             // chart square size in px
    fit: 'none'           // none | width | all
  };
  try {
    var savedMode = localStorage.getItem('waubun.mode');
    if (savedMode && MODES.some(function (m) { return m.id === savedMode; })) state.mode = savedMode;
  } catch (e) {}

  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function part() {
    for (var i = 0; i < PARTS.length; i++) if (PARTS[i].id === state.part) return PARTS[i];
    return PARTS[0];
  }
  function sceneById(id) {
    var list = part().scenes || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  }
  function sceneNo(id) {
    var list = part().scenes || [];
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return i;
    return -1;
  }

  /* ---------------- derived model ---------------- */
  function buildIndex(p) {
    var idx = { byChar: {}, order: [], scenes: p.scenes || [] };
    (p.scenes || []).forEach(function (sc, i) {
      (sc.cast || []).forEach(function (id) { mark(id, i, 'on'); });
      (sc.offstage || []).forEach(function (id) { mark(id, i, 'men'); });
    });
    function mark(id, i, kind) {
      if (!CH[id]) return;
      var rec = idx.byChar[id];
      if (!rec) { rec = idx.byChar[id] = { id: id, at: {}, present: [], mentioned: [], first: null, last: null }; idx.order.push(id); }
      if (rec.at[i] !== 'on') rec.at[i] = kind;
      if (kind === 'on') {
        rec.present.push(i);
        if (rec.first === null) rec.first = i;
        rec.last = i;
      } else rec.mentioned.push(i);
    }
    idx.order.sort(function (a, b) {
      var fa = FAC_ORDER.indexOf(CH[a].faction), fb = FAC_ORDER.indexOf(CH[b].faction);
      if (fa !== fb) return fa - fb;
      var A = idx.byChar[a], B = idx.byChar[b];
      var af = A.first === null ? A.mentioned[0] : A.first;
      var bf = B.first === null ? B.mentioned[0] : B.first;
      if (af !== bf) return af - bf;
      return CH[a].name.localeCompare(CH[b].name);
    });
    return idx;
  }
  var INDEX = {};
  PARTS.forEach(function (p) { INDEX[p.id] = buildIndex(p); });

  function visibleScenes() {
    var p = part();
    return (p.scenes || []).filter(function (sc) { return !state.pivotalOnly || sc.pivotal; });
  }
  function isSelected(id) { return state.selected.indexOf(id) >= 0; }

  function visibleChars() {
    var idx = INDEX[state.part], q = state.query.trim().toLowerCase();
    var cols = visibleScenes(), inCol = {};
    cols.forEach(function (sc) { inCol[sc.id] = true; });
    var sel = state.selected.filter(function (id) { return inCol[id]; });
    return idx.order.filter(function (id) {
      var c = CH[id], rec = idx.byChar[id];
      if (state.factions.indexOf(c.faction) < 0) return false;
      if (q && (c.name + ' ' + (c.alias || '') + ' ' + c.role).toLowerCase().indexOf(q) < 0) return false;
      // with scenes selected, only the people who appear in them (or are spoken of)
      if (sel.length) return sel.some(function (sid) { return !!rec.at[sceneNo(sid)]; });
      var any = false;
      (part().scenes || []).forEach(function (sc, i) { if (inCol[sc.id] && rec.at[i]) any = true; });
      return any;
    });
  }

  /* ---------------- history-driven navigation ---------------- */
  var pushed = 0;
  function snapshot() {
    return {
      part: state.part, view: state.view, scene: state.scene, mode: state.mode,
      selected: state.selected.slice(), panel: state.panel ? { kind: state.panel.kind, id: state.panel.id } : null,
      factions: state.factions.slice(), query: state.query, pivotalOnly: state.pivotalOnly
    };
  }
  function hashFor() {
    var h = '#/' + state.part + '/' + state.view;
    if (state.view === 'story' && state.scene) h += '/' + state.scene + (state.mode !== 'summary' ? '/' + state.mode : '');
    else if (state.panel && state.panel.kind === 'scene') h += '/' + state.panel.id;
    else if (state.selected.length) h += '/sel-' + state.selected.join('+');
    return h;
  }
  // `replace` keeps the current history entry (use for filter fiddling);
  // otherwise every move becomes a Back step.
  function go(patch, replace) {
    Object.assign(state, patch);
    if (replace) history.replaceState(snapshot(), '', hashFor());
    else { history.pushState(snapshot(), '', hashFor()); pushed++; }
    render();
  }
  window.addEventListener('popstate', function (e) {
    if (pushed > 0) pushed--;
    if (e.state) { Object.assign(state, e.state); render(); }
    else { readHash(); render(); }
  });
  function readHash() {
    var m = (location.hash || '').replace(/^#\//, '').split('/');
    if (m[0] && PARTS.some(function (p) { return p.id === m[0]; })) state.part = m[0];
    if (m[1] && ['chart', 'story', 'cast', 'table'].indexOf(m[1]) >= 0) state.view = m[1];
    if (m[2]) {
      if (m[2].indexOf('sel-') === 0) state.selected = m[2].slice(4).split('+');
      else if (state.view === 'story') state.scene = m[2];
      else state.panel = { kind: 'scene', id: m[2] };
    }
    if (m[3] && MODES.some(function (x) { return x.id === m[3]; })) state.mode = m[3];
  }

  /* ---------------- full text, fetched on demand ---------------- */
  var textState = 'idle';   // idle | loading | ready | failed
  var textWaiters = [];
  function ensureText(cb) {
    if (window.WAUBUN_TEXT_PART1) { textState = 'ready'; return cb(); }
    if (textState === 'failed') return cb();
    textWaiters.push(cb);
    if (textState === 'loading') return;
    textState = 'loading';
    var s = document.createElement('script');
    s.src = 'js/data-text-part1.js';
    s.onload = function () { textState = 'ready'; flush(); };
    s.onerror = function () { textState = 'failed'; flush(); };
    document.head.appendChild(s);
    function flush() { var w = textWaiters; textWaiters = []; w.forEach(function (f) { f(); }); }
  }
  function passage(sceneId, mode) {
    var store = window.WAUBUN_TEXT_PART1;
    if (state.part !== 'part1' || !store || !store[sceneId]) return null;
    return store[sceneId][mode] || null;
  }

  /* ---------------- chrome ---------------- */
  function renderParts() {
    var host = $('#wbParts');
    host.innerHTML = '';
    PARTS.forEach(function (p) {
      var b = el('button', 'wb-part');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', p.id === state.part ? 'true' : 'false');
      b.innerHTML = '<b>PART ' + p.number + '</b> ' + esc(p.title);
      b.addEventListener('click', function () {
        go({ part: p.id, scene: null, selected: [], panel: null,
             view: (p.scenes || []).length ? state.view : 'chart' });
      });
      host.appendChild(b);
    });
  }

  function renderHead() {
    var p = part(), idx = INDEX[p.id];
    $('#wbKicker').textContent = 'Part ' + p.number + ' · ' + p.chapters;
    $('#wbTitle').textContent = p.title;
    $('#wbBlurb').textContent = p.blurb;
    var stats = $('#wbStats');
    stats.innerHTML = '';
    function stat(n, label) { stats.appendChild(el('div', 'wb-stat', '<b>' + n + '</b><span>' + label + '</span>')); }
    stat(p.range, 'when');
    if ((p.scenes || []).length) {
      stat(p.scenes.length, 'scenes');
      stat(idx.order.length, 'characters');
      stat(p.scenes.filter(function (s) { return s.pivotal; }).length, 'pivotal turns');
      stat(uniquePlaces(p).length, 'places');
    } else {
      stat((p.outline || []).length, 'chapters');
      stat('Outline', 'status');
    }
  }
  function uniquePlaces(p) {
    var seen = [], out = [];
    (p.scenes || []).forEach(function (s) { if (seen.indexOf(s.placeShort) < 0) { seen.push(s.placeShort); out.push(s.placeShort); } });
    return out;
  }

  function renderToolbar() {
    var p = part(), has = (p.scenes || []).length > 0;
    var bar = $('#wbToolbar');
    bar.innerHTML = '';
    if (!has) { bar.classList.add('wb-hidden'); return; }
    bar.classList.remove('wb-hidden');

    var views = el('div', 'wb-views');
    views.setAttribute('role', 'tablist');
    [['chart', 'Chart'], ['story', 'Story'], ['cast', 'Cast'], ['table', 'Table']].forEach(function (v) {
      var b = el('button', 'wb-view', v[1]);
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', state.view === v[0] ? 'true' : 'false');
      b.addEventListener('click', function () { go({ view: v[0], panel: null }); });
      views.appendChild(b);
    });
    bar.appendChild(views);

    if (state.view === 'chart' || state.view === 'cast') {
      var facs = el('div', 'wb-facs');
      WAUBUN_FACTIONS.forEach(function (f) {
        var on = state.factions.indexOf(f.id) >= 0;
        var b = el('button', 'wb-fac', '<span class="wb-swatch"></span>' + esc(f.short));
        b.type = 'button';
        b.style.setProperty('--c', 'var(--f-' + f.id + ')');
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
        b.addEventListener('click', function () {
          var next = state.factions.slice(), i = next.indexOf(f.id);
          if (i >= 0) { if (next.length > 1) next.splice(i, 1); } else next.push(f.id);
          go({ factions: next }, true);
        });
        facs.appendChild(b);
      });
      bar.appendChild(facs);

      var search = el('input', 'wb-search');
      search.type = 'search';
      search.placeholder = 'Find a character…';
      search.value = state.query;
      search.addEventListener('input', function () {
        go({ query: search.value }, true);
        var fresh = $('.wb-search');
        if (fresh) { fresh.focus(); fresh.setSelectionRange(fresh.value.length, fresh.value.length); }
      });
      bar.appendChild(search);
    }
    if (state.view === 'chart') {
      var piv = el('button', 'wb-toggle', '★ Pivotal scenes only');
      piv.type = 'button';
      piv.setAttribute('aria-pressed', state.pivotalOnly ? 'true' : 'false');
      piv.addEventListener('click', function () { go({ pivotalOnly: !state.pivotalOnly }, true); });
      bar.appendChild(piv);
    }
  }

  /* ---------------- view: the presence chart ---------------- */
  function renderChart(host) {
    var p = part(), idx = INDEX[p.id];
    var scenes = visibleScenes();
    var chars = visibleChars();

    var fig = el('figure', 'wb-figure wb-chartwrap');
    fig.id = 'wbChartWrap';
    fig.appendChild(chartTools(scenes.length, chars.length));
    fig.appendChild(el('figcaption', 'wb-figtitle', 'Who appears, scene by scene'));
    fig.appendChild(el('p', 'wb-fignote',
      'Every character in Part ' + p.number + ' against every scene, in the order the narrative tells them. ' +
      'A filled mark means the character is present; a ringed mark is their first appearance; a dashed mark means they are spoken of, remembered, or acting at a distance. ' +
      'The faint line is the span between a character\'s first and last appearance.'));

    var legend = el('div', 'wb-legend');
    legend.innerHTML =
      '<span><i class="wb-key"></i>present in the scene</span>' +
      '<span><i class="wb-key first"></i>first appearance</span>' +
      '<span><i class="wb-key ghost"></i>spoken of, not present</span>' +
      '<span>★ pivotal plot point</span>';
    fig.appendChild(legend);
    fig.appendChild(selectionBar(scenes, chars));

    if (!scenes.length || !chars.length) {
      fig.appendChild(el('p', 'wb-empty', 'No scenes match the current filters.'));
      host.appendChild(fig);
      return;
    }

    var scroll = el('div', 'wb-scroll');
    var grid = el('div', 'wb-grid');
    grid.style.gridTemplateColumns = 'var(--namew) repeat(' + scenes.length + ', var(--cellw))';
    var anySel = state.selected.length > 0;

    // row 1 — act bands
    var corner = el('div', 'wb-corner');
    corner.style.gridRow = '1'; corner.style.gridColumn = '1'; corner.style.height = '44px';
    grid.appendChild(corner);
    var col = 2;
    p.acts.forEach(function (act) {
      var n = scenes.filter(function (s) { return s.act === act.id; }).length;
      if (!n) return;
      var band = el('div', 'wb-actband', '<b>' + esc(act.title) + '</b><em>' + esc(act.sub) + '</em>');
      band.style.gridRow = '1';
      band.style.gridColumn = col + ' / span ' + n;
      band.style.height = '44px';
      band.title = act.title + ' — ' + act.sub + ' (' + act.note + ')';
      grid.appendChild(band);
      col += n;
    });

    // row 2 — scene headers
    var corner2 = el('div', 'wb-corner');
    corner2.style.gridRow = '2'; corner2.style.gridColumn = '1'; corner2.style.top = '44px';
    corner2.appendChild(el('div', '', '<span style="display:block;padding:8px 10px;font-size:10.5px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase;color:var(--text-3)">Character ↓ &nbsp; Scene →</span>'));
    grid.appendChild(corner2);
    scenes.forEach(function (sc, c) {
      var sel = isSelected(sc.id);
      var h = el('div', 'wb-colhead' + (sc.pivotal ? ' pivotal' : '') + (sel ? ' sel' : '') + (anySel && !sel ? ' dim' : ''));
      h.style.gridRow = '2'; h.style.gridColumn = (c + 2);
      h.dataset.col = String(c);
      h.tabIndex = 0;
      h.setAttribute('role', 'button');
      h.setAttribute('aria-pressed', sel ? 'true' : 'false');
      h.appendChild(el('div', '', '<b>' + (sceneNo(sc.id) + 1) + '. ' + esc(sc.title) + '</b> <span>' + esc(sc.placeShort) + '</span>'));
      h.title = sc.title + ' — ' + sc.place + '\nClick to select · double-click to open';
      bindPick(h, sc.id);
      h.addEventListener('mouseenter', function () { highlight(null, c); });
      h.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleScene(sc.id); }
      });
      grid.appendChild(h);
    });

    // body rows
    var row = 3;
    FAC_ORDER.forEach(function (fid) {
      var members = chars.filter(function (id) { return CH[id].faction === fid; });
      if (!members.length) return;
      var gh = el('div', 'wb-grouphead', '<span class="wb-swatch" style="--c:var(--f-' + fid + ')"></span>' + esc(FAC[fid].name));
      gh.style.gridRow = String(row); gh.style.gridColumn = '1';
      grid.appendChild(gh);
      var filler = el('div', 'wb-grouprow');
      filler.style.gridRow = String(row); filler.style.gridColumn = '2 / span ' + scenes.length;
      grid.appendChild(filler);
      row++;

      members.forEach(function (id) {
        var c = CH[id], rec = idx.byChar[id], r = row++;
        var nm = el('div', 'wb-name', '<i></i><span>' + esc(c.name) + '</span>');
        nm.style.setProperty('--c', 'var(--f-' + fid + ')');
        nm.style.gridRow = String(r); nm.style.gridColumn = '1';
        nm.dataset.row = id;
        nm.title = c.name + (c.alias ? ' (' + c.alias + ')' : '') + ' — ' + c.role;
        nm.addEventListener('click', function () { go({ panel: { kind: 'character', id: id } }); });
        nm.addEventListener('mouseenter', function () { highlight(id, null); });
        grid.appendChild(nm);

        scenes.forEach(function (sc, cIdx) {
          var i = sceneNo(sc.id);
          var kind = rec.at[i];
          var sel = isSelected(sc.id);
          var inRange = rec.first !== null && i >= rec.first && i <= rec.last;
          var cell = el('div', 'wb-cell ' + (kind === 'on' ? 'present' : kind === 'men' ? 'mention' : 'empty') +
            (kind === 'on' && i === rec.first ? ' first' : '') + (sel ? ' sel' : '') + (anySel && !sel ? ' dim' : ''));
          cell.style.setProperty('--c', 'var(--f-' + fid + ')');
          cell.style.gridRow = String(r); cell.style.gridColumn = (cIdx + 2);
          cell.dataset.row = id; cell.dataset.col = String(cIdx);
          if (inRange) cell.appendChild(el('span', 'wb-arc'));
          cell.appendChild(el('span', 'wb-dot'));
          if (kind) {
            bindPick(cell, sc.id);
            cell.addEventListener('mouseenter', function (ev) {
              highlight(id, cIdx);
              tip(ev, '<b>' + esc(c.name) + '</b><em>' + (i === rec.first && kind === 'on' ? 'Enters the story · ' : '') +
                (kind === 'on' ? 'present' : 'spoken of') + '</em><br>' + (i + 1) + '. ' + esc(sc.title));
            });
            cell.addEventListener('mouseleave', hideTip);
          } else {
            cell.addEventListener('mouseenter', function () { highlight(id, cIdx); });
          }
          grid.appendChild(cell);
        });
      });
    });

    scroll.appendChild(grid);
    scroll.addEventListener('mouseleave', function () { highlight(null, null); hideTip(); });
    fig.appendChild(scroll);
    host.appendChild(fig);

    // the ground it covers
    var places = [];
    scenes.forEach(function (s) {
      var last = places[places.length - 1];
      if (last && last.name === s.placeShort) last.n++;
      else places.push({ name: s.placeShort, n: 1, scene: s.id });
    });
    var strip = el('div', 'wb-figure');
    strip.appendChild(el('div', 'wb-subhead', 'The ground it covers'));
    var row2 = el('div', 'wb-cast');
    places.forEach(function (pl) {
      var b = el('button', 'wb-person', esc(pl.name) + ' <em style="color:var(--text-3)">' + pl.n + ' scene' + (pl.n === 1 ? '' : 's') + '</em>');
      b.type = 'button';
      b.addEventListener('click', function () { go({ panel: { kind: 'scene', id: pl.scene } }); });
      row2.appendChild(b);
    });
    strip.appendChild(row2);
    host.appendChild(strip);
    applySize();
  }

  /* ---- size & full screen -------------------------------------------------
     The chart is a grid of --cell-sized squares, so zooming is one variable.
     "Fit width" puts every scene on screen and lets the rows scroll; "Fit all"
     squeezes both axes until the whole thing is in view at once, which is what
     full screen is for. Names and marks scale with the cell so nothing has to
     be re-laid-out. */
  var MINCELL = 5, MAXCELL = 34;
  function applySize() {
    var wrap = $('#wbChartWrap');
    if (!wrap) return;
    // below this the vertical scene labels and the names cannot be read at all,
    // so the chart drops to an overview: thin header, colour-chip rows, tooltips
    var TINY = 9;
    var cw = state.cell, ch = state.cell, nameW = 210;
    var cols = visibleScenes().length, rows = visibleChars().length;
    var groups = 0, vis = visibleChars();
    FAC_ORDER.forEach(function (fid) {
      if (vis.some(function (id) { return CH[id].faction === fid; })) groups++;
    });
    var scroll = $('.wb-scroll');
    if (state.fit !== 'none' && cols) {
      var availW = (scroll ? scroll.clientWidth : wrap.clientWidth) - 2;
      var guess = Math.floor((availW - 96) / cols);
      if (state.fit === 'all' && guess < TINY) nameW = 44;
      cw = Math.max(MINCELL, Math.min(MAXCELL, Math.floor((availW - nameW) / cols)));
      ch = cw;
      if (state.fit === 'all') {
        // act band + scene labels (or a thin band when they cannot be read)
        // plus one line per faction heading
        var chromeH = 44 + (cw < TINY ? 26 : 152) + groups * 30 + 8;
        var top = scroll ? scroll.getBoundingClientRect().top : 0;
        var availH = (isFullscreen() ? window.innerHeight - 24
                                     : window.innerHeight - Math.max(0, top) - 24) - chromeH;
        // rows and columns are sized independently — squeezing the height must
        // not also squeeze the width, or the chart shrinks into a corner
        ch = Math.max(MINCELL, Math.min(MAXCELL, Math.floor(availH / Math.max(1, rows))));
      }
    }
    paint(cw, ch, nameW);
    if (state.fit === 'all' && scroll) {
      for (var i = 0; i < 5 && ch > MINCELL; i++) {
        if (scroll.scrollHeight <= scroll.clientHeight + 1) break;
        ch = Math.max(MINCELL, ch - 1);
        paint(cw, ch, nameW);
        scroll.getBoundingClientRect();   // force reflow before re-measuring
      }
    }
    function paint(w, h, nw) {
      // columns and rows go "too small to letter" independently
      wrap.classList.toggle('wb-tinycols', w < TINY);
      wrap.classList.toggle('wb-tinyrows', h < TINY);
      wrap.style.setProperty('--cellw', w + 'px');
      wrap.style.setProperty('--cellh', h + 'px');
      wrap.style.setProperty('--namew', nw + 'px');
      wrap.style.setProperty('--namefs', Math.max(6.5, Math.min(12, h * 0.62)) + 'px');
      wrap.style.setProperty('--dot', Math.max(3, Math.min(12, Math.round(Math.min(w, h) * 0.55))) + 'px');
      var sc = $('.wb-scroll');
      if (sc) sc.style.maxHeight = (isFullscreen() || state.fit === 'all') ? 'calc(100vh - 132px)' : '78vh';
    }
  }

  function isFullscreen() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement);
  }
  function toggleFullscreen() {
    var wrap = $('#wbChartWrap');
    if (!wrap) return;
    if (isFullscreen()) {
      (document.exitFullscreen || document.webkitExitFullscreen).call(document);
    } else {
      var req = wrap.requestFullscreen || wrap.webkitRequestFullscreen;
      if (req) req.call(wrap);
      else { state.fit = 'all'; applySize(); }   // no API (older iOS): fit instead
    }
  }
  function chartTools(nCols, nRows) {
    var bar = el('div', 'wb-charttools');
    bar.appendChild(el('span', 'wb-toolnote', nRows + ' characters × ' + nCols + ' scenes'));
    function btn(label, title, fn, pressed) {
      var b = el('button', 'wb-toggle', label);
      b.type = 'button'; b.title = title;
      if (pressed !== undefined) b.setAttribute('aria-pressed', pressed ? 'true' : 'false');
      b.addEventListener('click', fn);
      bar.appendChild(b);
      return b;
    }
    btn('Fit width', 'Shrink the columns until every scene is on screen', function () {
      state.fit = state.fit === 'width' ? 'none' : 'width'; applySize(); syncTools();
    }, state.fit === 'width');
    btn('Fit all', 'Shrink both axes until the whole chart is on screen at once', function () {
      state.fit = state.fit === 'all' ? 'none' : 'all'; applySize(); syncTools();
    }, state.fit === 'all');
    btn('−', 'Smaller', function () {
      state.fit = 'none'; state.cell = Math.max(MINCELL, state.cell - 3); applySize(); syncTools();
    });
    btn('+', 'Bigger', function () {
      state.fit = 'none'; state.cell = Math.min(MAXCELL, state.cell + 3); applySize(); syncTools();
    });
    btn(isFullscreen() ? '✕ Exit full screen' : '⛶ Full screen',
      'Give the chart the whole screen', toggleFullscreen);
    return bar;
  }
  function syncTools() {
    var bar = $('.wb-charttools');
    if (!bar) return;
    var b = bar.querySelectorAll('.wb-toggle');
    b[0].setAttribute('aria-pressed', state.fit === 'width' ? 'true' : 'false');
    b[1].setAttribute('aria-pressed', state.fit === 'all' ? 'true' : 'false');
    b[4].textContent = isFullscreen() ? '✕ Exit full screen' : '⛶ Full screen';
  }

  // one click selects, two opens — a short timer keeps the two apart
  function bindPick(node, sceneId) {
    var timer = null;
    node.addEventListener('click', function () {
      if (timer) return;
      timer = setTimeout(function () { timer = null; toggleScene(sceneId); }, 230);
    });
    node.addEventListener('dblclick', function (e) {
      e.preventDefault();
      if (timer) { clearTimeout(timer); timer = null; }
      go({ panel: { kind: 'scene', id: sceneId } });
    });
  }
  function toggleScene(id) {
    var next = state.selected.slice(), i = next.indexOf(id);
    if (i >= 0) next.splice(i, 1); else next.push(id);
    next.sort(function (a, b) { return sceneNo(a) - sceneNo(b); });
    go({ selected: next });
  }

  function selectionBar(scenes, chars) {
    var wrap = el('div', 'wb-selbar');
    var sel = state.selected.filter(function (id) { return sceneById(id); });
    if (!sel.length) {
      wrap.classList.add('hint');
      wrap.innerHTML = '<span class="wb-selhint"><b>Click</b> a scene to focus it — the other scenes fade and the chart keeps only the people in it. ' +
        'Click more scenes to build a set. <b>Double-click</b> opens a scene; clicking a name opens that character.</span>';
      return wrap;
    }
    var idx = INDEX[state.part];
    var present = {}, spoken = {};
    sel.forEach(function (id) {
      var sc = sceneById(id);
      (sc.cast || []).forEach(function (c) { present[c] = true; });
      (sc.offstage || []).forEach(function (c) { if (!present[c]) spoken[c] = true; });
    });
    var head = el('div', 'wb-selhead');
    head.innerHTML = '<b>' + sel.length + ' scene' + (sel.length === 1 ? '' : 's') + ' selected</b>' +
      '<span>' + Object.keys(present).length + (Object.keys(present).length === 1 ? ' appears' : ' appear') +
      ' · ' + Object.keys(spoken).length + ' spoken of · ' +
      chars.length + ' row' + (chars.length === 1 ? '' : 's') + ' shown</span>';
    wrap.appendChild(head);

    var chips = el('div', 'wb-selchips');
    sel.forEach(function (id) {
      var sc = sceneById(id), n = sceneNo(id) + 1;
      var chip = el('div', 'wb-selchip');
      var open = el('button', 'wb-selopen', '<b>' + n + '</b>' + esc(sc.title) + (sc.pivotal ? ' <em>★</em>' : ''));
      open.type = 'button';
      open.title = 'Open the detail for this scene';
      open.addEventListener('click', function () { go({ panel: { kind: 'scene', id: id } }); });
      var drop = el('button', 'wb-seldrop', '✕');
      drop.type = 'button';
      drop.setAttribute('aria-label', 'Remove scene ' + n + ' from the selection');
      drop.addEventListener('click', function () { toggleScene(id); });
      chip.appendChild(open); chip.appendChild(drop);
      chips.appendChild(chip);
    });
    wrap.appendChild(chips);

    var acts = el('div', 'wb-selacts');
    var read = el('button', 'wb-btn primary', sel.length === 1 ? 'Read this scene →' : 'Read from scene ' + (sceneNo(sel[0]) + 1) + ' →');
    read.type = 'button';
    read.addEventListener('click', function () { go({ view: 'story', scene: sel[0], panel: null }); });
    acts.appendChild(read);
    if (sel.length === 1) {
      var det = el('button', 'wb-btn', 'Open details');
      det.type = 'button';
      det.addEventListener('click', function () { go({ panel: { kind: 'scene', id: sel[0] } }); });
      acts.appendChild(det);
    }
    var clr = el('button', 'wb-btn', 'Clear selection');
    clr.type = 'button';
    clr.addEventListener('click', function () { go({ selected: [] }); });
    acts.appendChild(clr);
    wrap.appendChild(acts);
    return wrap;
  }

  function highlight(rowId, colIdx) {
    var grid = $('.wb-grid');
    if (!grid) return;
    Array.prototype.forEach.call(grid.querySelectorAll('.rowon, .colon, .on'), function (n) {
      n.classList.remove('rowon', 'colon', 'on');
    });
    if (rowId) {
      Array.prototype.forEach.call(grid.querySelectorAll('[data-row="' + rowId + '"]'), function (n) {
        n.classList.add(n.classList.contains('wb-name') ? 'on' : 'rowon');
      });
    }
    if (colIdx !== null && colIdx !== undefined) {
      Array.prototype.forEach.call(grid.querySelectorAll('[data-col="' + colIdx + '"]'), function (n) {
        n.classList.add(n.classList.contains('wb-colhead') ? 'on' : 'colon');
      });
    }
  }

  var tipEl;
  function tip(ev, html) {
    if (!tipEl) { tipEl = el('div', 'wb-tip'); document.body.appendChild(tipEl); }
    tipEl.innerHTML = html;
    tipEl.classList.add('on');
    var x = ev.clientX + 14, y = ev.clientY + 14;
    var w = 270, h = tipEl.offsetHeight || 60;
    if (x + w > window.innerWidth) x = ev.clientX - w - 8;
    if (y + h > window.innerHeight) y = ev.clientY - h - 8;
    tipEl.style.left = x + 'px'; tipEl.style.top = y + 'px';
  }
  function hideTip() { if (tipEl) tipEl.classList.remove('on'); }

  /* ---------------- view: the story reader ---------------- */
  function renderStory(host) {
    var p = part(), scenes = p.scenes;
    if (!state.scene || sceneNo(state.scene) < 0) state.scene = scenes[0].id;
    var pos = sceneNo(state.scene), sc = scenes[pos];

    var wrap = el('div', 'wb-reader');
    var rail = el('nav', 'wb-rail');
    rail.setAttribute('aria-label', 'Scenes');
    p.acts.forEach(function (act) {
      var inAct = scenes.filter(function (s) { return s.act === act.id; });
      if (!inAct.length) return;
      rail.appendChild(el('div', 'wb-railact', act.title + ' · ' + act.sub));
      inAct.forEach(function (s) {
        var i = scenes.indexOf(s);
        var b = el('button', 'wb-railitem', '<b>' + (i + 1) + '</b>' + esc(s.title) + (s.pivotal ? ' ★' : ''));
        b.type = 'button';
        if (s.id === sc.id) b.setAttribute('aria-current', 'true');
        b.addEventListener('click', function () { go({ scene: s.id }); scrollToPage(); });
        rail.appendChild(b);
      });
    });
    wrap.appendChild(rail);

    var page = el('article', 'wb-page');
    page.id = 'wbPage';
    page.innerHTML = sceneHead(sc, pos);
    page.appendChild(modeSwitch(sc));
    page.appendChild(bodyForMode(sc));

    var nav = el('div', 'wb-pagenav');
    var prev = el('button', 'wb-btn', '← Previous');
    prev.type = 'button'; prev.disabled = pos === 0;
    prev.addEventListener('click', function () { go({ scene: scenes[pos - 1].id }); scrollToPage(); });
    var next = el('button', 'wb-btn primary', 'Next scene →');
    next.type = 'button'; next.disabled = pos === scenes.length - 1;
    next.addEventListener('click', function () { go({ scene: scenes[pos + 1].id }); scrollToPage(); });
    var prog = el('div', 'wb-progress', '<i style="width:' + Math.round(((pos + 1) / scenes.length) * 100) + '%"></i>');
    nav.appendChild(prev); nav.appendChild(prog); nav.appendChild(next);
    page.appendChild(nav);

    wrap.appendChild(page);
    host.appendChild(wrap);
    wireCast(page);
  }

  function modeSwitch(sc) {
    var box = el('div', 'wb-modes');
    var seg = el('div', 'wb-views');
    seg.setAttribute('role', 'tablist');
    seg.setAttribute('aria-label', 'How to read this scene');
    MODES.forEach(function (m) {
      var b = el('button', 'wb-view', m.label);
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', state.mode === m.id ? 'true' : 'false');
      b.title = m.note;
      b.addEventListener('click', function () {
        try { localStorage.setItem('waubun.mode', m.id); } catch (e) {}
        if (m.id === 'summary') return go({ mode: m.id });
        ensureText(function () { go({ mode: m.id }); });
        if (textState === 'loading') { state.mode = m.id; render(); }
      });
      seg.appendChild(b);
    });
    box.appendChild(seg);
    var note = MODES.filter(function (m) { return m.id === state.mode; })[0];
    box.appendChild(el('span', 'wb-modenote', note ? note.note : ''));
    return box;
  }

  function bodyForMode(sc) {
    var box = el('div');
    if (state.mode === 'summary') {
      box.innerHTML = summaryHTML(sc);
      return box;
    }
    if (state.part !== 'part1') {
      box.appendChild(el('div', 'wb-note', 'The full text is wired up for Part 1 so far. Summaries are available for every part that has scenes.'));
      box.innerHTML += summaryHTML(sc);
      return box;
    }
    if (textState === 'loading' || (textState === 'idle' && !window.WAUBUN_TEXT_PART1)) {
      ensureText(function () { render(); });
      box.appendChild(el('div', 'wb-note', 'Fetching the text…'));
      return box;
    }
    var paras = passage(sc.id, state.mode);
    if (!paras || !paras.length) {
      box.appendChild(el('div', 'wb-note', 'The text for this scene could not be loaded. The summary is below.'));
      box.innerHTML += summaryHTML(sc);
      return box;
    }
    var words = paras.join(' ').split(/\s+/).length;
    var pr = el('div', 'wb-prose wb-fulltext');
    pr.innerHTML = paras.map(function (t) { return '<p>' + esc(t) + '</p>'; }).join('');
    box.appendChild(pr);
    var store = window.WAUBUN_TEXT_PART1;
    var isRetold = !!(store && store[sc.id] && store[sc.id].retold);
    box.appendChild(el('div', 'wb-source',
      (state.mode === 'original'
        ? 'Chapter ' + esc(sc.chapter) + ' of the 1856 first edition — Juliette Kinzie\'s own words, unaltered.'
        : 'Chapter ' + esc(sc.chapter) + (isRetold
            ? ', retold in a plain modern voice — every event, name and detail of the original kept.'
            : ', in an earlier, lighter modernization. The full rewrite is working through the part scene by scene.')) +
      ' ' + words.toLocaleString() + ' words.'));
    var more = el('details', 'wb-details');
    more.appendChild(el('summary', '', 'Summary, plot points and cast'));
    more.appendChild(el('div', '', summaryHTML(sc)));
    box.appendChild(more);
    return box;
  }

  function scrollToPage() {
    var n = document.getElementById('wbPage');
    if (n && n.getBoundingClientRect().top < 0) n.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /* ---------------- shared: scene rendering ---------------- */
  function sceneHead(sc, pos) {
    var p = part();
    return '<div class="wb-meta">' +
      '<span class="wb-chip">Scene ' + (pos + 1) + ' of ' + p.scenes.length + '</span>' +
      '<span class="wb-chip">Chapter ' + esc(sc.chapter) + ' · ' + esc(sc.chapterTitle) + '</span>' +
      '<span class="wb-chip">' + esc(sc.place) + '</span>' +
      (sc.pivotal ? '<span class="wb-chip pivot">★ Pivotal</span>' : '') +
      '</div>' +
      '<div class="wb-when">' + esc(sc.date) + '</div>' +
      '<h2>' + esc(sc.title) + '</h2>';
  }

  function summaryHTML(sc) {
    var p = part(), idx = INDEX[p.id];
    var h = '<div class="wb-prose" style="margin-top:14px">' + esc(sc.summary) + '</div>';
    if (sc.points && sc.points.length) {
      h += '<div class="wb-subhead">Plot points</div><ul class="wb-points">' +
        sc.points.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>';
    }
    return h + castHTML(sc, idx, p);
  }

  function castHTML(sc, idx, p) {
    var i = p.scenes.indexOf(sc);
    var enters = [], exits = [];
    (sc.cast || []).forEach(function (id) {
      var rec = idx.byChar[id];
      if (!rec) return;
      if (rec.first === i) enters.push(id);
      if (rec.last === i && rec.present.length > 1) exits.push(id);
    });
    var h = '<div class="wb-subhead">Who is in this scene</div>';
    FAC_ORDER.forEach(function (fid) {
      var members = (sc.cast || []).filter(function (id) { return CH[id] && CH[id].faction === fid; });
      if (!members.length) return;
      h += '<div class="wb-castrow"><div>' + esc(FAC[fid].name) + '</div><div class="wb-cast">' +
        members.map(function (id) { return personHTML(id, enters.indexOf(id) >= 0 ? 'in' : (exits.indexOf(id) >= 0 ? 'out' : ''), false); }).join('') +
        '</div></div>';
    });
    if ((sc.offstage || []).length) {
      h += '<div class="wb-subhead">Spoken of, not present</div><div class="wb-cast">' +
        sc.offstage.map(function (id) { return personHTML(id, '', true); }).join('') + '</div>';
    }
    return h;
  }

  function personHTML(id, badge, ghost) {
    var c = CH[id];
    if (!c) return '';
    var b = badge === 'in' ? '<em class="in">enters</em>' : badge === 'out' ? '<em class="out">last seen</em>' : '';
    return '<button type="button" class="wb-person' + (ghost ? ' ghost' : '') + '" data-person="' + id + '" ' +
      'style="--c:var(--f-' + c.faction + ')"><i></i>' + esc(c.name) + b + '</button>';
  }

  function wireCast(root) {
    Array.prototype.forEach.call(root.querySelectorAll('[data-person]'), function (b) {
      b.addEventListener('click', function () { go({ panel: { kind: 'character', id: b.dataset.person } }); });
    });
    Array.prototype.forEach.call(root.querySelectorAll('[data-scene]'), function (b) {
      b.addEventListener('click', function () { go({ panel: { kind: 'scene', id: b.dataset.scene } }); });
    });
  }

  /* ---------------- view: cast ---------------- */
  function renderCast(host) {
    var p = part(), idx = INDEX[p.id];
    var chars = visibleChars();
    var fig = el('div', 'wb-figure');
    fig.appendChild(el('div', 'wb-fignote',
      'Everyone Part ' + p.number + ' puts on the page — ' + idx.order.length + ' named people and groups. ' +
      'The bar under each card is their run through the ' + p.scenes.length + ' scenes: solid where they are present, faint where they are only spoken of.'));
    host.appendChild(fig);

    FAC_ORDER.forEach(function (fid) {
      var members = chars.filter(function (id) { return CH[id].faction === fid; });
      if (!members.length) return;
      host.appendChild(el('div', 'wb-subhead', FAC[fid].name + ' · ' + members.length));
      var grid = el('div', 'wb-castgrid');
      members.forEach(function (id) {
        var c = CH[id], rec = idx.byChar[id];
        var card = el('button', 'wb-card');
        card.type = 'button';
        card.style.setProperty('--c', 'var(--f-' + fid + ')');
        var spark = p.scenes.map(function (s, i) {
          var k = rec.at[i];
          return '<i class="' + (k === 'on' ? 'on' : k === 'men' ? 'men' : '') + '"></i>';
        }).join('');
        var firstScene = rec.first !== null ? rec.first : rec.mentioned[0];
        card.innerHTML =
          '<h4>' + esc(c.name) + '</h4>' +
          (c.alias ? '<div class="wb-alias">' + esc(c.alias) + '</div>' : '') +
          '<div class="wb-role">' + esc(c.role) + '</div>' +
          '<p>' + esc(c.bio) + '</p>' +
          '<div class="wb-spark">' + spark + '</div>' +
          '<div class="wb-appear">' + (rec.present.length
            ? 'In ' + rec.present.length + ' scene' + (rec.present.length === 1 ? '' : 's') + ' · enters at scene ' + (firstScene + 1)
            : 'Spoken of in ' + rec.mentioned.length + ' scene' + (rec.mentioned.length === 1 ? '' : 's')) + '</div>';
        card.addEventListener('click', function () { go({ panel: { kind: 'character', id: id } }); });
        grid.appendChild(card);
      });
      host.appendChild(grid);
    });
    if (!chars.length) host.appendChild(el('p', 'wb-empty', 'Nobody matches the current filters.'));
  }

  /* ---------------- view: table ---------------- */
  function renderTable(host) {
    var p = part(), idx = INDEX[p.id];
    host.appendChild(el('div', 'wb-subhead', 'Scenes'));
    var w1 = el('div', 'wb-tablewrap');
    var t1 = el('table', 'wb-table');
    t1.innerHTML = '<caption class="wb-hidden">Every scene in Part ' + p.number + '</caption>' +
      '<thead><tr><th>#</th><th>Act</th><th>Chapter</th><th>Scene</th><th>Place</th><th>When</th><th>Present</th><th>Spoken of</th></tr></thead>';
    var tb = el('tbody');
    p.scenes.forEach(function (sc, i) {
      var act = p.acts.filter(function (a) { return a.id === sc.act; })[0] || { title: '' };
      var tr = el('tr');
      tr.innerHTML =
        '<td class="num">' + (i + 1) + (sc.pivotal ? ' ★' : '') + '</td>' +
        '<td>' + esc(act.title) + '</td>' +
        '<td>' + esc(sc.chapter) + '</td>' +
        '<td><b>' + esc(sc.title) + '</b></td>' +
        '<td>' + esc(sc.place) + '</td>' +
        '<td>' + esc(sc.date) + '</td>' +
        '<td>' + (sc.cast || []).map(function (id) { return esc(CH[id] ? CH[id].name : id); }).join(', ') + '</td>' +
        '<td>' + (sc.offstage || []).map(function (id) { return esc(CH[id] ? CH[id].name : id); }).join(', ') + '</td>';
      tr.style.cursor = 'pointer';
      tr.addEventListener('click', function () { go({ panel: { kind: 'scene', id: sc.id } }); });
      tb.appendChild(tr);
    });
    t1.appendChild(tb); w1.appendChild(t1); host.appendChild(w1);

    host.appendChild(el('div', 'wb-subhead', 'Characters'));
    var w2 = el('div', 'wb-tablewrap');
    var t2 = el('table', 'wb-table');
    t2.innerHTML = '<caption class="wb-hidden">Every character in Part ' + p.number + '</caption>' +
      '<thead><tr><th>Character</th><th>Also called</th><th>Group</th><th>Role</th><th>Enters</th><th>Last seen</th><th>Scenes</th></tr></thead>';
    var tb2 = el('tbody');
    idx.order.forEach(function (id) {
      var c = CH[id], rec = idx.byChar[id];
      var tr = el('tr');
      tr.innerHTML =
        '<td><b>' + esc(c.name) + '</b></td>' +
        '<td>' + esc(c.alias || '—') + '</td>' +
        '<td>' + esc(FAC[c.faction].short) + '</td>' +
        '<td>' + esc(c.role) + '</td>' +
        '<td class="num">' + (rec.first !== null ? rec.first + 1 : '—') + '</td>' +
        '<td class="num">' + (rec.last !== null ? rec.last + 1 : '—') + '</td>' +
        '<td class="num">' + rec.present.length + (rec.mentioned.length ? ' (+' + rec.mentioned.length + ' mentioned)' : '') + '</td>';
      tr.style.cursor = 'pointer';
      tr.addEventListener('click', function () { go({ panel: { kind: 'character', id: id } }); });
      tb2.appendChild(tr);
    });
    t2.appendChild(tb2); w2.appendChild(t2); host.appendChild(w2);
  }

  /* ---------------- view: outline (parts 2 & 3) ---------------- */
  function renderOutline(host) {
    var p = part();
    var box = el('div', 'wb-outline');
    box.appendChild(el('div', 'wb-note',
      'Part ' + p.number + ' is staged but not yet broken into scenes. The chapter spine below is the real one, ' +
      'exactly as the chapters stand in the narrative; the scene summaries, cast lists and the presence chart are built one part at a time, ' +
      'and Part 1 is complete. Open Part 1 to see the finished shape.'));
    var ol = el('ol');
    (p.outline || []).forEach(function (row) {
      ol.appendChild(el('li', '', '<b>CH. ' + esc(row.chapter) + '</b><span>' + esc(row.title) + '</span>'));
    });
    box.appendChild(ol);
    if ((p.leads || []).length) {
      box.appendChild(el('div', 'wb-subhead', 'Who this part belongs to'));
      var cast = el('div', 'wb-cast');
      cast.innerHTML = p.leads.map(function (id) { return personHTML(id, '', false); }).join('');
      box.appendChild(cast);
      wireCast(box);
    }
    host.appendChild(box);
  }

  /* ---------------- the detail panel ---------------- */
  function paintPanel() {
    var pn = $('#wbPanel'), body = $('#wbPanelBody');
    if (!state.panel) {
      pn.classList.remove('open');
      $('#wbScrim').classList.remove('open');
      pn.setAttribute('aria-hidden', 'true');
      return;
    }
    var title = '', html = '', after = null;
    if (state.panel.kind === 'scene') {
      var sc = sceneById(state.panel.id);
      if (!sc) { state.panel = null; return paintPanel(); }
      var pos = sceneNo(sc.id);
      title = sc.title;
      html = '<div class="wb-meta">' +
        '<span class="wb-chip">Scene ' + (pos + 1) + ' of ' + part().scenes.length + '</span>' +
        '<span class="wb-chip">Chapter ' + esc(sc.chapter) + ' · ' + esc(sc.chapterTitle) + '</span>' +
        '<span class="wb-chip">' + esc(sc.place) + '</span>' +
        (sc.pivotal ? '<span class="wb-chip pivot">★ Pivotal</span>' : '') +
        '</div><div class="wb-when">' + esc(sc.date) + '</div>' + summaryHTML(sc);
      after = function (b) {
        var acts = el('div', 'wb-panelacts');
        MODES.forEach(function (m) {
          var btn = el('button', 'wb-btn' + (m.id === 'summary' ? '' : ' primary'),
            m.id === 'summary' ? 'Read scene ' + (pos + 1) + ' →' : (m.id === 'modern' ? 'Full text →' : 'Original 1856 →'));
          btn.type = 'button';
          btn.title = m.note;
          btn.addEventListener('click', function () {
            try { localStorage.setItem('waubun.mode', m.id); } catch (e) {}
            if (m.id === 'summary') return go({ view: 'story', scene: sc.id, mode: 'summary', panel: null });
            ensureText(function () { go({ view: 'story', scene: sc.id, mode: m.id, panel: null }); });
          });
          acts.appendChild(btn);
        });
        var sel = el('button', 'wb-btn', isSelected(sc.id) ? 'Remove from selection' : 'Add to selection');
        sel.type = 'button';
        sel.addEventListener('click', function () { toggleScene(sc.id); });
        acts.appendChild(sel);
        b.appendChild(acts);
        b.appendChild(el('p', 'wb-backhint', 'The browser Back button returns you here.'));
      };
    } else {
      var c = CH[state.panel.id];
      if (!c) { state.panel = null; return paintPanel(); }
      var p = part(), idx = INDEX[p.id], rec = idx.byChar[state.panel.id];
      title = c.name;
      html = '<div class="wb-meta">' +
        '<span class="wb-chip" style="border-color:var(--f-' + c.faction + ');color:var(--f-' + c.faction + ')">' + esc(FAC[c.faction].name) + '</span>' +
        '<span class="wb-chip">' + esc(c.role) + '</span></div>';
      if (c.alias) html += '<div class="wb-when">also called ' + esc(c.alias) + '</div>';
      html += '<div class="wb-prose" style="margin-top:12px">' + esc(c.bio) + '</div>';
      if (rec) {
        html += '<div class="wb-subhead">Their run through Part ' + p.number + '</div><div class="wb-cast">';
        var seen = {};
        rec.present.forEach(function (i) { seen[i] = 'on'; });
        rec.mentioned.forEach(function (i) { if (!seen[i]) seen[i] = 'men'; });
        Object.keys(seen).map(Number).sort(function (a, b) { return a - b; }).forEach(function (i) {
          var s2 = p.scenes[i];
          html += '<button type="button" class="wb-person' + (seen[i] === 'men' ? ' ghost' : '') + '" data-scene="' + s2.id + '" ' +
            'style="--c:var(--f-' + c.faction + ')"><i></i>' + (i + 1) + '. ' + esc(s2.title) +
            (i === rec.first && rec.present.length ? '<em class="in">enters</em>' : '') + '</button>';
        });
        html += '</div>';
        after = function (b) {
          var acts = el('div', 'wb-panelacts');
          var only = el('button', 'wb-btn primary', 'Show only their scenes');
          only.type = 'button';
          only.addEventListener('click', function () {
            var ids = Object.keys(seen).map(Number).sort(function (a, b) { return a - b; })
              .map(function (i) { return p.scenes[i].id; });
            go({ view: 'chart', selected: ids, panel: null });
          });
          acts.appendChild(only);
          b.appendChild(acts);
        };
      } else {
        html += '<div class="wb-note" style="margin-top:18px">Does not appear in Part ' + p.number + '.</div>';
      }
    }
    $('#wbPanelTitle').textContent = title;
    body.innerHTML = html;
    wireCast(body);
    if (after) after(body);
    pn.classList.add('open');
    pn.setAttribute('aria-hidden', 'false');
    $('#wbScrim').classList.add('open');
    pn.scrollTop = 0;
  }

  function closePanel() {
    if (!state.panel) return;
    if (pushed > 0) history.back();          // keeps Back/forward honest
    else go({ panel: null }, true);
  }

  /* ---------------- render ---------------- */
  function render() {
    renderParts();
    renderHead();
    renderToolbar();
    var host = $('#wbMain');
    host.innerHTML = '';
    var p = part();
    if (!(p.scenes || []).length) renderOutline(host);
    else if (state.view === 'chart') renderChart(host);
    else if (state.view === 'story') renderStory(host);
    else if (state.view === 'cast') renderCast(host);
    else renderTable(host);
    paintPanel();
  }

  /* ---------------- boot ---------------- */
  function boot() {
    var root = document.documentElement, saved = null;
    try { saved = localStorage.getItem('custom.theme'); } catch (e) {}
    if (!saved && window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches) saved = 'dark';
    if (saved) root.setAttribute('data-theme', saved);
    var tbtn = $('#wbTheme');
    function paintTheme() { tbtn.textContent = root.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙'; }
    paintTheme();
    tbtn.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('custom.theme', next); } catch (e) {}
      paintTheme();
    });

    $('#wbPanelClose').addEventListener('click', closePanel);
    $('#wbScrim').addEventListener('click', closePanel);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { closePanel(); return; }
      if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
      if (state.view === 'story' && !state.panel) {
        var scenes = part().scenes || [], pos = sceneNo(state.scene);
        if (e.key === 'ArrowRight' && pos >= 0 && pos < scenes.length - 1) go({ scene: scenes[pos + 1].id });
        if (e.key === 'ArrowLeft' && pos > 0) go({ scene: scenes[pos - 1].id });
      }
    });

    ['fullscreenchange', 'webkitfullscreenchange'].forEach(function (ev) {
      document.addEventListener(ev, function () {
        document.body.classList.toggle('wb-isfs', isFullscreen());
        if (isFullscreen() && state.fit === 'none') state.fit = 'all';
        syncTools();
        // the element is not at its new size until after the next paint
        requestAnimationFrame(function () { requestAnimationFrame(applySize); });
        setTimeout(applySize, 120);
      });
    });
    var rt;
    window.addEventListener('resize', function () {
      clearTimeout(rt);
      rt = setTimeout(function () { if (state.fit !== 'none') applySize(); }, 120);
    });

    readHash();
    history.replaceState(snapshot(), '', hashFor());
    if (state.mode !== 'summary' && state.view === 'story') ensureText(function () { render(); });
    render();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
