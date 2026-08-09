/**
 * popup.js — pick a building, read its provenance.
 *
 * This is the other half of the confidence view, and the reason the project
 * exists: the tint you see and the citation you can quote come from the SAME
 * sidecar record, so they cannot drift apart. If the shader says amber, the
 * table says `inferred`, and the note underneath says why.
 *
 * The card shows, in order: what it is, where it stands and how sure we are of
 * that, every attribute with its own confidence chip and reasoning, the
 * citations with links to both the source and its archived copy, and a link out
 * to the full research dossier where the disagreements are argued.
 *
 * Nothing here invents a display value. An attribute with no note shows no note.
 * A citation with no archived copy says so, because the archived copy is part of
 * whether a claim can be re-read at all.
 */

const CONF_ORDER = { documented: 0, inferred: 1, conjectural: 2 };

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function prettyName(key) {
  return key.replace(/_/g, ' ').replace(/\bm\b/, '(m)');
}

function prettyValue(v) {
  if (v === true) return 'yes';
  if (v === false) return 'no';
  if (v === null || v === undefined) return '—';
  if (typeof v === 'number') return String(v);
  return String(v).replace(/_/g, ' ');
}

function chip(confidence) {
  const c = confidence || 'conjectural';
  return `<span class="conf conf-${escapeHtml(c)}">${escapeHtml(c)}</span>`;
}

function sourceList(sources) {
  if (!Array.isArray(sources) || !sources.length) return '';
  return `<span class="attr-note">sources: ${sources.map(escapeHtml).join(', ')}</span>`;
}

function attributeRows(attributes) {
  const entries = Object.entries(attributes || {});
  entries.sort((a, b) => (CONF_ORDER[a[1].confidence] ?? 3) - (CONF_ORDER[b[1].confidence] ?? 3)
    || a[0].localeCompare(b[0]));

  return entries.map(([key, attr]) => {
    const note = attr.note
      ? `<span class="attr-note" data-note hidden>${escapeHtml(attr.note)}</span>
         <button class="attr-toggle" type="button" data-toggle-note>why</button>`
      : '';
    return `<tr>
      <th scope="row">${escapeHtml(prettyName(key))}</th>
      <td><span class="val">${escapeHtml(prettyValue(attr.value))}</span>${chip(attr.confidence)}
        ${sourceList(attr.sources)}${note}</td>
    </tr>`;
  }).join('');
}

function citationItems(citations) {
  if (!Array.isArray(citations) || !citations.length) {
    return '<li>No citations in this record — that is itself a finding.</li>';
  }
  return citations.map((c) => {
    const links = [];
    if (c.url) links.push(`<a href="${escapeHtml(c.url)}" target="_blank" rel="noopener">source</a>`);
    if (c.archived_url) {
      links.push(`<a href="${escapeHtml(c.archived_url)}" target="_blank" rel="noopener">archived</a>`);
    } else if (c.url) {
      links.push('<span title="No archived copy recorded; this link may not survive">not archived</span>');
    }
    const tier = c.tier ? `<span class="tier">tier ${escapeHtml(c.tier)}</span>` : '';
    return `<li><span class="cite-text">${escapeHtml(c.citation ?? c.source_id)}</span>
      ${tier} ${links.join(' · ')}</li>`;
  }).join('');
}

/**
 * @param {HTMLElement} root  the <aside> to render into
 * @param {object} opts
 * @param {string} opts.docBase  where docs/ lives relative to the page
 */
export function createPopup(root, { docBase = '../../' } = {}) {
  let currentId = null;

  function close() {
    currentId = null;
    root.setAttribute('hidden', '');
    root.innerHTML = '';
  }

  root.addEventListener('click', (e) => {
    if (e.target.closest('[data-close]')) { close(); return; }
    const toggle = e.target.closest('[data-toggle-note]');
    if (toggle) {
      const note = toggle.parentElement.querySelector('[data-note]');
      const shown = !note.hasAttribute('hidden');
      note.toggleAttribute('hidden', shown);
      toggle.textContent = shown ? 'why' : 'hide';
    }
  });

  return {
    get openId() { return currentId; },
    close,

    /** @param {object} record  a registry entry: { id, sidecar, ... } */
    show(record) {
      if (!record?.sidecar) return false;
      const s = record.sidecar;
      currentId = record.id;

      const p = s.placement ?? {};
      const provisional = p.placement_provisional
        ? `<span class="pop-flag">Position is provisional — the coordinates are a stand-in,
             not a survey. Georeferencing from the 1834 sheets is not better than about
             ±${escapeHtml(p.uncertainty_m ?? 20)} m even once traced.</span>`
        : '';
      const placeholderAsset = s.asset_is_placeholder
        ? '<span class="pop-flag">This shape is a placeholder massing, not a bake from the record.</span>'
        : '';

      const range = s.documented_range
        ? `<div>Standing <strong>${escapeHtml(s.documented_range.from ?? '?')}</strong>
             to <strong>${escapeHtml(s.documented_range.to ?? '?')}</strong> ${chip(s.documented_range.confidence)}</div>`
        : '';

      const aka = Array.isArray(s.aka) && s.aka.length
        ? `<p class="pop-aka">also ${s.aka.map(escapeHtml).join(' · ')}</p>` : '';

      const doc = s.research_doc
        ? `<a href="${escapeHtml(docBase + s.research_doc)}" target="_blank" rel="noopener">
             ${escapeHtml(s.research_doc)}</a>`
        : 'no dossier recorded';

      root.innerHTML = `
        <div class="pop-head">
          <div>
            <h2>${escapeHtml(s.name ?? record.id)}</h2>
            ${aka}
          </div>
          <button class="pop-close" type="button" data-close aria-label="Close">×</button>
        </div>

        <div class="pop-meta">
          <div><strong>${escapeHtml(p.symbolic_location ?? 'Location not recorded')}</strong>
            ${chip(p.position_confidence)}</div>
          ${range}
          ${provisional}
          ${placeholderAsset}
        </div>

        <section class="pop-sec">
          <h3>Attributes and evidence</h3>
          <table class="attrs"><tbody>${attributeRows(s.attributes)}</tbody></table>
        </section>

        <section class="pop-sec">
          <h3>Citations</h3>
          <ol class="cites">${citationItems(s.citations)}</ol>
        </section>

        <p class="pop-foot">Full dossier: ${doc}<br>
          Phase <code>${escapeHtml(s.phase ?? '—')}</code> ·
          record <code>${escapeHtml(record.id)}</code></p>
      `;
      root.removeAttribute('hidden');
      root.scrollTop = 0;
      return true;
    },
  };
}
