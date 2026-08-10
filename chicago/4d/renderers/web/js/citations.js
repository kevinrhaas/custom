/**
 * citations.js — one way of showing a source, used everywhere a source is shown.
 *
 * The provenance card and the "what is not here" list both quote the same joined
 * citation records that `tools/compile_scene.py` writes into the sidecars. Two
 * renderers for one record is how two views start disagreeing about the evidence
 * — the liberties entry was pulled into one renderer for exactly that reason, and
 * this is the same move for the citation line.
 *
 * A citation with no archived copy says so. Whether a claim can be re-read is
 * part of the claim, and several of this project's hosts return 503 on a bad day.
 *
 * And a tier says what KIND of source it is, in words. The number alone has been
 * on this line since it was written — `tier 4`, at a visitor with no table to
 * look it up in — while the panel around it argues that a person should be able
 * to judge the evidence themselves. The words are compiled into the sidecar from
 * `data/source.schema.json` (see `tools/tiers.py`), which is the same ladder
 * `check_evidence_ladder` holds the dataset to, so what a value is graded
 * against and what a visitor is told cannot come apart.
 */

export function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

/**
 * `<li>` rows for an `<ol class="cites">`.
 *
 * @param {object[]} citations  joined citation records: source_id, citation, url,
 *                              archived_url, tier, tier_label
 * @param {object} [o]
 * @param {string} [o.empty]    what to say when there are none — the honest note
 *                              differs by context, and "none recorded" is itself
 *                              a finding rather than a blank
 */
export function citationItems(citations, { empty = 'No citations in this record — that is itself a finding.' } = {}) {
  if (!Array.isArray(citations) || !citations.length) return `<li>${escapeHtml(empty)}</li>`;
  return citations.map((c) => {
    const links = [];
    if (c.url) links.push(`<a href="${escapeHtml(c.url)}" target="_blank" rel="noopener">source</a>`);
    if (c.archived_url) {
      links.push(`<a href="${escapeHtml(c.archived_url)}" target="_blank" rel="noopener">archived</a>`);
    } else if (c.url) {
      links.push('<span title="No archived copy recorded; this link may not survive">not archived</span>');
    }
    // the label is the point; the bare number is the fallback for a rung the
    // compiled ladder has no words for, which is a finding for the validator
    // rather than something to print a guess about
    const tier = c.tier
      ? `<span class="tier">tier ${escapeHtml(c.tier)}${c.tier_label ? ` · ${escapeHtml(c.tier_label)}` : ''}</span>`
      : '';
    return `<li><span class="cite-text">${escapeHtml(c.citation ?? c.source_id)}</span>
      ${tier} ${links.join(' · ')}</li>`;
  }).join('');
}
