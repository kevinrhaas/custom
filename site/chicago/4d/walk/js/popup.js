/**
 * popup.js — pick a building, read its provenance.
 *
 * This is the other half of the confidence view, and the reason the project
 * exists: the tint you see and the citation you can quote come from the SAME
 * sidecar record, so they cannot drift apart. If the shader says amber, the
 * table says `reconstructed`, and the note underneath says why.
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
 * `attested` chip over an unbuilt feature is true about the evidence and false
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
// The title a visitor reads, which since T-0076 is not the production identity the
// generators number a roof by. Shared with the Go-to menu and the liberties list for
// the reason every other renderer thing here is shared: three surfaces naming one
// building three ways is how a town becomes a spreadsheet.
import { displayName } from './display-name.js';

const CONF_ORDER = { attested: 0, inferred: 1, reconstructed: 2 };

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
  const c = confidence || 'reconstructed';
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
 * Who was here.
 *
 * `data/residents/` reconstructs the town's population as a dataset and draws
 * nobody (docs/LIBERTIES.md L1 stands: v1 ships no human figures). Until this
 * section existed the layer reached no visitor at all — ninety-six researched
 * Chicagoans lived in a JSON file the renderer never fetched, which is
 * indistinguishable, from the street, from not having done the work.
 *
 * A person carries a GRADE, which is a different axis from an attribute's
 * confidence and must not be read as one: `attested` means a source names this
 * person, `inferred` means a real named person whose details are partly
 * reconstructed, `reconstructed` means a hypothesised resident filling a demonstrable
 * need of the town — a claim about a ratio, not about anybody. The chip is
 * therefore rendered in its own class, and an inferred household on a building
 * this project RAISED for it says so in the same breath, because otherwise the
 * card reads as evidence that somebody lived here.
 */
function gradeChip(grade) {
  const g = grade || 'reconstructed';
  return `<span class="grade grade-${escapeHtml(g)}">${escapeHtml(g)}</span>`;
}

function residentsSection(s) {
  const households = Array.isArray(s.residents) ? s.residents : [];
  if (!households.length) return '';

  const blocks = households.map((h) => {
    // `person`, not `p`: this module binds `p` to the sidecar's `placement`, and
    // the sidecar-contract scanner reads a bare `p.name` here as `placement.name`.
    const people = h.persons.map((person) => `<li>
        <span class="res-name">${escapeHtml(person.name)}</span>
        <span class="res-role">${escapeHtml(person.occupation ? person.occupation.replace(/_/g, ' ') : '')}${
          person.relationship && person.relationship !== 'head'
            ? ` · ${escapeHtml(person.relationship)}` : ''}</span>
        ${gradeChip(person.grade)}
        ${noteToggle(person.note)}
      </li>`).join('');
    const basis = h.basis ? `<p class="res-basis">${escapeHtml(h.basis)}</p>` : '';
    return `<div class="res-hh">
      <p class="res-head"><strong>${escapeHtml(h.name)}</strong> — ${escapeHtml(h.relation)}
        ${sourceList(h.sources)}${noteToggle(h.why)}</p>
      ${basis}
      <ul class="res-people">${people}</ul>
    </div>`;
  }).join('');

  return `<section class="pop-sec pop-residents">
    <h3>Who was here</h3>
    <p class="res-lead">From <code>data/residents/</code>. Nobody is drawn: this is the
      population as a dataset, and each person carries how much of them is reconstructed.</p>
    ${blocks}
  </section>`;
}

