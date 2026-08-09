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

const THEME_KEY = 'chicago4d.theme';
const CONF_KEY = 'chicago4d.confidence';

function readStored(key, fallback) {
  try { return window.localStorage.getItem(key) ?? fallback; } catch { return fallback; }
}

function store(key, value) {
  try { window.localStorage.setItem(key, value); } catch { /* private mode */ }
}

export function createHud({ root, scene, onConfidence, onHelp }) {
  const $ = (id) => root.querySelector(`#${id}`);
  const badgeYear = root.querySelector('.badge-year');
  const badgeSub = root.querySelector('.badge-sub');
  const btnConf = $('btn-confidence');
  const btnTheme = $('btn-theme');
  const btnHelp = $('btn-help');
  const legend = $('legend');
  const hint = $('hint');

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
    legend?.toggleAttribute('hidden', !confidenceOn);
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

  btnHelp?.addEventListener('click', () => {
    const shown = !legend.hasAttribute('hidden');
    legend.toggleAttribute('hidden', shown);
    onHelp?.(!shown);
  });

  return {
    say,
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
