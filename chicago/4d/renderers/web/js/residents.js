/**
 * residents.js — the town's people, in the Evidence panel.
 *
 * ROADMAP K52, from K51. `data/residents/` holds 173 households and 209 person
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
 * WHAT THIS IS NOT. It is a card, not a crowd. Nothing here is drawn: L1 and
 * AGENTS.md stand, v1 ships no human figures, and the standing constraint on
 * depicting the Potawatomi in the year of the removal is untouched by a section
 * that publishes what the sources say and nothing else.
 *
 * ONE FETCH, THEN ONE PER HOUSEHOLD A VISITOR OPENS. The manifest is a
 * denormalised summary of all 173 records — `tools/validate.py` fails the build
 * when a copy disagrees with its record — so the list renders from a single
 * file, and the full record is fetched the first time its own row is opened.
 * 173 fetches on mount to show 173 collapsed summaries would be a worse card and
 * a slower one; the summary is the manifest's job and the manifest says so.
 */

import { citationItems, escapeHtml } from './citations.js';

/** A closed-set token as a reader should see it: `tavern_keeper`. */
function words(token) {
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
function swatch(level) {
  const cls = { attested: 'sw-doc', inferred: 'sw-inf' }[level] || 'sw-rec';
  return `<i class="sw ${cls}" title="${escapeHtml(level || 'reconstructed')}"></i>`;
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
function personHtml(person, citationsById) {
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
      ${person.note ? `<dt>What the sources say</dt><dd>${escapeHtml(person.note)}</dd>` : ''}
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
function householdSummary(entry) {
  const reaches = Boolean(entry.lives_at || entry.works_at);
  const label = entry.id.replace(/^hh_/, '').replace(/_/g, ' ');
  return `<details class="lib res-hh" data-file="${escapeHtml(entry.file)}"
      data-id="${escapeHtml(entry.id)}" data-loaded="0"
      data-reach="${reaches ? 'building' : 'nowhere'}">
    <summary><span class="lib-title">${escapeHtml(label)}</span>
      <span class="res-role">${escapeHtml(words(entry.division))} division · ${
        entry.persons} ${entry.persons === 1 ? 'person' : 'people'}</span>
      <span class="res-chips">${gradeChips(entry.grades)}${
        reaches ? '' : '<span class="res-chip res-orphan">on no building card</span>'}</span></summary>
    <div class="lib-body res-hh-body"><p class="legend-note">Loading…</p></div>
  </details>`;
}

/** The household record itself, rendered into an opened row. */
function householdHtml(hh, citationsById) {
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
      ${hh.touches_removal
        ? `<dt>Touches the removal of 1835</dt><dd>Yes — read the standing constraint in
           <code>AGENTS.md</code>. This record is published as research; nothing about the
           removal is depicted or staged in the scene.</dd>` : ''}
      ${hh.research_note
        ? `<dt>What this record is worth</dt><dd>${escapeHtml(hh.research_note)}</dd>` : ''}
    </dl>
    <div class="res-people">${persons.map((p) => personHtml(p, citationsById)).join('')}</div>`;
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

/** The manifest's closed sets, shown rather than paraphrased. */
function vocabularyHtml(vocab) {
  const sets = [
    ['How much of a person is reconstructed', vocab.grades],
    ['Here on the scene date', vocab.presence],
    ['Divisions of the town', vocab.divisions],
    ['How exact an arrival year is', vocab.arrival_precision],
    ['Places in a household', vocab.relationships],
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
      + `people reached no card anywhere until this section existed. Nobody is drawn: this `
      + `is the research, not a population.`;
    noteMount.removeAttribute('aria-busy');
  }

  if (mount) {
    mount.innerHTML = vocabularyHtml(vocab)
      + notResidentHtml(notResident, citationsById)
      + entries.map((entry) => householdSummary(entry)).join('');
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
        if (body) body.innerHTML = householdHtml(hh, citationsById);
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
    notResident: notResident.length,
    error: null,
  };
}
