import { CONFIG } from '../js/config.js';
import { SETTINGS_URL, settingsFromConfig, validateSettings, validateSettingsDocument, normalizeFolderId } from '../js/settings.js';
import { SKINS } from '../js/skins.js';
import { loadDrive } from '../js/sources/drive.js';
import { publisher } from './publishing.js';

const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const labels = (text) => text.split(/[,;\n]+/).map(value => value.trim()).filter(Boolean);

/** Shared settings are saved to the album's publishing repository, never only
 * to this browser. The separate publishing token is kept in memory by publisher. */
export function mountSettings(container) {
  let disposed = false;
  let busy = false;
  let current = null;
  let rowNumber = 0;
  let checkedDrive = '';
  container.innerHTML = `
    <p>Change the family names, dedication, photo folder, and starting look here. Saving updates the album for everyone after it finishes publishing.</p>
    <div class="settings-publishing">
      <h3>Publishing access</h3>
      <p class="adm-small adm-muted">Your admin key opens these tools. To save shared changes, connect publishing for this session. The publishing token is forgotten when you lock this device or close this page.</p>
      <details class="settings-help"><summary>Set up publishing access</summary>
        <p>Create a <a href="https://github.com/settings/personal-access-tokens/new" target="_blank" rel="noopener noreferrer">fine-grained GitHub token</a> with access to only <b>kevinrhaas/custom</b>. Give it <b>Contents: Read and write</b>, and choose an expiration. Keep it in your password manager.</p>
        <p>No file editing is needed. This page saves your settings and starts the normal album publishing process.</p>
      </details>
      <div data-publishing-connect>
        <label class="adm-label" for="publishingToken">Publishing token</label>
        <input class="adm-field" id="publishingToken" type="password" autocomplete="off" autocapitalize="off" spellcheck="false">
        <button class="adm-btn" id="publishingConnect" type="button">Connect publishing</button>
      </div>
      <div data-publishing-connected hidden>
        <p class="adm-ok">Publishing is connected for this session.</p>
        <button class="adm-btn adm-quiet" id="publishingDisconnect" type="button">Disconnect publishing</button>
      </div>
    </div>
    <p data-settings-status class="adm-muted" role="status" aria-live="polite">Connect publishing to edit and save the shared settings.</p>
    <button class="adm-btn" id="settingsReload" type="button" hidden>Load latest saved settings</button>
    <form id="albumSettingsForm" novalidate>
      <fieldset class="settings-fields" disabled>
        <legend class="sr">Album settings</legend>
        <label class="adm-label" for="albumTitleInput">Album title</label>
        <input class="adm-field" id="albumTitleInput" type="text" maxlength="120" required>
        <h3 class="settings-heading">People the album remembers</h3>
        <div data-settings-honorees></div>
        <button class="adm-btn" data-settings-add-person type="button">Add a person</button>
        <label class="adm-label" for="albumDedicationInput">Dedication</label>
        <textarea class="adm-field" id="albumDedicationInput" rows="4" maxlength="4000"></textarea>
        <div class="settings-pair">
          <div><label class="adm-label" for="albumKeeperInput">Album keeper</label><input class="adm-field" id="albumKeeperInput" type="text" maxlength="120" required></div>
          <div><label class="adm-label" for="albumHelperInput">Person who helps with the site</label><input class="adm-field" id="albumHelperInput" type="text" maxlength="120" required></div>
        </div>
        <label class="adm-label" for="albumPeopleInput">Names to find in captions</label>
        <textarea class="adm-field" id="albumPeopleInput" rows="3" aria-describedby="albumPeopleHelp"></textarea>
        <p class="adm-small adm-muted" id="albumPeopleHelp">Separate names with commas or put one on each line. These names become searchable when they appear in a caption.</p>
        <label class="adm-label" for="albumSourceInput">Photo source</label>
        <select class="adm-field" id="albumSourceInput"><option value="drive">Shared Google Drive folder</option><option value="manifest">Sample photos</option></select>
        <div data-settings-drive>
          <label class="adm-label" for="albumFolderInput">Drive folder link or ID</label>
          <input class="adm-field" id="albumFolderInput" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="https://drive.google.com/drive/folders/…">
          <label class="adm-label" for="albumApiKeyInput">Google Drive API key</label>
          <input class="adm-field" id="albumApiKeyInput" type="text" autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="albumApiKeyHelp">
          <p class="adm-small adm-muted" id="albumApiKeyHelp">This browser key is public. Restrict it to the Google Drive API and <b>https://custom.polecat.live/*</b>. Never enter an AI key or publishing token here.</p>
          <button class="adm-btn" data-settings-check-drive type="button">Check the folder</button>
          <p data-settings-drive-status class="adm-muted" role="status" aria-live="polite"></p>
          <ul data-settings-drive-chapters class="adm-chapters"></ul>
        </div>
        <label class="adm-label" for="albumSkinInput">Starting look for new visitors</label>
        <select class="adm-field" id="albumSkinInput"></select>
        <p class="adm-small adm-muted">Visitors can still choose their own look and text size.</p>
        <button class="adm-btn adm-primary" id="settingsSave" type="submit">Save album settings</button>
      </fieldset>
    </form>
    <button class="adm-btn" id="settingsCheckLive" type="button" hidden>Check published version</button>
    <p class="adm-small adm-muted" data-settings-live-help hidden>Once published, reopen the album to see these settings. Reload this admin page before tagging photos from a different folder. Other visitors receive changes when they refresh.</p>`;
  const $ = selector => container.querySelector(selector);
  const status = (message, error = false) => {
    if (disposed) return;
    $('[data-settings-status]').textContent = message;
    $('[data-settings-status]').className = error ? 'adm-error' : 'adm-muted';
  };
  for (const skin of SKINS) {
    const option = document.createElement('option'); option.value = skin.id; option.textContent = skin.name;
    $('#albumSkinInput').append(option);
  }
  function setBusy(value) {
    busy = value;
    $('.settings-fields').disabled = value || !publisher.isConnected();
    $('#publishingConnect').disabled = value;
    $('#publishingDisconnect').disabled = value;
    $('#settingsReload').disabled = value;
    $('#settingsCheckLive').disabled = value;
    $('#publishingToken').disabled = value;
  }
  function updateConnection() {
    const connected = publisher.isConnected();
    $('[data-publishing-connect]').hidden = connected;
    $('[data-publishing-connected]').hidden = !connected;
    setBusy(busy);
  }
  function updateSource() { $('[data-settings-drive]').hidden = $('#albumSourceInput').value !== 'drive'; }
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
    addField('Name', 'name', person.name, 120); addField('Years (optional)', 'years', person.years, 100);
    const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'adm-btn adm-quiet'; remove.textContent = 'Remove person';
    remove.addEventListener('click', () => { row.remove(); updatePeopleButtons(); });
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
    $('[data-settings-drive-status]').textContent = ''; $('[data-settings-drive-chapters]').replaceChildren();
    checkedDrive = ''; updateSource();
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
  function accept(snapshot) {
    current = { ...snapshot, document: validateSettingsDocument(snapshot.document) };
    fill(current.document.settings); $('#settingsReload').hidden = true;
    $('#settingsCheckLive').hidden = false; $('[data-settings-live-help]').hidden = false;
  }
  async function checkDrive(settings) {
    const driveStatus = $('[data-settings-drive-status]');
    driveStatus.className = 'adm-muted'; driveStatus.textContent = 'Looking in the folder…';
    $('[data-settings-drive-chapters]').replaceChildren();
    try {
      const library = await loadDrive(settings.drive);
      if (disposed) return false;
      checkedDrive = JSON.stringify(settings.drive);
      driveStatus.textContent = `Found ${library.chapters.length} chapters and ${library.photos.length} photos.`;
      for (const chapter of library.chapters) {
        const li = document.createElement('li');
        const title = document.createElement('span'); title.textContent = chapter.title;
        const count = document.createElement('span'); count.className = 'adm-muted'; count.textContent = `${library.photos.filter(photo => photo.chapter === chapter.id).length} photos`;
        li.append(title, count); $('[data-settings-drive-chapters]').append(li);
      }
      return true;
    } catch (error) {
      if (!disposed) { driveStatus.className = 'adm-error'; driveStatus.textContent = error.friendly ? error.message : 'The Drive folder could not be checked. Verify the folder is shared and the key allows this website.'; }
      return false;
    }
  }
  $('#publishingConnect').addEventListener('click', async () => {
    if (busy) return;
    const token = $('#publishingToken').value.trim(); $('#publishingToken').value = '';
    if (!token) { status('Enter your publishing token first.', true); $('#publishingToken').focus(); return; }
    setBusy(true); status('Connecting to the saved album settings…');
    try {
      const snapshot = await publisher.connect(token);
      if (disposed) { publisher.disconnect(); return; }
      accept(snapshot); status('Connected. Edit the settings below, then save them for everyone.');
    } catch (error) { status(error.message || 'Publishing could not connect. Check the token and try again.', true); }
    finally { if (!disposed) { setBusy(false); updateConnection(); } }
  });
  $('#publishingDisconnect').addEventListener('click', () => {
    publisher.disconnect(); current = null; $('#publishingToken').value = '';
    $('#settingsCheckLive').hidden = true; $('[data-settings-live-help]').hidden = true; $('#settingsReload').hidden = true;
    updateConnection(); status('Publishing disconnected. Unsaved edits have not changed the album.');
  });
  $('[data-settings-add-person]').addEventListener('click', () => { addPerson(); $('[data-settings-honorees]').lastElementChild.querySelector('input').focus(); });
  $('#albumSourceInput').addEventListener('change', updateSource);
  $('[data-settings-check-drive]').addEventListener('click', async () => {
    if (busy) return;
    let settings;
    try { settings = read(); } catch (error) { status(error.message, true); return; }
    setBusy(true);
    try { await checkDrive(settings); } finally { if (!disposed) setBusy(false); }
  });
  $('#albumSettingsForm').addEventListener('input', () => {
    if (current && !busy) status('You have unsaved changes. Save album settings to share them with everyone.');
  });
  $('#albumSettingsForm').addEventListener('submit', async event => {
    event.preventDefault(); if (busy || !current || !publisher.isConnected()) return;
    let settings;
    try { settings = read(); } catch (error) { status(error.message, true); return; }
    if (same(settings, current.document.settings)) { status('These settings are already saved.'); return; }
    setBusy(true); status('Checking the settings…');
    try {
      const changedDrive = current.document.settings.source !== 'drive' || !same(settings.drive, current.document.settings.drive);
      if (settings.source === 'drive' && changedDrive && checkedDrive !== JSON.stringify(settings.drive)) {
        if (!await checkDrive(settings)) { status('The new Drive folder could not be verified. Settings have not been saved.', true); return; }
      }
      if (disposed) return;
      const document = validateSettingsDocument({ version: 1, revision: crypto.randomUUID(), settings });
      status('Saving the shared album settings…');
      const saved = await publisher.save(document, current.sha);
      if (disposed) return;
      accept(saved);
      status('Saved for everyone. The album is publishing; this can take a few minutes. Check the published version below.');
    } catch (error) {
      if (disposed) return;
      status(error.message || 'The settings could not be saved. Try again.', true);
      if (error.code === 'conflict') $('#settingsReload').hidden = false;
    } finally { if (!disposed) { setBusy(false); updateConnection(); } }
  });
  $('#settingsReload').addEventListener('click', async () => {
    if (busy || !publisher.isConnected()) return;
    if (!confirm('Load the latest saved settings? This replaces the unsaved values in this form.')) return;
    setBusy(true);
    try { const latest = await publisher.read(); if (!disposed) { accept(latest); status('Latest saved settings loaded. Make your changes again, then save.'); } }
    catch (error) { status(error.message || 'The latest settings could not be loaded.', true); }
    finally { if (!disposed) setBusy(false); }
  });
  $('#settingsCheckLive').addEventListener('click', async () => {
    if (busy || !current) return;
    try {
      if (!same(read(), current.document.settings)) { status('This form has unsaved changes. Save them before checking the published version.', true); return; }
    } catch { status('This form has unsaved changes. Finish and save them before checking the published version.', true); return; }
    setBusy(true); status('Checking the published album…');
    const controller = new AbortController(); const timeout = setTimeout(() => controller.abort(), 10000);
    try {
      const url = new URL(SETTINGS_URL, location.href); url.searchParams.set('check', crypto.randomUUID());
      const response = await fetch(url, { cache: 'no-store', signal: controller.signal });
      if (!response.ok) throw new Error('The published version could not be checked yet. Try again shortly.');
      const live = validateSettingsDocument(await response.json());
      if (disposed) return;
      status(live.revision === current.document.revision
        ? 'These saved settings are live. Reopen the album to see them.'
        : 'Your settings are saved, but the published album has a different version. If you just saved, publishing may still be running.');
    } catch { status('Your settings are saved. The published version could not be checked; try again shortly.', true); }
    finally { clearTimeout(timeout); if (!disposed) setBusy(false); }
  });
  fill(settingsFromConfig(CONFIG)); updateConnection();
  return { destroy() { if (disposed) return; disposed = true; publisher.disconnect(); const input = $('#publishingToken'); if (input) input.value = ''; container.replaceChildren(); } };
}
