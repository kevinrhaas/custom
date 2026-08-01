import { settings, type Settings } from '../core/Settings';

/**
 * Pause menu and settings.
 *
 * This exists because `Settings.ts` had a complete accessibility store —
 * sensitivity, FOV, head-bob, motion blur, subtitles, colourblind modes,
 * reduced motion — and **no way to change any of it**. Every option was
 * reachable only by hand-editing localStorage. Documenting accessibility
 * options in a settings module and shipping no UI for them is the same as not
 * having them, and it is worse than not having them because it looks done.
 *
 * Kept deliberately plain: sliders and checkboxes, generous hit targets, real
 * labels, keyboard reachable. No custom widgets — the point is that it works,
 * including for the people the options exist for.
 */

type Row =
  | { kind: 'slider'; key: keyof Settings; label: string; min: number; max: number; step: number; hint?: string }
  | { kind: 'toggle'; key: keyof Settings; label: string; hint?: string }
  | { kind: 'select'; key: keyof Settings; label: string; options: [string, string][]; hint?: string }
  | { kind: 'heading'; label: string };

const ROWS: Row[] = [
  { kind: 'heading', label: 'Camera' },
  { kind: 'slider', key: 'sensitivity', label: 'Look sensitivity', min: 0.05, max: 1, step: 0.01 },
  { kind: 'slider', key: 'fov', label: 'Field of view', min: 60, max: 100, step: 1 },
  { kind: 'toggle', key: 'invertY', label: 'Invert vertical look' },

  {
    kind: 'slider',
    key: 'moveSpeedScale',
    label: 'Movement speed',
    min: 0.75,
    max: 2,
    step: 0.05,
    hint: 'Scales walking, crouching and running together.',
  },
  { kind: 'toggle', key: 'showControlsHelp', label: 'Show controls on screen', hint: 'Or press H.' },

  { kind: 'heading', label: 'Comfort' },
  {
    kind: 'toggle',
    key: 'reducedMotion',
    label: 'Reduced motion',
    hint: 'Turns off motion blur and most head movement.',
  },
  {
    kind: 'slider',
    key: 'headBob',
    label: 'Head bob',
    min: 0,
    max: 1,
    step: 0.05,
    hint: 'Zero is completely still.',
  },
  { kind: 'slider', key: 'motionBlur', label: 'Motion blur', min: 0, max: 1, step: 0.05 },
  { kind: 'slider', key: 'filmGrain', label: 'Film grain', min: 0, max: 1, step: 0.05 },
  { kind: 'slider', key: 'vignette', label: 'Vignette', min: 0, max: 1, step: 0.05 },
  { kind: 'toggle', key: 'cameraLean', label: 'Camera lean' },

  { kind: 'heading', label: 'Accessibility' },
  { kind: 'toggle', key: 'subtitles', label: 'Subtitles' },
  { kind: 'toggle', key: 'speakerNames', label: 'Show speaker names' },
  { kind: 'slider', key: 'subtitleSize', label: 'Subtitle size', min: 0.8, max: 2, step: 0.1 },
  {
    kind: 'toggle',
    key: 'highContrastPrompts',
    label: 'High-contrast prompts',
  },
  {
    kind: 'toggle',
    key: 'visualAudioCues',
    label: 'Visual cues for sounds',
    hint: 'No puzzle in this game is gated on audio alone.',
  },
  {
    kind: 'select',
    key: 'colorblind',
    label: 'Colour vision',
    options: [
      ['none', 'Default'],
      ['protan', 'Protanopia'],
      ['deutan', 'Deuteranopia'],
      ['tritan', 'Tritanopia'],
    ],
  },

  { kind: 'heading', label: 'Assist' },
  {
    kind: 'toggle',
    key: 'traversalAssist',
    label: 'Traversal assist',
    hint: 'Forgiving hitboxes and ledge snapping.',
  },
  {
    kind: 'slider',
    key: 'hintDelaySeconds',
    label: 'Hint delay (seconds)',
    min: 20,
    max: 240,
    step: 10,
    hint: 'How long before a nudge appears if you are stuck.',
  },

  { kind: 'heading', label: 'Graphics' },
  {
    kind: 'select',
    key: 'quality',
    label: 'Quality',
    options: [
      ['low', 'Low'],
      ['medium', 'Medium'],
      ['high', 'High'],
      ['ultra', 'Ultra'],
    ],
  },
  { kind: 'slider', key: 'resolutionScale', label: 'Resolution scale', min: 0.5, max: 1, step: 0.05 },

  { kind: 'heading', label: 'Audio' },
  { kind: 'slider', key: 'masterVolume', label: 'Master', min: 0, max: 1, step: 0.05 },
  { kind: 'slider', key: 'sfxVolume', label: 'Effects', min: 0, max: 1, step: 0.05 },
  { kind: 'slider', key: 'voiceVolume', label: 'Voice', min: 0, max: 1, step: 0.05 },
  { kind: 'slider', key: 'musicVolume', label: 'Ambience', min: 0, max: 1, step: 0.05 },
];

