/**
 * residents.js — the town's people, in the Evidence panel.
 *
 * ROADMAP K52, from K51. `data/residents/` holds 201 households and 237 person
 * entries, every one of them graded and most of them cited, and unlike this
 * morning's fauna the layer already had *a* reader: `tools/compile_scene.py`
 * attaches a household to a building's sidecar and `popup.js` names it on the
 * building card. K52's own box says that makes it the harder question rather
 * than the easier one — *"a layer with one reader is exactly where an unread
 * figure hides, because 'the browser has it' reads as 'somebody looks at it'."*
 *
 * IT HID SEVENTEEN HOUSEHOLDS. `compile_residents()` reaches a building through
 * `lives_at` or `works_at`, so a household whose residence and workplace are
 * both unattested at the scene date attaches to nothing and appears on no card
 * anywhere — 17 households and 20 person entries, and one of them is the Mark
 * Beaubien household, which is the most famous in the town and one of the
 * thinnest records in the dataset. A dataset that drops a record for being
 * *poorly evidenced* is doing the opposite of what this project's confidence
 * model is for.
 *
 * AND IT CARRIED ONLY A THIRD OF EACH RECORD IT DID REACH. The building card
 * shows a household's name, division, relation, its note and its persons' names,
 * relationships, grades and occupation words. `arrival`, `origin`,
 * `reason_for_coming`, `party_size_on_arrival`, `present_on_scene_date` and
 * `touches_removal` reach nothing; nor do a person's `sex`, `age_on_scene_date`,
 * `birth_year`, `name_basis` or their own `sources`, nor the occupation's grade
 * and reasoning, nor the ten `researched_not_resident` findings — which are the
 * exclusions-style half of the dataset and as load-bearing as the households.
 *
 * TWO EVIDENCE STRENGTHS, KEPT APART (T-0378). The newspaper register reads people
 * out of the Democrat and the American, and the two kinds it reads are not the same
 * claim: a man who advertised his stock is named, dated, placed and given a trade,
 * while a name in the post office's list of uncalled-for letters is a name and
 * nothing else. `mint_letter_list_residents.py` carries `letter_list_only` onto the
 * person for the second kind, and this file is where the distinction has to survive
 * — it reached `gazetteer.json` and `register_1835.json` and stopped there, so on the
 * card the two read identically. It is now a row of its own on the person, and a
 * clause in the section's own count sentence.
 *
 * WHAT THIS IS NOT. It is a card, not a crowd. Nothing here is drawn: L1 and
 * AGENTS.md stand, v1 ships no human figures, and the standing constraint on
 * depicting the Potawatomi in the year of the removal is untouched by a section
 * that publishes what the sources say and nothing else.
 *
 * AND THEN THAT DISTINCTION BECAME THE SHAPE OF THE SECTION (T-0379). The owner was
 * asked how many of the letter-list names the town should hold and ruled, on
 * 30 August 2026, that it should hold every one the evidence admits. That is the
 * largest single change to this town's population the corpus can make — it took it
 * from a couple of hundred people to most of a thousand, roughly three quarters of
 * them a name on a post-office list and nothing else — and the ruling set its own
 * test for whether the implementation was any good: *a visitor who looks at the
 * whole must be able to tell at a glance which three quarters are names alone. If
 * that reads as a wall of undifferentiated people, the ruling has been implemented
 * badly, not chosen badly.* So the list is SPLIT rather than sorted: the households
 * the rest of the corpus documents keep the section they had, at the length they
 * had, and the cohort sits under them in one closed group that says what it is.
 *
 * ONE FETCH, THEN ONE PER HOUSEHOLD A VISITOR OPENS. The manifest is a
 * denormalised summary of every record — `tools/validate.py` fails the build
 * when a copy disagrees with its record — so the list renders from a single
 * file, and the full record is fetched the first time its own row is opened.
 * A fetch per household on mount, to show that many collapsed summaries, would be
 * a worse card and a slower one; the summary is the manifest's job and the manifest
 * says so. That was true of 201 records and it is the load-bearing decision at 920.
 */

import { citationItems, escapeHtml } from './citations.js';

/** A closed-set token as a reader should see it: `tavern_keeper`. */
export function words(token) {
  return String(token ?? '').replace(/_/g, ' ');
}

/** Order a value by its own vocabulary, unknown words last. */
function rank(list, value) {
  const i = Array.isArray(list) ? list.indexOf(value) : -1;
  return i < 0 ? 999 : i;
}

/**
 * The Evidence panel's own confidence swatch — one vocabulary for the whole
 * walkthrough. A person's `grade` and an attribute's `confidence` are two
 * different axes (the manifest is emphatic that they must not be conflated) but
 * they share the three words, so they share the chip rather than inventing a
 * second one that means the same thing.
 */
export function swatch(level) {
  const cls = { attested: 'sw-doc', inferred: 'sw-inf' }[level] || 'sw-rec';
  return `<i class="sw ${cls}" title="${escapeHtml(level || 'reconstructed')}"></i>`;
}

/**
 * `1835-07-01` as a reader should see it. The letter-list records carry the dates
 * of the returns that printed them as ISO strings so a gate can read them; a card
 * is not a database, and a visitor reading which day the post office was holding
 * a letter should not have to parse one.
 */
export function printedOn(iso) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(iso ?? ''));
  if (!m) return String(iso ?? '');
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];
  return `${Number(m[3])} ${months[Number(m[2]) - 1]} ${m[1]}`;
}

/** A `<dt>/<dd>` pair, omitted entirely when the record carries nothing. */
function row(label, value) {
  if (value === null || value === undefined || value === '') return '';
  return `<dt>${escapeHtml(label)}</dt><dd>${escapeHtml(value)}</dd>`;
}

/**
 * A graded household claim — `arrival`, `origin`, `reason_for_coming`,
 * `lives_at`, `works_at`, `present_on_scene_date` — as its value, its
 * confidence, its reasoning and its sources.
 *
 * The reasoning is the point. On this layer a note routinely says the record is
 * NOT attested and why the figure is carried anyway, and a card printing only
 * the value would be hiding the best part of it: Mark Beaubien's arrival year is
 * *"the figure in general circulation … carried as a conjecture that cites
 * nothing, precisely so that a reader can see it is not evidence."*
 *
 * `value` is passed in beside the block rather than dug out of it here, the same
 * way `fauna.js` does it and for the same reason: a figure read through a
 * generic accessor is a figure a read census cannot see in this file's text.
 */
