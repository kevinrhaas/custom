import { settings } from './Settings';

/**
 * The audio engine.
 *
 * In a game with no enemies, **sound is the entire tension model.** An empty
 * building at night is frightening because of what you can hear and cannot
 * place: your own footsteps carrying down a five-tier hall, water somewhere
 * below, wind through broken glazing, the radio going to static as the stone
 * gets between you and the crew.
 *
 * Everything here is **synthesised at runtime** rather than streamed from
 * files. That is a deliberate choice with three payoffs:
 *
 *  1. **Infinite variation.** A footstep sample played 4,000 times is the
 *     loudest repetition artefact in any first-person game. Every step here is
 *     generated fresh — different noise seed, different resonance, different
 *     scuff — so it never machine-guns.
 *  2. **Parametric surfaces.** Concrete, water, gravel, grating and stone
 *     differ by filter and envelope, not by asset, so a scene tags a mesh
 *     `surface: 'grating'` and the sound follows automatically.
 *  3. **Zero bytes.** The whole system costs no download at all, which keeps
 *     the load budget for geometry.
 *
 * The bus layout is: source → per-category gain → master → destination, with a
 * convolution reverb send whose impulse is itself generated per-space. Scenes
 * set the space (`setSpace`) and the reverb changes character — a cell block
 * is a long bright slap, the Void is short and dead.
 */

export type Surface =
  | 'concrete'
  | 'stone'
  | 'gravel'
  | 'asphalt'
  | 'grass'
  | 'water'
  | 'metal'
  | 'grating'
  | 'wood';

export type SpaceKind = 'exterior' | 'corridor' | 'cellblock' | 'tunnel' | 'chamber';

interface SurfaceProfile {
  /** Centre frequency of the body resonance, Hz. */
  body: number;
  /** Band-pass Q on the impact noise. */
  q: number;
  /** Impact decay, seconds. */
  decay: number;
  /** High-frequency scuff content, 0-1. */
  scuff: number;
  /** Overall level trim. */
  gain: number;
  /** Low-frequency thump, 0-1 — how much the floor itself resonates. */
  thump: number;
}

/**
 * Calibrated by ear against the reference locations. The cell-house corridor
 * is polished concrete over a void, so it has real low-end and a long tail;
 * the upper tier galleries are steel bar grating, which rings instead.
 */
const SURFACES: Record<Surface, SurfaceProfile> = {
  concrete: { body: 240, q: 0.7, decay: 0.2, scuff: 0.22, gain: 1.0, thump: 1.0 },
  stone: { body: 300, q: 0.9, decay: 0.16, scuff: 0.2, gain: 0.95, thump: 0.85 },
  gravel: { body: 900, q: 0.5, decay: 0.24, scuff: 0.7, gain: 0.85, thump: 0.4 },
  asphalt: { body: 210, q: 0.7, decay: 0.15, scuff: 0.3, gain: 0.85, thump: 0.8 },
  grass: { body: 260, q: 0.5, decay: 0.1, scuff: 0.7, gain: 0.45, thump: 0.15 },
  water: { body: 900, q: 0.7, decay: 0.42, scuff: 0.9, gain: 1.1, thump: 0.2 },
  metal: { body: 900, q: 3.5, decay: 0.36, scuff: 0.28, gain: 0.9, thump: 0.55 },
  grating: { body: 760, q: 4.5, decay: 0.55, scuff: 0.3, gain: 1.0, thump: 0.6 },
  wood: { body: 300, q: 2.4, decay: 0.2, scuff: 0.4, gain: 0.8, thump: 0.45 },
};

/** Reverb character per space. */
const SPACES: Record<SpaceKind, { seconds: number; decay: number; bright: number; wet: number }> = {
  // Outdoors against a 10 m limestone wall: a real slapback, little tail.
  exterior: { seconds: 1.1, decay: 3.4, bright: 0.55, wet: 0.16 },
  corridor: { seconds: 1.9, decay: 2.4, bright: 0.7, wet: 0.3 },
  // Five tiers of hard parallel surfaces. Famously long and bright.
  cellblock: { seconds: 3.6, decay: 1.7, bright: 0.85, wet: 0.42 },
  tunnel: { seconds: 2.4, decay: 2.1, bright: 0.3, wet: 0.38 },
  // Hand-cut stone, low ceiling, silt floor. Short and dead — the silence is
  // the point, and a big reverb here would wreck the scene.
  chamber: { seconds: 0.8, decay: 4.5, bright: 0.22, wet: 0.14 },
};

