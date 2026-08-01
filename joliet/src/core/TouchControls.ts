import { input, type Action } from './Input';

/**
 * On-screen touch controls.
 *
 * Twin-stick, but tuned for what this game actually is: a slow traversal and
 * observation game, not a shooter. So:
 *
 *  - the move stick FLOATS — it materialises wherever the thumb lands and
 *    tracks from there. A fixed stick forces the player to look at their
 *    hands and pick a spot, which is exactly wrong for a game about looking
 *    at the building.
 *  - sprint is a stick GESTURE (push past the rim), not a button. Holding a
 *    button while steering with the same thumb is miserable.
 *  - the look side is drag-to-look with a low-pass, because raw touch deltas
 *    are jittery and this game is mostly slow pans across dark surfaces.
 *
 * Everything is routed through `Input`'s existing named-action surface
 * (`padMoveX/Y`, `touchDX/Y`, `setTouchAction`), so `Player` needs no changes
 * and never learns that touch exists.
 *
 * Multi-touch is the whole ballgame: move, look and a button must work at the
 * same time, so every finger is tracked by `pointerId` and nothing anywhere
 * assumes there is only one.
 */

/** Thumb travel, in CSS px, from stick centre to full deflection. */
const STICK_RADIUS = 58;
/** Below this fraction of the radius the stick reads as centred. */
const STICK_DEADZONE = 0.16;
/** Push past this fraction of the radius to sprint. */
const SPRINT_AT = 0.85;
/** Knob travel is clamped to the rim; past that the whole stick follows. */
const RECENTRE = true;

export interface TouchControlsOptions {
  /**
   * Called on the first touch anywhere in the layer. Browsers refuse to start
   * an AudioContext outside a user gesture, and on touch the canvas never
   * receives a click because this layer is on top of it.
   */
  onFirstGesture?: () => void;
}

/** The buttons, in cluster order (grid is 2×2, bottom-right). */
const BUTTONS: { action: Action; label: string; key: string }[] = [
  { action: 'flashlight', label: 'Lamp', key: 'lamp' },
  { action: 'jump', label: 'Climb', key: 'climb' },
  { action: 'crouch', label: 'Crouch', key: 'crouch' },
  { action: 'interact', label: 'Use', key: 'use' },
];

/**
 * True only for devices that have touch and NO precise pointer.
 *
 * A laptop with a touchscreen still reports a fine pointer and hover, and must
 * keep the mouse path — showing it thumb sticks would be worse than useless.
 * `?touch` forces the layer on for testing, `?touch=0` forces it off.
 */
export function isTouchDevice(): boolean {
  const q = typeof location !== 'undefined' ? new URLSearchParams(location.search).get('touch') : null;
  if (q !== null) return q !== '0' && q !== 'false';

  const hasTouch =
    (typeof navigator !== 'undefined' && navigator.maxTouchPoints > 0) ||
    (typeof window !== 'undefined' && 'ontouchstart' in window);
  if (!hasTouch) return false;
  if (typeof matchMedia !== 'function') return false;
  return matchMedia('(pointer: coarse)').matches || matchMedia('(hover: none)').matches;
}

export class TouchControls {
  private root!: HTMLElement;
  private stick!: HTMLElement;
  private knob!: HTMLElement;
  private buttonEls = new Map<string, HTMLElement>();

  /** The finger driving the move stick, if any. */
  private moveId: number | null = null;
  private moveOx = 0;
  private moveOy = 0;

  /** The finger driving look, if any. */
  private lookId: number | null = null;
  private lookLx = 0;
  private lookLy = 0;

  /** pointerId → the action that finger is holding down. */
  private buttonPointers = new Map<number, Action>();

  private mounted = false;
  private visible = false;
  private firstGestureFired = false;

  constructor(private opts: TouchControlsOptions = {}) {}

