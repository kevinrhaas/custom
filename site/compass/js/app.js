/* Compass — passcode gate + research console.
   The opportunity data ships AES-GCM-encrypted in js/payload.js (built by
   tools/encrypt.mjs); the passcode never appears in this repo. Decryption is
   local (WebCrypto). Wrong passcode = failed GCM auth = shake and retry. */

/* ---------- theme ---------- */
(function () {
  var btn = document.getElementById('themeToggle');
  function paint() {
    var cur = document.documentElement.getAttribute('data-theme') || 'dark';
    btn.textContent = cur === 'dark' ? '☀️' : '🌙';
  }
  btn.addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme') || 'dark';
    var next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('compass.theme', next); } catch (e) {}
    paint();
  });
  paint();
})();

/* ---------- crypto ---------- */
function b64ToBytes(b64) {
  var bin = atob(b64), out = new Uint8Array(bin.length);
  for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
/* Forgiving normalization: case, spaces, hyphens, smart punctuation and any
   other separators are ignored — only letters and digits count. */
function normalizePass(p) { return (p || '').toLowerCase().replace(/[^a-z0-9]/g, ''); }

async function decryptPayload(pass) {
  var P = window.COMPASS_PAYLOAD;
  if (!P || !P.ct) throw new Error('no payload');
  var enc = new TextEncoder();
  var keyMaterial = await crypto.subtle.importKey(
    'raw', enc.encode(normalizePass(pass)), { name: 'PBKDF2' }, false, ['deriveKey']);
  var key = await crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt: b64ToBytes(P.salt), iterations: 310000, hash: 'SHA-256' },
    keyMaterial, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
  var plain = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: b64ToBytes(P.iv) }, key, b64ToBytes(P.ct));
  return JSON.parse(new TextDecoder().decode(plain));
}

/* ---------- gate ---------- */
var DATA = null;

(function () {
  var form = document.getElementById('gateForm');
  var card = document.getElementById('gateCard');
  var input = document.getElementById('passInput');
  var btn = document.getElementById('unlockBtn');

  async function attempt(pass, silent) {
    btn.disabled = true;
    try {
      DATA = await decryptPayload(pass);
      try { sessionStorage.setItem('compass.k', pass); } catch (e) {}
      openApp();
    } catch (e) {
      DATA = null;
      if (!silent) {
        card.classList.remove('wrong');
        void card.offsetWidth; /* restart the shake animation */
        card.classList.add('wrong');
        input.select();
      }
    }
    btn.disabled = false;
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    attempt(input.value, false);
  });

  var saved = null;
  try { saved = sessionStorage.getItem('compass.k'); } catch (e) {}
  if (saved) attempt(saved, true);

  document.getElementById('lockBtn').addEventListener('click', function () {
    try { sessionStorage.removeItem('compass.k'); } catch (e) {}
    location.reload();
  });
})();

/* ---------- app ---------- */
var state = { cat: 'All', type: 'All', mode: 'All', q: '', sort: 'overall' };
var CATS = ['Higher Ed', 'Workforce & Nonprofit', 'Youth & Teens', 'Mission & EdTech', 'Corporate Tech'];
var TYPES = [
  { key: 'All', label: 'All types', match: function () { return true; } },
  { key: 'full', label: 'Full-time', match: function (t) { return t === 'full-time'; } },
  { key: 'part', label: 'Part-time / adjunct', match: function (t) { return t === 'part-time' || t === 'adjunct'; } },
  { key: 'contract', label: 'Contract / fractional', match: function (t) { return t === 'contract' || t === 'fractional'; } },
  { key: 'vol', label: 'Volunteer / board', match: function (t) { return t === 'volunteer' || t === 'board'; } }
];
var MODES = ['All', 'remote', 'hybrid', 'onsite', 'flexible'];
var CAT_COLORS = {
  'Higher Ed': 'var(--c-highered)', 'Workforce & Nonprofit': 'var(--c-workforce)',
  'Youth & Teens': 'var(--c-youth)', 'Mission & EdTech': 'var(--c-mission)',
  'Corporate Tech': 'var(--c-corp)'
};

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function openApp() {
  document.getElementById('gate').style.display = 'none';
  document.getElementById('app').style.display = 'block';
  document.getElementById('lockBtn').hidden = false;

  document.getElementById('heroSub').textContent = DATA.focus || '';
  document.getElementById('genNote').textContent =
    'Researched & link-verified ' + (DATA.generated || '') + ' · ' + DATA.items.length +
    ' opportunities · every card links to the live posting';

  buildStats();
  buildControls();
  render();
}