export class AudioEngine {
  private ctx: AudioContext | null = null;
  private master!: GainNode;
  private sfxBus!: GainNode;
  private ambienceBus!: GainNode;
  private voiceBus!: GainNode;
  private reverb!: ConvolverNode;
  private reverbSend!: GainNode;

  private ambience: { source: AudioBufferSourceNode; gain: GainNode }[] = [];
  private space: SpaceKind = 'exterior';
  private started = false;
  private unsub: (() => void) | null = null;

  /** Browsers refuse to start audio without a gesture; call from a click. */
  async start(): Promise<void> {
    if (this.started) return;
    try {
      const Ctor =
        window.AudioContext ??
        (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      this.ctx = new Ctor();
      if (this.ctx.state === 'suspended') await this.ctx.resume();
    } catch {
      return; // no audio available — the game must remain fully playable
    }

    const ctx = this.ctx;
    this.master = ctx.createGain();
    // Reported as "very tinny". Everything here is synthesised from noise and
    // band-passes, which without a shelf on the end of the chain is all upper
    // midrange and no body. This tames the top and the per-surface profiles
    // below carry far more low end than they did.
    const tame = ctx.createBiquadFilter();
    tame.type = 'lowshelf';
    tame.frequency.value = 260;
    tame.gain.value = 5;
    const deHarsh = ctx.createBiquadFilter();
    deHarsh.type = 'peaking';
    deHarsh.frequency.value = 3200;
    deHarsh.Q.value = 1.1;
    deHarsh.gain.value = -6;
    this.master.connect(tame).connect(deHarsh).connect(ctx.destination);

    this.sfxBus = ctx.createGain();
    this.ambienceBus = ctx.createGain();
    this.voiceBus = ctx.createGain();

    this.reverb = ctx.createConvolver();
    this.reverbSend = ctx.createGain();
    this.reverbSend.connect(this.reverb);
    this.reverb.connect(this.master);

    for (const bus of [this.sfxBus, this.ambienceBus, this.voiceBus]) {
      bus.connect(this.master);
      bus.connect(this.reverbSend);
    }

    this.setSpace('exterior');
    this.applySettings();
    this.unsub = settings.subscribe(() => this.applySettings());
    this.started = true;
  }

  private applySettings(): void {
    if (!this.ctx) return;
    const s = settings.get();
    const t = this.ctx.currentTime;
    this.master.gain.setTargetAtTime(s.masterVolume, t, 0.05);
    this.sfxBus.gain.setTargetAtTime(s.sfxVolume, t, 0.05);
    this.ambienceBus.gain.setTargetAtTime(s.musicVolume, t, 0.05);
    this.voiceBus.gain.setTargetAtTime(s.voiceVolume, t, 0.05);
  }

  /** Swap the reverb character. Scenes call this on load and on transitions. */
  setSpace(kind: SpaceKind): void {
    if (!this.ctx) return;
    this.space = kind;
    const cfg = SPACES[kind];
    this.reverb.buffer = this.makeImpulse(cfg.seconds, cfg.decay, cfg.bright);
    this.reverbSend.gain.setTargetAtTime(cfg.wet, this.ctx.currentTime, 0.4);
  }

  /**
   * Generated impulse response: exponentially-decaying noise with a
   * frequency tilt. Not a measured space, but it is convincing and it costs
   * nothing to ship.
   */
  private makeImpulse(seconds: number, decay: number, bright: number): AudioBuffer {
    const ctx = this.ctx!;
    const rate = ctx.sampleRate;
    const len = Math.max(1, Math.floor(rate * seconds));
    const buf = ctx.createBuffer(2, len, rate);

    for (let ch = 0; ch < 2; ch++) {
      const data = buf.getChannelData(ch);
      // One-pole low-pass state, for the tilt.
      let lp = 0;
      const cutoff = 0.02 + bright * 0.55;
      for (let i = 0; i < len; i++) {
        const t = i / len;
        const env = Math.pow(1 - t, decay);
        const n = Math.random() * 2 - 1;
        lp += (n - lp) * cutoff;
        // Early reflections: a few discrete taps before the diffuse tail.
        const early = i < rate * 0.05 && i % Math.floor(rate * 0.011) < 3 ? 1.8 : 1;
        data[i] = lp * env * early * 0.6;
      }
    }
    return buf;
  }

  /* ---------------------------------------------------------- footsteps --- */

  /**
   * One footstep. Three layers: a filtered noise impact (the heel), a low
   * body thump (the floor responding), and a high scuff (the sole sliding).
   * Every parameter is jittered so no two steps are identical.
   */
  footstep(surface: string, intensity: number): void {
    if (!this.ctx) return;
    const p = SURFACES[(surface as Surface)] ?? SURFACES.concrete;
    const ctx = this.ctx;
    const t = ctx.currentTime;
    const jitter = (v: number, amt: number): number => v * (1 + (Math.random() * 2 - 1) * amt);

    const out = ctx.createGain();
    out.gain.value = p.gain * intensity * 0.85;
    out.connect(this.sfxBus);

    // --- impact ---
    const impact = ctx.createBufferSource();
    impact.buffer = this.noiseBurst(jitter(p.decay, 0.25));
    const bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = jitter(p.body, 0.18);
    bp.Q.value = jitter(p.q, 0.3);
    const impEnv = ctx.createGain();
    impEnv.gain.setValueAtTime(1, t);
    impEnv.gain.exponentialRampToValueAtTime(0.0001, t + jitter(p.decay, 0.25));
    impact.connect(bp).connect(impEnv).connect(out);
    impact.start(t);
    impact.stop(t + p.decay * 1.6);

    // --- body thump: the structure under the foot ---
    if (p.thump > 0.05) {
      const osc = ctx.createOscillator();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(jitter(58, 0.15), t);
      osc.frequency.exponentialRampToValueAtTime(jitter(30, 0.15), t + 0.14);
      const g = ctx.createGain();
      g.gain.setValueAtTime(p.thump * 0.85 * intensity, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.22);
      osc.connect(g).connect(out);
      osc.start(t);
      osc.stop(t + 0.25);
    }

    // --- scuff ---
    if (p.scuff > 0.05) {
      const scuff = ctx.createBufferSource();
      scuff.buffer = this.noiseBurst(0.09);
      const hp = ctx.createBiquadFilter();
      hp.type = 'highpass';
      hp.frequency.value = jitter(1500, 0.2);
      const g = ctx.createGain();
      const delay = Math.random() * 0.02;
      g.gain.setValueAtTime(0, t + delay);
      g.gain.linearRampToValueAtTime(p.scuff * 0.13 * intensity, t + delay + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, t + delay + 0.085);
      scuff.connect(hp).connect(g).connect(out);
      scuff.start(t + delay);
      scuff.stop(t + delay + 0.1);
    }
  }

  /** Heavier version of a footstep, for landing from a drop. */
  land(intensity: number, surface = 'concrete'): void {
    this.footstep(surface, Math.min(1, 0.7 + intensity));
    if (!this.ctx) return;
    // Add a gear rattle — a person carrying a bag and a camera.
    const ctx = this.ctx;
    const t = ctx.currentTime + 0.03;
    const n = ctx.createBufferSource();
    n.buffer = this.noiseBurst(0.18);
    const bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = 3400;
    bp.Q.value = 2;
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.14 * intensity, t);
    g.gain.exponentialRampToValueAtTime(0.0001, t + 0.2);
    n.connect(bp).connect(g).connect(this.sfxBus);
    n.start(t);
    n.stop(t + 0.22);
  }

