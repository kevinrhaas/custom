/**
 * world.js — sky, sun, light, environment, tone mapping.
 *
 * The sun is not art-directed. `data/scenes/1835.json` records a lighting
 * moment ("10:00", 1 July 1835) and `data/datum.json` records where that is
 * (41.8867 N, 87.6380 W); the azimuth and elevation are computed from those two
 * facts and drive both the sky and the single directional light. If the scene
 * date moves, the shadows move.
 *
 * On the clock: standard time zones did not exist in 1835 — they arrive with the
 * railroads in 1883. A time written against an 1835 scene can only mean LOCAL
 * MEAN time at that longitude, so that is how it is read here. It matters: the
 * datum longitude is 5h 50m west of Greenwich, nearly ten minutes off the
 * Central Standard meridian, and reading 10:00 as CST would put the sun in the
 * wrong place by about two and a half degrees.
 *
 * The sky's ABSOLUTE brightness, on the other hand, is not physics and has to be
 * calibrated — see SKY_EXPOSURE below.
 */

import * as THREE from 'three';
import { Sky } from 'three/addons/objects/Sky.js';

const DEG = Math.PI / 180;

/**
 * The one free constant in the sky, and why it has a number rather than a
 * default.
 *
 * Preetham's model — which `Sky.js` implements — produces radiance in arbitrary
 * units: its `EE = 1000.0` "sun intensity" is a convention, not a measurement,
 * so the model fixes the sky's COLOUR but says nothing about where that colour
 * should sit on the exposure scale. three's own example papers over this by
 * running the whole scene at `toneMappingExposure = 0.5`, which is not available
 * here: the same exposure lights the buildings, and their albedo is evidence.
 *
 * So the sky gets its own exposure, and the number is measured rather than
 * dialled by eye. Against `dupage_tallgrass_2018-07-24.jpg` — a verified 24 July
 * photograph of Illinois tallgrass at this latitude, framed the way the standard
 * `prairie_west` shot is framed — the sky reads sRGB (101,153,209) about 15°
 * above the horizon, (125,165,205) at 8°, (137,166,200) at 4°. Running this
 * shader through the same ACES + sRGB chain the renderer uses, 0.045 lands the
 * 1835 sky within a few units of all three at the shot's own view azimuth. The
 * scene default of 1.0 rendered (245,252,255) — a white wash at every elevation,
 * which is what the baseline showed.
 *
 * It is applied to the sky ALONE. It is deliberately NOT a change to
 * `toneMappingExposure`, which would move the ground, the water and every
 * documented wall colour with it.
 *
 * What it does NOT fix, because a single scalar cannot: the SHAPE of the sky
 * with elevation. Exposure moves all three channels at every elevation together;
 * the error against the photograph was concentrated in red and green, and only
 * near the horizon. That is HORIZON_RESTORE below.
 */
const SKY_EXPOSURE = 0.045;

