/**
 * exclusions.js — "what is not here", in the walkthrough.
 *
 * Eight buildings stand in a town the sources describe with roughly forty, and
 * from the air that emptiness is the most honest thing in the scene. What it
 * cannot show is the difference between three completely different statements:
 * a structure absent because nobody has researched it yet, one absent because
 * the evidence dates it after 1 July 1835, and one absent because it had already
 * come down. The first is a gap in the work. The other two are findings — they
 * cost research to establish, they carry citations, and until now they lived only
 * in `data/exclusions.json`, where the one audience that cannot read them is the
 * visitor standing in the gap.
 *
 * That file is the research record and stays authored by hand;
 * `tools/compile_scene.py` derives the per-scene view with the citations joined,
 * filtered by the scene's own year — an entry dating a building to 1837 is not an
 * exclusion from an 1837 scene — and `tools/check.sh` re-derives it, so this list
 * cannot fall behind the record it is quoting.
 *
 * The list deliberately does NOT claim to be everything missing. Most of the town
 * is simply not built yet, and saying otherwise would turn an honest hole into a
 * false claim of completeness — which is the failure mode this whole panel exists
 * to avoid.
 */

import { citationItems, escapeHtml } from './citations.js';

/**
 * One excluded structure, collapsed. Same `<details>` shape as a liberty, because
 * they are the same kind of disclosure and a visitor should not have to learn two
 * interfaces to read a confession.
 */
export function exclusionEntryHtml(ex) {
  // The chip is the record's own field, never a phrase derived from its absence:
  // an entry with no `earliest_scene` was excluded because it was GONE, not
  // because it was late, and inventing "gone by 1835" for it would be this
  // project's own sin in miniature. Those entries carry no chip; their reason
  // line says what happened.
  const when = ex.earliest_scene
    ? `<span class="lib-scope">not until ${escapeHtml(ex.earliest_scene)}</span>`
    : '';

  const detail = ex.detail
    ? `<dt>Detail</dt><dd>${escapeHtml(ex.detail)}</dd>`
    : '';

  return `<details class="lib excl">
    <summary>
      <span class="lib-title">${escapeHtml(ex.name || ex.id)}</span>
      ${when}
    </summary>
    <dl class="lib-body">
      <dt>Why it is not here</dt><dd>${escapeHtml(ex.reason || '')}</dd>
      ${detail}
    </dl>
    <ol class="cites excl-cites">${citationItems(ex.citations, {
      empty: 'No citation recorded for this exclusion.',
    })}</ol>
  </details>`;
}

/**
 * Fetch the scene's derived exclusions and render them into `mount`.
 *
 * Failure degrades the section and records a problem on the shared list, the same
 * way the liberties do — a missing file says so rather than rendering an empty
 * list, because an empty "what is not here" reads as "nothing was left out".
 *
 * @param {object} o
 * @param {HTMLElement|null} o.mount
 * @param {URL} o.dataBase        where data/ lives
 * @param {string} o.sceneId      the scene whose sidecars to read
 * @param {string[]} [o.problems] the shared collector
 */
export async function mountExclusions({ mount, dataBase, sceneId, problems = [] }) {
  let doc = null;
  try {
    const url = new URL(`sidecars/${sceneId}/exclusions.json`, dataBase);
    const res = await fetch(url, { cache: 'no-cache' });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    doc = await res.json();
  } catch (err) {
    problems.push(`exclusions: ${err.message} — the "what is not here" list is not shown`);
    if (mount) {
      mount.innerHTML = '<p class="legend-note">The list of researched exclusions could not '
        + 'be loaded. It is committed at <code>data/exclusions.json</code>.</p>';
      mount.removeAttribute('aria-busy');
    }
    return { count: 0, excluded: [], error: String(err.message || err) };
  }

  const excluded = Array.isArray(doc.excluded) ? doc.excluded : [];
  if (mount) {
    mount.innerHTML = excluded.map(exclusionEntryHtml).join('')
      || '<p class="legend-note">No researched exclusions recorded for this scene.</p>';
    mount.removeAttribute('aria-busy');
  }
  return { count: excluded.length, excluded, standard: doc.standard, error: null };
}
