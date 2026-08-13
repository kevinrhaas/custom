/* Wau-Bun — an interactive telling.
   No build step, no framework, no dependencies. Reads the data files loaded
   before it (WAUBUN_FACTIONS, WAUBUN_CHARACTERS, WAUBUN_PART1/2/3) and renders
   four views over the same model: the presence chart, the scene-by-scene
   reader, the cast, and a plain table.

   The model: a scene names who is present (`cast`) and who is spoken of
   (`offstage`). Everything else — first appearance, last appearance, arcs,
   counts, the "enters here" badges — is derived, never hand-maintained. */
(function () {
  'use strict';

  var PARTS = [WAUBUN_PART1, WAUBUN_PART2, WAUBUN_PART3];
  var FAC = {}, FAC_ORDER = WAUBUN_FACTIONS.map(function (f) { return f.id; });
  WAUBUN_FACTIONS.forEach(function (f) { FAC[f.id] = f; });
  var CH = {};
  WAUBUN_CHARACTERS.forEach(function (c) { CH[c.id] = c; });

  var state = {
    part: 'part1',
    view: 'chart',
    scene: null,          // scene id shown in the reader
    factions: FAC_ORDER.slice(),
    query: '',
    pivotalOnly: false
  };

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

  /* ---------------- derived model ---------------- */
  // For the active part: which characters appear, in which scenes, first & last.
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
    // stable order: faction block, then first appearance, then name
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
  function visibleChars() {
    var idx = INDEX[state.part], q = state.query.trim().toLowerCase();
    var scenes = visibleScenes(), keep = {};
    scenes.forEach(function (sc) { keep[sc.id] = true; });
    return idx.order.filter(function (id) {
      var c = CH[id], rec = idx.byChar[id];
      if (state.factions.indexOf(c.faction) < 0) return false;
      if (q && (c.name + ' ' + (c.alias || '') + ' ' + c.role).toLowerCase().indexOf(q) < 0) return false;
      // drop anyone with nothing to show under the current column filter
      var any = false;
      (part().scenes || []).forEach(function (sc, i) { if (keep[sc.id] && rec.at[i]) any = true; });
      return any;
    });
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
        state.part = p.id; state.scene = null;
        if (!(p.scenes || []).length && state.view !== 'chart') state.view = 'chart';
        render();
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
      b.addEventListener('click', function () { state.view = v[0]; render(); });
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
          var i = state.factions.indexOf(f.id);
          if (i >= 0) { if (state.factions.length > 1) state.factions.splice(i, 1); }
          else state.factions.push(f.id);
          render();
        });
        facs.appendChild(b);
      });
      bar.appendChild(facs);

      var search = el('input', 'wb-search');
      search.type = 'search';
      search.placeholder = 'Find a character…';
      search.value = state.query;
      search.addEventListener('input', function () {
        state.query = search.value;
        render();
        // the toolbar is rebuilt on every render — put the caret back where it was
        var fresh = $('.wb-search');
        if (fresh) { fresh.focus(); fresh.setSelectionRange(fresh.value.length, fresh.value.length); }
      });
      bar.appendChild(search);
    }
    if (state.view === 'chart') {
      var piv = el('button', 'wb-toggle', '★ Pivotal scenes only');
      piv.type = 'button';
      piv.setAttribute('aria-pressed', state.pivotalOnly ? 'true' : 'false');
      piv.addEventListener('click', function () { state.pivotalOnly = !state.pivotalOnly; render(); });
      bar.appendChild(piv);
    }
  }

  /* ---------------- view: the presence chart ---------------- */
  function renderChart(host) {
    var p = part(), idx = INDEX[p.id];
    var scenes = visibleScenes();
    var chars = visibleChars();
    var sceneIndexOf = {};
    (p.scenes || []).forEach(function (sc, i) { sceneIndexOf[sc.id] = i; });

    var fig = el('figure', 'wb-figure');
    fig.appendChild(el('figcaption', 'wb-figtitle', 'Who is on stage, scene by scene'));
    fig.appendChild(el('p', 'wb-fignote',
      'Every character in Part ' + p.number + ' against every scene, in the order the narrative tells them. ' +
      'A filled mark means the character is present; a ringed mark is their first appearance; a dashed mark means they are spoken of, remembered, or acting at a distance. ' +
      'The faint line is the span between a character\'s first and last appearance. Click any scene or name for the detail.'));

    var legend = el('div', 'wb-legend');
    legend.innerHTML =
      '<span><i class="wb-key"></i>present in the scene</span>' +
      '<span><i class="wb-key first"></i>first appearance</span>' +
      '<span><i class="wb-key ghost"></i>spoken of, not present</span>' +
      '<span>★ pivotal plot point</span>';
    fig.appendChild(legend);

    if (!scenes.length || !chars.length) {
      fig.appendChild(el('p', 'wb-empty', 'No scenes match the current filters.'));
      host.appendChild(fig);
      return;
    }

    var scroll = el('div', 'wb-scroll');
    var grid = el('div', 'wb-grid');
    grid.style.gridTemplateColumns = 'var(--namew) repeat(' + scenes.length + ', var(--cell))';

    // row 1 — act bands
    var corner = el('div', 'wb-corner');
    corner.style.gridRow = '1'; corner.style.gridColumn = '1';
    corner.style.height = '44px';
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
      var h = el('div', 'wb-colhead' + (sc.pivotal ? ' pivotal' : ''));
      h.style.gridRow = '2'; h.style.gridColumn = (c + 2);
      h.dataset.col = String(c);
      h.appendChild(el('div', '', '<b>' + (sceneIndexOf[sc.id] + 1) + '. ' + esc(sc.title) + '</b> <span>' + esc(sc.placeShort) + '</span>'));
      h.title = sc.title + ' — ' + sc.place;
      h.addEventListener('click', function () { openScene(sc.id); });
      h.addEventListener('mouseenter', function () { highlight(null, c); });
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
        nm.addEventListener('click', function () { openCharacter(id); });
        nm.addEventListener('mouseenter', function () { highlight(id, null); });
        grid.appendChild(nm);

        scenes.forEach(function (sc, cIdx) {
          var i = sceneIndexOf[sc.id];
          var kind = rec.at[i];
          var inRange = rec.first !== null && i >= rec.first && i <= rec.last;
          var cell = el('div', 'wb-cell ' + (kind === 'on' ? 'present' : kind === 'men' ? 'mention' : 'empty') +
            (kind === 'on' && i === rec.first ? ' first' : ''));
          cell.style.setProperty('--c', 'var(--f-' + fid + ')');
          cell.style.gridRow = String(r); cell.style.gridColumn = (cIdx + 2);
          cell.dataset.row = id; cell.dataset.col = String(cIdx);
          if (inRange) cell.appendChild(el('span', 'wb-arc'));
          cell.appendChild(el('span', 'wb-dot'));
          if (kind) {
            cell.addEventListener('click', function () { openScene(sc.id); });
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

    // journey strip — the season is a journey, so show the ground it covers
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
      b.addEventListener('click', function () { openScene(pl.scene); });
      row2.appendChild(b);
    });
    strip.appendChild(row2);
    host.appendChild(strip);
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
    if (!state.scene) state.scene = scenes[0].id;
    var pos = 0;
    scenes.forEach(function (s, i) { if (s.id === state.scene) pos = i; });
    var sc = scenes[pos];

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
        b.addEventListener('click', function () { state.scene = s.id; render(); scrollToPage(); });
        rail.appendChild(b);
      });
    });
    wrap.appendChild(rail);

    var page = el('article', 'wb-page');
    page.id = 'wbPage';
    page.innerHTML = sceneHTML(sc, pos, true);
    wireCast(page);

    var nav = el('div', 'wb-pagenav');
    var prev = el('button', 'wb-btn', '← Previous');
    prev.type = 'button'; prev.disabled = pos === 0;
    prev.addEventListener('click', function () { state.scene = scenes[pos - 1].id; render(); scrollToPage(); });
    var next = el('button', 'wb-btn primary', 'Next scene →');
    next.type = 'button'; next.disabled = pos === scenes.length - 1;
    next.addEventListener('click', function () { state.scene = scenes[pos + 1].id; render(); scrollToPage(); });
    var prog = el('div', 'wb-progress', '<i style="width:' + Math.round(((pos + 1) / scenes.length) * 100) + '%"></i>');
    nav.appendChild(prev);
    nav.appendChild(prog);
    nav.appendChild(next);
    page.appendChild(nav);

    wrap.appendChild(page);
    host.appendChild(wrap);
  }
  function scrollToPage() {
    var n = document.getElementById('wbPage');
    if (n && n.getBoundingClientRect().top < 0) n.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  /* ---------------- shared: scene rendering ---------------- */
  function sceneHTML(sc, pos, long) {
    var p = part(), idx = INDEX[p.id];
    var h = '';
    h += '<div class="wb-meta">' +
      '<span class="wb-chip">Scene ' + (pos + 1) + ' of ' + p.scenes.length + '</span>' +
      '<span class="wb-chip">Chapter ' + esc(sc.chapter) + ' · ' + esc(sc.chapterTitle) + '</span>' +
      '<span class="wb-chip">' + esc(sc.place) + '</span>' +
      (sc.pivotal ? '<span class="wb-chip pivot">★ Pivotal</span>' : '') +
      '</div>';
    h += '<div class="wb-when">' + esc(sc.date) + '</div>';
    // in the side panel the title already sits in the panel header
    if (long) h += '<h2>' + esc(sc.title) + '</h2>';
    h += '<div class="wb-prose" style="margin-top:14px">' + esc(sc.summary) + '</div>';
    if (sc.points && sc.points.length) {
      h += '<div class="wb-subhead">Plot points</div><ul class="wb-points">' +
        sc.points.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>';
    }
    h += castHTML(sc, idx, p);
    return h;
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
      b.addEventListener('click', function () { openCharacter(b.dataset.person); });
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
        card.addEventListener('click', function () { openCharacter(id); });
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
      tr.addEventListener('click', function () { openScene(sc.id); });
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
      tr.addEventListener('click', function () { openCharacter(id); });
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
      wireCast(cast);
      box.appendChild(cast);
    }
    host.appendChild(box);
  }

  /* ---------------- panel ---------------- */
  function openScene(id) {
    var p = part(), pos = -1;
    p.scenes.forEach(function (s, i) { if (s.id === id) pos = i; });
    if (pos < 0) return;
    var sc = p.scenes[pos];
    panel(sc.title, sceneHTML(sc, pos, false), function (body) {
      var read = el('button', 'wb-btn primary', 'Read this scene →');
      read.type = 'button';
      read.style.marginTop = '22px';
      read.addEventListener('click', function () { state.view = 'story'; state.scene = sc.id; closePanel(); render(); });
      body.appendChild(read);
    });
  }

  function openCharacter(id) {
    var c = CH[id];
    if (!c) return;
    var p = part(), idx = INDEX[p.id], rec = idx.byChar[id];
    var h = '<div class="wb-meta">' +
      '<span class="wb-chip" style="border-color:var(--f-' + c.faction + ');color:var(--f-' + c.faction + ')">' + esc(FAC[c.faction].name) + '</span>' +
      '<span class="wb-chip">' + esc(c.role) + '</span></div>';
    if (c.alias) h += '<div class="wb-when">also called ' + esc(c.alias) + '</div>';
    h += '<div class="wb-prose" style="margin-top:12px">' + esc(c.bio) + '</div>';
    if (rec) {
      h += '<div class="wb-subhead">Their run through Part ' + p.number + '</div>';
      h += '<div class="wb-cast">';
      var seen = {};
      rec.present.forEach(function (i) { seen[i] = 'on'; });
      rec.mentioned.forEach(function (i) { if (!seen[i]) seen[i] = 'men'; });
      Object.keys(seen).map(Number).sort(function (a, b) { return a - b; }).forEach(function (i) {
        var sc = p.scenes[i];
        h += '<button type="button" class="wb-person' + (seen[i] === 'men' ? ' ghost' : '') + '" data-scene="' + sc.id + '" ' +
          'style="--c:var(--f-' + c.faction + ')"><i></i>' + (i + 1) + '. ' + esc(sc.title) +
          (i === rec.first && rec.present.length ? '<em class="in">enters</em>' : '') + '</button>';
      });
      h += '</div>';
    } else {
      h += '<div class="wb-note" style="margin-top:18px">Does not appear in Part ' + p.number + '.</div>';
    }
    panel(c.name, h);
  }

  function panel(title, html, after) {
    var pn = $('#wbPanel'), body = $('#wbPanelBody');
    $('#wbPanelTitle').textContent = title;
    body.innerHTML = html;
    wireCast(body);
    Array.prototype.forEach.call(body.querySelectorAll('[data-scene]'), function (b) {
      b.addEventListener('click', function () { openScene(b.dataset.scene); });
    });
    if (after) after(body);
    pn.classList.add('open');
    $('#wbScrim').classList.add('open');
    pn.scrollTop = 0;
    $('#wbPanelClose').focus();
  }
  function closePanel() {
    $('#wbPanel').classList.remove('open');
    $('#wbScrim').classList.remove('open');
  }

  /* ---------------- render ---------------- */
  function render() {
    renderParts();
    renderHead();
    renderToolbar();
    var host = $('#wbMain');
    host.innerHTML = '';
    var p = part();
    if (!(p.scenes || []).length) { renderOutline(host); }
    else if (state.view === 'chart') renderChart(host);
    else if (state.view === 'story') renderStory(host);
    else if (state.view === 'cast') renderCast(host);
    else renderTable(host);
    writeHash();
  }

  function writeHash() {
    var h = '#/' + state.part + '/' + state.view + (state.view === 'story' && state.scene ? '/' + state.scene : '');
    if (location.hash !== h) history.replaceState(null, '', h);
  }
  function readHash() {
    var m = (location.hash || '').replace(/^#\//, '').split('/');
    if (m[0] && PARTS.some(function (p) { return p.id === m[0]; })) state.part = m[0];
    if (m[1] && ['chart', 'story', 'cast', 'table'].indexOf(m[1]) >= 0) state.view = m[1];
    if (m[2]) state.scene = m[2];
  }

  /* ---------------- boot ---------------- */
  function boot() {
    // theme, shared with the rest of the workshop site
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
      if (e.key === 'Escape') closePanel();
      if (state.view === 'story' && !$('#wbPanel').classList.contains('open')) {
        var p = part(), scenes = p.scenes || [], pos = -1;
        scenes.forEach(function (s, i) { if (s.id === state.scene) pos = i; });
        if (e.key === 'ArrowRight' && pos >= 0 && pos < scenes.length - 1) { state.scene = scenes[pos + 1].id; render(); }
        if (e.key === 'ArrowLeft' && pos > 0) { state.scene = scenes[pos - 1].id; render(); }
      }
    });

    readHash();
    render();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
