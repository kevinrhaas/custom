/**
 * popup.js — pick a building, read its provenance.
 *
 * This is the other half of the confidence view, and the reason the project
 * exists: the tint you see and the citation you can quote come from the SAME
 * sidecar record, so they cannot drift apart. If the shader says amber, the
 * table says `inferred`, and the note underneath says why.
 *
 * The card shows, in order: what it is, where it stands and how sure we are of
 * that, whether it was here at all on the day you are standing in, whether it
 * was this shape, whether any of that is a tracked open question, every attribute
 * with its own confidence chip and reasoning, the liberties taken with THIS
 * building, the citations with links to both the source and its archived copy,
 * and a link out to the full research dossier where the disagreements are argued.
 *
 * The open question is the newest section and it qualifies the two claims above
 * it rather than adding a third. A chip says how sure we are; it cannot say that
 * the uncertainty is a live dispute between two sources, that the grade is being
 * held down deliberately until evidence arrives, and what would change if it did.
 * That was readable in the Evidence panel — whose entry for the standing one says
 * in as many words that "the provenance card shows it" — and not on the building
 * the panel is talking about. Same gap the liberties had, closed the same way.
 *
 * The shape is the newest of those and was the largest silence. The footprint is
 * the biggest single claim a visitor stands in front of, six of the eight in
 * this dataset are placeholders that say so in their first line, and the card
 * showed no chip, no source and no reasoning for any of them — while the
 * confidence tint had been narrowed to stop carrying dimensional uncertainty on
 * the stated understanding that the card would carry it instead.
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
 * The record's own account is the newest section and the last of the compiled
 * fields that reached no visitor. Every structure record carries a
 * `research_note` written for a reader — what it actually asserts, which sources
 * disagree, what was decided and why, where the record is weakest — and it was
 * compiled into every sidecar and shown nowhere. That is not the same fault as
 * the two before it: nothing was broken, the field simply had no surface. It is
 * shown verbatim, because a note about how far the evidence goes is the last
 * thing on this card that should be summarised by a program.
 *
 * Nothing here invents a display value. An attribute with no note shows no note.
 * A citation with no archived copy says so, because the archived copy is part of
 * whether a claim can be re-read at all. And a building with no recorded
 * liberties says exactly that — that none were written down, which is not the
 * same claim as none having been taken.
 */

import { citationItems } from './citations.js';
import { libertiesFor, libertyEntryHtml } from './liberties.js';
// The Evidence panel's own open-question entry, rendered here for the building
// being inspected. Shared for the liberties' reason: the panel's entry for the
// Western Hotel says in as many words that "the provenance card shows it", and
// two renderers would let the two surfaces describe one uncertainty differently.
import { openQuestionsFor, uncertaintyEntryHtml } from './exclusions.js';
// What the mesh does with a value its archetype never reads — `not built`, `not
// modelled from this`. Shared with the Evidence panel's ground section, which
// says the same thing about the terrain: one wording in one module, for the
// reason the liberties have one entry renderer. The argument for the mark, and
// for the two states that deliberately get none, is in that file.
import { geometryMark } from './geometry.js';

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
 *  differently for reasons nobody chose.
 *
 *  A `null` value renders no value cell at all, which is not the same as `—`.
 *  One claim here has no printable value and inventing one would be the exact
 *  fault this card exists to report — see `shapeSection`. The rest of the row is
 *  unchanged, because how sure we are and why is the whole of what a chip, a
 *  source list and a `why` are for. */
