/**
 * facade.js — the finish a record states, drawn on the building that states it.
 *
 * ROADMAP § K4, the owner's words: *the buildings read as freshly painted and
 * identical*. Both halves of that are true, and neither is a shader bug.
 *
 * **Freshly painted.** 142 of the 174 phases that state a finish state
 * `unpainted`, and the dossiers already say what that looked like: the fort is
 * to be modelled "serviceable, weathered, whitewashed/unpainted log-and-brick"
 * (`docs/research/04-structures-south.md` § Fort Dearborn), the Dearborn Street
 * bridge "weathered, patched, sagging" (ibid.), and the Green Tree memo puts the
 * whole argument in one sentence — the difference between a white building and
 * "a weathered one standing a block from the Sauganash, whose white paint was
 * remarkable precisely because its neighbours were not"
 * (`docs/RESEARCH/green_tree_tavern.md` § 4). `generators/common/mesh.py` gives
 * `unpainted` one warm fresh-sawn tan and every archetype resolves the record's
 * value through that single table, so the town was drawn the colour of new
 * lumber on the day it was cut.
 *
 * **Identical.** That is not a shortcut anyone took; it is a consequence of the
 * draw-call budget, and it is the reason this lives in the renderer rather than
 * in the bake. `buildings.js` collapses materials that render identically into
 * one `BatchedMesh` each — that is what keeps 242 structures inside 80 draw
 * calls. Giving each building its own weathered wall colour in Blender would
 * give each building its own material and therefore its own draw call: 242
 * against a budget of 80. Per-building variation cannot be a baked material. It
 * has to be a per-vertex channel riding inside the shared batch, which is
 * exactly the shape `_CONFIDENCE` already has (confidence.js), and this module
 * is that channel's twin.
 *
 * **Why it desaturates rather than mixing toward a chosen grey — the design
 * decision with a pipeline behind it.** The obvious implementation tints each
 * surface toward an invented weathered colour, and to avoid greying out window
 * voids and glazing it would have to know which surface it was looking at. The
 * generators name their materials (`wall`, `log`, `roof`, `glass`, `dark`,
 * `chinking`, …) so that looks free — and it is not available where it counts.
 * `tools/bake.sh` runs gltf-transform over `assets/web/`, whose palette pass
 * MERGES materials and renames the survivors `PaletteMaterial001…`: the
 * Sauganash master carries `wall / roof / log / shutter / glass` and the
 * derivative the visitor downloads carries three paletted materials with the
 * colours moved into a texture. 38 of the published building assets are in that
 * state. A renderer keyed on material names would therefore behave one way under
 * `tools/smoke_renderer.mjs`, which loads the masters from `assets/gltf/`, and
 * another way on the live site, which loads the derivatives from `data/gltf/` —
 * a green gate reporting on a pipeline it is not running, which is a failure
 * this project has already paid for once (STATUS, the nightly bake).
 *
 * So the rule reads no names and no colours. Weathering here is the REMOVAL of
 * colour: each fragment is mixed toward its own luminance. A tan board goes
 * grey-brown, a shingle roof greys, and a near-neutral window void moves by
 * almost nothing because it has almost no colour to lose — the surfaces that
 * would have needed protecting protect themselves, arithmetically, in both
 * pipelines. Nothing in this module can tell the two apart, which is the point.
 *
 * **What is data and what is invented.** The finish is the record's
 * (`attributes.paint`) and so is the first date it claims to have existed
 * (`documented_range.from`). How far each finish travels, the age ramp and the
 * per-building tone spread are this renderer's, and they are admitted in
 * `docs/LIBERTIES.md` L91.
 *
 * Three rules the numbers below encode:
 *
 *  1. **A finish that cannot silver, does not.** `brick`, `stone` and `earth`
 *     weather, but not by going grey the way bare timber does, and this
 *     treatment has no vocabulary for what they do instead. They get an honest
 *     zero rather than an approximate something. A record with no `paint` at all
 *     — 68 of the scene's 242 structures — likewise gets nothing.
 *  2. **Age is a lower bound and is used as one.** `documented_range.from` is
 *     the first date the record CLAIMS the phase existed, which is on or before
 *     the date it was built and never after. So the age term can only ADD to a
 *     floor every building of that finish already carries. 173 of the scene's
 *     242 structures — overwhelmingly the inferred-infill roofs — carry a range
 *     that opens inside 1835 itself, because nothing is known about when they
 *     went up; they sit within half a year of the scene date and the age term
 *     adds at most 3 % of their finish's travel. The 69 whose ranges open
 *     earlier, back to 1816, are the ones it moves.
 *  3. **An attested finish is drawn as attested.** The two records whose
 *     `paint` is graded at the top level — the Sauganash's white and St Mary's — get
 *     neither treatment: no silvering, no tone offset. Where a source states the
 *     colour, the colour it states is what is drawn, and the variation exists to
 *     stop INVENTED buildings reading as clones.
 */

