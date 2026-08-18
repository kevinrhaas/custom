/**
 * facades.js — why no two buildings in this town are the same colour.
 *
 * The owner's report (T-0002, legacy K4; this half is T-0048): the buildings "read as freshly
 * painted and identical". Both halves of that were literally true of the
 * render. Every wall in the town took its colour from its ARCHETYPE — 114 wall
 * slots carrying four base colours between them (R-W2a §1) — so two neighbours
 * of the same archetype were the same brown to the bit, and nothing anywhere
 * asked how long a building had been standing in the weather.
 *
 * What this module is, in the project's own vocabulary
 * ---------------------------------------------------
 * It is **reconstructed** — invented within bounds because the scene needs it
 * and nothing states it (AGENTS.md § RECONSTRUCTED IS A TIER). No source this
 * repository holds gives the colour of any wall in 1835 Chicago, and the
 * dataset says so itself: of 335 records, `paint` is `reconstructed` on 236,
 * `inferred` on 15, and **`attested` on exactly two**. So the honest move is
 * not to leave 333 buildings identical — it is to vary them within a stated
 * bound, record the invention in `docs/LIBERTIES.md`, and NEVER touch the two
 * records a source actually speaks for.
 *
 * The one hard rule: **a record whose paint is `attested` is not touched at
 * all** — not weathered, not jittered, not by a thousandth. That is the
 * Sauganash's documented white (`Wau-Bun`) and the one attested `unpainted`.
 * `toneFor` returns the identity tone for them and says so in `reason`, and the
 * smoke asserts their drawn colour is unchanged to the bit.
 *
 * The two inputs, and why they are the ones available
 * --------------------------------------------------
 * **1. Age, where the dataset has one.** `documented_range.from` is the earliest
 * date the record is claimed to have stood in this form. Against the scene's
 * target date it gives an age in years: 1816 for the fort's buildings, 1833 for
 * the Green Tree, 1835 for most of the anonymous infill. Older wood silvers —
 * `docs/research/04-structures-south.md` reads the fort in 1835 as "serviceable,
 * weathered, whitewashed/unpainted log-and-brick" `[INF]`, which is the closest
 * thing to a statement about surface condition this repository holds.
 *
 * **The limit, stated rather than hidden: for the 262 records dated 1835-01-01
 * the date is a SCENE-PROGRAMME date, not a construction date.** Those records
 * are the inferred infill; the programme places them in the 1835 town and says
 * nothing about when they were built. So their age reads as ~0 and they get
 * essentially no silvering, which is not a claim that they are new — it is the
 * absence of a claim. Inventing ages for them would be a second reconstruction
 * stacked on the first, and it is not needed: the jitter below is what makes
 * them differ from each other.
 *
 * **2. Identity.** A deterministic hash of `id|phase` gives every structure its
 * own small offset in value and in warmth. Deterministic because a scene that
 * repainted itself on reload would make every frame gate in this suite
 * non-reproducible, and keyed on the record's own identity because that is the
 * only per-building quantity in the dataset that is not evidence.
 *
 * What it does NOT do
 * -------------------
 * - It does not read material names. On 38 of the 334 shipped assets
 *   `gltf-transform`'s palette pass folds the names away entirely (ROADMAP
 *   K36(a)), so a name-keyed rule would silently skip exactly the buildings
 *   with the most materials. The tone is per STRUCTURE and multiplies whatever
 *   that structure's surfaces are, textured or not.
 * - It does not add a draw call. The tone is folded into the per-vertex colour
 *   the batch already carries (R-W5a), so the untextured town stays one batch.
 * - It does not change board WIDTH or the lap rhythm. That is geometry, it
 *   needs the nightly bake, and it is the other half of T-0002 — ticket T-0049.
 */

/**
 * The bounds of the invention. Every number here is a limit on how far a
 * surface may be moved from the colour its archetype baked, and none of them is
 * derived from a source, because no source states one.
 *
 * `silverMax` and `soilMax` are set so that the oldest building in the town
 * (the fort, 19 years) reads as visibly grey and dirty beside a new one without
 * either of them reaching a colour the archetype could not have baked: 0.35 of
 * the way to its own luminance is still recognisably the same brown, and 0.10
 * of darkening is under the spread the archetypes already use between their own
 * wall finishes.
 *
 * `jitterValue` and `jitterWarm` are the "no two alike" half, and their ceiling
 * is the one bound this file can take from something already committed: **the
 * spread the archetypes themselves bake.** An unpainted wall is
 * `0.52, 0.44, 0.34` and an outbuilding's board is `0.335, 0.310, 0.268`
 * (R-W2a §1) — about 30 % of value between two surfaces this project already
 * calls the same material. ±16 % of value sits inside that, so no building is
 * tinted to a shade the generators could not have given it outright, and it is
 * a difference a visitor reads as two houses rather than two paints.
 *
 * They were ±10 % and ±4.5 % when this shipped, and the frames said that was
 * too little: photographed at `lake_market` and `from_above` with the tone on
 * and off, the two pictures were hard to tell apart. The measurement was never
 * the problem — 331 tones, no two neighbours alike — but the acceptance clause
 * is written about what a visitor SEES, and a difference only an instrument can
 * find does not discharge it.
 */
