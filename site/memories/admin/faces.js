import { groupFaces, collectPeople, loadFaceModels, inspectLocalPhoto } from './face-engine.js';

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function button(text, action) {
  const node = element('button', text, 'adm-btn');
  node.type = 'button'; node.addEventListener('click', action);
  return node;
}

function normalizedFilename(value) {
  return String(value || '').split(/[\\/]/).pop().toLocaleLowerCase();
}

export function matchPhotoFile(filename, photos) {
  const name = normalizedFilename(filename);
  const candidates = photos.filter(photo => normalizedFilename(photo.filename) === name ||
    normalizedFilename(photo.downloadName) === name || normalizedFilename(photo.src).split('?')[0] === name);
  return candidates.length === 1 ? candidates[0].id : '';
}

/** Names returned here are suggestions for the parent's final metadata review.
 * No face vectors or images are included in the callback or persisted. */
export function mountFaceTool(container, { photos = [], onApprove = () => {} } = {}) {
  let disposed = false, generation = 0, busy = false;
  let files = [], faces = [], groups = [];
  const photoMap = new Map(photos.map(photo => [String(photo.id), photo]));
  const root = element('section', '', 'face-tool');
  const description = element('p', 'Choose copies of your album photos from this device. Face matching happens here in your browser; these copies are never uploaded. Faded prints can produce wrong matches, so check every face before adding a name.');
  const privacy = element('p', 'The face tools download about 7 MB once. Face measurements and crops are kept only while this page is open. Only names you review and save are added to search on this device.', 'face-note');
  const label = element('label', 'Choose JPG, PNG or WebP photos');
  const input = document.createElement('input');
  input.type = 'file'; input.multiple = true; input.accept = 'image/jpeg,image/png,image/webp';
  label.append(input);
  const mapping = element('div', '', 'face-mapping');
  const controls = element('div', '', 'face-actions');
  const start = button('Find faces on this device', run);
  start.disabled = true;
  const cancel = button('Stop', () => { generation++; busy = false; setBusy(false); status.textContent = 'Stopped. Choose Find faces to start again.'; });
  cancel.hidden = true;
  controls.append(start, cancel);
  const status = element('p', '', 'face-status');
  status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
  const errors = element('ul', '', 'face-errors');
  const review = element('div', '', 'face-review');
  const clear = button('Clear face results from this page', () => {
    generation++; busy = false; files = []; faces = []; groups = []; input.value = '';
    mapping.replaceChildren(); review.replaceChildren(); errors.replaceChildren();
    setBusy(false); status.textContent = 'Selected files, face measurements and crops cleared.';
  });
  root.append(description, privacy, label, mapping, controls, status, errors, review, clear);
  container.append(root);

  function setBusy(value) {
    busy = value; input.disabled = value; cancel.hidden = !value;
    start.disabled = value || !files.some(item => item.photoId);
    mapping.querySelectorAll('select').forEach(select => { select.disabled = value; });
  }

  input.addEventListener('change', () => {
    generation++; faces = []; groups = [];
    review.replaceChildren(); errors.replaceChildren(); mapping.replaceChildren();
    files = Array.from(input.files).map(file => ({ file, photoId: matchPhotoFile(file.name, photos) }));
    if (files.length) mapping.append(element('p', 'Match each file to its album photo. Unmatched files are skipped. A photo can be selected only once.'));
    for (const entry of files) {
      const row = element('label', '', 'face-file-row');
      row.append(element('span', entry.file.name));
      const select = document.createElement('select');
      select.setAttribute('aria-label', `Album photo for ${entry.file.name}`);
      const empty = element('option', 'Skip this file'); empty.value = ''; select.append(empty);
      for (const photo of photos) {
        const option = element('option', `${photo.title || photo.filename || photo.id} (${photo.id})`);
        option.value = String(photo.id); select.append(option);
      }
      select.value = entry.photoId;
      select.addEventListener('change', () => { entry.photoId = select.value; setBusy(false); });
      row.append(select); mapping.append(row);
    }
    status.textContent = files.length ? `${files.length} file${files.length === 1 ? '' : 's'} selected. Check the album matches, then find faces.` : '';
    setBusy(false);
  });

  async function run() {
    if (busy || disposed) return;
    const selected = files.filter(item => item.photoId);
    if (new Set(selected.map(item => item.photoId)).size !== selected.length) {
      status.textContent = 'Two files are matched to the same album photo. Choose a different match or skip one.'; return;
    }
    const token = ++generation;
    faces = []; groups = []; review.replaceChildren(); errors.replaceChildren(); setBusy(true);
    status.textContent = 'Loading the face tools. Selected photos stay on this device.';
    try {
      await loadFaceModels();
      for (let i = 0; i < selected.length; i++) {
        if (disposed || token !== generation) return;
        const entry = selected[i];
        status.textContent = `Checking photo ${i + 1} of ${selected.length}: ${entry.file.name}`;
        try {
          const found = await inspectLocalPhoto(entry.file, entry.photoId);
          if (disposed || token !== generation) return;
          faces.push(...found);
          if (!found.length) errors.append(element('li', `${entry.file.name}: no faces found. You can still add names manually in the photo review.`));
        } catch (error) {
          if (disposed || token !== generation) return;
          errors.append(element('li', `${entry.file.name}: ${error.message || 'Could not examine this photo.'}`));
        }
        await new Promise(resolve => setTimeout(resolve, 0));
      }
      if (disposed || token !== generation) return;
      status.textContent = `Found ${faces.length} face${faces.length === 1 ? '' : 's'} in ${selected.length} photo${selected.length === 1 ? '' : 's'}.`;
      if (faces.length) renderReview();
    } catch (error) {
      if (token === generation && !disposed) status.textContent = error.message || 'The face tools could not start.';
    } finally {
      if (token === generation && !disposed) setBusy(false);
    }
  }

  function renderReview() {
    review.replaceChildren();
    const thresholdLabel = element('label', 'How closely should faces match?');
    const threshold = document.createElement('select');
    for (const [value, text] of [['0.42', 'Strict — fewer suggested matches'], ['0.5', 'Balanced'], ['0.58', 'Loose — check carefully']]) {
      const option = element('option', text); option.value = value; threshold.append(option);
    }
    threshold.value = '0.5'; thresholdLabel.append(threshold);
    const groupList = element('div', '', 'face-group-list');
    const approve = button('Add checked names to photo review', () => {
      const names = collectPeople(groups);
      const count = Object.keys(names).length;
      if (!count) { status.textContent = 'Name at least one group or individual face first.'; return; }
      onApprove(names);
      status.textContent = `Names added for ${count} photo${count === 1 ? '' : 's'}. Review each photo, then use Save approved tags to make the names searchable on this device.`;
    });
    review.append(element('h3', 'Check these suggested groups'), element('p', 'Name a group only after checking its faces. To fix a wrong match, enter a different name beside that face, or uncheck it. Blank groups are ignored.'), thresholdLabel, groupList, approve);
    function regroup() {
      // Retain manual decisions by face ID when changing match sensitivity.
      const previous = new Map(groups.flatMap(group => group.faces.map(face => [face.id, { name: face.name || group.name, excluded: face.excluded }])));
      groups = groupFaces(faces, Number(threshold.value)).map(items => ({ name: '', faces: items.map(face => ({ ...face, ...previous.get(face.id) })) }));
      groupList.replaceChildren();
      groups.forEach((group, index) => {
        const section = element('fieldset', '', 'face-group');
        section.append(element('legend', `Suggested group ${index + 1} · ${group.faces.length} face${group.faces.length === 1 ? '' : 's'}`));
        const nameLabel = element('label', 'Name for this group');
        const name = document.createElement('input'); name.type = 'text'; name.maxLength = 100; name.placeholder = 'For example, Kevin';
        name.addEventListener('input', () => { group.name = name.value; }); nameLabel.append(name); section.append(nameLabel);
        const cards = element('div', '', 'face-cards');
        group.faces.forEach(face => {
          const card = element('div', '', 'face-card');
          const img = document.createElement('img'); img.src = face.thumbnail; img.width = 144; img.height = 144;
          img.alt = `Face from ${photoMap.get(face.photoId)?.title || face.photoId}`;
          const includeLabel = element('label', 'Include this face');
          const include = document.createElement('input'); include.type = 'checkbox'; include.checked = !face.excluded;
          include.addEventListener('change', () => { face.excluded = !include.checked; }); includeLabel.prepend(include);
          const individualLabel = element('label', 'Different name for this face (optional)');
          const individual = document.createElement('input'); individual.type = 'text'; individual.maxLength = 100; individual.value = face.name || '';
          individual.addEventListener('input', () => { face.name = individual.value; }); individualLabel.append(individual);
          card.append(img, element('p', photoMap.get(face.photoId)?.title || face.photoId), includeLabel, individualLabel); cards.append(card);
        });
        section.append(cards); groupList.append(section);
      });
    }
    threshold.addEventListener('change', regroup); regroup();
  }

  return { destroy() { disposed = true; generation++; files = []; faces = []; groups = []; root.remove(); } };
}
