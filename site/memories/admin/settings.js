import { CONFIG, SETTINGS_STATE } from '../js/config.js';
import { settingsFromConfig, validateSettings, normalizeFolderId, saveLocalSettings } from '../js/settings.js';
import { SKINS } from '../js/skins.js';
import { loadDrive } from '../js/sources/drive.js';

const labels = text => text.split(/[,;\n]+/).map(value => value.trim()).filter(Boolean);
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

/** Personal settings stay in this browser. Saving never writes to a server. */
export function mountSettings(container, { onSave = () => {} } = {}) {
  let disposed = false, busy = false, rowNumber = 0;
  let savedSettings = settingsFromConfig(CONFIG);
  const currentSkin = document.documentElement.dataset.skin;
  if (SKINS.some(skin => skin.id === currentSkin)) savedSettings.defaultSkin = currentSkin;
  container.innerHTML = `
    <p>Make the album your own.</p>
    <p class="adm-small adm-muted">These settings are saved in this browser on this device.</p>
    <form id="albumSettingsForm" novalidate>
      <fieldset class="settings-fields">
        <legend class="sr">Album settings</legend>
        <label class="adm-label" for="albumTitleInput">Album title</label>
        <input class="adm-field" id="albumTitleInput" type="text" maxlength="120" required>
        <h3 class="settings-heading">Names on the album</h3>
        <div data-settings-honorees></div>
        <button class="adm-btn" data-settings-add-person type="button">Add a person</button>
        <label class="adm-label" for="albumDedicationInput">Welcome message</label>
        <textarea class="adm-field" id="albumDedicationInput" rows="4" maxlength="4000"></textarea>
        <label class="adm-label" for="albumSourceInput">Photos</label>
        <select class="adm-field" id="albumSourceInput"><option value="drive">My Google Drive photos</option><option value="manifest">Sample photos</option></select>
        <div data-settings-drive>
          <label class="adm-label" for="albumFolderInput">Photo folder</label>
          <input class="adm-field" id="albumFolderInput" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="Paste your folder link">
          <button class="adm-btn" data-settings-check-drive type="button">Check folder</button>
          <p data-settings-drive-status class="adm-muted" role="status" aria-live="polite"></p>
          <ul data-settings-drive-chapters class="adm-chapters"></ul>
          <details class="settings-help">
            <summary>Connection details</summary>
            <label class="adm-label" for="albumApiKeyInput">Connection key</label>
            <input class="adm-field" id="albumApiKeyInput" type="password" autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="albumApiKeyHelp">
            <p class="adm-small adm-muted" id="albumApiKeyHelp">Use the key provided for this album.</p>
          </details>
        </div>
        <label class="adm-label" for="albumSkinInput">Look</label>
        <select class="adm-field" id="albumSkinInput"></select>
        <details class="settings-help">
          <summary>More settings</summary>
          <div class="settings-pair">
            <div><label class="adm-label" for="albumKeeperInput">Album keeper</label><input class="adm-field" id="albumKeeperInput" type="text" maxlength="120" required></div>
            <div><label class="adm-label" for="albumHelperInput">Person who helps with the album</label><input class="adm-field" id="albumHelperInput" type="text" maxlength="120" required></div>
          </div>
          <label class="adm-label" for="albumPeopleInput">Names to find in captions</label>
          <textarea class="adm-field" id="albumPeopleInput" rows="3" aria-describedby="albumPeopleHelp"></textarea>
          <p class="adm-small adm-muted" id="albumPeopleHelp">Separate names with commas or put one on each line.</p>
        </details>
        <div class="settings-actions">
          <button class="adm-btn adm-primary" id="settingsSave" type="submit">Save</button>
          <a class="adm-btn" id="settingsOpenAlbum" href="../">Open the album</a>
        </div>
      </fieldset>
    </form>
    <p data-settings-status class="adm-muted" role="status" aria-live="polite"></p>`;
  const $ = selector => container.querySelector(selector);
  const status = (message, error = false) => {
    if (disposed) return;
    $('[data-settings-status]').textContent = message;
    $('[data-settings-status]').className = error ? 'adm-error' : 'adm-muted';
  };
  const friendly = error => /API|AIza|browser key|publishing|document|schema/i.test(error?.message || '')
    ? 'Check the connection key in Connection details.'
    : error?.message || 'The settings could not be saved. Please try again.';
  for (const skin of SKINS) {
    const option = document.createElement('option'); option.value = skin.id; option.textContent = skin.name;
    $('#albumSkinInput').append(option);
  }
  function setBusy(value) {
    busy = value;
    $('.settings-fields').disabled = value;
  }
  function clearFolderCheck() {
    $('[data-settings-drive-status]').textContent = '';
    $('[data-settings-drive-chapters]').replaceChildren();
  }
  function updateSource() { $('[data-settings-drive]').hidden = $('#albumSourceInput').value !== 'drive'; clearFolderCheck(); }
  function updatePeopleButtons() {
    const rows = [...container.querySelectorAll('[data-settings-person]')];
    $('[data-settings-add-person]').disabled = rows.length >= 8;
    rows.forEach(row => { row.querySelector('button').disabled = rows.length <= 1; });
  }
  function addPerson(person = { name: '', years: '' }) {
    const number = ++rowNumber;
    const row = document.createElement('div'); row.className = 'settings-person'; row.dataset.settingsPerson = '';
    const addField = (labelText, field, value, limit) => {
      const wrap = document.createElement('div');
      const label = document.createElement('label'); label.className = 'adm-label'; label.htmlFor = `honoree-${field}-${number}`; label.textContent = labelText;
      const input = document.createElement('input'); input.className = 'adm-field'; input.id = label.htmlFor; input.type = 'text'; input.maxLength = limit; input.value = value;
      input.dataset[field === 'name' ? 'honoreeName' : 'honoreeYears'] = '';
      wrap.append(label, input); row.append(wrap);
    };
    addField('Name', 'name', person.name, 120); addField('Dates or a short note (optional)', 'years', person.years, 100);
    const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'adm-btn adm-quiet'; remove.textContent = 'Remove person';
    remove.addEventListener('click', () => { row.remove(); updatePeopleButtons(); status('You have unsaved changes.'); });
    row.append(remove); $('[data-settings-honorees]').append(row); updatePeopleButtons();
  }
  function fill(settings) {
    $('#albumTitleInput').value = settings.title;
    $('#albumDedicationInput').value = settings.dedication;
    $('#albumKeeperInput').value = settings.keeper;
    $('#albumHelperInput').value = settings.helper;
    $('#albumPeopleInput').value = settings.people.join('\n');
    $('#albumSourceInput').value = settings.source;
    $('#albumApiKeyInput').value = settings.drive.apiKey;
    $('#albumFolderInput').value = settings.drive.folderId;
    $('#albumSkinInput').value = settings.defaultSkin;
    $('[data-settings-honorees]').replaceChildren(); settings.honorees.forEach(addPerson);
    updateSource();
  }
  function read() {
    const source = $('#albumSourceInput').value;
    return validateSettings({
      title: $('#albumTitleInput').value, dedication: $('#albumDedicationInput').value,
      keeper: $('#albumKeeperInput').value, helper: $('#albumHelperInput').value,
      honorees: [...container.querySelectorAll('[data-settings-person]')].map(row => ({ name: row.querySelector('[data-honoree-name]').value, years: row.querySelector('[data-honoree-years]').value })),
      people: labels($('#albumPeopleInput').value), source, sample: source === 'manifest',
      drive: { apiKey: $('#albumApiKeyInput').value.trim(), folderId: normalizeFolderId($('#albumFolderInput').value) },
      defaultSkin: $('#albumSkinInput').value,
    });
  }
  function applyLook(document) {
    const skin = document.settings.defaultSkin;
    // Keep the chosen light/dark mode and text size when changing the look.
    const key = `${CONFIG.access?.prefix || 'memories'}.prefs`;
    try {
      const previous = JSON.parse(localStorage.getItem(key) || '{}');
      localStorage.setItem(key, JSON.stringify({ ...previous, skin, settingsRevision: document.revision }));
    } catch { /* The settings themselves are already saved and take priority on next open. */ }
    window.document.documentElement.dataset.skin = skin;
  }
  $('[data-settings-add-person]').addEventListener('click', () => {
    addPerson(); $('[data-settings-honorees]').lastElementChild.querySelector('input').focus(); status('You have unsaved changes.');
  });
  $('#albumSourceInput').addEventListener('change', updateSource);
  $('#albumFolderInput').addEventListener('input', clearFolderCheck);
  $('#albumApiKeyInput').addEventListener('input', clearFolderCheck);
  $('#albumSettingsForm').addEventListener('input', () => status('You have unsaved changes.'));
  $('[data-settings-check-drive]').addEventListener('click', async () => {
    if (busy) return;
    let settings;
    try { settings = read(); } catch (error) { status(friendly(error), true); return; }
    setBusy(true);
    const output = $('[data-settings-drive-status]');
    output.className = 'adm-muted'; output.textContent = 'Opening the folder…';
    $('[data-settings-drive-chapters]').replaceChildren();
    try {
      const library = await loadDrive(settings.drive);
      if (disposed) return;
      output.textContent = `Found ${library.chapters.length} chapters and ${library.photos.length} photos.`;
      for (const chapter of library.chapters) {
        const li = document.createElement('li');
        const title = document.createElement('span'); title.textContent = chapter.title;
        const count = document.createElement('span'); count.className = 'adm-muted'; count.textContent = `${library.photos.filter(photo => photo.chapter === chapter.id).length} photos`;
        li.append(title, count); $('[data-settings-drive-chapters]').append(li);
      }
    } catch {
      if (!disposed) { output.className = 'adm-error'; output.textContent = 'The folder could not be opened. Check its link, sharing, and connection key.'; }
    } finally { if (!disposed) setBusy(false); }
  });
  $('#albumSettingsForm').addEventListener('submit', event => {
    event.preventDefault(); if (busy) return;
    try {
      const settings = read();
      const saved = saveLocalSettings(settings);
      const libraryChanged = settings.source !== savedSettings.source || !same(settings.drive, savedSettings.drive) || !same(settings.people, savedSettings.people);
      savedSettings = saved.settings;
      Object.assign(CONFIG, saved.settings);
      applyLook(saved);
      fill(saved.settings);
      status('Saved on this device.');
      try { onSave(saved, { libraryChanged }); }
      catch { status('Saved on this device. Reopen the album to use your settings.'); }
    } catch (error) { status(friendly(error), true); }
  });
  fill(savedSettings);
  if (SETTINGS_STATE.localStatus === 'invalid') status('Your previous settings could not be read. Check these settings and save them again.', true);
  return { destroy() { if (disposed) return; disposed = true; container.replaceChildren(); } };
}
