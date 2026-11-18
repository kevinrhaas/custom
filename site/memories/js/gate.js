// -----------------------------------------------------------------------
// gate.js — the album's front door.
//
//   const gate = await runGate(CONFIG, document.getElementById('main'));
//   // → { granted, label, isAdmin, access }
//
// With CONFIG.access.enabled false it resolves at once. Otherwise it checks
// this device for an earlier invite (or consumes ?invite= from the address),
// and if there is none it shows a calm "this album is just for family"
// screen where a relative can paste the link or code they were sent. The
// promise resolves only once access is granted — no reload needed.
//
// Styles: css/gate.css (classes .gate-*), themed only through the skin's
// custom properties. The sheet is added to <head> here if the page forgot.
//
// Reminder (see access.js): this is a polite front door, not a lock. The
// photos themselves are public files.
// -----------------------------------------------------------------------

import { createAccess } from '../vendor/polecat-shell/access.js';
import { icon, registerIcons } from '../vendor/polecat-shell/icons.js';

// A framed photo for the door (stroke, currentColor, like the rest of the set).
registerIcons({
  'gate-photo': '<path d="M12 20s-7.5-4.6-9.2-9.4C1.6 7 3.9 4 7.2 4c2 0 3.6 1.1 4.8 2.8C13.2 5.1 14.8 4 16.8 4c3.3 0 5.6 3 4.4 6.6C19.5 15.4 12 20 12 20z"/>',
});

const ALBUM_ROOT = new URL('../', import.meta.url).href; // …/memories/

export async function runGate(CONFIG, mountEl) {
  const cfg = CONFIG.access || {};
  if (!cfg.enabled) return { granted: true, label: '', isAdmin: false, access: null };

  const access = createAccess({
    prefix: cfg.prefix || 'memories',
    publicKey: cfg.publicKey,
    revoked: cfg.revoked || [],
    linkBase: ALBUM_ROOT,
  });
  const first = await access.init();
  const result = () => {
    const info = access.info() || {};
    return {
      granted: true,
      // The admin device is "Admin" inside access.js; don't greet anyone by that.
      label: info.via === 'admin' ? '' : info.label || '',
      isAdmin: access.isAdmin(),
      access,
    };
  };
  if (first.granted) return result();

  await ensureStyles();
  return new Promise((resolve) => {
    let keeperUnlocked = false;
    render(CONFIG, mountEl, first.inviteError, async (code, raw) => {
      const r = await access.verifyInvite(code);
      if (r.ok) { access.grant('invite', r.payload?.label || ''); return null; }
      // The keeper may paste the admin key here instead of on the admin page.
      // Accept it: it opens the album and unlocks link-making on this device.
      const key = adminKeyIn(raw);
      if (key && await access.unlockAdmin(key)) { keeperUnlocked = true; return null; }
      return r.reason;
    }, () => resolve({ ...result(), keeperUnlocked }));
  });
}

// ---- pulling a code out of whatever got pasted -------------------------