  mount(): void {
    if (this.mounted) return;
    this.mounted = true;

    document.documentElement.classList.add('is-touch');

    const root = document.createElement('div');
    root.id = 'touch';
    root.className = 'touch';
    root.setAttribute('hidden', '');
    root.innerHTML = `
      <div class="touch-zone touch-move" data-zone="move" aria-hidden="true"></div>
      <div class="touch-zone touch-look" data-zone="look" aria-hidden="true"></div>
      <div class="touch-stick" id="touch-stick"><i class="touch-knob" id="touch-knob"></i></div>
      <div class="touch-buttons">
        ${BUTTONS.map(
          (b) =>
            `<button type="button" class="tbtn" data-touch-action="${b.action}" data-key="${b.key}">${b.label}</button>`,
        ).join('')}
      </div>
      <button type="button" class="tbtn tbtn-pause" data-touch-action="pause"
              data-key="pause" aria-label="Pause and settings">❚❚</button>
      <p class="touch-hint" id="touch-hint">Left half moves · right half looks · push the stick to run</p>
    `;
    document.body.appendChild(root);

    this.root = root;
    this.stick = root.querySelector('#touch-stick') as HTMLElement;
    this.knob = root.querySelector('#touch-knob') as HTMLElement;
    for (const b of [...BUTTONS, { action: 'pause' as Action, label: 'Pause', key: 'pause' }]) {
      const el = root.querySelector(`[data-key="${b.key}"]`) as HTMLElement;
      if (el) this.buttonEls.set(b.key, el);
    }

    // pointerdown on the layer; move/up on the window so a finger that slides
    // out of its zone (or off the screen edge) keeps being tracked.
    root.addEventListener('pointerdown', this.onDown, { passive: false });
    addEventListener('pointermove', this.onMove, { passive: false });
    addEventListener('pointerup', this.onUp, { passive: false });
    addEventListener('pointercancel', this.onUp, { passive: false });
    // `touch-action: none` handles scroll and double-tap zoom on modern
    // engines; these two close the gaps left on iOS Safari.
    root.addEventListener('touchmove', prevent, { passive: false });
    document.addEventListener('gesturestart', prevent, { passive: false });
    addEventListener('contextmenu', this.onContextMenu);
    addEventListener('blur', this.releaseAll);

    input.touchActive = true;
  }

  /** Show the controls. Kept hidden behind the loading screen. */
  setVisible(on: boolean): void {
    this.visible = on;
    if (!this.mounted) return;
    if (on) {
      this.root.removeAttribute('hidden');
      this.root.classList.add('on');
      // Fade the hint out once, a few seconds in.
      setTimeout(() => this.root.querySelector('#touch-hint')?.classList.add('gone'), 6500);
    } else {
      this.root.classList.remove('on');
      this.root.setAttribute('hidden', '');
      this.releaseAll();
    }
  }

  dispose(): void {
    if (!this.mounted) return;
    this.releaseAll();
    this.root.removeEventListener('pointerdown', this.onDown);
    removeEventListener('pointermove', this.onMove);
    removeEventListener('pointerup', this.onUp);
    removeEventListener('pointercancel', this.onUp);
    document.removeEventListener('gesturestart', prevent);
    removeEventListener('contextmenu', this.onContextMenu);
    removeEventListener('blur', this.releaseAll);
    this.root.remove();
    document.documentElement.classList.remove('is-touch');
    input.touchActive = false;
    this.mounted = false;
  }

  // ----------------------------------------------------------- pointers ---

  private onDown = (e: PointerEvent): void => {
    if (!this.visible) return;
    const target = e.target as HTMLElement | null;

    if (!this.firstGestureFired) {
      this.firstGestureFired = true;
      this.opts.onFirstGesture?.();
    }

    const btn = target?.closest?.('[data-touch-action]') as HTMLElement | null;
    if (btn) {
      e.preventDefault();
      const action = btn.dataset.touchAction as Action;
      this.buttonPointers.set(e.pointerId, action);
      btn.classList.add('on');
      // Capture so the release lands on the button even if the thumb rolls
      // off it, which on a 64 px target happens constantly.
      try {
        btn.setPointerCapture(e.pointerId);
      } catch {
        /* capture is an optimisation, not a requirement */
      }
      input.setTouchAction(action, true);
      return;
    }

    const zone = target?.closest?.('[data-zone]') as HTMLElement | null;
    const kind = zone?.dataset.zone;
    if (kind === 'move') {
      if (this.moveId !== null) return; // a second finger on the move side is not a second stick
      e.preventDefault();
      this.moveId = e.pointerId;
      this.moveOx = e.clientX;
      this.moveOy = e.clientY;
      this.placeStick(e.clientX, e.clientY);
      this.stick.classList.add('on');
      this.applyStick(0, 0);
    } else if (kind === 'look') {
      if (this.lookId !== null) return;
      e.preventDefault();
      this.lookId = e.pointerId;
      this.lookLx = e.clientX;
      this.lookLy = e.clientY;
    }
  };

