// -----------------------------------------------------------------------
// admin.js — the keeper's "Make invite links" page (/memories/admin/).
//
//   1. Unlock: paste the admin (private) key once; access.js keeps it in
//      localStorage on this device only. It is never in the repo.
//   2. Make a link: name + how long → a signed ?invite= link, with copy /
//      share / text / email buttons and a QR code to scan.
//   •  Links you've made: kept on this device (access.minted()).
//   3. Edit and publish the shared album settings from the admin form.
// -----------------------------------------------------------------------

import { CONFIG } from '../js/config.js';
import { createAccess } from '../vendor/polecat-shell/access.js';
import { icon, registerIcons } from '../vendor/polecat-shell/icons.js';
import qrcode from '../vendor/qrcode/qrcode.mjs';

registerIcons({
  share: '<path d="M12 15V3m0 0L7.5 7.5M12 3l4.5 4.5"/><path d="M5 11.5V19a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-7.5"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
});

const ALBUM_ROOT = new URL('../', location.href).href;
const KEEPER = CONFIG.keeper || 'the family';
const HELPER = CONFIG.helper || 'Kevin'; // who helps with the album
const cfg = CONFIG.access || {};
const access = createAccess({
  prefix: cfg.prefix || 'memories',
  publicKey: cfg.publicKey,
  revoked: cfg.revoked || [],
  linkBase: ALBUM_ROOT,
});

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];

// ---- chrome --------------------------------------------------------------

if (CONFIG.defaultSkin) {
  try {
    const saved = JSON.parse(localStorage.getItem('memories.prefs') || '{}');
    if (!saved.skin) document.documentElement.dataset.skin = CONFIG.defaultSkin;
  } catch {}
}
paintIcons(document);
$('#albumName').textContent = CONFIG.title || 'Family album';
document.title = `Care for the album · ${CONFIG.title || 'Family album'}`;
$$('.helperName').forEach((el) => { el.textContent = HELPER; });
$('#unlockHelp').textContent =
  `Paste the admin key ${HELPER} gave you. You only need to do this once on each phone or computer.`;
if (!cfg.enabled) {
  const b = $('#openBanner');
  b.hidden = false;
  b.innerHTML = `${icon('info', 22)}<span>Invite links are switched off right now, so the album opens for anyone who has its address. Links you make will still work if they're switched back on.</span>`;
}

function paintIcons(root) {
  $$('[data-icon]', root).forEach((el) => {
    if (!el.firstChild) el.innerHTML = icon(el.dataset.icon, 22);
  });
}

let toastTimer = 0;
function toast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.hidden = true; }, 2600);
}

async function copyText(text, el) {
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    // Older browsers / insecure contexts: copy from a selected field.
    const ta = el || Object.assign(document.createElement('textarea'), { value: text });
    if (!el) { ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.append(ta); }
    ta.select();
    try { document.execCommand('copy'); } catch {}
    if (!el) ta.remove();
  }
  toast('Copied. You can paste it into a message now.');
}

const fmtDate = (ms) => new Date(ms).toLocaleDateString(undefined, { month: 'long', day: 'numeric', year: 'numeric' });

// ---- step 1: unlock --------------------------------------------------------

function cleanKey(s) {
  return String(s || '').replace(/-----[^-]+-----/g, '').replace(/\s+/g, '');
}

let settingsController;
let settingsHost;

async function showSettings(admin) {
  $('#settingsCard').hidden = !admin;
  if (!admin) {
    settingsController?.destroy?.();
    settingsController = null; settingsHost = null;
    $('#settingsTools').replaceChildren();
    return;
  }
  if (settingsHost) return;
  const host = document.createElement('div'); settingsHost = host;
  $('#settingsTools').append(host);
  host.textContent = 'Opening album settings…';
  try {
    const { mountSettings } = await import('./settings.js');
    if (settingsHost !== host || !access.isAdmin()) return;
    const controller = mountSettings(host);
    if (settingsHost !== host || !access.isAdmin()) controller?.destroy?.();
    else settingsController = controller;
  } catch {
    if (settingsHost === host) host.textContent = 'Album settings could not open. Reload this page to try again.';
  }
}

let taggingController;
let taggingHost;