/** A full link, a whole text message with the link in it, or the bare code. */
export function extractCode(text) {
  let s = String(text || '').trim();
  if (!s) return '';
  const inParam = /[?&#]invite=([^&\s#"'<>]+)/.exec(s);
  if (inParam) {
    try { return decodeURIComponent(inParam[1]).trim(); } catch { return inParam[1].trim(); }
  }
  // Codes are base64url "payload.signature"; email clients sometimes wrap
  // them across lines, so look for the shape after removing whitespace.
  const bare = /[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{40,}/.exec(s.replace(/\s+/g, ''));
  return bare ? bare[0] : s.replace(/\s+/g, '');
}

/** A pasted admin key: one long standard-base64 run (PKCS#8 P-256 ≈ 184 chars). */
export function adminKeyIn(text) {
  const m = /[A-Za-z0-9+/]{120,}={0,2}/.exec(String(text || '').replace(/\s+/g, ''));
  return m ? m[0] : '';
}

// ---- view --------------------------------------------------------------

function messageFor(reason, keeper) {
  if (!reason) return '';
  if (reason === 'expired') return `This link has expired. Ask ${keeper} for a fresh one.`;
  if (reason === 'empty') return 'Paste the link or code first, then tap "Open the album".';
  return `That link didn't work. Ask ${keeper} to send it again.`;
}

function render(CONFIG, mountEl, inviteError, tryCode, done) {
  const keeper = CONFIG.keeper || 'the family';
  const honorees = (CONFIG.honorees || []).filter((h) => h && h.name);
  const root = document.createElement('section');
  root.className = 'gate';
  root.setAttribute('aria-labelledby', 'gate-title');
  root.innerHTML = `
    <div class="gate-card">
      <div class="gate-mark" aria-hidden="true">${icon('gate-photo', 30)}</div>
      <h1 class="gate-title" id="gate-title"></h1>
      ${honorees.length ? `<p class="gate-kicker">In loving memory of</p><ul class="gate-names"></ul>` : ''}
      <div class="gate-rule" aria-hidden="true"><span></span></div>
      <p class="gate-lead">This album is just for family.</p>
      <p class="gate-sub"></p>
      <form class="gate-form" novalidate>
        <label class="gate-label" for="gate-code">Paste your link or code</label>
        <textarea class="gate-input" id="gate-code" name="code" rows="2" placeholder="Tap here, then choose Paste"
          autocomplete="off" autocapitalize="off" autocorrect="off" spellcheck="false"
          aria-describedby="gate-error gate-help"></textarea>
        <p class="gate-error" id="gate-error" role="alert"></p>
        <button class="gate-btn" type="submit">
          <span class="gate-btn-text">Open the album</span>${icon('arrowRight', 24)}
        </button>
      </form>
      <p class="gate-help" id="gate-help">Got your link in a text or an email? Tapping it opens the album too.</p>
    </div>`;

  root.querySelector('.gate-title').textContent = CONFIG.title || 'Family album';
  root.querySelector('.gate-sub').textContent =
    `Ask ${keeper} for your own link — it opens the album on this device.`;
  const list = root.querySelector('.gate-names');
  for (const h of honorees) {
    const li = document.createElement('li');
    li.className = 'gate-name';
    li.textContent = h.name;
    if (h.years) {
      const y = document.createElement('span');
      y.className = 'gate-years';
      y.textContent = h.years;
      li.append(y);
    }
    list.append(li);
  }

  const form = root.querySelector('.gate-form');
  const input = root.querySelector('.gate-input');
  const error = root.querySelector('.gate-error');
  const button = root.querySelector('.gate-btn');
  const btnText = root.querySelector('.gate-btn-text');

  const showError = (reason) => {
    const msg = messageFor(reason, keeper);
    error.textContent = msg;
    form.classList.toggle('gate-has-error', !!msg);
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
  };
  showError(inviteError);

  // Enter submits (it's a textarea only so long codes wrap visibly).
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
  });
  input.addEventListener('input', () => { if (error.textContent) showError(null); });

  let busy = false;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (busy) return;
    const code = extractCode(input.value);
    if (!code) { showError('empty'); input.focus(); return; }
    busy = true;
    button.disabled = true;
    btnText.textContent = 'Opening…';
    const reason = await tryCode(code, input.value);
    if (reason) {
      busy = false;
      button.disabled = false;
      btnText.textContent = 'Open the album';
      showError(reason);
      input.focus();
      input.select();
      return;
    }
    showError(null);
    btnText.textContent = 'Welcome';
    root.classList.add('gate-leaving');
    const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
    setTimeout(() => { root.remove(); done(); }, calm ? 0 : 420);
  });

  mountEl.append(root);
  return root;
}

function ensureStyles() {
  const href = new URL('../css/gate.css', import.meta.url).href;
  const has = [...document.querySelectorAll('link[rel="stylesheet"]')].some((l) => l.href === href);
  if (has) return Promise.resolve();
  return new Promise((resolve) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.onload = link.onerror = () => resolve();
    document.head.append(link);
    setTimeout(resolve, 1500); // never hold the door shut on a slow sheet
  });
}