  private noiseBurst(seconds: number): AudioBuffer {
    const ctx = this.ctx!;
    const len = Math.max(1, Math.floor(ctx.sampleRate * seconds));
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
    return buf;
  }

  /* ----------------------------------------------------------- ambience --- */

  /**
   * A looping ambience bed. Layers of filtered noise at different rates read
   * as wind, distant traffic and building tone without any recorded material.
   */
  startAmbience(kind: SpaceKind = 'exterior'): void {
    if (!this.ctx) return;
    this.stopAmbience();
    const ctx = this.ctx;

    const layers: { cutoff: number; type: BiquadFilterType; gain: number; lfo: number }[] =
      kind === 'exterior'
        ? [
            // Reported as "a hissing screen". Broadband noise at these gains is
            // literally hiss — the low-passed layers need to sit much lower and
            // the high-passed air layer is the worst offender by far, because
            // that IS the sound of tape hiss. Cut hard and darkened.
            { cutoff: 220, type: 'lowpass', gain: 0.13, lfo: 0.07 }, // wind
            { cutoff: 110, type: 'lowpass', gain: 0.11, lfo: 0.03 }, // distant city
          ]
        : kind === 'chamber'
          ? [
              { cutoff: 170, type: 'lowpass', gain: 0.07, lfo: 0.02 }, // near-silence
            ]
          : [
              { cutoff: 340, type: 'lowpass', gain: 0.12, lfo: 0.05 },
            ];

    for (const layer of layers) {
      const src = ctx.createBufferSource();
      src.buffer = this.noiseBurst(4);
      src.loop = true;

      const filt = ctx.createBiquadFilter();
      filt.type = layer.type;
      filt.frequency.value = layer.cutoff;

      const gain = ctx.createGain();
      gain.gain.value = layer.gain;

      // Slow amplitude drift so the bed breathes instead of sitting flat.
      const lfo = ctx.createOscillator();
      lfo.frequency.value = layer.lfo;
      const lfoGain = ctx.createGain();
      lfoGain.gain.value = layer.gain * 0.55;
      lfo.connect(lfoGain).connect(gain.gain);
      lfo.start();

      src.connect(filt).connect(gain).connect(this.ambienceBus);
      src.start();
      this.ambience.push({ source: src, gain });
    }
  }