async function showTagging(admin) {
  $('#tagCard').hidden = !admin;
  if (!admin) {
    taggingController?.destroy?.();
    taggingController = null;
    taggingHost = null;
    $('#tagTools').replaceChildren();
    return;
  }
  if (taggingHost) return;
  const host = document.createElement('div');
  taggingHost = host;
  $('#tagTools').append(host);
  host.textContent = 'Opening photo tags…';
  try {
    const { mountTagging } = await import('./tagging.js');
    if (taggingHost !== host || !access.isAdmin()) return;
    const controller = await mountTagging(host);
    if (taggingHost !== host || !access.isAdmin()) controller?.destroy?.();
    else taggingController = controller;
  } catch (error) {
    if (taggingHost === host) host.textContent = `Photo tagging could not open. Reload this page to try again. ${error.message}`;
  }
}

function showLockState() {
  const admin = access.isAdmin();
  $('#lockedView').hidden = admin;
  $('#unlockedView').hidden = !admin;
  $('#makeCard').hidden = !admin;
  $('#madeCard').hidden = !admin;
  showSettings(admin);
  showTagging(admin);
  if (admin) renderMade();
}

$('#unlockBtn').addEventListener('click', async () => {
  const err = $('#unlockError');
  const key = cleanKey($('#adminKey').value);
  err.textContent = '';
  if (!key) { err.textContent = 'Paste the admin key into the box first.'; $('#adminKey').focus(); return; }
  const btn = $('#unlockBtn');
  btn.disabled = true;
  const ok = await access.unlockAdmin(key);
  btn.disabled = false;
  if (!ok) {
    err.textContent = `That key doesn't fit this album. Check that you copied all of it, or ask ${HELPER} to send it again.`;
    return;
  }
  $('#adminKey').value = '';
  showLockState();
  toast('Unlocked. This device can make links now.');
  $('#who').focus();
});

$('#lockBtn').addEventListener('click', () => {
  if (!confirm("Lock this device? You'll need the admin key again to make links here.")) return;
  access.lockAdmin();
  $('#result').hidden = true;
  showLockState();
  toast('Locked.');
});

// ---- step 2: make a link -------------------------------------------------

let current = null;

$('#makeForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const label = $('#who').value.trim().replace(/\s+/g, ' ').slice(0, 60);
  const days = +($('input[name="days"]:checked')?.value || 0);
  try {
    current = await access.mintInvite({ label, days });
  } catch {
    toast('This device is locked. Unlock it first.');
    showLockState();
    return;
  }
  showResult(current);
  renderMade();
});

function firstNames() {
  const names = (CONFIG.honorees || []).map((h) => String(h.name || '').split(' ')[0]).filter(Boolean);
  if (names.length < 2) return names.join('');
  return `${names.slice(0, -1).join(', ')} and ${names.at(-1)}`;
}

function messages(rec) {
  const hi = rec.label ? `Hi ${rec.label}` : 'Hi';
  const who = firstNames();
  const about = who ? ` — all the photos of ${who}` : '';
  const sms = `${hi}, here's your link to the family album${about}. Just tap it and it opens: ${rec.link}`;
  const subject = `Your link to ${CONFIG.title || 'the family album'}`;
  const body = [
    `${hi}, here's your link to the family album${about}.`,
    '',
    rec.link,
    '',
    'Just tap or click it and the album opens. It remembers your phone or computer, so next time you can open it straight away. If you use more than one device, tap this same link on each one.',
    '',
    'You can look through the photos, read the stories and save copies of any you like.',
    '',
    'With love,',
    KEEPER,
  ].join('\n');
  return { sms, subject, body };
}

function showResult(rec) {
  const box = $('#result');
  box.hidden = false;
  $('#resultTitle').textContent = rec.label ? `${possessive(rec.label)} link is ready` : 'Your link is ready';
  $('#resultWhen').textContent = rec.exp ? `It works until ${fmtDate(rec.exp)}.` : 'It works for good.';
  const field = $('#resultLink');
  field.value = rec.link;
  field.style.height = 'auto';
  field.style.height = `${field.scrollHeight + 4}px`; // show the whole link

  const m = messages(rec);
  $('[data-act="sms"]', box).href = `sms:?&body=${encodeURIComponent(m.sms)}`;
  $('[data-act="mail"]', box).href =
    `mailto:?subject=${encodeURIComponent(m.subject)}&body=${encodeURIComponent(m.body)}`;
  $('[data-act="share"]', box).hidden = !navigator.share;
  $('#qr').innerHTML = qrSvg(rec.link);
  $('#qr').setAttribute('aria-label', rec.label ? `QR code for ${possessive(rec.label)} link` : 'QR code for the link');
  box.focus({ preventScroll: true });
  box.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
}

