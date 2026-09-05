/**
 * census.js — live town/population statistics on the gate screen.
 *
 * T-0036 established the rule: the front screen never carries hand-typed population
 * numbers. Buildings standing and people housed come from `data/town_census.json`.
 * T-0490 extends the same rule to the evidence population: named/attested/inferred/
 * projected/reconstructed counts come directly from `data/residents/index.json`.
 *
 * That distinction matters. `people housed` is the subset already assigned to a dwelling
 * that stands in the rendered town. `named residents` is the evidence population we have
 * identified so far, including people not yet placed. Neither is silently substituted for
 * the November 1835 town census total of 3,265.
 *
 * FAIL SOFT, ALWAYS. Either source may be absent while a branch is being built. Show the
 * rows that can be read and never turn a census nicety into a page error on the first
 * screen a visitor sees.
 */

/** `3265` → `3,265`, in the locale-independent form the rest of the UI uses. */
function group(n) {
  return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

async function readJson(url) {
  try {
    const res = await fetch(url, { cache: 'no-cache' });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

/**
 * Fill the gate census/evidence row from committed derived data.
 *
 * @param {{ dataBase: URL|string, root?: Element|null }} opts
 * @returns {Promise<object|null>} the town census as loaded, or null if it could not be read
 */
export async function mountGateCensus({ dataBase, root }) {
  const host = root ?? document.getElementById('gate-census');
  if (!host) return null;

  const [census, residents] = await Promise.all([
    readJson(new URL('town_census.json', dataBase)),
    readJson(new URL('residents/index.json', dataBase)),
  ]);

  const rows = [];
  const aria = [];

  const standing = Number(census?.buildings?.standing);
  const target = Number(census?.buildings?.target);
  const housed = Number(census?.people?.housed);
  const town = Number(census?.people?.town_total);

  if (Number.isFinite(standing)) {
    rows.push({
      n: standing,
      label: 'buildings standing',
      of: Number.isFinite(target) ? `of the ${group(target)} the town held` : '',
      title: census?.buildings?.basis || '',
    });
    aria.push(`${group(standing)} buildings standing`);
  }

  if (Number.isFinite(housed)) {
    rows.push({
      n: housed,
      label: 'people housed',
      of: Number.isFinite(town) ? `of roughly ${group(town)}` : '',
      title: [census?.people?.basis, census?.people?.town_total_note]
        .filter(Boolean).join(' '),
    });
    aria.push(`${group(housed)} people housed`);
  }

  const counts = residents?.counts || {};
  const named = Number(counts.persons);
  const grades = counts.by_grade || {};
  const attested = Number(grades.attested);
  const inferred = Number(grades.inferred);
  const reconstructed = Number(grades.reconstructed);
  const projected = Number(counts.projected_residents);

  if (Number.isFinite(named)) {
    const parts = [];
    if (Number.isFinite(attested)) parts.push(`${group(attested)} attested`);
    if (Number.isFinite(inferred)) {
      parts.push(Number.isFinite(projected)
        ? `${group(inferred)} inferred (${group(projected)} projected)`
        : `${group(inferred)} inferred`);
    }
    if (Number.isFinite(reconstructed)) parts.push(`${group(reconstructed)} reconstructed`);
    rows.push({
      n: named,
      label: 'named residents',
      of: parts.join(' · '),
      title: residents?._doc || 'Evidence-based named resident population identified so far.',
    });
    aria.push(`${group(named)} named residents${parts.length ? `: ${parts.join(', ')}` : ''}`);
  }

  if (!rows.length) return null;

  host.innerHTML = rows.map((r) => `<p class="gc-fig"${r.title
    ? ` title="${String(r.title).replace(/"/g, '&quot;')}"` : ''}>`
    + `<b class="gc-n">${group(r.n)}</b>`
    + `<span class="gc-l">${r.label}</span>`
    + (r.of ? `<span class="gc-of">${r.of}</span>` : '')
    + '</p>').join('');
  host.setAttribute('aria-label', aria.join(', '));
  host.removeAttribute('hidden');
  return census;
}
