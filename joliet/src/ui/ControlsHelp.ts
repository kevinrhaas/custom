import { settings } from '../core/Settings';
import { isTouchDevice } from '../core/TouchControls';

/**
 * The always-available control reminder.
 *
 * Reported straight after the title screen landed: "I can't remember the
 * controls." Putting them on a screen you see once and then never again is
 * only marginally better than not having them — the moment you need them is
 * three minutes later, in the dark, mid-corridor.
 *
 * So it lives in the corner, on by default, toggled with `H`, and persisted.
 * Anyone who finds it noise turns it off once and never sees it again.
 */

const DESKTOP: [string, string][] = [
  ['W A S D', 'Move'],
  ['Shift', 'Run'],
  ['C', 'Crouch'],
  ['Z', 'Crawl'],
  ['Space', 'Climb'],
  ['F', 'Headlamp'],
  ['E', 'Interact'],
  ['H', 'Hide this'],
  ['Esc', 'Pause'],
];

const TOUCH: [string, string][] = [
  ['Left', 'Move'],
  ['Right', 'Look'],
  ['Push stick', 'Run'],
  ['Lamp', 'Headlamp'],
  ['❚❚', 'Pause'],
];

let root: HTMLElement | null = null;

export function mountControlsHelp(): void {
  const ui = document.getElementById('ui');
  if (!ui || root) return;

  const rows = isTouchDevice() ? TOUCH : DESKTOP;
  root = document.createElement('div');
  root.id = 'ctrlhelp';
  root.className = 'ctrlhelp';
  root.innerHTML = `
    <ul>${rows.map(([k, v]) => `<li><kbd>${k}</kbd><span>${v}</span></li>`).join('')}</ul>`;
  ui.appendChild(root);

  apply();
  settings.subscribe(apply);
}

function apply(): void {
  if (!root) return;
  root.classList.toggle('off', !settings.get().showControlsHelp);
}

/** Bound to `H`. */
export function toggleControlsHelp(): void {
  settings.set('showControlsHelp', !settings.get().showControlsHelp);
}
