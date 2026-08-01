import { settings } from '../core/Settings';
import type { Player } from '../core/Player';

/**
 * The stuck-detector.
 *
 * `docs/DESIGN.md` specifies "a contextual hint surfaces after 3 failures or
 * 90 s of no progress" as part of operationalising "fun and not too hard". It
 * was never built, and the first player spent a long time in the Void unable
 * to work out how to leave.
 *
 * Progress is measured as distance covered from the last place a hint fired.
 * Standing still, or circling a small area, both read as stuck — which they
 * are.
 */

const HINTS: Record<string, string[]> = {
  perimeter: [
    'Three ways through the wall: the drainage trench east, a breach in the stonework west, and the maintenance gate. The trench is the easiest.',
    'The trench is the dark cut in the ground away from the lamp — the light is a landmark, not the way in.',
  ],
  cellblocks: [
    'The stairs against the window wall climb to the upper tiers. Walk onto the landing at the foot of a flight first.',
    'The gallery runs the length of the hall. There is nothing to solve here — it is a place to look at.',
  ],
  void: [
    'There is no exit yet. This chamber is a dead end in the current build — the names on the walls are the whole of it. Press Esc to go back to the menu.',
    'Try the walls rather than the rubble. The carvings are on the stone at head height, and the headlamp is on F.',
  ],
  powerhouse: [
    'Two ducts leave the south wall. One is labelled No. 1 in cast iron from 1901; the other is stencilled No. 1 in paint. Only one of them still goes anywhere.',
    'The cast plate was true when it was made. Look at which duct has cable still running through it.',
  ],
};

let root: HTMLElement | null = null;
let idx = 0;
let sinceProgress = 0;
let lastPos = { x: 0, z: 0 };
let sceneKey = '';

export function mountHints(scene: string): void {
  sceneKey = scene;
  idx = 0;
  sinceProgress = 0;
  const ui = document.getElementById('ui');
  if (!ui || root) return;
  root = document.createElement('div');
  root.className = 'hint';
  root.setAttribute('hidden', '');
  ui.appendChild(root);
}

export function updateHints(dt: number, player: Player): void {
  if (!root || !settings.get().hintsEnabled) return;
  const list = HINTS[sceneKey];
  if (!list || idx >= list.length) return;

  const p = player.position;
  const moved = Math.hypot(p.x - lastPos.x, p.z - lastPos.z);
  if (moved > 12) {
    // Real progress — reset the clock and move the reference point.
    lastPos = { x: p.x, z: p.z };
    sinceProgress = 0;
    return;
  }

  sinceProgress += dt;
  if (sinceProgress >= settings.get().hintDelaySeconds) {
    show(list[idx]);
    idx++;
    sinceProgress = 0;
    lastPos = { x: p.x, z: p.z };
  }
}

function show(text: string): void {
  if (!root) return;
  root.innerHTML = `<span class="hint-label">Stuck?</span><span>${text}</span>`;
  root.removeAttribute('hidden');
  root.classList.add('on');
  setTimeout(() => root?.classList.remove('on'), 13000);
  setTimeout(() => root?.setAttribute('hidden', ''), 14000);
}
