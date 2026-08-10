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
 * liberties taken with THIS building, the citations with links to both the
 * source and its archived copy, and a link out to the full research dossier
 * where the disagreements are argued.
 *
 * The liberties section is the answer to a gap this card had until now. An
 * attribute chip tells a visitor how sure we are of a value we recorded; it
 * cannot tell them about the decisions that belong to no attribute — that the
 * Green Tree's footprint was reasoned out of a room module and its side
 * additions deliberately left off, that three Wolf Point buildings were placed
 * from bank geometry because no corner survives. Those were readable in the
 * Evidence panel as one undifferentiated list of eighteen. Now the ones that
 * constrain the building you are looking at are on the building you are looking
 * at, which is where a visitor would think to ask.
 *
 * The attribute table now answers a second question beside "how sure are you":
 * whether you are looking at the thing at all. An attribute its archetype never
 * reads is marked — `not built` where the model contains nothing of it, `not
 * modelled from this` where a fixed default stands in its place — because a
 * `documented` chip over an unbuilt feature is true about the evidence and false
 * about the view, and the view is what a visitor is standing in.
 *
 * Nothing here invents a display value. An attribute with no note shows no note.
 * A citation with no archived copy says so, because the archived copy is part of
 * whether a claim can be re-read at all. And a building with no recorded
 * liberties says exactly that — that none were written down, which is not the
 * same claim as none having been taken.
 */

import { citationItems } from './citations.js';
import { libertiesFor, libertyEntryHtml } from './liberties.js';

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

/**
 * What the mesh does with a value its archetype never reads.
 *
 * A confidence chip answers how sure we are of a value. It cannot answer whether
 * you are looking at it — and the two come apart in the worst possible direction:
 * the Wolf Point Tavern's painted wolf sign is `documented`, the strongest claim
 * this project makes, on a building with no sign on it. So an attribute the
 * generator does not read says so beside its chip, in the visitor's words rather
 * than the schema's.
 *
 * `record_only` gets no marker on purpose. A rejected reading carried in the
 * record is not a thing missing from the view, and marking it would tell a
 * visitor to go looking for something that was never there.
 */
const GEOMETRY_LABEL = {
  absent: ['not built', 'Attested, and nothing of it is in the model.'],
  simplified: ['not modelled from this', 'Something stands in its place, but this value does not drive it.'],
};

function geometryMark(state) {
  const mark = GEOMETRY_LABEL[state];
  if (!mark) return '';
  return `<span class="geom geom-${escapeHtml(state)}" title="${escapeHtml(mark[1])}"
    >${escapeHtml(mark[0])}</span>`;
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
        ${geometryMark(attr.geometry)}${sourceList(attr.sources)}${note}</td>
    </tr>`;
  }).join('');
}

/**
 * The liberties taken with this building, or an honest note that none are
 * recorded. Rendered with the Evidence panel's own entry renderer so the two
 * views cannot describe the same liberty differently.
 *
 * The scope chip is suppressed for `per_subject` entries — here the subject IS
 * the card — but kept for anything broader, because a scene-wide liberty landing
 * on one building is a fact worth showing rather than flattening.
 */
function libertySection(liberties, structureId) {
  if (!Array.isArray(liberties)) return '';   // not loaded: claim nothing
  const mine = libertiesFor(liberties, structureId);
  const body = mine.length
    ? `<div class="liberties">${mine.map((lib) => libertyEntryHtml(lib, {
      showSubjects: false,
      showScope: lib.section !== 'per_subject',
    })).join('')}</div>`
    : `<p class="pop-lib-none">No liberties are recorded against this building —
         which means none were written down, not that none were taken.</p>`;

  return `<section class="pop-sec pop-liberties">
    <h3>What we made up here${mine.length ? ` <span class="pop-count">${mine.length}</span>` : ''}</h3>
    ${body}
  </section>`;
}

/**
 * @param {HTMLElement} root  the <aside> to render into
 * @param {object} opts
 * @param {string} opts.docBase  where docs/ lives relative to the page
 */
export function createPopup(root, { docBase = '../../' } = {}) {
  let currentId = null;
  /** Null until the derived list loads; never faked to an empty list. */
  let liberties = null;
  let currentRecord = null;

  function close() {
    currentId = null;
    currentRecord = null;
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

    /**
     * Hand the popup the derived liberties once they load. Boot awaits the list
     * before the gate opens, so in practice a card is never drawn without it —
     * but a card already on screen is redrawn rather than left stale, because
     * the one failure mode that matters here is a building quietly showing
     * fewer admissions than the record holds.
     *
     * @param {object[]|null} list  `data/liberties.json`'s `liberties`
     */
    setLiberties(list) {
      liberties = Array.isArray(list) ? list : null;
      if (currentRecord) this.show(currentRecord);
    },

    /** @param {object} record  a registry entry: { id, sidecar, ... } */
    show(record) {
      if (!record?.sidecar) return false;
      const s = record.sidecar;
      currentId = record.id;
      currentRecord = record;

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

        ${libertySection(liberties, record.id)}

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