let root: HTMLElement | null = null;
let onResume: (() => void) | null = null;

export function mountPauseMenu(resume: () => void): void {
  onResume = resume;
  const ui = document.getElementById('ui');
  if (!ui || root) return;

  root = document.createElement('div');
  root.id = 'pause';
  root.className = 'pause';
  root.setAttribute('hidden', '');
  root.setAttribute('role', 'dialog');
  root.setAttribute('aria-modal', 'true');
  root.setAttribute('aria-label', 'Paused');

  root.innerHTML = `
    <div class="pause-panel">
      <header class="pause-head">
        <h2>Paused</h2>
        <button type="button" class="pause-resume" id="pause-resume">Resume</button>
      </header>
      <div class="pause-body">${ROWS.map(renderRow).join('')}</div>
      <footer class="pause-foot">
        <button type="button" class="pause-reset" id="pause-reset">Reset to defaults</button>
        <span class="pause-note">Settings save automatically.</span>
      </footer>
    </div>`;
  ui.appendChild(root);

  root.querySelector('#pause-resume')?.addEventListener('click', () => onResume?.());
  root.querySelector('#pause-reset')?.addEventListener('click', () => {
    settings.reset();
    syncInputs();
  });

  root.addEventListener('input', (e) => {
    const el = e.target as HTMLInputElement | HTMLSelectElement;
    const key = el.dataset.key as keyof Settings | undefined;
    if (!key) return;
    if (el instanceof HTMLInputElement && el.type === 'checkbox') {
      settings.set(key, el.checked as never);
    } else if (el instanceof HTMLInputElement) {
      settings.set(key, Number(el.value) as never);
    } else {
      settings.set(key, el.value as never);
    }
    syncInputs();
    applyDocumentFlags();
  });

  settings.subscribe(applyDocumentFlags);
  applyDocumentFlags();
}

function renderRow(r: Row): string {
  if (r.kind === 'heading') return `<h3 class="pause-h3">${r.label}</h3>`;
  const s = settings.get();
  const id = `set-${String(r.key)}`;
  const hint = r.hint ? `<span class="pause-hint">${r.hint}</span>` : '';

  if (r.kind === 'toggle') {
    return `<label class="pause-row" for="${id}">
      <span class="pause-label">${r.label}${hint}</span>
      <input type="checkbox" id="${id}" data-key="${String(r.key)}" ${s[r.key] ? 'checked' : ''}>
    </label>`;
  }
  if (r.kind === 'select') {
    return `<label class="pause-row" for="${id}">
      <span class="pause-label">${r.label}${hint}</span>
      <select id="${id}" data-key="${String(r.key)}">
        ${r.options.map(([v, t]) => `<option value="${v}" ${s[r.key] === v ? 'selected' : ''}>${t}</option>`).join('')}
      </select>
    </label>`;
  }
  return `<label class="pause-row" for="${id}">
    <span class="pause-label">${r.label}${hint}</span>
    <span class="pause-slider">
      <input type="range" id="${id}" data-key="${String(r.key)}"
             min="${r.min}" max="${r.max}" step="${r.step}" value="${String(s[r.key])}">
      <output data-out="${String(r.key)}">${fmt(s[r.key])}</output>
    </span>
  </label>`;
}

function fmt(v: unknown): string {
  return typeof v === 'number' ? (Number.isInteger(v) ? String(v) : v.toFixed(2)) : String(v);
}

function syncInputs(): void {
  if (!root) return;
  const s = settings.get();
  for (const el of root.querySelectorAll<HTMLInputElement | HTMLSelectElement>('[data-key]')) {
    const key = el.dataset.key as keyof Settings;
    const v = s[key];
    if (el instanceof HTMLInputElement && el.type === 'checkbox') el.checked = Boolean(v);
    else el.value = String(v);
  }
  for (const out of root.querySelectorAll<HTMLOutputElement>('[data-out]')) {
    out.textContent = fmt(s[out.dataset.out as keyof Settings]);
  }
}

/** Push settings that CSS cares about onto the document element. */
function applyDocumentFlags(): void {
  const s = settings.get();
  const de = document.documentElement;
  de.dataset.contrast = s.highContrastPrompts ? 'high' : 'normal';
  de.dataset.colorblind = s.colorblind;
  de.style.setProperty('--subtitle-scale', String(s.subtitleSize));
}

export function showPause(): void {
  root?.removeAttribute('hidden');
  syncInputs();
  (root?.querySelector('#pause-resume') as HTMLElement | null)?.focus();
}

export function hidePause(): void {
  root?.setAttribute('hidden', '');
}
