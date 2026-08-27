/**
 * census.js — the two numbers on the gate screen: buildings standing, people housed.
 *
 * T-0036, the owner's ask: *"on the front screen, show the number of buildings in the
 * city and the population — people living in their buildings"*, and the population
 * *"should get to the correct Chicago 1835 population number as the buildings all
 * complete"*.
 *
 * NOTHING HERE IS A NUMBER SOMEBODY TYPED, and that is the whole design. Both figures
 * AND both denominators come out of `data/town_census.json`, which `tools/town_census.py`
 * derives from the roof programme and the residents layer and `tools/check.sh`
 * re-derives on every commit. Writing "322" into this file would have been three lines
 * shorter and stale by the next bake — the front screen is the most visible possible
 * place to carry a number the dataset has moved past. The DENOMINATOR proved that on
 * 2026-08-27: T-0032 took the town's roof total from 665 to 662 when three civic slots
 * turned out to count nothing, and this file needed no edit at all.
 *
 * THE SECOND FIGURE IS A FLOOR AND SAYS SO. `people housed` counts person entries in
 * households whose `lives_at` names a building that stands, and three of the entries it
 * counts stand for a group a source counts without naming — an unnamed wife, "the rest
 * of the Beaubien household". Each is at least one person, so the count is a floor on
 * the people this dataset houses and never a population estimate. The town's own recorded
 * size (3,265 in November 1835, four months after the scene date) is quoted as the town's,
 * with the "roughly" the records support, not as the scene's population on 1 July.
 *
 * FAIL SOFT, ALWAYS. A missing or malformed census leaves the row hidden and the gate
 * exactly as it was. A count is not worth a page error on the panel a visitor meets
 * first, and the smoke's zero-pageerrors gate is not a place to spend a nicety.
 */

/** `3265` → `3,265`, in the visitor's locale-independent form the rest of the UI uses. */
function group(n) {
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/**
 * Fill the gate's census row from the committed census document.
 *
 * @param {{ dataBase: URL|string, root?: Element|null }} opts
 * @returns {Promise<object|null>} the census as loaded, or null if it could not be read
 */
export async function mountGateCensus({ dataBase, root }) {
  const host = root ?? document.getElementById('gate-census');
  if (!host) return null;

  let census = null;
  try {
    const res = await fetch(new URL('town_census.json', dataBase), { cache: 'no-cache' });
    if (!res.ok) return null;
    census = await res.json();
  } catch {
    return null;
  }

  const standing = Number(census?.buildings?.standing);
  const target = Number(census?.buildings?.target);
  const housed = Number(census?.people?.housed);
  const town = Number(census?.people?.town_total);
  if (!Number.isFinite(standing) || !Number.isFinite(housed)) return null;

  // Two figures, each with the denominator that makes it mean something. The
  // denominators are the point: 322 alone reads as a total, and it is a progress
  // report on a town that is still being built.
  const rows = [
    { n: standing, label: 'buildings standing',
      of: Number.isFinite(target) ? `of the ${group(target)} the town held` : '',
      title: census?.buildings?.basis || '' },
    { n: housed, label: 'people housed',
      of: Number.isFinite(town) ? `of roughly ${group(town)}` : '',
      title: [census?.people?.basis, census?.people?.town_total_note]
        .filter(Boolean).join(' ') },
  ];

  host.innerHTML = rows.map((r) => `<p class="gc-fig"${r.title
    ? ` title="${r.title.replace(/"/g, '&quot;')}"` : ''}>`
    + `<b class="gc-n">${group(r.n)}</b>`
    + `<span class="gc-l">${r.label}</span>`
    + (r.of ? `<span class="gc-of">${r.of}</span>` : '')
    + '</p>').join('');
  host.setAttribute('aria-label',
    `${group(standing)} buildings standing, ${group(housed)} people housed`);
  host.removeAttribute('hidden');
  return census;
}
