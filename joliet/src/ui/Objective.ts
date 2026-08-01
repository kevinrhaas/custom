import { settings } from '../core/Settings';
import { SCENE_CHOICES } from './TitleScreen';

/**
 * The persistent objective readout.
 *
 * The goal used to appear for seven seconds on entering a scene and then
 * vanish forever, which is no use to anyone who looked away or spent more than
 * seven seconds thinking. Standard practice — and the reasonable expectation —
 * is that the current objective stays available and can be dismissed by
 * players who don't want it.
 */

let root: HTMLElement | null = null;
let current = '';

export function mountObjective(sceneKey: string): void {
  const choice = SCENE_CHOICES.find((s) => s.key === sceneKey);
  if (!choice) return;
  const ui = document.getElementById('ui');
  if (!ui || root) return;

  current = choice.objective;
  root = document.createElement('div');
  root.id = 'objhud';
  root.className = 'objhud';
  root.innerHTML = `
    <span class="objhud-label">Objective</span>
    <span class="objhud-text" id="objhud-text">${current}</span>`;
  ui.appendChild(root);
  apply();
  settings.subscribe(apply);
}

/** Scenes call this as the player makes progress. */
export function setObjective(text: string): void {
  current = text;
  const el = document.getElementById('objhud-text');
  if (el) el.textContent = text;
}

function apply(): void {
  root?.classList.toggle('off', !settings.get().showObjective);
}

export function toggleObjective(): void {
  settings.set('showObjective', !settings.get().showObjective);
}
