// Bootstrap paths, invite verification, and recovery defaults for the album.
// Family settings entered in the admin page are saved on this device.
// This browser uses its saved settings before the published album defaults.
import { loadSettings, settingsFromConfig } from './settings.js';

const BOOTSTRAP_CONFIG = {
  // Shown on the welcome page and the browser tab.
  title: 'Our Life in Pictures',
  // Names on the album. Keep it to the names you use.
  honorees: [
    { name: 'Kevin', years: '' },
    { name: 'Lee', years: '' },
  ],
  // One or two sentences. Shown under the names on the welcome page.
  dedication:
    "The places we've been, the people we love, and the moments we want to keep.",
  // Who keeps the album. Used in "Ask Lauren for your link" and "Made by Lauren".
  keeper: 'Lauren',
  // Who maintains the site (named on the admin page for help).
  helper: 'Kevin',

  // Names that appear in captions. The app finds them in photo titles and
  // captions automatically, so nobody has to tag anything by hand.
  people: ['Kevin', 'Lee'],

  // true while the sample photos are showing. Adds a small "Sample photos" note.
  sample: false,

  // ---- where the photos come from ---------------------------------------
  // 'manifest' → data/library.json in this folder (the sample set).
  // 'drive'    → a Google Drive folder shared "Anyone with the link can view".
  //              Subfolders become chapters; the file's Drive description is the
  //              caption; a year at the start of the file name dates the photo.
  source: 'drive',
  manifestUrl: 'data/library.json',
  // Approved tags, names and caption edits exported from the admin review tool.
  // Set false to use only the photo source's descriptions. Never put drafts here.
  metadataUrl: 'data/tags.json',
  drive: {
    // A Google API key restricted to the Drive API and to this site's address
    // (HTTP referrer custom.polecat.live/*). Safe to publish once restricted.
    apiKey: 'AIzaSyASZFkUdwLnHwtjxm3O-VcXybTVZIOEyY8',
    // The ID at the end of the folder's share link: drive.google.com/drive/folders/<ID>
    folderId: '16sNwmbN-tsJHJ6jCAamgFCG3MKpdZ06E',
  },

  // ---- invite links -------------------------------------------------------
  // Invite-only: visitors need a personal link (…/memories/?invite=…) once per
  // device. The admin key that MAKES links is never stored in this repo.
  // NOTE: this is a polite front door, not a vault — the files are public.
  access: {
    enabled: true,
    prefix: 'memories', // localStorage namespace
    publicKey:
      'MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE+y0OpgS9uUWUZ6EMC0jj5/2hcLpgEcZpf15SAfYekWXQYzOuemt7B9XvSFUs0p/UVmMc9H7JDiUp92OoQvbbSQ==',
    revoked: [], // invite IDs (jti) to turn off, e.g. ['a1B2c3D4']
  },

  // Skin shown on first visit. Visitors can change it; their choice is kept.
  defaultSkin: 'heirloom',
};


export const DEFAULT_SETTINGS = settingsFromConfig(BOOTSTRAP_CONFIG);
// Node-based tools use the bootstrap without trying to fetch a file:// URL.
export const SETTINGS_STATE = typeof window !== 'undefined'
  ? await loadSettings(DEFAULT_SETTINGS)
  : { document: { version: 1, revision: 'bootstrap', settings: DEFAULT_SETTINGS }, source: 'defaults', localStatus: 'none' };
export const CONFIG = { ...BOOTSTRAP_CONFIG, ...SETTINGS_STATE.document.settings };
