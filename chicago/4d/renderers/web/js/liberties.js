/**
 * liberties.js — "what we made up", in the walkthrough.
 *
 * The project's standard is that a visitor should be able to tell you which
 * parts we made up. The confidence view and the provenance popup answer that
 * for attributes: pick a building and every value carries its own chip, its
 * sources and its reasoning.
 *
 * They cannot answer it for the decisions that belong to no attribute — that the
 * town is uniformly unpeopled, that two prairie swales were drawn where nothing
 * attests them, that the river is a wall to the walker, that the ground past the
 * box is a skirt and not a claim. Those are the liberties, they are written in
 * `docs/LIBERTIES.md`, and until this module they shipped nowhere a visitor
 * could read them. A confession filed where only the confessor looks is not one.
 *
 * The list is derived, never authored here: `tools/compile_liberties.py` turns
 * the append-only markdown into `data/liberties.json` and `tools/check.sh`
 * re-derives it on every commit, so the panel cannot quietly fall behind the
 * document it is quoting.
 */

/** Escape first, then re-admit exactly two markdown inflections. */
function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function inline(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
}

const SECTION_LABEL = {
  standing: 'whole scene',
  per_subject: 'one subject',
  resolved: 'resolved',
};

function entryHtml(lib, names) {
  const fields = (lib.fields || [])
    // Recorded/Revised are shown as a dateline, not as rows of their own.
    .filter((f) => !/^(Recorded|Revised)$/i.test(f.label));

  const rows = fields.map((f) => `
    <dt>${escapeHtml(f.label)}</dt>
    <dd>${inline(f.text)}</dd>`).join('');

  const subjects = (lib.subjects || [])
    .map((id) => `<span class="lib-subject">${escapeHtml(names.get(id) || id)}</span>`)
    .join('');

  const dateline = lib.revised && lib.revised !== lib.recorded
    ? `recorded ${escapeHtml(lib.recorded)} · revised ${escapeHtml(lib.revised)}`
    : `recorded ${escapeHtml(lib.recorded || '—')}`;

  return `<details class="lib">
    <summary>
      <span class="lib-id">${escapeHtml(lib.id)}</span>
      <span class="lib-title">${escapeHtml(lib.title)}</span>
      <span class="lib-scope">${escapeHtml(SECTION_LABEL[lib.section] || lib.section)}</span>
    </summary>
    <dl class="lib-body">${rows}</dl>
    <p class="lib-meta">${subjects}<span class="lib-date">${dateline}</span></p>
  </details>`;
}

/**
 * Fetch the derived liberties and render them into `mount`.
 *
 * Failure is reported, never papered over: a missing file leaves a line saying
 * the list could not be loaded and pushes the reason onto the loader's problem
 * list, the same one every other integration fault lands on.
 *
 * @param {object} o
 * @param {HTMLElement|null} o.mount    where the list goes
 * @param {URL} o.dataBase              where data/ lives
 * @param {Map<string, object>} [o.registry]  loaded structures, for subject names
 * @param {string[]} [o.problems]       the shared collector
 */
export async function mountLiberties({ mount, dataBase, registry = new Map(), problems = [] }) {
  const names = new Map();
  for (const [id, record] of registry) names.set(id, record?.sidecar?.name || id);

  let doc = null;
  try {
    const url = new URL('liberties.json', dataBase);
    const res = await fetch(url, { cache: 'no-cache' });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    doc = await res.json();
  } catch (err) {
    problems.push(`liberties: ${err.message} — the "what we made up" list is not shown`);
    if (mount) {
      mount.innerHTML = '<p class="legend-note">The liberties list could not be loaded. '
        + 'It is committed at <code>docs/LIBERTIES.md</code>.</p>';
      mount.removeAttribute('aria-busy');
    }
    return { count: 0, liberties: [], error: String(err.message || err) };
  }

  const liberties = Array.isArray(doc.liberties) ? doc.liberties : [];
  if (mount) {
    mount.innerHTML = liberties.map((lib) => entryHtml(lib, names)).join('')
      || '<p class="legend-note">No liberties recorded.</p>';
    mount.removeAttribute('aria-busy');
  }
  return { count: liberties.length, liberties, standard: doc.standard, error: null };
}
