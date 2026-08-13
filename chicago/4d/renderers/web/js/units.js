/**
 * units.js — visitor-facing measurement formatting.
 *
 * Scene data, terrain sampling and movement stay in SI units.  This module is
 * the one presentation boundary: a visitor can choose Imperial or Metric in
 * Settings without changing any simulation value or historical record.
 */

const M_TO_FT = 3.280839895;
const MPS_TO_MPH = 2.236936292;
const MPS_TO_KPH = 3.6;
const METRES_PER_MILE = 1609.344;

export function normalUnitSystem(value) {
  return value === 'metric' ? 'metric' : 'imperial';
}

/** Short distances stay in feet/metres; map-scale distances use miles/km. */
export function formatDistance(metres, units = 'imperial') {
  const value = Number(metres) || 0;
  if (normalUnitSystem(units) === 'metric') {
    if (Math.abs(value) >= 1000) return `${(value / 1000).toFixed(1)} km`;
    return `${Math.round(value)} m`;
  }
  if (Math.abs(value) >= METRES_PER_MILE) {
    return `${(value / METRES_PER_MILE).toFixed(1)} mi`;
  }
  return `${Math.round(value * M_TO_FT)} ft`;
}

/** Height remains in feet/metres even at free-fly altitudes. */
export function formatHeight(metres, units = 'imperial') {
  const value = Number(metres) || 0;
  return normalUnitSystem(units) === 'metric'
    ? `${Math.round(value)} m`
    : `${Math.round(value * M_TO_FT)} ft`;
}

export function formatSpeed(metresPerSecond, units = 'imperial') {
  const value = Number(metresPerSecond) || 0;
  return normalUnitSystem(units) === 'metric'
    ? `${(value * MPS_TO_KPH).toFixed(1)} km/h`
    : `${(value * MPS_TO_MPH).toFixed(1)} mph`;
}
