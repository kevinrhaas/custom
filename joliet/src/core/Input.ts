import { settings } from './Settings';

/**
 * Unified keyboard + mouse + gamepad input.
 *
 * Everything downstream reads *actions*, never raw keys, so remapping is a
 * data change. Pointer lock is the mouse-look gate; the game never reads mouse
 * deltas while unlocked.
 */

export type Action =
  | 'forward'
  | 'back'
  | 'left'
  | 'right'
  | 'sprint'
  | 'crouch'
  | 'prone'
  | 'jump'
  | 'interact'
  | 'flashlight'
  | 'scan'
  | 'ability'
  | 'journal'
  | 'leanLeft'
  | 'leanRight'
  | 'pause';

export type Binding = { keys: string[]; pad?: number; padAxis?: never };

const DEFAULT_BINDINGS: Record<Action, Binding> = {
  forward: { keys: ['KeyW', 'ArrowUp'] },
  back: { keys: ['KeyS', 'ArrowDown'] },
  left: { keys: ['KeyA', 'ArrowLeft'] },
  right: { keys: ['KeyD', 'ArrowRight'] },
  sprint: { keys: ['ShiftLeft', 'ShiftRight'], pad: 10 },
  crouch: { keys: ['KeyC', 'ControlLeft'], pad: 1 },
  prone: { keys: ['KeyZ'], pad: 11 },
  jump: { keys: ['Space'], pad: 0 },
  interact: { keys: ['KeyE'], pad: 2 },
  flashlight: { keys: ['KeyF'], pad: 3 },
  scan: { keys: ['KeyQ'], pad: 4 },
  ability: { keys: ['KeyR'], pad: 5 },
  journal: { keys: ['Tab'], pad: 8 },
  leanLeft: { keys: ['KeyQ'] },
  leanRight: { keys: ['KeyE'] },
  pause: { keys: ['Escape'], pad: 9 },
};

const BINDINGS_KEY = 'joliet.bindings.v1';

class InputManager {
  private down = new Set<string>();
  private pressedThisFrame = new Set<Action>();
  private heldActions = new Set<Action>();
  private prevHeld = new Set<Action>();
  private bindings: Record<Action, Binding> = structuredClone(DEFAULT_BINDINGS);

  /** Accumulated mouse delta since last consume(), in raw pixels. */
  mouseDX = 0;
  mouseDY = 0;
  /** Right-stick look, normalised -1..1, already deadzoned. */
  padLookX = 0;
  padLookY = 0;
  /** Left-stick move, normalised -1..1, already deadzoned. */
  padMoveX = 0;
  padMoveY = 0;

  locked = false;
  private canvas: HTMLCanvasElement | null = null;
  private padIndex: number | null = null;
  private prevPadButtons: boolean[] = [];

  attach(canvas: HTMLCanvasElement): void {
    this.canvas = canvas;
    this.loadBindings();

    addEventListener('keydown', this.onKeyDown, { passive: false });
    addEventListener('keyup', this.onKeyUp);
    addEventListener('blur', this.onBlur);
    document.addEventListener('pointerlockchange', this.onLockChange);
    canvas.addEventListener('mousemove', this.onMouseMove);
    canvas.addEventListener('mousedown', this.onMouseDown);

    addEventListener('gamepadconnected', (e) => {
      this.padIndex = (e as GamepadEvent).gamepad.index;
    });
    addEventListener('gamepaddisconnected', () => {
      this.padIndex = null;
    });
  }

  requestLock(): void {
    this.canvas?.requestPointerLock?.();
  }

  releaseLock(): void {
    if (document.pointerLockElement) document.exitPointerLock();
  }

  /** True while the action is held. */
  held(a: Action): boolean {
    return this.heldActions.has(a);
  }

  /** True only on the frame the action went down. */
  pressed(a: Action): boolean {
    return this.pressedThisFrame.has(a);
  }