import * as THREE from 'three';

import { LEVELS } from './confidence.js';

/**
 * The most certain level, whatever it is currently called. Rule 3 below turns
 * on it, and it was written as the literal 'documented' — which stopped being
 * the word on 2026-08-13 when the vocabulary was renamed for the second time
 * in a day. Nothing raised: the comparison simply went false for every record,
 * so the two finishes a source actually states began to weather like the rest
 * of the town. Derived from LEVELS so the next rename cannot repeat it.
 */
const ATTESTED = Object.keys(LEVELS).reduce((a, b) => (LEVELS[a] <= LEVELS[b] ? a : b));

/**
 * How far each finish can travel toward its own greyscale. `unpainted` stops
 * well short of 1.0: a wall with every trace of colour removed is a different
 * overstatement from the one being fixed.
 */
export const FINISH_WEATHERS = Object.freeze({
  unpainted: 0.80,
  whitewash: 0.35,   // renewed cheaply, and chalks off between coats
  white: 0.18,       // a maintained painted surface
  red: 0.18,
  brick: 0.0,        // rule 1 — masonry does not silver
  stone: 0.0,
  earth: 0.0,
});

/** The share of a finish's travel a building carries with no age evidence. */
export const AGE_FLOOR = 0.55;

/** Years standing at which the age term saturates. */
export const FULL_YEARS = 8;

/** Peak per-building lightness offset, either way. */
export const TONE_AMPLITUDE = 0.075;

/** Years between an ISO date and the scene's target date; null if either is absent. */
export function yearsStanding(from, targetDate) {
  if (!from || !targetDate) return null;
  const a = Date.parse(`${from}T00:00:00Z`);
  const b = Date.parse(`${targetDate}T00:00:00Z`);
  if (!Number.isFinite(a) || !Number.isFinite(b)) return null;
  return Math.max(0, (b - a) / (365.2425 * 86400000));
}

/**
 * A stable per-building offset in [-1, 1], from the structure id alone.
 *
 * Id-anchored rather than position-anchored, and that is deliberate: almost
 * every position in this dataset is symbolic and moves as research lands, and a
 * building that changed colour because its coordinate was corrected would be
 * reporting a research result as a repaint. FNV-1a, so the same id gives the
 * same face in every session, on every machine, for good.
 */
export function toneHash(id) {
  let h = 0x811c9dc5;
  const s = String(id);
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  // Two draws from the same stream so the low bits get a say as well as the
  // high ones: the ids here share long prefixes (`recon_1835_north_d1_0…`) and
  // one shift alone clusters them visibly.
  const u = ((h >>> 8) & 0xffff) / 0xffff;
  const v = ((h >>> 24) & 0xff) / 0xff;
  return (u * 0.75 + v * 0.25) * 2 - 1;
}

/**
 * What this building's face does, from its own record and nothing else.
 * @param {object} sidecar  the compiled per-structure sidecar
 */
export function weatheringFor(sidecar) {
  const attr = sidecar?.attributes?.paint ?? null;
  const paint = attr?.value ?? null;
  const paintConfidence = attr?.confidence ?? null;
  const documented = paintConfidence === ATTESTED;              // rule 3
  const travel = (paint == null || documented) ? 0 : (FINISH_WEATHERS[paint] ?? 0);

  const years = yearsStanding(sidecar?.documented_range?.from, sidecar?.target_date);
  // Rule 2: `aged` is null — not zero — where nothing is known, and the age term
  // only ever adds to the floor.
  const aged = years == null ? null : Math.min(1, years / FULL_YEARS);
  const silvering = travel * (AGE_FLOOR + (1 - AGE_FLOOR) * (aged ?? 0));
  const tone = documented ? 0 : toneHash(sidecar?.id ?? '') * TONE_AMPLITUDE;

  return { id: sidecar?.id ?? null, paint, paintConfidence, years, aged, silvering, tone };
}

const VERTEX_DECL = /* glsl */`
attribute vec2 _facade;
varying vec2 vFacade;
`;