/**
 * Putting the colour back into Preetham's horizon.
 *
 * THE DEFECT. Follow the model down to the horizon and watch the wavelength
 * dependence leave it. `Sky.js` builds in-scatter as
 *
 *     Lin = ( sunE * (betaR*rPhase + betaM*mPhase) / (betaR + betaM) * (1 - Fex) ) ^ 1.5
 *
 * and `Fex`, the extinction, is by far the strongest wavelength-dependent factor
 * in it. Along a horizon ray the model's own optical-length term runs to ~26×
 * the zenith path at 1° up and ~37× at the horizontal, so `Fex` has gone to
 * zero in all three channels and `1 - Fex` is 1, 1, 1. What is left is the
 * ratio of the two phase functions, and those are almost achromatic:
 * evaluated for this scene at 1° up, the red:green:blue in-scatter comes out
 * 0.816 : 0.919 : 1.000. The model therefore renders a WHITE horizon and hands
 * the whitening job to a neutral, so the band above the skyline arrived as
 * sRGB (181,191,195) at saturation 0.072.
 *
 * The photograph disagrees, and not by a little. `bar/dupage_tallgrass_
 * 2018-07-24.jpg` reads (136,163,192) at saturation 0.288 immediately above its
 * own sky/land step — B-R +55 against our +14. Note WHERE the error is: our
 * blue is essentially right (195 against 191). The whole of it is red +45 and
 * green +28. The horizon was not short of blue, it was carrying red and green
 * that a real horizon does not carry.
 *
 * THE CORRECTION. So this restores the channel dependence the saturated `1-Fex`
 * threw away, and does it the only way that leaves everything else alone: red
 * and green are attenuated toward the horizon, blue is not touched at all, and
 * the attenuation dies out with height fast enough that the upper sky renders as
 * the model built it — 0.3 % of the green at 30°, 0.03 % at 40°, nothing that
 * survives rounding to 8 bits anywhere above that.
 *
 *     scale(channel) = 1 - A * exp( -( sin(elevation) / E ) ^ P )
 *
 * A, E and P are FITTED — to the photograph, not by eye. The bar's sky was
 * sampled at ten elevations from 16° down to 0.5°, and A and E were solved by
 * running each candidate back through this scene's own shader, exposure, ACES
 * curve and sRGB encode and least-squaring against those samples
 * (`gaa_fit4.mjs` in the working directory). Residuals: 1.6 units RMS in red,
 * 1.0 in green, worst case 4, and the last degree — the elevation the
 * verification actually reads — lands within one unit on both.
 *
 * Red and green have to be solved TOGETHER, which is easy to get wrong: ACES is
 * not a per-channel curve. Its input matrix row for red is
 * (0.597, 0.355, 0.048), so taking green out takes red with it, and fitting the
 * two channels separately produced a pair that each looked right alone and
 * overshot red by 10 units together. The exponent is shared and lands at 1.6; a
 * plain exponential (P = 1) fits the middle of the band and then overshoots the
 * last degree, which is exactly where the check is.
 *
 * WHAT IT IS NOT. It is not exposure and it is not a tone curve: the ground
 * matches the bar to a few counts already and nothing here can move it — the
 * patch multiplies `texColor` inside the SKY shader, which nothing else in the
 * scene samples (the PMREM environment built from it is disposed unused, see
 * below). It is not "add blue": blue is untouched, and every unit of the change
 * is red and green coming off.
 *
 * ITS ONE HONEST COST, so nobody has to rediscover it. The fit is azimuth-blind,
 * because the model's horizon goes achromatic in every direction and the defect
 * is therefore the same in every direction — but the model's horizon BRIGHTNESS
 * is not the same in every direction. `prairie_west` looks south, within 19° of
 * the sun's azimuth and into the forward-scattering lobe, and the bar photograph
 * is framed the same way. The anti-sun views (`river_bank`, looking north) start
 * darker, so subtracting the same fraction of red and green leaves them bluer
 * and DARKER than the photograph: measured at 1° above the north horizon,
 * (104,132,166) — hue improved (B-R +62 against the bar's +55, where before it
 * was +17) but luminance down to 128 against the bar's 160, because red and
 * green are most of what luminance is. So the render brackets the photograph
 * rather than sitting on it, and it now brackets from the blue side instead of
 * the grey side.
 *
 * A floor keyed on the horizon's own chromaticity was tried and thrown away: it
 * scales with the blue channel, and the anti-sun blue is low too, so it moved
 * B-R by three units and earned nothing. Fixing this properly means an azimuth
 * term, and an azimuth term needs a second VERIFIED July photograph shot away
 * from the sun to fit against. `bar/REFERENCES.md` does not have one, and
 * guessing the anti-sun sky from the solar one is exactly the kind of invention
 * this project does not do.
 */
const HORIZON_RESTORE = {
  /** red: how much comes off at the horizon, and the scale in sin(elevation) */
  redAmount: 0.495, redScale: 0.130,
  /** green: two thirds as much to remove, and it reaches a little higher */
  greenAmount: 0.330, greenScale: 0.190,
  /** shared falloff exponent */
  power: 1.6,
};