  /** Returns the mouse delta and zeroes the accumulator. */
  consumeLook(): { x: number; y: number } {
    const sens = settings.get().sensitivity;
    const inv = settings.get().invertY ? -1 : 1;
    // Mouse is raw pixels; pad is per-second so it gets scaled by the caller.
    const x = this.mouseDX * sens * 0.0022 + this.padLookX * sens * 0.05;
    const y = (this.mouseDY * sens * 0.0022 + this.padLookY * sens * 0.05) * inv;
    this.mouseDX = 0;
    this.mouseDY = 0;
    return { x, y };
  }

  /** Call once per frame, before any held()/pressed() reads. */
  update(): void {
    this.pollGamepad();

    this.prevHeld = new Set(this.heldActions);
    this.heldActions.clear();
    for (const action of Object.keys(this.bindings) as Action[]) {
      const b = this.bindings[action];
      if (b.keys.some((k) => this.down.has(k))) this.heldActions.add(action);
    }
    // Gamepad buttons fold into the same held set.
    const pad = this.getPad();
    if (pad) {
      for (const action of Object.keys(this.bindings) as Action[]) {
        const idx = this.bindings[action].pad;
        if (idx !== undefined && pad.buttons[idx]?.pressed) {
          this.heldActions.add(action);
        }
      }
    }

    this.pressedThisFrame.clear();
    for (const a of this.heldActions) {
      if (!this.prevHeld.has(a)) this.pressedThisFrame.add(a);
    }
  }

  rebind(action: Action, keys: string[]): void {
    this.bindings[action] = { ...this.bindings[action], keys };
    try {
      localStorage.setItem(BINDINGS_KEY, JSON.stringify(this.bindings));
    } catch {
      /* ignore */
    }
  }

  resetBindings(): void {
    this.bindings = structuredClone(DEFAULT_BINDINGS);
    try {
      localStorage.removeItem(BINDINGS_KEY);
    } catch {
      /* ignore */
    }
  }

  getBindings(): Readonly<Record<Action, Binding>> {
    return this.bindings;
  }

  private loadBindings(): void {
    try {
      const raw = localStorage.getItem(BINDINGS_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw) as Partial<Record<Action, Binding>>;
      for (const a of Object.keys(DEFAULT_BINDINGS) as Action[]) {
        if (parsed[a]?.keys) this.bindings[a] = { ...this.bindings[a], ...parsed[a] };
      }
    } catch {
      /* ignore */
    }
  }

  private getPad(): Gamepad | null {
    if (this.padIndex === null) return null;
    return navigator.getGamepads?.()[this.padIndex] ?? null;
  }

  private pollGamepad(): void {
    const pad = this.getPad();
    if (!pad) {
      this.padLookX = this.padLookY = this.padMoveX = this.padMoveY = 0;
      return;
    }
    const dz = settings.get().gamepadDeadzone;
    const clean = (v: number) => {
      if (Math.abs(v) < dz) return 0;
      // Rescale so the stick still reaches 1.0 at the rim after deadzoning.
      const s = (Math.abs(v) - dz) / (1 - dz);
      return Math.sign(v) * s * s; // squared for fine low-speed control
    };
    this.padMoveX = clean(pad.axes[0] ?? 0);
    this.padMoveY = clean(pad.axes[1] ?? 0);
    this.padLookX = clean(pad.axes[2] ?? 0);
    this.padLookY = clean(pad.axes[3] ?? 0);
  }

  private onKeyDown = (e: KeyboardEvent): void => {
    // Tab would move focus out of the canvas; Space would scroll.
    if (e.code === 'Tab' || e.code === 'Space') e.preventDefault();
    this.down.add(e.code);
  };

  private onKeyUp = (e: KeyboardEvent): void => {
    this.down.delete(e.code);
  };

  private onBlur = (): void => {
    // Losing focus mid-sprint must not leave the key stuck down.
    this.down.clear();
    this.heldActions.clear();
  };

  private onLockChange = (): void => {
    this.locked = document.pointerLockElement === this.canvas;
    if (!this.locked) this.down.clear();
  };

  private onMouseMove = (e: MouseEvent): void => {
    if (!this.locked) return;
    this.mouseDX += e.movementX;
    this.mouseDY += e.movementY;
  };

  private onMouseDown = (): void => {
    if (!this.locked) this.requestLock();
  };
}

export const input = new InputManager();