const VERTEX_ASSIGN = /* glsl */`
  // Sanitised at source for the reason confidence.js spells out at length: a
  // geometry reaching a batch without this attribute leaves it unbound, and an
  // unbound attribute is not reliably zero on real hardware. (c == c) is false
  // only for NaN — the portable test, since isnan() is unreliable across drivers.
  vec2 chicagoF = _facade;
  vFacade = vec2(
    (chicagoF.x == chicagoF.x) ? clamp(chicagoF.x, 0.0, 1.0) : 0.0,
    (chicagoF.y == chicagoF.y) ? clamp(chicagoF.y, -0.5, 0.5) : 0.0
  );
`;

const FRAGMENT_DECL = /* glsl */`
varying vec2 vFacade;
uniform float uFacadeMode;
`;

const FRAGMENT_MIX = /* glsl */`
  // Off must mean untouched — not "multiplied by one". Guarding on the mode
  // before the channel is read is what makes the treatment measurable by
  // switching it off, and it is the same guard confidence.js needs for the same
  // hardware reason.
  if (uFacadeMode > 0.0) {
    // Rec. 709 luminance, in the linear working space diffuseColor is already in.
    float chicagoL = dot(diffuseColor.rgb, vec3(0.2126, 0.7152, 0.0722));
    diffuseColor.rgb = mix(diffuseColor.rgb, vec3(chicagoL), vFacade.x * uFacadeMode);
    diffuseColor.rgb = clamp(diffuseColor.rgb * (1.0 + vFacade.y * uFacadeMode), 0.0, 1.0);
  }
`;

/**
 * One uniforms object shared by every patched material, exactly as the
 * confidence view does it, so the treatment cannot end up on some buildings and
 * not others.
 *
 * ORDER MATTERS AGAINST confidence.js, and buildings.js depends on it: patch the
 * confidence view FIRST and this one SECOND. Both hang their code off
 * `#include <color_fragment>`, and the later patch's insert lands nearer the
 * include — so patching this second puts weathering BEFORE the confidence tint,
 * which is the only correct order. Weathering is part of what the building looks
 * like; the confidence tint is a statement ABOUT it, and a statement that got
 * weathered would be unreadable.
 */
export function createFacadeView({ enabled = true } = {}) {
  const uniforms = { uFacadeMode: { value: enabled ? 1 : 0 } };

  const patched = new Set();
  /** structure id -> the weathering it was drawn with. */
  const applied = new Map();

  function patch(material) {
    if (!material || patched.has(material)) return material;
    patched.add(material);

    const prior = material.onBeforeCompile;
    material.onBeforeCompile = (shader, renderer) => {
      if (typeof prior === 'function') prior(shader, renderer);
      Object.assign(shader.uniforms, uniforms);

      shader.vertexShader = VERTEX_DECL + shader.vertexShader.replace(
        '#include <begin_vertex>',
        '#include <begin_vertex>' + VERTEX_ASSIGN,
      );

      let f = FRAGMENT_DECL + shader.fragmentShader;
      if (f.includes('#include <color_fragment>')) {
        f = f.replace(
          '#include <color_fragment>',
          '#include <color_fragment>' + FRAGMENT_MIX,
        );
      }
      shader.fragmentShader = f;
    };
    material.needsUpdate = true;
    return material;
  }

  /**
   * Write the channel onto one mesh's geometry. The whole mesh carries one
   * value, because the statement is about the building and not about a vertex.
   *
   * @param {THREE.BufferGeometry} geo
   * @param {object} weathering   from weatheringFor()
   */
  function applyTo(geo, weathering) {
    const count = geo.getAttribute('position').count;
    const data = new Float32Array(count * 2);
    const s = weathering?.silvering ?? 0;
    const t = weathering?.tone ?? 0;
    for (let i = 0; i < count; i++) { data[i * 2] = s; data[i * 2 + 1] = t; }
    geo.setAttribute('_facade', new THREE.BufferAttribute(data, 2));
    if (weathering?.id) applied.set(weathering.id, weathering);
    return weathering;
  }

  return {
    uniforms,
    patch,
    applyTo,
    weatheringFor,
    /** What the building with this id was drawn with, or null. */
    weatheringOf(id) { return applied.get(id) ?? null; },
    /** Every building the channel was written for, as plain data. */
    entries() { return [...applied.values()]; },
    get enabled() { return uniforms.uFacadeMode.value > 0; },
    /** Off means untouched, which is what makes the treatment measurable. */
    set(on) { uniforms.uFacadeMode.value = on ? 1 : 0; return this.enabled; },
  };
}