  private onMove = (e: PointerEvent): void => {
    if (e.pointerId === this.moveId) {
      e.preventDefault();
      let dx = e.clientX - this.moveOx;
      let dy = e.clientY - this.moveOy;
      const dist = Math.hypot(dx, dy);
      if (dist > STICK_RADIUS) {
        if (RECENTRE) {
          // Drag the origin along behind the thumb so a long push does not
          // walk the stick off under the palm.
          const pull = dist - STICK_RADIUS;
          this.moveOx += (dx / dist) * pull;
          this.moveOy += (dy / dist) * pull;
          this.placeStick(this.moveOx, this.moveOy);
        }
        dx = (dx / dist) * STICK_RADIUS;
        dy = (dy / dist) * STICK_RADIUS;
      }
      this.applyStick(dx, dy);
      return;
    }

    if (e.pointerId === this.lookId) {
      e.preventDefault();
      input.touchDX += e.clientX - this.lookLx;
      input.touchDY += e.clientY - this.lookLy;
      this.lookLx = e.clientX;
      this.lookLy = e.clientY;
      return;
    }

    // Buttons keep their own finger; nothing to do while it is held.
  };

  private onUp = (e: PointerEvent): void => {
    if (e.pointerId === this.moveId) {
      this.moveId = null;
      this.stick.classList.remove('on', 'sprint');
      this.applyStick(0, 0);
      input.setTouchAction('sprint', false);
      return;
    }
    if (e.pointerId === this.lookId) {
      this.lookId = null;
      return;
    }
    const action = this.buttonPointers.get(e.pointerId);
    if (action !== undefined) {
      this.buttonPointers.delete(e.pointerId);
      input.setTouchAction(action, false);
      const el = this.root.querySelector(`[data-touch-action="${action}"]`);
      el?.classList.remove('on');
    }
  };

  private onContextMenu = (e: Event): void => {
    // A long press on a control must not open the iOS/Android callout.
    if (this.visible && (e.target as HTMLElement | null)?.closest?.('#touch')) e.preventDefault();
  };

  private releaseAll = (): void => {
    this.moveId = null;
    this.lookId = null;
    for (const action of this.buttonPointers.values()) input.setTouchAction(action, false);
    this.buttonPointers.clear();
    for (const el of this.buttonEls.values()) el.classList.remove('on');
    this.stick?.classList.remove('on', 'sprint');
    this.applyStick(0, 0);
    input.setTouchAction('sprint', false);
    input.touchDX = 0;
    input.touchDY = 0;
  };

  // -------------------------------------------------------------- stick ---

  private placeStick(x: number, y: number): void {
    this.stick.style.left = `${x}px`;
    this.stick.style.top = `${y}px`;
  }

  /**
   * Deflection in px → normalised stick, using the same shaping as the
   * gamepad path in `Input.pollGamepad`: deadzone, rescale so the rim still
   * reaches 1.0, then square it for fine control at low speed. Applied
   * radially rather than per-axis, because a thumb on glass has no axes.
   */
  private applyStick(dx: number, dy: number): void {
    const raw = Math.min(1, Math.hypot(dx, dy) / STICK_RADIUS);

    let out = 0;
    if (raw > STICK_DEADZONE) {
      const s = (raw - STICK_DEADZONE) / (1 - STICK_DEADZONE);
      out = s * s;
    }
    const nx = raw > 0 ? dx / STICK_RADIUS / Math.max(raw, 1e-6) : 0;
    const ny = raw > 0 ? dy / STICK_RADIUS / Math.max(raw, 1e-6) : 0;

    // Written to the touch fields rather than padMoveX/Y directly: the gamepad
    // poll runs first every frame and zeroes the pad axes when no pad is
    // connected, which would wipe the stick before Player ever read it.
    // `Input.update()` folds these into padMoveX/Y afterwards.
    input.touchMoveX = nx * out;
    // Screen-down is +y; the gamepad's forward is -y. Same convention, so
    // Player's `iz -= padMoveY` needs nothing special.
    input.touchMoveY = ny * out;

    const sprinting = raw >= SPRINT_AT;
    input.setTouchAction('sprint', sprinting);
    this.stick.classList.toggle('sprint', sprinting);

    this.knob.style.transform = `translate(${dx}px, ${dy}px)`;
  }
}

function prevent(e: Event): void {
  if (e.cancelable) e.preventDefault();
}