/**
 * What did we include at each level, and where did it come from?
 *
 * The owner asked for this from a card on the dev preview, and the ask was
 * precise: *"when you say what we made up, say what we included in the
 * recreation, or what we included in the inferred building, or what we included
 * in the attested building."* Everything needed to answer was already on the
 * card and none of it was answered — a visitor could read nineteen rows, each
 * with its own chip, and still not be able to say which parts of the building in
 * front of them are evidence and which are ours. The parts were all there; the
 * summary a person reads FIRST was not.
 *
 * It is a partition, not a highlight reel. Every graded claim the card renders
 * below lands in exactly one row here — the presence claim, the position, the
 * outline and every attribute — so the counts add up to the card and a claim
 * cannot be quietly left out of the summary of itself. That is also what makes
 * it gateable: `smoke_renderer.mjs` recounts the chips off the RENDERED card and
 * requires the same three numbers, which is the only form of this section that
 * cannot drift from the card it describes.
 *
 * The three glosses are the Evidence panel's own words, trimmed at a clause
 * boundary so each is a literal substring of the legend in `index.html` — the
 * liberties' rule, applied to prose that has no shared renderer to hold it. Two
 * surfaces defining `inferred` differently is exactly the drift K23a spent a run
 * cleaning up.
 *
 * WHAT THE SOURCES MEAN CHANGES WITH THE LEVEL, and printing one label over all
 * three would be the same category error the card's own history is made of. On
 * an `attested` claim a source is where the value came FROM. On a `reconstructed`
 * one it is what BOUNDED an invention — the record's own note says so in as many
 * words ("the spec is cited because the invention is bounded by it, which is what
 * makes it defensible rather than arbitrary") — and reading that as attribution
 * would turn the citation into evidence for a building nobody claims existed.
 *
 * An empty level says so rather than disappearing. A building with nothing
 * attested is the single most important thing this section can tell a visitor,
 * and a row that renders only when it is non-empty is a row that goes silent
 * exactly when it matters most. The same reasoning the liberties use for their
 * "none are recorded" note, in the opposite direction.
 *
 * And it does not claim to cover the liberties. A liberty belongs to no
 * attribute — that is why it has its own section — so the lead points at "What we
 * made up here" instead of pretending three rows of claim labels are the whole of
 * what was invented.
 */
const LEVELS = ['attested', 'inferred', 'reconstructed'];

/** The Evidence panel's own definitions (`index.html`, the legend list), each a
 *  literal substring of the legend text so the smoke can prove the two agree. */
const LEVEL_GLOSS = {
  attested: 'a source attests this at the scene date',
  inferred: 'reasoned from evidence about this thing',
  reconstructed: 'no source speaks to this one; built to fill a demonstrable need of the town',
};

/** What a citation IS at this level. Not decoration — see the header. */
const LEVEL_SOURCE_LEAD = {
  attested: 'From',
  inferred: 'Reasoned from',
  reconstructed: 'Bounded by',
};

/** A level with no sources, said plainly. `attested` is the interesting one: the
 *  grade REQUIRES a resolving source (`validate.py`, CONFIDENCE), so a card that
 *  reaches this branch is reporting a defect in its own record rather than a
 *  quirk of presentation, and it should say so where a reader can see it. */
const LEVEL_NO_SOURCE = {
  attested: 'No source is cited — which this grade requires, so the record is at fault.',
  inferred: 'No source is cited; the reasoning for each is on its own row below.',
  reconstructed: 'Nothing is cited as bounding these.',
};

const LEVEL_EMPTY = {
  attested: 'Nothing about this building is attested by a source.',
  inferred: 'Nothing here was reasoned from evidence about this particular building.',
  reconstructed: 'Nothing here was invented.',
};

/** Every graded claim the card renders below, in the order it renders them, and
 *  under exactly the conditions each section uses — a summary that counted a
 *  claim the card suppresses would be describing a different card. */
function gradedClaims(s, place) {
  const claims = [];
  const range = s.documented_range;
  if (range && (range.from || range.to)) {
    claims.push({ label: 'whether it stood here', claim: range });
  }
  claims.push({ label: 'where it stood', claim: place });
  if (s.footprint?.confidence) claims.push({ label: 'its outline', claim: s.footprint });
  for (const [key, attr] of Object.entries(s.attributes || {})) {
    claims.push({ label: prettyName(key), claim: attr || {} });
  }
  return claims;
}