export const FACADE = {
  /** Years of exposure at which weathering is complete. */
  ageFullYears: 12,
  /** How far a fully weathered surface moves toward its own luminance. */
  silverMax: 0.35,
  /** How far a fully weathered surface darkens (rain, smoke, mud). */
  soilMax: 0.10,
  /** Per-building value jitter, plus or minus. */
  jitterValue: 0.16,
  /** Per-building warm/cool tilt, plus or minus, applied to red against blue. */
  jitterWarm: 0.07,
  /** Lime is renewed; a whitewashed wall silvers at this fraction of the rate. */
  whitewashRate: 0.5,
  /** Masonry does not silver at all, and its jitter is halved. */
  masonry: ['brick', 'stone', 'earth'],
  masonryJitter: 0.5,
};

/** Rec. 709 luminance, in the renderer's linear working space. */
function luminance(r, g, b) {
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

/**
 * FNV-1a over the record's identity. Any stable hash would do; this one is four
 * lines and has no dependencies, which matters in a renderer that vendors
 * everything it uses.
 */
function hash32(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i += 1) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return h >>> 0;
}

/** Two independent uniforms in [0,1) from one hash, by splitting its halves. */
function uniforms(seed) {
  const h = hash32(seed);
  return [(h >>> 16) / 65536, (h & 0xffff) / 65536];
}

/** Whole years between an ISO date and the scene's target date, floored at 0. */
function ageYears(fromISO, targetISO) {
  const from = Date.parse(`${String(fromISO ?? '').slice(0, 10)}T00:00:00Z`);
  const to = Date.parse(`${String(targetISO ?? '').slice(0, 10)}T00:00:00Z`);
  if (!Number.isFinite(from) || !Number.isFinite(to)) return 0;
  return Math.max(0, (to - from) / (365.2425 * 24 * 3600 * 1000));
}

/**
 * The tone for one structure: how its archetype's colours are to be moved.
 *
 * @param {object} sidecar  the record's compiled sidecar
 * @returns {{
 *   silver: number, soil: number, value: number, warm: number,
 *   age: number, paint: string|null, confidence: string|null,
 *   eligible: boolean, reason: string,
 * }}
 */
export function toneFor(sidecar) {
  const identity = { silver: 0, soil: 0, value: 1, warm: 0 };
  const paintAttr = sidecar?.attributes?.paint ?? null;
  const paint = paintAttr?.value ?? null;
  const confidence = paintAttr?.confidence ?? null;
  const age = ageYears(sidecar?.documented_range?.from, sidecar?.target_date);

  // The whole of the honesty rule, in one branch: a source spoke for this
  // surface, so nothing here may move it.
  if (confidence === 'attested') {
    return {
      ...identity, age, paint, confidence, eligible: false,
      reason: `paint is attested (${paint}) — a documented finish is never modulated`,
    };
  }

  const masonry = FACADE.masonry.includes(paint);
  const rate = masonry ? 0 : (paint === 'whitewash' ? FACADE.whitewashRate : 1);
  const weather = Math.min(1, age / FACADE.ageFullYears) * rate;

  const [u1, u2] = uniforms(`${sidecar?.id ?? ''}|${sidecar?.phase ?? ''}`);
  const spread = masonry ? FACADE.masonryJitter : 1;

  return {
    silver: FACADE.silverMax * weather,
    soil: FACADE.soilMax * weather,
    value: 1 + FACADE.jitterValue * spread * (u1 * 2 - 1),
    warm: FACADE.jitterWarm * spread * (u2 * 2 - 1),
    age,
    paint,
    confidence,
    eligible: true,
    reason: masonry
      ? `masonry (${paint}) — jitter only, no silvering`
      : `${paint ?? 'no stated paint'} at ${age.toFixed(1)} y`,
  };
}

/** The identity tone, for callers with no record at all. */
export const NEUTRAL_TONE = {
  silver: 0, soil: 0, value: 1, warm: 0, age: 0, paint: null, confidence: null,
  eligible: false, reason: 'no record',
};

/**
 * Apply a tone to one linear RGB triple and return the FACTORS, not the colour.
 *
 * Factors rather than colours because the renderer has to be able to wind the
 * whole thing back at runtime — `buildings.setWeathering(0)` is what lets a
 * gate photograph the same scene with and without this module and prove the
 * difference reaches the render (R-BUG6(a): a compile-time flag is not a
 * runtime handle). A per-channel factor is exact for that, because a source
 * mesh carries ONE material colour across all its vertices, so one triple
 * describes the whole range.
 *
 * Silvering is a mix toward the surface's own luminance, which is what
 * weathered wood does — it loses chroma and keeps roughly its value — and it is
 * expressed as a factor by dividing, which is why a zero channel falls back to
 * 1: a channel that is already zero cannot be moved toward anything.
 */
export function toneFactors(r, g, b, tone) {
  const lum = luminance(r, g, b);
  const mixed = [
    r + (lum - r) * tone.silver,
    g + (lum - g) * tone.silver,
    b + (lum - b) * tone.silver,
  ];
  const dim = (1 - tone.soil) * tone.value;
  const tilt = [1 + tone.warm, 1, 1 - tone.warm];
  const src = [r, g, b];
  return mixed.map((m, i) => (src[i] > 1e-6 ? (m / src[i]) * dim * tilt[i] : dim * tilt[i]));
}
