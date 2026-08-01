/**
 * Title screen, location select and controls.
 *
 * This exists because the game shipped without it and the first person to play
 * it could not tell where to start. Three scenes had been built and the app
 * dropped you straight into a dark corridor with no title, no objective and no
 * controls — every piece of information a player needs to begin was in the
 * repository's README instead of on the screen.
 *
 * The lesson is not "add a menu". It is that "does it render" and "can someone
 * play it" are different questions, and only the first one was ever being
 * asked.
 */

import { isTouchDevice } from '../core/TouchControls';

export interface SceneChoice {
  key: string;
  title: string;
  /** Where it sits in the story. */
  chapter: string;
  /** What the player is there to do. */
  objective: string;
  blurb: string;
}

export const SCENE_CHOICES: SceneChoice[] = [
  {
    key: 'perimeter',
    title: 'Perimeter Approach',
    chapter: 'Act I · 00:14',
    objective: 'Find a way inside.',
    blurb:
      'Collins Street, past midnight. Ten metres of limestone between you and the yard, ' +
      'and three ways through it: a drainage trench, a breach at the old quarry cut, ' +
      'and a maintenance gate. Start here — nothing in this scene can hurt you.',
  },
  {
    key: 'cellblocks',
    title: 'The Cellblocks',
    chapter: 'Act III · 02:40',
    objective: 'Cross the gallery. Listen to the building.',
    blurb:
      'The East cell house. Four tiers, four hundred cells, and steel grating underfoot ' +
      'that carries every step the length of the hall. The showpiece — and the place ' +
      'where the drawings and the scan stop agreeing with each other.',
  },
  {
    key: 'void',
    title: 'The Void',
    chapter: 'Act III · 03:55',
    objective: 'Read the names cut into the walls.',
    blurb:
      'Beneath the east block, behind a wall somebody bricked up and then removed from ' +
      'the record. Hand-cut stone, quarried by the men who were kept above it. ' +
      'Nothing down here will hurt you. Read the carvings — that is the whole of ' +
      'it, and there is no exit yet: Esc takes you back to the menu.',
  },
];

let root: HTMLElement | null = null;
let onStart: ((key: string) => void) | null = null;

export function mountTitleScreen(start: (key: string) => void): void {
  onStart = start;
  const ui = document.getElementById('ui');
  if (!ui) return;

  const touch = isTouchDevice();
  root = document.createElement('div');
  root.id = 'title';
  root.className = 'title';
  root.innerHTML = `
    <div class="title-inner">
      <header class="title-head">
        <div class="title-mark" aria-hidden="true"><span></span><span></span><span></span><span></span></div>
        <h1>Joliet</h1>
        <p class="title-sub">Midnight Infiltration</p>
        <p class="title-tag">
          Old Joliet Prison, 1125 Collins Street. Closed 2002.<br>
          There are no weapons in this game and nothing is chasing you.
        </p>
      </header>

      <section class="title-scenes" aria-label="Choose a location">
        <h2 class="title-h2">Choose a location</h2>
        <div class="title-grid">
          ${SCENE_CHOICES.map(
            (s, i) => `
            <button type="button" class="scene-card" data-scene="${s.key}" ${i === 0 ? 'autofocus' : ''}>
              <span class="scene-chapter">${s.chapter}</span>
              <span class="scene-title">${s.title}</span>
              <span class="scene-objective">${s.objective}</span>
              <span class="scene-blurb">${s.blurb}</span>
              <span class="scene-go">Enter →</span>
            </button>`,
          ).join('')}
        </div>
        <p class="title-note">
          The three locations are not yet connected — there is no walk between them.
          Pick one and it loads on its own.
        </p>
      </section>

      <section class="title-controls" aria-label="Controls">
        <h2 class="title-h2">Controls</h2>
        ${touch ? touchControlsHtml() : desktopControlsHtml()}
      </section>

      <footer class="title-foot">
        <p>A fictional story set in a real, protected historic place.
        The prison is a museum and runs public tours — that is the way in.</p>
      </footer>
    </div>`;
  ui.appendChild(root);

  for (const btn of root.querySelectorAll<HTMLElement>('[data-scene]')) {
    btn.addEventListener('click', () => {
      const key = btn.dataset.scene!;
      hideTitleScreen();
      onStart?.(key);
    });
  }
}

function desktopControlsHtml(): string {
  const rows: [string, string][] = [
    ['W A S D', 'Move'],
    ['Mouse', 'Look'],
    ['Shift', 'Run'],
    ['C', 'Crouch'],
    ['Z', 'Crawl'],
    ['Space', 'Climb / vault'],
    ['F', 'Headlamp on / off'],
    ['E', 'Interact'],
    ['Esc', 'Pause & settings'],
  ];
  return `
    <ul class="ctrl-list">
      ${rows.map(([k, v]) => `<li><kbd>${k}</kbd><span>${v}</span></li>`).join('')}
    </ul>
    <p class="ctrl-hint">
      Click the screen once to capture the mouse; <kbd>Esc</kbd> releases it.
      These stay in the corner while you play — <kbd>H</kbd> hides them.
      Movement speed is adjustable in <kbd>Esc</kbd> → Pause.
    </p>`;
}

function touchControlsHtml(): string {
  const rows: [string, string][] = [
    ['Left half', 'Drag to move'],
    ['Right half', 'Drag to look'],
    ['Push the stick', 'Run'],
    ['Lamp', 'Headlamp on / off'],
    ['Crouch', 'Crouch'],
    ['Climb', 'Climb / vault'],
    ['❚❚ top right', 'Pause & settings'],
  ];
  return `
    <ul class="ctrl-list">
      ${rows.map(([k, v]) => `<li><kbd>${k}</kbd><span>${v}</span></li>`).join('')}
    </ul>
    <p class="ctrl-hint">Turn your sound on — this game is mostly listening.</p>`;
}

export function hideTitleScreen(): void {
  root?.classList.add('gone');
  setTimeout(() => root?.setAttribute('hidden', ''), 420);
}

export function showTitleScreen(): void {
  root?.removeAttribute('hidden');
  root?.classList.remove('gone');
}

/** The objective banner that appears for a few seconds on entering a scene. */
export function showObjective(sceneKey: string): void {
  const choice = SCENE_CHOICES.find((s) => s.key === sceneKey);
  if (!choice) return;
  const ui = document.getElementById('ui');
  if (!ui) return;

  const el = document.createElement('div');
  el.className = 'objective';
  el.innerHTML = `
    <span class="obj-chapter">${choice.chapter}</span>
    <span class="obj-title">${choice.title}</span>
    <span class="obj-line">${choice.objective}</span>`;
  ui.appendChild(el);

  requestAnimationFrame(() => el.classList.add('on'));
  setTimeout(() => el.classList.remove('on'), 7000);
  setTimeout(() => el.remove(), 8200);
}