function basisRow(level, mine, total) {
  const sources = [...new Set(mine.flatMap((c) => (
    Array.isArray(c.claim.sources) ? c.claim.sources : [])))];
  const what = mine.length
    ? `<p class="basis-what">${mine.map((c) => escapeHtml(c.label)).join(' · ')}</p>`
    : `<p class="basis-what basis-empty">${escapeHtml(LEVEL_EMPTY[level])}</p>`;
  const from = !mine.length ? ''
    : sources.length
      ? `<p class="basis-from">${escapeHtml(LEVEL_SOURCE_LEAD[level])}:
           ${sources.map(escapeHtml).join(' · ')}</p>`
      : `<p class="basis-from">${escapeHtml(LEVEL_NO_SOURCE[level])}</p>`;
  // An `attested` chip over something the model does not contain is true about
  // the evidence and false about the view — the rows below already mark it, and
  // a summary of what was INCLUDED that ignored it would be the worse half of
  // the same fault.
  const absent = mine.filter((c) => c.claim.geometry === 'absent');
  const notBuilt = absent.length
    ? `<p class="basis-absent">Not in the model:
         ${absent.map((c) => escapeHtml(c.label)).join(' · ')}</p>`
    : '';

  return `<div class="basis-row" data-level="${escapeHtml(level)}">
    <p class="basis-head">${chip(level)}<span class="basis-count">${mine.length} of ${total}</span>
      <span class="basis-gloss">${escapeHtml(LEVEL_GLOSS[level])}</span></p>
    ${what}${from}${notBuilt}
  </div>`;
}