function buildStats() {
  var host = document.getElementById('stats');
  var html = '';
  CATS.forEach(function (c) {
    var n = DATA.items.filter(function (it) { return it.category === c; }).length;
    html += '<div class="stat" data-cat="' + esc(c) + '" role="button" tabindex="0" style="cursor:pointer" title="Filter: ' + esc(c) + '">' +
      '<div class="n">' + n + '</div><div class="l">' + esc(c) + '</div></div>';
  });
  host.innerHTML = html;
  host.querySelectorAll('.stat').forEach(function (el) {
    function act() {
      state.cat = (state.cat === el.getAttribute('data-cat')) ? 'All' : el.getAttribute('data-cat');
      syncSegs(); render();
    }
    el.addEventListener('click', act);
    el.addEventListener('keydown', function (ev) { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); act(); } });
  });
}

function segHtml(items, attr, current, labelFn) {
  var h = '<div class="seg">';
  items.forEach(function (it) {
    var key = typeof it === 'string' ? it : it.key;
    var label = labelFn ? labelFn(it) : (typeof it === 'string' ? it : it.label);
    h += '<button data-' + attr + '="' + esc(key) + '"' + (current === key ? ' class="on"' : '') + '>' + esc(label) + '</button>';
  });
  return h + '</div>';
}

function buildControls() {
  var catRow = document.getElementById('controlsCat');
  catRow.innerHTML =
    segHtml(['All'].concat(CATS), 'cat', state.cat) +
    segHtml(TYPES, 'type', state.type) +
    segHtml(MODES, 'mode', state.mode, function (m) {
      return m === 'All' ? 'Any mode' : m.charAt(0).toUpperCase() + m.slice(1);
    });

  catRow.addEventListener('click', function (ev) {
    var b = ev.target.closest('button'); if (!b) return;
    if (b.hasAttribute('data-cat')) state.cat = b.getAttribute('data-cat');
    if (b.hasAttribute('data-type')) state.type = b.getAttribute('data-type');
    if (b.hasAttribute('data-mode')) state.mode = b.getAttribute('data-mode');
    syncSegs(); render();
  });

  document.getElementById('q').addEventListener('input', function (ev) {
    state.q = ev.target.value.toLowerCase(); render();
  });
  document.getElementById('sortSel').addEventListener('change', function (ev) {
    state.sort = ev.target.value; render();
  });
}

function syncSegs() {
  var catRow = document.getElementById('controlsCat');
  catRow.querySelectorAll('button[data-cat]').forEach(function (b) {
    b.classList.toggle('on', b.getAttribute('data-cat') === state.cat);
  });
  catRow.querySelectorAll('button[data-type]').forEach(function (b) {
    b.classList.toggle('on', b.getAttribute('data-type') === state.type);
  });
  catRow.querySelectorAll('button[data-mode]').forEach(function (b) {
    b.classList.toggle('on', b.getAttribute('data-mode') === state.mode);
  });
}

function typeMatcher(key) {
  for (var i = 0; i < TYPES.length; i++) if (TYPES[i].key === key) return TYPES[i].match;
  return function () { return true; };
}

function filtered() {
  var tm = typeMatcher(state.type);
  return DATA.items.filter(function (it) {
    if (state.cat !== 'All' && it.category !== state.cat) return false;
    if (!tm(it.type)) return false;
    if (state.mode !== 'All' && it.workMode !== state.mode) return false;
    if (state.q) {
      var hay = [it.org, it.title, it.desc, it.location, it.area, it.category,
        it.compText, it.whyFit, it.type, it.modeNotes].join(' ').toLowerCase();
      if (hay.indexOf(state.q) === -1) return false;
    }
    return true;
  });
}

