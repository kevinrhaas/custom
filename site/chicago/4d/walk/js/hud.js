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
import { formatHeight, formatSpeed, normalUnitSystem } from './units.js';

const THEME_KEY = 'chicago4d.theme';
const CONF_KEY = 'chicago4d.confidence';
const SET_KEY = 'chicago4d.settings';
const CONTROL_HELP_KEY = 'chicago4d.controlHelpDismissed';

const DEFAULT_SETTINGS = {
  speed: 1.45, fov: 72, quality: 1.5,
  compass: true, overviewMap: true, streetNames: true, units: 'imperial',
  // '' = never chosen, so main.js's device guess stands (phone light, desktop full).
  detail: '',
};

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

export function createHud({
  root, scene, registry, intersections = [], onConfidence, onFly, onHelp,
  onSetting, onGoTo, isTouch, resolvedDetail = 'full',
}) {
  const $ = (id) => root.querySelector(`#${id}`);
  const badgeYear = root.querySelector('.badge-year');
  const badgeSub = root.querySelector('.badge-sub');
  const badgeAlt = $('badge-alt');
  const btnConf = $('btn-confidence');
  const btnFly = $('btn-fly');
  const flyLabel = $('fly-label');
  const btnTheme = $('btn-theme');
  const btnHelp = $('btn-help');
  const panel = $('panel');
  const controlHelp = $('control-help');
  const hint = $('hint');
  const settings = readSettings();
  settings.units = normalUnitSystem(settings.units);

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

  // ---- free-fly -----------------------------------------------------------

  let flying = false;
  function setFly(on, { announce = true } = {}) {
    flying = !!on;
    btnFly?.setAttribute('aria-pressed', String(flying));
    if (flyLabel) flyLabel.textContent = flying ? 'Walk' : 'Fly';
    if (btnFly) {
      btnFly.title = flying ? 'Back to walking (F)' : 'Free-fly — rise above the town (F)';
    }
    if (!flying) { badgeAlt?.setAttribute('hidden', ''); badgeAlt?.parentElement?.classList.remove('has-alt'); }
    onFly?.(flying);
    if (announce) {
      say(flying
        // Said on entry because it is the honest frame for the view they are
        // about to get: from above, the edge of what has been built is visible,
        // and the ground beyond it is a skirt rather than a claim.
        ? (isTouch ? 'Flying — ▲ ▼ to rise and descend. The modelled town ends where the detail does.'
          : 'Flying — Space and Q to rise and descend. The modelled town ends where the detail does.')
        : 'Back on foot');
    }
    return flying;
  }

  btnFly?.addEventListener('click', () => setFly(!flying));

  /** Altitude readout, driven from the frame loop. Stored internally in metres. */
  let lastAltitudeM = 0;
  function setAltitude(m) {
    lastAltitudeM = m;
    if (!badgeAlt) return;
    const show = flying && m > 1;
    badgeAlt.toggleAttribute('hidden', !show);
    badgeAlt.parentElement?.classList.toggle('has-alt', show);
    if (show) badgeAlt.textContent = `${formatHeight(m, settings.units)} up`;
  }

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
    root.classList.toggle('panel-open', !!open);
    btnHelp?.setAttribute('aria-pressed', String(!!open));
    // Release the pointer lock on open. While the cursor is captured for
    // looking around, every click goes to the canvas and none of these controls
    // can be operated at all — the panel would look fine and do nothing.
    if (open && document.pointerLockElement) document.exitPointerLock?.();
    onHelp?.(!!open);
  }

  btnHelp?.addEventListener('click', () => setPanel(!panelOpen()));
  $('panel-close')?.addEventListener('click', () => setPanel(false));

  function dismissControlHelp({ remember = true } = {}) {
    if (!controlHelp) return;
    controlHelp.setAttribute('hidden', '');
    if (remember) store(CONTROL_HELP_KEY, '1');
    onHelp?.(false);
  }

  function showControlHelp({ auto = false } = {}) {
    if (!controlHelp || (auto && readStored(CONTROL_HELP_KEY, '0') === '1')) return false;
    setPanel(false);
    controlHelp.removeAttribute('hidden');
    if (document.pointerLockElement) document.exitPointerLock?.();
    onHelp?.(true);
    return true;
  }

  $('control-help-close')?.addEventListener('click', () => dismissControlHelp());
  $('control-help-gotit')?.addEventListener('click', () => dismissControlHelp());
  $('s-show-control-help')?.addEventListener('click', () => showControlHelp());
  $('control-help-desktop')?.toggleAttribute('hidden', !!isTouch);
  $('control-help-touch')?.toggleAttribute('hidden', !isTouch);

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

  /** G, and the one route the touch build reaches by tapping the tab. */
  function openGoTo() {
    setPanel(true);
    selectTab('goto');
    // Only for a visitor who came by keyboard: focusing this on a phone raises
    // the on-screen keyboard over the list the tap was meant to open.
    if (!isTouch) {
      const input = $('jump-search');
      input?.focus();
      input?.select?.();
    }
  }

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
    return paint;
  }
  const paintSpeed = wireRange('s-speed', 'v-speed', 'speed',
    (v) => formatSpeed(v, settings.units));
  wireRange('s-fov', 'v-fov', 'fov', (v) => `${Math.round(v)}°`);

  const units = $('s-units');
  if (units) {
    units.value = settings.units;
    units.addEventListener('change', () => {
      settings.units = normalUnitSystem(units.value);
      units.value = settings.units;
      paintSpeed?.();
      setAltitude(lastAltitudeM);
      onSetting?.('units', settings.units);
      store(SET_KEY, JSON.stringify(settings));
    });
  }

  // Scene detail. Distinct from Render quality on purpose: quality is how many
  // PIXELS are drawn, detail is how much GEOMETRY. Conflating them would hide
  // which one a visitor with a slow machine actually needs to turn down.
  const detail = $('s-detail');
  if (detail) {
    // '' means the visitor has never chosen, and the level in force is the
    // device guess main.js made. Show THAT, not the first option in the list:
    // a phone running `light` must not display `Full`.
    detail.value = settings.detail || resolvedDetail;
    detail.addEventListener('change', () => {
      settings.detail = detail.value;
      onSetting?.('detail', settings.detail);
      store(SET_KEY, JSON.stringify(settings));
    });
  }

  const qual = $('s-quality');
  if (qual) {
    qual.value = String(settings.quality);
    qual.addEventListener('change', () => {
      settings.quality = Number(qual.value);
      onSetting?.('quality', settings.quality);
      store(SET_KEY, JSON.stringify(settings));
    });
  }

  function wireToggle(id, key) {
    const el = $(id);
    if (!el) return;
    el.checked = settings[key] !== false;
    el.addEventListener('change', () => {
      settings[key] = el.checked;
      onSetting?.(key, settings[key]);
      store(SET_KEY, JSON.stringify(settings));
    });
  }
  wireToggle('s-compass', 'compass');
  wireToggle('s-overview-map', 'overviewMap');
  wireToggle('s-street-names', 'streetNames');

  // Every authored viewpoint, every verified street-control intersection and
  // every structure in the compiled scene — one list, in the Go to tab.  It is
  // complete by construction: the scene, the index and the registry are the
  // same three collections the renderer loaded, rather than a hand-maintained
  // menu that becomes stale when the town grows.  The viewpoints used to be a
  // second, shorter list of the same ground a few rows below this one; a
  // visitor had no way to know which of the two to reach for.
  const jumpTargets = [];
  for (const a of scene?.anchors ?? []) {
    jumpTargets.push({
      kind: 'anchor', id: a.id, label: a.label || a.id,
      search: [a.id, a.label].filter(Boolean).join(' '),
    });
  }
  for (const i of intersections) {
    jumpTargets.push({
      kind: 'intersection', id: i.id, label: i.label || i.id,
      local_e: i.local_e, local_n: i.local_n,
      search: [i.id, i.label, ...(i.search_terms ?? [])].filter(Boolean).join(' '),
    });
  }
  for (const [id, record] of registry?.entries?.() ?? []) {
    const structureSidecar = record.sidecar ?? {};
    jumpTargets.push({
      kind: 'structure', id, label: structureSidecar.name || id,
      // How well the POSITION is attested, straight off the record the popup
      // reads when the visitor arrives.  Not a summary of the building: most
      // of this town is documented in character and placed by argument, and a
      // menu that hid that difference would be the more flattering of the two
      // available lies.
      confidence: structureSidecar.placement?.position_confidence || null,
      search: [id, structureSidecar.name, ...(structureSidecar.aka ?? []),
        structureSidecar.placement?.symbolic_location]
        .filter(Boolean).join(' '),
    });
  }
  const KIND_ORDER = { anchor: 0, intersection: 1, structure: 2 };
  const KIND_GROUP = {
    anchor: 'Viewpoints', intersection: 'Intersections', structure: 'Structures',
  };
  jumpTargets.sort((a, b) => (KIND_ORDER[a.kind] ?? 9) - (KIND_ORDER[b.kind] ?? 9)
    || a.label.localeCompare(b.label));

  const jumpSearch = $('jump-search');
  const jumpResults = $('jump-results');
  const jumpCount = $('jump-count');
  const normal = (value) => String(value ?? '').toLocaleLowerCase().normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');

  function paintJumpResults(query = '') {
    if (!jumpResults) return;
    const terms = normal(query).trim().split(/\s+/).filter(Boolean);
    const matched = jumpTargets.filter((t) => terms.every((word) => normal(t.search).includes(word)));
    jumpResults.replaceChildren();
    if (jumpCount) jumpCount.textContent = terms.length
      ? `${matched.length} of ${jumpTargets.length}` : `${jumpTargets.length} places`;
    if (!matched.length) {
      const empty = document.createElement('p');
      empty.className = 'jump-empty';
      empty.textContent = 'No matching structure or intersection.';
      jumpResults.appendChild(empty);
      return;
    }
    let lastKind = '';
    for (const target of matched) {
      if (target.kind !== lastKind) {
        const heading = document.createElement('p');
        heading.className = 'jump-group';
        heading.textContent = KIND_GROUP[target.kind] ?? target.kind;
        jumpResults.appendChild(heading);
        lastKind = target.kind;
      }
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'jump-result';
      button.dataset.jumpKind = target.kind;
      button.dataset.jumpId = target.id;
      button.setAttribute('role', 'option');
      const name = document.createElement('span');
      name.textContent = target.label;
      button.append(name);
      // Structures carry their position grade into the menu; a viewpoint and a
      // survey junction are not claims about the town and get no chip, because
      // an empty chip would read as a missing grade rather than as a category
      // that has none.
      if (target.kind === 'structure') {
        const grade = target.confidence || 'conjectural';
        button.dataset.jumpConfidence = grade;
        const conf = document.createElement('small');
        conf.className = `conf conf-${grade}`;
        conf.textContent = grade;
        button.append(conf);
      }
      button.addEventListener('click', () => { onGoTo?.(target); setPanel(false); });
      jumpResults.appendChild(button);
    }
  }

  // What the chips add up to, counted from the same list they are painted from
  // rather than typed into the prose beside them. It is not a flattering line
  // and it is the honest summary of where this town stands: not one structure
  // position in it is documented.
  function paintJumpNote() {
    const note = $('jump-note');
    if (!note) return;
    const tally = { documented: 0, inferred: 0, conjectural: 0 };
    let structures = 0;
    for (const target of jumpTargets) {
      if (target.kind !== 'structure') continue;
      structures++;
      const grade = target.confidence || 'conjectural';
      if (grade in tally) tally[grade]++;
    }
    const viewpoints = jumpTargets.filter((t) => t.kind === 'anchor').length;
    const junctions = jumpTargets.filter((t) => t.kind === 'intersection').length;
    note.textContent = `${viewpoints} viewpoints, ${junctions} verified junctions and `
      + `${structures} structures. Of the structure positions, ${tally.documented} are `
      + `documented, ${tally.inferred} inferred and ${tally.conjectural} conjectural.`;
  }
  paintJumpNote();
  jumpSearch?.addEventListener('input', () => paintJumpResults(jumpSearch.value));
  jumpSearch?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const first = jumpResults?.querySelector('.jump-result');
      if (first) { e.preventDefault(); first.click(); }
    }
  });
  paintJumpResults();

  window.addEventListener('keydown', (e) => {
    if (e.target instanceof HTMLInputElement || e.target instanceof HTMLSelectElement) {
      if (e.key === 'Escape' && panelOpen()) setPanel(false);
      return;
    }
    const k = e.key.toLowerCase();
    if (k === 'h' || k === '?') { e.preventDefault(); setPanel(!panelOpen()); }
    else if (k === 'c') { e.preventDefault(); setConfidence(!confidenceOn); }
    else if (k === 'n') { e.preventDefault(); setPanel(true); selectTab('whatsnew'); }
    else if (k === 'g') { e.preventDefault(); openGoTo(); }
    else if (k === 'f') { e.preventDefault(); setFly(!flying); }
    else if (e.key === 'Escape' && panelOpen()) setPanel(false);
  });

  return {
    say,
    settings,
    setPanel,
    showControlHelp,
    dismissControlHelp,
    get confidenceOn() { return confidenceOn; },
    setConfidence,
    get flying() { return flying; },
    setFly,
    setAltitude,
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