function claimRow(label, value, block, citationsById) {
  if (!block) return '';
  const shown = value === null || value === undefined || value === ''
    ? 'not recorded' : value;
  const note = block.note ? `<br><span class="res-why">${escapeHtml(block.note)}</span>` : '';
  const cites = (block.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  const list = cites.length ? `<ol class="cites">${citationItems(cites)}</ol>` : '';
  return `<dt>${escapeHtml(label)}</dt>
    <dd>${swatch(block.confidence)}${escapeHtml(shown)}${note}${list}</dd>`;
}

/**
 * The household's kin rows — a relationship that crosses to ANOTHER household
 * record (T-0597).
 *
 * `persons[].relationship` is a person's place inside one household and stops
 * at its edge, so until `kin` existed the only place a family tie between two
 * records could go was a free-text note, where a reader may find it and a query
 * never will. The row renders like any other graded claim, which is the whole
 * argument: the tie carries its confidence swatch, its reasoning and its
 * citations exactly as an arrival does, because it is exactly as much of a
 * claim as an arrival is.
 *
 * The far person and household are shown as their ids, humanised the same way
 * the collapsed summary humanises a household id. The card holds ONE record —
 * the others are fetched only when their own row is opened — so printing a
 * neighbour's display name here would mean either a fetch per kin row or a
 * denormalised copy that can go stale, and the manifest's rule is that a copy
 * which can disagree with its record does not get made.
 */
function kinRows(hh, citationsById) {
  const kin = Array.isArray(hh.kin) ? hh.kin : [];
  return kin.map((k) => claimRow(
    'Related to',
    `${words(k.person)} is the ${words(k.relation)} of ${words(k.value)}, `
      + `in the ${words(String(k.household ?? '').replace(/^hh_/, ''))} household`,
    k,
    citationsById,
  )).join('');
}

/**
 * One person. `grade` says how much of the PERSON is reconstructed and the
 * occupation's `confidence` says how well that one attribute is evidenced —
 * the manifest's two orthogonal axes, shown as two chips rather than merged
 * into a single misleading one.
 *
 * The five placeholder entries are the reason `name_basis` and the note are
 * printed here: an unnamed wife or "four children" is an ADMISSION carrying a
 * count, and the record says in as many words that it must not be counted as an
 * individual. That sentence belongs in front of a reader, not in a JSON file.
 *
 * THREE OF THESE ARE GRADED CLAIM BLOCKS AND WERE PRINTED AS OBJECTS. `age_on_
 * scene_date`, `birth_year` and `name_basis` carry `{value, confidence, note,
 * sources}` exactly like the household's own claims, and this function handed
 * the whole block to `row()`, which escapes whatever it is given: 113 person
 * rows read `How this person is named — [object Object]` and nine read it twice
 * more for the age and the birth year. The census of ROADMAP K52 (T-0021) is
 * what found it, and it is the finding that section exists to make — a figure
 * that reaches the card as `[object Object]` has not reached a visitor, and the
 * sentence it was hiding is the one this project most needs read: *"THE NAME IS
 * INVENTED. No source names this resident."* They go through `claimRow` now,
 * with the same swatch, reasoning and citations every other graded claim gets.
 */
function researchHtml(review, citationsById) {
  if (!review) return '';
  const labels = {
    corroborated_enrichment: 'corroborated profile finding',
    candidate_identity: 'candidate identity — not merged',
    no_corroboration: 'reviewed — no safe match found',
  };
  const cites = (review.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  const candidates = (review.candidates || []).map((candidate) => {
    const cc = (candidate.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
    return `<li><b>${escapeHtml(candidate.name)}</b> · ${escapeHtml(words(candidate.assessment))}
      <br><span class="res-why">${escapeHtml(candidate.basis)} ${escapeHtml((candidate.conflicts || []).join(' '))}
      This candidate is not an asserted identity.</span>
      ${cc.length ? `<ol class="cites">${citationItems(cc)}</ol>` : ''}</li>`;
  }).join('');
  return `<dt>Resident research review</dt><dd><span class="res-chip res-research">${
      escapeHtml(labels[review.outcome] || words(review.outcome))}</span>
    <span class="res-why">Reviewed ${escapeHtml(printedOn(review.reviewed_on))}. ${
      escapeHtml(review.summary)} A no-find records the limits of this search; it is not
      evidence that the person did not exist.</span>
    ${candidates ? `<ul class="res-candidates">${candidates}</ul>` : ''}
    ${cites.length ? `<ol class="cites">${citationItems(cites)}</ol>` : ''}</dd>`;
}

/**
 * The 1840 census household a person's record is bridged to — five years after
 * this scene, and that gap is the whole reason this block is rendered rather
 * than banked.
 *
 * PR #670 attached the bridge to three people and declared none of its figures,
 * so twenty-four values were being shipped to a browser with nothing reading
 * them (T-0491). Banking them would have been the cheap answer and the wrong
 * one: an identity bridge is an ARGUMENT — a transcribed name, a normalised
 * reading of it, the page and row it stands on, the serial it was assigned and
 * three separate confidences in those steps — and an argument a visitor cannot
 * see is an assertion. It is shown whole, headed by the year, so that no part of
 * it can be mistaken for an 1835 fact.
 *
 * THE HOUSEHOLD TALLIES ARE SHOWN FOR THE SAME REASON. They are the strongest
 * temptation on this card — six people under a roof in 1840 is not six people
 * under it in 1835 — and the record's own note says so in as many words. The
 * note is printed directly beneath them, because a figure withheld cannot be
 * argued with and a figure shown with its refusal can.
 */
function laterCensusHtml(census, citationsById) {
  if (!census) return '';
  const hh = census.household || {};
  const cite = citationsById.get(census.source_id);
  const tallies = [
    ['People in the household', hh.persons],
    ['Children under ten', hh.children_under_10],
    ['Male', hh.male],
    ['Female', hh.female],
    ['Employed in agriculture', hh.agriculture],
    ['Employed in commerce', hh.commerce],
    ['Employed in manufactures and trades', hh.manufactures_trades],
    ['Employed in inland navigation', hh.inland_navigation],
    ['In a learned profession or engineering', hh.professions_engineering],
    ['Foreigners not naturalized', hh.foreigners_not_naturalized],
    ['Over twenty-one and unable to read or write', hh.illiterate_over_21],
  ].filter(([, n]) => Number.isFinite(n))
    .map(([label, n]) => `<li>${escapeHtml(label)}: ${escapeHtml(String(n))}</li>`)
    .join('');
  return `<dt>Found again in the ${escapeHtml(String(census.year))} census</dt>
    <dd>${swatch(null)}Head of household <b>${escapeHtml(census.head_name_normalized)}</b>,
      transcribed on the page as <q>${escapeHtml(census.head_name_transcribed)}</q>${
        census.bridge_status ? ` · ${escapeHtml(words(census.bridge_status))} bridge` : ''}
      <br><span class="res-why">Page ${escapeHtml(String(census.census_page))}, row ${
        escapeHtml(String(census.census_row))}, enumeration serial ${
        escapeHtml(String(census.serial))}${
        census.source_image ? `, from image ${escapeHtml(census.source_image)}` : ''}${
        census.source_kind ? ` (${escapeHtml(census.source_kind)})` : ''}.
        The reading of the name is graded ${escapeHtml(words(census.name_confidence))}, the
        identification of it with this person ${escapeHtml(words(census.identity_confidence))},
        and the assignment of the row to that serial ${
        escapeHtml(words(census.serial_mapping_confidence))} — three separate steps, each of
        which can be wrong on its own.</span>
      <br><span class="res-why">${escapeHtml(census.bridge_basis)}</span>
      ${tallies ? `<ul class="res-candidates">${tallies}</ul>` : ''}
      ${census.note ? `<span class="res-why">${escapeHtml(census.note)}</span>` : ''}
      ${cite ? `<ol class="cites">${citationItems([cite])}</ol>` : ''}</dd>
    ${scanHtml(census, citationsById)}`;
}

/**
 * The same line, read off the photograph of the sheet (T-0530).
 *
 * The block above it is a RECOVERY: 210 rows taken out of a workbook the owner
 * has ruled lost, which cite no line on any page. Where the page has since been
 * read — column by column, checked against the footings the enumerator wrote at
 * the bottom of his own sheet — the two do not always agree, and on the one
 * household this reaches they disagree about how many people in it were men.
 *
 * BOTH ARE SHOWN, and the sentence between them says which is senior and why.
 * Replacing the recovered figures with the scan would have been tidier and would
 * have destroyed the finding: the bridge that put this person on this line was
 * built out of the workbook's row, so a card showing only the sheet would be
 * quoting evidence the identification never rested on.
 */
function scanHtml(census, citationsById) {
  const scan = census.scan_verified;
  if (!scan) return '';
  const cites = (scan.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  const tallies = [
    ['People on the line', scan.free_persons],
    ['Male', scan.males],
    ['Female', scan.females],
    ['Children under ten', scan.children_under_10],
  ].filter(([, n]) => Number.isFinite(n))
    .map(([label, n]) => `<li>${escapeHtml(label)}: ${escapeHtml(String(n))}</li>`)
    .join('');
  return `<dt>Read again off the page itself</dt>
    <dd>${swatch('attested')}Line ${escapeHtml(String(scan.line))} of the photographed sheet,
      where the head of the household is written <q>${escapeHtml(scan.head_name_as_read)}</q>.
      <br><span class="res-why">From ${escapeHtml(scan.image)}, read by ${escapeHtml(scan.read_by)}.</span>
      ${tallies ? `<ul class="res-candidates">${tallies}</ul>` : ''}
      <span class="res-why">On the line, band by band: ${escapeHtml(scan.age_bands)}.</span>
      <br><span class="res-why">The sheet foots its own columns and that footing is the only
        check this reading has: ${escapeHtml(scan.column_totals_check)}.</span>
      ${census.scan_disagreement
        ? `<br><span class="res-why">${escapeHtml(census.scan_disagreement)}</span>` : ''}
      ${cites.length ? `<ol class="cites">${citationItems(cites)}</ol>` : ''}</dd>`;
}

/**
 * The Chicago directories of 1839, 1843 and 1844, on the people they meet (T-0632).
 *
 * Every volume here is later than this scene and that gap is the whole reason this
 * is rendered rather than banked. A later line can only do two things for a person
 * of 1835 — say they were still in Chicago, and print a trade or a street the 1835
 * record never had — and both of those are ARGUMENTS a reader can only disagree
 * with if they can see the line, the page and the rule that reached it.
 *
 * THE THREE STATUSES ARE ALL SHOWN, and that is the point of the section rather
 * than a caveat on it. A person met by one entry nobody else meets is a single
 * entry; met by several, this project does not choose between them; sharing one
 * entry with another person in this town, no match is made. A section that showed
 * only the first would be reporting the crosswalks' successes and hiding their
 * arithmetic.
 *
 * WHAT CROSSES AND WHAT DOES NOT. Norris's alphabetical volume sets a partnership
 * where the trade would go — "of Horace Norton & Co", twice simply "of" — so its
 * split yields a value containing no trade at all and T-0569 refused it. The line
 * is quoted and its parse is not. The Fergus volumes set the trade first and its
 * qualifiers after, so their split crosses with the caution printed beside it.
 */
function laterDirectoryHtml(found, citationsById) {
  if (!found) return '';
  const cites = (found.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  const volumes = (found.appearances || []).map((a) => {
    const lines = (a.entries || []).map((e) => `<li><q>${escapeHtml(e.as_printed)}</q>${
      e.firm ? ` — ${escapeHtml(e.firm)}` : ''}
      <br><span class="res-why">Printed page ${escapeHtml(String(e.printed_page))}, entry ${
        escapeHtml(e.claim_id)}.</span></li>`).join('');
    const holds = (a.holds || []).map((c) => (c === 'occupation' ? 'a trade' : 'a street'));
    return `<dt>Found again in ${escapeHtml(a.title)}</dt>
      <dd>${swatch(null)}<span class="res-chip res-research">${
        escapeHtml(words(a.match_status))}</span>${
        holds.length
          ? `<span class="res-chip res-research">${escapeHtml(String(a.year))} holds ${
              escapeHtml(holds.join(' and '))}${a.parse_carries ? '' : ', and its parse does not cross'}</span>`
          : ''}
        ${lines ? `<ul class="res-candidates">${lines}</ul>` : ''}
        <span class="res-why">${escapeHtml(a.match_rule)}</span></dd>`;
  }).join('');
  return `${volumes}
    <dd><span class="res-why">${escapeHtml(found.standard || '')}</span>
      ${cites.length ? `<ol class="cites">${citationItems(cites)}</ol>` : ''}</dd>`;
}

/**
 * And what the RECORD itself now carries (T-0632). The layer above holds the
 * printed lines and the crosswalks' arithmetic; the household record holds the
 * CLAIM — the later trade and the later address, each graded, dated to the year
 * it describes and citing the volume it was read out of. It is rendered from the
 * record rather than from the layer on purpose: the record is what a reader who
 * opens the JSON sees, and a card showing something its own file does not say
 * would be two answers to one question.
 */
function laterClaimHtml(block, citationsById) {
  if (!block) return '';
  const one = (claim, label) => {
    if (!claim) return '';
    const cites = (claim.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
    return `<dt>${escapeHtml(label)} in ${escapeHtml(String(claim.describes_date))}</dt>
      <dd>${swatch(claim.confidence)}${escapeHtml(claim.value)}
        <br><span class="res-why">${escapeHtml(claim.note)}</span>
        ${cites.length ? `<ol class="cites">${citationItems(cites)}</ol>` : ''}</dd>`;
  };
  return one(block.occupation_later, 'A trade printed against this name')
    + one(block.address_later, 'An address printed against this name')
    + backProjectionHtml(block.back_projection)
    + residenceBackProjectionHtml(block.residence_back_projection, citationsById);
}

/**
 * And what was done with the later address (T-0633), which is the half a reader
 * cannot check from the address alone.
 *
 * `docs/ADDRESS-BACK-PROJECTION.md` is the fourth grammar for placing a business:
 * a street printed four to nine years after the scene, read backwards, carried as
 * the business's street FACE and nothing narrower. Fifteen of the eighty-seven
 * addresses on this layer earn one; the other seventy-two do not.
 *
 * ALL EIGHTY-SEVEN ARE SHOWN, and that is the section rather than a caveat on it.
 * An address the pass declines is a reading it made — the 1835 record prints no
 * trade to position, or the directory prints a home and not a shop, or the street
 * is `Michigan ave` where 1835 has Michigan Street, or `cor. Monroe` puts a grocer
 * three blocks outside the platted town. A card showing only the placements would
 * be reporting this pass's successes and hiding its arithmetic, which is exactly
 * what the crosswalks' three match statuses above already refuse to do.
 *
 * NOTHING IS DRAWN. The face has no geometry, on purpose: dealing a roof to a
 * back-projected address would be two inventions under one chip (L218, and
 * `STREET-FACE-ADOPTION.md` limit 3). This row is where the placement reaches a
 * visitor, the same way the fauna layer reaches one under L2.
 */
function backProjectionHtml(bp) {
  if (!bp) return '';
  const placed = bp.outcome === 'placed';
  const label = {
    placed: 'Positioned by reading that address backwards',
    already_better_placed: 'Not read backwards — something better already places it',
  }[bp.outcome] || 'That address was refused, and here is why';
  const where = placed
    ? `${bp.value} — ${bp.placement === 'face'
      ? 'the street face, and nothing narrower'
      : `${words(bp.placement)} on a crossing at ${
        (bp.position_local_enu_m || []).join(', ')} m in the scene's local frame`}`
    : 'no position taken';
  const carried = bp.read_back_years
    ? `<span class="res-chip res-research">${escapeHtml(String(bp.read_back_years))} years back, from ${
      escapeHtml(String(bp.describes_date))}</span>` : '';
  const clause = bp.clause
    ? `<span class="res-chip res-research">clause ${escapeHtml(String(bp.clause))}</span>` : '';
  // A chip only where there is a claim to grade. A refusal is not a figure held
  // at low confidence; it is the absence of a figure, and the record carries no
  // `confidence` on one for exactly that reason.
  const chip = placed ? swatch(bp.confidence) : '';
  return `<dt>${escapeHtml(label)}</dt>
    <dd>${chip}${escapeHtml(where)}${carried}${clause}
      <br><span class="res-why">${escapeHtml(bp.note)}</span></dd>`;
}

/**
 * And the same question asked about a HOME (T-0669), which is a different question and
 * so gets a different row rather than a wider one.
 *
 * `docs/RESIDENCE-BACK-PROJECTION.md` is L218's mechanism aimed at where a man slept:
 * a street the volume prints as `res` or `bds`, read backwards and carried as the
 * household's street FACE. It departs from the business rule in two places, and both
 * are visible here. A home needs no attested trade — everybody the town holds lived
 * somewhere in it — which is why forty-four of these forty-eight belong to people the
 * 1835 papers give no trade and the business pass refused before it ever asked about
 * their houses. And a home never reaches a POINT, not even where the volume prints a
 * corner: that corner hangs off a street number from a grid 1835 did not have.
 *
 * BOTH ROWS CAN APPEAR ON ONE CARD, and that is deliberate. One printed address can
 * carry two rulings because two policies asked two questions of it, and a card showing
 * only the second would leave a reader wondering what became of the first.
 */
function residenceBackProjectionHtml(rp, citationsById) {
  if (!rp) return '';
  const placed = rp.outcome === 'placed';
  const label = {
    placed: 'That home address was read backwards, and here is what it reaches',
    already_better_placed: 'Not read backwards — something better already houses him',
  }[rp.outcome] || 'That home address was refused, and here is why';
  // `rp.placement` is always `face` and is read rather than assumed: the day this
  // policy grows a second unit, the row says so instead of the prose lying.
  const where = placed
    ? `${rp.value} — the ${words(rp.placement)}, and nothing narrower`
    : 'no position taken';
  const kind = rp.kind
    ? `<span class="res-chip res-research">${escapeHtml(
      rp.kind === 'boards' ? 'printed as a lodging' : 'printed as a residence')}</span>` : '';
  const carried = rp.read_back_years
    ? `<span class="res-chip res-research">${escapeHtml(String(rp.read_back_years))} years back, from ${
      escapeHtml(String(rp.describes_date))}</span>` : '';
  const clause = rp.clause
    ? `<span class="res-chip res-research">clause ${escapeHtml(String(rp.clause))}</span>` : '';
  // A chip only where there is a claim to grade, for the reason the row above gives.
  const chip = placed ? swatch(rp.confidence) : '';
  const cites = (rp.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  return `<dt>${escapeHtml(label)}</dt>
    <dd>${chip}${escapeHtml(where)}${kind}${carried}${clause}
      <br><span class="res-why">${escapeHtml(rp.note)}</span>
      ${cites.length ? `<ol class="cites">${citationItems(cites)}</ol>` : ''}</dd>`;
}

/**
 * THE CONSOLIDATION'S OWN READING, WHICH NOTHING SHOWED (T-0668).
 *
 * `tools/consolidate_resident_evidence.py` reads seven source domains, decides who
 * is who, and grades each person on a ratified ladder. It writes the whole of that
 * work onto the person: the rung it fired (`ladder_rule`), the fact that the person
 * exists in this layer because that consolidation minted them (`civic_mint`), and
 * every appearance it spent — a quoted reading of the name, the list it stands in,
 * where on the page, the record id, the date the line describes and the source.
 *
 * FORTY-FOUR FIGURES ACROSS 531 PEOPLE, and `tools/measure_layer_reads.py` had
 * every one of them banked as reaching nothing. That is the defect T-0491 named on
 * the 1840 bridge, at twenty times the scale: a grade is a VERDICT, the appearances
 * are the argument that produced it, and a verdict shipped without its argument is
 * an assertion. A reader cannot disagree with `attested` unless they can see the
 * rung that awarded it and the lines it was awarded on.
 *
 * THE RUNG'S TEXT COMES FROM THE DATA, not from here. `GRADE_RULES` in the
 * consolidation tool is the ratified ladder and it is Python; this section reads
 * `vocabulary.ladder_rules` out of `data/residents/index.json`, which that tool
 * writes and its gated `--check` holds equal to the constant. Restating a rung in
 * JavaScript would have been two answers to one question, and the one on the card
 * would be the one that drifted.
 *
 * EVERY LINE CARRIES THE DATE IT DESCRIBES, and that is the section rather than a
 * caveat on it. The domains are not contemporaries of each other: the 1833-1835
 * press names a person in this town, the 1844 directory names them nine years
 * after this scene, and the ladder grades those differently on purpose. A block
 * that showed the readings without their dates would flatten the one distinction
 * the whole consolidation is built on.
 */
const EVIDENCE_DOMAINS = [
  ['press_evidence', 'Named by the town\u2019s own newspapers'],
  ['civic_evidence', 'Named on a civic list \u2014 poll, tax or muster'],
  ['church_evidence', 'Named in the parish register'],
  ['book_evidence', 'Named in a directory or a recollection'],
  ['census_evidence', 'Named in a census'],
];

function evidenceLineHtml(entry, citationsById) {
  const cite = citationsById.get(entry.source);
  return `<li><q>${escapeHtml(String(entry.as_read ?? ''))}</q>
    <br><span class="res-why">In <b>${escapeHtml(words(entry.list))}</b>, describing ${
      escapeHtml(printedOn(entry.describes_date))}${
      entry.locator ? `, at ${escapeHtml(String(entry.locator))}` : ''}. Record ${
      escapeHtml(String(entry.record_id))}, accepted by rung ${
      escapeHtml(String(entry.rule))}.</span>
    ${cite ? `<ol class="cites">${citationItems([cite])}</ol>` : ''}</li>`;
}

function evidenceLadderHtml(person, citationsById, ladderRules) {
  const domains = EVIDENCE_DOMAINS
    .map(([key, label]) => [label, (person[key] || []).filter(Boolean)])
    .filter(([, list]) => list.length);
  const bio = person.biographical_evidence || null;
  if (!domains.length && !person.ladder_rule && !bio) return '';

  const rung = person.ladder_rule
    ? (ladderRules || []).find((r) => r.rung === person.ladder_rule) : null;
  const rungRow = person.ladder_rule
    ? `<dt>The rung this person is graded on</dt>
      <dd>${swatch(rung && rung.grade)}<span class="res-chip res-research">${
        escapeHtml(String(person.ladder_rule))}</span>${
        rung ? escapeHtml(rung.rule) : 'The manifest carries no text for this rung.'}
        <br><span class="res-why">The ladder was ratified on 3 September 2026 and every
          person it reaches is graded by ONE of its rungs, named here. ${
        person.civic_mint
          ? 'This person is in the town because that consolidation minted them: they were '
            + 'read out of the lists below and matched to nobody the project already carried.'
          : 'This person was already in the town; the consolidation graded them rather than '
            + 'minted them.'}</span></dd>`
    : '';

  const evidence = domains.map(([label, list]) => `<dt>${escapeHtml(label)}</dt>
    <dd>${swatch(null)}<span class="res-chip res-research">${list.length} ${
      list.length === 1 ? 'appearance' : 'appearances'}</span>
      <ul class="res-candidates">${
        list.map((e) => evidenceLineHtml(e, citationsById)).join('')}</ul></dd>`).join('');

  const age = bio && bio.age_on_1835_07_01;
  const ageValue = age && age.value && Number.isFinite(age.value.min)
    ? (age.value.min === age.value.max
      ? `${age.value.min}`
      : `between ${age.value.min} and ${age.value.max}`)
    : null;
  const biography = bio
    ? claimRow('Born', bio.birth_year && bio.birth_year.value, bio.birth_year, citationsById)
      + claimRow('Age on 1 July 1835', ageValue, age, citationsById)
    : '';

  return `${rungRow}${evidence}${biography}${
    evidence
      ? `<dd><span class="res-why">Each line above is an APPEARANCE — somebody wrote this
        name down, on that date, in that place. It is evidence about this person and it is
        not an 1835 fact: a directory line of 1844 says the person was in Chicago in 1844,
        and the rung above says what this project was willing to conclude from the set of
        them together.</span></dd>` : ''}`;
}

export function personHtml(person, citationsById, researchByPerson, directoryByPerson,
  directoriesOnRecord, ladderRules) {
  const occ = person.occupation || {};
  const cites = (person.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  const occCites = (occ.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
  const born = person.birth_year || null;
  const aged = person.age_on_scene_date || null;
  const named = person.name_basis || null;
  return `<details class="lib res-person">
    <summary><span class="lib-title">${swatch(person.grade)}${escapeHtml(person.name || 'unnamed')}</span>
      <span class="res-role">${escapeHtml(words(person.relationship))}${
        occ.value ? ` · ${escapeHtml(words(occ.value))}` : ''}</span></summary>
    <dl class="lib-body">
      ${row('In the household as', words(person.relationship))}
      ${row('Sex', words(person.sex))}
      ${claimRow('Age on 1 July 1835', aged && aged.value, aged, citationsById)}
      ${claimRow('Born', born && born.value, born, citationsById)}
      ${occ.value ? `<dt>Occupation</dt><dd>${swatch(occ.confidence)}${escapeHtml(words(occ.value))}${
        occ.note ? `<br><span class="res-why">${escapeHtml(occ.note)}</span>` : ''}${
        occCites.length ? `<ol class="cites">${citationItems(occCites)}</ol>` : ''}</dd>` : ''}
      ${claimRow('How this person is named', named && named.value, named, citationsById)}
      ${person.letter_list_only
        ? `<dt>How this person is known</dt><dd>${swatch('attested')}Only from the post office's lists of uncalled-for letters. A name on one of those lists is somebody a correspondent believed was reachable at Chicago; it gives no trade, no street and no household, and it is the weakest evidence this project accepts for a resident. A shopkeeper who advertised his stock is a different claim, and this row is here so the two never read as the same one.</dd>` : ''}
      ${person.letter_list_only && (person.letter_list_returns || []).length
        ? `<dt>The post office was holding a letter on</dt><dd>${swatch('attested')}${
          (person.letter_list_returns || []).map((d) => escapeHtml(printedOn(d))).join(' · ')
        }<br><span class="res-why">Each date is a separate return of uncalled-for letters
          carrying this name — not a reprint of one. It is the sharpest thing this record
          can be dated by: a letter waiting on 1 July 1835 is the day this scene is set,
          and one waiting eighteen months earlier is a different claim about the same
          person.</span></dd>` : ''}
      ${person.note ? `<dt>What the sources say</dt><dd>${escapeHtml(person.note)}</dd>` : ''}
      ${evidenceLadderHtml(person, citationsById, ladderRules)}
      ${researchHtml(researchByPerson.get(person.id), citationsById)}
      ${laterCensusHtml(person.later_census, citationsById)}
      ${laterDirectoryHtml(directoryByPerson.get(person.id), citationsById)}
      ${laterClaimHtml((directoriesOnRecord || []).find((row) => row.person_id === person.id), citationsById)}
      ${cites.length ? `<dt>Sources</dt><dd><ol class="cites">${citationItems(cites)}</ol></dd>` : ''}
    </dl>
  </details>`;
}

/** The grade tally a manifest entry already carries, as chips. */
function gradeChips(grades) {
  return ['attested', 'inferred', 'reconstructed']
    .filter((g) => (grades || {})[g])
    .map((g) => `<span class="res-chip">${swatch(g)}${grades[g]} ${escapeHtml(g)}</span>`)
    .join('');
}

/**
 * One household, closed. The summary is the manifest's denormalised copy; the
 * body arrives on first open, from the record itself, which is authoritative.
 *
 * `data-file` and `data-loaded` are how the lazy read is driven, and `data-reach`
 * is the finding: a household with neither residence nor workplace attested
 * reaches no building sidecar, so before this section it appeared nowhere a
 * visitor could go.
 */
function householdSummary(entry, { orphanChip = true } = {}) {
  const reaches = Boolean(entry.lives_at || entry.works_at);
  const label = entry.id.replace(/^hh_/, '').replace(/_/g, ' ');
  return `<details class="lib res-hh" data-file="${escapeHtml(entry.file)}"
      data-id="${escapeHtml(entry.id)}" data-loaded="0"
      data-reach="${reaches ? 'building' : 'nowhere'}">
    <summary><span class="lib-title">${escapeHtml(label)}</span>
      <span class="res-role">${escapeHtml(words(entry.division))} division · ${
        entry.persons} ${entry.persons === 1 ? 'person' : 'people'}</span>
      <span class="res-chips">${gradeChips(entry.grades)}${
        entry.civic_mint
          ? '<span class="res-chip res-research">minted by the evidence consolidation</span>' : ''}${
        entry.census_1840_linked
          ? `<span class="res-chip res-research">${entry.census_1840_linked} bridged to an 1840 census household</span>` : ''}${
        reaches || !orphanChip
          ? '' : '<span class="res-chip res-orphan">on no building card</span>'}</span></summary>
    <div class="lib-body res-hh-body"><p class="legend-note">Loading…</p></div>
  </details>`;
}

/** The household record itself, rendered into an opened row. */
export function householdHtml(hh, citationsById, researchByPerson, directoryByPerson, ladderRules) {
  // T-0632's block on the record: `directories.note` states what a later volume is
  // worth and `directories.sources` names every one that met this household.
  const onRecord = hh.directories || {};
  const persons = Array.isArray(hh.persons) ? hh.persons : [];
  const party = hh.party_size_on_arrival || null;
  return `<dl class="lib-body res-fields">
      ${claimRow('Came to Chicago', (hh.arrival || {}).value, hh.arrival, citationsById)}
      ${row('How exact that year is', words((hh.arrival || {}).precision))}
      ${claimRow('In a party of', party && party.value, party, citationsById)}
      ${claimRow('Came from', (hh.origin || {}).value, hh.origin, citationsById)}
      ${claimRow('Why they came', (hh.reason_for_coming || {}).value,
        hh.reason_for_coming, citationsById)}
      ${claimRow('Lived at', (hh.lives_at || {}).value, hh.lives_at, citationsById)}
      ${claimRow('Worked at', (hh.works_at || {}).value, hh.works_at, citationsById)}
      ${claimRow('Here on 1 July 1835', (hh.present_on_scene_date || {}).value,
        hh.present_on_scene_date, citationsById)}
      ${kinRows(hh, citationsById)}
      ${hh.touches_removal
        ? `<dt>Touches the removal of 1835</dt><dd>Yes — read the standing constraint in
           <code>AGENTS.md</code>. This record is published as research; nothing about the
           removal is depicted or staged in the scene.</dd>` : ''}
      ${hh.research_note
        ? `<dt>What this record is worth</dt><dd>${escapeHtml(hh.research_note)}</dd>` : ''}
    </dl>
    ${onRecord.note ? `<p class="res-why">${escapeHtml(onRecord.note)} Volumes cited on this record: ${
        escapeHtml((onRecord.sources || []).join(', '))}.</p>` : ''}
    <div class="res-people">${persons.map((p) => personHtml(p, citationsById, researchByPerson, directoryByPerson, onRecord.people, ladderRules)).join('')}</div>`;
}

/**
 * The researched-and-not-resident list — the exclusions-style half.
 *
 * Its own manifest doc calls it "as load-bearing as the households" and it
 * reached nobody at all: three kinds of finding, ten people, including one this
 * project believes was here and cannot cite, *"recorded so that the gap is
 * visible rather than quietly filled."* That is this project's whole argument
 * about evidence, and it was in a file nothing opened.
 */
function notResidentHtml(entries, citationsById) {
  const body = entries.map((e) => {
    const cites = (e.sources || []).map((id) => citationsById.get(id)).filter(Boolean);
    return `<details class="lib res-nr">
      <summary><span class="lib-title">${escapeHtml(e.name || e.id)}</span>
        <span class="res-role">${escapeHtml(words(e.category))}</span></summary>
      <dl class="lib-body">
        ${row('Why not a household here', e.reason)}
        ${e.note ? `<dt>The reasoning</dt><dd>${escapeHtml(e.note)}</dd>` : ''}
        ${cites.length ? `<dt>Sources</dt><dd><ol class="cites">${citationItems(cites)}</ol></dd>` : ''}
      </dl>
    </details>`;
  }).join('');
  return `<details class="lib res-nr-group">
    <summary><span class="lib-title">Researched, and not a resident of this town</span>
      <span class="res-role">${entries.length} people</span></summary>
    <div class="lib-body">
      <p class="legend-note">Three different findings share this list: someone who arrived
        after 1 July 1835, someone the sources place at Chicago but not as a household of it,
        and someone this project believes was here and <b>cannot cite</b>. The third kind is
        recorded so the gap stays visible instead of being quietly filled, which is the same
        rule the excluded buildings follow.</p>
      ${body}
    </div>
  </details>`;
}

/**
 * The letter-list cohort, held together in one group (T-0379).
 *
 * The owner ruled on 30 August 2026 that every name the post office's lists of
 * uncalled-for letters yields, and the mint's refusals admit, joins the town. That
 * took it from a couple of hundred people to most of a thousand and made roughly
 * three quarters of them a name on a list and nothing else — which is a change to
 * what a visitor is looking at, not only to what the data holds, and the ruling
 * said so in as many words: *if that reads as a wall of undifferentiated people,
 * the ruling has been implemented badly, not chosen badly.*
 *
 * So they do not sit interleaved with the town's evidenced households. They are one
 * closed disclosure that says what they are and how many, and the list above it is
 * the town as the rest of the corpus documents it — the same records, in the same
 * order, at the same length it was before the ruling. Opening this group is a
 * deliberate act, and the rows inside it behave exactly like every other row.
 *
 * The `on no building card` chip is dropped inside here on purpose. On an evidenced
 * household it is a FINDING — a record this project could not attach to a building.
 * On 727 rows that by construction have no address it is wallpaper, and the group's
 * own summary says the same thing once, where it means something.
 */
function letterListGroupHtml(entries, persons) {
  if (!entries.length) return '';
  const share = persons ? Math.round((entries.length / persons) * 100) : 0;
  return `<details class="lib res-ll-group">
    <summary><span class="lib-title">Known only from the post office's letter lists</span>
      <span class="res-role">${entries.length} ${entries.length === 1 ? 'person' : 'people'}
        · about ${share}% of this town</span></summary>
    <div class="lib-body">
      <p class="legend-note">Each of these is a name the Chicago post office printed in a
        list of letters nobody had called for. That establishes one thing: a correspondent
        believed a person of that name was reachable at Chicago on that date. It does
        <b>not</b> establish that they lived here, kept a trade here, or were here on
        1 July 1835 — and the office served the country around the town as well as the town.
        It is the weakest evidence this project accepts for a resident, and it is admitted
        by an owner's ruling of 30 August 2026 rather than by the sources getting better.
        Every row carries the date of the return that printed it; none of them has a
        building, a household or a trade, because a letter list gives none.</p>
      ${entries.map((entry) => householdSummary(entry, { orphanChip: false })).join('')}
    </div>
  </details>`;
}

/** The manifest's closed sets, shown rather than paraphrased. */
function vocabularyHtml(vocab) {
  const sets = [
    ['How much of a person is reconstructed', vocab.grades],
    ['Here on the scene date', vocab.presence],
    ['Divisions of the town', vocab.divisions],
    ['How exact an arrival year is', vocab.arrival_precision],
    ['Places in a household', vocab.relationships],
    // T-0597. A place in a household and a tie between two households are
    // different questions, so they are two sets: `relationships` stops at the
    // household's edge and `kin_relations` is what may cross it. Shown for the
    // same reason every other set here is — the degrees are the point, and a
    // reader who cannot see that `half_brother` and `brother` are both in the
    // set cannot see that the dataset keeps them apart.
    ['Ties between two households', vocab.kin_relations],
    // Shown because `sex` is shown. The census of T-0021 found this set reaching
    // nothing while the value it governs was on every person's card — five closed
    // sets listed and the sixth withheld, which reads as a set the dataset does
    // not have rather than one nobody printed.
    ['Sex, as the records give it', vocab.sexes],
    ['Trades', vocab.occupations],
  ];
  const rows = sets
    .filter(([, list]) => Array.isArray(list) && list.length)
    .map(([label, list]) => `<dt>${escapeHtml(label)}</dt>
      <dd>${list.map((v) => `<code>${escapeHtml(words(v))}</code>`).join(' · ')}</dd>`)
    .join('');
  return `<details class="lib res-vocab">
    <summary><span class="lib-title">The words on these cards, and they are a closed set</span></summary>
    <dl class="lib-body">
      <p class="legend-note">Two of these are different questions and the dataset refuses to
        merge them. <b>How much of a person is reconstructed</b> grades the PERSON; the
        swatch beside any single figure grades that one attribute's evidence. A documented
        man can have a conjectural arrival year, and this town has several.</p>
      ${rows}
    </dl>
  </details>`;
}

/**
 * Fetch the residents layer and render it into `mount`.
 *
 * Failure is reported, never papered over, the same way the liberties, the
 * exclusions and the wildlife do it: a missing manifest leaves a line saying so
 * and pushes the reason onto the loader's shared problem list, and a household
 * whose own file 404s says so inside its own row rather than taking the section
 * down.
 *
 * @param {object} o
 * @param {HTMLElement|null} o.mount        where the households go
 * @param {HTMLElement|null} [o.noteMount]  where the count sentence goes
 * @param {string} o.sceneId                which scene's citation join to read
 * @param {URL} o.dataBase                  where data/ lives
 * @param {string[]} [o.problems]           the shared collector
 */
export async function mountResidents({ mount, noteMount = null, sceneId, dataBase, problems = [] }) {
  const fail = (message) => {
    problems.push(`residents: ${message} — the town's people are not shown`);
    if (mount) {
      mount.innerHTML = '<p class="legend-note">The household records could not be loaded. '
        + 'They are committed at <code>data/residents/</code>.</p>';
      mount.removeAttribute('aria-busy');
    }
    if (noteMount) {
      noteMount.textContent = '';
      noteMount.removeAttribute('aria-busy');
    }
    return { households: 0, persons: 0, offCard: 0, error: message };
  };

  const getJson = async (rel) => {
    const res = await fetch(new URL(rel, dataBase), { cache: 'no-cache' });
    if (!res.ok) throw new Error(`${rel}: ${res.status} ${res.statusText}`);
    return res.json();
  };

  let index;
  try {
    index = await getJson('residents/index.json');
  } catch (err) {
    return fail(String(err.message || err));
  }

  // The citation join. Its absence degrades the section to bare notes rather
  // than taking it down: a card without its sources is poorer, not wrong.
  const citationsById = new Map();
  try {
    const joined = await getJson(`sidecars/${sceneId}/residents_sources.json`);
    for (const [id, record] of Object.entries(joined.citations || {})) {
      citationsById.set(id, record);
    }
  } catch (err) {
    problems.push(`residents: ${err.message} — the household records are shown without their citations`);
  }

  // The deliberately separate review layer. A possible identity must not
  // become an asserted household fact merely because its biography is useful.
  const researchByPerson = new Map();
  let researchCounts = {};
  let researchEligible = 0;
  try {
    const pilot = await getJson('residents/research_pilot.json');
    researchCounts = pilot.counts || {};
    researchEligible = pilot.eligible_real_named_people || 0;
    for (const review of pilot.reviews || []) researchByPerson.set(review.person_id, review);
  } catch (err) {
    problems.push(`residents: ${err.message} — resident research reviews are not shown`);
  }

  // The four directory crosswalks, joined on person_id (T-0632, replacing T-0569's
  // 1844-only layer). Beside the records as well as on them: the record carries the
  // later trade and street and cites the volume, and this layer carries the printed
  // lines, the match rule and the arithmetic the card has no room for. Its absence
  // costs the section this block and nothing else.
  const directoryByPerson = new Map();
  let directoryCounts = {};
  let directoryVolumes = [];
  try {
    const found = await getJson('residents/directories.json');
    directoryCounts = found.counts || {};
    directoryVolumes = found.volumes || [];
    for (const row of found.people || []) {
      directoryByPerson.set(row.person_id, { ...row, standard: found.standard });
    }
  } catch (err) {
    problems.push(`residents: ${err.message} — the directory findings are not shown`);
  }

  const vocab = index.vocabulary || {};
  const entries = Array.isArray(index.households) ? [...index.households] : [];
  if (!entries.length) return fail('the manifest lists no household');
  entries.sort((a, b) => rank(vocab.divisions, a.division) - rank(vocab.divisions, b.division)
    || String(a.id).localeCompare(String(b.id)));

  const notResident = Array.isArray(index.researched_not_resident)
    ? index.researched_not_resident : [];
  const counts = index.counts || {};
  const persons = counts.persons ?? entries.reduce((n, e) => n + (e.persons || 0), 0);
  const offCard = entries.filter((e) => !e.lives_at && !e.works_at).length;
  const offCardPersons = entries
    .filter((e) => !e.lives_at && !e.works_at)
    .reduce((n, e) => n + (e.persons || 0), 0);
  // T-0379. The manifest says which rows are the letter-list cohort, so the split
  // is read from the data rather than from a mint tool's id prefix — and it is a
  // split rather than a sort because after the ruling those rows outnumber the
  // town's evidenced households roughly three to one.
  const letterList = entries.filter((e) => e.letter_list_only);
  const evidenced = entries.filter((e) => !e.letter_list_only);
  const letterListOffCard = letterList.filter((e) => !e.lives_at && !e.works_at).length;

  if (noteMount) {
    // The layer's own grade tally, which the manifest has always carried and
    // nothing read (T-0021). "Every one of them graded" was true and told a
    // visitor nothing: the shape of this dataset is that most of its people are
    // hypotheses, and a sentence that does not say so is the wrong sentence.
    const byGrade = counts.by_grade || {};
    noteMount.textContent = `${entries.length} households and ${persons} people — `
      + `${byGrade.attested} named by a source, ${byGrade.inferred} real people whose `
      + `details are partly reconstructed, and ${byGrade.reconstructed} hypothesised to `
      + `fill a demonstrable need of the town. `
      + `${offCard} of the households are attached to no building in this scene — neither `
      + `where they lived nor where they worked is attested on 1 July 1835 — so ${offCardPersons} `
      + `people reached no card anywhere until this section existed. `
      + (counts.letter_list_only
        ? `${counts.letter_list_only} of the people here are known ONLY from the post `
          + `office's lists of uncalled-for letters, which is the weakest evidence this `
          + `layer carries and is marked as such on each of their cards. That is about `
          + `${Math.round((counts.letter_list_only / persons) * 100)} per cent of this `
          + `town: the owner ruled on 30 August 2026 that every such name the evidence `
          + `admits should be held, so they are listed together, below the households the `
          + `rest of the corpus documents, and which of these people are a name and `
          + `nothing else can be seen without opening anything. ` : '')
      + (counts.census_1840_linked
        // T-0491. Three people carry an identity bridge to a named head of household
        // in the 1840 census, and the bridge is an argument rather than a fact: it is
        // shown whole on the person's card, three confidences and all. The count is
        // here so that a reader can see how few of them there are before opening one.
        ? `${counts.census_1840_linked} of these people are bridged to a named household `
          + `in the 1840 census, five years after this scene — later evidence, shown with `
          + `its reasoning and never read back onto 1835. ` : '')
      + (counts.civic_mint
        // T-0668. The consolidation of 3 September 2026 read seven source domains and
        // minted this many of the people below — they are here because a list the town
        // made of its own inhabitants names them, and nothing the project already
        // carried matched. The number is here so a reader can see how much of this
        // town is that one pass before opening a single card.
        ? `${counts.civic_mint} of these people were minted by the evidence `
          + `consolidation, which graded every one of them on a named rung of a ratified `
          + `ladder and wrote the appearances it spent onto their cards — the quoted `
          + `reading, the list, the page and the date each line describes. `
          + `That is ${Math.round((counts.civic_mint / persons) * 100)} per cent of the `
          + `people here, and the rung and its lines are on each of their cards so that `
          + `the grade can be disagreed with rather than taken. ` : '')
      + (researchByPerson.size
        ? `${researchByPerson.size} real named people (${Math.round((researchByPerson.size / researchEligible) * 100)}% of the eligible research population) received a dated identity review: `
          + `${researchCounts.corroborated_enrichment || 0} corroborated findings, `
          + `${researchCounts.candidate_identity || 0} candidate identities kept unmerged, and `
          + `${researchCounts.no_corroboration || 0} searches with no safe match. ` : '')
      + (directoryByPerson.size
        // T-0632. The earliest Chicago directory is of 1839 and this town is of 1835,
        // so the sentence leads with the gap rather than with the number: what these
        // people gain is corroboration, a line to read and — where the volume prints
        // one — a trade or a street OF ITS OWN YEAR, never a date, a trade or a street
        // in 1835.
        ? `${directoryByPerson.size} of them are met by a name in one of the `
          + `${directoryVolumes.length} Chicago directories read here, of 1839, 1843 and `
          + `1844 — ${directoryCounts.people_met_by_more_than_one_volume || 0} in more `
          + `than one. ${directoryCounts.carrying_an_occupation || 0} carry a trade the `
          + `1835 record never had and ${directoryCounts.carrying_an_address || 0} an `
          + `address, each written as its own year's and read back onto nobody; `
          + `${directoryCounts.line_held_but_parse_refused || 0} hold only a line whose `
          + `parse this project will not cross. ` : '')
      + `Nobody is drawn: this is the research, not a population.`;
    noteMount.removeAttribute('aria-busy');
  }

  if (mount) {
    mount.innerHTML = vocabularyHtml(vocab)
      + notResidentHtml(notResident, citationsById)
      + evidenced.map((entry) => householdSummary(entry)).join('')
      + letterListGroupHtml(letterList, persons);
    mount.removeAttribute('aria-busy');

    // The lazy read. A row's body arrives the first time it is opened, from the
    // household record rather than from the manifest's summary of it — the
    // manifest is denormalised for the list and the record is authoritative for
    // everything else.
    mount.addEventListener('toggle', async (event) => {
      const el = event.target;
      if (!(el instanceof HTMLElement) || !el.classList.contains('res-hh')) return;
      if (!el.open || el.dataset.loaded === '1') return;
      el.dataset.loaded = '1';
      const body = el.querySelector('.res-hh-body');
      try {
        const hh = await getJson(`residents/${el.dataset.file}`);
        if (body) body.innerHTML = householdHtml(hh, citationsById, researchByPerson, directoryByPerson,
          vocab.ladder_rules);
      } catch (err) {
        el.dataset.loaded = '0';
        problems.push(`residents: ${err.message} — one household record is missing`);
        if (body) {
          body.innerHTML = `<p class="legend-note">This household's record could not be
            loaded. It is committed at <code>data/residents/${escapeHtml(el.dataset.file || '')}</code>.</p>`;
        }
      }
    }, true);
  }

  return {
    households: entries.length,
    persons,
    offCard,
    offCardPersons,
    // T-0379's two halves, separately, because the interesting assertion is not
    // the total: it is that the town's evidenced households did not move when
    // seven hundred letter-list names joined it, and that the cohort is held
    // apart where a visitor can see it.
    evidenced: evidenced.length,
    letterList: letterList.length,
    letterListOffCard,
    notResident: notResident.length,
    researchReviewed: researchByPerson.size,
    researchCounts,
    error: null,
  };
}

/**
 * The joins a household card needs, loaded once for a caller that is not this
 * section (the People directory, `people.js`).
 *
 * `mountResidents` above fetches the citation join, the identity reviews and the
 * directory crosswalks and keeps them in its own closure, because until the
 * directory existed it was the only thing that rendered a household record. The
 * directory renders the same record with the same `householdHtml`, and a card
 * that quoted a bare source id because its caller skipped the join would be the
 * defect `compile_residents_sources` exists to prevent. So the four reads are
 * repeated here as ONE function returning the shapes `householdHtml` takes, and
 * cached per scene so the two sections opening the same town cost one set of
 * fetches between them. `mountResidents` is left as it was — the read census in
 * `tools/measure_layer_reads.py` scans this file's text — and a failure here
 * degrades exactly the way it does there: a missing join is reported and the
 * card renders without that block, never not at all.
 *
 * @param {URL} dataBase   where data/ lives
 * @param {string} sceneId which scene's citation join to read
 * @param {string[]} [problems] the shared collector
 * @returns {Promise<{citationsById: Map, researchByPerson: Map, directoryByPerson: Map,
 *   ladderRules: object[], getJson: (rel: string) => Promise<any>}>}
 */
const residentJoinCache = new Map();
export function loadResidentJoins(dataBase, sceneId, problems = []) {
  const key = `${sceneId}@${String(dataBase)}`;
  if (residentJoinCache.has(key)) return residentJoinCache.get(key);
  const getJson = async (rel) => {
    const res = await fetch(new URL(rel, dataBase), { cache: 'no-cache' });
    if (!res.ok) throw new Error(`${rel}: ${res.status} ${res.statusText}`);
    return res.json();
  };
  const promise = (async () => {
    const citationsById = new Map();
    const researchByPerson = new Map();
    const directoryByPerson = new Map();
    let ladderRules = [];
    const [joined, pilot, found, index] = await Promise.all([
      getJson(`sidecars/${sceneId}/residents_sources.json`).catch((err) => {
        problems.push(`people: ${err.message} — person cards are shown without their citations`);
        return null;
      }),
      getJson('residents/research_pilot.json').catch((err) => {
        problems.push(`people: ${err.message} — resident research reviews are not shown on person cards`);
        return null;
      }),
      getJson('residents/directories.json').catch((err) => {
        problems.push(`people: ${err.message} — the directory findings are not shown on person cards`);
        return null;
      }),
      getJson('residents/index.json').catch((err) => {
        problems.push(`people: ${err.message} — the grading ladder's text is not shown on person cards`);
        return null;
      }),
    ]);
    for (const [id, record] of Object.entries(joined?.citations || {})) citationsById.set(id, record);
    for (const review of pilot?.reviews || []) researchByPerson.set(review.person_id, review);
    for (const row of found?.people || []) {
      directoryByPerson.set(row.person_id, { ...row, standard: found.standard });
    }
    ladderRules = index?.vocabulary?.ladder_rules || [];
    return { citationsById, researchByPerson, directoryByPerson, ladderRules, getJson };
  })();
  residentJoinCache.set(key, promise);
  return promise;
}
