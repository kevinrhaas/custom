/**
 * hud.js — year badge, confidence toggle, theme, hints.
 *
 * Deliberately small. The interface competes with the thing it is showing, so it
 * stays out of the way: a date, one switch that matters, and a line of text that
 * appears when there is something to say and fades when there is not.
 *
 * The confidence toggle is the only control here that changes what you are
 * looking at, and it is styled as the primary one for that reason.
 */

import { markSeen, renderWhatsNew, unseenCount } from './whatsnew.js';

const THEME_KEY = 'chicago4d.theme';
const CONF_KEY = 'chicago4d.confidence';
const SET_KEY = 'chicago4d.settings';

const DEFAULT_SETTINGS = { speed: 1.45, fov: 72, quality: 1.5 };

function readSettings() {
  try {
    return { ...DEFAULT_SETTINGS, ...JSON.parse(window.localStorage.getItem(SET_KEY) || '{}') };
  } catch { return { ...DEFAULT_SETTINGS }; }
}

function readStored(key, fallback) {
  try { return window.localStorage.getItem(key) ?? fallback; } catch { return fallback; }
}

function store(key, value) {
  try { window.localStorage.setItem(key, value); } catch { /* private mode */ }
}

export function createHud({ root, scene, onConfidence, onHelp, onSetting, onGoTo, isTouch }) {
  const $ = (id) => root.querySelector(`#${id}`);
  const badgeYear = root.querySelector('.badge-year');
  const badgeSub = root.querySelector('.badge-sub');
  const btnConf = $('btn-confidence');
  const btnTheme = $('btn-theme');
  const btnHelp = $('btn-help');
  const panel = $('panel');
  const hint = $('hint');
  const settings = readSettings();

  if (badgeYear) badgeYear.textContent = scene?.id ?? '';
  if (badgeSub) badgeSub.textContent = formatSceneDate(scene?.target_date);

  // Theme: dark by default — this is a walkthrough, and a bright interface over
  // a daylight scene is the one combination that reads as neither.
  const theme = readStored(THEME_KEY, 'dark');
  document.documentElement.setAttribute('data-theme', theme === 'light' ? 'light' : 'dark');

  let hintTimer = 0;
  function say(text, ms = 2600) {
    if (!hint) return;
    hint.textContent = text;
    hint.classList.add('on');
    clearTimeout(hintTimer);
    if (ms) hintTimer = setTimeout(() => hint.classList.remove('on'), ms);
  }

  let confidenceOn = false;
  function setConfidence(on, { announce = true } = {}) {
    confidenceOn = !!on;
    btnConf?.setAttribute('aria-pressed', String(confidenceOn));
    store(CONF_KEY, confidenceOn ? '1' : '0');
    onConfidence?.(confidenceOn);
    if (announce) {
      say(confidenceOn
        ? 'Confidence view — amber is inferred, dithered massing is a guess'
        : 'Confidence view off');
    }
    return confidenceOn;
  }

  btnConf?.addEventListener('click', () => setConfidence(!confidenceOn));

  btnTheme?.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', next);
    store(THEME_KEY, next);
  });

  // ---- the controls / settings panel -------------------------------------
  //
  // Everything here was discoverable only by guessing before: run already
  // existed on Shift and nobody could know that. A walkthrough that does not
  // say how to walk is not finished.

  function panelOpen() { return panel && !panel.hasAttribute('hidden'); }

  function setPanel(open) {
    if (!panel) return;
    panel.toggleAttribute('hidden', !open);
    btnHelp?.setAttribute('aria-pressed', String(!!open));
    // Release the pointer lock on open. While the cursor is captured for
    // looking around, every click goes to the canvas and none of these controls
    // can be operated at all — the panel would look fine and do nothing.
    if (open && document.pointerLockElement) document.exitPointerLock?.();
    onHelp?.(!!open);
  }

  btnHelp?.addEventListener('click', () => setPanel(!panelOpen()));
  $('panel-close')?.addEventListener('click', () => setPanel(false));

  // ---- What's new ---------------------------------------------------------
  //
  // Painted once, lazily, the first time the tab is actually opened. The
  // unseen marker clears on that same open — not on render — so the dot means
  // "you have not looked at this", which is the only thing it could honestly
  // mean if the panel paints the tab whether or not you visit it.

  const whatsNewDot = $('whatsnew-dot');
  const helpDot = $('help-dot');
  let whatsNewPainted = false;

  function paintUnseen() {
    const n = unseenCount();
    whatsNewDot?.toggleAttribute('hidden', n === 0);
    helpDot?.toggleAttribute('hidden', n === 0);
    if (n > 0) {
      btnHelp?.setAttribute('title',
        `Controls, settings and what's new — ${n} unread (H)`);
    }
  }
  paintUnseen();

  function openWhatsNew() {
    if (!whatsNewPainted) { renderWhatsNew($('whatsnew')); whatsNewPainted = true; }
    markSeen();
    paintUnseen();
  }

  function selectTab(want) {
    root.querySelectorAll('.panel-tab').forEach((x) => {
      x.classList.toggle('is-on', x.dataset.tab === want);
    });
    root.querySelectorAll('.panel-body').forEach((s) => {
      s.toggleAttribute('hidden', s.dataset.panel !== want);
    });
    if (want === 'whatsnew') openWhatsNew();
  }

  root.querySelectorAll('.panel-tab').forEach((tab) => {
    tab.addEventListener('click', () => selectTab(tab.dataset.tab));
  });

  // Show the control list that matches how this visitor is actually driving.
  $('keys-desktop')?.toggleAttribute('hidden', !!isTouch);
  $('keys-touch')?.toggleAttribute('hidden', !isTouch);

  function wireRange(id, label, key, fmt) {
    const el = $(id); const out = $(label);
    if (!el) return;
    el.value = String(settings[key]);
    const paint = () => { if (out) out.textContent = fmt(Number(el.value)); };
    paint();
    el.addEventListener('input', () => {
      settings[key] = Number(el.value);
      paint();
      onSetting?.(key, settings[key]);
      store(SET_KEY, JSON.stringify(settings));
    });
  }
  wireRange('s-speed', 'v-speed', 'speed', (v) => `${v.toFixed(1)} m/s`);
  wireRange('s-fov', 'v-fov', 'fov', (v) => `${Math.round(v)}°`);

  const qual = $('s-quality');
  if (qual) {
    qual.value = String(settings.quality);
    qual.addEventListener('change', () => {
      settings.quality = Number(qual.value);
      onSetting?.('quality', settings.quality);
      store(SET_KEY, JSON.stringify(settings));
    });
  }

  // Anchor jumps: the scene already names viewpoints for the smoke harness, so
  // the visitor may as well have them too.
  const anchors = $('anchors');
  if (anchors && Array.isArray(scene?.anchors)) {
    for (const a of scene.anchors) {
      const b = document.createElement('button');
      b.className = 'anchor-btn';
      b.textContent = a.label || a.id;
      b.addEventListener('click', () => { onGoTo?.(a.id); setPanel(false); });
      anchors.appendChild(b);
    }
  }

  window.addEventListener('keydown', (e) => {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLSelectElement) return;
    const k = e.key.toLowerCase();
    if (k === 'h' || k === '?') { e.preventDefault(); setPanel(!panelOpen()); }
    else if (k === 'c') { e.preventDefault(); setConfidence(!confidenceOn); }
    else if (k === 'n') { e.preventDefault(); setPanel(true); selectTab('whatsnew'); }
    else if (e.key === 'Escape' && panelOpen()) setPanel(false);
  });

  return {
    say,
    settings,
    setPanel,
    get confidenceOn() { return confidenceOn; },
    setConfidence,
    /** Restore the visitor's last choice without narrating it back at them. */
    restore() {
      if (readStored(CONF_KEY, '0') === '1') setConfidence(true, { announce: false });
    },
    show() { root.removeAttribute('hidden'); },
    setLocked(locked) { document.body.classList.toggle('is-locked', !!locked); },
  };
}

function formatSceneDate(iso) {
  if (!iso) return '';
  const [y, m, d] = iso.split('-').map(Number);
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];
  if (!y || !m || !d) return iso;
  return `${d} ${months[m - 1]}`;
}