/**
 * The colour the air itself is, and therefore the colour distance goes to.
 *
 * This is the MEASURED horizon sky of `bar/dupage_tallgrass_2018-07-24.jpg`:
 * sRGB (136,163,192), taken from the twelve pixels immediately above the
 * sky/land step, which is a reading that does not depend on knowing the
 * photograph's field of view.
 *
 * It replaces a hand-picked grey-green (0x98a69d), and the reason is worth
 * keeping. That value was reasoned from "a hazed plain keeps some of its own
 * green", and it does — but it was set so far toward the sward that a
 * fully-hazed surface rendered at sRGB (143,157,130): GREENER than the sky it
 * was supposed to converge on, and REDDER than it was blue (B-R -13). Real
 * aerial perspective pushes distance toward the sky, i.e. BLUE — the bar's own
 * most distant land reads (118,146,145), B-R +27. With a haze that goes the
 * other way, no amount of distance can make ground and air meet: the horizon
 * stayed a step rather than a convergence (63 luminance across four pixels,
 * where the note below this one had designed for 15).
 *
 * The green does not disappear, it just stops being IN the air: the ground
 * keeps its own colour and the haze mixes it toward the sky, which is the
 * order the physics happens in. A fully-hazed surface now renders sRGB
 * (152,175,195) — B-R +43, and 12 luminance off this scene's own horizon sky.
 *
 * Shared with the water's grazing-angle term in terrain.js, and with the
 * horizon-timber band in trees.js, so the river, the far ground and the far
 * timber all agree about what distance looks like. Changing it here without
 * changing it there splits the scene's idea of distance in three.
 */
export const HORIZON_HAZE = 0x88a3c0;

/**
 * Exponential-squared haze, tuned so it is nothing at conversational range,
 * a readable recession across the middle distance, and total at the edge of what
 * is modelled: ~1.7 % at 100 m, 13 % at 300 m, 46 % at 700 m, 98 % at 1500 m.
 *
 * That last figure is the point, and it is a HONESTY constraint rather than a
 * look: docs/LIBERTIES.md L17 records that the ground beyond the 640 m
 * heightfield is a radial skirt carried out to 1400 m — geometry for the horizon
 * only, nothing modelled, sampled or claimed — on the standing condition that
 * "the scene's fog is total by 1500 m". Fog here hides ground we have not built.
 * It must never be turned down far enough to display it, and it is not doing any
 * work the other way either: no distant landform is drawn INTO the haze.
 */
const HAZE_DENSITY = 0.00125;

/**
 * Solar azimuth and elevation, NOAA's algorithm.
 *
 * @param {object} o
 * @param {number} o.lat            degrees north
 * @param {number} o.lon            degrees east (negative west)
 * @param {string} o.date           'YYYY-MM-DD'
 * @param {string} o.localMeanTime  'HH:MM', local mean solar time at `lon`
 * @returns {{azimuthDeg:number, elevationDeg:number, declinationDeg:number,
 *            equationOfTimeMin:number, utcHours:number}}
 */
export function solarPosition({ lat, lon, date, localMeanTime = '12:00' }) {
  const [y, mo, d] = date.split('-').map(Number);
  const [hh, mm] = localMeanTime.split(':').map(Number);
  const localHours = hh + (mm || 0) / 60;

  // Local mean time -> UTC. Longitude west is negative, so this adds.
  const utcHours = localHours - lon / 15;

  // Julian day (Fliegel & Van Flandern), then centuries from J2000.0.
  const a = Math.floor((14 - mo) / 12);
  const yy = y + 4800 - a;
  const mm2 = mo + 12 * a - 3;
  const jdn = d + Math.floor((153 * mm2 + 2) / 5) + 365 * yy + Math.floor(yy / 4)
    - Math.floor(yy / 100) + Math.floor(yy / 400) - 32045;
  const jd = jdn - 0.5 + utcHours / 24;
  const T = (jd - 2451545.0) / 36525;

  const L0 = mod360(280.46646 + T * (36000.76983 + 0.0003032 * T));
  const M = 357.52911 + T * (35999.05029 - 0.0001537 * T);
  const e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T);
  const C = Math.sin(M * DEG) * (1.914602 - T * (0.004817 + 0.000014 * T))
    + Math.sin(2 * M * DEG) * (0.019993 - 0.000101 * T)
    + Math.sin(3 * M * DEG) * 0.000289;
  const trueLong = L0 + C;
  const omega = 125.04 - 1934.136 * T;
  const lambda = trueLong - 0.00569 - 0.00478 * Math.sin(omega * DEG);
  const eps0 = 23 + (26 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60) / 60;
  const eps = eps0 + 0.00256 * Math.cos(omega * DEG);

  const decl = Math.asin(Math.sin(eps * DEG) * Math.sin(lambda * DEG)) / DEG;

  const varY = Math.tan(eps / 2 * DEG) ** 2;
  const eqTime = 4 / DEG * (
    varY * Math.sin(2 * L0 * DEG)
    - 2 * e * Math.sin(M * DEG)
    + 4 * e * varY * Math.sin(M * DEG) * Math.cos(2 * L0 * DEG)
    - 0.5 * varY * varY * Math.sin(4 * L0 * DEG)
    - 1.25 * e * e * Math.sin(2 * M * DEG)
  );

  const trueSolarMin = mod(utcHours * 60 + eqTime + 4 * lon, 1440);
  const hourAngle = trueSolarMin / 4 - 180;

  const latR = lat * DEG, declR = decl * DEG, haR = hourAngle * DEG;
  const cosZenith = Math.min(1, Math.max(-1,
    Math.sin(latR) * Math.sin(declR) + Math.cos(latR) * Math.cos(declR) * Math.cos(haR)));
  const zenith = Math.acos(cosZenith);
  const elevation = 90 - zenith / DEG;

  let azimuth;
  const denom = Math.cos(latR) * Math.sin(zenith);
  if (Math.abs(denom) < 1e-9) {
    azimuth = hourAngle > 0 ? 180 : 0;
  } else {
    const cosAz = Math.min(1, Math.max(-1,
      (Math.sin(latR) * cosZenith - Math.sin(declR)) / denom));
    const a = Math.acos(cosAz) / DEG;
    // NOAA's branch, and it is easy to get backwards: before local solar noon
    // the sun is EAST of south, after it is west. Getting this wrong put the
    // 10 a.m. July sun in the north-east and the shadows on the wrong side.
    azimuth = hourAngle > 0 ? mod360(a + 180) : mod360(540 - a);
  }

  return {
    azimuthDeg: mod360(azimuth),
    elevationDeg: elevation,
    declinationDeg: decl,
    equationOfTimeMin: eqTime,
    utcHours,
  };
}