function sorted(items) {
  var s = state.sort;
  var arr = items.slice();
  if (s === 'org') {
    arr.sort(function (a, b) { return a.org.localeCompare(b.org) || b.ratings.overall - a.ratings.overall; });
  } else {
    arr.sort(function (a, b) {
      var d = (b.ratings[s] || 0) - (a.ratings[s] || 0);
      if (d) return d;
      d = b.ratings.overall - a.ratings.overall;
      if (d) return d;
      return (b.ratings.mission || 0) - (a.ratings.mission || 0);
    });
  }
  return arr;
}

function dots(n) {
  var h = '<span class="dots">';
  for (var i = 1; i <= 5; i++) h += '<i' + (i <= n ? ' class="on"' : '') + '></i>';
  return h + '</span>';
}

function modeBadge(it) {
  var label = it.workMode.charAt(0).toUpperCase() + it.workMode.slice(1);
  if (it.modeNotes) label += ' · ' + it.modeNotes;
  var cls = 'badge';
  if (it.workMode === 'remote') cls += ' mode-remote';
  if (/5 days|five days|fully on.?site/i.test(it.modeNotes || '')) cls += ' mode-onsite5';
  return '<span class="' + cls + '">' + esc(label) + '</span>';
}

function card(it) {
  var r = it.ratings;
  var h = '<article class="card" data-cat="' + esc(it.category) + '">';
  h += '<div class="card-top"><div>';
  h += '<div class="card-org">' + esc(it.org) + '</div>';
  h += '<div class="card-title"><a href="' + esc(it.url) + '" target="_blank" rel="noopener noreferrer">' + esc(it.title) + '</a></div>';
  h += '</div><div class="overall-chip"><span class="num">' + r.overall.toFixed(1) + '</span><span class="lbl">Overall</span></div></div>';

  h += '<div class="badges">';
  h += '<span class="badge"><span class="dot" style="background:' + (CAT_COLORS[it.category] || 'var(--border-2)') + '"></span>' + esc(it.category) + '</span>';
  h += '<span class="badge">' + esc(it.type.charAt(0).toUpperCase() + it.type.slice(1)) + '</span>';
  h += modeBadge(it);
  if (it.area) h += '<span class="badge">📍 ' + esc(it.area) + '</span>';
  h += '</div>';

  h += '<p class="card-desc">' + esc(it.desc) + '</p>';
  if (it.whyFit) h += '<p class="card-why"><b>Why you:</b> ' + esc(it.whyFit) + '</p>';
  h += '<div class="fact-row"><span class="k">Comp</span><span class="v">' + esc(it.compText || 'Not listed') + '</span></div>';
  if (it.benefitsText && it.benefitsText !== 'Not listed') {
    h += '<div class="fact-row"><span class="k">Benefits</span><span class="v">' + esc(it.benefitsText) + '</span></div>';
  }
  if (it.location) {
    h += '<div class="fact-row"><span class="k">Where</span><span class="v">' + esc(it.location) + '</span></div>';
  }

  h += '<div class="ratings">';
  h += '<span class="rating"><span class="rl">Mission</span>' + dots(r.mission) + '</span>';
  h += '<span class="rating"><span class="rl">Fit</span>' + dots(r.fit) + '</span>';
  h += '<span class="rating dim-comp"><span class="rl">Comp</span>' + dots(r.comp) + '</span>';
  h += '<span class="rating"><span class="rl">Flex</span>' + dots(r.flex) + '</span>';
  h += '</div>';

  h += '<div class="card-foot">';
  h += '<a class="apply-btn" href="' + esc(it.url) + '" target="_blank" rel="noopener noreferrer">View posting ↗</a>';
  if (it.verified) h += '<span class="verified-note">✓ ' + esc(it.verified) + '</span>';
  h += '</div>';

  return h + '</article>';
}

function render() {
  var items = sorted(filtered());
  document.getElementById('countNote').textContent =
    items.length + ' of ' + DATA.items.length + ' opportunities shown';
  var host = document.getElementById('list');
  host.innerHTML = items.length
    ? items.map(card).join('')
    : '<div class="empty">Nothing matches those filters — loosen one and try again.</div>';
}
