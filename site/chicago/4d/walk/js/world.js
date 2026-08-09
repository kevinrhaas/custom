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
 */

import * as THREE from 'three';
import { Sky } from 'three/addons/objects/Sky.js';

const DEG = Math.PI / 180;

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
 */
export function createWorld({ renderer, scene, sceneJson, datum, lowSpec = false }) {
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.58;
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
  // is hazier than a clear modern day and cheaper than any volumetric.
  const sky = new Sky();
  sky.name = 'sky';
  sky.scale.setScalar(45000);
  sky.material.uniforms.turbidity.value = 6.0;
  sky.material.uniforms.rayleigh.value = 2.2;
  sky.material.uniforms.mieCoefficient.value = 0.006;
  sky.material.uniforms.mieDirectionalG.value = 0.82;
  sky.material.uniforms.sunPosition.value.copy(dir).multiplyScalar(45000 * 0.9);
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
  scene.environment = envRT.texture;
  scene.environmentIntensity = 0.40;
  pmrem.dispose();

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

  scene.fog = new THREE.Fog(0xc9cdbe, 340, 1500);

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