function possessive(name) {
  return /s$/i.test(name) ? `${name}'` : `${name}'s`;
}

$('#result').addEventListener('click', async (e) => {
  const act = e.target.closest('[data-act]')?.dataset.act;
  if (!act || !current) return;
  if (act === 'copy') copyText(current.link, $('#resultLink'));
  if (act === 'share') {
    const m = messages(current);
    try {
      await navigator.share({ title: m.subject, text: m.sms.replace(current.link, '').replace(/:\s*$/, '.'), url: current.link });
    } catch {}
  }
});
$('#resultLink').addEventListener('focus', (e) => e.target.select());

function qrSvg(text) {
  const qr = qrcode(0, 'L');
  qr.addData(text);
  qr.make();
  const n = qr.getModuleCount();
  const q = 4; // quiet zone, in modules
  let d = '';
  for (let r = 0; r < n; r++) {
    for (let c = 0; c < n; c++) if (qr.isDark(r, c)) d += `M${c + q} ${r + q}h1v1h-1z`;
  }
  const s = n + q * 2;
  return `<svg viewBox="0 0 ${s} ${s}" role="img" aria-hidden="true" shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg"><rect width="${s}" height="${s}" fill="#fff"/><path d="${d}" fill="#000"/></svg>`;
}

// ---- links you've made -------------------------------------------------------

function renderMade() {
  const list = access.minted();
  const ul = $('#made');
  $('#madeEmpty').hidden = list.length > 0;
  $('#madeHelp').hidden = list.length === 0;
  ul.replaceChildren(...list.map((rec) => {
    const li = document.createElement('li');
    li.className = 'adm-item';
    const forAll = (cfg.revoked || []).includes(rec.jti);
    const here = !forAll && access.localRevoked().includes(rec.jti);
    const expired = rec.exp && Date.now() > rec.exp;
    let status = rec.exp ? `Works until ${fmtDate(rec.exp)}` : 'Works always';
    let state = 'on';
    if (forAll) { status = 'Turned off for everyone'; state = 'off'; }
    else if (here) { status = 'Turned off on this device'; state = 'off'; }
    else if (expired) { status = `Ended ${fmtDate(rec.exp)}`; state = 'off'; }

    li.innerHTML = `
      <div class="adm-item-main">
        <p class="adm-item-name"></p>
        <p class="adm-item-meta"></p>
        <p class="adm-item-status" data-state="${state}"></p>
        ${here ? '<p class="adm-item-tell"></p>' : ''}
      </div>
      <div class="adm-item-actions">
        <button class="adm-btn adm-small-btn" type="button" data-do="copy">${icon('copy', 20)}<span>Copy again</span></button>
        ${state === 'on' ? `<button class="adm-btn adm-small-btn adm-quiet" type="button" data-do="off">${icon('eyeOff', 20)}<span>Turn off on this device</span></button>` : ''}
      </div>`;
    $('.adm-item-name', li).textContent = rec.label || 'No name';
    $('.adm-item-meta', li).textContent = `Made ${fmtDate(rec.iat)} · ID ${rec.jti}`;
    $('.adm-item-status', li).textContent = status;
    if (here) $('.adm-item-tell', li).textContent = `To turn this link off for everyone, send ${HELPER} its ID: ${rec.jti}`;
    li.addEventListener('click', (e) => {
      const what = e.target.closest('[data-do]')?.dataset.do;
      if (what === 'copy') copyText(rec.link);
      if (what === 'off') {
        if (!confirm(`Turn off ${rec.label ? possessive(rec.label) : 'this'} link on this device?`)) return;
        access.revoke(rec.jti);
        renderMade();
        toast(`Turned off here. To turn it off for everyone, send ${HELPER} its ID: ${rec.jti}`);
      }
    });
    return li;
  }));
}

showLockState();
