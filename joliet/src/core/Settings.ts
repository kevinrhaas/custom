/**
 * Player-facing settings, persisted to localStorage.
 *
 * Accessibility items here are ship requirements, not stretch goals: head-bob
 * and motion-blur are independently disableable, subtitles default ON, and
 * every interaction prompt can be forced to high contrast.
 */

export type QualityTier = 'low' | 'medium' | 'high' | 'ultra';

export interface Settings {
  // Camera / input
  sensitivity: number; // 0.05 – 1.0
  invertY: boolean;
  fov: number; // vertical degrees, 60 – 100
  gamepadDeadzone: number;

  // Visual quality
  quality: QualityTier;
  resolutionScale: number; // 0.5 – 1.0, applied on top of the tier
  motionBlur: number; // 0 = off
  filmGrain: number; // 0 = off
  chromaticAberration: number;
  vignette: number;

  // Accessibility
  headBob: number; // 0 = fully off
  cameraLean: boolean;
  subtitles: boolean;
  subtitleSize: number; // 1 = default
  speakerNames: boolean;
  highContrastPrompts: boolean;
  reducedMotion: boolean;
  colorblind: 'none' | 'protan' | 'deutan' | 'tritan';
  /** Puzzle audio cues also get a visual representation. Never gate on audio. */
  visualAudioCues: boolean;

  // Audio
  masterVolume: number;
  musicVolume: number;
  sfxVolume: number;
  voiceVolume: number;

  // Assist
  /** Surfaces a contextual hint after N seconds of no progress. */
  hintDelaySeconds: number;
  /** Widens traversal hitboxes and enables ledge snapping. */
  traversalAssist: boolean;
}

export const DEFAULTS: Settings = {
  sensitivity: 0.22,
  invertY: false,
  fov: 78,
  gamepadDeadzone: 0.18,

  quality: 'high',
  resolutionScale: 1,
  motionBlur: 0.35,
  filmGrain: 0.55,
  chromaticAberration: 0.6,
  vignette: 0.5,

  headBob: 1,
  cameraLean: true,
  subtitles: true,
  subtitleSize: 1,
  speakerNames: true,
  highContrastPrompts: false,
  reducedMotion: false,
  colorblind: 'none',
  visualAudioCues: true,

  masterVolume: 0.9,
  musicVolume: 0.5,
  sfxVolume: 1,
  voiceVolume: 1,

  hintDelaySeconds: 90,
  traversalAssist: true,
};

const KEY = 'joliet.settings.v1';

type Listener = (s: Readonly<Settings>) => void;

class SettingsStore {
  private state: Settings = { ...DEFAULTS };
  private listeners = new Set<Listener>();

  constructor() {
    this.load();
    // Respect the OS-level reduced-motion preference on first run.
    if (
      typeof matchMedia === 'function' &&
      matchMedia('(prefers-reduced-motion: reduce)').matches &&
      !localStorage.getItem(KEY)
    ) {
      this.state.reducedMotion = true;
      this.state.motionBlur = 0;
      this.state.headBob = 0.25;
    }
  }

  get(): Readonly<Settings> {
    return this.state;
  }

  set<K extends keyof Settings>(key: K, value: Settings[K]): void {
    if (this.state[key] === value) return;
    this.state[key] = value;
    // Reduced motion is a master switch over the motion-y effects.
    if (key === 'reducedMotion' && value === true) {
      this.state.motionBlur = 0;
      this.state.headBob = Math.min(this.state.headBob, 0.25);
    }
    this.save();
    this.emit();
  }

  patch(partial: Partial<Settings>): void {
    Object.assign(this.state, partial);
    this.save();
    this.emit();
  }

  reset(): void {
    this.state = { ...DEFAULTS };
    this.save();
    this.emit();
  }

  subscribe(fn: Listener): () => void {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  }

  private emit(): void {
    for (const fn of this.listeners) fn(this.state);
  }

  private save(): void {
    try {
      localStorage.setItem(KEY, JSON.stringify(this.state));
    } catch {
      /* private browsing — settings just won't persist */
    }
  }

  private load(): void {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw) as Partial<Settings>;
      // Additive migration: unknown keys are ignored, missing keys keep their
      // default. Never wipe a player's stored settings on upgrade.
      for (const k of Object.keys(DEFAULTS) as (keyof Settings)[]) {
        if (parsed[k] !== undefined) (this.state[k] as unknown) = parsed[k];
      }
    } catch {
      /* corrupt payload — fall back to defaults rather than crash */
    }
  }
}

export const settings = new SettingsStore();

/** Per-tier renderer knobs. The scene code reads these, never raw quality. */
export interface QualityProfile {
  shadowMapSize: number;
  cascades: number;
  shadowDistance: number;
  ssao: boolean;
  ssaoRatio: number;
  bloom: boolean;
  volumetrics: boolean;
  volumetricSamples: number;
  particleBudget: number;
  maxLights: number;
  anisotropy: number;
  /** Screen-space reflections on standing water. Expensive; ultra only. */
  waterSSR: boolean;
  hardwareScale: number;
}

export const QUALITY: Record<QualityTier, QualityProfile> = {
  low: {
    shadowMapSize: 1024,
    cascades: 2,
    shadowDistance: 45,
    ssao: false,
    ssaoRatio: 0.5,
    bloom: true,
    volumetrics: false,
    volumetricSamples: 0,
    particleBudget: 250,
    maxLights: 4,
    anisotropy: 2,
    waterSSR: false,
    hardwareScale: 1.35,
  },
  medium: {
    shadowMapSize: 1024,
    cascades: 3,
    shadowDistance: 70,
    ssao: true,
    ssaoRatio: 0.5,
    bloom: true,
    volumetrics: true,
    volumetricSamples: 24,
    particleBudget: 700,
    maxLights: 6,
    anisotropy: 4,
    waterSSR: false,
    hardwareScale: 1.15,
  },
  high: {
    shadowMapSize: 2048,
    cascades: 4,
    shadowDistance: 110,
    ssao: true,
    ssaoRatio: 0.75,
    bloom: true,
    volumetrics: true,
    volumetricSamples: 48,
    particleBudget: 1600,
    maxLights: 8,
    anisotropy: 8,
    waterSSR: false,
    hardwareScale: 1,
  },
  ultra: {
    shadowMapSize: 2048,
    cascades: 4,
    shadowDistance: 160,
    ssao: true,
    ssaoRatio: 1,
    bloom: true,
    volumetrics: true,
    volumetricSamples: 72,
    particleBudget: 3000,
    maxLights: 10,
    anisotropy: 16,
    waterSSR: true,
    hardwareScale: 1,
  },
};

export function profile(): QualityProfile {
  return QUALITY[settings.get().quality];
}
