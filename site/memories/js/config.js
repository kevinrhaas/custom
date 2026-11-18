// -----------------------------------------------------------------------
// config.js — the ONE file to edit when making this album someone's own.
//
// Everything family-specific lives here: names, dates, the dedication, who
// hands out invite links, and where the photos come from. The rest of the app
// reads from this object and never hardcodes a name.
// -----------------------------------------------------------------------

export const CONFIG = {
  // Shown on the welcome page and the browser tab.
  title: 'Our Family Album',
  // The people this album remembers. Keep it to the names the family uses.
  honorees: [
    { name: 'Walter Hale', years: '1921 – 2019' },
    { name: 'June Hale', years: '1924 – 2011' },
  ],
  // One or two sentences. Shown under the names on the welcome page.
  dedication:
    'For the grandkids, nieces and nephews: the boxes from the closet, kept safe here so everyone can see them, anytime.',
  // Who keeps the album. Used in "Ask Lauren for your link" and "Made by Lauren".
  keeper: 'Lauren',
  // Who maintains the site (named on the admin page for permanent link changes).
  helper: 'Kevin',

  // Names that appear in captions. The app finds them in photo titles and
  // captions automatically, so nobody has to tag anything by hand.
  people: ['Walter', 'June', 'Margaret', 'Robert', 'Eleanor', 'Grandma Rose', 'Uncle Frank', 'Peggy', 'Danny'],

  // true while the sample photos are showing. Adds a small "Sample photos" note.
  sample: true,

  // ---- where the photos come from ---------------------------------------
  // 'manifest' → data/library.json in this folder (the sample set).
  // 'drive'    → a Google Drive folder shared "Anyone with the link can view".
  //              Subfolders become chapters; the file's Drive description is the
  //              caption; a year at the start of the file name dates the photo.
  source: 'manifest',
  manifestUrl: 'data/library.json',
  drive: {
    // A Google API key restricted to the Drive API and to this site's address
    // (HTTP referrer custom.polecat.live/*). Safe to publish once restricted.
    apiKey: '',
    // The ID at the end of the folder's share link: drive.google.com/drive/folders/<ID>
    folderId: '',
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
