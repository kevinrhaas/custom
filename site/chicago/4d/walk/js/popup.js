/**
 * popup.js — pick a building, read its provenance.
 *
 * This is the other half of the confidence view, and the reason the project
 * exists: the tint you see and the citation you can quote come from the SAME
 * sidecar record, so they cannot drift apart. If the shader says amber, the
 * table says `inferred`, and the note underneath says why.
 *
 * The card shows, in order: what it is, where it stands and how sure we are of
 * that, whether it was here at all on the day you are standing in, every
 * attribute with its own confidence chip and reasoning, the liberties taken with
 * THIS building, the citations with links to both the source and its archived
 * copy, and a link out to the full research dossier where the disagreements are
 * argued.
 *
 * "Whether it was here at all" is the newest of those and was the oldest gap.
 * This file has read `documented_range` since it was written and the sidecar
 * compiler never wrote the field, so the line never rendered once: the claim the
 * entire scene rests on — that this building stood in Chicago on 1 July 1835 —
 * was the one claim on the card with no chip, no source and no reasoning, while
 * a roof pitch had all three. The same was half-true of the position, whose
 * argument is often the longest thing in the record and reached the card as a
 * bare chip. Both now render through the attribute table's own row renderer,
 * because a card that qualified its load-bearing claims differently from its
 * details is how the two drift.
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

/**
 * The reasoning, folded away behind `why`.
 *
 * Split out of the attribute row because the phase-level claims need exactly the
 * same affordance and a second implementation of it would drift — the same
 * argument that put the Evidence panel and this card on one liberty renderer.
 * An empty note renders nothing at all: a `why` button that opens on silence
 * teaches a visitor that the reasoning is missing everywhere.
 */
function noteToggle(note) {
  if (!note) return '';
  return `<span class="attr-note" data-note hidden>${escapeHtml(note)}</span>
    <button class="attr-toggle" type="button" data-toggle-note>why</button>`;
}

/** Chip, sources and reasoning — everything that qualifies a value. */
function evidence(claim) {
  return `${chip(claim.confidence)}${geometryMark(claim.geometry)}
    ${sourceList(claim.sources)}${noteToggle(claim.note)}`;
}

function attributeRows(attributes) {
  const entries = Object.entries(attributes || {});
  entries.sort((a, b) => (CONF_ORDER[a[1].confidence] ?? 3) - (CONF_ORDER[b[1].confidence] ?? 3)
    || a[0].localeCompare(b[0]));

  return entries.map(([key, attr]) => claimRow(prettyName(key), prettyValue(attr.value), attr))
    .join('');
}

/** One row of the evidence table. Used by the attribute table and by the
 *  phase-level claims above it, so the two cannot be styled or qualified
 *  differently for reasons nobody chose. */
function claimRow(label, value, claim) {
  return `<tr>
    <th scope="row">${escapeHtml(label)}</th>
    <td><span class="val">${escapeHtml(value)}</span>${evidence(claim)}</td>
  </tr>`;
}

/**
 * Was this building here on the day you are standing in, and how do we know
 * where it stood?
 *
 * These two are the load-bearing claims of the whole scene and the card carried
 * neither of their arguments. The date span never rendered at all — the markup
 * read `documented_range` and the compiler never wrote it — so a visitor could
 * read why a roof pitch was 35 degrees and not why the building was in the town.
 *
 * The dates are printed as recorded rather than prettified. `1835-12-31` is
 * frequently the end of a continuity argument rather than an event, and turning
 * it into "December 1835" would dress a bound up as a date somebody wrote down;
 * the note beside it is where that is explained, in the record's own words.
 */
function presenceSection(s) {
  const range = s.documented_range;
  if (!range || !(range.from || range.to)) return '';

  const span = `${range.from || '?'} → ${range.to || '?'}`;
  const account = s.change_note
    ? `<p class="pop-account">${escapeHtml(s.change_note)}</p>` : '';

  return `<section class="pop-sec">
    <h3>Was it here?</h3>
    ${account}
    <table class="attrs"><tbody>
      ${claimRow('recorded standing', span, range)}
    </tbody></table>
  </section>`;
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

      // The position's own reasoning, on the line that shows the position. Every
      // placement here is an argument — three of the eight are derived from bank
      // geometry because no corner survives — and the card showed the conclusion
      // with a chip over it and no way to read the argument.
      const place = {
        confidence: p.position_confidence,
        sources: p.position_sources,
        note: p.position_note,
      };

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
            ${evidence(place)}</div>
          ${provisional}
          ${placeholderAsset}
        </div>

        ${presenceSection(s)}

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