/** Compass bearing + elevation -> a unit direction in three's world frame. */
export function sunDirection(azimuthDeg, elevationDeg, target = new THREE.Vector3()) {
  const az = azimuthDeg * DEG;
  const el = elevationDeg * DEG;
  const horiz = Math.cos(el);
  return target.set(
    Math.sin(az) * horiz,     // +x east
    Math.sin(el),             // +y up
    -Math.cos(az) * horiz,    // -z north
  ).normalize();
}

function mod(a, n) { return ((a % n) + n) % n; }
function mod360(a) { return mod(a, 360); }

/**
 * Build the sky, the sun and the environment for a scene.
 *
 * @param {object} o
 * @param {THREE.WebGLRenderer} o.renderer
 * @param {THREE.Scene} o.scene
 * @param {object} o.sceneJson   data/scenes/<year>.json
 * @param {object} o.datum       data/datum.json
 * @param {boolean} o.lowSpec    smaller shadow map, cheaper env
 * @param {string[]} [o.problems] collector, same list the scene loader writes to
 */
export function createWorld({
  renderer, scene, sceneJson, datum, lowSpec = false, problems = [],
}) {
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.95;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = lowSpec ? THREE.PCFShadowMap : THREE.PCFSoftShadowMap;

  const sun = solarPosition({
    lat: datum.origin_lat,
    lon: datum.origin_lon,
    date: sceneJson.target_date,
    localMeanTime: sceneJson.lighting?.local_time ?? '12:00',
  });
  const dir = sunDirection(sun.azimuthDeg, sun.elevationDeg);

  // Prairie haze and woodsmoke, per the scene's own lighting note. Turbidity 6
  // is hazier than a clear modern day and cheaper than any volumetric. It is the
  // aerosol term: it whitens the horizon and leaves the zenith alone, which is
  // the right shape — at 24° up it moves the sky by three or four units out of
  // 255, and at 3° up by fourteen.
  const sky = new Sky();
  sky.name = 'sky';
  sky.scale.setScalar(45000);
  sky.material.uniforms.turbidity.value = 6.0;
  sky.material.uniforms.rayleigh.value = 2.2;
  sky.material.uniforms.mieCoefficient.value = 0.006;
  sky.material.uniforms.mieDirectionalG.value = 0.82;
  sky.material.uniforms.sunPosition.value.copy(dir).multiplyScalar(45000 * 0.9);

  // No clouds. The vendored Sky ships an fbm cloud layer on by default
  // (coverage 0.4) whose `time` uniform nothing in this renderer drives, so what
  // it actually produces is one frozen noise field — an invented cloudscape over
  // a specific hour of a specific day, held still. There is no weather record
  // for 1 July 1835; drawing no clouds claims less than drawing those, so the
  // layer is switched off rather than animated.
  sky.material.uniforms.cloudCoverage.value = 0.0;
  sky.material.uniforms.cloudDensity.value = 0.0;

  // The sky's own exposure (see SKY_EXPOSURE). Patched into the vendored shader
  // rather than forked: vendor/ is read-only and pinned by sha256 in
  // vendor/MANIFEST, so this marker cannot move underneath us without a
  // deliberate three bump — and if a bump ever does move it, say so out loud
  // instead of silently rendering the white sky again.
  sky.material.uniforms.skyExposure = { value: SKY_EXPOSURE };
  sky.material.uniforms.horizonAmount = {
    value: new THREE.Vector2(HORIZON_RESTORE.redAmount, HORIZON_RESTORE.greenAmount),
  };
  sky.material.uniforms.horizonScale = {
    value: new THREE.Vector2(HORIZON_RESTORE.redScale, HORIZON_RESTORE.greenScale),
  };
  sky.material.uniforms.horizonPower = { value: HORIZON_RESTORE.power };

  const skyFrag = sky.material.fragmentShader;
  const declared = skyFrag.replace('uniform float time;', /* glsl */`uniform float time;
		uniform float skyExposure;
		uniform vec2 horizonAmount;
		uniform vec2 horizonScale;
		uniform float horizonPower;`);
  // `direction` is the vendored shader's own view ray, already normalised, so
  // direction.y IS sin(elevation) and no trig is needed. Clamped at 0 because
  // the box is drawn below the horizon too and a negative elevation would run
  // the exponential the wrong way; the sliver of sky under the horizontal is
  // a tenth of a degree at eye height and the ground covers it.
  const patched = declared.replace('gl_FragColor = vec4( texColor, 1.0 );', /* glsl */`
			// Restore the wavelength dependence Preetham's saturated (1 - Fex)
			// term loses at the horizon. See HORIZON_RESTORE. Red and green only:
			// the blue channel already matches the reference photograph.
			vec2 chiFade = exp( -pow( max( direction.y, 0.0 ) / horizonScale, vec2( horizonPower ) ) );
			texColor.rg *= max( vec2( 0.0 ), vec2( 1.0 ) - horizonAmount * chiFade );

			gl_FragColor = vec4( texColor * skyExposure, 1.0 );`);
  sky.material.fragmentShader = patched;
  // Both markers are load-bearing and they fail differently: without the first
  // the sky renders at the model's arbitrary scale (a white wash at every
  // elevation), without the second it renders Preetham's white horizon under a
  // correctly exposed zenith. Check them separately so the message names the
  // one that actually broke rather than guessing.
  const lost = [];
  if (declared === skyFrag) lost.push('the exposure uniform (the sky will read as a white wash)');
  if (patched === declared) lost.push('the horizon restore (the skyline will read grey, not blue)');
  if (lost.length) {
    const said = `world: the vendored Sky shader no longer carries ${lost.join(' or ')}`;
    problems.push(said);
    // Also to the console, because the caller is not obliged to pass a collector
    // and a silent fallback to the white sky is exactly the failure this guards.
    console.warn(`[4D Chicago] ${said}`);
  }
  sky.material.needsUpdate = true;
  scene.add(sky);

  // The sky IS the environment. One PMREM pass at boot; nothing animates it.
  //
  // The sun disc MUST be switched off for that pass. Its radiance runs to five
  // or six figures in linear space, which overflows the half-float cube target
  // PMREM blurs through; the overflow becomes Inf, the blur turns Inf into NaN,
  // and a NaN environment map makes every lit surface in the scene render pure
  // black while the sky itself — an unlit shader — keeps looking fine. That is
  // a genuinely baffling failure to debug from the symptom, so it is written
  // down here rather than rediscovered. The disc goes straight back on for the
  // real render, where tone mapping handles it.
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envScene = new THREE.Scene();
  const skyParent = sky.parent;
  sky.material.uniforms.showSunDisc.value = false;
  envScene.add(sky);
  const envRT = pmrem.fromScene(envScene);
  skyParent.add(sky);
  sky.material.uniforms.showSunDisc.value = true;
  // NOT installed as scene.environment. Measured: at 0.40 it rendered a brown
  // log wall at an R/B ratio of 1.08 against the 1.75 its base colour asks for,
  // and even at 0.05 it only reached 1.14 — every surface converging on the sky
  // colour regardless of what it was made of. For a project whose whole claim is
  // that a documented white wall reads as white, an environment that overrides
  // albedo is not a lighting choice, it is a data-integrity problem. The sky is
  // kept as the visible backdrop; the lighting is the hemisphere fill plus the
  // sun, which keep materials' hues intact. Revisit with a properly exposed HDRI
  // rather than a PMREM of an analytic sky.
  envRT.texture.dispose();
  // Kept deliberately low. A PMREM of this sky is an intense, strongly BLUE
  // light, and at any useful intensity it swamps albedo: measured at 0.40, a
  // brown log wall rendered with an R/B ratio of 1.08 against the 1.75 its own
  // base colour specifies — every surface converged on the sky colour and the
  // building read as pale grey whatever it was made of. The environment is here
  // for a touch of specular sky in the glazing, not to light the town. The fill
  // that actually matters is the hemisphere light below, which can be given a
  // warm ground bounce and therefore lets materials keep their hue.

  pmrem.dispose();

  // Sky above, warm ground bounce below — the cheap approximation of outdoor
  // fill, and the one that keeps browns brown. Prairie and mud reflect warm, so
  // the ground colour is a dun rather than a grey.
  const hemi = new THREE.HemisphereLight(0xa8c4e0, 0x7a6b4e, 2.4);
  hemi.name = 'sky-fill';
  scene.add(hemi);

  const light = new THREE.DirectionalLight(0xfff2dc, 3.0);
  light.name = 'sun';
  light.castShadow = true;
  light.position.copy(dir).multiplyScalar(320);
  light.target.position.set(0, 0, 0);
  scene.add(light);
  scene.add(light.target);

  // One tight shadow camera that follows the walker. +/-60 m covers what you can
  // actually resolve on foot; a town-sized frustum would waste every texel.
  const half = 60;
  const cam = light.shadow.camera;
  cam.left = -half; cam.right = half; cam.top = half; cam.bottom = -half;
  cam.near = 1; cam.far = 900;
  cam.updateProjectionMatrix();
  // 1024 over a 120 m frustum is about 12 cm per texel — finer than the shadow
  // of a clapboard eave needs, and a quarter of the fill cost of 2048.
  light.shadow.mapSize.setScalar(lowSpec ? 512 : 1024);
  light.shadow.bias = -0.0004;
  light.shadow.normalBias = 0.045;

  // A little bounce off the prairie and the lake so north elevations are not
  // black. Hemisphere light, not ambient: the ground colour matters. Kept low
  // because the sky environment above is already doing most of this job.
  const bounce = new THREE.HemisphereLight(0xbfd4ea, 0x6d6b45, 0.20);
  scene.add(bounce);

  // Aerial perspective. Exponential-squared rather than the linear ramp it
  // replaces, because linear fog starts at nothing and then turns on: with
  // near 340 / far 1500 the whole walkable town sat at exactly zero haze and the
  // ground at 400 m was the same colour as the ground at 3 m, which is what the
  // baseline showed. Exp2 has no near plane — it is small everywhere and never
  // zero, so distance reads continuously.
  //
  // The colour is HORIZON_HAZE — the photograph's own horizon sky. Distance
  // goes toward the AIR, and the air over a July plain is blue; the prairie's
  // green survives in the mix because the fog only reaches 95 % at the far edge
  // of what is drawn, not because the fog itself is green. See the constant for
  // what the green-tinted haze it replaces did to the horizon.
  scene.fog = new THREE.FogExp2(HORIZON_HAZE, HAZE_DENSITY);

  const offset = new THREE.Vector3();
  return {
    sky, light, bounce, sun, direction: dir.clone(),
    /** Keep the shadow frustum on the walker. Cheap; call every frame. */
    follow(position) {
      light.target.position.set(position.x, 0, position.z);
      light.target.updateMatrixWorld();
      offset.copy(dir).multiplyScalar(320);
      light.position.copy(light.target.position).add(offset);
      light.updateMatrixWorld();
    },
    describe() {
      return `sun ${sun.elevationDeg.toFixed(1)}° up, bearing ${sun.azimuthDeg.toFixed(1)}°`
        + ` (${sceneJson.lighting?.local_time ?? '?'} local mean time, ${sceneJson.target_date})`;
    },
    dispose() {
      envRT.dispose();
      sky.geometry.dispose();
      sky.material.dispose();
    },
  };
}