function basisSection(s, place) {
  const claims = gradedClaims(s, place);
  if (!claims.length) return '';

  const buckets = new Map(LEVELS.map((l) => [l, []]));
  // Anything outside the three-level scale. `validate.py` refuses it in the
  // data, so this is not an expected state — but silently folding an unknown
  // grade into `reconstructed` would make the counts lie to hide a bug, and the
  // counts are the whole reason this section can be gated.
  const offScale = [];
  for (const c of claims) {
    (buckets.get(c.claim.confidence || 'reconstructed') ?? offScale).push(c);
  }

  const rows = LEVELS.map((l) => basisRow(l, buckets.get(l), claims.length)).join('');
  const odd = offScale.length
    ? `<div class="basis-row"><p class="basis-head"><span class="basis-count">${offScale.length}
         of ${claims.length}</span> <span class="basis-gloss">not graded on this scale — a fault
         in the record</span></p>
       <p class="basis-what">${offScale.map((c) => escapeHtml(c.label)).join(' · ')}</p></div>`
    : '';

  return `<section class="pop-sec pop-basis">
    <h3>What did we include, and where did it come from?</h3>
    <p class="basis-lead">${claims.length} claims stand behind this building, and every one of
      them is in exactly one row here. The tables further down carry them one at a time, with
      the reasoning behind <em>why</em>; the decisions that belong to no single claim are under
      “What we made up here”.</p>
    ${rows}${odd}
  </section>`;
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
 * `1834-01-01 → 1840-12-31` with an `reconstructed` chip over it could learn that we
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
 * Where a dossier is READ, which is not where it lives in this repository.
 *
 * The card used to link `docBase + s.research_doc` — a path relative to the page,
 * which resolves in the source tree and nowhere a visitor stands: `publish.sh`
 * deliberately leaves `docs/` out of the payload ("the uncompressed GLB masters,
 * the research dossiers and the raw dataset all stay in the repo and out of the
 * payload"), so every card on the deployed site linked to a 404 (ROADMAP K26).
 * The dossiers are markdown and a browser will not render markdown, so publishing
 * them would want a viewer; GitHub already is one, and renders the file with its
 * tables and its images intact.
 *
 * `main` and not `dev`, deliberately: this is the branch a visitor's copy of the
 * walkthrough was promoted from. A dossier written on `dev` and not yet promoted
 * therefore links to a page that appears when the promotion lands — the same lag
 * the rest of the tier carries, rather than a second one.
 */
export const DOSSIER_BASE = 'https://github.com/kevinrhaas/custom/blob/main/chicago/4d/';

/**
 * @param {HTMLElement} root  the <aside> to render into
 * @param {object} opts
 * @param {string} opts.docBase  where a dossier is read — see DOSSIER_BASE
 */
export function createPopup(root, { docBase = DOSSIER_BASE } = {}) {
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
      // "reconstructed", which is the vocabulary docs/PROVENANCE.md already uses) —
      // both generators, all 108 records and the GLB filenames moved, and this
      // line did not. The test on a value nothing carries is always false, so
      // every one of the 108 anonymous roofs was rendering with NO reconstruction
      // flag at all: the card stopped saying the building was not a recovered
      // one. That is the third time a card has silently lost a flag by reading a
      // key the data does not write (STATUS § 28, and the placeholder line
      // directly above). The release gate caught it; nothing else would have.
      //
      // The FLAG's own wording moved with K23a, and the KEY deliberately did not.
      // `inferred_anonymous` is a machine value — it is never printed, it names
      // the GLB files, and the last time a rename of it went through this line
      // the flag silently vanished for 108 roofs. The words a visitor reads are
      // what claimed the wrong tier: this said "Inferred reconstruction" over a
      // record graded `reconstructed` at every attribute, and `inferred` is now
      // the MIDDLE tier — reasoned from evidence about this particular thing,
      // which an anonymous count-unit is exactly not.
      const reconstruction = s.reconstruction?.status === 'inferred_anonymous'
        ? `<span class="pop-flag"><strong>Reconstructed — anonymous ${escapeHtml(s.reconstruction.family)} roof.</strong>
             Its family and district come from the modern production specification;
             this is not an attested named building or a recovered parcel.</span>`
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

      // WHAT THIS BUILDING IS CALLED (T-0076, the owner on 2026-08-18: "give the
      // locations useful names not technical D3 #03 names, you can have that somewhere
      // on the card for reference identity purposes but dont make it the title"). The
      // rule and its reasoning are in display-name.js; what belongs here is the other
      // half of his sentence — the production identity keeps a line on the card, because
      // `Reconstructed D3 one-room frame cottage #017` is what the parcel re-derives,
      // what the GLB is named for, and what somebody reading the dataset has in hand.
      const called = displayName(s, record.id);
      const spec = called.spec
        ? `<p class="pop-spec">Reconstruction reference
             <code>${escapeHtml(called.spec)}</code></p>`
        : '';
      // A title that says "vacant" or "to let" is asserting an ABSENCE, and this project
      // does not let an absence pass as a finding. The residents layer places the
      // households the town's trades demand — 104 of the 222 anonymous roofs — and stops
      // there; the rest are unmodelled, not attested empty. The distinction is one
      // sentence and the alternative is a card that quietly upgrades silence to evidence.
      const unoccupied = called.vacant
        ? `<span class="pop-flag">No household is recorded here, which is not evidence
             that it stood empty. The residents layer models the households this town's
             trades demand and reaches 104 of the anonymous roofs; this is one of the
             others, so the title describes the building rather than its occupancy.</span>`
        : '';

      // Empty when no dossier has been WRITTEN for this record — the compiler
      // resolves the path against the repository rather than naming one by
      // convention and hoping (ROADMAP K26). Thirty documented buildings are in
      // that state, and offering them a link that breaks taught a visitor to
      // distrust the 302 that do not. The sentence says which of the two it is.
      const doc = s.research_doc
        ? `<a href="${escapeHtml(docBase + s.research_doc)}" target="_blank" rel="noopener">
             ${escapeHtml(s.research_doc)}</a>`
        : 'no dossier written for this building yet';

      root.innerHTML = `
        <div class="pop-head">
          <div>
            <h2>${escapeHtml(called.title)}</h2>
            ${aka}
            ${spec}
          </div>
          <button class="pop-close" type="button" data-close aria-label="Close">×</button>
        </div>

        <div class="pop-meta">
          <div><strong>${escapeHtml(p.symbolic_location ?? 'Location not recorded')}</strong>
            ${evidence(place)}</div>
          ${provisional}
          ${reconstruction}
          ${unoccupied}
          ${placeholderAsset}
        </div>

        ${basisSection(s, place)}

        ${presenceSection(s)}

        ${shapeSection(s)}

        ${residentsSection(s)}

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