function claimRow(label, value, claim) {
  const val = value === null ? '' : `<span class="val">${escapeHtml(value)}</span>`;
  return `<tr>
    <th scope="row">${escapeHtml(label)}</th>
    <td>${val}${evidence(claim)}</td>
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
 * Is this the shape it was?
 *
 * The outline is the largest claim a visitor is standing in front of and the
 * card said nothing about it whatever. Six of the eight footprints in this
 * dataset open with the word PLACEHOLDER — no dimension of the Sauganash, the
 * Wolf Point Tavern, Miller's house or Walker's meeting house is attested in
 * anything read — and two are the opposite: Hogan's store is twenty by
 * forty-five feet in Andreas, twice, and the North Branch bridge's deck is
 * Cleaver's ten feet across a span measured between the traced 1834 banks. A
 * visitor could read none of that. `compile_scene.py` carried the footprint's
 * confidence and dropped its sources and its argument.
 *
 * That gap has a specific history, which is why it is worth a section rather
 * than a line. The massing rule used to take the worst confidence across the
 * footprint, so an unknown SIZE dithered a well-documented building into ghost
 * massing; it was narrowed to the attributes that say what a building WAS, on
 * the stated understanding that dimensional uncertainty would be carried in the
 * sidecar where the popup shows it. The tint stopped saying it and nothing
 * started. So the one claim deliberately taken out of the view is the one the
 * card had no words for.
 *
 * NO DIMENSION IS PRINTED, and that is a decision rather than an omission. The
 * only value available is the polygon, and the only way to print a polygon in a
 * table is to reduce it — a bounding box over Miller's L-plan would be a new
 * invention on the card that exists to admit them, and it would be the reader's
 * impression of a measurement where the record has none. The shape itself is
 * already in front of the visitor at full size. What the card owes is how much
 * of it is evidence, and that is a chip, a source list and the record's own
 * reasoning.
 */
function shapeSection(s) {
  const fp = s.footprint;
  if (!fp || !fp.confidence) return '';
  return `<section class="pop-sec pop-shape">
    <h3>Was it this shape?</h3>
    <table class="attrs"><tbody>
      ${claimRow('footprint', null, fp)}
    </tbody></table>
  </section>`;
}

/**
 * Is what this card just told you actually settled?
 *
 * `data/exclusions.json`'s watch list is the third category — researched, and
 * neither built nor ruled out — and one of its four entries is STANDING in the
 * scene. The Evidence panel has carried all four since they became data, and its
 * entry for the standing one ends by saying that the doubt sits on the record's
 * own dated claim "and the provenance card shows it". The card showed the claim.
 * It never showed that the claim is a tracked open question, so a visitor reading
 * `1834-01-01 → 1840-12-31` with an `inferred` chip over it could learn that we
 * are not certain, and could not learn that the uncertainty is a live dispute
 * between two sources, what settling it would change, or that this project is
 * holding the grade down on purpose until evidence arrives. The doubt reached
 * whoever opened a panel about the whole scene, not whoever walked up to the
 * building it is about — which is the gap the liberties had before they were
 * attached to their buildings.
 *
 * A building with nothing open renders NOTHING here, and that is the honest
 * shape rather than a missing empty state. "No open questions are recorded about
 * this building" would read as *this building is settled*, and the list cannot
 * support that: four entries against roughly forty researched structures, and an
 * open question nobody has noticed is exactly as invisible as a liberty nobody
 * noticed taking. Silence claims nothing; a reassurance would claim a lot.
 */
function openQuestionSection(questions, structureId) {
  if (!Array.isArray(questions)) return '';   // not loaded: claim nothing
  const mine = openQuestionsFor(questions, structureId);
  if (!mine.length) return '';                // nothing open: say nothing
  return `<section class="pop-sec pop-question">
    <h3>Is this settled?</h3>
    <p class="pop-question-lead">No — what this card tells you about this building is
      on the project's list of open questions.</p>
    <div class="liberties">${mine.map((u) => uncertaintyEntryHtml(u, { onCard: true })).join('')}</div>
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
 * What the record says about itself, in the record's own words.
 *
 * `research_note` is on every structure record and in every compiled sidecar,
 * and until now no surface in the walkthrough showed it — the sidecar-contract
 * gate reported it as compiled-and-never-read on 2026-08-10 and called it an
 * unshipped claim rather than dead weight. It is the paragraph that says which
 * of two sources was believed and why, that this building held the post office
 * and is not the post office on the day you are standing in, that the likeliest
 * reconciliation of the evidence is that this record models the wrong building.
 * None of that is expressible as a value with a chip over it, which is why it
 * was written as prose and why it belongs here rather than in a table.
 *
 * Verbatim, and folded away. Verbatim because a note whose subject is the limit
 * of the evidence is the last text on this card that should be trimmed,
 * re-punctuated or summarised — the record's emphasis is the author's, including
 * the shouted phrases, and a renderer that tidied it would be editing a source.
 * Folded because these run to several hundred words and an open one would push
 * the citations off the card on a phone, where the panel is 62vh.
 *
 * @param {object} s  the sidecar
 */
function researchSection(s) {
  const note = s.research_note;
  if (!note) return '';        // no note: no section, and no sentence about why
  return `<section class="pop-sec pop-research">
    <h3>The record's own account</h3>
    <details class="research">
      <summary>in the record's own words</summary>
      <p class="research-body">${escapeHtml(note)}</p>
    </details>
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
  /** Same rule for the scene's open questions: null means "not loaded", which is
   *  not the same claim as "nothing is open about this building". */
  let openQuestions = null;
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

    /**
     * Hand the popup the scene's open questions, for the same reason and with the
     * same redraw: the failure that matters is a card quietly showing fewer
     * caveats than the dataset holds.
     *
     * @param {object[]|null} list  the compiled `uncertain` list for this scene
     */
    setOpenQuestions(list) {
      openQuestions = Array.isArray(list) ? list : null;
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
      // Whether the shape is a stand-in is a fact about the MESH, not about the
      // record, so it arrives on the registry entry from the loader that opened
      // the file. This line read `s.asset_is_placeholder` off the sidecar until
      // 2026-08-10 — a field the compiler has never written and, reading only
      // `data/`, could not write — so the flag never once rendered. Same failure
      // as the presence line before it (STATUS § 28), and the sidecar-contract
      // gate is what found the second one.
      const placeholderAsset = record.assetIsPlaceholder
        ? '<span class="pop-flag">This shape is a placeholder massing, not a bake from the record.</span>'
        : '';
      // `inferred_anonymous`, not `recommended_anonymous`. The dataset's word for
      // these roofs changed with the merge of 2026-08-13 ("recommended" becomes
      // "inferred", which is the vocabulary docs/PROVENANCE.md already uses) —
      // both generators, all 108 records and the GLB filenames moved, and this
      // line did not. The test on a value nothing carries is always false, so
      // every one of the 108 anonymous roofs was rendering with NO reconstruction
      // flag at all: the card stopped saying the building was not a recovered
      // one. That is the third time a card has silently lost a flag by reading a
      // key the data does not write (STATUS § 28, and the placeholder line
      // directly above). The release gate caught it; nothing else would have.
      const reconstruction = s.reconstruction?.status === 'inferred_anonymous'
        ? `<span class="pop-flag"><strong>Inferred reconstruction — anonymous ${escapeHtml(s.reconstruction.family)} roof.</strong>
             Its family and district come from the modern production specification;
             this is not a documented named building or recovered parcel.</span>`
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
          ${reconstruction}
          ${placeholderAsset}
        </div>

        ${presenceSection(s)}

        ${shapeSection(s)}

        ${openQuestionSection(openQuestions, record.id)}

        <section class="pop-sec">
          <h3>Attributes and evidence</h3>
          <table class="attrs"><tbody>${attributeRows(s.attributes)}</tbody></table>
        </section>

        ${libertySection(liberties, record.id)}

        ${researchSection(s)}

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
