/**
 * confidence.js — THE confidence view.
 *
 * `docs/PROVENANCE.md`: "For a museum, a classroom, or a civic audience this is
 * the single most valuable thing the project offers." It is a deliverable, not a
 * debug overlay, and it is implemented exactly once — as a single
 * `onBeforeCompile` patch on the shared building material — so that it cannot be
 * forgotten per-building.
 *
 * The channel is `_CONFIDENCE`, a custom glTF SCALAR float attribute
 * (docs/GLB-CONTRACT.md): 0.0 documented, 0.5 inferred, 1.0 conjectural.
 * GLTFLoader lowercases unknown attributes, so it arrives as
 * `geometry.attributes._confidence`. three will not wire it up for us and must
 * not: it is data, not colour, and nothing may tint by accident. We declare the
 * attribute in the patch and carry it to the fragment stage ourselves.
 *
 * How each level renders when the view is on:
 *
 *   documented   unchanged
 *   inferred     lerped toward amber
 *   conjectural  screen-door dithered translucent massing — an ordered 4x4
 *                Bayer threshold against gl_FragCoord with a `discard`, IN THE
 *                OPAQUE PASS. No blending, no depth sorting, no per-object
 *                render order. That is what lets it work inside one BatchedMesh,
 *                where every building shares a draw call and sorting is not
 *                available even in principle.
 */

import * as THREE from 'three';

export const LEVELS = {
  documented: 0.0,
  inferred: 0.5,
  conjectural: 1.0,
};

/** Level name for a raw channel value — the inverse of LEVELS, band-wise. */
export function levelOf(value) {
  if (value >= 0.75) return 'conjectural';
  if (value >= 0.25) return 'inferred';
  return 'documented';
}

const VERTEX_DECL = /* glsl */`
attribute float _confidence;
varying float vConfidence;
`;

const VERTEX_ASSIGN = /* glsl */`
  vConfidence = _confidence;
`;

const FRAGMENT_DECL = /* glsl */`
varying float vConfidence;
uniform float uConfMode;
uniform float uConjecturalAlpha;
uniform vec3 uInferredTint;
uniform vec3 uConjecturalTint;

// Ordered 4x4 Bayer matrix. Screen-door translucency: a stable per-pixel
// threshold means no sorting, no blending, and no order dependence between the
// buildings sharing a batch.
float chicago_bayer4(vec2 fragXY) {
  int x = int(mod(fragXY.x, 4.0));
  int y = int(mod(fragXY.y, 4.0));
  int i = x + y * 4;
  float m[16];
  m[0]  =  0.0; m[1]  =  8.0; m[2]  =  2.0; m[3]  = 10.0;
  m[4]  = 12.0; m[5]  =  4.0; m[6]  = 14.0; m[7]  =  6.0;
  m[8]  =  3.0; m[9]  = 11.0; m[10] =  1.0; m[11] =  9.0;
  m[12] = 15.0; m[13] =  7.0; m[14] = 13.0; m[15] =  5.0;
  float v = 0.0;
  for (int k = 0; k < 16; k++) { if (k == i) v = m[k]; }
  return (v + 0.5) / 16.0;
}

// Crisp bands, because the contract's values are exactly 0.0 / 0.5 / 1.0 — but
// they degrade sanely if a generator ever emits something in between.
float chicago_wInferred(float c)    { return 1.0 - min(abs(c - 0.5) * 4.0, 1.0); }
float chicago_wConjectural(float c) { return clamp((c - 0.75) * 4.0, 0.0, 1.0); }
`;

const FRAGMENT_DISCARD = /* glsl */`
  {
    float conj = chicago_wConjectural(vConfidence) * uConfMode;
    if (conj > 0.0) {
      float alpha = mix(1.0, uConjecturalAlpha, conj);
      if (chicago_bayer4(gl_FragCoord.xy) >= alpha) discard;
    }
  }
`;

const FRAGMENT_TINT = /* glsl */`
  {
    float wInf = chicago_wInferred(vConfidence) * uConfMode;
    float wCon = chicago_wConjectural(vConfidence) * uConfMode;
    diffuseColor.rgb = mix(diffuseColor.rgb, uInferredTint, wInf * 0.72);
    diffuseColor.rgb = mix(diffuseColor.rgb, uConjecturalTint, wCon * 0.80);
  }
`;

/**
 * One uniforms object shared by every patched material, so flipping the view is
 * a single assignment no matter how many materials exist.
 */
export function createConfidenceView({
  inferred = 0xe2a63f,
  conjectural = 0x93a6bb,
  conjecturalAlpha = 0.34,
} = {}) {
  const uniforms = {
    uConfMode: { value: 0 },
    uConjecturalAlpha: { value: conjecturalAlpha },
    uInferredTint: { value: new THREE.Color(inferred).convertSRGBToLinear() },
    uConjecturalTint: { value: new THREE.Color(conjectural).convertSRGBToLinear() },
  };

  const patched = new Set();

  /**
   * Patch a material in place. Safe to call twice on the same material.
   * Works on MeshStandardMaterial / MeshPhysicalMaterial and on
   * MeshDepthMaterial (so a dithered wall casts a dithered shadow).
   */
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
      // Discard first: a conjectural fragment that is dithered away should not
      // pay for lighting, and it must not write depth.
      f = f.replace(
        '#include <clipping_planes_fragment>',
        '#include <clipping_planes_fragment>' + FRAGMENT_DISCARD,
      );
      // Tint after diffuseColor is final (map + any vertex colour applied).
      if (f.includes('#include <color_fragment>')) {
        f = f.replace(
          '#include <color_fragment>',
          '#include <color_fragment>' + FRAGMENT_TINT,
        );
      }
      shader.fragmentShader = f;
    };
    material.needsUpdate = true;
    return material;
  }

  /**
   * Guarantee the attribute exists. A geometry without `_CONFIDENCE` is a
   * generator bug, not something to paper over — we fill it with `documented`
   * so the scene still renders, and shout, because silently rendering unmarked
   * geometry as if it were attested is the one failure mode this whole view
   * exists to prevent.
   */
  function ensureAttribute(geometry, label = 'geometry') {
    if (geometry.getAttribute('_confidence')) return null;
    const count = geometry.getAttribute('position').count;
    geometry.setAttribute('_confidence',
      new THREE.BufferAttribute(new Float32Array(count), 1));
    const msg = `${label}: no _CONFIDENCE attribute in the GLB — rendering it as `
      + `documented, which it may not be. See docs/GLB-CONTRACT.md.`;
    console.warn(`[4D Chicago] ${msg}`);
    return msg;
  }

  /** Count vertices per level — the honest picture of what is on screen. */
  function census(geometry) {
    const attr = geometry.getAttribute('_confidence');
    const out = { documented: 0, inferred: 0, conjectural: 0 };
    if (!attr) return out;
    for (let i = 0; i < attr.count; i++) out[levelOf(attr.getX(i))]++;
    return out;
  }

  let enabled = false;
  return {
    uniforms,
    patch,
    ensureAttribute,
    census,
    get enabled() { return enabled; },
    /** @param {boolean} on */
    set(on) {
      enabled = !!on;
      uniforms.uConfMode.value = enabled ? 1 : 0;
      return enabled;
    },
    toggle() { return this.set(!enabled); },
  };
}