  stopAmbience(): void {
    for (const a of this.ambience) {
      try {
        a.source.stop();
      } catch {
        /* already stopped */
      }
    }
    this.ambience = [];
  }

  /** The sodium lamp's mains hum. Positional-ish via a simple gain ramp. */
  lampHum(distance: number): void {
    if (!this.ctx) return;
    const ctx = this.ctx;
    const osc = ctx.createOscillator();
    osc.type = 'sawtooth';
    osc.frequency.value = 120; // 2× mains
    const filt = ctx.createBiquadFilter();
    filt.type = 'lowpass';
    filt.frequency.value = 400;
    const g = ctx.createGain();
    g.gain.value = Math.max(0, 0.02 * (1 - distance / 22));
    osc.connect(filt).connect(g).connect(this.ambienceBus);
    osc.start();
  }

  /* --------------------------------------------------------------- radio --- */

  /**
   * Radio comms with depth-based degradation.
   *
   * `clarity` runs 1 (line of sight) to 0 (deep under stone). Below ~0.35 the
   * voice starts dropping out and the static rises. This is a **diegetic
   * signal that you are going too far**, not a cosmetic effect — the design
   * doc treats it as a mechanic.
   *
   * Speech itself is not synthesised; this shapes the channel. When VO exists
   * it plays through `voiceBus` and inherits this processing.
   */
  radioBurst(clarity: number, seconds = 0.6): void {
    if (!this.ctx) return;
    const ctx = this.ctx;
    const t = ctx.currentTime;
    const c = Math.max(0, Math.min(1, clarity));

    // Squelch open.
    const noise = ctx.createBufferSource();
    noise.buffer = this.noiseBurst(seconds);
    const bp = ctx.createBiquadFilter();
    bp.type = 'bandpass';
    bp.frequency.value = 1800;
    bp.Q.value = 0.8;
    const g = ctx.createGain();
    const staticLevel = 0.03 + (1 - c) * 0.22;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(staticLevel, t + 0.02);
    // Dropouts: the worse the clarity, the more of them.
    const drops = Math.floor((1 - c) * 6);
    for (let i = 0; i < drops; i++) {
      const at = t + 0.05 + Math.random() * (seconds - 0.1);
      g.gain.setValueAtTime(staticLevel, at);
      g.gain.linearRampToValueAtTime(staticLevel * 3.2, at + 0.015);
      g.gain.linearRampToValueAtTime(staticLevel, at + 0.06);
    }
    g.gain.linearRampToValueAtTime(0, t + seconds);
    noise.connect(bp).connect(g).connect(this.voiceBus);
    noise.start(t);
    noise.stop(t + seconds + 0.05);
  }

  /** Whether a line should be intelligible at this clarity. */
  static isIntelligible(clarity: number): boolean {
    return clarity > 0.35;
  }

  get currentSpace(): SpaceKind {
    return this.space;
  }

  get isRunning(): boolean {
    return this.started;
  }

  dispose(): void {
    this.unsub?.();
    this.stopAmbience();
    void this.ctx?.close();
    this.ctx = null;
    this.started = false;
  }
}

export const audio = new AudioEngine();
