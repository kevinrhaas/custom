import { CONFIG } from '../js/config.js';
import { loadLibrary } from '../js/library.js';
import { uniqueLabels, validateMetadata } from '../js/metadata.js';
import { reconcileApproved } from './tagging-state.js';

const ROOT = new URL('../', import.meta.url);
const MAX_IMPORT = 5 * 1024 * 1024;
const empty = () => ({ version: 1, photos: Object.create(null) });
const copy = (value) => ({ version: 1, photos: Object.assign(Object.create(null), JSON.parse(JSON.stringify(value.photos))) });
const count = (value) => Object.keys(value.photos).length;

// The only published artifact is tags.json. Drafts, image files and face
// descriptors never enter it. Importing a suggestion cannot approve it.
export async function mountTagging(container) {
  let disposed = false;
  let faces;
  let currentId = '';
  const storageKey = `${CONFIG.access?.prefix || 'memories'}.tagging.v1.${CONFIG.source === 'drive' ? CONFIG.drive?.folderId : 'manifest'}`;
  container.innerHTML = `
    <p>Help the family find a horse, a place, or someone they love. Review each photo before saving its additions.</p>
    <p class="adm-muted adm-small">Drafts and approvals are saved on this browser. Nothing is sent to the album until the approved file is published.</p>
    <p class="adm-muted" data-tag-status role="status" aria-live="polite">Loading the album…</p>
    <p class="adm-error" data-tag-storage-warning role="alert"></p>
    <div data-tag-controls hidden>
      <details class="tag-help">
        <summary>Get suggestions or restore your work</summary>
        <p>AI suggestions come from the local tagging tool. It uses Claude only when you connect an API key on your computer. Never paste that key into this page.</p>
        <button class="adm-btn" type="button" data-tag-ai-list>Download AI photo list</button>
        <p class="adm-small">Put the photo list beside downloaded originals, keeping their file names. With your key set locally, run <code>node memories/tools/tag-photos.mjs --input /path/photo-list.json --out /path/album.drafts.json</code>, then open the draft JSON below. Use JPG or PNG scans up to 5 MB and 8000 pixels per side. Suggested captions can be wrong; check them against what your family knows.</p>
        <label class="adm-label" for="tagDraftFile">Import AI draft suggestions</label>
        <input class="adm-field tag-file" id="tagDraftFile" type="file" accept=".json,application/json">
        <label class="adm-label" for="tagApprovedFile">Restore an approved tags.json file</label>
        <input class="adm-field tag-file" id="tagApprovedFile" type="file" accept=".json,application/json">
        <p class="adm-small adm-muted">Restore merges previously approved additions. AI drafts always need individual approval.</p>
      </details>
      <label class="adm-label" for="tagFilter">Find a photo to tag</label>
      <input class="adm-field" id="tagFilter" type="search" placeholder="Title, year, or file name">
      <label class="adm-label" for="tagPhoto">Photo</label>
      <select class="adm-field" id="tagPhoto"></select>
      <div data-tag-editor>
        <figure class="tag-preview"><img data-tag-image alt=""><figcaption data-tag-source></figcaption></figure>
        <p class="adm-muted adm-small" data-tag-original></p>
        <form data-tag-form>
          <label class="adm-label" for="tagLabels">Additional tags</label>
          <input class="adm-field" id="tagLabels" type="text" placeholder="horse, county fair, Ferris wheel">
          <label class="adm-label" for="tagPeople">Additional people</label>
          <input class="adm-field" id="tagPeople" type="text" placeholder="June, Uncle Frank">
          <p class="adm-small adm-muted">Separate tags and names with commas. These add to the names and tags already in the photo’s description.</p>
          <label class="tag-check"><input id="tagReplaceCaption" type="checkbox"> Use a reviewed caption instead of the original</label>
          <p class="adm-small adm-muted">Replacing a caption can change which names search finds. Names from the original caption are added to People for you to check; remove any that are wrong.</p>
          <label class="adm-label" for="tagCaption">Reviewed caption</label>
          <textarea class="adm-field" id="tagCaption" rows="4" disabled></textarea>
          <p class="adm-small" data-tag-review-state></p>
          <div class="adm-actions">
            <button class="adm-btn adm-primary" type="submit">Approve this photo</button>
            <button class="adm-btn" type="button" data-tag-next>Next photo</button>
            <button class="adm-btn adm-quiet" type="button" data-tag-reset>Discard this draft</button>
            <button class="adm-btn adm-quiet" type="button" data-tag-remove>Remove approved additions</button>
          </div>
        </form>
      </div>
      <details class="tag-help" data-tag-faces>
        <summary>Find people in local scans</summary>
        <div data-tag-face-tool></div>
      </details>
      <div class="tag-export">
        <h3>Save the approved additions</h3>
        <p data-tag-count></p>
        <button class="adm-btn adm-primary" type="button" data-tag-export>Download approved tags.json</button>
        <p class="adm-small adm-muted">Give this file to the person maintaining the album. Replace <code>site/memories/data/tags.json</code> with it and publish the site. Draft suggestions are excluded.</p>
        <button class="adm-btn adm-quiet" type="button" data-tag-clear>Clear tagging data on this browser</button>
      </div>
    </div>`;
  const $ = (selector) => container.querySelector(selector);
  const status = (text, error = false) => {
    if (disposed) return;
    $('[data-tag-status]').textContent = text;
    $('[data-tag-status]').className = error ? 'adm-error' : 'adm-muted';
  };
  let approved = empty();
  let drafts = empty();
  let published = empty();
  let savedWarning = '';
  const conflicts = new Set();
  let photos;
  try {
    const config = { ...CONFIG, metadataUrl: false,
      manifestUrl: new URL(CONFIG.manifestUrl || 'data/library.json', ROOT).href };
    const library = await loadLibrary(config);
    photos = library.photos;
    if (!photos.length) throw new Error('Add photos to the album before tagging them.');
    if (CONFIG.metadataUrl !== false && CONFIG.metadataUrl !== null) {
      const response = await fetch(new URL(CONFIG.metadataUrl || 'data/tags.json', ROOT), { cache: 'no-store' });
      if (response.ok) published = copy(validateMetadata(await response.json()));
      else if (response.status !== 404) throw new Error('The approved tags could not be loaded. Try again before making changes.');
    }
    approved = copy(published);
    let saved;
    try { saved = localStorage.getItem(storageKey); } catch {}
    if (saved) {
      try {
        const state = JSON.parse(saved);
        drafts = copy(validateMetadata(state.drafts));
        const reconciled = reconcileApproved(published, validateMetadata(state.approved), state.baseline ? validateMetadata(state.baseline) : empty());
        approved = reconciled.approved;
        const knownIds = new Set(photos.map((photo) => String(photo.id)));
        for (const id of state.conflicts || []) if (knownIds.has(id)) conflicts.add(id);
        for (const conflict of reconciled.conflicts) {
          if (!knownIds.has(conflict.id)) continue;
          conflicts.add(conflict.id);
          if (!drafts.photos[conflict.id]) drafts.photos[conflict.id] = conflict.local || {};
        }
        if (conflicts.size) savedWarning = 'Published tags changed while you were working. Review the marked photos before downloading; the latest published additions are kept until you choose.';
      } catch {
        savedWarning = 'Saved tagging data could not be restored. Published additions are loaded; restore a backup tags.json if you have one.';
      }
    }
  } catch (error) {
    status(`Could not open tagging: ${error.message}`, true);
    const retry = document.createElement('button');
    retry.className = 'adm-btn'; retry.textContent = 'Try again';
    retry.addEventListener('click', () => location.reload());
    container.append(retry);
    return { destroy() { disposed = true; container.replaceChildren(); } };
  }
  if (disposed) return;
  const byId = new Map(photos.map((photo) => [String(photo.id), photo]));
  const save = () => {
    try {
      localStorage.setItem(storageKey, JSON.stringify({ approved, drafts, baseline: published, conflicts: [...conflicts] }));
      $('[data-tag-storage-warning]').textContent = '';
    } catch {
      $('[data-tag-storage-warning]').textContent = 'This browser could not save your work. Download approved tags.json before leaving.';
    }
  };
  function updateCounts() {
    $('[data-tag-count]').textContent = `${count(approved)} photos have approved additions. ${count(drafts)} photos have drafts awaiting review.`;
    if (conflicts.size) $('[data-tag-count]').textContent += ` ${conflicts.size} changed published photos need a decision before download.`;
    $('[data-tag-export]').disabled = conflicts.size > 0;
  }
  function renderOptions() {
    const query = $('#tagFilter').value.trim().toLocaleLowerCase();
    const visible = photos.filter((photo) => `${photo.title} ${photo.year || ''} ${photo.downloadName || ''} ${photo.id}`.toLocaleLowerCase().includes(query));
    $('#tagPhoto').replaceChildren(...visible.map((photo) => {
      const option = document.createElement('option');
      option.value = String(photo.id);
      option.textContent = `${conflicts.has(String(photo.id)) ? 'Review changes · ' : ''}${photo.year ? `${photo.year} · ` : ''}${photo.title}`;
      return option;
    }));
    if (visible.some((photo) => String(photo.id) === currentId)) $('#tagPhoto').value = currentId;
    currentId = $('#tagPhoto').value;
    $('[data-tag-editor]').hidden = !currentId;
    if (!currentId) status('No photos match that search.');
    else renderPhoto();
  }
  function renderPhoto() {
    const photo = byId.get(currentId);
    if (!photo) return;
    const values = drafts.photos[currentId] || approved.photos[currentId] || {};
    $('#tagLabels').value = (values.tags || []).join(', ');
    $('#tagPeople').value = (values.people || []).join(', ');
    const hasCaption = Object.hasOwn(values, 'caption');
    $('#tagReplaceCaption').checked = hasCaption;
    $('#tagCaption').disabled = !hasCaption;
    $('#tagCaption').value = hasCaption ? values.caption : photo.caption || '';
    const img = $('[data-tag-image]');
    img.alt = photo.title;
    img.onerror = () => {
      img.onerror = null;
      if (photo.thumbFallback || photo.fallback) img.src = new URL(photo.thumbFallback || photo.fallback, ROOT);
    };
    img.src = new URL(photo.thumb || photo.src, ROOT);
    $('[data-tag-source]').textContent = photo.caption ? `Original caption: ${photo.caption}` : 'No original caption yet.';
    const originals = [photo.tags?.length ? `Tags: ${photo.tags.join(', ')}` : '', photo.people?.length ? `People: ${photo.people.join(', ')}` : ''].filter(Boolean);
    $('[data-tag-original]').textContent = originals.length ? `From the original description · ${originals.join(' · ')}` : 'Add tags or people to make this photo easier to find.';
    updateReviewState();
  }
  function updateReviewState() {
    $('[data-tag-review-state]').textContent = conflicts.has(currentId) ? 'Published additions changed. Approve your draft to replace them, discard the draft to keep the published additions, or remove additions.' : drafts.photos[currentId] ? 'Draft · review and approve when ready.' : approved.photos[currentId] ? 'Approved · included in your next download.' : 'No additions approved yet.';
    updateCounts();
  }
  function readFields() {
    const fields = { tags: uniqueLabels($('#tagLabels').value), people: uniqueLabels($('#tagPeople').value) };
    if ($('#tagReplaceCaption').checked) fields.caption = $('#tagCaption').value.trim();
    return fields;
  }
  function editDraft() {
    if (!currentId) return;
    drafts.photos[currentId] = readFields();
    save(); updateReviewState();
  }
  $('[data-tag-form]').addEventListener('input', editDraft);
  $('#tagReplaceCaption').addEventListener('change', () => {
    $('#tagCaption').disabled = !$('#tagReplaceCaption').checked;
    if ($('#tagReplaceCaption').checked) $('#tagPeople').value = uniqueLabels([...uniqueLabels($('#tagPeople').value), ...(byId.get(currentId)?.people || [])]).join(', ');
    editDraft();
  });
  $('#tagPhoto').addEventListener('change', () => { currentId = $('#tagPhoto').value; renderPhoto(); });
  $('#tagFilter').addEventListener('input', renderOptions);
  $('[data-tag-form]').addEventListener('submit', (event) => {
    event.preventDefault();
    approved.photos[currentId] = readFields();
    delete drafts.photos[currentId];
    conflicts.delete(currentId);
    save(); updateReviewState(); status('Approved for your next download. The live album has not changed yet.');
  });
  $('[data-tag-next]').addEventListener('click', () => {
    const select = $('#tagPhoto');
    select.selectedIndex = (select.selectedIndex + 1) % select.options.length;
    currentId = select.value; renderPhoto(); select.focus();
  });
  $('[data-tag-reset]').addEventListener('click', () => {
    delete drafts.photos[currentId]; conflicts.delete(currentId); save(); renderPhoto(); status('Draft discarded. Approved additions are kept.');
  });
  $('[data-tag-remove]').addEventListener('click', () => {
    delete approved.photos[currentId]; delete drafts.photos[currentId];
    conflicts.delete(currentId);
    save(); renderPhoto(); status('Removed from your next download. Original photo descriptions are kept.');
  });
  async function importFile(input, isApproved) {
    const file = input.files?.[0];
    if (!file) return;
    try {
      if (file.size > MAX_IMPORT) throw new Error('Choose a JSON file smaller than 5 MB.');
      const data = validateMetadata(JSON.parse(await file.text()));
      if (disposed) return;
      let added = 0; let skipped = 0;
      for (const [id, item] of Object.entries(data.photos)) {
        if (!byId.has(id)) { skipped++; continue; }
        if (isApproved) { approved.photos[id] = item; conflicts.delete(id); }
        else {
          const previous = drafts.photos[id] || approved.photos[id] || {};
          const retainedNames = Object.hasOwn(item, 'caption') && !Object.hasOwn(item, 'people') ? byId.get(id).people || [] : [];
          drafts.photos[id] = { ...previous, ...item, tags: uniqueLabels([...(previous.tags || []), ...(item.tags || [])]), people: uniqueLabels([...(previous.people || []), ...(item.people || []), ...retainedNames]) };
        }
        added++;
      }
      save(); renderPhoto();
      status(`${added} ${isApproved ? 'approved additions restored' : 'drafts imported for review'}.${skipped ? ` ${skipped} unknown photo IDs skipped.` : ''}`);
    } catch (error) { status(`Could not import that file: ${error.message}`, true); }
    input.value = '';
  }
  $('#tagDraftFile').addEventListener('change', (event) => importFile(event.target, false));
  $('#tagApprovedFile').addEventListener('change', (event) => importFile(event.target, true));
  function downloadJSON(value, filename) {
    const url = URL.createObjectURL(new Blob([`${JSON.stringify(value, null, 2)}\n`], { type: 'application/json' }));
    const link = document.createElement('a'); link.href = url; link.download = filename;
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  $('[data-tag-ai-list]').addEventListener('click', () => {
    const candidates = photos.flatMap((photo) => {
      let filename = photo.downloadName;
      if (!filename && CONFIG.source !== 'drive') {
        try { filename = decodeURIComponent(new URL(photo.download || photo.src, ROOT).pathname.split('/').pop()); } catch {}
      }
      if (!filename || /[\\/]/.test(filename) || !/\.(jpe?g|png)$/i.test(filename)) return [];
      return [{ id: photo.id, path: filename, title: photo.title, caption: photo.caption || '' }];
    });
    const names = new Map();
    for (const photo of candidates) names.set(photo.path.toLocaleLowerCase(), (names.get(photo.path.toLocaleLowerCase()) || 0) + 1);
    const mapped = candidates.filter((photo) => names.get(photo.path.toLocaleLowerCase()) === 1);
    const duplicates = candidates.length - mapped.length;
    if (!mapped.length) { status(duplicates ? 'The original file names are duplicated. Give each scan a unique name before making an AI photo list.' : 'No JPG or PNG original file names are available. Add scans to the album first.', true); return; }
    downloadJSON({ photos: mapped }, 'photo-list.json');
    status(`Downloaded a list of ${mapped.length} photos.${candidates.length !== photos.length ? ' Files without a JPG or PNG original name were skipped.' : ''}${duplicates ? ` ${duplicates} photos with duplicate file names were skipped; give each original a unique name first.` : ''} Put it beside the matching originals before running the tagging tool.`);
  });
  $('[data-tag-export]').addEventListener('click', async () => {
    if (conflicts.size) { status('Resolve the changed published photos before downloading.', true); return; }
    $('[data-tag-export]').disabled = true;
    try {
      if (CONFIG.metadataUrl !== false && CONFIG.metadataUrl !== null) {
        status('Checking for newly published additions before downloading…');
        const response = await fetch(new URL(CONFIG.metadataUrl || 'data/tags.json', ROOT), { cache: 'no-store' });
        if (!response.ok && response.status !== 404) throw new Error('The latest published tags could not be checked. Try the download again when the connection returns.');
        const latest = response.ok ? copy(validateMetadata(await response.json())) : empty();
        if (disposed) return;
        const reconciled = reconcileApproved(latest, approved, published);
        published = latest;
        approved = reconciled.approved;
        for (const conflict of reconciled.conflicts) {
          if (!byId.has(conflict.id)) continue;
          conflicts.add(conflict.id);
          if (!drafts.photos[conflict.id]) drafts.photos[conflict.id] = conflict.local || {};
        }
        save(); renderOptions();
        if (conflicts.size) { status('Published tags changed. Review the marked photos before downloading; discard a draft to keep the latest published additions.', true); return; }
      }
      downloadJSON(approved, 'tags.json');
      status('Downloaded approved tags.json. Publish this file to update the album.');
    } catch (error) {
      status(`Could not download safely: ${error.message}`, true);
    } finally {
      if (!disposed) updateCounts();
    }
  });
  $('[data-tag-clear]').addEventListener('click', () => {
    if (!confirm('Clear drafts and unpublished approvals on this browser? Download your approved file first if you want to keep it.')) return;
    approved = copy(published); drafts = empty();
    conflicts.clear();
    try { localStorage.removeItem(storageKey); } catch {}
    faces?.destroy?.(); faces = undefined;
    $('[data-tag-face-tool]').replaceChildren(); $('[data-tag-faces]').open = false;
    renderPhoto(); status('Local tagging data cleared. Published additions are still available.');
  });
  $('[data-tag-faces]').addEventListener('toggle', async () => {
    if (!$('[data-tag-faces]').open || faces) return;
    faces = { loading: true };
    const faceContainer = $('[data-tag-face-tool]');
    try {
      const { mountFaceTool } = await import('./faces.js');
      if (disposed) return;
      faces = await mountFaceTool(faceContainer, { photos, onApprove: (named) => {
        if (disposed) return;
        for (const [id, additions] of Object.entries(named)) {
          if (!byId.has(id)) continue;
          const previous = drafts.photos[id] || approved.photos[id] || {};
          drafts.photos[id] = { ...previous, people: uniqueLabels([...(previous.people || []), ...(additions.people || [])]) };
        }
        save(); renderPhoto(); status('Names added to photo drafts. Review each photo before approving.');
      } });
    } catch (error) {
      faces = undefined; faceContainer.textContent = `Could not open face grouping: ${error.message}`;
    }
  });
  $('[data-tag-controls]').hidden = false;
  renderOptions(); status(savedWarning || 'Ready. Choose a photo, or import suggestions to review.', !!savedWarning);
  return { destroy() { disposed = true; faces?.destroy?.(); container.replaceChildren(); } };
}
